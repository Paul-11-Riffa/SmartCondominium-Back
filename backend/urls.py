from django.contrib import admin
from django.urls import path, include
from api.views import ComprobantePDFView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),   # <--- monta todos los endpoints
    path('api/comprobante/<int:pk>/', ComprobantePDFView.as_view(), name='comprobante-pdf'),
]
