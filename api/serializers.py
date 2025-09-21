from rest_framework import serializers
from .models import (
    Rol, Usuario, Propiedad, Multa, Pagos, Notificaciones, AreasComunes, Tareas,
    Vehiculo, Pertenece, ListaVisitantes, DetalleMulta, Factura, Finanzas,
    Comunicados, Horarios, Reserva, Asignacion, Envio, Registro, Bitacora,
    PerfilFacial, ReconocimientoFacial, DeteccionPlaca, ReporteSeguridad
)


class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = "__all__"


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = "__all__"


class PropiedadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Propiedad
        fields = "__all__"


class MultaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Multa
        fields = "__all__"


class PagosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pagos
        fields = "__all__"


class NotificacionesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notificaciones
        fields = "__all__"


class AreasComunesSerializer(serializers.ModelSerializer):
    class Meta:
        model = AreasComunes
        fields = "__all__"


class TareasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tareas
        fields = "__all__"


class VehiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehiculo
        fields = "__all__"


class PerteneceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pertenece
        fields = "__all__"


class ListaVisitantesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListaVisitantes
        fields = "__all__"


class DetalleMultaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleMulta
        fields = "__all__"


class FacturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Factura
        fields = "__all__"


class FinanzasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Finanzas
        fields = "__all__"


class ComunicadosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comunicados
        fields = "__all__"


class HorariosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Horarios
        fields = "__all__"


class ReservaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reserva
        fields = "__all__"


class AsignacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asignacion
        fields = "__all__"


class EnvioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Envio
        fields = "__all__"


class RegistroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registro
        fields = "__all__"


class BitacoraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bitacora
        fields = "__all__"


# Agregar al final de api/serializers.py

class PerfilFacialSerializer(serializers.ModelSerializer):
    usuario_nombre = serializers.SerializerMethodField()

    class Meta:
        model = PerfilFacial
        fields = ['id', 'codigo_usuario', 'imagen_url', 'fecha_registro', 'activo', 'usuario_nombre']

    def get_usuario_nombre(self, obj):
        return f"{obj.codigo_usuario.nombre} {obj.codigo_usuario.apellido}"


class ReconocimientoFacialSerializer(serializers.ModelSerializer):
    usuario_nombre = serializers.SerializerMethodField()

    class Meta:
        model = ReconocimientoFacial
        fields = "__all__"

    def get_usuario_nombre(self, obj):
        if obj.codigo_usuario:
            return f"{obj.codigo_usuario.nombre} {obj.codigo_usuario.apellido}"
        return "Desconocido"


class DeteccionPlacaSerializer(serializers.ModelSerializer):
    vehiculo_info = serializers.SerializerMethodField()

    class Meta:
        model = DeteccionPlaca
        fields = "__all__"

    def get_vehiculo_info(self, obj):
        if obj.vehiculo:
            return {
                'id': obj.vehiculo.id,
                'descripcion': obj.vehiculo.descripcion,
                'estado': obj.vehiculo.estado
            }
        return None


class ReporteSeguridadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReporteSeguridad
        fields = "__all__"