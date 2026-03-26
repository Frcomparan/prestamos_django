# Sistema de Nombres Únicos para Fotos de Empleados

## Descripción

Se ha implementado un sistema automático para generar nombres únicos para los archivos de fotos, evitando conflictos y duplicados en el almacenamiento.

## ¿Por Qué es Importante?

### Problemas sin nombres únicos:

- ❌ Si dos empleados suben "foto.jpg", el segundo archivo sobrescribe el primero
- ❌ Si un empleado sube la misma foto dos veces, se pierde la primera
- ❌ Dificulta la búsqueda y gestión de archivos
- ❌ Causa pérdida de datos

### Solución implementada:

- ✅ Cada archivo recibe un nombre único automáticamente
- ✅ Los datos no se sobrescriben
- ✅ Fácil rastrear qué foto pertenece a quién
- ✅ Compatible con backups y migraciones

---

## Funcionamiento

### Método Actual: UUID + ID del Empleado

**Función:** `generar_nombre_foto_empleado()`

**Formato:** `empleados/fotos/{empleado_id}-{uuid}.{extension}`

**Ejemplos:**

```
empleados/fotos/1-a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6.jpg
empleados/fotos/2-b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6a1.png
empleados/fotos/3-c3d4e5f6g7h8i9j0k1l2m3n4o5p6a1b2.jpg
```

**Ventajas:**

- UUID garantiza unicidad global
- ID del empleado facilita búsquedas
- No requiere timestamp (más eficiente)
- Se pueden subir múltiples fotos del mismo empleado sin conflictos

---

## Opciones Alternativas

### Opción 1: UUID Puro

```python
upload_to = lambda instance, filename: f"empleados/fotos/{uuid.uuid4()}{os.path.splitext(filename)[1]}"
```

**Resultado:** `empleados/fotos/a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6.jpg`

**Ventajas:**

- Máxima privacidad (no se ve el ID del empleado)
- Totalmente único

**Desventajas:**

- No se sabe a quién pertenece sin consultar BD
- Más difícil de depurar

---

### Opción 2: Timestamp

**Función:** `generar_nombre_foto_con_timestamp()`

**Formato:** `empleados/fotos/{empleado_id}-{timestamp}.{extension}`

**Ejemplo:** `empleados/fotos/1-20250326101530.jpg`

**Ventajas:**

- Fácil de leer y ordenar cronológicamente
- Sabe cuándo se subió la foto

**Desventajas:**

- Si se suben dos fotos en el mismo segundo, hay conflicto
- Especialmente problemático en sistemas de alta carga

---

### Opción 3: Nombre Descriptivo

**Función:** `generar_nombre_foto_descriptivo()`

**Formato:** `empleados/fotos/{empleado_id}-{slug_nombre}-{uuid_corto}.{extension}`

**Ejemplos:**

```
empleados/fotos/1-juan-perez-a1b2c3d4.jpg
empleados/fotos/2-maria-garcia-e5f6g7h8.png
empleados/fotos/3-carlos-rodriguez-i9j0k1l2.jpg
```

**Ventajas:**

- Muy descriptivo (se ve el nombre del empleado)
- Fácil de entender a primera vista
- UUID corto mantiene unicidad

**Desventajas:**

- Más largo
- Si el nombre cambia, el archivo mantiene el antiguo nombre

---

## Cómo Cambiar el Método

Si deseas usar otro método, edita el campo `foto_perfil` en [apps/empleados/models.py](apps/empleados/models.py):

### Cambiar a Timestamp:

```python
class Empleado(models.Model):
    foto_perfil = models.ImageField(
        upload_to=generar_nombre_foto_con_timestamp,  # ← Cambiar esta línea
        blank=True,
        null=True,
        help_text='Foto de perfil o identificación del empleado'
    )
```

### Cambiar a Nombre Descriptivo:

```python
class Empleado(models.Model):
    foto_perfil = models.ImageField(
        upload_to=generar_nombre_foto_descriptivo,  # ← Cambiar esta línea
        blank=True,
        null=True,
        help_text='Foto de perfil o identificación del empleado'
    )
```

Luego generar migración:

```bash
docker-compose run --rm web python manage.py makemigrations empleados
docker-compose exec web python manage.py migrate
```

---

## Estructura del Archivo utils.py

El archivo [apps/empleados/utils.py](apps/empleados/utils.py) contiene **3 funciones**:

### 1. `generar_nombre_foto_empleado()` ⭐ (ACTUAL)

```python
def generar_nombre_foto_empleado(instance, filename):
    """Genera nombre con UUID"""
    ext = os.path.splitext(filename)[1].lower()
    nombre_unico = uuid.uuid4().hex
    nombre_archivo = f"{instance.id}-{nombre_unico}{ext}"
    return f"empleados/fotos/{nombre_archivo}"
```

### 2. `generar_nombre_foto_con_timestamp()`

```python
def generar_nombre_foto_con_timestamp(instance, filename):
    """Genera nombre con timestamp"""
    from datetime import datetime
    ext = os.path.splitext(filename)[1].lower()
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    nombre_archivo = f"{instance.id}-{timestamp}{ext}"
    return f"empleados/fotos/{nombre_archivo}"
```

### 3. `generar_nombre_foto_descriptivo()`

```python
def generar_nombre_foto_descriptivo(instance, filename):
    """Genera nombre descriptivo con nombre del empleado"""
    ext = os.path.splitext(filename)[1].lower()
    nombre_slug = slugify(instance.nombre)
    uuid_corto = uuid.uuid4().hex[:8]
    nombre_archivo = f"{instance.id}-{nombre_slug}-{uuid_corto}{ext}"
    return f"empleados/fotos/{nombre_archivo}"
```

---

## Ejemplo de Uso

### Subir una foto en el Admin Pan:

1. Ir a `http://localhost:8000/admin/empleados/empleado/`
2. Seleccionar empleado
3. En "Foto de perfil" seleccionar imagen
4. Hacer click en "Guardar"

**Lo que ocurre internamente:**

```
Usuario sube: "foto.jpg"
↓
Django ejecuta: generar_nombre_foto_empleado(empleado_instance, "foto.jpg")
↓
Se genera nombre único: "1-a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6.jpg"
↓
Se guarda en: /app/media/empleados/fotos/1-a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6.jpg
↓
Se accede desde: http://localhost:8000/media/empleados/fotos/1-a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6.jpg
```

---

## Acceder a la Foto

En plantillas:

```html
{% if empleado.foto_perfil %}
<img src="{{ empleado.foto_perfil.url }}" alt="{{ empleado.nombre }}" />
{% endif %}
```

En Python:

```python
empleado = Empleado.objects.get(id=1)
print(empleado.foto_perfil.name)      # empleados/fotos/1-a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6.jpg
print(empleado.foto_perfil.url)       # /media/empleados/fotos/1-a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6.jpg
print(empleado.foto_perfil.size)      # 234567 bytes
```

---

## Migraciones

La migración `0004_alter_empleado_foto_perfil` actualiza el campo para usar la nueva función:

```
[X] 0001_initial
[X] 0002_alter_empleado_nombre
[X] 0003_empleado_foto_perfil_alter_historialpuesto_empleado
[X] 0004_alter_empleado_foto_perfil
```

---

## Seguridad

- ✅ Los nombres no contienen caracteres especiales
- ✅ Los UUIDs son imposibles de adivinar
- ✅ No se exponen detalles sensibles en la URL (excepto ID)
- ✅ Los archivos se guardan fuera del directorio web

---

## Ventajas Finales

| Aspecto            | Antes         | Después                 |
| ------------------ | ------------- | ----------------------- |
| **Duplicados**     | ❌ Posibles   | ✅ Imposibles           |
| **Sobrescrituras** | ❌ Sí         | ✅ No                   |
| **Trazabilidad**   | ❌ Difícil    | ✅ Fácil (ID en nombre) |
| **Escalabilidad**  | ❌ Limitada   | ✅ Ilimitada            |
| **Backup**         | ❌ Complicado | ✅ Sencillo             |

---

## Comandos Útiles

```bash
# Ver fotos guardadas
docker-compose exec web ls -la /app/media/empleados/fotos/

# Listar con detalles
docker-compose exec web ls -lh /app/media/empleados/fotos/

# Contar cantidad de fotos
docker-compose exec web sh -c 'ls /app/media/empleados/fotos/ | wc -l'

# Ver información en BD
docker-compose exec web python manage.py shell
>>> from apps.empleados.models import Empleado
>>> emp = Empleado.objects.filter(foto_perfil__isnull=False)
>>> for e in emp:
...     print(f"{e.nombre}: {e.foto_perfil.name}")
```

---

## Solución de Problemas

### Problema: "Cambié el método pero las fotos viejas siguen con el nombre antiguo"

**Solución:** El cambio solo afecta fotos nuevas. Las viejas mantienen su nombre. Puedes:

1. Mantenerlas como están
2. Renombrarlas manualmente
3. Resubir las fotos con el nuevo método

### Problema: "No veo las fotos después de cambiar el método"

**Verificar:**

1. Que ejecutaste las migraciones: `docker-compose exec web python manage.py migrate`
2. Que el archivo [apps/empleados/utils.py](apps/empleados/utils.py) existe
3. Que importaste la función correctamente en models.py

---

## Próximas Mejoras

1. **Archivos múltiples por empleado**
   - Crear modelo `FotoEmpleado` con relación ManyToMany
   - Permitir foto principal + documentos

2. **Compresión automática**
   - Comprimir al guardar (libuljpeg, WebP)
   - Generar thumbnails

3. **Almacenamiento en nube**
   - Migrar a Azure Blob Storage
   - Usar boto3 para AWS S3

4. **Validación avanzada**
   - Detección de rostro
   - Validación de documentos
   - OCR para extraer datos

---

**Fecha de implementación:** 26 de marzo de 2026
**Estado:** ✅ Completado y funcional
