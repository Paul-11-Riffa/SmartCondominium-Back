from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from django.utils import timezone
from datetime import timedelta
from .services.ai_detection import FacialRecognitionService, PlateDetectionService
from .services.supabase_storage import SupabaseStorageService
import logging
import base64
from rest_framework.parsers import MultiPartParser, FormParser
import traceback
import time

from .models import (
    Rol, Usuario, Propiedad, Multa, Pagos, Notificaciones, AreasComunes, Tareas,
    Vehiculo, Pertenece, ListaVisitantes, DetalleMulta, Factura, Finanzas,
    Comunicados, Horarios, Reserva, Asignacion, Envio, Registro, Bitacora,
    PerfilFacial, ReconocimientoFacial, DeteccionPlaca, ReporteSeguridad
)
from .serializers import (
    RolSerializer, UsuarioSerializer, PropiedadSerializer, MultaSerializer,
    PagosSerializer, NotificacionesSerializer, AreasComunesSerializer, TareasSerializer,
    VehiculoSerializer, PerteneceSerializer, ListaVisitantesSerializer, DetalleMultaSerializer,
    FacturaSerializer, FinanzasSerializer, ComunicadosSerializer, HorariosSerializer,
    ReservaSerializer, AsignacionSerializer, EnvioSerializer, RegistroSerializer,
    BitacoraSerializer, ReconocimientoFacialSerializer, PerfilFacialSerializer, DeteccionPlacaSerializer,
    ReporteSeguridadSerializer
)


# ---------------------------------------------------------------------
# Base genérica: agrega filtros, búsqueda y ordenamiento a todos
# ---------------------------------------------------------------------
class BaseModelViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # Cada viewset define: queryset, serializer_class, filterset_fields, search_fields, ordering_fields


# ---------------------------------------------------------------------
# Catálogos / tablas simples
# ---------------------------------------------------------------------
class RolViewSet(BaseModelViewSet):
    queryset = Rol.objects.all().order_by('id')
    serializer_class = RolSerializer
    filterset_fields = ['tipo', 'estado']
    search_fields = ['descripcion', 'tipo', 'estado']
    ordering_fields = ['id', 'tipo', 'estado']


class PropiedadViewSet(BaseModelViewSet):
    queryset = Propiedad.objects.all().order_by('codigo')
    serializer_class = PropiedadSerializer
    filterset_fields = ['nrocasa', 'piso', 'descripcion']
    search_fields = ['descripcion']
    ordering_fields = ['codigo', 'nrocasa', 'piso', 'tamano_m2']


class MultaViewSet(BaseModelViewSet):
    queryset = Multa.objects.all().order_by('id')
    serializer_class = MultaSerializer
    filterset_fields = ['monto']
    search_fields = ['descripcion']
    ordering_fields = ['id', 'monto']


class PagosViewSet(BaseModelViewSet):
    queryset = Pagos.objects.all().order_by('id')
    serializer_class = PagosSerializer
    filterset_fields = ['tipo', 'monto']
    search_fields = ['tipo', 'descripcion']
    ordering_fields = ['id', 'monto']


class NotificacionesViewSet(BaseModelViewSet):
    queryset = Notificaciones.objects.all().order_by('id')
    serializer_class = NotificacionesSerializer
    filterset_fields = ['tipo']
    search_fields = ['tipo', 'descripcion']
    ordering_fields = ['id']


class AreasComunesViewSet(BaseModelViewSet):
    queryset = AreasComunes.objects.all().order_by('id')
    serializer_class = AreasComunesSerializer
    filterset_fields = ['estado', 'capacidadmax', 'costo']
    search_fields = ['descripcion', 'estado']
    ordering_fields = ['id', 'capacidadmax', 'costo']


class TareasViewSet(BaseModelViewSet):
    queryset = Tareas.objects.all().order_by('id')
    serializer_class = TareasSerializer
    filterset_fields = ['tipo', 'vigencia', 'costos']
    search_fields = ['tipo', 'descripcion']
    ordering_fields = ['id', 'vigencia', 'costos']


class VehiculoViewSet(BaseModelViewSet):
    queryset = Vehiculo.objects.all().order_by('id')
    serializer_class = VehiculoSerializer
    filterset_fields = ['estado', 'nroplaca']
    search_fields = ['nroplaca', 'descripcion', 'estado']
    ordering_fields = ['id']


# ---------------------------------------------------------------------
# Entidades con FK
# ---------------------------------------------------------------------
class UsuarioViewSet(BaseModelViewSet):
    queryset = Usuario.objects.all().order_by('codigo')
    serializer_class = UsuarioSerializer
    filterset_fields = ['idrol', 'sexo', 'estado', 'correo', 'telefono']
    search_fields = ['nombre', 'apellido', 'correo', 'estado']
    ordering_fields = ['codigo', 'telefono']


class PerteneceViewSet(BaseModelViewSet):
    queryset = Pertenece.objects.all().order_by('id')
    serializer_class = PerteneceSerializer
    filterset_fields = ['codigousuario', 'codigopropiedad', 'fechaini', 'fechafin']
    search_fields = []
    ordering_fields = ['id', 'fechaini', 'fechafin']


class ListaVisitantesViewSet(BaseModelViewSet):
    queryset = ListaVisitantes.objects.all().order_by('id')
    serializer_class = ListaVisitantesSerializer
    filterset_fields = ['codigopropiedad', 'fechaini', 'fechafin', 'carnet']
    search_fields = ['nombre', 'apellido', 'carnet', 'motivovisita']
    ordering_fields = ['id', 'fechaini', 'fechafin']


class DetalleMultaViewSet(BaseModelViewSet):
    queryset = DetalleMulta.objects.all().order_by('id')
    serializer_class = DetalleMultaSerializer
    filterset_fields = ['codigo_propiedad', 'idmulta', 'fechaemi', 'fechalim']
    search_fields = []
    ordering_fields = ['id', 'fechaemi', 'fechalim']


class FacturaViewSet(BaseModelViewSet):
    queryset = Factura.objects.all().order_by('id')
    serializer_class = FacturaSerializer
    filterset_fields = ['codigousuario', 'idpago', 'fecha', 'estado', 'tipopago']
    search_fields = ['estado', 'tipopago']
    ordering_fields = ['id', 'fecha']


class FinanzasViewSet(BaseModelViewSet):
    queryset = Finanzas.objects.all().order_by('id')
    serializer_class = FinanzasSerializer
    filterset_fields = ['tipo', 'fecha', 'origen', 'idfactura']
    search_fields = ['tipo', 'descripcion', 'origen']
    ordering_fields = ['id', 'fecha', 'monto']


class ComunicadosViewSet(BaseModelViewSet):
    queryset = Comunicados.objects.all().order_by('id')
    serializer_class = ComunicadosSerializer
    filterset_fields = ['tipo', 'fecha', 'estado', 'codigousuario']
    search_fields = ['titulo', 'contenido', 'url', 'tipo', 'estado']
    ordering_fields = ['id', 'fecha']


class HorariosViewSet(BaseModelViewSet):
    queryset = Horarios.objects.all().order_by('id')
    serializer_class = HorariosSerializer
    filterset_fields = ['idareac', 'horaini', 'horafin']
    search_fields = []
    ordering_fields = ['id', 'horaini', 'horafin']


class ReservaViewSet(BaseModelViewSet):
    queryset = Reserva.objects.all().order_by('id')
    serializer_class = ReservaSerializer
    filterset_fields = ['codigousuario', 'idareac', 'fecha', 'estado']
    search_fields = ['estado']
    ordering_fields = ['id', 'fecha']


class AsignacionViewSet(BaseModelViewSet):
    queryset = Asignacion.objects.all().order_by('id')
    serializer_class = AsignacionSerializer
    filterset_fields = ['codigousuario', 'idtarea', 'fechaini', 'fechafin', 'estado']
    search_fields = ['descripcion', 'dificultades', 'estado']
    ordering_fields = ['id', 'fechaini', 'fechafin', 'costo']


class EnvioViewSet(BaseModelViewSet):
    queryset = Envio.objects.all().order_by('id')
    serializer_class = EnvioSerializer
    filterset_fields = ['codigousuario', 'idnotific', 'fecha', 'estado']
    search_fields = ['estado']
    ordering_fields = ['id', 'fecha']


class RegistroViewSet(BaseModelViewSet):
    queryset = Registro.objects.all().order_by('id')
    serializer_class = RegistroSerializer
    filterset_fields = ['codigousuario', 'idvehic', 'fecha']
    search_fields = []
    ordering_fields = ['id', 'fecha', 'hora']


class BitacoraViewSet(BaseModelViewSet):
    queryset = Bitacora.objects.all().order_by('-fecha', '-hora')
    serializer_class = BitacoraSerializer
    filterset_fields = ['codigousuario', 'fecha', 'accion', 'ip']
    search_fields = ['accion', 'ip']
    ordering_fields = ['id', 'fecha', 'hora']


# CU01. Iniciar sesion
class LoginView(APIView):
    permission_classes = [permissions.AllowAny]  # sin auth para poder loguear

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response({"detail": "email y password son requeridos."},
                            status=status.HTTP_400_BAD_REQUEST)

        # 1) Buscar en TU tabla Usuario
        try:
            u = Usuario.objects.get(correo=email)
        except Usuario.DoesNotExist:
            return Response({"detail": "Usuario no existe."}, status=status.HTTP_404_NOT_FOUND)

        # 2) Comparación simple (demo). En prod: NO uses texto plano.
        if u.contrasena != password:
            return Response({"detail": "Credenciales inválidas."}, status=status.HTTP_401_UNAUTHORIZED)

        # 3) Sincronizar/crear auth.User para usar TokenAuth
        dj_user, _ = User.objects.get_or_create(username=email, defaults={"email": email})
        if not dj_user.has_usable_password() or not dj_user.check_password(password):
            dj_user.set_password(password)
            dj_user.save()

        # 4) Crear/obtener token
        token, _ = Token.objects.get_or_create(user=dj_user)

        # 5) Armar payload con datos del usuario (y rol)
        rol_obj = None
        if u.idrol_id:
            try:
                r = Rol.objects.get(pk=u.idrol_id)
                rol_obj = {
                    "id": r.id,
                    "descripcion": r.descripcion,
                    "tipo": r.tipo,
                    "estado": r.estado,
                }
            except Rol.DoesNotExist:
                pass

        return Response({
            "token": token.key,
            "user": {
                "codigo": u.codigo,
                "nombre": u.nombre,
                "apellido": u.apellido,
                "correo": u.correo,
                "sexo": u.sexo,
                "telefono": u.telefono,
                "estado": u.estado,
                "idrol": u.idrol_id,
                "rol": rol_obj,
            }
        }, status=status.HTTP_200_OK)

# CU02. Registrarse en el sistema
class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        data = request.data.copy()

        # Validaciones mínimas
        required = ["nombre", "apellido", "correo", "contrasena"]
        missing = [f for f in required if not data.get(f)]
        if missing:
            return Response(
                {"detail": f"Faltan campos requeridos: {', '.join(missing)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # ¿correo ya existe?
        if Usuario.objects.filter(correo=data["correo"]).exists():
            return Response(
                {"detail": "El correo ya está registrado."},
                status=status.HTTP_409_CONFLICT
            )

        # ---- Defaults solo si NO vienen desde el front ----
        # estado: si no viene o viene vacío => "pendiente"
        estado = (data.get("estado") or "").strip()
        if not estado:
            data["estado"] = "pendiente"

        # idrol: si no viene => 2
        if data.get("idrol") in [None, "", 0, "0"]:
            data["idrol"] = 2
        # (opcional) convertir a int si vino en string
        try:
            data["idrol"] = int(data["idrol"])
        except Exception:
            return Response({"detail": "idrol debe ser numérico."}, status=status.HTTP_400_BAD_REQUEST)

        # Crea Usuario con serializer general
        serializer = UsuarioSerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        u = serializer.save()  # Usuario creado

        # Sincroniza auth.User (para emitir token y usar TokenAuth)
        dj_user, created = User.objects.get_or_create(
            username=u.correo,
            defaults={"email": u.correo, "first_name": u.nombre, "last_name": u.apellido},
        )
        dj_user.set_password(data["contrasena"])  # hash en Django
        dj_user.is_active = True
        dj_user.save()

        token, _ = Token.objects.get_or_create(user=dj_user)

        # Info de rol (si existe)
        rol_obj = None
        if u.idrol_id:
            try:
                r = Rol.objects.get(pk=u.idrol_id)
                rol_obj = {
                    "id": r.id,
                    "descripcion": r.descripcion,
                    "tipo": r.tipo,
                    "estado": r.estado,
                }
            except Rol.DoesNotExist:
                pass

        return Response({
            "token": token.key,
            "user": {
                "codigo": u.codigo,
                "nombre": u.nombre,
                "apellido": u.apellido,
                "correo": u.correo,
                "sexo": u.sexo,
                "telefono": u.telefono,
                "estado": u.estado,    # lo que mandó el front o "pendiente"
                "idrol": u.idrol_id,   # lo que mandó el front o 2
                "rol": rol_obj,
            }
        }, status=status.HTTP_201_CREATED)

# CU04. Cierre de sesion
class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        # Si el cliente envía Authorization: Token <...>, DRF pone el token en request.auth
        all_sessions = bool(request.data.get("all", False))

        if all_sessions:
            Token.objects.filter(user=request.user).delete()
            detail = "Sesiones cerradas en todos los dispositivos."
        else:
            # Borra SOLO el token de esta sesión
            try:
                if request.auth:
                    request.auth.delete()
            except Exception:
                # si ya estaba borrado/no válido, seguimos devolviendo 200 para idempotencia
                pass
            detail = "Sesión cerrada."

        return Response({"detail": detail}, status=status.HTTP_200_OK)

# Agregar estos ViewSets al final de api/views.py, después de LogoutView y antes de AIDetectionViewSet:

class ReconocimientoFacialViewSet(BaseModelViewSet):
    queryset = ReconocimientoFacial.objects.all().order_by('-fecha_deteccion')
    serializer_class = ReconocimientoFacialSerializer
    filterset_fields = ['codigo_usuario', 'es_residente', 'ubicacion_camara', 'estado', 'fecha_deteccion']
    search_fields = ['ubicacion_camara', 'estado']
    ordering_fields = ['id', 'fecha_deteccion', 'confianza']


class DeteccionPlacaViewSet(BaseModelViewSet):
    queryset = DeteccionPlaca.objects.all().order_by('-fecha_deteccion')
    serializer_class = DeteccionPlacaSerializer
    filterset_fields = ['placa_detectada', 'vehiculo', 'es_autorizado', 'ubicacion_camara', 'tipo_acceso', 'fecha_deteccion']
    search_fields = ['placa_detectada', 'ubicacion_camara', 'tipo_acceso']
    ordering_fields = ['id', 'fecha_deteccion', 'confianza']


class PerfilFacialViewSet(BaseModelViewSet):
    queryset = PerfilFacial.objects.all().order_by('-fecha_registro')
    serializer_class = PerfilFacialSerializer
    filterset_fields = ['codigo_usuario', 'activo', 'fecha_registro']
    search_fields = ['codigo_usuario__nombre', 'codigo_usuario__apellido', 'codigo_usuario__correo']
    ordering_fields = ['id', 'fecha_registro']


class ReporteSeguridadViewSet(BaseModelViewSet):
    queryset = ReporteSeguridad.objects.all().order_by('-fecha_evento')
    serializer_class = ReporteSeguridadSerializer
    filterset_fields = ['tipo_evento', 'nivel_alerta', 'revisado', 'revisor', 'fecha_evento']
    search_fields = ['descripcion', 'tipo_evento', 'nivel_alerta']
    ordering_fields = ['id', 'fecha_evento', 'nivel_alerta']


logger = logging.getLogger(__name__)


class AIDetectionViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.facial_service = FacialRecognitionService()
        self.plate_service = PlateDetectionService()
        self.storage_service = SupabaseStorageService()

    # ============= RECONOCIMIENTO FACIAL =============
    @action(detail=False, methods=['post'])
    def recognize_face(self, request):
        try:
            # Obtener imagen del FormData
            image_file = request.FILES.get('image')
            camera_location = request.data.get('camera_location', 'Principal')

            if not image_file:
                return Response(
                    {'error': 'La imagen es requerida como archivo'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            logger.info(f"Procesando reconocimiento facial - cámara: {camera_location}")

            # USAR EL NUEVO MÉTODO QUE MANEJA ARCHIVOS DIRECTAMENTE
            result = self.facial_service.recognize_face_from_file(image_file, camera_location)

            # Crear reporte de seguridad si es necesario
            if not result['is_resident']:
                ReporteSeguridad.objects.create(
                    tipo_evento='intruso_detectado',
                    reconocimiento_facial_id=result['id'],
                    descripcion=f"Persona no identificada detectada en {camera_location}",
                    nivel_alerta='alto'
                )

            logger.info(f"Reconocimiento completado - residente: {result['is_resident']}")
            return Response(result, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error en reconocimiento facial: {e}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            return Response(
                {'error': 'Error interno del servidor'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    # ============= REGISTRO DE PERFILES FACIALES =============
    @action(detail=False, methods=['post'])
    def register_profile(self, request):
        """Registra un nuevo perfil facial para un usuario específico"""
        try:
            user_id = request.data.get('user_id')
            image_file = request.FILES.get('image')

            if not user_id or not image_file:
                return Response({
                    'success': False,
                    'error': 'user_id e imagen son requeridos'
                }, status=status.HTTP_400_BAD_REQUEST)

            # Verificar que el usuario existe
            try:
                usuario = Usuario.objects.get(codigo=user_id)
            except Usuario.DoesNotExist:
                return Response({
                    'success': False,
                    'error': 'Usuario no encontrado'
                }, status=status.HTTP_404_NOT_FOUND)

            # USAR EL NUEVO MÉTODO QUE MANEJA ARCHIVOS DIRECTAMENTE
            success = self.facial_service.register_face_from_file(int(user_id), image_file)

            if success:
                # Obtener el perfil creado
                perfil = PerfilFacial.objects.get(codigo_usuario=usuario)

                return Response({
                    'success': True,
                    'message': f'Perfil facial registrado exitosamente para {usuario.nombre} {usuario.apellido}',
                    'profile_id': perfil.id,
                    'user': {
                        'codigo': usuario.codigo,
                        'nombre': usuario.nombre,
                        'apellido': usuario.apellido,
                        'correo': usuario.correo
                    },
                    'image_url': perfil.imagen_url
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    'success': False,
                    'error': 'No se pudo registrar el perfil facial'
                }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.error(f"Error registrando perfil facial: {str(e)}")
            return Response({
                'success': False,
                'error': f'Error interno del servidor: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    @action(detail=False, methods=['post'])
    def register_current_user(self, request):
        """Registra perfil facial del usuario autenticado actual"""
        try:
            # Obtener imagen del FormData
            image_file = request.FILES.get('image')

            logger.info(f"Datos recibidos - image_file: {'Si' if image_file else 'No'}")

            if not image_file:
                return Response({
                    'success': False,
                    'error': 'La imagen es requerida como archivo'
                }, status=status.HTTP_400_BAD_REQUEST)

            # Obtener usuario autenticado desde token
            try:
                usuario = Usuario.objects.get(correo=request.user.email)
                logger.info(f"Usuario encontrado: {usuario.nombre} {usuario.apellido}")
            except Usuario.DoesNotExist:
                return Response({
                    'success': False,
                    'error': 'Usuario no encontrado en el sistema'
                }, status=status.HTTP_404_NOT_FOUND)

            # Verificar si ya tiene un perfil registrado
            existing_profile = PerfilFacial.objects.filter(codigo_usuario=usuario, activo=True).first()
            if existing_profile:
                logger.info(f"Usuario ya tiene perfil facial: {existing_profile.id}")
                return Response({
                    'success': False,
                    'error': 'Ya tienes un perfil facial registrado. Elimínalo primero si quieres crear uno nuevo.'
                }, status=status.HTTP_400_BAD_REQUEST)

            # USAR EL NUEVO MÉTODO QUE MANEJA ARCHIVOS DIRECTAMENTE
            success = self.facial_service.register_face_from_file(usuario.codigo, image_file)

            if success:
                # Obtener el perfil creado por el servicio
                profile = PerfilFacial.objects.get(codigo_usuario=usuario, activo=True)

                logger.info(f"Perfil facial creado exitosamente: {profile.id}")

                return Response({
                    'success': True,
                    'message': f'Perfil facial registrado exitosamente para {usuario.nombre}',
                    'profile_id': profile.id,
                    'user': {
                        'codigo': usuario.codigo,
                        'nombre': usuario.nombre,
                        'apellido': usuario.apellido,
                        'correo': usuario.correo
                    },
                    'image_url': profile.imagen_url
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    'success': False,
                    'error': 'No se pudo registrar el perfil facial. Verifica que la imagen contenga una cara visible.'
                }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.error(f"Error registrando perfil del usuario actual: {str(e)}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            return Response({
                'success': False,
                'error': 'Error interno del servidor'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



    @action(detail=False, methods=['get'])
    def list_profiles(self, request):
        """Lista todos los perfiles faciales registrados"""
        try:
            profiles = PerfilFacial.objects.filter(activo=True).select_related('codigo_usuario')

            profiles_data = []
            for profile in profiles:
                profiles_data.append({
                    'id': profile.id,
                    'user_id': profile.codigo_usuario.codigo,
                    'user_name': f"{profile.codigo_usuario.nombre} {profile.codigo_usuario.apellido}",
                    'user_email': profile.codigo_usuario.correo,
                    'image_url': profile.imagen_url,
                    'fecha_registro': profile.fecha_registro.isoformat(),
                    'activo': profile.activo
                })

            return Response({
                'success': True,
                'profiles': profiles_data,
                'count': len(profiles_data)
            }, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error listando perfiles: {str(e)}")
            return Response({
                'success': False,
                'error': 'Error interno del servidor',
                'profiles': [],
                'count': 0
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Y la función delete_profile:

    @action(detail=True, methods=['delete'])
    def delete_profile(self, request, pk=None):
        """Elimina un perfil facial específico"""
        try:
            profile = PerfilFacial.objects.get(id=pk, activo=True)

            # Verificar que el usuario puede eliminar este perfil
            # (solo el propietario o un admin)
            usuario = Usuario.objects.get(correo=request.user.email)
            if profile.codigo_usuario != usuario and not request.user.is_staff:
                return Response({
                    'success': False,
                    'message': 'No tienes permisos para eliminar este perfil'
                }, status=status.HTTP_403_FORBIDDEN)

            # Marcar como inactivo en lugar de eliminar
            profile.activo = False
            profile.save()

            # Opcionalmente, eliminar imagen de Supabase
            try:
                from supabase import create_client, Client
                import os

                supabase_url = os.getenv('SUPABASE_URL')
                supabase_key = os.getenv('SUPABASE_ANON_KEY')
                supabase: Client = create_client(supabase_url, supabase_key)

                if profile.imagen_path:
                    supabase.storage.from_('ai-detection-images').remove([profile.imagen_path])
                    logger.info(f"Imagen eliminada de Supabase: {profile.imagen_path}")
            except Exception as e:
                logger.warning(f"Error eliminando imagen de Supabase: {str(e)}")

            logger.info(f"Perfil facial eliminado: {profile.id}")

            return Response({
                'success': True,
                'message': 'Perfil facial eliminado correctamente'
            }, status=status.HTTP_200_OK)

        except PerfilFacial.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Perfil facial no encontrado'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error eliminando perfil: {str(e)}")
            return Response({
                'success': False,
                'message': 'Error interno del servidor'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




    @action(detail=False, methods=['get'])
    def list_profiles(self, request):
        """Lista todos los perfiles faciales registrados"""
        try:
            perfiles = PerfilFacial.objects.select_related('codigo_usuario').filter(activo=True)

            profiles_data = []
            for perfil in perfiles:
                profiles_data.append({
                    'id': perfil.id,
                    'user_id': perfil.codigo_usuario.codigo,
                    'user_name': f"{perfil.codigo_usuario.nombre} {perfil.codigo_usuario.apellido}",
                    'user_email': perfil.codigo_usuario.correo,
                    'image_url': perfil.imagen_url,
                    'fecha_registro': perfil.fecha_registro.isoformat(),
                    'activo': perfil.activo
                })

            return Response({
                'success': True,
                'profiles': profiles_data,
                'count': len(profiles_data)
            }, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error obteniendo perfiles: {str(e)}")
            return Response({
                'success': False,
                'error': 'Error obteniendo perfiles'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['delete'])
    def delete_profile(self, request, pk=None):
        """Elimina un perfil facial"""
        try:
            perfil = PerfilFacial.objects.get(id=pk)

            # Eliminar imagen de Supabase Storage
            if perfil.imagen_path:
                self.storage_service.delete_file(perfil.imagen_path)

            # Eliminar registro
            user_name = f"{perfil.codigo_usuario.nombre} {perfil.codigo_usuario.apellido}"
            perfil.delete()

            # Recargar perfiles faciales en el servicio
            self.facial_service.load_known_faces()

            return Response({
                'success': True,
                'message': f'Perfil facial de {user_name} eliminado exitosamente'
            }, status=status.HTTP_200_OK)

        except PerfilFacial.DoesNotExist:
            return Response({
                'success': False,
                'error': 'Perfil no encontrado'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error eliminando perfil: {str(e)}")
            return Response({
                'success': False,
                'error': 'Error eliminando perfil'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # ============= DETECCIÓN DE PLACAS =============
    @action(detail=False, methods=['post'])
    def detect_plate(self, request):
        try:
            # Obtener datos del FormData
            image_file = request.FILES.get('image')
            camera_location = request.data.get('camera_location', 'Estacionamiento')
            access_type = request.data.get('access_type', 'entrada')

            if not image_file:
                return Response(
                    {'error': 'La imagen es requerida como archivo'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            logger.info(f"Procesando detección de placa - cámara: {camera_location}, tipo: {access_type}")

            # USAR EL NUEVO MÉTODO QUE MANEJA ARCHIVOS DIRECTAMENTE
            result = self.plate_service.detect_plate_from_file(
                image_file, camera_location, access_type
            )

            # Crear reporte de seguridad si la placa no está autorizada
            if result['plate'] and not result['is_authorized']:
                ReporteSeguridad.objects.create(
                    tipo_evento='placa_no_autorizada',
                    deteccion_placa_id=result['id'],
                    descripcion=f"Placa no autorizada detectada: {result['plate']} en {camera_location}",
                    nivel_alerta='medio'
                )

            logger.info(f"Detección completada - placa: {result.get('plate', 'No detectada')}")
            return Response(result, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error en detección de placa: {e}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            return Response(
                {'error': 'Error interno del servidor'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    # ============= ESTADÍSTICAS =============
    @action(detail=False, methods=['get'])
    def detection_stats(self, request):
        try:
            now = timezone.now()
            last_24h = now - timedelta(hours=24)
            last_week = now - timedelta(days=7)

            stats = {
                'facial_recognitions_today': ReconocimientoFacial.objects.filter(
                    fecha_deteccion__gte=last_24h
                ).count(),
                'plate_detections_today': DeteccionPlaca.objects.filter(
                    fecha_deteccion__gte=last_24h
                ).count(),
                'residents_detected_today': ReconocimientoFacial.objects.filter(
                    fecha_deteccion__gte=last_24h,
                    es_residente=True
                ).count(),
                'unauthorized_plates_today': DeteccionPlaca.objects.filter(
                    fecha_deteccion__gte=last_24h,
                    es_autorizado=False
                ).count(),
                'security_alerts_week': ReporteSeguridad.objects.filter(
                    fecha_evento__gte=last_week,
                    nivel_alerta__in=['alto', 'critico']
                ).count(),
                'registered_faces': PerfilFacial.objects.filter(activo=True).count()
            }

            return Response(stats, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error obteniendo estadísticas: {e}")
            return Response(
                {'error': 'Error interno del servidor'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )