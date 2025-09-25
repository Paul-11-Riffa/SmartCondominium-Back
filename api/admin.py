from django.contrib import admin
# Importar todos los modelos que quieres ver en el admin
from .models import (
    Rol, Usuario, Propiedad, Pertenece, ListaVisitantes, Multa, Pagos,
    AreasComunes, Reserva
)

# Registrar los modelos para que aparezcan en el panel
admin.site.register(Rol)
admin.site.register(Usuario)
admin.site.register(Propiedad)
admin.site.register(Pertenece)
admin.site.register(ListaVisitantes)
admin.site.register(Multa)
admin.site.register(Pagos)
admin.site.register(AreasComunes)
admin.site.register(Reserva)