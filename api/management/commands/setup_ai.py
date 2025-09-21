from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from api.models import Rol, Usuario, Vehiculo
from api.services.supabase_storage import SupabaseStorageService


class Command(BaseCommand):
    help = 'Configura datos iniciales para el sistema de IA'

    def handle(self, *args, **options):
        self.stdout.write('Configurando sistema de IA...')

        # Configurar Supabase Storage
        try:
            storage_service = SupabaseStorageService()
            self.stdout.write('Supabase Storage configurado exitosamente')
        except Exception as e:
            self.stdout.write(f'Error configurando Supabase: {e}')
            return

        # Crear roles si no existen
        admin_rol, created = Rol.objects.get_or_create(
            id=1,
            defaults={
                'descripcion': 'Administrador',
                'tipo': 'admin',
                'estado': 'activo'
            }
        )

        residente_rol, created = Rol.objects.get_or_create(
            id=2,
            defaults={
                'descripcion': 'Residente',
                'tipo': 'residente',
                'estado': 'activo'
            }
        )

        # Crear usuario de prueba
        test_user, created = Usuario.objects.get_or_create(
            correo='test@condominio.com',
            defaults={
                'nombre': 'Usuario',
                'apellido': 'Prueba',
                'contrasena': 'test123',
                'sexo': 'M',
                'telefono': 12345678,
                'estado': 'activo',
                'idrol': residente_rol
            }
        )

        # Crear token
        django_user, created = User.objects.get_or_create(
            username='test@condominio.com',
            defaults={'email': 'test@condominio.com'}
        )
        django_user.set_password('test123')
        django_user.save()

        token, created = Token.objects.get_or_create(user=django_user)

        # Crear vehículos de ejemplo
        vehiculos_ejemplo = [
            {'nro_placa': 'ABC-1234', 'descripcion': 'Toyota Corolla Blanco', 'estado': 'activo'},
            {'nro_placa': 'XYZ-5678', 'descripcion': 'Honda Civic Azul', 'estado': 'activo'},
        ]

        for vehiculo_data in vehiculos_ejemplo:
            Vehiculo.objects.get_or_create(
                nro_placa=vehiculo_data['nro_placa'],
                defaults=vehiculo_data
            )

        self.stdout.write(
            self.style.SUCCESS(
                f'Sistema configurado!\nToken: {token.key}\nUsuario: test@condominio.com / test123'
            )
        )