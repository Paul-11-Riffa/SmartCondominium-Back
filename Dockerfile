# Usamos una imagen base de Python
FROM python:3.11-slim

# Instalamos las dependencias del sistema operativo que dlib y opencv necesitan
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libgtk2.0-dev \
    pkg-config \
    libavcodec-dev \
    libavformat-dev \
    libswscale-dev \
    && rm -rf /var/lib/apt/lists/*

# Establecemos el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiamos el archivo de requisitos e instalamos las dependencias de Python
# Esto es lo que consume mucha memoria, pero lo haremos en tu PC, no en Render.
COPY requirements.txt .
RUN pip install --default-timeout=300 --no-cache-dir -r requirements.txt

# Copiamos el resto del código de tu aplicación al contenedor
COPY . .

# El comando que se ejecutará cuando Render inicie el contenedor
# Render nos dará el puerto a través de la variable $PORT
CMD ["uvicorn", "worker:app", "--host", "0.0.0.0", "--port", "10000"]