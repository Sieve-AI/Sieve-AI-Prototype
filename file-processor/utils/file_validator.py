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
        file_name (str): Nombre del archivo
    
    Returns:
        dict: Información del archivo validado
    """
    try:
        # Obtener extensión y metadata básica
        file_extension = os.path.splitext(file_name)[1].lower()
        
        # Verificar tipo real con magic numbers
        real_mime_type = get_file_mime_type(bucket_name, file_name)
        
        if not real_mime_type:
            return {
                'valid': False,
                'reason': 'No se pudo determinar el tipo de archivo'
            }
        
        # Clasificar por tipo MIME real
        file_type = None
        if real_mime_type in config.AUDIO_FORMATS['mime_types']:
            file_type = 'audio'
        elif real_mime_type in config.IMAGE_FORMATS['mime_types']:
            file_type = 'image'
        elif real_mime_type in config.TEXT_FORMATS['mime_types']:
            file_type = 'text'
        elif real_mime_type in config.DATA_FORMATS['mime_types']:
            file_type = 'data'
        else:
            return {
                'valid': False,
                'reason': f'Tipo MIME no soportado: {real_mime_type}'
            }
        
        return {
            'valid': True,
            'file_type': file_type,
            'real_mime_type': real_mime_type,
            'extension': file_extension,
            'file_name': file_name
        }
        
    except Exception as e:
        logger.error(f"Error en validación de archivo: {e}")
        return {
            'valid': False,
            'reason': f'Error de validación: {str(e)}'
        }