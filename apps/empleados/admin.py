from django.contrib import admin
from .models import Puesto, Empleado, HistorialPuesto

@admin.register(Puesto)
class PuestoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'sueldo']
    search_fields = ['nombre']
    ordering = ['-sueldo']
    list_per_page = 20

def marcar_inactivo(modeladmin, request, queryset):
    queryset.update(activo=False)

class HistorialPuestoInline(admin.TabularInline):
    model = HistorialPuesto
    extra = 1

@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'fecha_ingreso', 'activo', 'antiguedad_años', 'tiene_foto']
    search_fields = ['nombre']
    list_filter = ['activo', 'fecha_ingreso']
    readonly_fields = ['preview_foto']
    fields = ['nombre', 'fecha_ingreso', 'activo', 'foto_perfil', 'preview_foto']
    # readonly_fields = ['fecha_ingreso']
    ordering = ['-fecha_ingreso']
    list_per_page = 25
    date_hierarchy = 'fecha_ingreso'  # Agrega navegación por fecha en la parte superior

    # Acción personalizada para marcar empleados como inactivos
    actions = [marcar_inactivo]
    
    def tiene_foto(self, obj):
        return bool(obj.foto_perfil)
    
    tiene_foto.boolean = True
    tiene_foto.short_description = 'Foto de perfil'
    
    def preview_foto(self, obj):
        if obj.foto_perfil:
            from django.utils.html import format_html
            return format_html(
                '<img src="{}" width="150" height="150" style="border-radius: 8px;" />',
                obj.foto_perfil.url
            )
        return 'Sin foto de perfil'
    preview_foto.short_description = 'Vista previa de foto'

    # Mostrar el historial de puestos directamente en la página del empleado
    inlines = [HistorialPuestoInline]

    @admin.display(description='Antigüedad (años)')
    def antiguedad_años(self, obj):
        from datetime import date
        if obj.fecha_ingreso:
            dias = (date.today() - obj.fecha_ingreso).days
            años = dias / 365
            return f"{años:.1f} años"
        return "N/A"


@admin.register(HistorialPuesto)
class HistorialPuestoAdmin(admin.ModelAdmin):
    list_display = ['empleado', 'puesto', 'fecha_inicio', 'fecha_fin', 'esta_activo']
    search_fields = ['empleado__nombre', 'puesto__nombre']
    list_filter = ['puesto', 'fecha_inicio']
    fieldsets = (
        ('Información del Empleado', {
            'fields': ('empleado',)
        }),
        ('Información del Puesto', {
            'fields': ('puesto',)
        }),
        ('Fechas', {
            'fields': ('fecha_inicio', 'fecha_fin'),
            'description': 'Si fecha_fin está vacía, el puesto está activo'
        }),
    )
    ordering = ['-fecha_inicio']
    list_per_page = 30

    @admin.display(boolean=True, description='¿Activo?')
    def esta_activo(self, obj):
        return obj.fecha_fin is None