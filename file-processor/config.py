"""
Configuración global del sistema de procesamiento de archivos
"""

import os

# Configuración de Google Cloud
BUCKET_NAME = os.environ.get("BUCKET_NAME", "data_lake_sieve")
PROJECT_ID = os.environ.get("PROJECT_ID", "sieve-ai-470820")
MAX_FILE_SIZE = int(os.environ.get("MAX_FILE_SIZE", 10485760))  # 10MB

# Formatos de archivo soportados
AUDIO_FORMATS = {
    'mime_types': ['audio/mpeg', 'audio/wav', 'audio/x-wav', 'audio/ogg'],
    'extensions': ['.mp3', '.wav', '.ogg', '.mpeg']
}

IMAGE_FORMATS = {
    'mime_types': ['image/jpeg', 'image/png'],
    'extensions': ['.jpg', '.jpeg', '.png']
}

TEXT_FORMATS = {
    'mime_types': ['text/plain', 'application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'],
    'extensions': ['.txt', '.pdf', '.doc', '.docx']
}

DATA_FORMATS = {
    'mime_types': ['application/json', 'text/csv'],
    'extensions': ['.json', '.csv']
}

# Tipos MIME adicionales para cada tipo de archivo
AUDIO_MIME_TYPES_EXTRAS = ['audio/mp3', 'audio/flac', 'audio/x-m4a']
IMAGE_MIME_TYPES_EXTRAS = ['image/bmp', 'image/gif', 'image/tiff', 'image/webp']
TEXT_MIME_TYPES_EXTRAS = []
DATA_MIME_TYPES_EXTRAS = []

# Variable que contiene todas las extensiones permitidas para la validación
ALL_FORMATS = set(
    AUDIO_FORMATS['extensions'] +
    IMAGE_FORMATS['extensions'] +
    TEXT_FORMATS['extensions'] +
    DATA_FORMATS['extensions']
)

# Rutas dentro del bucket
PATHS = {
    'raw_storage': 'raw/storage/',
    'processing': 'processing/',
    'quarantine': 'quarantine/',
    'processed_results': 'processed/processed_results/',
    'processed_stacks': 'processed/stacks/',
    'processed_raw_reports': 'processed/raw_reports/'
}