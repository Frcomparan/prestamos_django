from django.db import models
from apps.empleados.models import Empleado
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Prestamo(models.Model):
    # Relación con el empleado que solicita el préstamo.
    # PROTECT evita borrar al empleado si tiene préstamos registrados.
    empleado = models.ForeignKey(Empleado, on_delete=models.PROTECT, related_name='prestamos')

    # Datos principales del préstamo.
    # monto: cantidad de dinero solicitada.
    # plazo_meses: duración del préstamo, con un mínimo de 1 y máximo de 24 meses.
    monto = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0.01)])
    plazo_meses = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(24)])

    # Fechas importantes dentro del ciclo de vida del préstamo.
    # fecha_solicitud se asigna automáticamente al crear el registro.
    # Las demás fechas se llenan conforme avanza el proceso.
    fecha_solicitud = models.DateField(auto_now_add=True, help_text='Fecha de solicitud del préstamo')
    fecha_aprobacion = models.DateField(null=True, blank=True, help_text='Fecha de aprobación del préstamo')
    fecha_inicio_descuento = models.DateField(null=True, blank=True, help_text='Fecha de inicio de los descuentos en nómina')
    fecha_fin_descuento = models.DateField(null=True, blank=True, help_text='Fecha de fin de los descuentos en nómina')

    # Campos financieros.
    # tasa_interes_mensual: porcentaje mensual aplicado al saldo.
    # pago_fijo_capital: cuánto se abonará cada mes al capital.
    # saldo_actual: cuánto falta por pagar.
    tasa_interes_mensual = models.DecimalField(max_digits=5, decimal_places=2, default=1.00, validators=[MinValueValidator(0)], help_text='Tasa de interés mensual en porcentaje')
    pago_fijo_capital = models.DecimalField(max_digits=12, decimal_places=2, help_text='Pago fijo de capital mensual')
    saldo_actual = models.DecimalField(max_digits=12, decimal_places=2, help_text='Saldo pendiente del préstamo')

    # Posibles estados del préstamo.
    # El primer valor se guarda en la base de datos.
    # El segundo valor es el que verá el usuario en formularios y admin.
    ESTADO_CHOICES = [
        ('SOLICITADO', 'Solicitado'),
        ('APROBADO', 'Aprobado'),
        ('ACTIVO', 'Activo'),
        ('CONCLUIDO', 'Concluido'),
        ('RECHAZADO', 'Rechazado'),
    ]

    # Estado actual del préstamo. Inicia como SOLICITADO.
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='SOLICITADO')

    def __str__(self):
        # Define cómo se mostrará el objeto en el admin y en la shell.
        return f"Préstamo de {self.empleado.nombre} por {self.monto:.2f} a {self.plazo_meses} meses - Estado: {self.estado}"
    
    # Sobreescritura de metodos
    def save(self, *args, **kwargs):
        # Si todavía no existe pago fijo, se calcula dividiendo
        # el monto total entre el plazo del préstamo.
        if not self.pago_fijo_capital:
            self.pago_fijo_capital = self.monto / self.plazo_meses

        # Si el préstamo es nuevo, el saldo inicial es igual al monto solicitado.
        if not self.pk:
            self.saldo_actual = self.monto

        # Finalmente se llama al save original de Django.
        super().save(*args, **kwargs)

    def calcular_monto_maximo(self):
        # Import local para evitar dependencias circulares al cargar modelos.
        from apps.empleados.models import HistorialPuesto

        # Buscar el puesto actual del empleado.
        # fecha_fin__isnull=True significa que ese historial sigue activo.
        historial_actual = HistorialPuesto.objects.filter(
            empleado=self.empleado,
            fecha_fin__isnull=True
        ).first()

        # Si existe un puesto actual, el monto máximo será 6 veces su sueldo.
        if historial_actual:
            return historial_actual.puesto.sueldo * 6

        # Si no tiene puesto actual, no debería poder solicitar préstamo.
        return 0
    
    def puede_solicitar_prestamo(self):
        # Validación mínima: el préstamo debe tener empleado asignado.
        if not self.empleado:
            return False, "El préstamo debe estar asociado a un empleado."

        # Reutilizar la lógica de validación definida en el modelo Empleado.
        puede_solicitar_prestamo, mensaje = self.empleado.puede_solicitar_prestamo(excluir_prestamo_id=self.pk)

        # Si el empleado no cumple una regla, se devuelve ese mensaje tal cual.
        if not puede_solicitar_prestamo:
            return False, mensaje

        # Validar que el monto solicitado no rebase el límite permitido.
        monto_maximo = self.calcular_monto_maximo()
        if self.monto > monto_maximo:
            return False, f"El monto solicitado excede el máximo permitido de {monto_maximo:.2f} basado en su puesto actual."

        # Si pasó todas las validaciones, puede solicitar el préstamo.
        return True, "Puede solicitar el préstamo."
    
    def clean(self):
        # ValidationError es la excepción que Django usa para indicar
        # que un objeto no cumple las reglas del negocio.
        from django.core.exceptions import ValidationError

        # Validar el préstamo al crearlo o cuando sigue en estado SOLICITADO.
        if not self.pk or self.estado == 'SOLICITADO':
            puede_solicitar, mensaje = self.puede_solicitar_prestamo()
            if not puede_solicitar:
                raise ValidationError(mensaje)

        # Validar coherencia entre fechas.
        # No tiene sentido aprobar antes de solicitar.
        if self.fecha_aprobacion and self.fecha_aprobacion < self.fecha_solicitud:
            raise ValidationError('La fecha de aprobación no puede ser anterior a la fecha de solicitud.')
        
class Abono(models.Model):
    # Relación con el préstamo al que pertenece este pago.
    prestamo = models.ForeignKey(Prestamo, on_delete=models.CASCADE, related_name='abonos')

    # Número consecutivo del abono dentro del préstamo.
    numero_abono = models.PositiveIntegerField(help_text='Número secuencial del abono', default=1)

    # Fecha automática en que se registra el abono.
    fecha = models.DateField(auto_now_add=True, help_text='Fecha del abono')

    # Desglose del pago.
    # monto_capital: parte del pago que reduce la deuda.
    # monto_interes: costo financiero del periodo.
    # monto_cobrado: suma de capital + interés.
    # saldo_actual: saldo restante después de aplicar el abono.
    monto_capital = models.DecimalField(max_digits=12, decimal_places=2, default=0, help_text='Monto del abono aplicado a capital')
    monto_interes = models.DecimalField(max_digits=12, decimal_places=2, default=0, help_text='Monto del abono aplicado a intereses')
    monto_cobrado = models.DecimalField(max_digits=12, decimal_places=2, default=0, help_text='Monto total cobrado en este abono')
    saldo_actual = models.DecimalField(max_digits=12, decimal_places=2, default=0, help_text='Saldo restante del préstamo después de este abono')

    def save(self, *args, **kwargs):
        # Solo hacer cálculos automáticos cuando el abono es nuevo.
        if not self.pk:
            # Tomar el saldo actual del préstamo antes de aplicar el nuevo abono.
            saldo_anterior = self.prestamo.saldo_actual

            # Calcular interés del periodo usando la tasa mensual del préstamo.
            self.monto_interes = saldo_anterior * (self.prestamo.tasa_interes_mensual / 100)

            # El capital pagado es el pago fijo definido en el préstamo.
            self.monto_capital = self.prestamo.pago_fijo_capital

            # El total cobrado es capital + interés.
            self.monto_cobrado = self.monto_capital + self.monto_interes

            # Actualizar el saldo restante después del pago.
            self.saldo_actual = saldo_anterior - self.monto_capital

            # Sincronizar el nuevo saldo en el préstamo.
            self.prestamo.saldo_actual = self.saldo_actual

            # Si el saldo llega a cero o menos, el préstamo termina.
            if self.saldo_actual <= 0:
                self.prestamo.estado = 'CONCLUIDO'

            # Calcular el número consecutivo del abono.
            ultimo_abono = Abono.objects.filter(prestamo=self.prestamo).order_by('-numero_abono').first()
            self.numero_abono = ultimo_abono.numero_abono + 1 if ultimo_abono else 1

            # Guardar primero el préstamo con su nuevo saldo.
            self.prestamo.save()

        # Guardar finalmente el abono.
        super().save(*args, **kwargs)

