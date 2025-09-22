"""
Utilidad para procesar archivos de datos (CSV, JSON, Texto, PDF, Word)
"""

import json
import logging
import os
import io # Importación para manejar archivos en memoria
from google.cloud import storage
import vertexai
from vertexai.generative_models import GenerativeModel
from google.api_core.exceptions import NotFound

# Importaciones adicionales para los nuevos formatos
import PyPDF2
import docx

# Importamos el esquema desde el nuevo archivo
from .schema import data_schema_manager

# Configuración de logging
logger = logging.getLogger(__name__)

# Configuración inicial de Vertex AI y Gemini
PROJECT_ID = os.environ.get("GCP_PROJECT")
LOCATION = os.environ.get("GCP_REGION")

if not PROJECT_ID or not LOCATION:
    logger.error("No se pudieron cargar las variables de entorno GCP_PROJECT o GCP_REGION.")

# Inicializar Vertex AI
vertexai.init(project=PROJECT_ID, location=LOCATION)

# Cargar el modelo de Gemini
model = GenerativeModel("gemini-2.5-flash-lite")

def process_data(bucket_name: str, file_name: str, file_info: dict, text_content: str = None):
    """
    Función principal para procesar archivos de texto o datos.
    Descarga el archivo de Cloud Storage, lo analiza con Gemini y retorna el resultado.

    Args:
        bucket_name (str): El nombre del bucket de Google Cloud Storage.
        file_name (str): El nombre del archivo a procesar.
        file_info (dict): Información del archivo, incluyendo su tipo.
        text_content (str): Texto extraído previamente de la imagen (opcional).
    """
    extracted_text = ""

    # Si el texto ya ha sido proporcionado (desde la API de Vision), lo usamos directamente.
    if text_content:
        extracted_text = text_content
        logger.info(f"Usando el texto extraído de la imagen para el análisis.")
    else:
        # Si no se ha proporcionado texto, descargamos el archivo y lo procesamos.
        try:
            logger.info(f"Procesando archivo de tipo '{file_info['file_type']}' desde el bucket '{bucket_name}'.")

            storage_client = storage.Client()
            bucket = storage_client.bucket(bucket_name)
            blob = bucket.blob(file_name)

            try:
                file_bytes = blob.download_as_bytes()
                logger.info(f"Contenido del archivo '{file_name}' descargado exitosamente.")
            except NotFound as e:
                logger.error(f"Error 404: El archivo '{file_name}' no fue encontrado en el bucket '{bucket_name}'.")
                return None
            except Exception as e:
                logger.error(f"Error desconocido al descargar el archivo '{file_name}': {e}")
                raise

            real_mime_type = file_info.get('real_mime_type')

            if real_mime_type == 'application/pdf':
                pdf_file = io.BytesIO(file_bytes)
                reader = PyPDF2.PdfReader(pdf_file)
                for page in reader.pages:
                    extracted_text += page.extract_text() or ""
            elif real_mime_type in ['application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']:
                doc_file = io.BytesIO(file_bytes)
                doc = docx.Document(doc_file)
                for paragraph in doc.paragraphs:
                    extracted_text += paragraph.text + "\n"
            elif file_info.get('file_type') in ['text', 'data']:
                extracted_text = file_bytes.decode('utf-8')
                if real_mime_type == 'application/json':
                    extracted_text = json.dumps(json.loads(extracted_text), indent=2)
            else:
                logger.warning(f"Tipo de archivo no soportado para extracción de texto: {file_name}")
                return None

        except Exception as e:
            logger.error(f"Error en la función 'process_data': {e}")
            raise

    if not extracted_text.strip():
        logger.warning(f"No se pudo extraer texto del archivo: {file_name}")
        return None

    prompt_data = json.dumps(data_schema_manager, ensure_ascii=False)
    analysis_result = _process_text_with_gemini(extracted_text, prompt_data)

    if "error" not in analysis_result:
        return analysis_result
    else:
        logger.error(f"Error durante el análisis del texto: {analysis_result['error']}")
        return None

def _process_text_with_gemini(text_to_process: str, prompt_data: str) -> dict:
    """
    Función auxiliar privada para procesar el texto con Gemini.
    """
    try:
        combined_prompt = f"{prompt_data}\n\nTexto a analizar:\n{text_to_process}"
        logger.info("Enviando solicitud a Gemini...")
        response = model.generate_content(combined_prompt,
            generation_config= {
                "response_mime_type": "application/json"
            }
        )
        response_text = response.text.strip()
        logger.info("Respuesta de Gemini recibida.")

        # Buscar el inicio y fin del objeto JSON para un parsing seguro
        start_index = response_text.find('{')
        end_index = response_text.rfind('}')
        if start_index == -1 or end_index == -1:
            logger.error("No se encontró un JSON válido en la respuesta del modelo.")
            return {"error": "Invalid JSON response from model", "response": response_text}

        json_string = response_text[start_index:end_index+1]

        try:
            processed_data = json.loads(json_string)
            return processed_data
        except json.JSONDecodeError:
            logger.error("La respuesta del modelo no es un JSON válido después de la limpieza.")
            return {"error": "Invalid JSON response from model after cleaning", "response": json_string}
    except Exception as e:
        return {"error": str(e)}