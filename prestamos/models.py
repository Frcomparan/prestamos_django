from django.db import models
from empleados.models import Empleado
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Prestamo(models.Model):
    # Quien solicita el préstamo
    empleado = models.ForeignKey(Empleado, on_delete=models.PROTECT, related_name='prestamos')

    # Cuanto se paga y por cuanto tiempo
    monto = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0.01)])
    plazo_meses = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(24)])

    # Fechas importantes
    fecha_solicitud = models.DateField(auto_now_add=True, help_text="Fecha de solicitud del préstamo")
    fecha_aprobacion = models.DateField(null=True, blank=True, help_text="Fecha de aprobación del préstamo")
    fecha_inicio_descuento = models.DateField(null=True, blank=True, help_text="Fecha de inicio de los descuentos en nómina")
    fecha_fin_descuento = models.DateField(null=True, blank=True, help_text="Fecha de fin de los descuentos en nómina")
    
    # Calculos financieros
    tasa_interes_mensual = models.DecimalField(max_digits=5, decimal_places=2, default=1.00, validators=[MinValueValidator(0)], help_text="Tasa de interés mensual en porcentaje")
    pago_fijo_capital = models.DecimalField(max_digits=12, decimal_places=2, help_text="Pago fijo de capital mensual")
    saldo_actual = models.DecimalField(max_digits=12, decimal_places=2, help_text="Saldo pendiente del préstamo")

    # Estado del préstamo
    ESTADO_CHOICES = [
        ('SOLICITADO', 'Solicitado'),
        ('APROBADO', 'Aprobado'),
        ('ACTIVO', 'Activo'),
        ('CONCLUIDO', 'Concluido'),
        ('RECHAZADO', 'Rechazado'),
    ]
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='SOLICITADO')

    def __str__(self):
        return f"{self.empleado.nombre} - {self.monto}"
    
    # Sobreescritura de metodos
    def save(self, *args, **kwargs):
        # Calcular el pago fijo de capital si no se ha proporcionado
        if not self.pago_fijo_capital:
            self.pago_fijo_capital = self.monto / self.plazo_meses

        # Solo calcular el saldo inicial al crear el préstamo
        if not self.pk:
            self.saldo_actual = self.monto

        super().save(*args, **kwargs)
        


