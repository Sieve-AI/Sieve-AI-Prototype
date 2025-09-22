"""
Utilidad para verificación de formatos de archivo mediante el nombre de archivo
"""

import mimetypes
from google.cloud import storage
import logging
import os

logger = logging.getLogger(__name__)

def get_file_mime_type(bucket_name, file_name):
    """
    Obtiene el tipo MIME real de un archivo basándose en su nombre.
    
    Args:
        bucket_name (str): Nombre del bucket
        file_name (str): Nombre del archivo
    
    Returns:
        str: Tipo MIME detectado o None en caso de error
    """
    try:
        # Usar la librería mimetypes, que no tiene dependencias externas
        mime_type, encoding = mimetypes.guess_type(file_name)
        
        if mime_type:
            logger.info(f"Tipo MIME detectado con mimetypes: {mime_type}")
            return mime_type
        else:
            # Si mimetypes falla, se puede intentar adivinar por la extensión
            ext = os.path.splitext(file_name)[1].lower()
            if ext == '.mp3':
                return 'audio/mpeg'
            elif ext == '.wav':
                return 'audio/wav'
            elif ext == '.ogg':
                return 'audio/ogg'
            # Puedes añadir más extensiones aquí si lo necesitas
            
            logger.warning(f"No se pudo determinar el tipo MIME para el archivo: {file_name}")
            return None
            
    except Exception as e:
        logger.error(f"Error inesperado al verificar tipo MIME: {e}")
        return None