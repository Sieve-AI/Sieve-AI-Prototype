"""
Función principal de Cloud Function para procesamiento de archivos
"""

from google.cloud import storage
from utils.file_validator import validate_file
from utils.audio_processor import process_audio
from utils.image_processor import process_image
from utils.data_processor import process_data
import config
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def file_processor(event, context):
    """
    Función que se ejecuta cuando se sube un archivo a Cloud Storage
    
    Args:
        event (dict): Información del evento de Cloud Storage
        context (google.cloud.functions.Context): Metadatos del evento
    """
    # Obtener información del archivo
    file_name = event['name']
    bucket_name = event['bucket']
    
    logger.info(f"Procesando archivo: {file_name}")
    
    # Validar archivo
    file_info = validate_file(bucket_name, file_name)
    
    if not file_info['valid']:
        logger.warning(f"Archivo inválido: {file_name}. Razón: {file_info['reason']}")
        # Mover a cuarentena
        from utils.audio_processor import move_to_quarantine
        move_to_quarantine(bucket_name, file_name, file_info['reason'])
        return
    
    # Procesar según tipo
    try:
        if file_info['file_type'] == 'audio':
            process_audio(bucket_name, file_name, file_info)
        elif file_info['file_type'] == 'image':
            process_image(bucket_name, file_name, file_info)
        elif file_info['file_type'] == 'text':
            process_data(bucket_name, file_name, file_info)  # Para texto simple
        elif file_info['file_type'] == 'data':
            process_data(bucket_name, file_name, file_info)  # Para datos estructurados
        else:
            raise ValueError(f"Tipo de archivo no manejado: {file_info['file_type']}")
            
        logger.info(f"Procesamiento completado: {file_name}")
        
    except Exception as e:
        logger.error(f"Error procesando {file_name}: {e}")
        # Mover a cuarentena en caso de error
        from utils.audio_processor import move_to_quarantine
        move_to_quarantine(bucket_name, file_name, f"Error de procesamiento: {e}")