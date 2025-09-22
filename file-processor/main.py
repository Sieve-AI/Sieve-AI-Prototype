"""
Función principal de Cloud Function para procesamiento de archivos
"""

import logging
import base64
import json
import os
import pandas as pd
from google.cloud import storage
from google.api_core.exceptions import NotFound
import functions_framework

# Importa tus módulos de procesamiento
from utils.file_validator import validate_file
from utils.audio_processor import process_audio
from utils.image_processor import process_image
from utils.data_processor import process_data
# Importa la función de cuarentena desde un módulo de utilidades
from utils.file_mover import move_to_quarantine
# Importa el nuevo módulo para el análisis de BigFrames
from utils.bigframes_processor import analyze_data_with_bigframes

# Configuración del registro
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define las ubicaciones de los buckets y carpetas
DESTINATION_BUCKET = "data-framed-sieve"
QUARANTINE_FOLDER = "quarantine/"
PROCESSED_RESULTS_FOLDER = "processed/processed_results/"
PROCESSED_STACKS_FOLDER = "processed/stacks/"
PROCESSED_RAW_REPORTS_FOLDER = "processed/raw_reports/"
FINAL_REPORTS_FOLDER = "final_reports/"


def _save_as_json(data: dict, file_name: str):
    """
    Guarda los datos procesados como un archivo JSON en Cloud Storage.
    """
    try:
        storage_client = storage.Client()
        bucket = storage_client.bucket(DESTINATION_BUCKET)
        blob = bucket.blob(file_name)

        json_string = json.dumps(data)
        blob.upload_from_string(json_string, content_type='application/json')
        logger.info(f"Archivo JSON guardado en: {file_name}")
    except Exception as e:
        logger.error(f"Error al guardar el archivo JSON en {file_name}: {e}")
        raise


def _process_and_save_as_csv(json_data: dict, original_file_name: str):
    """
    Procesa un diccionario JSON y lo convierte a un archivo CSV en Cloud Storage.
    """
    try:
        if isinstance(json_data, dict) and 'dataframe_package' in json_data and 'data' in json_data['dataframe_package']:
            table_data = json_data['dataframe_package']['data']
            if not table_data:
                logger.warning(f"La estructura 'dataframe_package' está vacía después de la limpieza para el archivo {original_file_name}. No se puede crear el DataFrame.")
                return None
            
            df = pd.DataFrame.from_dict(table_data)
        elif isinstance(json_data, list):
            df = pd.DataFrame(json_data)
        elif isinstance(json_data, dict) and 'data' in json_data:
            df = pd.DataFrame.from_dict(json_data['data'])
        else:
            logger.warning(f"Estructura JSON no reconocida para el archivo {original_file_name}. No se puede crear el DataFrame.")
            return None

        logger.info(f"DataFrame creado con {df.shape[0]} filas y {df.shape[1]} columnas.")

        storage_client = storage.Client()
        bucket = storage_client.bucket(DESTINATION_BUCKET)

        base_name = os.path.basename(original_file_name)
        base_name_without_ext = os.path.splitext(base_name)[0]
        destination_blob_name = f"{PROCESSED_STACKS_FOLDER}{base_name_without_ext}.csv"

        csv_string = df.to_csv(index=False)
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_string(csv_string, content_type='text/csv')

        logger.info(f"DataFrame convertido y guardado como CSV en: {destination_blob_name}")
        return destination_blob_name

    except Exception as e:
        logger.error(f"Error en la conversión y guardado del DataFrame para {original_file_name}: {e}")
        raise


def _save_text_report(json_data: dict, original_file_name: str, report_content: str = None):
    """
    Extrae y guarda un reporte de texto. Si se proporciona `report_content`, lo usa.
    De lo contrario, extrae el reporte del JSON.
    """
    try:
        if report_content:
            report_to_save = report_content
            folder = FINAL_REPORTS_FOLDER
        elif 'generated_report' in json_data and 'findings' in json_data.get('generated_report', {}):
            report_data = json_data['generated_report']
            findings_data = report_data['findings']
            report_to_save = (
                f"Tipo de Reporte: {report_data.get('report_type', 'N/A')}\n"
                "--------------------------------------\n"
                "Observaciones:\n"
                f"{findings_data.get('observations', 'No hay observaciones.')}\n\n"
                "Puntos Clave:\n"
            )
            key_points = findings_data.get('key_points', [])
            report_to_save += "\n".join([f"- {point}" for point in key_points]) if key_points else "No se encontraron puntos clave.\n"
            folder = PROCESSED_RAW_REPORTS_FOLDER
        else:
            logger.warning(f"El JSON no contiene las claves 'generated_report' o 'findings' y no se proporcionó un reporte para el archivo {original_file_name}.")
            return

        storage_client = storage.Client()
        bucket = storage_client.bucket(DESTINATION_BUCKET)

        base_name = os.path.basename(original_file_name)
        base_name_without_ext = os.path.splitext(base_name)[0]
        destination_blob_name = f"{folder}{base_name_without_ext}_report.txt"

        blob = bucket.blob(destination_blob_name)
        blob.upload_from_string(report_to_save, content_type='text/plain')
        logger.info(f"Informe de texto guardado en: {destination_blob_name}")
    except Exception as e:
        logger.error(f"Error al guardar el informe de texto para {original_file_name}: {e}")
        raise


@functions_framework.http
def file_processor(request):
    """
    Función que procesa el evento de Cloud Storage desde un mensaje de Pub/Sub.
    """
    try:
        event_payload = request.get_json(silent=True)
        if not event_payload or 'message' not in event_payload:
            logger.error("Error: El payload de la solicitud no es un mensaje de Pub/Sub válido.")
            return ('Bad Request: Invalid Pub/Sub message', 400)

        message_data = event_payload['message'].get('data')
        if not message_data:
            logger.error("Error: El mensaje de Pub/Sub no contiene datos.")
            return ('Bad Request: Missing data in Pub/Sub message', 400)

        decoded_data = base64.b64decode(message_data).decode('utf-8')
        cloud_storage_event = json.loads(decoded_data)

        bucket_name = cloud_storage_event.get('bucket')
        file_name = cloud_storage_event.get('name')

    except (KeyError, json.JSONDecodeError, TypeError) as e:
        logger.error(f"Error fatal al procesar el evento de Cloud Storage: {e}")
        return ('Bad Request: Failed to parse event', 400)

    if not bucket_name or not file_name:
        logger.error("Faltan datos esenciales del evento (bucket o nombre del archivo).")
        return ('Bad Request: Missing essential data', 400)

    return process_file(bucket_name, file_name)


def process_file(bucket_name, file_name):
    """
    Función auxiliar para procesar el archivo.
    """
    if file_name.endswith('/') or file_name.startswith('quarantine/'):
        logger.info(f"Omitiendo evento para: {file_name}")
        return ('OK', 200)

    logger.info(f"Iniciando el procesamiento del archivo: {file_name} del bucket {bucket_name}")

    try:
        file_info = validate_file(bucket_name, file_name)

        if not file_info['valid']:
            logger.warning(f"Archivo inválido: {file_name}. Razón: {file_info['reason']}")
            move_to_quarantine(bucket_name, file_name, file_info['reason'], DESTINATION_BUCKET)
            return ('OK', 200)

        processed_data_json = None
        if file_info['file_type'] == 'audio':
            processed_data_json = process_audio(bucket_name, file_name, file_info)
        elif file_info['file_type'] == 'image':
            extracted_text = process_image(bucket_name, file_name, file_info)
            if extracted_text:
                processed_data_json = process_data(bucket_name, file_name, file_info, text_content=extracted_text)
            else:
                logger.warning(f"No se extrajo texto de la imagen {file_name}.")
                move_to_quarantine(bucket_name, file_name, "No se pudo extraer texto de la imagen", DESTINATION_BUCKET)
                return ('OK', 200)
        elif file_info['file_type'] in ['text', 'data']:
            processed_data_json = process_data(bucket_name, file_name, file_info)
        else:
            raise ValueError(f"Tipo de archivo no manejado: {file_info['file_type']}")

        if processed_data_json:
            json_file_name = f"{PROCESSED_RESULTS_FOLDER}{os.path.splitext(os.path.basename(file_name))[0]}.json"
            _save_as_json(processed_data_json, json_file_name)
            
            # Crea el archivo CSV y obtén su ruta
            csv_file_path = _process_and_save_as_csv(processed_data_json, file_name)

            # Guarda el reporte inicial del JSON
            _save_text_report(processed_data_json, file_name)

            # Si el CSV se creó exitosamente, realiza el análisis avanzado con BigFrames
            if csv_file_path:
                bigframes_report_content = analyze_data_with_bigframes(csv_file_path)
                # Vuelve a guardar el reporte final en la carpeta correcta
                _save_text_report(processed_data_json, file_name, report_content=bigframes_report_content)

            # El archivo original debe ser borrado al final del proceso
            storage_client = storage.Client()
            source_bucket = storage_client.bucket(bucket_name)
            source_blob = source_bucket.blob(file_name)
            source_blob.delete()
            logger.info(f"Archivo original eliminado: {file_name}")

        logger.info(f"Procesamiento completado para: {file_name}")
        return ('OK', 200)

    except NotFound:
        logger.warning(f"Archivo no encontrado en el bucket de origen: {file_name}. Probablemente ya fue procesado.")
        return ('OK', 200)
    except Exception as e:
        logger.error(f"Error procesando {file_name}: {e}")
        move_to_quarantine(bucket_name, file_name, f"Error de procesamiento: {e}", DESTINATION_BUCKET)
        return (f"Error de procesamiento: {e}", 500)

    except Exception as e:
        logger.error(f"Error en la conversión y guardado del DataFrame para {original_file_name}: {e}")
        raise


def _save_text_report(json_data: dict, original_file_name: str, report_content: str = None):
    """
    Extrae y guarda un reporte de texto. Si se proporciona `report_content`, lo usa.
    De lo contrario, extrae el reporte del JSON.
    """
    try:
        if report_content:
            report_to_save = report_content
            folder = FINAL_REPORTS_FOLDER
        elif 'generated_report' in json_data and 'findings' in json_data.get('generated_report', {}):
            report_data = json_data['generated_report']
            findings_data = report_data['findings']
            report_to_save = (
                f"Tipo de Reporte: {report_data.get('report_type', 'N/A')}\n"
                "--------------------------------------\n"
                "Observaciones:\n"
                f"{findings_data.get('observations', 'No hay observaciones.')}\n\n"
                "Puntos Clave:\n"
            )
            key_points = findings_data.get('key_points', [])
            report_to_save += "\n".join([f"- {point}" for point in key_points]) if key_points else "No se encontraron puntos clave.\n"
            folder = PROCESSED_RAW_REPORTS_FOLDER
        else:
            logger.warning(f"El JSON no contiene las claves 'generated_report' o 'findings' y no se proporcionó un reporte para el archivo {original_file_name}.")
            return

        storage_client = storage.Client()
        bucket = storage_client.bucket(DESTINATION_BUCKET)

        base_name = os.path.basename(original_file_name)
        base_name_without_ext = os.path.splitext(base_name)[0]
        destination_blob_name = f"{folder}{base_name_without_ext}_report.txt"

        blob = bucket.blob(destination_blob_name)
        blob.upload_from_string(report_to_save, content_type='text/plain')
        logger.info(f"Informe de texto guardado en: {destination_blob_name}")
    except Exception as e:
        logger.error(f"Error al guardar el informe de texto para {original_file_name}: {e}")
        raise


@functions_framework.http
def file_processor(request):
    """
    Función que procesa el evento de Cloud Storage desde un mensaje de Pub/Sub.
    """
    try:
        event_payload = request.get_json(silent=True)
        if not event_payload or 'message' not in event_payload:
            logger.error("Error: El payload de la solicitud no es un mensaje de Pub/Sub válido.")
            return ('Bad Request: Invalid Pub/Sub message', 400)

        message_data = event_payload['message'].get('data')
        if not message_data:
            logger.error("Error: El mensaje de Pub/Sub no contiene datos.")
            return ('Bad Request: Missing data in Pub/Sub message', 400)

        decoded_data = base64.b64decode(message_data).decode('utf-8')
        cloud_storage_event = json.loads(decoded_data)

        bucket_name = cloud_storage_event.get('bucket')
        file_name = cloud_storage_event.get('name')

    except (KeyError, json.JSONDecodeError, TypeError) as e:
        logger.error(f"Error fatal al procesar el evento de Cloud Storage: {e}")
        return ('Bad Request: Failed to parse event', 400)

    if not bucket_name or not file_name:
        logger.error("Faltan datos esenciales del evento (bucket o nombre del archivo).")
        return ('Bad Request: Missing essential data', 400)

    return process_file(bucket_name, file_name)


def process_file(bucket_name, file_name):
    """
    Función auxiliar para procesar el archivo.
    """
    if file_name.endswith('/') or file_name.startswith('quarantine/'):
        logger.info(f"Omitiendo evento para: {file_name}")
        return ('OK', 200)

    logger.info(f"Iniciando el procesamiento del archivo: {file_name} del bucket {bucket_name}")

    try:
        file_info = validate_file(bucket_name, file_name)

        if not file_info['valid']:
            logger.warning(f"Archivo inválido: {file_name}. Razón: {file_info['reason']}")
            move_to_quarantine(bucket_name, file_name, file_info['reason'], DESTINATION_BUCKET)
            return ('OK', 200)

        processed_data_json = None
        if file_info['file_type'] == 'audio':
            processed_data_json = process_audio(bucket_name, file_name, file_info)
        elif file_info['file_type'] == 'image':
            extracted_text = process_image(bucket_name, file_name, file_info)
            if extracted_text:
                processed_data_json = process_data(bucket_name, file_name, file_info, text_content=extracted_text)
            else:
                logger.warning(f"No se extrajo texto de la imagen {file_name}.")
                move_to_quarantine(bucket_name, file_name, "No se pudo extraer texto de la imagen", DESTINATION_BUCKET)
                return ('OK', 200)
        elif file_info['file_type'] in ['text', 'data']:
            processed_data_json = process_data(bucket_name, file_name, file_info)
        else:
            raise ValueError(f"Tipo de archivo no manejado: {file_info['file_type']}")

        if processed_data_json:
            json_file_name = f"{PROCESSED_RESULTS_FOLDER}{os.path.splitext(os.path.basename(file_name))[0]}.json"
            _save_as_json(processed_data_json, json_file_name)
            
            # Crea el archivo CSV y obtén su ruta
            csv_file_path = _process_and_save_as_csv(processed_data_json, file_name)

            # Guarda el reporte inicial del JSON
            _save_text_report(processed_data_json, file_name)

            # Si el CSV se creó exitosamente, realiza el análisis avanzado con BigFrames
            if csv_file_path:
                bigframes_report_content = analyze_data_with_bigframes(csv_file_path)
                # Vuelve a guardar el reporte final en la carpeta correcta
                _save_text_report(processed_data_json, file_name, report_content=bigframes_report_content)

            # El archivo original debe ser borrado al final del proceso
            storage_client = storage.Client()
            source_bucket = storage_client.bucket(bucket_name)
            source_blob = source_bucket.blob(file_name)
            source_blob.delete()
            logger.info(f"Archivo original eliminado: {file_name}")

        logger.info(f"Procesamiento completado para: {file_name}")
        return ('OK', 200)

    except NotFound:
        logger.warning(f"Archivo no encontrado en el bucket de origen: {file_name}. Probablemente ya fue procesado.")
        return ('OK', 200)
    except Exception as e:
        logger.error(f"Error procesando {file_name}: {e}")
        move_to_quarantine(bucket_name, file_name, f"Error de procesamiento: {e}", DESTINATION_BUCKET)
        return (f"Error de procesamiento: {e}", 500)
