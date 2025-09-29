# api/management/commands/enviar_recordatorios_pago.py

import datetime
from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
# Se asegura de que todos los modelos necesarios estén importados
from api.models import Usuario, Pagos, Factura, Notificaciones, Envio
from django.utils import timezone


class Command(BaseCommand):
    help = 'Revisa las cuotas pendientes del mes actual y envía recordatorios.'

    def handle(self, *args, **options):
        self.stdout.write("Iniciando tarea de envío de recordatorios de pago...")

        today = timezone.now().date()

        cargos_mensuales = Pagos.objects.all()
        if not cargos_mensuales.exists():
            self.stdout.write("No hay cargos mensuales configurados en el catálogo de Pagos.")
            return

        residentes_activos = Usuario.objects.filter(estado='activo', idrol__tipo='residente')

        for residente in residentes_activos:
            lista_deudas = []

            for cargo in cargos_mensuales:
                pago_realizado = Factura.objects.filter(
                    codigo_usuario=residente,
                    id_pago=cargo,
                    fecha__month=today.month,
                    fecha__year=today.year,
                    estado='pagado'
                ).exists()

                if not pago_realizado:
                    lista_deudas.append(cargo)

            if lista_deudas:
                self.stdout.write(f"El residente {residente.correo} tiene {len(lista_deudas)} pago(s) pendiente(s).")
                # Se mantiene el envío de correo electrónico
                self.enviar_correo_recordatorio(residente, lista_deudas)
                # --- ¡MEJORA AÑADIDA! ---
                # Ahora también crea una notificación dentro de la app
                self.crear_notificacion_interna(residente, lista_deudas)

        self.stdout.write(self.style.SUCCESS("Tarea de envío de recordatorios finalizada con éxito."))

    def enviar_correo_recordatorio(self, residente, deudas):
        # Esta función no cambia, sigue enviando el email como antes.
        asunto = "Recordatorio de Pago de Cuotas del Condominio"
        monto_total = sum(d.monto for d in deudas)
        mensaje_lista_deudas = ""
        for deuda in deudas:
            mensaje_lista_deudas += f"- {deuda.descripcion}: Bs. {deuda.monto}\n"

        mensaje = f"""
Hola {residente.nombre},

Este es un recordatorio amistoso de que tienes los siguientes pagos pendientes para este mes:

{mensaje_lista_deudas}
Monto Total Pendiente: Bs. {monto_total}

Puedes realizar tu pago ingresando a nuestro portal en línea.

Gracias,
Administración de SmartCondominium
"""
        try:
            send_mail(asunto, mensaje, settings.DEFAULT_FROM_EMAIL, [residente.correo], fail_silently=False)
            self.stdout.write(self.style.SUCCESS(f"Correo enviado exitosamente a {residente.correo}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error al enviar correo a {residente.correo}: {e}"))

    # --- ¡NUEVA FUNCIÓN AÑADIDA! ---
    def crear_notificacion_interna(self, residente, deudas):
        """Crea la notificación y el envío en la base de datos para la campanita."""
        monto_total = sum(d.monto for d in deudas)

        # 1. Creamos el objeto de la notificación con el mensaje.
        notificacion_obj = Notificaciones.objects.create(
            tipo='Recordatorio de Pago',
            descripcion=f"Hola {residente.nombre}, tienes un saldo pendiente de Bs. {monto_total}. Por favor, realiza tu pago."
        )

        # 2. Creamos el "Envio" para conectar esa notificación con el usuario específico.
        Envio.objects.create(
            codigo_usuario=residente,
            id_notific=notificacion_obj,
            fecha=timezone.now().date(),
            hora=timezone.now().time(),
            estado='no leido'  # Marcamos la notificación como no leída.
        )
        self.stdout.write(self.style.SUCCESS(f"Notificación interna creada para {residente.correo}"))