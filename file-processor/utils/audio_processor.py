"""
Utilidad para procesamiento de archivos de audio
"""

from google.cloud import speech, storage
import config
import logging
import os

logger = logging.getLogger(__name__)

def process_audio(bucket_name, file_name, file_info):
    """
    Procesa un archivo de audio usando Speech-to-Text API
    
    Args:
        bucket_name (str): Nombre del bucket
        file_name (str): Nombre del archivo
        file_info (dict): Información del archivo validado
    """
    try:
        client = speech.SpeechClient()
        storage_client = storage.Client()
        
        # Configurar reconocimiento de audio
        audio = speech.RecognitionAudio(
            uri=f"gs://{bucket_name}/{file_name}"
        )
        
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.MP3,
            sample_rate_hertz=16000,
            language_code="es-ES",  # Ajustar según necesidad
            enable_automatic_punctuation=True,
        )
        
        # Operación de reconocimiento
        operation = client.long_running_recognize(
            config=config, 
            audio=audio
        )
        
        response = operation.result(timeout=90)
        
        # Extraer texto
        transcript = ""
        for result in response.results:
            transcript += result.alternatives[0].transcript + "\n"
        
        # Guardar resultado
        result_file_name = f"{os.path.splitext(file_name)[0]}.txt"
        result_blob = storage_client.bucket(bucket_name).blob(
            f"{config.PATHS['audio_results']}{result_file_name}"
        )
        
        result_blob.upload_from_string(transcript)
        
        logger.info(f"Audio procesado: {file_name} -> {result_file_name}")
        
    except Exception as e:
        logger.error(f"Error procesando audio {file_name}: {e}")
        # Mover a cuarentena en caso de error
        move_to_quarantine(bucket_name, file_name, f"Error procesamiento audio: {e}")

def move_to_quarantine(bucket_name, file_name, reason):
    """Mueve un archivo a cuarentena"""
    try:
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        
        source_blob = bucket.blob(file_name)
        destination_blob = bucket.blob(
            f"{config.PATHS['quarantine']}{file_name}"
        )
        
        # Copiar a cuarentena
        bucket.copy_blob(
            source_blob, bucket, destination_blob
        )
        
        logger.warning(f"Archivo movido a cuarentena: {file_name}. Razón: {reason}")
        
    except Exception as e:
        logger.error(f"Error moviendo a cuarentena {file_name}: {e}")