# finance/models.py

from django.db import models
from django.core.validators import MinValueValidator
from django.db.models import Sum
from django.utils import timezone
from decimal import Decimal
import uuid
from authentication.models import User, HousingUnit


class Expense(models.Model):
    """Modelo para Expensas/Cuotas mensuales"""
    STATUS_CHOICES = [
        ('PENDING', 'Pendiente'),
        ('PAID', 'Pagado'),
        ('PARTIAL', 'Pago Parcial'),
        ('OVERDUE', 'Vencido'),
        ('CANCELLED', 'Cancelado'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    unit = models.ForeignKey(HousingUnit, on_delete=models.CASCADE, related_name='expenses')
    period_month = models.IntegerField()  # 1-12
    period_year = models.IntegerField()

    base_amount = models.DecimalField(max_digits=10, decimal_places=2,
                                      validators=[MinValueValidator(Decimal('0.00'))])
    additional_services = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'),
                                              validators=[MinValueValidator(Decimal('0.00'))])
    previous_balance = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    total_amount = models.DecimalField(max_digits=10, decimal_places=2,
                                       validators=[MinValueValidator(Decimal('0.00'))])
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'),
                                      validators=[MinValueValidator(Decimal('0.00'))])

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')

    due_date = models.DateField()
    payment_date = models.DateTimeField(null=True, blank=True)

    description = models.TextField(blank=True)
    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_expenses')

    class Meta:
        db_table = 'expenses'
        verbose_name = 'Expensa'
        verbose_name_plural = 'Expensas'
        unique_together = ['unit', 'period_month', 'period_year']
        ordering = ['-period_year', '-period_month', 'unit__unit_number']

    def __str__(self):
        return f"Expensa {self.unit.unit_number} - {self.period_month}/{self.period_year}"

    def calculate_total(self):
        self.total_amount = self.base_amount + self.additional_services + self.previous_balance
        return self.total_amount

    def get_balance(self):
        return self.total_amount - self.paid_amount


class Fine(models.Model):
    """Modelo para Multas"""
    FINE_TYPE_CHOICES = [
        ('NOISE', 'Ruido excesivo'),
        ('DAMAGE', 'Daño a áreas comunes'),
        ('PARKING', 'Mal estacionamiento'),
        ('PETS', 'Infracción de mascotas'),
        ('LATE_PAYMENT', 'Pago tardío'),
        ('OTHER', 'Otro'),
    ]
    STATUS_CHOICES = [
        ('PENDING', 'Pendiente'),
        ('PAID', 'Pagado'),
        ('APPEALED', 'Apelado'),
        ('CANCELLED', 'Cancelado'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    unit = models.ForeignKey(HousingUnit, on_delete=models.CASCADE, related_name='fines')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='fines')

    fine_type = models.CharField(max_length=20, choices=FINE_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2,
                                 validators=[MinValueValidator(Decimal('0.01'))])

    description = models.TextField()
    evidence = models.FileField(upload_to='fines/evidence/', null=True, blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')

    issue_date = models.DateField()
    due_date = models.DateField()
    payment_date = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_fines')

    class Meta:
        db_table = 'fines'
        verbose_name = 'Multa'
        verbose_name_plural = 'Multas'
        ordering = ['-issue_date']

    def __str__(self):
        return f"Multa {self.unit.unit_number} - {self.get_fine_type_display()} - ${self.amount}"


class Payment(models.Model):
    """Modelo para Pagos realizados"""

    PAYMENT_METHOD_CHOICES = [
        ('CASH', 'Efectivo'),
        ('TRANSFER', 'Transferencia Bancaria'),
        ('CARD', 'Tarjeta de Crédito/Débito'),
        ('QR', 'Pago QR'),
        ('CHECK', 'Cheque'),
    ]
    PAYMENT_TYPE_CHOICES = [
        ('EXPENSE', 'Expensa'),
        ('FINE', 'Multa'),
        ('RESERVATION', 'Reserva de Área Común'),
        ('SERVICE', 'Servicio Adicional'),
        ('OTHER', 'Otro'),
    ]
    STATUS_CHOICES = [
        ('PENDING', 'Pendiente'),
        ('PROCESSING', 'Procesando'),
        ('COMPLETED', 'Completado'),
        ('FAILED', 'Fallido'),
        ('REFUNDED', 'Reembolsado'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    unit = models.ForeignKey(HousingUnit, on_delete=models.CASCADE, related_name='payments')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='payments')

    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPE_CHOICES)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')

    amount = models.DecimalField(max_digits=10, decimal_places=2,
                                 validators=[MinValueValidator(Decimal('0.01'))])

    # Referencias a otros modelos según el tipo de pago
    expense = models.ForeignKey(
        Expense,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='payments'
    )
    fine = models.ForeignKey(
        Fine,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='payments'
    )

    reference = models.CharField(max_length=120, blank=True)   # nro. de recibo, ref. bancaria, etc.
    transaction_id = models.CharField(max_length=120, blank=True)
    receipt = models.FileField(upload_to='payments/receipts/', null=True, blank=True)
    notes = models.TextField(blank=True)

    payment_date = models.DateTimeField(null=True, blank=True)  # momento del cobro efectivo (si aplica)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_payments')

    class Meta:
        db_table = 'payments'
        verbose_name = 'Pago'
        verbose_name_plural = 'Pagos'
        ordering = ['-created_at']

    def __str__(self):
        return f"Pago {self.get_payment_type_display()} - {self.amount} - {self.get_status_display()}"

    # --------- Validaciones y actualizaciones automáticas ---------
    def clean(self):
        """Valida consistencia de referencias según el tipo."""
        from django.core.exceptions import ValidationError
        if self.payment_type == 'EXPENSE' and not self.expense:
            raise ValidationError({'expense': 'Debe vincular una Expensa cuando el tipo es EXPENSE.'})
        if self.payment_type == 'FINE' and not self.fine:
            raise ValidationError({'fine': 'Debe vincular una Multa cuando el tipo es FINE.'})

    def _recompute_expense_status(self):
        """Recalcula monto pagado y estado de la expensa ligada."""
        if not self.expense_id:
            return
        agg = Payment.objects.filter(
            expense=self.expense, status='COMPLETED'
        ).aggregate(total=Sum('amount'))
        paid = agg['total'] or Decimal('0.00')
        exp = self.expense
        exp.paid_amount = paid
        if paid >= exp.total_amount:
            exp.status = 'PAID'
            if not exp.payment_date:
                exp.payment_date = timezone.now()
        elif paid > 0:
            exp.status = 'PARTIAL'
        else:
            exp.status = 'PENDING'
        exp.save(update_fields=['paid_amount', 'status', 'payment_date', 'updated_at'])

    def _maybe_mark_fine_paid(self):
        """Si la suma pagada cubre la multa, márcala como pagada."""
        if not self.fine_id:
            return
        agg = Payment.objects.filter(
            fine=self.fine, status='COMPLETED'
        ).aggregate(total=Sum('amount'))
        paid = agg['total'] or Decimal('0.00')
        if paid >= self.fine.amount and self.fine.status != 'PAID':
            f = self.fine
            f.status = 'PAID'
            if not f.payment_date:
                f.payment_date = timezone.now()
            f.save(update_fields=['status', 'payment_date', 'updated_at'])

    def save(self, *args, **kwargs):
        # Asigna payment_date automáticamente cuando pasa a COMPLETED
        if self.status == 'COMPLETED' and self.payment_date is None:
            self.payment_date = timezone.now()

        super().save(*args, **kwargs)

        # Actualiza estados relacionados sólo si el pago está completado
        if self.status == 'COMPLETED':
            self._recompute_expense_status()
            self._maybe_mark_fine_paid()
