"""
Utilidad para procesamiento de archivos de imagen
"""

from google.cloud import vision, storage
import config
import logging
import os

logger = logging.getLogger(__name__)

def process_image(bucket_name, file_name, file_info):
    """
    Procesa una imagen usando Vision API OCR
    
    Args:
        bucket_name (str): Nombre del bucket
        file_name (str): Nombre del archivo
        file_info (dict): Información del archivo validado
    """
    try:
        client = vision.ImageAnnotatorClient()
        storage_client = storage.Client()
        
        # Configurar imagen
        image = vision.Image()
        image.source.image_uri = f"gs://{bucket_name}/{file_name}"
        
        # Realizar OCR
        response = client.text_detection(image=image)
        texts = response.text_annotations
        
        if response.error.message:
            raise Exception(f"Vision API error: {response.error.message}")
        
        # Extraer texto
        extracted_text = ""
        if texts:
            extracted_text = texts[0].description
        
        # Guardar resultado
        result_file_name = f"{os.path.splitext(file_name)[0]}.txt"
        result_blob = storage_client.bucket(bucket_name).blob(
            f"{config.PATHS['image_results']}{result_file_name}"
        )
        
        result_blob.upload_from_string(extracted_text)
        
        logger.info(f"Imagen procesada: {file_name} -> {result_file_name}")
        
    except Exception as e:
        logger.error(f"Error procesando imagen {file_name}: {e}")
        # Mover a cuarentena en caso de error
        from .audio_processor import move_to_quarantine
        move_to_quarantine(bucket_name, file_name, f"Error procesamiento imagen: {e}")