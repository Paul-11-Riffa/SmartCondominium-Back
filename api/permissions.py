# En: api/permissions.py

from rest_framework import permissions
from .models import Usuario

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Permiso personalizado para permitir que solo los administradores creen/editen/borren.
    El resto de los usuarios (residentes) solo tendrán acceso de lectura.
    """
    def has_permission(self, request, view):
        # Los permisos de lectura (GET, HEAD, OPTIONS) se permiten a cualquier usuario autenticado.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Los permisos de escritura (POST, PUT, DELETE) solo se permiten si el usuario es un administrador.
        try:
            # Buscamos al usuario en nuestro modelo Usuario para verificar su rol
            usuario = Usuario.objects.get(correo=request.user.email)
            return usuario.idrol and usuario.idrol.tipo == 'admin'
        except Usuario.DoesNotExist:
            return False