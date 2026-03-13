from django.contrib import admin
from apps.prestamos.models import Prestamo, Abono

# Register your models here.
fieldsets = (
    ('Información del empleado', {
        'fields': ('empleado',)
    }),
    ('Detalle del prestamo', {
        'fields': ('monto', 'plazo_meses', 'tasa_interes_mensual', "saldo_actual"),
    }),
)

readonly_fields = ['pago_fijo_capital', 'saldo_actual']


@admin.register(Prestamo)
class PrestamoAdmin(admin.ModelAdmin):
    list_display = ('empleado', 'monto', "saldo_actual",'plazo_meses', 'estado')
    list_filter = ('estado',)
    search_fields = ('empleado__nombre',)
    fieldsets = fieldsets
    readonly_fields = readonly_fields

@admin.register(Abono)
class AbonoAdmin(admin.ModelAdmin):
    list_display = ('prestamo', 'numero_abono', 'fecha', 'monto_capital', 'monto_interes', 'monto_cobrado', 'saldo_actual')
    search_fields = ('prestamo__empleado__nombre',)

    def has_change_permission(self, request, obj=None):
        return False

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['prestamo', 'numero_abono', 'fecha', 'monto_capital', 'monto_interes', 'monto_cobrado', 'saldo_actual']
        return ['numero_abono', 'fecha', 'monto_capital', 'monto_interes', 'monto_cobrado', 'saldo_actual']