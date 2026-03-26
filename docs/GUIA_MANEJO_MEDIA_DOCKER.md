# Guía: Manejo de Archivos (Media) en Django con Docker

## Descripción General

Este documento explica cómo se ha configurado el proyecto para manejar archivos (media) de forma persistente en un volumen Docker, permitiendo que los empleados puedan subir fotos de perfil e identificación con **garantía de unicidad y sin conflictos de nombres**.

### Características Principales

✅ **Almacenamiento persistente** - Volumen Docker que persiste entre contenedores  
✅ **Nombres únicos automáticos** - Sistema que previene archivos duplicados y sobrescrituras  
✅ **Fácil de usar** - Interfaz admin de Django integrada  
✅ **Escalable** - Soporta millones de archivos sin problemas  
✅ **Auditable** - ID del empleado incluido en el nombre de cada archivo

## Cambios Realizados

### 1. Modelo Empleado

Se agregó un nuevo campo `ImageField` al modelo `Empleado`:

```python
class Empleado(models.Model):
    nombre = models.CharField(max_length=200)
    fecha_ingreso = models.DateField()
    activo = models.BooleanField(default=True)
    foto_perfil = models.ImageField(
        upload_to='empleados/fotos/',
        blank=True,
        null=True,
        help_text='Foto de perfil o identificación del empleado'
    )
```

**Características:**

- `upload_to='empleados/fotos/'`: Los archivos se guardan en esta carpeta dentro del volumen media
- `blank=True`: El campo es opcional en formularios
- `null=True`: El campo puede estar vacío en la base de datos
- `help_text`: Ayuda descriptiva para los usuarios

### 2. Configuración en settings.py

Se agregaron las configuraciones necesarias para servir archivos media:

```python
# Media files (Fotos, documentos, etc.)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

- **MEDIA_URL**: URL pública para acceder a los archivos (ej: `/media/empleados/fotos/foto.jpg`)
- **MEDIA_ROOT**: Ruta física en el contenedor donde se guardan los archivos

### 3. URLs Configuradas

En `config/urls.py` se agregó soporte para servir archivos en modo desarrollo:

```python
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

Esto permite acceder a los archivos en desarrollo visitando URLs como:

- `http://localhost:8000/media/empleados/fotos/foto.jpg`

### 4. Volumen Docker Persistente

En `docker-compose.yml` se configuró un volumen para persistencia de datos:

```yaml
volumes:
  postgres_data:
  media_data:

services:
  web:
    volumes:
      - .:/app
      - media_data:/app/media # ← Nuevo volumen para archivos
```

**Ventajas:**

- Los archivos persisten aunque se elimine el contenedor
- Los cambios son visibles inmediatamente en el sistema de archivos host
- Facilita el backup y la migración de datos

### 5. Dependencias

Se agregó `Pillow` a `requirements.txt` para procesar imágenes:

```
Pillow==10.1.0
```

### 6. Sistema de Nombres Únicos

Se implementó un sistema automático para generar nombres únicos y evitar conflictos:

```python
# apps/empleados/utils.py
def generar_nombre_foto_empleado(instance, filename):
    """
    Genera un nombre único para cada foto
    Formato: empleados/fotos/{empleado_id}-{uuid}.{extension}
    Ejemplo: empleados/fotos/1-a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6.jpg
    """
    import os
    import uuid
    ext = os.path.splitext(filename)[1].lower()
    nombre_unico = uuid.uuid4().hex
    nombre_archivo = f"{instance.id}-{nombre_unico}{ext}"
    return f"empleados/fotos/{nombre_archivo}"
```

**Por qué es importante:**

- ✅ Evita archivos duplicados (cada foto tiene nombre único)
- ✅ Previene sobrescrituras accidentales
- ✅ Si dos empleados suben "foto.jpg", ambos se guardan correctamente
- ✅ Fácil rastrear qué foto pertenece a quién (ID en el nombre)
- ✅ Compatible con backups y migraciones de datos

El modelo Empleado usa esta función automáticamente:

```python
class Empleado(models.Model):
    foto_perfil = models.ImageField(
        upload_to=generar_nombre_foto_empleado,  # ← Función dinámica
        blank=True,
        null=True,
        help_text='Foto de perfil o identificación del empleado'
    )
```

### 7. Admin Interface

Se mejoró la interfaz de administración de Django para mostrar:

- Vista previa de la foto en el formulario
- Indicador visual de si el empleado tiene foto
- Campo exclusivo para subir la foto

```python
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'fecha_ingreso', 'activo', 'antiguedad_años', 'tiene_foto']
    readonly_fields = ['preview_foto']
    fields = ['nombre', 'fecha_ingreso', 'activo', 'foto_perfil', 'preview_foto']

    def tiene_foto(self, obj):
        return bool(obj.foto_perfil)
    tiene_foto.boolean = True

    def preview_foto(self, obj):
        if obj.foto_perfil:
            from django.utils.html import format_html
            return format_html(
                '<img src="{}" width="150" height="150" style="border-radius: 8px;" />',
                obj.foto_perfil.url
            )
        return 'Sin foto de perfil'
```

## Estructura de Archivos

```
/app/
├── media/                          # Volumen persistente de archivos
│   └── empleados/
│       └── fotos/
│           ├── foto_empleado_1.jpg
│           ├── foto_empleado_2.jpg
│           └── ...
├── apps/
│   └── empleados/
│       ├── models.py
│       ├── admin.py
│       └── uploads/                # No necesario - se usa /media
└── config/
    ├── settings.py
    └── urls.py
```

## Cómo Usar

### 1. Subir una Foto desde el Admin Panel

1. Ir a `http://localhost:8000/admin/empleados/empleado/`
2. Seleccionar o crear un empleado
3. En el campo "Foto de perfil", click en "Elegir archivo"
4. Seleccionar una imagen JPG o PNG
5. Click en "Guardar"

**Lo que ocurre internamente:**

- Usuario sube: `foto.jpg`
- Sistema ejecuta: `generar_nombre_foto_empleado()`
- Se genera nombre único: `1-a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6.jpg`
- Se guarda en: `/app/media/empleados/fotos/1-a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6.jpg`

### 2. Acceder a la Foto

Una vez subida, la foto estará disponible en:

```
http://localhost:8000/media/empleados/fotos/1-a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6.jpg
```

El nombre único garantiza que:

- ✅ Si otra persona sube también "foto.jpg", no se sobrescribe
- ✅ Ambas fotos se guardan con nombres diferentes
- ✅ Se puede identificar el archivo por el ID del empleado

### 3. Uso Programático

En plantillas Django (templates):

```html
{% if empleado.foto_perfil %}
<img src="{{ empleado.foto_perfil.url }}" alt="{{ empleado.nombre }}" />
{% else %}
<img src="/static/images/default-avatar.png" alt="Sin foto" />
{% endif %}
```

En vistas Python:

```python
from apps.empleados.models import Empleado

empleado = Empleado.objects.get(id=1)
if empleado.foto_perfil:
    foto_url = empleado.foto_perfil.url
    # Resultado: /media/empleados/fotos/1-a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6.jpg

    foto_nombre = empleado.foto_perfil.name
    # Resultado: empleados/fotos/1-a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6.jpg

    foto_path = empleado.foto_perfil.path
    # Resultado: /app/media/empleados/fotos/1-a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6.jpg
```

## Comandos Docker Útiles

### Iniciar servicios

```bash
docker-compose up -d
```

### Ver logs de la aplicación

```bash
docker-compose logs -f web
```

### Acceder a la shell de Django

```bash
docker-compose exec web python manage.py shell
```

### Hacer migraciones nuevas

```bash
docker-compose run --rm web python manage.py makemigrations
docker-compose exec web python manage.py migrate
```

### Listar volúmenes

```bash
docker volume ls
```

### Inspeccionar ubicación del volumen en el host

```bash
docker volume inspect aplicacion_prestamos_media_data
```

### Limpiar contenedores huérfanos

```bash
docker-compose down --remove-orphans
```

## Ventajas de esta Configuración

✅ **Persistencia**: Los archivos se mantienen aunque se reconstruya el contenedor  
✅ **Sin duplicados**: Sistema de nombres únicos impide conflictos  
✅ **Escalabilidad**: Fácil agregar más tipos de archivos (documentos, certificados, etc.)  
✅ **Desarrollo**: Se puede acceder a los archivos directamente desde el host  
✅ **Seguridad**: Los archivos no se versionan en git (se ignoran con .dockerignore)  
✅ **Backup**: El volumen puede respaldarse fácilmente  
✅ **Trazabilidad**: El ID del empleado está en el nombre del archivo

---

## Opciones de Nombres Únicos

Se implementaron **3 estrategias** diferentes para generar nombres. Actualmente se usa **UUID + ID** (recomendado), pero puedes cambiar si lo necesitas.

### Opción 1: UUID + ID (ACTUAL ⭐)

**Función:** `generar_nombre_foto_empleado()`

**Formato:** `empleados/fotos/{empleado_id}-{uuid}.{extension}`

**Ejemplo:** `empleados/fotos/1-a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6.jpg`

**Ventajas:**

- UUID garantiza unicidad global (implicar 0 duplicados)
- ID del empleado facilita búsquedas y auditoría
- No requiere timestamp (más eficiente)

```python
def generar_nombre_foto_empleado(instance, filename):
    import os, uuid
    ext = os.path.splitext(filename)[1].lower()
    nombre_unico = uuid.uuid4().hex
    return f"empleados/fotos/{instance.id}-{nombre_unico}{ext}"
```

### Opción 2: Timestamp

**Función:** `generar_nombre_foto_con_timestamp()`

**Formato:** `empleados/fotos/{empleado_id}-{timestamp}.{extension}`

**Ejemplo:** `empleados/fotos/1-20250326101530.jpg`

**Ventajas:**

- Fácil de leer y ordenar cronológicamente
- Sabe exactamente cuándo se subió cada foto

**Desventajas:**

- Si se suben dos fotos en el mismo segundo, hay conflicto (raro pero posible)

```python
def generar_nombre_foto_con_timestamp(instance, filename):
    from datetime import datetime
    import os
    ext = os.path.splitext(filename)[1].lower()
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"empleados/fotos/{instance.id}-{timestamp}{ext}"
```

### Opción 3: Nombre Descriptivo

**Función:** `generar_nombre_foto_descriptivo()`

**Formato:** `empleados/fotos/{empleado_id}-{slug_nombre}-{uuid_corto}.{extension}`

**Ejemplos:**

```
empleados/fotos/1-juan-perez-a1b2c3d4.jpg
empleados/fotos/2-maria-garcia-e5f6g7h8.png
```

**Ventajas:**

- Muy legible (se ve el nombre del empleado)
- Fácil de entender a primera vista

**Desventajas:**

- Más largo
- Si el nombre del empleado cambia, el archivo mantiene el antiguo nombre

```python
def generar_nombre_foto_descriptivo(instance, filename):
    from django.utils.text import slugify
    import os, uuid
    ext = os.path.splitext(filename)[1].lower()
    nombre_slug = slugify(instance.nombre)
    uuid_corto = uuid.uuid4().hex[:8]
    return f"empleados/fotos/{instance.id}-{nombre_slug}-{uuid_corto}{ext}"
```

---

## Cómo Cambiar el Sistema de Nombres

Si deseas usar otro método, edita `apps/empleados/models.py`:

### Cambiar a Timestamp:

```python
from .utils import generar_nombre_foto_con_timestamp

class Empleado(models.Model):
    foto_perfil = models.ImageField(
        upload_to=generar_nombre_foto_con_timestamp,  # ← Cambiar esta línea
        blank=True,
        null=True
    )
```

### Cambiar a Nombre Descriptivo:

```python
from .utils import generar_nombre_foto_descriptivo

class Empleado(models.Model):
    foto_perfil = models.ImageField(
        upload_to=generar_nombre_foto_descriptivo,  # ← Cambiar esta línea
        blank=True,
        null=True
    )
```

Luego crear la migración:

```bash
docker-compose run --rm web python manage.py makemigrations
docker-compose exec web python manage.py migrate
```

**Nota:** El cambio solo afecta fotos nuevas. Las fotos antiguas mantienen su nombre anterior.

---

## Ventajas de esta Configuración

## Impacto de los Nombres Únicos

### Problema sin Nombres Únicos

Sin este sistema, podrían ocurrir problemas críticos:

| Escenario                                | Sin Nombres Únicos                   | Con Nombres Únicos                      |
| ---------------------------------------- | ------------------------------------ | --------------------------------------- |
| Dos empleados suben "foto.jpg"           | ❌ La segunda sobrescribe la primera | ✅ Ambas se guardan correctamente       |
| Un empleado sube la misma foto dos veces | ❌ Se pierden datos                  | ✅ Ambas fotos se conservan             |
| Auditoría de cambios                     | ❌ No se puede rastrear              | ✅ Fácil con ID en el nombre            |
| Migración de servidores                  | ❌ Archivos se pierden o mezclan     | ✅ Nombres únicos garantizan integridad |
| Backup y restauración                    | ❌ Complejo                          | ✅ Sencillo y seguro                    |

### Ejemplo Real de Problema Evitado

**Sin nombres únicos:**

```
Empleado 1 (Juan) sube: foto.jpg → /media/empleados/fotos/foto.jpg
Empleado 2 (María) sube: foto.jpg → /media/empleados/fotos/foto.jpg [SOBRESCRIBE!]
Resultado: Se pierde la foto de Juan ❌
```

**Con nombres únicos:**

```
Empleado 1 (Juan) sube: foto.jpg → /media/empleados/fotos/1-a1b2c3d4.jpg
Empleado 2 (María) sube: foto.jpg → /media/empleados/fotos/2-e5f6g7h8.jpg
Resultado: Ambas fotos se conservan ✅
```

---

## Próximas Mejoras Sugeridas

1. **Validación de archivos**: Limitar tipos y tamaños de imagen

   ```python
   def validate_image(image):
       if image.size > 5 * 1024 * 1024:  # 5MB
           raise ValidationError("La imagen no puede superar 5MB")
   ```

2. **Thumbnail automático**: Generar miniaturas para optimizar carga

   ```python
   from sorl.thumbnail import ImageField
   ```

3. **Almacenamiento en nube**: Cambiar a S3 o Blob Storage en producción

   ```python
   if not DEBUG:
       DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
   ```

4. **Procesamiento de imágenes**: Usar Celery para procesar imágenes async

   ```python
   @task
   def procesar_foto_empleado(empleado_id):
       # Redimensionar, comprimir, etc.
   ```

5. **Múltiples fotos por empleado**: Crear modelo para almacenar varias fotos
   ```python
   class FotoEmpleado(models.Model):
       empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
       imagen = models.ImageField(upload_to=generar_nombre_foto_empleado)
       descripcion = models.CharField(max_length=100)
       es_principal = models.BooleanField(default=False)
   ```

## Solución de Problemas

### "ImageField because Pillow is not installed"

**Solución**: Reconstruir la imagen Docker

```bash
docker-compose build --no-cache
```

### Los archivos no persisten después de eliminar contenedores

**Verificar**: Que el volumen esté en docker-compose.yml y en los servicios

### No puedo ver la imagen subida

**Verificar**:

1. Que DEBUG=True en settings.py
2. Que el archivo existe en `docker volume inspect aplicacion_prestamos_media_data`
3. Que la URL es correcta (con nombre único): `/media/empleados/fotos/1-a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6.jpg`

### Cambié el sistema de nombres pero las fotos viejas siguen con el nombre antiguo

**Explicación:** Es normal. El cambio solo afecta fotos nuevas. Las viejas mantienen su nombre anterior.

**Opciones:**

1. Mantenerlas como están (compatibles sin problemas)
2. Renombrarlas manualmente
3. Resubir las fotos con el nuevo método

### No veo la foto después de cambiar el método de nombres

**Verificar:**

1. Que ejecutaste las migraciones: `docker-compose exec web python manage.py migrate`
2. Que el archivo `apps/empleados/utils.py` existe
3. Que importaste la función correctamente en `models.py`

### Dos empleados subieron la misma foto.jpg (sin el sistema de nombres únicos hubiera habido problema)

**Con nombres únicos:** Se guardan correctamente con nombres diferentes

- Empleado 1: `/media/empleados/fotos/1-a1b2c3d4.jpg`
- Empleado 2: `/media/empleados/fotos/2-e5f6g7h8.jpg`

**Beneficio:** Sin este sistema, la segunda foto hubiera sobrescrito la primera ✅

---

## Comandos Útiles para Inspeccionar Archivos

### Ver todas las fotos guardadas

```bash
docker-compose exec web ls -lah /app/media/empleados/fotos/
```

### Contar archivos guardados

```bash
docker-compose exec web sh -c 'ls /app/media/empleados/fotos/ | wc -l'
```

### Ver información de fotos en la BD

```bash
docker-compose exec web python manage.py shell
>>> from apps.empleados.models import Empleado
>>> empleados = Empleado.objects.filter(foto_perfil__isnull=False)
>>> for emp in empleados:
...     print(f"{emp.nombre}: {emp.foto_perfil.name}")
```

---

## Referencias

- [Django File Storage](https://docs.djangoproject.com/en/5.0/topics/files/)
- [ImageField Documentation](https://docs.djangoproject.com/en/5.0/ref/models/fields/#imagefield)
- [Docker Volumes](https://docs.docker.com/storage/volumes/)
- [Pillow Documentation](https://pillow.readthedocs.io/)
- [Django UUID Documentation](https://docs.python.org/3/library/uuid.html)
