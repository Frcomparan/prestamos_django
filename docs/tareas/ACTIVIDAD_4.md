# Actividad para Casa 4: Completar Backend de Préstamos y Reorganizar Apps

**Curso:** Taller de Django  
**Tipo:** Actividad individual  
**Tiempo estimado:** 90-120 minutos

---

## 🎯 Objetivo

Completar los temas pendientes, dejando listo el backend de préstamos con:

- Organización del proyecto moviendo las apps `empleados` y `prestamos` a una carpeta `apps`
- Modelos completos de `Prestamo` y `Abono`
- Métodos de apoyo y validaciones de negocio
- Configuración avanzada del Django Admin para préstamos y abonos

---

## 📋 Prerrequisitos

Antes de iniciar, asegúrate de tener:

- ✅ Proyecto Django funcionando con Docker
- ✅ Base de datos PostgreSQL configurada
- ✅ App `empleados` funcionando
- ✅ Modelos `Puesto`, `Empleado` y `HistorialPuesto` creados
- ✅ Admin de empleados configurado
- ✅ Superusuario creado

**⚠️ Importante:** Esta actividad da continuidad a la Sesión 1 y a las actividades anteriores. Antes de empezar, asegúrate de que tu proyecto levanta correctamente con `docker compose up`.

---

## 🧭 Resultado Esperado

Al finalizar esta actividad, tu proyecto debe cumplir con lo siguiente:

```text
proyecto/
├── apps/
│   ├── __init__.py
│   ├── empleados/
│   └── prestamos/
├── config/
├── manage.py
├── docker-compose.yml
└── ...
```

Y además:

- La app `prestamos` debe tener los modelos `Prestamo` y `Abono`
- El modelo `Empleado` debe incluir utilidades para validaciones
- Deben ejecutarse correctamente las migraciones
- El admin debe permitir administrar préstamos y registrar abonos con restricciones

---

## 📝 Instrucciones de la Actividad

### Paso 1: Verificar que todo sigue funcionando antes de reorganizar

Antes de mover carpetas, primero verifica que tu proyecto actual funciona. Esto te servirá para comparar si algo falla después.

#### 1.1 Verificar contenedores

```bash
docker compose ps
```

**✅ Verificación:** Debes ver los servicios `web` y `db` con estado "Up".

Si no están corriendo:

```bash
docker compose up -d
```

#### 1.2 Ejecutar una revisión rápida del proyecto

```bash
docker compose exec web python manage.py check
```

**¿Qué hace este comando?**

- Revisa errores comunes de configuración en Django
- Detecta problemas en modelos, apps y admin
- No modifica nada, solo valida

**✅ Verificación:** Debes ver un mensaje como:

```text
System check identified no issues (0 silenced).
```

---

### Paso 2: Organizar el proyecto dentro de una carpeta `apps`

En esta actividad vamos a mover las apps `empleados` y `prestamos` a una carpeta llamada `apps`.

#### 2.1 Crear la carpeta `apps`

Puedes hacerlo desde el explorador de archivos o con comandos.

**Opción con PowerShell (Windows):**

```powershell
New-Item -ItemType Directory apps
New-Item -ItemType File apps\__init__.py
```

**Opción con terminal tipo bash:**

```bash
mkdir apps
touch apps/__init__.py
```

**Explicación:**

- La carpeta `apps/` servirá para agrupar las aplicaciones del proyecto
- El archivo `__init__.py` indica a Python que `apps` es un paquete importable

#### 2.2 Mover las apps `empleados` y `prestamos`

**Opción con PowerShell (Windows):**

```powershell
Move-Item empleados apps\
Move-Item prestamos apps\
```

**Opción con terminal tipo bash:**

```bash
mv empleados apps/
mv prestamos apps/
```

**✅ Verificación:** La estructura debe verse así:

```text
proyecto/
├── apps/
│   ├── __init__.py
│   ├── empleados/
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── migrations/
│   │   └── models.py
│   └── prestamos/
│       ├── admin.py
│       ├── apps.py
│       ├── migrations/
│       └── models.py
├── config/
└── manage.py
```

**⚠️ Importante:**

- No elimines las carpetas `migrations/`
- No cambies el nombre de las apps; solo cambia su ubicación
- Si `prestamos` todavía no existe, la crearás en el paso 5 dentro de `apps/`

---

### Paso 3: Actualizar la configuración para que Django reconozca las apps movidas

Mover carpetas no es suficiente. Ahora debes actualizar la configuración del proyecto.

#### 3.1 Editar `apps.py` de `empleados`

Abre el archivo `apps/empleados/apps.py` y actualízalo así:

```python
from django.apps import AppConfig


class EmpleadosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.empleados'
```

**Explicación:**

- `name = 'apps.empleados'` indica la nueva ruta completa de la app
- Django usará esta ruta para cargar modelos, admin y migraciones

#### 3.2 Editar `apps.py` de `prestamos`

Abre el archivo `apps/prestamos/apps.py` y actualízalo así:

```python
from django.apps import AppConfig


class PrestamosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.prestamos'
```

#### 3.3 Actualizar `INSTALLED_APPS`

Abre `config/settings.py` y reemplaza las referencias anteriores por las nuevas:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.empleados',
    'apps.prestamos',
]
```

**⚠️ Importante:** Si todavía no existe la app `prestamos`, por ahora deja solo la de `empleados` y agrega la de `prestamos` cuando la crees.

#### 3.4 Actualizar imports en el proyecto

Ahora debes corregir todos los imports que apuntaban a `empleados` o `prestamos` directamente.

**Ejemplos de cambio:**

```python
# Antes
from empleados.models import Empleado
from prestamos.models import Prestamo

# Después
from apps.empleados.models import Empleado
from apps.prestamos.models import Prestamo
```

**Archivos donde normalmente debes revisar imports:**

- `apps/empleados/admin.py`
- `apps/empleados/models.py`
- `apps/prestamos/admin.py`
- `apps/prestamos/models.py`
- Cualquier archivo de pruebas o shell scripts si los tienes

#### 3.5 Verificar la reorganización

Ejecuta nuevamente:

```bash
docker compose exec web python manage.py check
```

Si aparece un error de importación, corrígelo antes de continuar.

---

### Paso 4: Actualizar el modelo `Empleado` con métodos de apoyo

La lógica de préstamos depende de que `Empleado` tenga métodos de utilidad.

#### 4.1 Abrir `apps/empleados/models.py`

Debes dejar el modelo `Empleado` con métodos que permitan:

- Calcular antigüedad
- Verificar si tiene puesto asignado
- Obtener puesto actual
- Validar si puede solicitar préstamo

#### 4.2 Código sugerido para `Empleado`

Tu archivo debe contener al menos esta parte:

```python
class Empleado(models.Model):
    nombre = models.CharField(max_length=200)
    fecha_ingreso = models.DateField()
    activo = models.BooleanField(default=True)

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
```

## _NOTA IMPORTANTE:_

Si tu modelo `HistorialPuesto` no tiene el `related_name='historial_puestos'`, debes agregarlo para que los métodos de `Empleado` funcionen correctamente.

```python
class HistorialPuesto(models.Model):
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, related_name='historial_puestos')
    puesto = models.ForeignKey(Puesto, on_delete=models.PROTECT)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)
```

#### 4.3 Explicación de la lógica

**¿Por qué agregar estos métodos en `Empleado`?**

Porque el préstamo depende del estado del empleado. Si el empleado sabe responder preguntas como:

- "¿Está activo?"
- "¿Tiene puesto actual?"
- "¿Tiene antigüedad suficiente?"

entonces el modelo `Prestamo` solo reutiliza esa lógica sin repetir código.

**Concepto clave:**

> Un modelo no solo guarda datos. También puede tener comportamiento útil y reutilizable.

---

### Paso 5: Crear o completar la app `prestamos`

Si todavía no existe la app `prestamos`, créala ahora dentro del proyecto.

#### 5.1 Crear la app `prestamos` si hace falta

Si aún no la tienes creada, ejecuta:

```bash
docker compose exec web python manage.py startapp prestamos
```

Luego muévela dentro de `apps/` como se explicó antes.

Si ya existe, continúa al siguiente paso.

#### 5.2 Importaciones necesarias en `apps/prestamos/models.py`

El archivo debe comenzar así:

```python
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.empleados.models import Empleado
```

---

### Paso 6: Crear el modelo `Prestamo`

#### 6.1 Agregar el modelo completo

En `apps/prestamos/models.py`, crea el modelo `Prestamo` con esta estructura base:

```python
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
```

#### 6.1.1 Lectura rápida del modelo

- Este modelo concentra la información principal del préstamo.
- Primero indica **quién** solicita el préstamo (`empleado`).
- Después guarda **cuánto** pide y **a cuántos meses** (`monto`, `plazo_meses`).
- También controla el flujo del trámite con fechas y estado.
- Finalmente incluye los campos que se usarán para cálculos financieros.

#### 6.1.2 Cómo leer este código

La forma más fácil de entenderlo es por grupos:

- **Relación:** `empleado`
- **Datos base:** `monto`, `plazo_meses`
- **Fechas:** solicitud, aprobación, inicio y fin de descuento
- **Cálculos:** tasa, pago fijo y saldo
- **Control:** `estado`

#### 6.2 Agregar comportamiento en `save()`

El modelo debe calcular automáticamente el pago fijo a capital y el saldo inicial.

```python
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
```

#### 6.2.1 Explicación rápida de `save()`

- `save()` se ejecuta cada vez que el objeto se guarda.
- Aquí se aprovecha para calcular automáticamente datos que no conviene capturar a mano.
- `if not self.pk` significa que el objeto todavía no existe en la base de datos.
- `super().save()` es la llamada final que realmente guarda el registro.

#### 6.2.2 Ejemplo mental

Si un empleado solicita `$24,000` a `12` meses:

- `pago_fijo_capital = 24000 / 12 = 2000`
- `saldo_actual = 24000` al momento de crear el préstamo

#### 6.3 Agregar `__str__()`

```python
def __str__(self):
    # Define cómo se mostrará el objeto en el admin y en la shell.
    return f"Préstamo de {self.empleado.nombre} por {self.monto:.2f} a {self.plazo_meses} meses - Estado: {self.estado}"
```

#### 6.3.1 Explicación rápida de `__str__()`

- Sin este método, Django mostraría algo poco útil como `Prestamo object (1)`.
- Con este método, el registro se ve más claro en el admin y en la terminal.
- Es una mejora de lectura, no una validación.

#### 6.4 Explicación rápida

- `monto`: dinero solicitado
- `plazo_meses`: duración del préstamo
- `fecha_solicitud`: se registra automáticamente
- `tasa_interes_mensual`: porcentaje mensual
- `pago_fijo_capital`: parte fija del pago mensual
- `saldo_actual`: cuánto debe todavía el empleado
- `estado`: control del ciclo del préstamo

---

### Paso 7: Agregar validaciones de negocio al modelo `Prestamo`

Aquí comienza el trabajo del módulo 2.

#### 7.1 Método `calcular_monto_maximo()`

Agrega este método al modelo `Prestamo`:

```python
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
```

**¿Qué hace?**

Calcula el monto máximo permitido según el sueldo actual del empleado.

**Regla de negocio:**

> El empleado solo puede solicitar hasta 6 meses de su sueldo actual.

#### 7.1.1 Explicación rápida

- Este método no guarda nada; solo calcula un valor.
- Se apoya en `HistorialPuesto` para saber cuál es el puesto activo.
- Si no encuentra puesto activo, devuelve `0`.

#### 7.1.2 Ejemplo

Si el puesto actual del empleado tiene sueldo de `$15,000`:

- monto máximo = `15000 * 6`
- monto máximo = `$90,000`

#### 7.2 Método `puede_solicitar_prestamo()`

```python
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
```

#### 7.2.1 Explicación rápida

- Este método funciona como una lista de chequeo.
- Primero valida que exista empleado.
- Después reutiliza reglas del modelo `Empleado`.
- Al final compara el monto solicitado contra el máximo permitido.

#### 7.2.2 Idea importante

Aquí se está aplicando una buena práctica: **no duplicar lógica**.

En lugar de volver a escribir todas las validaciones del empleado dentro de `Prestamo`, se llama al método `self.empleado.puede_solicitar_prestamo(...)`.

#### 7.3 Método `clean()`

```python
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
```

**Explicación:**

- `clean()` se usa para validaciones de negocio más complejas
- Si el préstamo no cumple las reglas, Django lanza `ValidationError`
- Esto evita guardar datos incorrectos en la base de datos

#### 7.3.1 Cuándo usar `clean()`

Usa `clean()` cuando la validación:

- dependa de varios campos al mismo tiempo
- dependa de reglas del negocio
- no pueda resolverse solo con `MinValueValidator` o `MaxValueValidator`

#### 7.3.2 Diferencia rápida entre validadores y `clean()`

- `validators`: validan un campo individual
- `clean()`: valida relaciones entre campos y reglas completas del modelo

---

### Paso 8: Crear el modelo `Abono`

Este modelo representa cada pago realizado sobre un préstamo.

#### 8.1 Agregar el modelo `Abono`

En el mismo archivo `apps/prestamos/models.py`, agrega:

```python
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
```

#### 8.1.1 Lectura rápida del modelo `Abono`

- Cada `Abono` pertenece a un `Prestamo`.
- El abono guarda cuánto se fue a capital, cuánto se cobró de interés y cuál es el nuevo saldo.
- Este modelo permite construir el historial completo de pagos del préstamo.

#### 8.2 Agregar lógica automática en `save()`

```python
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
```

**¿Qué hace esta lógica?**

- Calcula el interés del abono
- Calcula el total cobrado
- Reduce el saldo del préstamo
- Actualiza el estado a `CONCLUIDO` cuando el saldo llega a cero
- Asigna el número consecutivo del abono automáticamente

#### 8.2.1 Explicación paso a paso

El orden del cálculo importa mucho:

1. Primero se toma el saldo anterior.
2. Después se calcula el interés con ese saldo.
3. Luego se asigna el capital fijo.
4. Se obtiene el total cobrado.
5. Finalmente se calcula el nuevo saldo.

Si cambias este orden, los resultados pueden salir mal.

#### 8.2.2 Ejemplo rápido

Supongamos este préstamo:

- `saldo_actual = 20000`
- `tasa_interes_mensual = 1.00`
- `pago_fijo_capital = 1000`

Entonces el abono quedaría así:

- `monto_interes = 20000 * 0.01 = 200`
- `monto_capital = 1000`
- `monto_cobrado = 1000 + 200 = 1200`
- `saldo_actual = 20000 - 1000 = 19000`

---

### Paso 9: Crear y aplicar migraciones

Una vez terminados los modelos, debes reflejar los cambios en la base de datos.

#### 9.1 Crear migraciones

```bash
docker compose exec web python manage.py makemigrations empleados prestamos
```

#### 9.2 Aplicar migraciones

```bash
docker compose exec web python manage.py migrate
```

#### 9.3 Verificar que no haya errores

```bash
docker compose exec web python manage.py check
```

**✅ Verificación esperada:**

- No debe haber errores de importación
- No debe haber errores de configuración de apps
- Las migraciones deben aplicarse correctamente

---

### Paso 10: Configurar el admin de préstamos

Aquí completas el módulo 3.

#### 10.1 Crear `apps/prestamos/admin.py`

Tu archivo debe comenzar así:

```python
from django.contrib import admin
from apps.prestamos.models import Prestamo, Abono
```

#### 10.2 Configurar `PrestamoAdmin`

```python
fieldsets = (
    ('Información del empleado', {
        'fields': ('empleado',)
    }),
    ('Detalle del prestamo', {
        'fields': ('monto', 'saldo_actual', 'plazo_meses', 'tasa_interes_mensual')
    }),
)

readonly_fields = ['pago_fijo_capital', 'saldo_actual']


@admin.register(Prestamo)
class PrestamoAdmin(admin.ModelAdmin):
    list_display = ('empleado', 'monto','saldo_actual', 'plazo_meses', 'estado')
    list_filter = ('estado',)
    search_fields = ('empleado__nombre',)
    fieldsets = fieldsets
    readonly_fields = readonly_fields
```

**Explicación:**

- `list_display`: columnas en la lista
- `list_filter`: filtro por estado
- `search_fields`: búsqueda por nombre del empleado
- `fieldsets`: organiza el formulario por secciones
- `readonly_fields`: no permite editar campos calculados manualmente

#### 10.3 Configurar `AbonoAdmin`

```python
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
```

**Explicación de permisos:**

- Un abono no debe editarse una vez creado
- Los montos e interés deben calcularse automáticamente
- Cuando se crea un nuevo abono, el usuario solo selecciona el préstamo

---

### Paso 11: Probar el flujo completo en el admin

Ahora debes comprobar que el trabajo realmente funciona.

#### 11.1 Levantar el proyecto

```bash
docker compose up -d
```

#### 11.2 Entrar al admin

Abre en el navegador:

**http://localhost:8000/admin**

#### 11.3 Crear un préstamo de prueba

Debes crear al menos un préstamo válido para un empleado que:

- Esté activo
- Tenga puesto asignado
- Tenga más de 1 año de antigüedad

#### 11.4 Probar validaciones

Intenta crear un préstamo inválido con alguno de estos casos:

- Monto demasiado alto
- Empleado inactivo
- Empleado sin antigüedad suficiente
- Fecha de aprobación anterior a la solicitud

**✅ Verificación:** Debe aparecer un mensaje de error y no debe guardarse.

#### 11.5 Crear un abono

Desde el admin, crea un abono asociado a un préstamo.

**Verifica que ocurra automáticamente:**

- Se asigne `numero_abono`
- Se calcule `monto_interes`
- Se calcule `monto_cobrado`
- Se actualice `saldo_actual`
- El préstamo cambie de saldo

---

## 📦 Entregables

Para comprobar que completaste la actividad correctamente, debes entregar:

### 1. Captura de la nueva organización del proyecto

**Nombre del archivo:** `estructura_apps.png` o `estructura_apps.jpg`

**Debe mostrar:**

- La carpeta `apps/`
- Las subcarpetas `empleados/` y `prestamos/`
- El archivo `apps/__init__.py`

### 2. Captura de `settings.py`

**Nombre del archivo:** `settings_apps.png` o `settings_apps.jpg`

**Debe mostrar:**

- La sección `INSTALLED_APPS`
- Las referencias:
  - `apps.empleados.apps.EmpleadosConfig`
  - `apps.prestamos.apps.PrestamosConfig`

### 3. Captura del modelo `Empleado`

**Nombre del archivo:** `empleado_validaciones.png` o `empleado_validaciones.jpg`

**Debe mostrar:**

- Los métodos `calcular_antiguedad()`
- `tiene_puesto_asignado()`
- `obtener_puesto_actual()`
- `puede_solicitar_prestamo()`

### 4. Captura del archivo `apps/prestamos/models.py`

**Nombre del archivo:** `prestamos_modelos.png` o `prestamos_modelos.jpg`

**Debe mostrar:**

- El modelo `Prestamo`
- El modelo `Abono`
- Los métodos `save()`, `clean()`, `calcular_monto_maximo()` y `puede_solicitar_prestamo()`

### 5. Captura de las migraciones ejecutadas

**Nombre del archivo:** `migraciones_backend.png` o `migraciones_backend.jpg`

**Debe mostrar:**

- La terminal con `makemigrations`
- La terminal con `migrate`
- Sin errores

### 6. Captura del admin de préstamos

**Nombre del archivo:** `admin_prestamos.png` o `admin_prestamos.jpg`

**Debe mostrar:**

- La sección de préstamos en el admin
- Al menos un préstamo registrado

### 7. Captura del admin de abonos

**Nombre del archivo:** `admin_abonos.png` o `admin_abonos.jpg`

**Debe mostrar:**

- La lista de abonos
- Las columnas calculadas visibles

### 8. Captura de una validación fallando correctamente

**Nombre del archivo:** `validacion_error.png` o `validacion_error.jpg`

**Debe mostrar:**

- El formulario del admin con un error visible
- O la terminal mostrando una `ValidationError`

---

## 📨 Forma de Entrega

**Fecha límite:** Definida por el instructor

**Medio de entrega:** Classroom

**Formato:**

- Crea una carpeta: `NoControl_Apellido_Nombre_A4`
- Incluye las 8 evidencias
- Comprime en formato ZIP
- Nombra el archivo: `NoControl_Apellido_Nombre_A4.zip`

**Ejemplo:**

```text
19460000_Garcia_Juan_A4.zip
├── estructura_apps.png
├── settings_apps.png
├── empleado_validaciones.png
├── prestamos_modelos.png
├── migraciones_backend.png
├── admin_prestamos.png
├── admin_abonos.png
└── validacion_error.png
```

---

## 🔧 Troubleshooting (Solución de Problemas)

### Problema 1: `ModuleNotFoundError: No module named 'empleados'`

**Causa:** Moviste la app, pero no actualizaste imports.

**Solución:**

Busca imports como este:

```python
from empleados.models import Empleado
```

Y cámbialos por:

```python
from apps.empleados.models import Empleado
```

### Problema 2: Django no reconoce la app después de moverla

**Causa:** No actualizaste el valor `name` en `apps.py`.

**Solución:**

Verifica que diga:

```python
name = 'apps.empleados'
```

y

```python
name = 'apps.prestamos'
```

### Problema 3: Error en `INSTALLED_APPS`

**Causa:** Las rutas siguen apuntando a `empleados` o `prestamos` sin el prefijo `apps.`

**Solución:**

Usa:

```python
'apps.empleados.apps.EmpleadosConfig'
'apps.prestamos.apps.PrestamosConfig'
```

### Problema 4: `No changes detected`

**Causa:** No guardaste los archivos o no cambiaste realmente el modelo.

**Solución:**

1. Guarda todos los archivos
2. Ejecuta de nuevo `makemigrations`
3. Revisa que el archivo `models.py` tenga los cambios correctos

### Problema 5: `ValidationError` al crear préstamos válidos

**Causa:** El empleado no cumple alguna regla de negocio.

**Solución:**

Verifica que el empleado:

- Esté activo
- Tenga un puesto actual
- Tenga más de 1 año de antigüedad
- No tenga otro préstamo activo

### Problema 6: No aparece la app `prestamos` en el admin

**Causa:** No registraste los modelos en `apps/prestamos/admin.py` o hay error de importación.

**Solución:**

Verifica:

```python
from apps.prestamos.models import Prestamo, Abono
```

Y confirma que las clases tengan `@admin.register(...)`.

### Problema 7: No se calculan automáticamente los abonos

**Causa:** La lógica del método `save()` de `Abono` está incompleta o tiene error.

**Solución:**

Revisa que el método actualice:

- `monto_interes`
- `monto_capital`
- `monto_cobrado`
- `saldo_actual`
- `self.prestamo.saldo_actual`

### Problema 8: Los campos calculados aparecen editables en el admin

**Causa:** No configuraste `readonly_fields` o `get_readonly_fields()`.

**Solución:**

Revisa las configuraciones de `PrestamoAdmin` y `AbonoAdmin`.

---

## 🎓 Conceptos Clave Aprendidos

Al completar esta actividad, habrás aprendido:

✅ Reorganizar apps dentro de una carpeta `apps/`  
✅ Actualizar `apps.py`, `INSTALLED_APPS` e imports  
✅ Crear modelos complejos con relaciones  
✅ Implementar lógica automática en `save()`  
✅ Implementar validaciones de negocio con `clean()`  
✅ Reutilizar lógica entre modelos  
✅ Configurar Django Admin para modelos con cálculos  
✅ Restringir permisos en el admin  
✅ Probar el flujo completo de backend con préstamos y abonos

---

## 📚 Recursos Adicionales

Si quieres profundizar:

- [Django Models](https://docs.djangoproject.com/es/5.0/topics/db/models/)
- [Model Validation](https://docs.djangoproject.com/es/5.0/ref/models/instances/#validating-objects)
- [Django Admin](https://docs.djangoproject.com/es/5.0/ref/contrib/admin/)
- [Django AppConfig](https://docs.djangoproject.com/es/5.0/ref/applications/)

---

## 📊 Criterios de Evaluación

| Criterio                            | Puntos | Descripción                                                        |
| ----------------------------------- | ------ | ------------------------------------------------------------------ |
| **Organización en carpeta `apps`**  | 20%    | Estructura correcta, `apps.py`, settings e imports actualizados    |
| **Modelos y métodos de backend**    | 30%    | `Prestamo`, `Abono` y métodos de apoyo implementados correctamente |
| **Validaciones de negocio**         | 20%    | Reglas funcionando en `Empleado` y `Prestamo`                      |
| **Admin de préstamos y abonos**     | 20%    | Admin configurado con fieldsets, readonly y permisos               |
| **Evidencias y formato de entrega** | 10%    | Capturas claras, nombres correctos, entrega ordenada               |

**Total:** 100 puntos

---

## 💡 Consejos Finales

1. Haz la actividad por bloques: primero organización, luego modelos, luego validaciones y al final admin.

2. Después de mover las apps, ejecuta `python manage.py check` antes de seguir. Ese paso puede ahorrarte mucho tiempo.

3. No intentes resolver todo de una sola vez. Haz un cambio, guarda, prueba y continúa.

4. Si aparece un error de importación, casi siempre significa que falta actualizar la ruta a `apps.empleados` o `apps.prestamos`.

5. Cuando algo falle en el admin, revisa primero imports, decoradores y nombres de campos.

6. Si tienes dudas, usa la terminal para validar con:

```bash
docker compose exec web python manage.py check
docker compose exec web python manage.py makemigrations
docker compose exec web python manage.py migrate
```

---

¡Éxito con tu actividad!
