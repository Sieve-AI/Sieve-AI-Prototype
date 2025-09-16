"""
Configuración global del sistema de procesamiento de archivos
"""

import os

# Configuración de Google Cloud
BUCKET_NAME = os.environ.get("BUCKET_NAME", "data_lake_sieve")
PROJECT_ID = os.environ.get("PROJECT_ID", "tu-project-id")  # Reemplazar con tu project ID real
MAX_FILE_SIZE = int(os.environ.get("MAX_FILE_SIZE", 10485760))  # 10MB

# Formatos de archivo soportados
AUDIO_FORMATS = {
    'mime_types': ['audio/mpeg', 'audio/wav', 'audio/x-wav'],
    'extensions': ['.mp3', '.wav']
}

IMAGE_FORMATS = {
    'mime_types': ['image/jpeg', 'image/png'],
    'extensions': ['.jpg', '.jpeg', '.png']
}

TEXT_FORMATS = {
    'mime_types': ['text/plain'],
    'extensions': ['.txt']
}

DATA_FORMATS = {
    'mime_types': ['application/json', 'text/csv'],
    'extensions': ['.json', '.csv']
}

# Rutas dentro del bucket
PATHS = {
    'raw_storage': 'raw/storage/',
    'audio_results': 'raw/audio_results/',
    'image_results': 'raw/image_results/',
    'text_files': 'raw/text_files/',
    'pending_data': 'processed/pending_data/',
    'quarantine': 'quarantine/specials/'
}