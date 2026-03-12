# Sesión 2: Backend - Modelos Completos y API

**Duración estimada:** 3-4 horas  
**Nivel:** Intermedio  
**Prerequisito:** Sesión 1 completada

## 🎯 Objetivos de la Sesión

Al finalizar esta sesión, podrás:

- ✅ Completar los modelos de Préstamos y Abonos
- ✅ Agregar validaciones de negocio
- ✅ Crear métodos personalizados en modelos
- ✅ Implementar señales de Django
- ✅ Crear una API REST básica

---

## 📚 Parte 1: Completar Modelos de Préstamos

### Recordatorio: ¿Dónde estamos?

En la sesión anterior creamos:

- ✅ Puesto
- ✅ Empleado
- ✅ HistorialPuesto

Ahora crearemos:

- ⏳ Prestamo
- ⏳ Abono

### Paso 1: Crear App de Préstamos

```bash
# Crear nueva app
docker compose exec web python manage.py startapp prestamos

# Registrar en settings.py
```

Edita `config/settings.py`:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'empleados',
    'prestamos',  # ← Agregar esta línea
]
```

### Paso 2: Modelo Prestamo Completo

Abre `prestamos/models.py`:

```python
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from empleados.models import Empleado
from datetime import date
from dateutil.relativedelta import relativedelta

class Prestamo(models.Model):
    """
    Préstamo otorgado a un empleado.
    """

    # Opciones de estado
    ESTADO_CHOICES = [
        ('SOLICITADO', 'Solicitado'),
        ('APROBADO', 'Aprobado'),
        ('ACTIVO', 'Activo'),
        ('CONCLUIDO', 'Concluido'),
        ('RECHAZADO', 'Rechazado'),
    ]

    # Campos
    empleado = models.ForeignKey(
        Empleado,
        on_delete=models.PROTECT,
        related_name='prestamos',
        help_text="Empleado que solicita el préstamo"
    )

    monto = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        help_text="Monto total del préstamo"
    )

    plazo_meses = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(24)
        ],
        help_text="Duración del préstamo en meses (máx. 24)"
    )

    fecha_solicitud = models.DateField(
        default=date.today,
        help_text="Fecha de solicitud del préstamo"
    )

    fecha_aprobacion = models.DateField(
        null=True,
        blank=True,
        help_text="Fecha de aprobación del préstamo"
    )

    tasa_interes_mensual = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=1.00,
        help_text="Tasa de interés mensual (%)"
    )

    pago_fijo_capital = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        help_text="Pago mensual fijo a capital"
    )

    fecha_inicio_descuento = models.DateField(
        null=True,
        blank=True,
        help_text="Primera fecha de descuento"
    )

    fecha_fin_descuento = models.DateField(
        null=True,
        blank=True,
        help_text="Última fecha de descuento"
    )

    saldo_actual = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        help_text="Saldo pendiente del préstamo"
    )

    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='SOLICITADO',
        help_text="Estado actual del préstamo"
    )

    class Meta:
        verbose_name = "Préstamo"
        verbose_name_plural = "Préstamos"
        ordering = ['-fecha_solicitud']

    def __str__(self):
        return f"Préstamo #{self.id} - {self.empleado.nombre} - ${self.monto}"
```

**Conceptos nuevos explicados:**

#### 1. Choices (Opciones)

```python
ESTADO_CHOICES = [
    ('SOLICITADO', 'Solicitado'),  # (valor_db, etiqueta_mostrar)
]
```

- Limita los valores posibles
- Primer valor va a la base de datos
- Segundo valor se muestra al usuario

#### 2. Validators (Validadores)

```python
validators=[MinValueValidator(0.01)]
```

- Validan que el valor cumpla reglas
- `MinValueValidator`: Mínimo permitido
- `MaxValueValidator`: Máximo permitido

#### 3. default

```python
fecha_solicitud = models.DateField(default=date.today)
```

- Valor automático si no se proporciona

### Paso 3: Agregar Métodos al Modelo Prestamo

Agrega estos métodos dentro de la clase `Prestamo`:

```python
# prestamos/models.py (dentro de la clase Prestamo)

def save(self, *args, **kwargs):
    """
    Sobrescribe el método save para calcular valores automáticos.
    """
    # Calcular pago fijo a capital
    if not self.pago_fijo_capital:
        self.pago_fijo_capital = self.monto / self.plazo_meses

    # Inicializar saldo si es nuevo
    if not self.pk:  # Si es un préstamo nuevo
        self.saldo_actual = self.monto

    super().save(*args, **kwargs)

def calcular_monto_maximo(self):
    """
    Calcula el monto máximo que puede solicitar el empleado.
    Regla: 6 meses de su sueldo actual.
    """
    from empleados.models import HistorialPuesto

    # Obtener puesto actual
    historial_actual = HistorialPuesto.objects.filter(
        empleado=self.empleado,
        fecha_fin__isnull=True
    ).first()

    if historial_actual:
        return historial_actual.puesto.sueldo * 6
    return 0

def puede_solicitar_prestamo(self):
    """
    Valida si el empleado puede solicitar un préstamo.
    Retorna (puede, mensaje_error)
    """
    from datetime import date

    # 1. Verificar antigüedad (mínimo 1 año)
    antiguedad = (date.today() - self.empleado.fecha_ingreso).days / 365
    if antiguedad < 1:
        return False, "El empleado requiere mínimo 1 año de antigüedad"

    # 2. Verificar que no tenga préstamo activo
    tiene_prestamo_activo = Prestamo.objects.filter(
        empleado=self.empleado,
        estado='ACTIVO'
    ).exclude(pk=self.pk).exists()

    if tiene_prestamo_activo:
        return False, "El empleado ya tiene un préstamo activo"

    # 3. Verificar monto máximo
    monto_maximo = self.calcular_monto_maximo()
    if self.monto > monto_maximo:
        return False, f"El monto máximo permitido es ${monto_maximo}"

    return True, "Validación exitosa"

def aprobar(self, fecha_inicio):
    """
    Aprueba el préstamo y establece las fechas de descuento.
    """
    self.estado = 'APROBADO'
    self.fecha_aprobacion = date.today()
    self.fecha_inicio_descuento = fecha_inicio

    # Calcular fecha fin (plazo_meses - 1 porque el primer mes cuenta)
    self.fecha_fin_descuento = fecha_inicio + relativedelta(months=self.plazo_meses - 1)

    self.save()

def esta_concluido(self):
    """
    Verifica si el préstamo está completamente pagado.
    """
    return self.saldo_actual == 0
```

**Conceptos explicados:**

#### save()

- Se ejecuta automáticamente al guardar
- Aquí hacemos cálculos previos
- `super().save()` llama al método original

#### Métodos personalizados

- Son funciones que puedes crear
- Encapsulan lógica de negocio
- Hacen el código más legible

### Paso 4: Modelo Abono

En el mismo archivo `prestamos/models.py`, agrega:

```python
# prestamos/models.py (después de Prestamo)

class Abono(models.Model):
    """
    Registro de cada pago mensual de un préstamo.
    """
    prestamo = models.ForeignKey(
        Prestamo,
        on_delete=models.CASCADE,
        related_name='abonos',
        help_text="Préstamo al que pertenece el abono"
    )

    numero_abono = models.IntegerField(
        validators=[MinValueValidator(1)],
        help_text="Número secuencial del abono"
    )

    fecha = models.DateField(
        help_text="Fecha del pago"
    )

    monto_capital = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        help_text="Pago aplicado a capital"
    )

    monto_interes = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        help_text="Interés cobrado del mes"
    )

    monto_cobrado = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        help_text="Total cobrado (capital + interés)"
    )

    saldo_actual = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        help_text="Saldo restante después del pago"
    )

    class Meta:
        verbose_name = "Abono"
        verbose_name_plural = "Abonos"
        ordering = ['prestamo', 'numero_abono']
        unique_together = [['prestamo', 'numero_abono']]

    def __str__(self):
        return f"Abono #{self.numero_abono} - Préstamo #{self.prestamo.id}"

    def save(self, *args, **kwargs):
        """
        Calcula automáticamente los montos y actualiza el saldo del préstamo.
        """
        if not self.pk:  # Solo en nuevos abonos
            # Calcular interés: saldo_anterior * (tasa / 100)
            saldo_anterior = self.prestamo.saldo_actual
            self.monto_interes = saldo_anterior * (self.prestamo.tasa_interes_mensual / 100)

            # El capital es fijo
            self.monto_capital = self.prestamo.pago_fijo_capital

            # Total cobrado
            self.monto_cobrado = self.monto_capital + self.monto_interes

            # Nuevo saldo
            self.saldo_actual = saldo_anterior - self.monto_capital

            # Actualizar saldo del préstamo
            self.prestamo.saldo_actual = self.saldo_actual

            # Si saldo llega a 0, marcar como concluido
            if self.saldo_actual <= 0:
                self.prestamo.estado = 'CONCLUIDO'
            elif self.prestamo.estado == 'APROBADO':
                self.prestamo.estado = 'ACTIVO'

            self.prestamo.save()

        super().save(*args, **kwargs)
```

**Conceptos nuevos:**

#### unique_together

```python
unique_together = [['prestamo', 'numero_abono']]
```

- No permite duplicados de la combinación
- Un préstamo no puede tener dos "Abono #1"

#### Cálculos automáticos en save()

```python
self.monto_interes = saldo_anterior * (tasa / 100)
```

- Fórmula: Interés = Saldo × Tasa
- Ejemplo: $20,000 × 0.01 = $200

### Paso 5: Crear Migraciones

```bash
# Crear migraciones
docker compose exec web python manage.py makemigrations prestamos

# Aplicar migraciones
docker compose exec web python manage.py migrate prestamos
```

✅ **Checkpoint:** Las tablas de Préstamo y Abono fueron creadas.

---

## 🔐 Parte 2: Validaciones de Negocio

### ¿Por qué validaciones?

Las validaciones aseguran que los datos cumplan las reglas del negocio.

**Ejemplo:** No permitir que un empleado con 6 meses solicite un préstamo (requiere 1 año).

### Tipos de Validaciones en Django

1. **Validaciones a nivel de campo** (ya usamos algunas)
2. **Validaciones a nivel de modelo** (vamos a agregar)
3. **Validaciones en formularios** (próxima sesión)

### Paso 1: Agregar Validación clean()

En `prestamos/models.py`, agrega este método en la clase `Prestamo`:

```python
# prestamos/models.py (dentro de la clase Prestamo)

def clean(self):
    """
    Validaciones personalizadas del modelo.
    Se ejecuta automáticamente antes de guardar.
    """
    from django.core.exceptions import ValidationError

    # Solo validar en préstamos nuevos o en estado SOLICITADO
    if not self.pk or self.estado == 'SOLICITADO':
        puede, mensaje = self.puede_solicitar_prestamo()
        if not puede:
            raise ValidationError(mensaje)

    # Validar fechas
    if self.fecha_aprobacion and self.fecha_aprobacion < self.fecha_solicitud:
        raise ValidationError("La fecha de aprobación no puede ser anterior a la solicitud")
```

**Cómo funciona:**

- `clean()` se ejecuta antes de `save()`
- Si algo está mal, lanza `ValidationError`
- El error se muestra al usuario

### Paso 2: Agregar Validaciones en Empleado

Edita `empleados/models.py` y agrega métodos en la clase `Empleado`:

```python
# empleados/models.py (dentro de la clase Empleado)

def calcular_antiguedad(self):
    """
    Calcula los años de antigüedad del empleado.
    """
    from datetime import date
    dias = (date.today() - self.fecha_ingreso).days
    return dias / 365.25  # .25 por años bisiestos

def obtener_puesto_actual(self):
    """
    Retorna el puesto actual del empleado.
    """
    historial = self.historial_puestos.filter(fecha_fin__isnull=True).first()
    return historial.puesto if historial else None

def obtener_sueldo_actual(self):
    """
    Retorna el sueldo actual del empleado.
    """
    puesto = self.obtener_puesto_actual()
    return puesto.sueldo if puesto else 0

def puede_solicitar_prestamo(self):
    """
    Verifica si el empleado cumple los requisitos para solicitar préstamo.
    """
    # Verificar que esté activo
    if not self.activo:
        return False, "El empleado no está activo"

    # Verificar antigüedad
    if self.calcular_antiguedad() < 1:
        return False, "Requiere mínimo 1 año de antigüedad"

    # Verificar préstamos activos
    from prestamos.models import Prestamo
    tiene_activo = Prestamo.objects.filter(
        empleado=self,
        estado='ACTIVO'
    ).exists()

    if tiene_activo:
        return False, "Ya tiene un préstamo activo"

    return True, "Puede solicitar préstamo"
```

### Paso 3: Probar las Validaciones

```bash
# Abrir shell de Django
docker compose exec web python manage.py shell
```

```python
# Probar validaciones
from empleados.models import Empleado
from prestamos.models import Prestamo
from datetime import date, timedelta

# Obtener un empleado
empleado = Empleado.objects.first()

# Verificar si puede solicitar
puede, mensaje = empleado.puede_solicitar_prestamo()
print(f"¿Puede solicitar? {puede} - {mensaje}")

# Intentar crear un préstamo con monto muy alto
prestamo = Prestamo(
    empleado=empleado,
    monto=1000000,  # ← Monto muy alto
    plazo_meses=12,
)
prestamo.full_clean()  # Esto lanzará ValidationError
```

---

## 🎨 Parte 3: Registrar en Admin

### Paso 1: Admin de Préstamo

Edita `prestamos/admin.py`:

```python
from django.contrib import admin
from .models import Prestamo, Abono

@admin.register(Prestamo)
class PrestamoAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'empleado',
        'monto',
        'plazo_meses',
        'estado',
        'saldo_actual',
        'fecha_solicitud'
    ]

    list_filter = ['estado', 'fecha_solicitud']
    search_fields = ['empleado__nombre']
    readonly_fields = ['pago_fijo_capital', 'saldo_actual']

    fieldsets = (
        ('Información del Empleado', {
            'fields': ('empleado',)
        }),
        ('Detalles del Préstamo', {
            'fields': (
                'monto',
                'plazo_meses',
                'tasa_interes_mensual',
                'pago_fijo_capital'
            )
        }),
        ('Fechas', {
            'fields': (
                'fecha_solicitud',
                'fecha_aprobacion',
                'fecha_inicio_descuento',
                'fecha_fin_descuento'
            )
        }),
        ('Estado', {
            'fields': ('estado', 'saldo_actual')
        }),
    )

    def save_model(self, request, obj, form, change):
        """
        Personaliza el guardado desde el admin.
        """
        if not change:  # Si es nuevo
            obj.save()  # Esto ejecutará nuestras validaciones
        else:
            obj.save()

@admin.register(Abono)
class AbonoAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'prestamo',
        'numero_abono',
        'fecha',
        'monto_capital',
        'monto_interes',
        'monto_cobrado',
        'saldo_actual'
    ]

    list_filter = ['fecha']
    readonly_fields = [
        'monto_capital',
        'monto_interes',
        'monto_cobrado',
        'saldo_actual'
    ]

    def has_change_permission(self, request, obj=None):
        """
        No permitir modificar abonos ya creados.
        """
        return False
```

**Conceptos nuevos:**

#### fieldsets

- Organiza campos en secciones
- Mejora la legibilidad

#### readonly_fields

- Campos que no se pueden editar
- Solo lectura en el admin

#### has_change_permission

- Controla permisos
- `return False` = no se puede editar

---

## 🚀 Parte 4: API REST Básica

### ¿Qué es una API REST?

**API** = Application Programming Interface (Interfaz de Programación)  
**REST** = Representational State Transfer

Es una forma de que otras aplicaciones se comuniquen con tu sistema usando HTTP.

**Ejemplo:**

```
GET /api/empleados/     → Lista de empleados (JSON)
POST /api/prestamos/    → Crear préstamo
```

### Paso 1: Instalar Django REST Framework

Edita `requirements.txt`:

```txt
Django==5.0.2
psycopg2-binary==2.9.9
python-decouple==3.8
djangorestframework==3.14.0  # ← Agregar esta línea
```

```bash
# Reconstruir imagen
docker compose build

# Reiniciar servicios
docker compose up
```

### Paso 2: Configurar REST Framework

Edita `config/settings.py`:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',  # ← Agregar
    'empleados',
    'prestamos',
]

# Agregar al final del archivo
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}
```

### Paso 3: Crear Serializers

Los **serializers** convierten modelos a JSON y viceversa.

Crea `empleados/serializers.py`:

```python
from rest_framework import serializers
from .models import Empleado, Puesto, HistorialPuesto

class PuestoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Puesto
        fields = ['id', 'nombre', 'sueldo']

class EmpleadoSerializer(serializers.ModelSerializer):
    # Campos calculados
    antiguedad = serializers.SerializerMethodField()
    puesto_actual = serializers.SerializerMethodField()

    class Meta:
        model = Empleado
        fields = [
            'id',
            'nombre',
            'fecha_ingreso',
            'activo',
            'antiguedad',
            'puesto_actual'
        ]

    def get_antiguedad(self, obj):
        """Calcula antigüedad en años."""
        return round(obj.calcular_antiguedad(), 2)

    def get_puesto_actual(self, obj):
        """Obtiene el puesto actual."""
        puesto = obj.obtener_puesto_actual()
        if puesto:
            return PuestoSerializer(puesto).data
        return None

class HistorialPuestoSerializer(serializers.ModelSerializer):
    empleado_nombre = serializers.CharField(source='empleado.nombre', read_only=True)
    puesto_nombre = serializers.CharField(source='puesto.nombre', read_only=True)

    class Meta:
        model = HistorialPuesto
        fields = [
            'id',
            'empleado',
            'empleado_nombre',
            'puesto',
            'puesto_nombre',
            'fecha_inicio',
            'fecha_fin'
        ]
```

Crea `prestamos/serializers.py`:

```python
from rest_framework import serializers
from .models import Prestamo, Abono
from empleados.serializers import EmpleadoSerializer

class PrestamoSerializer(serializers.ModelSerializer):
    empleado_detalle = EmpleadoSerializer(source='empleado', read_only=True)
    total_abonos = serializers.SerializerMethodField()

    class Meta:
        model = Prestamo
        fields = [
            'id',
            'empleado',
            'empleado_detalle',
            'monto',
            'plazo_meses',
            'fecha_solicitud',
            'fecha_aprobacion',
            'tasa_interes_mensual',
            'pago_fijo_capital',
            'fecha_inicio_descuento',
            'fecha_fin_descuento',
            'saldo_actual',
            'estado',
            'total_abonos'
        ]
        read_only_fields = ['pago_fijo_capital', 'saldo_actual']

    def get_total_abonos(self, obj):
        """Cuenta el número de abonos."""
        return obj.abonos.count()

class AbonoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Abono
        fields = [
            'id',
            'prestamo',
            'numero_abono',
            'fecha',
            'monto_capital',
            'monto_interes',
            'monto_cobrado',
            'saldo_actual'
        ]
        read_only_fields = [
            'monto_capital',
            'monto_interes',
            'monto_cobrado',
            'saldo_actual'
        ]
```

### Paso 4: Crear ViewSets

Los **ViewSets** manejan las peticiones HTTP.

Crea `empleados/views.py`:

```python
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Empleado, Puesto, HistorialPuesto
from .serializers import (
    EmpleadoSerializer,
    PuestoSerializer,
    HistorialPuestoSerializer
)

class PuestoViewSet(viewsets.ModelViewSet):
    queryset = Puesto.objects.all()
    serializer_class = PuestoSerializer

class EmpleadoViewSet(viewsets.ModelViewSet):
    queryset = Empleado.objects.all()
    serializer_class = EmpleadoSerializer

    @action(detail=True, methods=['get'])
    def historial_puestos(self, request, pk=None):
        """
        Endpoint personalizado: /api/empleados/{id}/historial_puestos/
        """
        empleado = self.get_object()
        historial = empleado.historial_puestos.all()
        serializer = HistorialPuestoSerializer(historial, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def puede_solicitar_prestamo(self, request, pk=None):
        """
        Endpoint: /api/empleados/{id}/puede_solicitar_prestamo/
        """
        empleado = self.get_object()
        puede, mensaje = empleado.puede_solicitar_prestamo()
        return Response({
            'puede_solicitar': puede,
            'mensaje': mensaje
        })

class HistorialPuestoViewSet(viewsets.ModelViewSet):
    queryset = HistorialPuesto.objects.all()
    serializer_class = HistorialPuestoSerializer
```

Crea`prestamos/views.py`:

```python
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .models import Prestamo, Abono
from .serializers import PrestamoSerializer, AbonoSerializer

class PrestamoViewSet(viewsets.ModelViewSet):
    queryset = Prestamo.objects.all()
    serializer_class = PrestamoSerializer

    @action(detail=True, methods=['post'])
    def aprobar(self, request, pk=None):
        """
        Endpoint: /api/prestamos/{id}/aprobar/
        """
        prestamo = self.get_object()
        fecha_inicio = request.data.get('fecha_inicio')

        if not fecha_inicio:
            return Response(
                {'error': 'Se requiere fecha_inicio'},
                status=status.HTTP_400_BAD_REQUEST
            )

        from datetime import datetime
        fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()

        prestamo.aprobar(fecha_inicio)
        serializer = self.get_serializer(prestamo)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def abonos(self, request, pk=None):
        """
        Endpoint: /api/prestamos/{id}/abonos/
        """
        prestamo = self.get_object()
        abonos = prestamo.abonos.all()
        serializer = AbonoSerializer(abonos, many=True)
        return Response(serializer.data)

class AbonoViewSet(viewsets.ModelViewSet):
    queryset = Abono.objects.all()
    serializer_class = AbonoSerializer
```

### Paso 5: Configurar URLs

Crea `empleados/urls.py`:

```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmpleadoViewSet, PuestoViewSet, HistorialPuestoViewSet

router = DefaultRouter()
router.register(r'empleados', EmpleadoViewSet)
router.register(r'puestos', PuestoViewSet)
router.register(r'historial-puestos', HistorialPuestoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
```

Crea `prestamos/urls.py`:

```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PrestamoViewSet, AbonoViewSet

router = DefaultRouter()
router.register(r'prestamos', PrestamoViewSet)
router.register(r'abonos', AbonoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
```

Edita `config/urls.py`:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('empleados.urls')),
    path('api/', include('prestamos.urls')),
]
```

### Paso 6: Probar la API

Ve a tu navegador y prueba estos endpoints:

```
http://localhost:8000/api/empleados/
http://localhost:8000/api/puestos/
http://localhost:8000/api/prestamos/
http://localhost:8000/api/empleados/1/
http://localhost:8000/api/empleados/1/historial_puestos/
http://localhost:8000/api/empleados/1/puede_solicitar_prestamo/
```

Django REST Framework incluye una interfaz web interactiva para probar.

---

## 📝 Ejercicio Práctico

**Objetivo:** Crear un endpoint personalizado para obtener el reporte de un préstamo.

```python
# En prestamos/views.py, dentro de PrestamoViewSet

@action(detail=True, methods=['get'])
def reporte(self, request, pk=None):
    """
    Endpoint: /api/prestamos/{id}/reporte/
    """
    prestamo = self.get_object()
    abonos = prestamo.abonos.all()

    return Response({
        'prestamo': PrestamoSerializer(prestamo).data,
        'abonos': AbonoSerializer(abonos, many=True).data,
        'resumen': {
            'total_pagado': sum(a.monto_cobrado for a in abonos),
            'total_interes': sum(a.monto_interes for a in abonos),
            'abonos_realizados': abonos.count(),
            'abonos_pendientes': prestamo.plazo_meses - abonos.count()
        }
    })
```

---

## ✅ Checklist de la Sesión

- [ ] Modelos completos (Prestamo, Abono)
- [ ] Validaciones implementadas
- [ ] Métodos personalizados creados
- [ ] Admin configurado
- [ ] Django REST Framework instalado
- [ ] Serializers creados
- [ ] ViewSets implementados
- [ ] URLs configuradas
- [ ] API funcionando

---

## 🎯 Para la Próxima Sesión

Prepárate para:

- Crear templates HTML
- Implementar vistas con formularios
- Generar reportes en PDF
- Mejorar la interfaz de usuario

---

**¡Excelente trabajo!** Ya tienes un backend completo con API REST. 🚀
