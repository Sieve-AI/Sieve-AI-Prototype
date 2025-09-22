"""
Utilidad para validar y clasificar archivos
"""

import os
from google.cloud import storage
from .magic_checker import get_file_mime_type
import config
import logging

logger = logging.getLogger(__name__)

def validate_file(bucket_name, file_name):
    """
    Valida y clasifica un archivo según su tipo real

    Args:
        bucket_name (str): Nombre del bucket
        file_name (str): Nombre del archivo (incluyendo la ruta completa si está en una subcarpeta)

    Returns:
        dict: Información del archivo validado
    """
    try:
        # Extraer el nombre de archivo base para el log
        base_file_name = os.path.basename(file_name)

        # Verificar tipo real con magic numbers
        real_mime_type = get_file_mime_type(bucket_name, file_name)
        
        if not real_mime_type:
            logger.warning(f"No se pudo determinar el tipo MIME para el archivo: {file_name}")
            return {
                'valid': False,
                'reason': 'No se pudo determinar el tipo de archivo'
            }
        
        # Clasificar por tipo MIME real, incluyendo los extras
        file_type = None
        if real_mime_type in config.AUDIO_FORMATS.get('mime_types', []) or real_mime_type in config.AUDIO_MIME_TYPES_EXTRAS:
            file_type = 'audio'
        elif real_mime_type in config.IMAGE_FORMATS.get('mime_types', []) or real_mime_type in config.IMAGE_MIME_TYPES_EXTRAS:
            file_type = 'image'
        elif real_mime_type in config.TEXT_FORMATS.get('mime_types', []) or real_mime_type in config.TEXT_MIME_TYPES_EXTRAS:
            file_type = 'text'
        elif real_mime_type in config.DATA_FORMATS.get('mime_types', []) or real_mime_type in config.DATA_MIME_TYPES_EXTRAS:
            file_type = 'data'
        else:
            logger.warning(f"Tipo MIME no soportado para el archivo {file_name}: {real_mime_type}")
            return {
                'valid': False,
                'reason': f'Tipo MIME no soportado: {real_mime_type}'
            }
        
        # Validar la extensión del archivo
        file_extension = os.path.splitext(file_name)[1].lower()
        
        allowed_extensions = config.ALL_FORMATS
        
        if file_extension and file_extension not in allowed_extensions:
            logger.warning(f"Extensión de archivo no válida para {file_name}: {file_extension}. Tipos de archivo permitidos: {allowed_extensions}")
            return {
                'valid': False,
                'reason': f"Extensión no válida: {file_extension}"
            }

        logger.info(f"Archivo validado: {file_name} -> Tipo: {file_type}, MIME: {real_mime_type}")
        return {
            'valid': True,
            'file_type': file_type,
            'real_mime_type': real_mime_type,
            'extension': file_extension,
            'file_name': file_name
        }
        
    except Exception as e:
        logger.error(f"Error inesperado en la validación de archivo {file_name}: {e}")
        return {
            'valid': False,
            'reason': f'Error de validación inesperado: {str(e)}'
        }