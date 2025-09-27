# worker.py
import os
import django

# --- ESTE ES EL BLOQUE MÁGICO ---
# Le decimos a nuestro script dónde encontrar la configuración de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
# Cargamos la configuración de Django
django.setup()
# ---------------------------------

# Ahora que Django está configurado, podemos importar el resto.
from fastapi import FastAPI, UploadFile, File
from api.services.ai_detection import FacialRecognitionService, PlateDetectionService
import uvicorn

app = FastAPI()

# Esta parte necesita que Django esté cargado para acceder a los settings.
facial_service = FacialRecognitionService()
plate_service = PlateDetectionService()


@app.post("/recognize_face")
def recognize_face_endpoint(image: UploadFile = File(...)):
    # Pasamos el archivo directamente al servicio.
    result = facial_service.recognize_face_from_file(image.file)
    return result


@app.post("/detect_plate")
def detect_plate_endpoint(image: UploadFile = File(...)):
    result = plate_service.detect_plate_from_file(image.file)
    return result


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
