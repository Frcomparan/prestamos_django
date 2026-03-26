from django.db import models
from .utils import generar_nombre_foto_empleado

# Create your models here.
class Puesto(models.Model):
  nombre = models.CharField(max_length=100)
  sueldo = models.DecimalField(max_digits=10, decimal_places=2)

  def __str__(self):
    return self.nombre
  
class Empleado(models.Model):
  nombre = models.CharField(max_length=200)
  fecha_ingreso = models.DateField()
  activo = models.BooleanField(default=True)
  foto_perfil = models.ImageField(
    upload_to=generar_nombre_foto_empleado,
    blank=True,
    null=True,
    help_text='Foto de perfil o identificación del empleado'
  )

  def __str__(self):
      return self.nombre

  def calcular_antiguedad(self):
      from datetime import date
      dias = (date.today() - self.fecha_ingreso).days
      return dias / 365

  def tiene_puesto_asignado(self):
      return self.historial_puestos.filter(fecha_fin__isnull=True).exists()

  def obtener_puesto_actual(self):
      historial_actual = self.historial_puestos.filter(fecha_fin__isnull=True).first()
      if historial_actual:
          return historial_actual.puesto
      return None

  def puede_solicitar_prestamo(self, excluir_prestamo_id=None):
      if not self.tiene_puesto_asignado():
          return False, "El empleado no tiene un puesto asignado actualmente."

      if not self.activo:
          return False, "El empleado no está activo."

      if self.calcular_antiguedad() < 1:
          return False, "Requiere al menos 1 año de antigüedad para solicitar un préstamo."

      prestamos_activos = self.prestamos.filter(estado='ACTIVO')
      if excluir_prestamo_id:
          prestamos_activos = prestamos_activos.exclude(id=excluir_prestamo_id)

      if prestamos_activos.exists():
          return False, "El empleado ya tiene un préstamo activo."

      return True, "Puede solicitar el préstamo."
  
class HistorialPuesto(models.Model):
  empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, related_name='historial_puestos')
  puesto = models.ForeignKey(Puesto, on_delete=models.PROTECT)
  fecha_inicio = models.DateField()
  fecha_fin = models.DateField(null=True, blank=True)

  def __str__(self):
    return f"{self.empleado.nombre} - {self.puesto.nombre} ({self.fecha_inicio} - {self.fecha_fin or 'Actual'})"