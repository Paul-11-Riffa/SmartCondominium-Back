from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    RolViewSet, UsuarioViewSet, PropiedadViewSet, MultaViewSet, PagosViewSet,
    NotificacionesViewSet, AreasComunesViewSet, TareasViewSet, VehiculoViewSet,
    PerteneceViewSet, ListaVisitantesViewSet, DetalleMultaViewSet, FacturaViewSet,
    FinanzasViewSet, ComunicadosViewSet, HorariosViewSet, ReservaViewSet,
    AsignacionViewSet, EnvioViewSet, RegistroViewSet, BitacoraViewSet,
    LoginView, RegisterView, LogoutView
)

router = DefaultRouter()
router.register(r'roles', RolViewSet)
router.register(r'usuarios', UsuarioViewSet)
router.register(r'propiedades', PropiedadViewSet)
router.register(r'multas', MultaViewSet)
router.register(r'pagos', PagosViewSet)
router.register(r'notificaciones', NotificacionesViewSet)
router.register(r'areas-comunes', AreasComunesViewSet)
router.register(r'tareas', TareasViewSet)
router.register(r'vehiculos', VehiculoViewSet)
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
router.register(r'bitacora', BitacoraViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/login/', LoginView.as_view(), name='auth-login'),
    path('auth/register/', RegisterView.as_view(), name='auth-register'),
    path('auth/logout/', LogoutView.as_view(), name='auth-logout'),

]
