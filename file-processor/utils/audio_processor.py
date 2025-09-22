"""
Utilidad para procesamiento de archivos de audio
"""

import os
import logging
from google.cloud import speech_v1p1beta1 as speech
from google.cloud import storage
import config

# Importa la función de cuarentena desde un módulo de utilidades separado
from utils.file_mover import move_to_quarantine

logger = logging.getLogger(__name__)


def process_audio(bucket_name, file_name, file_info):
    """
    Procesa un archivo de audio directamente desde un URI de Cloud Storage usando la API de Speech-to-Text.
    """
    try:
        storage_client = storage.Client()
        gcs_uri = f"gs://{bucket_name}/{file_name}"
        logger.info(f"Enviando solicitud a Speech-to-Text para procesar el archivo: {gcs_uri}")
        
        client = speech.SpeechClient()
        audio = speech.RecognitionAudio(uri=gcs_uri)
        
        # Se asume la codificación MP3 y la tasa de muestreo estándar
        config_api = speech.RecognitionConfig(
            language_code="es-ES",
            enable_automatic_punctuation=True,
            encoding=speech.RecognitionConfig.AudioEncoding.MP3,
            sample_rate_hertz=44100,  # Frecuencia de muestreo estándar para MP3.
        )
        
        operation = client.long_running_recognize(
            config=config_api,
            audio=audio
        )
        
        response = operation.result(timeout=600)
        
        transcript = "".join([result.alternatives[0].transcript + "\n" for result in response.results])
        base_file_name = os.path.splitext(os.path.basename(file_name))[0]
        
        audio_results_path = config.PATHS.get('audio_results', 'audio_results/')
        result_file_name = f"{audio_results_path}{base_file_name}.txt"
        
        result_blob = storage_client.bucket(bucket_name).blob(result_file_name)
        result_blob.upload_from_string(transcript)
        
        logger.info(f"Audio procesado y transcrito: {file_name} -> {result_file_name}")
        
        return result_file_name

    except Exception as e:
        logger.error(f"Error procesando audio {file_name}: {e}")
        move_to_quarantine(bucket_name, file_name, f"Error procesamiento audio: {e}")
        return None