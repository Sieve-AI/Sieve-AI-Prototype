"""
Utilidad para procesamiento de archivos de imagen
"""

from google.cloud import vision
import logging
import os

logger = logging.getLogger(__name__)

def process_image(bucket_name, file_name, file_info):
    """
    Procesa una imagen usando Vision API OCR.
    
    Args:
        bucket_name (str): Nombre del bucket.
        file_name (str): Nombre del archivo.
        file_info (dict): Información del archivo validado.
    
    Returns:
        str: El texto extraído de la imagen, o None si hay un error.
    """
    try:
        client = vision.ImageAnnotatorClient()
        
        image = vision.Image()
        image.source.image_uri = f"gs://{bucket_name}/{file_name}"
        
        response = client.text_detection(image=image)
        texts = response.text_annotations
        
        if response.error.message:
            raise Exception(f"Vision API error: {response.error.message}")
        
        extracted_text = ""
        if texts:
            extracted_text = texts[0].description
        
        logger.info(f"Texto extraído de la imagen {file_name} exitosamente.")
        
        return extracted_text
        
    except Exception as e:
        logger.error(f"Error procesando imagen {file_name}: {e}")
        return None