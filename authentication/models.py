from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
import uuid


class UserManager(BaseUserManager):
    """Manager personalizado para el modelo User"""

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El usuario debe tener un correo electrónico')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', 'ADMIN')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('El superusuario debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('El superusuario debe tener is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """Modelo personalizado de Usuario"""

    ROLE_CHOICES = [
        ('ADMIN', 'Administrador'),
        ('OWNER', 'Copropietario'),
        ('TENANT', 'Inquilino'),
        ('SECURITY', 'Personal de Seguridad'),
        ('MAINTENANCE', 'Personal de Mantenimiento'),
    ]

    STATUS_CHOICES = [
        ('ACTIVE', 'Activo'),
        ('INACTIVE', 'Inactivo'),
        ('PENDING', 'Pendiente de Verificación'),
        ('BLOCKED', 'Bloqueado'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, max_length=255)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True, null=True)
    document_type = models.CharField(max_length=20, default='CI')
    document_number = models.CharField(max_length=20, unique=True)

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='TENANT')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Campos adicionales
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)
    failed_login_attempts = models.IntegerField(default=0)
    last_failed_login = models.DateTimeField(null=True, blank=True)
    password_reset_token = models.CharField(max_length=255, null=True, blank=True)
    password_reset_token_created = models.DateTimeField(null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'document_number']

    class Meta:
        db_table = 'users'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['-date_joined']

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.first_name


class HousingUnit(models.Model):
    """Modelo para Unidades Habitacionales"""

    UNIT_TYPE_CHOICES = [
        ('APARTMENT', 'Departamento'),
        ('HOUSE', 'Casa'),
        ('OFFICE', 'Oficina'),
        ('COMMERCIAL', 'Local Comercial'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    unit_number = models.CharField(max_length=20, unique=True)
    unit_type = models.CharField(max_length=20, choices=UNIT_TYPE_CHOICES, default='APARTMENT')
    floor = models.IntegerField(null=True, blank=True)
    building = models.CharField(max_length=50, null=True, blank=True)

    area_m2 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    bedrooms = models.IntegerField(default=1)
    bathrooms = models.IntegerField(default=1)
    parking_spaces = models.IntegerField(default=0)

    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='owned_units',
        limit_choices_to={'role': 'OWNER'}
    )

    current_tenant = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='rented_units',
        limit_choices_to={'role': 'TENANT'}
    )

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'housing_units'
        verbose_name = 'Unidad Habitacional'
        verbose_name_plural = 'Unidades Habitacionales'
        ordering = ['building', 'floor', 'unit_number']

    def __str__(self):
        return f"Unidad {self.unit_number} - {self.get_unit_type_display()}"


class UserUnitRelation(models.Model):
    """Relación entre usuarios y unidades (histórico)"""

    RELATION_TYPE_CHOICES = [
        ('OWNER', 'Propietario'),
        ('TENANT', 'Inquilino'),
        ('AUTHORIZED', 'Autorizado'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='unit_relations')
    unit = models.ForeignKey(HousingUnit, on_delete=models.CASCADE, related_name='user_relations')
    relation_type = models.CharField(max_length=20, choices=RELATION_TYPE_CHOICES)

    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_unit_relations'
        verbose_name = 'Relación Usuario-Unidad'
        verbose_name_plural = 'Relaciones Usuario-Unidad'
        unique_together = ['user', 'unit', 'start_date']

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.unit.unit_number} ({self.relation_type})"


class Role(models.Model):
    """Modelo para gestión de roles personalizados"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    permissions = models.JSONField(default=dict)  # Almacena permisos como JSON

    is_system_role = models.BooleanField(default=False)  # Roles del sistema no se pueden eliminar
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_roles')

    class Meta:
        db_table = 'roles'
        verbose_name = 'Rol'
        verbose_name_plural = 'Roles'
        ordering = ['name']

    def __str__(self):
        return self.name


class AuditLog(models.Model):
    """Modelo para bitácora de auditoría"""

    ACTION_CHOICES = [
        ('LOGIN', 'Inicio de Sesión'),
        ('LOGOUT', 'Cierre de Sesión'),
        ('CREATE', 'Crear'),
        ('UPDATE', 'Actualizar'),
        ('DELETE', 'Eliminar'),
        ('VIEW', 'Ver'),
        ('EXPORT', 'Exportar'),
        ('PASSWORD_CHANGE', 'Cambio de Contraseña'),
        ('PASSWORD_RESET', 'Reseteo de Contraseña'),
        ('FAILED_LOGIN', 'Intento de Login Fallido'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='audit_logs')
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    module = models.CharField(max_length=50)
    model_name = models.CharField(max_length=50, null=True, blank=True)
    object_id = models.CharField(max_length=255, null=True, blank=True)

    description = models.TextField()
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)

    success = models.BooleanField(default=True)
    error_message = models.TextField(null=True, blank=True)

    extra_data = models.JSONField(default=dict, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'audit_logs'
        verbose_name = 'Registro de Auditoría'
        verbose_name_plural = 'Registros de Auditoría'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['action', '-created_at']),
        ]

    def __str__(self):
        return f"{self.user} - {self.action} - {self.created_at}"


class EmailVerificationToken(models.Model):
    """Token para verificación de email"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='email_tokens')
    token = models.CharField(max_length=255, unique=True)
    is_used = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    class Meta:
        db_table = 'email_verification_tokens'
        verbose_name = 'Token de Verificación de Email'
        verbose_name_plural = 'Tokens de Verificación de Email'

    def is_valid(self):
        return not self.is_used and self.expires_at > timezone.now()
