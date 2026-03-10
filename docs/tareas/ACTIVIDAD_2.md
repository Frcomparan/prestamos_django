# Actividad para Casa 2: Crear App de Préstamos

**Curso:** Taller de Django  
**Tipo:** Actividad individual  
**Tiempo estimado:** 30-45 minutos

---

## 🎯 Objetivo

Crear la aplicación de préstamos en Django, configurarla correctamente y desarrollar un modelo básico de Préstamo con sus campos principales.

---

## 📋 Prerrequisitos

Antes de iniciar, asegúrate de tener:

- ✅ Sesión 1 completada (Docker funcionando, proyecto creado)
- ✅ Actividad 1 completada (proyecto levantado correctamente)
- ✅ App `empleados` creada y funcionando
- ✅ Modelos `Puesto`, `Empleado` y `HistorialPuesto` creados y migrados
- ✅ Contenedores de Docker corriendo

**⚠️ Importante:** Esta actividad se basa en el trabajo realizado en clase.

---

## 📝 Instrucciones de la Actividad

### Paso 1: Crear la App de Préstamos

#### 1.1 Verificar que Docker está corriendo

Antes de crear la app, asegúrate de que tus contenedores estén activos:

```bash
docker compose ps
```

**✅ Verificación:** Deberías ver ambos servicios (`web` y `db`) con estado "Up".

Si no están corriendo, inícielos:

```bash
docker compose up -d
```

**Nota:** La bandera `-d` ejecuta los contenedores en segundo plano (detached mode).

#### 1.2 Crear la aplicación prestamos

Ejecuta el siguiente comando para crear la nueva app:

```bash
docker compose exec web python manage.py startapp prestamos
```

**¿Qué hace este comando?**

- `docker compose exec web`: Ejecuta un comando dentro del contenedor `web`
- `python manage.py startapp`: Comando de Django para crear una nueva aplicación
- `prestamos`: Nombre de la nueva aplicación

**✅ Verificación:** Se debe crear una nueva carpeta llamada `prestamos/` en tu proyecto.

#### 1.3 Verificar la estructura creada

Confirma que tienes esta nueva estructura:

```
sistema_prestamos/
├── config/
├── empleados/
├── prestamos/          ← NUEVA CARPETA
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py      ← Aquí trabajaremos
│   ├── tests.py
│   └── views.py
├── manage.py
├── requirements.txt
├── Dockerfile
└── docker-compose.yml
```

**Explicación de los archivos importantes:**

- `models.py` → Aquí definiremos el modelo Prestamo
- `admin.py` → Aquí registraremos el modelo en el admin (después)
- `apps.py` → Configuración de la app
- `views.py` → Para la lógica de vistas

---

### Paso 2: Registrar la App en Settings

Para que Django reconozca la nueva aplicación, debemos registrarla en la configuración del proyecto.

#### 2.1 Abrir el archivo de configuración

Abre el archivo: `config/settings.py`

#### 2.2 Localizar INSTALLED_APPS

Busca la sección `INSTALLED_APPS` (aproximadamente línea 33). Deberías ver algo así:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'empleados',  # ← Ya está registrada de la clase
]
```

#### 2.3 Agregar la app prestamos

Agrega `'prestamos'` al final de la lista:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'empleados',
    'prestamos',  # ← AGREGAR ESTA LÍNEA
]
```

**⚠️ Importante:**

- Respeta la indentación (4 espacios)
- Agrega la coma al final
- No olvides las comillas simples

#### 2.4 Guardar el archivo

Guarda los cambios en `config/settings.py`.

**✅ Verificación:** Django ahora reconoce la aplicación `prestamos`.

---

### Paso 3: Crear el Modelo Prestamo

Ahora crearemos un modelo básico de Préstamo con los campos esenciales.

#### 3.1 Abrir models.py

Abre el archivo: `prestamos/models.py`

Verás algo así:

```python
from django.db import models

# Create your models here.
```

#### 3.2 Importar el modelo Empleado

Antes de crear el modelo Prestamo, necesitamos importar `Empleado` para crear la relación. Agrega esta línea después de los imports existentes:

```python
from django.db import models
from empleados.models import Empleado  # ← AGREGAR ESTA LÍNEA

# Create your models here.
```

**Explicación:**

- `from empleados.models`: Importamos desde la app empleados
- `import Empleado`: Traemos el modelo Empleado que creamos en clase

#### 3.3 Crear el modelo Prestamo

Ahora crea el modelo completo. Reemplaza todo el contenido del archivo con:

```python
from django.db import models
from django.core.validators import MinValueValidator
from empleados.models import Empleado


class Prestamo(models.Model):
    """
    Modelo básico para representar un préstamo solicitado por un empleado.
    """

    # ¿QUIÉN solicita el préstamo?
    empleado = models.ForeignKey(
        Empleado,
        on_delete=models.PROTECT,
        related_name='prestamos',
        help_text="Empleado que solicita el préstamo"
    )

    # ¿CUÁNTO solicita?
    monto = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        help_text="Monto solicitado del préstamo"
    )

    # ¿CUÁNDO lo solicita?
    fecha_solicitud = models.DateField(
        help_text="Fecha en que se solicita el préstamo"
    )

    # Método para mostrar el préstamo como texto
    def __str__(self):
        return f"Préstamo de {self.empleado.nombre} - ${self.monto}"

    # Configuración adicional del modelo
    class Meta:
        verbose_name = "Préstamo"
        verbose_name_plural = "Préstamos"
        ordering = ['-fecha_solicitud']  # Ordenar por fecha más reciente primero
```

#### 3.4 Entender el código - Explicación campo por campo

**Campo 1: empleado (ForeignKey)**

```python
empleado = models.ForeignKey(
    Empleado,
    on_delete=models.PROTECT,
    related_name='prestamos',
    help_text="Empleado que solicita el préstamo"
)
```

- **`ForeignKey`**: Crea una relación hacia el modelo Empleado. Significa "este préstamo pertenece a un empleado"
- **`on_delete=models.PROTECT`**: Si intentas eliminar un empleado que tiene préstamos, Django NO lo permitirá. Es una protección de datos.
- **`related_name='prestamos'`**: Permite hacer `empleado.prestamos.all()` para obtener todos los préstamos de un empleado
- **`help_text`**: Texto de ayuda que se muestra en el admin

**Analogía:** Es como decir "este préstamo le pertenece a Juan". No puedes eliminar a Juan si tiene préstamos pendientes.

**Campo 2: monto (DecimalField)**

```python
monto = models.DecimalField(
    max_digits=12,
    decimal_places=2,
    validators=[MinValueValidator(0.01)],
    help_text="Monto solicitado del préstamo"
)
```

- **`DecimalField`**: Campo para números con decimales. Perfecto para dinero (más preciso que FloatField)
- **`max_digits=12`**: Máximo 12 dígitos en total (ejemplo: 999,999,999.99)
- **`decimal_places=2`**: Dos decimales (los centavos)
- **`MinValueValidator(0.01)`**: El monto mínimo debe ser $0.01 (no se permiten préstamos de $0 o negativos)

**Ejemplos válidos:**

- `1500.00` → $1,500.00
- `25000.50` → $25,000.50
- `100000.99` → $100,000.99

**Campo 3: fecha_solicitud (DateField)**

```python
fecha_solicitud = models.DateField(
    help_text="Fecha en que se solicita el préstamo"
)
```

- **`DateField`**: Campo para guardar solo fecha (sin hora)
- Formato: `YYYY-MM-DD` (ejemplo: 2024-03-10)
- Es obligatorio (no tiene `null=True`)

**Método **str\*\*\*\*

```python
def __str__(self):
    return f"Préstamo de {self.empleado.nombre} - ${self.monto}"
```

- Define cómo se muestra el objeto como texto
- Sin esto verías: `<Prestamo object (1)>`
- Con esto verás: `Préstamo de Juan Pérez - $25000.00`

**Clase Meta**

```python
class Meta:
    verbose_name = "Préstamo"
    verbose_name_plural = "Préstamos"
    ordering = ['-fecha_solicitud']
```

- **`verbose_name`**: Nombre singular en español
- **`verbose_name_plural`**: Nombre plural en español
- **`ordering`**: Orden por defecto (el `-` significa descendente, más recientes primero)

#### 3.5 Guardar el archivo

Guarda los cambios en `prestamos/models.py`.

---

## 📦 Entregables

Para comprobar que completaste la actividad correctamente, debes entregar:

### 1. Captura de pantalla del código del modelo

**Nombre del archivo:** `modelo_prestamo.png` o `modelo_prestamo.jpg`

**Debe mostrar:**

- El archivo `prestamos/models.py` abierto en tu editor
- El código completo del modelo Prestamo visible
- Los tres campos: empleado, monto, fecha_solicitud

### 2. Captura de pantalla del settings.py

**Nombre del archivo:** `settings_prestamos.png` o `settings_prestamos.jpg`

**Debe mostrar:**

- El archivo `config/settings.py` abierto
- La sección `INSTALLED_APPS`
- La línea `'prestamos',` agregada a la lista

## 📨 Forma de Entrega

**Fecha límite:** Jueves 12 de Marzo de 2026 a las 09:59 PM

**Medio de entrega:** Classroom

**Formato:**

- Crea una carpeta con tu nombre: `NoControl_Apellido_Nombre_A2`
- Incluye las 2 capturas de pantalla
- Comprime en formato ZIP
- Nombra el archivo: `NoControl_Apellido_Nombre_A2.zip`

**Ejemplo:**

```
19460000_Garcia_Juan_A2.zip
├── modelo_prestamo.png
├── settings_prestamos.png
```

---

## 🔧 Troubleshooting (Solución de Problemas)

### Problema 1: "No module named 'empleados'"

**Causa:** La app empleados no está registrada en `INSTALLED_APPS` o no existe.

**Solución:**

1. Verifica que `empleados` esté en `config/settings.py`:

```python
INSTALLED_APPS = [
    ...
    'empleados',  # ← Debe estar aquí
    'prestamos',
]
```

2. Si no existe la carpeta `empleados/`, significa que no completaste la Sesión 1. Consulta con tu instructor.

### Problema 2: "django.db.migrations.exceptions.InconsistentMigrationHistory"

**Causa:** Conflictos en el historial de migraciones.

**Solución:**

```bash
# Eliminar la base de datos y volverla a crear
docker compose down
docker volume rm sistema_prestamos_postgres_data
docker compose up -d

# Volver a aplicar todas las migraciones
docker compose exec web python manage.py migrate
```

**Nota:** Esto eliminará todos los datos. Solo úsalo en desarrollo.

### Problema 3: "ImportError: cannot import name 'Empleado'"

**Causa:** Error de sintaxis en el import o el modelo Empleado no existe.

**Solución:**

1. Verifica que el import sea correcto:

```python
from empleados.models import Empleado  # Correcto
```

2. Verifica que el modelo Empleado exista en `empleados/models.py`

3. Si no existe, significa que no completaste la Parte 4 de la Sesión 1.

### Problema 4: "makemigrations no detecta cambios"

**Causa:** El archivo `models.py` no se guardó o hay un error de sintaxis.

**Solución:**

1. Guarda el archivo `prestamos/models.py`
2. Verifica que no haya errores de sintaxis Python
3. Intenta de nuevo:

```bash
docker compose exec web python manage.py makemigrations prestamos
```

### Problema 5: Error de sintaxis en models.py

**Causa:** Falta una coma, paréntesis, o hay problemas de indentación.

**Solución:**

Revisa estos puntos comunes:

- ¿Todos los paréntesis están cerrados?
- ¿Las comas están en su lugar?
- ¿La indentación es consistente? (4 espacios por nivel)
- ¿Las comillas están balanceadas?

**Usa un linter o el editor para detectar errores de sintaxis.**

## 🎓 Recursos Adicionales

Si quieres profundizar:

- [Documentación de Modelos en Django](https://docs.djangoproject.com/es/5.0/topics/db/models/)
- [Tipos de Campos de Django](https://docs.djangoproject.com/es/5.0/ref/models/fields/)
- [Relaciones en Django (ForeignKey)](https://docs.djangoproject.com/es/5.0/topics/db/examples/many_to_one/)
- [Sistema de Migraciones](https://docs.djangoproject.com/es/5.0/topics/migrations/)

---

## 📊 Criterios de Evaluación

Tu actividad será evaluada con los siguientes criterios:

| Criterio                         | Puntos | Descripción                                                   |
| -------------------------------- | ------ | ------------------------------------------------------------- |
| **Código del modelo correcto**   | 45%    | Modelo Prestamo con los 3 campos solicitados                  |
| **Configuración de settings.py** | 45%    | App registrada correctamente en INSTALLED_APPS                |
| **Formato de entrega**           | 10%    | Archivos nombrados correctamente, entrega en ZIP, puntualidad |

**Total:** 100 puntos

---

## 💡 Consejos Finales

1. **Lee los mensajes de error:** Django es muy descriptivo. Los errores te dicen exactamente qué está mal.

2. **Verifica la ortografía:** Un error común es escribir mal el nombre de los campos o modelos.

3. **Usa la documentación:** Si tienes dudas, consulta la [documentación oficial de Django](https://docs.djangoproject.com/).

4. **Guarda los archivos:** Asegúrate de guardar todos los archivos antes de ejecutar comandos.

---

¡Éxito con tu actividad! 🚀
