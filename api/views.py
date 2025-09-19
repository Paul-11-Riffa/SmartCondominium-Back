from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from .models import (
    Rol, Usuario, Propiedad, Multa, Pagos, Notificaciones, AreasComunes, Tareas,
    Vehiculo, Pertenece, ListaVisitantes, DetalleMulta, Factura, Finanzas,
    Comunicados, Horarios, Reserva, Asignacion, Envio, Registro, Bitacora
)
from .serializers import (
    RolSerializer, UsuarioSerializer, PropiedadSerializer, MultaSerializer,
    PagosSerializer, NotificacionesSerializer, AreasComunesSerializer, TareasSerializer,
    VehiculoSerializer, PerteneceSerializer, ListaVisitantesSerializer, DetalleMultaSerializer,
    FacturaSerializer, FinanzasSerializer, ComunicadosSerializer, HorariosSerializer,
    ReservaSerializer, AsignacionSerializer, EnvioSerializer, RegistroSerializer,
    BitacoraSerializer
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
