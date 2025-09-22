import logging
import os
from google.cloud import storage
from google.api_core.exceptions import NotFound

# Configuración de logging
logger = logging.getLogger(__name__)

def move_to_quarantine(bucket_name: str, file_name: str, reason: str, destination_bucket: str = None):
    """
    Mueve un archivo a la carpeta de cuarentena, opcionalmente a un bucket diferente.
    """
    try:
        storage_client = storage.Client()
        source_bucket = storage_client.bucket(bucket_name)
        
        # Define el blob de origen
        source_blob = source_bucket.blob(file_name)

        # Si no existe el archivo de origen, no hacemos nada
        if not source_blob.exists():
            logger.warning(f"No se pudo mover a cuarentena. El archivo de origen ya no existe: {file_name}")
            return

        # Determina el bucket de destino
        target_bucket = storage_client.bucket(destination_bucket if destination_bucket else bucket_name)

        # Define la ruta de destino en la carpeta de cuarentena
        base_name = os.path.basename(file_name)
        destination_blob_name = f"quarantine/{base_name}"
        
        # Copia el archivo al bucket y la carpeta de destino
        source_blob.copy_to(target_bucket.blob(destination_blob_name))
        
        # Elimina el archivo original del bucket de origen
        source_blob.delete()
        
        logger.info(f"Archivo movido a cuarentena: {destination_blob_name} en el bucket {target_bucket.name}. Razón: {reason}")
    except NotFound:
        logger.warning(f"El archivo de origen {file_name} ya no existe. No es necesario moverlo a cuarentena.")
    except Exception as e:
        logger.error(f"Error moviendo a cuarentena {file_name}: {e}")