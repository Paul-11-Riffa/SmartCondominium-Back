# api/management/commands/enviar_recordatorios_pago.py

import datetime
from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
from api.models import Usuario, Pagos, Factura


class Command(BaseCommand):
    help = 'Revisa las cuotas pendientes del mes actual y envía recordatorios por correo electrónico.'

    def handle(self, *args, **options):
        self.stdout.write("Iniciando tarea de envío de recordatorios de pago...")

        today = datetime.date.today()
        # --- Lógica de Cuándo Enviar ---
        # Puedes cambiar este día. Por ejemplo, el día 25 de cada mes.
        DIA_DE_RECORDATORIO = 25

        #if today.day != DIA_DE_RECORDATORIO:
         #   self.stdout.write(f"Hoy no es día {DIA_DE_RECORDATORIO}. No se enviarán recordatorios.")
          #  return

        # 1. Obtener todos los cargos mensuales recurrentes del catálogo
        cargos_mensuales = Pagos.objects.all()
        if not cargos_mensuales.exists():
            self.stdout.write("No hay cargos mensuales configurados en el catálogo de Pagos.")
            return

        # 2. Obtener todos los residentes activos
        residentes_activos = Usuario.objects.filter(estado='activo', idrol__tipo='residente')

        # 3. Revisar cada residente
        for residente in residentes_activos:
            lista_deudas = []

            # Para cada cargo mensual, ver si el residente ya lo pagó este mes
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

            # 4. Si se encontraron deudas, enviar el correo
            if lista_deudas:
                self.stdout.write(f"El residente {residente.correo} tiene {len(lista_deudas)} pago(s) pendiente(s).")
                self.enviar_correo_recordatorio(residente, lista_deudas)

        self.stdout.write(self.style.SUCCESS("Tarea de envío de recordatorios finalizada con éxito."))

    def enviar_correo_recordatorio(self, residente, deudas):
        """Compone y envía el correo electrónico al residente."""

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
            send_mail(
                asunto,
                mensaje,
                settings.DEFAULT_FROM_EMAIL,
                [residente.correo],
                fail_silently=False,
            )
            self.stdout.write(self.style.SUCCESS(f"Correo enviado exitosamente a {residente.correo}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error al enviar correo a {residente.correo}: {e}"))