# api/services/supabase_storage.py
import base64
import io
import uuid
from datetime import datetime
from typing import Optional, Dict, Any
from PIL import Image
from supabase import create_client, Client
from django.conf import settings
import logging
from django.core.files.uploadedfile import InMemoryUploadedFile

logger = logging.getLogger(__name__)


class SupabaseStorageService:
    """Servicio para manejar almacenamiento de imágenes en Supabase Storage"""

    def __init__(self):
        self.supabase: Client = create_client(
            settings.SUPABASE_URL,
            settings.SUPABASE_SERVICE_KEY
        )
        self.bucket_name = settings.SUPABASE_STORAGE_BUCKET
        self._ensure_bucket_exists()

    def _ensure_bucket_exists(self):
        """Asegura que el bucket existe"""
        try:
            buckets = self.supabase.storage.list_buckets()
            bucket_exists = any(bucket.name == self.bucket_name for bucket in buckets)

            if not bucket_exists:
                self.supabase.storage.create_bucket(
                    self.bucket_name,
                    options={"public": True}
                )
                logger.info(f"Bucket '{self.bucket_name}' creado exitosamente")

        except Exception as e:
            logger.error(f"Error verificando/creando bucket: {e}")

    def upload_base64_image(self, base64_string: str, folder: str, prefix: str = "img") -> Optional[Dict[str, Any]]:
        """Sube una imagen Base64 a Supabase Storage"""
        try:
            processed_image = self._process_base64_image(base64_string)
            if not processed_image:
                return None

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            unique_id = uuid.uuid4().hex[:8]
            filename = f"{prefix}_{timestamp}_{unique_id}.jpg"
            file_path = f"{folder}/{filename}"

            response = self.supabase.storage.from_(self.bucket_name).upload(
                file_path,
                processed_image,
                file_options={
                    "content-type": "image/jpeg",
                    "cache-control": "3600"
                }
            )

            if response:
                public_url = self.get_public_url(file_path)

                return {
                    'file_path': file_path,
                    'public_url': public_url,
                    'filename': filename,
                    'folder': folder,
                    'size_bytes': len(processed_image)
                }

            return None

        except Exception as e:
            logger.error(f"Error subiendo imagen a Supabase: {e}")
            return None

    def _process_base64_image(self, base64_string: str) -> Optional[bytes]:
        """Procesa y optimiza imagen Base64"""
        try:
            if base64_string.startswith('data:image'):
                base64_string = base64_string.split(',', 1)[1]

            image_data = base64.b64decode(base64_string)
            image = Image.open(io.BytesIO(image_data))

            if image.mode != 'RGB':
                image = image.convert('RGB')

            max_size = settings.AI_IMAGE_SETTINGS['THUMBNAIL_SIZE']
            image.thumbnail(max_size, Image.Resampling.LANCZOS)

            output = io.BytesIO()
            image.save(
                output,
                format='JPEG',
                quality=settings.AI_IMAGE_SETTINGS['JPEG_QUALITY'],
                optimize=True
            )

            return output.getvalue()

        except Exception as e:
            logger.error(f"Error procesando imagen Base64: {e}")
            return None

    def get_public_url(self, file_path: str) -> str:
        """Obtiene URL pública de un archivo"""
        return f"{settings.SUPABASE_STORAGE_URL}/{file_path}"

    def delete_file(self, file_path: str) -> bool:
        """Elimina un archivo del storage"""
        try:
            response = self.supabase.storage.from_(self.bucket_name).remove([file_path])
            return len(response) > 0
        except Exception as e:
            logger.error(f"Error eliminando archivo {file_path}: {e}")
            return False

    def upload_django_file(self, django_file: InMemoryUploadedFile, folder: str, prefix: str = "img") -> Optional[
        Dict[str, Any]]:
        """Sube un archivo Django a Supabase Storage"""
        try:
            # Leer y procesar el archivo
            django_file.seek(0)  # Asegurar que estamos al inicio
            file_data = django_file.read()

            # Procesar la imagen
            processed_image = self._process_django_file_data(file_data)
            if not processed_image:
                return None

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            unique_id = uuid.uuid4().hex[:8]
            filename = f"{prefix}_{timestamp}_{unique_id}.jpg"
            file_path = f"{folder}/{filename}"

            response = self.supabase.storage.from_(self.bucket_name).upload(
                file_path,
                processed_image,
                file_options={
                    "content-type": "image/jpeg",
                    "cache-control": "3600"
                }
            )

            if response:
                public_url = self.get_public_url(file_path)

                return {
                    'file_path': file_path,
                    'public_url': public_url,
                    'filename': filename,
                    'folder': folder,
                    'size_bytes': len(processed_image)
                }

            return None

        except Exception as e:
            logger.error(f"Error subiendo archivo Django a Supabase: {e}")
            return None

    def _process_django_file_data(self, file_data: bytes) -> Optional[bytes]:
        """Procesa y optimiza datos de archivo Django"""
        try:
            image = Image.open(io.BytesIO(file_data))

            if image.mode != 'RGB':
                image = image.convert('RGB')

            max_size = settings.AI_IMAGE_SETTINGS['THUMBNAIL_SIZE']
            image.thumbnail(max_size, Image.Resampling.LANCZOS)

            output = io.BytesIO()
            image.save(
                output,
                format='JPEG',
                quality=settings.AI_IMAGE_SETTINGS['JPEG_QUALITY'],
                optimize=True
            )

            return output.getvalue()

        except Exception as e:
            logger.error(f"Error procesando datos de archivo Django: {e}")
            return None