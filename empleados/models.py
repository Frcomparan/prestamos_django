from django.db import models

# Create your models here.
class Puesto(models.Model):
  nombre = models.CharField(max_length=100)
  sueldo = models.DecimalField(max_digits=10, decimal_places=2)

  def __str__(self):
    return self.nombre
  
class Empleado(models.Model):
  nombre = models.CharField(max_length=100)
  fecha_ingreso = models.DateField()
  activo = models.BooleanField(default=True)

  def __str__(self):
    return self.nombre
  
class HistorialPuesto(models.Model):
  empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
  puesto = models.ForeignKey(Puesto, on_delete=models.PROTECT)
  fecha_inicio = models.DateField()
  fecha_fin = models.DateField(null=True, blank=True)

  def __str__(self):
    return f"{self.empleado.nombre} - {self.puesto.nombre} ({self.fecha_inicio} - {self.fecha_fin or 'Actual'})"