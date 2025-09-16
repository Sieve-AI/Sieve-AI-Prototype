"""
Utilidad para verificación de formatos de archivo mediante magic numbers
"""

import magic
from google.cloud import storage
from google.api_core.exceptions import GoogleAPIError
import logging

logger = logging.getLogger(__name__)

def get_file_mime_type(bucket_name, file_name):
    """
    Obtiene el tipo MIME real de un archivo usando magic numbers
    
    Args:
        bucket_name (str): Nombre del bucket
        file_name (str): Nombre del archivo
    
    Returns:
        str: Tipo MIME detectado o None en caso de error
    """
    try:
        client = storage.Client()
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(file_name)
        
        # Descargar los primeros bytes para análisis
        chunk = blob.download_as_bytes(start=0, end=1024)
        
        # Detectar tipo MIME usando magic numbers
        mime_type = magic.from_buffer(chunk, mime=True)
        
        return mime_type
        
    except GoogleAPIError as e:
        logger.error(f"Error de Google Cloud al verificar magic numbers: {e}")
        return None
    except Exception as e:
        logger.error(f"Error inesperado al verificar magic numbers: {e}")
        return None