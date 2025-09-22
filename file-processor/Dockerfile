# Usa la imagen base oficial para Cloud Functions en Python 3.11.
FROM python:3.11-slim

# Copia todos los archivos de tu proyecto al contenedor.
COPY . /app

# Establece el directorio de trabajo dentro del contenedor.
WORKDIR /app

# Agrega la carpeta de tu proyecto al PYTHONPATH para que encuentre tus módulos locales.
ENV PYTHONPATH=/app

# Instala las librerías de Python desde tu archivo requirements.txt.
RUN pip install -r requirements.txt


CMD ["functions-framework", "--target", "file_processor", "--port", "8080", "--signature-type", "cloudevent"]