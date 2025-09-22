"""
Módulo para el procesamiento de datos con BigFrames.
Contiene la lógica para el análisis y pronóstico de datos transaccionales,
utilizando una amplia gama de columnas de datos.
"""

import logging
import os
import bigframes.pandas as bfp
import bigframes.ml.llm as bfml
from google.cloud import storage
import vertexai

# Configuración del registro
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Define las ubicaciones de los buckets y carpetas
DESTINATION_BUCKET = "data-framed-sieve"
FINAL_REPORTS_FOLDER = "final_reports/"

# Define listas de posibles nombres de columnas para un análisis dinámico
TEXT_COLUMNS = [
    'client_name', 'address', 'user_review', 'product_description',
    'website_url', 'mix_of_numbers_and_text', 'raw_data_applied',
    'address_and_city', 'country', 'product_reviews',
    'social_media_comments', 'description_of_log_errors'
]
FINANCIAL_COLUMNS = [
    'number_of_units_sold', 'number_of_transactions', 'edad', 'scores',
    'unit_price', 'total_cost', 'revenue', 'interest_rates',
    'temperature', 'weight', 'hight', 'width', 'atmospheric_pressure',
    'humidity', 'average_score', 'percentage_of_sales', 'growth_rate',
    'min_mean_max', 'latitude', 'longitude'
]
TIME_COLUMNS = [
    'record_creation', 'transaction_date', 'session_start_time',
    'birthdate', 'timestamp', 'reading_date', 'event_time_log',
    'holiday_day', 'product_expiration_date', 'invoice_due'
]
IDENTIFIER_COLUMNS = [
    'client_id', 'product_id', 'order_number', 'employee_number',
    'postal_code', 'order_status', 'civil_status', 'gender', 'product_type',
    'payment_method', 'brand', 'level_of_education', 'product_rating',
    'clothing_size', 'satisfaction_level', 'product_in_stock'
]

PROJECT_ID = "sieve-ai-470820"
LOCATION = "us-central1"

try:
    vertexai.init(project=PROJECT_ID, location=LOCATION)
except Exception as e:
    logger.error(f"Error al inicializar Vertex AI: {e}")

try:
    BIGFRAMES_IMPORTED = True
except ImportError as e:
    logger.warning(f"No se pudieron importar las bibliotecas de BigFrames: {e}. El análisis de reportes no estará disponible.")
    BIGFRAMES_IMPORTED = False

def analyze_data_with_bigframes(csv_file_path: str):
    """
    Realiza un análisis profundo de los datos en el archivo CSV usando BigFrames
    y genera un reporte estructurado en formato de texto.

    Args:
        csv_file_path (str): La ruta al archivo CSV en el bucket de GCS.
    
    Returns:
        str: El contenido del reporte de análisis y pronóstico en formato de texto.
    """
    if not BIGFRAMES_IMPORTED:
        return "Error: Las bibliotecas de BigFrames no están disponibles. El análisis no se pudo realizar."

    storage_client = storage.Client()
    bucket = storage_client.bucket(DESTINATION_BUCKET)
    blob = bucket.blob(csv_file_path)

    if not blob.exists():
        error_message = f"Error 404: El archivo '{csv_file_path}' no fue encontrado en el bucket '{DESTINATION_BUCKET}'."
        logger.error(error_message)
        return f"status: error\nmessage: {error_message}\ndetails: El proceso no continuó porque el archivo de origen no existe."

    logger.info("Iniciando análisis de datos con BigFrames...")

    try:
        df = bfp.read_csv(f"gs://{DESTINATION_BUCKET}/{csv_file_path}")
        logger.info(f"Datos cargados. Columnas disponibles: {df.columns.tolist()}")

        relevant_text_cols = [col for col in TEXT_COLUMNS if col in df.columns]
        if relevant_text_cols:
            # Genera un prompt dinámico para resumir el contenido
            prompt_content = f"""
            Analiza los datos de las columnas de texto {relevant_text_cols} y las columnas financieras {FINANCIAL_COLUMNS} del siguiente DataFrame.
            Genera un reporte ejecutivo detallado sobre los hallazgos clave, correlaciones, y patrones de comportamiento.
            Proporciona una síntesis en un párrafo claro.
            DataFrame en formato JSON: {df.to_json(orient='records', lines=True, index=False)[:2000]}...
            """
            
            try:
                # Crea una instancia del modelo
                model = bfml.GeminiTextGenerator()
                
                # Crea un DataFrame con el prompt para pasarlo a la función predict
                prompt_df = bfp.DataFrame({"prompt": [prompt_content]})
                
                # Usa el modelo para predecir, pasando solo el DataFrame
                summary_result = model.predict(prompt_df)
                
                # Usa el nombre de columna correcto para el resultado
                return summary_result["ml_generate_text_llm_result"].iloc[0]
            except Exception as text_analysis_error:
                logger.warning(f"No se pudo generar el reporte de texto: {text_analysis_error}")
                return "Ocurrió un error al generar el reporte de texto. Este paso fue omitido."
        else:
            logger.warning("No se encontraron columnas de texto relevantes para el análisis.")
            return "No se encontraron columnas de texto relevantes para el análisis."
    
    except Exception as e:
        logger.error(f"Error fatal en el análisis de BigFrames: {e}")
        return f"Error en el análisis. Consulte los registros para más detalles: {e}"