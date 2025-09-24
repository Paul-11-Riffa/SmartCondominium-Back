# En api/permissions.py

from rest_framework import permissions
from .models import Usuario

class IsAdmin(permissions.BasePermission):
    """
    Permiso personalizado para permitir acceso solo a usuarios con rol de administrador.
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        try:
            # Verificamos en nuestro modelo Usuario si el rol es de tipo 'admin'
            usuario = Usuario.objects.get(correo=request.user.email)
            return usuario.idrol and usuario.idrol.tipo == 'admin'
        except Usuario.DoesNotExist:
            return False

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Permiso para permitir que solo los admins creen/editen, pero todos lean.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        # Para métodos no seguros (POST, PUT, DELETE), usamos nuestra lógica IsAdmin.
        if not request.user or not request.user.is_authenticated:
            return False
        try:
            usuario = Usuario.objects.get(correo=request.user.email)
            return usuario.idrol and usuario.idrol.tipo == 'admin'
        except Usuario.DoesNotExist:
            return False