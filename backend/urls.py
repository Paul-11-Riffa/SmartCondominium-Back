# En el archivo: backend/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Esta única línea se encarga de todas las rutas de tu API.
    # Delega todo lo que empiece con 'api/' al archivo de URLs de tu app 'api'.
    path('api/', include('api.urls')),
]