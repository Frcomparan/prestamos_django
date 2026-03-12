from django.db import models
from empleados.models import Empleado

# Create your models here.
class Prestamo(models.Model):
    empleado = models.ForeignKey(Empleado, on_delete=models.PROTECT)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_prestamo = models.DateField()
    
    def __str__(self):
        return f"{self.empleado.nombre} - {self.monto}"