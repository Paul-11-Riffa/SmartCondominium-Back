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
    StripeWebhookView, HistorialPagosView, MisNotificacionesView, ActualizarFotoPerfilView, MiPropiedadView,
)

router = DefaultRouter()
# --- Registros del Router (ViewSets genéricos) ---
router.register(r'roles', RolViewSet)
router.register(r'usuarios', UsuarioViewSet)
router.register(r'propiedades', PropiedadViewSet)
router.register(r'multas', MultaViewSet, basename='multas')
router.register(r'pagos', PagoViewSet, basename='pagos')
router.register(r'notificaciones', NotificacionesViewSet)
router.register(r'areas-comunes', AreasComunesViewSet)
router.register(r'tareas', TareasViewSet)
router.register(r'vehiculos', VehiculoViewSet, basename='vehiculo')
router.register(r'pertenece', PerteneceViewSet)
router.register(r'lista-visitantes', ListaVisitantesViewSet)
router.register(r'detalle-multa', DetalleMultaViewSet)
router.register(r'facturas', FacturaViewSet)
router.register(r'finanzas', FinanzasViewSet)
router.register(r'comunicados', ComunicadosViewSet)
router.register(r'horarios', HorariosViewSet)
router.register(r'reservas', ReservaViewSet)
router.register(r'asignaciones', AsignacionViewSet)
router.register(r'envios', EnvioViewSet)
router.register(r'registros', RegistroViewSet)
router.register(r'solicitudes-mantenimiento', SolicitudMantenimientoViewSet, basename='solicitud-mantenimiento')
router.register(r'bitacora', BitacoraViewSet)
router.register(r'ai-detection', AIDetectionViewSet, basename='ai-detection')
router.register(r'reconocimientos-faciales', ReconocimientoFacialViewSet)
router.register(r'detecciones-placas', DeteccionPlacaViewSet)
router.register(r'perfiles-faciales', PerfilFacialViewSet)
router.register(r'reportes-seguridad', ReporteSeguridadViewSet)
router.register(r'mantenimientos-preventivos', MantenimientoPreventivoViewSet, basename='mantenimiento-preventivo')

# --- Lista de URLs ---
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
    path("mi-propiedad/", MiPropiedadView.as_view(), name="mi-propiedad"),
    path('usuario/actualizar-foto/', ActualizarFotoPerfilView.as_view(), name='actualizar-foto-perfil'),

    # --- 2. El enrutador genérico (la "red") va AL FINAL de todas las demás ---
    path('', include(router.urls)),
]
