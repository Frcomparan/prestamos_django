# Actividad para Casa 3: Configurar Django Admin Completo

**Curso:** Taller de Django  
**Tipo:** Actividad individual  
**Tiempo estimado:** 45-60 minutos

---

## 🎯 Objetivo

Configurar completamente la interfaz de administración de Django para los modelos de empleados (Puesto, Empleado, HistorialPuesto), personalizando vistas, agregando funcionalidades de búsqueda y filtrado, y creando datos de prueba.

---

## 📋 Prerrequisitos

Antes de iniciar, asegúrate de tener:

- ✅ Sesión 1 completada (Parte 4 - Modelos creados)
- ✅ Modelos `Puesto`, `Empleado` y `HistorialPuesto` creados y migrados
- ✅ Contenedores de Docker corriendo
- ✅ Superusuario creado (si no lo tienes, lo crearemos en esta actividad)

**⚠️ Importante:** Esta actividad requiere que hayas completado la creación de los 3 modelos de empleados en clase.

---

## 🎓 ¿Qué es Django Admin?

Antes de iniciar, es importante entender qué es el Django Admin y por qué es tan poderoso.

### Concepto Básico

Django Admin es una **interfaz de administración automática** que Django genera basándose en tus modelos. Es como tener un panel de control completo para tu base de datos sin escribir una sola línea de HTML.

### Capacidades del Admin

El Django Admin incluye automáticamente:

1. **CRUD Completo**: Create (Crear), Read (Leer), Update (Actualizar), Delete (Eliminar)
2. **Búsqueda**: Buscar registros por campos específicos
3. **Filtros**: Filtrar datos por categorías, fechas, etc.
4. **Ordenamiento**: Ordenar columnas con un clic
5. **Paginación**: Manejo automático de grandes cantidades de datos
6. **Validación**: Verifica que los datos cumplan las reglas antes de guardar
7. **Relaciones**: Maneja ForeignKeys con dropdowns automáticos
8. **Permisos**: Control de quién puede ver/editar/eliminar datos
9. **Historial**: Registro de cambios realizados
10. **Interfaz responsive**: Funciona en escritorio, tablet y móvil

### Valor Real

Lo que normalmente tomaría **semanas programar desde cero**, Django lo genera en **minutos**. Esto es una de las razones por las que Django es tan popular en la industria.

---

## 📝 Instrucciones de la Actividad

### Paso 1: Verificar Entorno y Crear Superusuario

#### 1.1 Verificar que Docker está corriendo

```bash
docker compose ps
```

**✅ Verificación:** Ambos servicios (`web` y `db`) deben estar "Up".

Si no están corriendo:

```bash
docker compose up -d
```

#### 1.2 Verificar si ya tienes un superusuario

Si ya creaste un superusuario en clase, **puedes saltarte al Paso 2**.

Para verificar, intenta acceder a: **http://localhost:8000/admin**

- Si ves una pantalla de login → Ya tienes superusuario ✅
- Si ves un error → Necesitas crear uno

#### 1.3 Crear superusuario (si es necesario)

Si no tienes superusuario, créalo con:

```bash
docker compose exec web python manage.py createsuperuser
```

**El sistema te pedirá:**

```
Username: admin
Email address: admin@ejemplo.com
Password: admin123
Password (again): admin123
```

**⚠️ Notas importantes:**

- El username y password son sensibles a mayúsculas
- Anota tus credenciales, las necesitarás constantemente
- En desarrollo puedes usar contraseñas simples, en producción NUNCA

**✅ Verificación:** Deberías ver el mensaje:

```
Superuser created successfully.
```

#### 1.4 Verificar acceso al admin

1. Abre tu navegador
2. Ve a: **http://localhost:8000/admin**
3. Ingresa con tus credenciales
4. Deberías ver el panel de administración de Django

**Por ahora verás solo:**

- **AUTHENTICATION AND AUTHORIZATION**
  - Grupos
  - Usuarios

---

### Paso 2: Configurar Admin de Puesto

Ahora vamos a registrar y personalizar el modelo Puesto en el admin.

#### 2.1 Abrir el archivo admin.py

Abre el archivo: `empleados/admin.py`

Verás algo así:

```python
from django.contrib import admin

# Register your models here.
```

#### 2.2 Importar los modelos

Primero, importa todos los modelos que vamos a registrar:

```python
from django.contrib import admin
from .models import Puesto, Empleado, HistorialPuesto
```

**Explicación:**

- `from django.contrib import admin`: Importa las herramientas del admin
- `from .models import ...`: Importa nuestros modelos (el `.` significa "del mismo paquete")

#### 2.3 Registrar Puesto con configuración básica

Agrega esta configuración para el modelo Puesto:

```python
@admin.register(Puesto)
class PuestoAdmin(admin.ModelAdmin):
    # Columnas que se mostrarán en la lista
    list_display = ['nombre', 'sueldo']

    # Campos por los que se puede buscar
    search_fields = ['nombre']

    # Ordenar por sueldo descendente (más alto primero)
    ordering = ['-sueldo']

    # Número de registros por página
    list_per_page = 20
```

**Explicación línea por línea:**

1. **`@admin.register(Puesto)`**
   - Es un "decorador" que registra automáticamente el modelo
   - Alternativa moderna a `admin.site.register(Puesto, PuestoAdmin)`

2. **`class PuestoAdmin(admin.ModelAdmin)`**
   - Clase que configura cómo se ve Puesto en el admin
   - Hereda de `ModelAdmin` que tiene toda la funcionalidad base

3. **`list_display = ['nombre', 'sueldo']`**
   - Define qué columnas se muestran en la tabla
   - Sin esto, solo verías el resultado de `__str__()`
   - Puedes agregar métodos personalizados aquí también

4. **`search_fields = ['nombre']`**
   - Agrega una caja de búsqueda arriba de la tabla
   - Busca en el campo `nombre` del modelo
   - Puedes agregar múltiples campos: `['nombre', 'otro_campo']`

5. **`ordering = ['-sueldo']`**
   - Define el orden por defecto
   - El `-` significa descendente (de mayor a menor)
   - Sin `-` sería ascendente (de menor a mayor)

6. **`list_per_page = 20`**
   - Cuántos registros mostrar por página
   - Por defecto son 100
   - Útil cuando tienes muchos datos

#### 2.4 Guardar y verificar

1. Guarda el archivo `empleados/admin.py`
2. Ve a: **http://localhost:8000/admin**
3. Refresca la página (F5)
4. Deberías ver una nueva sección: **EMPLEADOS** → **Puestos**

---

### Paso 3: Configurar Admin de Empleado

Ahora vamos a configurar un admin más avanzado para Empleado.

#### 3.1 Agregar configuración de Empleado

En el mismo archivo `empleados/admin.py`, **después** de la clase `PuestoAdmin`, agrega:

```python
@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    # Columnas que se mostrarán en la lista
    list_display = ['nombre', 'fecha_ingreso', 'activo', 'antiguedad_años']

    # Campos por los que se puede buscar
    search_fields = ['nombre']

    # Filtros en la barra lateral
    list_filter = ['activo', 'fecha_ingreso']

    # Campos de solo lectura (no se pueden editar)
    readonly_fields = ['fecha_ingreso']

    # Ordenar por fecha de ingreso más reciente primero
    ordering = ['-fecha_ingreso']

    # Registros por página
    list_per_page = 25

    # Método personalizado para mostrar antigüedad
    @admin.display(description='Antigüedad (años)')
    def antiguedad_años(self, obj):
        """Calcula los años de antigüedad del empleado"""
        from datetime import date
        if obj.fecha_ingreso:
            dias = (date.today() - obj.fecha_ingreso).days
            años = dias / 365
            return f"{años:.1f} años"
        return "N/A"
```

**Explicación de las nuevas opciones:**

1. **`list_display` con método personalizado**
   - Incluye `'antiguedad_años'` que es un método que definimos abajo
   - Permite mostrar datos calculados, no solo campos del modelo

2. **`list_filter = ['activo', 'fecha_ingreso']`**
   - Agrega filtros en la barra lateral derecha
   - `activo`: Filtra por Sí/No
   - `fecha_ingreso`: Filtra por año (Django lo detecta automáticamente)

3. **`readonly_fields = ['fecha_ingreso']`**
   - Estos campos se muestran pero NO se pueden editar
   - Útil para campos que no deben cambiar después de crearse

4. **Método `antiguedad_años(self, obj)`**
   - Método personalizado que calcula la antigüedad
   - `obj` es el objeto Empleado actual
   - Retorna una cadena de texto formateada

5. **`@admin.display(description='...')`**
   - Decorador que define cómo se muestra el método
   - `description`: El título de la columna en la tabla

#### 3.2 Guardar y verificar

1. Guarda el archivo
2. Refresca **http://localhost:8000/admin**
3. Haz clic en **Empleados**
4. Deberías ver:
   - Columnas: Nombre, Fecha ingreso, Activo, Antigüedad
   - Barra de búsqueda arriba
   - Filtros a la derecha

---

### Paso 4: Configurar Admin de HistorialPuesto

Este es el más complejo porque tiene relaciones con otros modelos.

#### 4.1 Agregar configuración de HistorialPuesto

En `empleados/admin.py`, **después** de `EmpleadoAdmin`, agrega:

```python
@admin.register(HistorialPuesto)
class HistorialPuestoAdmin(admin.ModelAdmin):
    # Columnas que se mostrarán en la lista
    list_display = ['empleado', 'puesto', 'fecha_inicio', 'fecha_fin', 'esta_activo']

    # Campos por los que se puede buscar
    # Nota: Para buscar en relaciones, usa __ (doble guión bajo)
    search_fields = ['empleado__nombre', 'puesto__nombre']

    # Filtros en la barra lateral
    list_filter = ['puesto', 'fecha_inicio']

    # Organizar el formulario en secciones
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

    # Ordenar por fecha de inicio más reciente
    ordering = ['-fecha_inicio']

    # Registros por página
    list_per_page = 30

    # Método personalizado para mostrar si está activo
    @admin.display(boolean=True, description='¿Activo?')
    def esta_activo(self, obj):
        """Indica si este es el puesto actual del empleado"""
        return obj.fecha_fin is None
```

**Explicación de las nuevas opciones:**

1. **`search_fields` con relaciones**

   ```python
   search_fields = ['empleado__nombre', 'puesto__nombre']
   ```

   - `empleado__nombre`: Busca en el campo `nombre` del modelo `Empleado` relacionado
   - El `__` (doble guión bajo) atraviesa la relación ForeignKey
   - Permite buscar "Juan" y encontrar todos sus historiales

2. **`fieldsets`**
   - Organiza el formulario de edición en secciones
   - Hace más legible el formulario cuando hay muchos campos
   - Cada sección tiene:
     - Título: `'Información del Empleado'`
     - Campos: `'fields': ('empleado',)`
     - Descripción opcional: `'description': '...'`

3. **Método `esta_activo(self, obj)`**
   - Retorna `True` o `False`
   - Con `@admin.display(boolean=True)`, Django muestra ✅ o ❌
   - Mucho más visual que ver "True" o "False"

#### 4.2 Código completo de admin.py

Tu archivo `empleados/admin.py` debe verse así:

```python
from django.contrib import admin
from .models import Puesto, Empleado, HistorialPuesto


@admin.register(Puesto)
class PuestoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'sueldo']
    search_fields = ['nombre']
    ordering = ['-sueldo']
    list_per_page = 20


@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'fecha_ingreso', 'activo', 'antiguedad_años']
    search_fields = ['nombre']
    list_filter = ['activo', 'fecha_ingreso']
    readonly_fields = ['fecha_ingreso']
    ordering = ['-fecha_ingreso']
    list_per_page = 25

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
```

#### 4.3 Guardar y verificar

1. Guarda el archivo
2. Refresca **http://localhost:8000/admin**
3. Deberías ver ahora 3 secciones bajo **EMPLEADOS**:
   - Empleados
   - Historiales de puestos
   - Puestos

---

### Paso 5: Crear Datos de Prueba

Ahora vamos a crear datos de prueba para verificar que todo funciona.

#### 5.1 Crear Puestos

1. Ve a **http://localhost:8000/admin**
2. Haz clic en **Puestos** → **Agregar Puesto**
3. Crea los siguientes puestos:

| Nombre              | Sueldo   |
| ------------------- | -------- |
| ANALISTA JR         | 12000.00 |
| PROGRAMADOR JR      | 16000.00 |
| PROGRAMADOR SENIOR  | 40000.00 |
| LÍDER TÉCNICO       | 55000.00 |
| GERENTE DE PROYECTO | 70000.00 |

**Cómo crear cada uno:**

- Escribe el nombre en MAYÚSCULAS
- Escribe el sueldo sin comas ni símbolos (solo el número)
- Haz clic en "GUARDAR Y CREAR OTRO" para crear el siguiente
- En el último, haz clic en "GUARDAR"

#### 5.2 Crear Empleados

1. Haz clic en **Empleados** → **Agregar Empleado**
2. Crea los siguientes empleados:

| Nombre              | Fecha Ingreso | Activo |
| ------------------- | ------------- | ------ |
| Juan Pérez García   | 2020-01-15    | ✅ Sí  |
| María López Ruiz    | 2021-06-10    | ✅ Sí  |
| Carlos Sánchez Díaz | 2019-03-22    | ✅ Sí  |
| Ana Martínez Torres | 2022-09-01    | ✅ Sí  |
| Pedro González Luna | 2018-11-05    | ❌ No  |

**Notas:**

- La fecha debe ser en formato: YYYY-MM-DD (2020-01-15)
- El checkbox "Activo" debe estar marcado o desmarcado según la tabla
- El campo "Activo" indica si el empleado sigue trabajando en la empresa

#### 5.3 Crear Historiales de Puesto

Ahora vamos a asignar puestos a los empleados. Crearemos algunos con historial completo.

1. Haz clic en **Historiales de puestos** → **Agregar Historial de puesto**

**Histórico de Juan Pérez García:**

| Empleado          | Puesto             | Fecha Inicio | Fecha Fin  |
| ----------------- | ------------------ | ------------ | ---------- |
| Juan Pérez García | PROGRAMADOR JR     | 2020-01-15   | 2022-06-30 |
| Juan Pérez García | PROGRAMADOR SENIOR | 2022-07-01   | (vacío)    |

**Histórico de María López Ruiz:**

| Empleado         | Puesto         | Fecha Inicio | Fecha Fin  |
| ---------------- | -------------- | ------------ | ---------- |
| María López Ruiz | ANALISTA JR    | 2021-06-10   | 2023-01-31 |
| María López Ruiz | PROGRAMADOR JR | 2023-02-01   | (vacío)    |

**Histórico de Carlos Sánchez Díaz:**

| Empleado            | Puesto         | Fecha Inicio | Fecha Fin  |
| ------------------- | -------------- | ------------ | ---------- |
| Carlos Sánchez Díaz | PROGRAMADOR JR | 2019-03-22   | 2021-08-15 |
| Carlos Sánchez Díaz | LÍDER TÉCNICO  | 2021-08-16   | (vacío)    |

**Histórico de Ana Martínez Torres:**

| Empleado            | Puesto      | Fecha Inicio | Fecha Fin |
| ------------------- | ----------- | ------------ | --------- |
| Ana Martínez Torres | ANALISTA JR | 2022-09-01   | (vacío)   |

**Histórico de Pedro González Luna (inactivo):**

| Empleado            | Puesto              | Fecha Inicio | Fecha Fin  |
| ------------------- | ------------------- | ------------ | ---------- |
| Pedro González Luna | GERENTE DE PROYECTO | 2018-11-05   | 2024-12-31 |

**Cómo llenar el formulario:**

- **Empleado**: Selecciona del dropdown
- **Puesto**: Selecciona del dropdown
- **Fecha inicio**: Formato YYYY-MM-DD
- **Fecha fin**: Déjala vacía si es el puesto actual, o ponle una fecha si ya terminó

---

### Paso 6: Explorar las Funcionalidades del Admin

Ahora que tienes datos, explora las capacidades del admin.

#### 6.1 Probar la búsqueda

1. Ve a **Empleados**
2. En la caja de búsqueda, escribe "Juan"
3. Presiona Enter
4. Deberías ver solo a Juan Pérez García

#### 6.2 Probar los filtros

1. En **Empleados**, mira la barra lateral derecha
2. Haz clic en "No" bajo "ACTIVO"
3. Deberías ver solo a Pedro González Luna
4. Haz clic en "Todos" para ver todos de nuevo
5. Prueba filtrar por "FECHA INGRESO" (elige un año)

#### 6.3 Probar el ordenamiento

1. Ve a **Puestos**
2. Los puestos deben estar ordenados por sueldo (mayor primero)
3. GERENTE DE PROYECTO debe aparecer primero

#### 6.4 Probar los fieldsets

1. Ve a **Historiales de puestos**
2. Haz clic en cualquier registro para editarlo
3. Observa cómo el formulario está organizado en secciones:
   - Información del Empleado
   - Información del Puesto
   - Fechas (con descripción)

#### 6.5 Probar el indicador visual

1. En la lista de **Historiales de puestos**
2. Observa la columna "¿Activo?"
3. Los registros sin fecha_fin muestran ✅ (check verde)
4. Los registros con fecha_fin muestran ❌ (X roja)

#### 6.6 Verificar columnas calculadas

1. Ve a **Empleados**
2. Observa la columna "Antigüedad (años)"
3. Debería mostrar valores como "4.2 años", "2.7 años", etc.
4. Este valor se calcula automáticamente en tiempo real

---

## 📦 Entregables

Para comprobar que completaste la actividad correctamente, debes entregar:

### 1. Captura del código admin.py completo

**Nombre del archivo:** `admin_codigo.png` o `admin_codigo.jpg`

**Debe mostrar:**

- El archivo `empleados/admin.py` abierto en tu editor
- Las 3 clases Admin completas: PuestoAdmin, EmpleadoAdmin, HistorialPuestoAdmin
- El código debe ser legible

### 2. Captura del panel principal del admin

**Nombre del archivo:** `admin_panel.png` o `admin_panel.jpg`

**Debe mostrar:**

- La página principal de **http://localhost:8000/admin**
- La sección "EMPLEADOS" con sus 3 modelos:
  - Empleados
  - Historiales de puestos
  - Puestos

### 3. Captura de la lista de Empleados

**Nombre del archivo:** `admin_empleados_lista.png` o `admin_empleados_lista.jpg`

**Debe mostrar:**

- La vista de lista de Empleados
- Las 4 columnas: Nombre, Fecha ingreso, Activo, Antigüedad (años)
- Al menos 3 empleados visibles
- La barra de búsqueda arriba
- Los filtros a la derecha (Activo, Fecha ingreso)

### 4. Captura de la lista de Historiales

**Nombre del archivo:** `admin_historiales_lista.png` o `admin_historiales_lista.jpg`

**Debe mostrar:**

- La vista de lista de Historiales de puestos
- Las columnas incluyendo la de "¿Activo?" con ✅ y ❌
- Al menos 4 registros visibles

### 5. Captura del formulario con fieldsets

**Nombre del archivo:** `admin_fieldsets.png` o `admin_fieldsets.jpg`

**Debe mostrar:**

- El formulario de edición/creación de un Historial de puesto
- Las 3 secciones claramente visibles:
  - Información del Empleado
  - Información del Puesto
  - Fechas (con su descripción)

### 6. Captura de búsqueda funcionando

**Nombre del archivo:** `admin_busqueda.png` o `admin_busqueda.jpg`

**Debe mostrar:**

- Una búsqueda realizada (por ejemplo, "Juan" o "María")
- El término de búsqueda visible en la caja de búsqueda
- Los resultados filtrados mostrando solo coincidencias

---

## 📨 Forma de Entrega

**Fecha límite:** Viernes 03 de Marzo de 2026 a las 09:59 PM

**Medio de entrega:** Classroom

**Formato:**

- Crea una carpeta: `NoControl_Apellido_Nombre_A3`
- Incluye las 6 capturas de pantalla
- Comprime en formato ZIP
- Nombra el archivo: `NoControl_Apellido_Nombre_A3.zip`

**Ejemplo:**

```
19460000_Garcia_Juan_A3.zip
├── admin_codigo.png
├── admin_panel.png
├── admin_empleados_lista.png
├── admin_historiales_lista.png
├── admin_fieldsets.png
└── admin_busqueda.png
```

---

## 🔧 Troubleshooting (Solución de Problemas)

### Problema 1: "No veo la sección EMPLEADOS en el admin"

**Causa:** Los modelos no están registrados o hay un error de sintaxis en admin.py.

**Solución:**

1. Verifica que guardaste el archivo `empleados/admin.py`
2. Revisa que no haya errores de sintaxis
3. Reinicia el servidor:
   ```bash
   docker compose restart web
   ```
4. Refresca el navegador

### Problema 2: Error "NameError: name 'Puesto' is not defined"

**Causa:** No importaste los modelos correctamente.

**Solución:**

Verifica que la primera línea después de `from django.contrib import admin` sea:

```python
from .models import Puesto, Empleado, HistorialPuesto
```

### Problema 3: La columna "Antigüedad" no se muestra

**Causa:** Error en el método `antiguedad_años` o falta el decorador.

**Solución:**

1. Verifica que el método esté dentro de la clase `EmpleadoAdmin`
2. Verifica la indentación (debe estar al mismo nivel que `list_display`)
3. Verifica que tenga el decorador `@admin.display(description='...')`

### Problema 4: Los fieldsets no se muestran en HistorialPuesto

**Causa:** Error de sintaxis en la definición de fieldsets.

**Solución:**

Verifica que la sintaxis sea exactamente:

```python
fieldsets = (
    ('Título', {
        'fields': ('campo1', 'campo2')
    }),
)
```

Nota: Son paréntesis externos `( )` y llaves internas `{ }`.

### Problema 5: "OperationalError: no such table"

**Causa:** Las migraciones no se han aplicado.

**Solución:**

```bash
docker compose exec web python manage.py migrate
```

### Problema 6: No puedo buscar por nombre del empleado en Historiales

**Causa:** Error en la sintaxis de `search_fields` con relaciones.

**Solución:**

Verifica que use doble guión bajo `__`:

```python
search_fields = ['empleado__nombre', 'puesto__nombre']
```

**NO** uses un solo guión bajo `_`.

### Problema 7: Los íconos ✅ ❌ no aparecen en "¿Activo?"

**Causa:** Falta el parámetro `boolean=True` en el decorador.

**Solución:**

```python
@admin.display(boolean=True, description='¿Activo?')
def esta_activo(self, obj):
    return obj.fecha_fin is None
```

---

## 🎓 Conceptos Clave Aprendidos

Al completar esta actividad, habrás aprendido:

✅ **Registrar modelos** en Django Admin con `@admin.register()`  
✅ **Personalizar vistas de lista** con `list_display`  
✅ **Agregar búsqueda** con `search_fields`  
✅ **Agregar filtros** con `list_filter`  
✅ **Buscar en relaciones** usando `__` (doble guión bajo)  
✅ **Crear métodos personalizados** para mostrar datos calculados  
✅ **Organizar formularios** con `fieldsets`  
✅ **Usar decoradores** como `@admin.display()`  
✅ **Indicadores booleanos** con íconos ✅ ❌  
✅ **Campos de solo lectura** con `readonly_fields`  
✅ **Controlar ordenamiento** y paginación

---

## 📚 Capacidades Adicionales del Admin (Para explorar)

Estas no son parte de la actividad, pero puedes explorarlas por tu cuenta:

### 1. Actions (Acciones masivas)

Permite realizar acciones en múltiples registros:

```python
@admin.action(description='Marcar empleados como inactivos')
def marcar_inactivos(modeladmin, request, queryset):
    queryset.update(activo=False)

class EmpleadoAdmin(admin.ModelAdmin):
    actions = [marcar_inactivos]
```

### 2. Inlines (Modelos relacionados inline)

Muestra historiales dentro del formulario del empleado:

```python
class HistorialPuestoInline(admin.TabularInline):
    model = HistorialPuesto
    extra = 1

class EmpleadoAdmin(admin.ModelAdmin):
    inlines = [HistorialPuestoInline]
```

### 3. list_editable

Permite editar campos directamente desde la lista:

```python
class PuestoAdmin(admin.ModelAdmin):
    list_editable = ['sueldo']
```

### 4. date_hierarchy

Agrega navegación por fechas:

```python
class EmpleadoAdmin(admin.ModelAdmin):
    date_hierarchy = 'fecha_ingreso'
```

### 5. Personalizar URLs del admin

```python
class EmpleadoAdmin(admin.ModelAdmin):
    def get_urls(self):
        # Agregar URLs personalizadas
        pass
```

---

## 📖 Recursos Adicionales

Si quieres profundizar:

- [Django Admin Site - Documentación Oficial](https://docs.djangoproject.com/es/5.0/ref/contrib/admin/)
- [ModelAdmin Options](https://docs.djangoproject.com/es/5.0/ref/contrib/admin/#modeladmin-options)
- [Admin Actions](https://docs.djangoproject.com/es/5.0/ref/contrib/admin/actions/)
- [Customizing the Admin](https://docs.djangoproject.com/es/5.0/intro/tutorial07/)

---

## 📊 Criterios de Evaluación

Tu actividad será evaluada con los siguientes criterios:

| Criterio                           | Puntos | Descripción                                        |
| ---------------------------------- | ------ | -------------------------------------------------- |
| **Código admin.py completo**       | 25%    | 3 clases Admin correctamente configuradas          |
| **Datos de prueba creados**        | 15%    | Al menos 5 puestos, 5 empleados, 8 historiales     |
| **Funcionalidades visibles**       | 25%    | Búsqueda, filtros, ordenamiento funcionando        |
| **Métodos personalizados**         | 15%    | Antigüedad y está_activo mostrándose correctamente |
| **Fieldsets configurados**         | 10%    | Formulario organizado en secciones                 |
| **Capturas de pantalla completas** | 10%    | 6 capturas mostrando todas las funcionalidades     |

**Total:** 100 puntos

---

## 💡 Consejos Finales

1. **Prueba cada configuración:** Después de agregar cada clase Admin, refresca el navegador para ver los cambios.

2. **Lee los mensajes de error:** Django Admin muestra errores muy descriptivos en rojo.

3. **Explora por tu cuenta:** El admin tiene muchas más capacidades. ¡Experimenta!

4. **Documenta tus datos:** Anota los nombres de empleados que creas para usarlos en las búsquedas.

5. **Guarda frecuentemente:** No pierdas tu trabajo, guarda el archivo después de cada cambio importante.

6. **Usa nombres descriptivos:** En los métodos personalizados, usa nombres claros como `antiguedad_años` en lugar de `calc1`.

7. **Formatea tu código:** Mantén la indentación consistente (4 espacios por nivel).

---

## 🌟 Reto Extra (Opcional - No suma puntos)

Si terminas antes y quieres un desafío adicional:

### Reto 1: Agregar un método que muestre el sueldo actual

En `EmpleadoAdmin`, agrega un método que muestre el sueldo del puesto actual del empleado.

**Pista:**

```python
@admin.display(description='Sueldo Actual')
def sueldo_actual(self, obj):
    historial_actual = HistorialPuesto.objects.filter(
        empleado=obj,
        fecha_fin__isnull=True
    ).first()
    if historial_actual:
        return f"${historial_actual.puesto.sueldo:,.2f}"
    return "Sin puesto activo"
```

### Reto 2: Personalizar los colores del admin

Investiga cómo cambiar los colores del tema del admin de Django.

### Reto 3: Agregar validación personalizada

En `HistorialPuestoAdmin`, agrega validación para que no se pueda crear un historial con fecha_inicio posterior a fecha_fin.

---

¡Éxito con tu actividad! 🚀
