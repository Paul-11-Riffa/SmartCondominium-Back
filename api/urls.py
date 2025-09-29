# Contenido para: api/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RolViewSet, UsuarioViewSet, PropiedadViewSet, MultaViewSet, PagoViewSet,
    NotificacionesViewSet, AreasComunesViewSet, TareasViewSet, VehiculoViewSet,
    PerteneceViewSet, ListaVisitantesViewSet, DetalleMultaViewSet, FacturaViewSet,
    FinanzasViewSet, ComunicadosViewSet, HorariosViewSet, ReservaViewSet, SolicitudMantenimientoViewSet,
    AsignacionViewSet, EnvioViewSet, RegistroViewSet, BitacoraViewSet,
    LoginView, RegisterView, LogoutView, AIDetectionViewSet, ReconocimientoFacialViewSet, DeteccionPlacaViewSet,
    PerfilFacialViewSet, ReporteSeguridadViewSet, EstadoCuentaView, ComprobantePDFView,
    ReporteUsoAreasComunesView, test_view, MantenimientoPreventivoViewSet, ReporteBitacoraView, PagarCuotaView,
    StripeWebhookView, HistorialPagosView, MisNotificacionesView
)

router = DefaultRouter()
# --- Registros del Router (ViewSets genéricos) ---
router.register(r'roles', RolViewSet)
router.register(r'usuarios', UsuarioViewSet)
# ... (y todos los demás router.register que ya tienes)
router.register(r'mantenimientos-preventivos', MantenimientoPreventivoViewSet, basename='mantenimiento-preventivo')

# --- ESTA ES LA ESTRUCTURA CORRECTA Y DEFINITIVA ---
urlpatterns = [
    # --- 1. TODAS las rutas personalizadas (que no son del router) van PRIMERO ---
    path('auth/login/', LoginView.as_view(), name='auth-login'),
    path('auth/register/', RegisterView.as_view(), name='auth-register'),
    path('auth/logout/', LogoutView.as_view(), name='auth-logout'),
    path("estado-cuenta/", EstadoCuentaView.as_view(), name="estado-cuenta"),
    path('comprobante/<int:pk>/', ComprobantePDFView.as_view(), name='comprobante-pdf'),
    path("reporte/areas-comunes/", ReporteUsoAreasComunesView.as_view(), name="reporte-uso-areas"),
    path("reporte/bitacora/", ReporteBitacoraView.as_view(), name="reporte-bitacora"),
    path("pagar-cuota/", PagarCuotaView.as_view(), name="pagar-cuota"),
    path("stripe-webhook/", StripeWebhookView.as_view(), name="stripe-webhook"),
    path("historial-pagos/", HistorialPagosView.as_view(), name="historial-pagos"),
    path("mis-notificaciones/", MisNotificacionesView.as_view(), name="mis-notificaciones"),
    path("test/", test_view, name="test-view"),

    # --- 2. El enrutador genérico (la "red") va AL FINAL de todas las demás ---
    path('', include(router.urls)),
]