from django.contrib import admin
from .models import Empleado, Puesto, HistorialPuesto

# Register your models here.
@admin.register(Puesto)
class PuestoAdmin(admin.ModelAdmin):
  list_display = ["nombre", "sueldo"]

  search_fields = ["nombre"]

@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
  list_display = ["nombre", "fecha_ingreso", "activo"]
  search_fields = ["nombre"]
  list_filter = ["activo"]



