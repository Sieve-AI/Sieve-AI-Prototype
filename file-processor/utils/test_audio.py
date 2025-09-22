import os
import logging
from google.cloud import speech, storage

# Configuración de logging para ver los resultados
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Importación relativa para que funcione correctamente
from .audio_processor import process_audio


# Configuración de los buckets de prueba
BUCKET_NAME = "data_lake_sieve" # <<--- Cambia esto
FILE_NAME = "quarantine/specials/luvvoice.com-20250912-SMGgQw.mp3"

def test_file_processor():
    """
    Función de prueba que llama directamente a process_audio
    para verificar que funciona con la API de Speech-to-Text.
    """
    try:
        file_info = {
            'file_type': 'audio',
            'mime_type': 'audio/mpeg' # o el tipo de tu archivo .mp3
        }
        
        logger.info(f"Iniciando prueba de procesamiento para el archivo: {FILE_NAME}")
        
        # Llamamos directamente a la función que queremos probar
        process_audio(BUCKET_NAME, FILE_NAME, file_info)

        logger.info("¡Prueba de procesamiento finalizada con éxito!")
        logger.info("Revisa la carpeta 'processed_results' en tu bucket de Cloud Storage.")
        
    except Exception as e:
        logger.error(f"La prueba falló con el siguiente error: {e}")

if __name__ == "__main__":
    test_file_processor()