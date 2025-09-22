import os
import json
import logging
import pandas as pd
from google.cloud import storage

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuración del bucket y la carpeta
BUCKET_NAME = "data_lake_sieve" 
SOURCE_FOLDER = "processed/processed_results/"
DESTINATION_FOLDER = "data_lake_sieve/curated/structured_results/" 

def process_json_event(bucket_name: str, file_name: str):
    """
    Procesa un solo archivo JSON de Cloud Storage, lo convierte en un DataFrame de Pandas
    y guarda el resultado como CSV.

    Args:
        bucket_name (str): El nombre del bucket de Google Cloud Storage.
        file_name (str): La ruta completa del archivo JSON a procesar.
    """
    try:
        # Inicializa el cliente de Cloud Storage
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)

        # Procesa solo si el archivo está en la carpeta de origen y es un JSON
        if file_name.startswith(SOURCE_FOLDER) and file_name.endswith('.json'):
            logger.info(f"Procesando archivo JSON: {file_name}")

            blob = bucket.blob(file_name)
            
            try:
                # Descarga el contenido del archivo JSON
                json_content = blob.download_as_text()
                
                # Carga el contenido en un objeto de Python
                data = json.loads(json_content)
                
                # Usa la estructura del ejemplo para obtener la lista de datos
                if 'dataframe_package' in data and 'data' in data['dataframe_package']:
                    table_data = data['dataframe_package']['data']
                    
                    # Convierte la lista de diccionarios a un DataFrame de Pandas
                    df = pd.DataFrame.from_dict(table_data)
                    
                    logger.info(f"DataFrame creado con {df.shape[0]} filas y {df.shape[1]} columnas.")
                    
                    # Define la ruta de destino para el archivo CSV
                    base_name = os.path.basename(file_name).replace('.json', '.csv')
                    destination_blob_name = os.path.join(DESTINATION_FOLDER, base_name)

                    # Guarda el DataFrame en un archivo CSV en el bucket
                    _save_dataframe_as_csv(df, bucket, destination_blob_name)
                else:
                    logger.warning(f"El archivo {file_name} no contiene la estructura esperada.")

            except Exception as e:
                logger.error(f"Error al procesar el archivo {file_name}: {e}")
        else:
            logger.info(f"El archivo {file_name} no cumple con los criterios para ser procesado.")

    except Exception as e:
        logger.error(f"Error general: {e}")

def _save_dataframe_as_csv(df: pd.DataFrame, bucket: storage.Bucket, destination_blob_name: str):
    """
    Guarda un DataFrame de Pandas como un archivo CSV en un bucket de GCS.
    """
    try:
        # Convierte el DataFrame a un CSV en memoria
        csv_string = df.to_csv(index=False)
        
        # Sube la cadena CSV a Cloud Storage
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_string(csv_string, content_type='text/csv')
        
        logger.info(f"DataFrame guardado exitosamente como CSV en: {destination_blob_name}")
    except Exception as e:
        logger.error(f"Error al guardar el DataFrame como CSV: {e}")

