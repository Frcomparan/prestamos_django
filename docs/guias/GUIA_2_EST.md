# Sesión 2: Backend - Modelos Completos, Controladores y Templates

**Duración estimada:** 3-4 horas  
**Nivel:** Intermedio  
**Prerequisito:** Sesión 1 completada

## 🎯 Objetivos de la Sesión

Al finalizar esta sesión, podrás:

- ✅ Completar los modelos de Préstamos y Abonos
- ✅ Agregar validaciones de negocio
- ✅ Crear métodos personalizados en modelos
- ✅ Implementar CRUD básico de Empleados con controladores y templates
- ✅ Dejar definido el plan para CRUD de Préstamos como actividad

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

## 🖥️ Parte 4: Configuración de Templates y Archivos Estáticos

En esta sección, prepararemos la estructura para servir templates e archivos estáticos desde Django.

### Paso 1: Crear Estructura de Carpetas de Templates

Desde la raíz del proyecto (donde está `manage.py`), crea la siguiente estructura:

```bash
mkdir -p templates/components
mkdir -p templates/empleados
mkdir -p templates/prestamos
```

Tu estructura debe verse así:

```
aplicacion_prestamos/
├── templates/
│   ├── base.html                    # Template base (navbar, footer, etc)
│   ├── components/
│   │   ├── navbar.html             # Navegación reutilizable
│   │   └── footer.html             # Pie de página
│   ├── empleados/
│   │   ├── empleado_list.html      # Listado de empleados
│   │   ├── empleado_detail.html    # Detalle de un empleado
│   │   ├── empleado_form.html      # Formulario crear/editar
│   │   └── empleado_confirm_delete.html
│   └── prestamos/
│       ├── prestamo_list.html
│       ├── prestamo_form.html
│       └── prestamo_confirm_delete.html
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── main.js
│   └── img/
│       └── logo.png
├── manage.py
└── ...
```

### Paso 2: Configurar Django para Templates

Edita `config/settings.py` y busca la sección `TEMPLATES`:

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',  # ← Agregar esta línea
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

**Explicación:**

- **DIRS**: Lista de carpetas donde Django busca templates globales
- **APP_DIRS**: Si está True, Django también busca en `app/templates/` de cada app
- **BASE_DIR / 'templates'**: Ruta absoluta a la carpeta de templates

### Paso 3: Archivos Estáticos (CSS, Imágenes, JavaScript)

Los **archivos estáticos** son aquellos que no cambian según el usuario:

- **CSS**: Estilos visuales
- **JavaScript**: Lógica del navegador
- **Imágenes**: Logo, iconos, fotos

#### Paso A: Crear Estructura de Carpetas

En la raíz del proyecto (donde está `manage.py`), crea:

```bash
mkdir -p static/css static/js static/img
```

Tu estructura debe verse así:

```
aplicacion_prestamos/
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── main.js
│   └── img/
│       └── logo.png
├── templates/
├── manage.py
└── ...
```

#### Paso B: Crear CSS Base

Crea `static/css/style.css`:

```css
/* Estilos globales */
:root {
  --primary: #0f766e;
  --danger: #b91c1c;
  --success: #16a34a;
  --gray: #6b7280;
}

body {
  font-family: Arial, sans-serif;
  margin: 0;
  padding: 20px;
  background-color: #f3f4f6;
}

table {
  border-collapse: collapse;
  width: 100%;
  background: white;
  margin: 20px 0;
}

table th {
  background-color: var(--primary);
  color: white;
  padding: 12px;
  text-align: left;
}

table td {
  padding: 10px;
  border-bottom: 1px solid #e5e7eb;
}

table tr:hover {
  background-color: #f9fafb;
}

.btn {
  display: inline-block;
  padding: 8px 16px;
  margin: 4px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  text-decoration: none;
  font-size: 14px;
}

.btn-primary {
  background-color: var(--primary);
  color: white;
}

.btn-primary:hover {
  background-color: #0d5a52;
}

.btn-danger {
  background-color: var(--danger);
  color: white;
}

.btn-danger:hover {
  background-color: #991b1b;
}

form {
  background: white;
  padding: 20px;
  border-radius: 4px;
  margin: 20px 0;
  max-width: 600px;
}

form label {
  display: block;
  margin: 10px 0 5px 0;
  font-weight: bold;
  color: var(--gray);
}

form input,
form select {
  width: 100%;
  padding: 8px;
  margin-bottom: 15px;
  border: 1px solid #d1d5db;
  border-radius: 4px;
  box-sizing: border-box;
}

form input:focus,
form select:focus {
  border-color: var(--primary);
  outline: none;
}

.card {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
}

h1 {
  color: var(--primary);
  margin-top: 0;
}

.error {
  background-color: #fee2e2;
  color: #991b1b;
  padding: 12px;
  border-left: 4px solid var(--danger);
  margin-bottom: 20px;
}
```

#### Paso C: Crear JavaScript Base

Crea `static/js/main.js`:

```javascript
// Confirmar eliminaciones
document.addEventListener('DOMContentLoaded', function () {
  const deleteButtons = document.querySelectorAll('[data-confirm="delete"]');

  deleteButtons.forEach((button) => {
    button.addEventListener('click', function (e) {
      const name = this.getAttribute('data-name');
      if (!confirm(`¿Seguro que deseas eliminar: ${name}?`)) {
        e.preventDefault();
      }
    });
  });
});

// Validación simple de formularios
function validarMonto(value) {
  if (isNaN(value) || value <= 0) {
    alert('El monto debe ser un número positivo');
    return false;
  }
  return true;
}
```

#### Paso D: Actualizar Base Template

Edita `templates/base.html` y usa `{% load static %}` en la cabecera:

```html
{% load static %}
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{% block title %}Sistema de Prestamos{% endblock %}</title>

    <!-- CSS externo -->
    <link rel="stylesheet" href="{% static 'css/style.css' %}" />
    {% block extra_css %}{% endblock %}
  </head>
  <body>
    <!-- Navbar y contenido aquí -->

    <!-- JavaScript externo -->
    <script src="{% static 'js/main.js' %}"></script>
    {% block extra_js %}{% endblock %}
  </body>
</html>
```

**Conceptos clave:**

- **`{% load static %}`**: Activa el sistema de archivos estáticos de Django
- **`{% static 'css/style.css' %}`**: Genera la URL correcta del archivo (`/static/css/style.css`)
- **En desarrollo**: Django sirve automáticamente desde la carpeta `static/`
- **En producción**: Ejecutar `python manage.py collectstatic` para copiar los archivos

#### Paso E: Usar Imágenes en Templates

Ejemplo de cómo usar una imagen en `templates/components/navbar.html`:

```html
{% load static %}
<header style="background: #0b3c5d; color: #fff; padding: 10px;">
  <div style="display: flex; align-items: center; gap: 15px;">
    <img src="{% static 'img/logo.png' %}" alt="Logo" style="height: 50px;" />
    <strong>Sistema de Prestamos</strong>
  </div>
</header>
```

#### Paso F: Cargar CSS en un Template Específico

Si necesitas CSS adicional solo para una página:

```html
{% extends "base.html" %} {% load static %} {% block extra_css %}
<link rel="stylesheet" href="{% static 'css/empleados-styles.css' %}" />
{% endblock %} {% block content %}
<!-- Contenido -->
{% endblock %}
```

#### Paso G: Incluir JavaScript en un Template

```html
{% extends "base.html" %} {% load static %} {% block extra_js %}
<script src="{% static 'js/empleados-validation.js' %}"></script>
{% endblock %} {% block content %}
<form onsubmit="return validarMonto(document.getElementById('monto').value)">
  <!-- Formulario -->
</form>
{% endblock %}
```

#### ¿Dónde va cada cosa?

| Archivo        | Camino                     | Uso                 |
| -------------- | -------------------------- | ------------------- |
| CSS global     | `static/css/style.css`     | Todos los templates |
| CSS específico | `static/css/empleados.css` | Solo empleados      |
| JS global      | `static/js/main.js`        | Todos los templates |
| JS específico  | `static/js/empleados.js`   | Solo empleados      |
| Logo           | `static/img/logo.png`      | Header/navbar       |
| Iconos         | `static/img/icons/`        | Botones, tablas     |
| Fotos          | `static/img/uploads/`      | Galería             |

---

### Paso 4: Probar CRUD de Empleados

Levanta el proyecto:

```bash
docker compose up
```

Abre en el navegador:

```
http://localhost:8000/empleados/
```

Valida lo siguiente:

1. Puedes crear un empleado.
2. Puedes editar un empleado.
3. Puedes eliminar un empleado.
4. La lista se actualiza correctamente.

---

## 📝 Actividad (Controladores y Templates de Préstamos)

Como práctica para reforzar, implementa CRUD de préstamos con el mismo patrón usado en empleados.

### Requisitos mínimos

1. Crear rutas en `prestamos/urls.py` para listar, crear, editar y eliminar.
2. Crear controladores en `prestamos/views.py` para esas rutas.
3. Crear templates en `prestamos/templates/prestamos/`:
   - `prestamo_list.html`
   - `prestamo_form.html`
   - `prestamo_confirm_delete.html`
4. Mostrar en la lista: empleado, monto, plazo, estado y saldo.
5. Reutilizar las validaciones del modelo `Prestamo` al guardar.

### Entregable de la actividad

- Captura de la lista de préstamos funcionando.
- Captura del formulario de creación.
- Captura de una validación fallando correctamente (por ejemplo monto excesivo).

---

## ✅ Checklist de la Sesión

- [ ] Modelos completos (Prestamo, Abono)
- [ ] Validaciones implementadas
- [ ] Métodos personalizados creados
- [ ] Admin configurado
- [ ] URLs de empleados configuradas
- [ ] Controladores de empleados implementados
- [ ] Templates de empleados creados
- [ ] CRUD de empleados funcionando
- [ ] Actividad de préstamos asignada

---

## 🎯 Para la Próxima Sesión

Prepárate para:

- Integrar formularios de Django
- Mejorar estilos con base template
- Generar reportes en PDF
- Mejorar la interfaz de usuario

---

**¡Excelente trabajo!** Ya tienes backend completo y primer CRUD web con controladores y templates. 🚀
