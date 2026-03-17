# Actividad para Casa 5: Modulo 4 - Controladores y Plantillas (Empleados)

**Curso:** Taller de Django  
**Tipo:** Actividad individual  
**Tiempo estimado:** 75-100 minutos

---

## 🎯 Objetivo

Implementar y comprender el flujo completo del CRUD web de **Empleados** con 5 controladores basicos:

- Listado
- Detalle
- Creacion
- Actualizacion
- Eliminacion

Ademas, comprender el funcionamiento de las plantillas de Django en este proyecto:

- por que existe `base.html`
- para que sirven los componentes (`navbar`, `footer`)
- como una plantilla hija envia contenido a la plantilla base
- como Django mezcla Python + HTML mediante contexto, etiquetas y filtros

---

## 📋 Prerrequisitos

Antes de iniciar, asegurate de tener:

- ✅ Proyecto Django levantando con Docker
- ✅ App `apps.empleados` registrada en `INSTALLED_APPS`
- ✅ Migraciones aplicadas
- ✅ Registros de empleados en base de datos (al menos 2)
- ✅ Plantillas base ya disponibles en `templates/`

**Nota importante de esta actividad:**

- El HTML ya esta proporcionado.
- No es necesario "disenar" vistas HTML nuevas.
- Se busca **entender** como funciona lo que ya esta hecho.

---

## 🧠 Marco Conceptual Rapido

En Django (MTV), el flujo para esta actividad es:

```text
Navegador -> URL -> View -> Modelo -> Template -> HTML
```

Para este modulo, lo central es entender que:

1. La **URL** decide que vista ejecutar.
2. La **view** obtiene/guarda datos y arma un contexto.
3. La **template** renderiza HTML dinamico con ese contexto.

---

## 📝 Instrucciones de la Actividad

### Paso 1: Verificar que el entorno funciona

#### 1.1 Revisar contenedores

```bash
docker compose ps
```

**✅ Verificacion:** servicios `web` y `db` en estado `Up`.

Si no estan activos:

```bash
docker compose up -d
```

#### 1.2 Verificacion rapida de Django

```bash
docker compose exec web python manage.py check
```

**✅ Verificacion esperada:**

```text
System check identified no issues (0 silenced).
```

---

### Paso 2: Confirmar rutas de empleados (5 endpoints)

Abre y revisa el archivo de rutas de empleados.

Debe existir una configuracion equivalente a esta:

```python
from django.urls import path
from . import views

urlpatterns = [
    path("", views.empleado_list, name="empleado_list"),
    path("<int:pk>/", views.empleado_detail, name="empleado_detail"),
    path("nuevo/", views.empleado_create, name="empleado_create"),
    path("<int:pk>/editar/", views.empleado_update, name="empleado_update"),
    path("<int:pk>/eliminar/", views.empleado_delete, name="empleado_delete"),
]
```

#### 2.1 Explicacion de estas rutas

- `name="..."` es un alias para referenciar la URL desde templates con `{% url %}`.
- `<int:pk>` captura el id del empleado y lo envia como parametro a la view.
- Estas 5 rutas cubren todo el CRUD web solicitado.

---

### Paso 3: Implementar o validar los 5 controladores en `views.py`

Asegurate de tener los 5 controladores para empleados.

```python
from django.shortcuts import get_object_or_404, redirect, render
from .models import Empleado


def empleado_list(request):
    empleados = Empleado.objects.all().order_by("nombre")
    return render(request, "empleados/empleado_list.html", {"empleados": empleados})


def empleado_detail(request, pk):
    empleado = get_object_or_404(Empleado, pk=pk)
    historial = empleado.historial_puestos.all().order_by("-fecha_inicio")
    prestamos = empleado.prestamos.all().order_by("-fecha_solicitud")

    context = {
        "empleado": empleado,
        "historial": historial,
        "prestamos": prestamos,
    }
    return render(request, "empleados/empleado_detail.html", context)


def empleado_create(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre", "").strip()
        fecha_ingreso = request.POST.get("fecha_ingreso")
        activo = request.POST.get("activo", "").lower() in {"on", "true", "1", "si"}

        Empleado.objects.create(
            nombre=nombre,
            fecha_ingreso=fecha_ingreso,
            activo=activo,
        )
        return redirect("empleado_list")

    return render(request, "empleados/empleado_form.html")


def empleado_update(request, pk):
    empleado = get_object_or_404(Empleado, pk=pk)

    if request.method == "POST":
        empleado.nombre = request.POST.get("nombre", "").strip()
        empleado.fecha_ingreso = request.POST.get("fecha_ingreso")
        empleado.activo = request.POST.get("activo", "").lower() in {"on", "true", "1", "si"}
        empleado.save()
        return redirect("empleado_list")

    return render(request, "empleados/empleado_form.html", {"empleado": empleado})


def empleado_delete(request, pk):
    empleado = get_object_or_404(Empleado, pk=pk)

    if request.method == "POST":
        empleado.delete()
        return redirect("empleado_list")

    return render(request, "empleados/empleado_confirm_delete.html", {"empleado": empleado})
```

#### 3.1 Explicacion de cada controlador

- `empleado_list`: lectura de todos los empleados y envio a template.
- `empleado_detail`: lectura de 1 empleado + informacion relacionada.
- `empleado_create`: flujo `GET/POST` para crear.
- `empleado_update`: flujo `GET/POST` para editar.
- `empleado_delete`: confirmacion `GET` y eliminacion real con `POST`.

#### 3.2 Patron del flujo GET y POST

En los controladores se repite este patron:

- `GET` -> mostrar formulario o confirmacion
- `POST` -> ejecutar accion en base de datos y `redirect`

---

### Paso 4: Revisar la base de plantillas (sin reescribir HTML)

En este proyecto las plantillas ya estan hechas. En este paso se revisa **como esta organizada la arquitectura de templates**.

#### 4.1 Por que existe `base.html`

`base.html` centraliza:

- estructura HTML global (`<html>`, `<head>`, `<body>`)
- estilos comunes
- layout general de pagina

Ventajas:

1. Evita repetir codigo en cada vista.
2. Mantiene consistencia visual.
3. Permite cambios globales en un solo archivo.

#### 4.2 Para que sirven los componentes

En `base.html` se usan:

```django
{% include "components/navbar.html" %}
...
{% include "components/footer.html" %}
```

Esto permite reutilizar piezas UI independientes.

- `navbar.html`: navegacion principal
- `footer.html`: pie de pagina

Si cambias un componente, impacta todas las paginas que extienden de `base.html`.

#### 4.3 Como una plantilla hija "envia" contenido al base

Las plantillas de empleados usan:

```django
{% extends "base.html" %}

{% block title %}Empleados{% endblock %}

{% block content %}
    <!-- HTML especifico de la pantalla -->
{% endblock %}
```

Interpretacion:

- `extends`: hereda toda la estructura de `base.html`.
- `block title`: rellena el titulo de la pagina.
- `block content`: inyecta el contenido principal de cada pantalla.

#### 4.4 Que significa "Python sobre HTML" en Django templates

No es Python arbitrario, es el lenguaje de plantillas de Django:

- Variables: `{{ empleado.nombre }}`
- Etiquetas de control: `{% if %}`, `{% for %}`, `{% with %}`
- Filtros: `{{ fecha|date:'Y-m-d' }}`, `{{ monto|floatformat:2 }}`
- URLs reversas: `{% url 'empleado_update' empleado.id %}`
- Seguridad en formularios: `{% csrf_token %}`

Esto permite que el HTML sea dinamico sin escribir logica pesada dentro de la plantilla.

---

### Paso 5: Relacionar cada controlador con su plantilla

Usa esta tabla como referencia en tu evidencia:

| Controlador       | Template que renderiza                   | Funcion principal    |
| ----------------- | ---------------------------------------- | -------------------- |
| `empleado_list`   | `empleados/empleado_list.html`           | Listar registros     |
| `empleado_detail` | `empleados/empleado_detail.html`         | Mostrar detalle      |
| `empleado_create` | `empleados/empleado_form.html`           | Crear registro       |
| `empleado_update` | `empleados/empleado_form.html`           | Editar registro      |
| `empleado_delete` | `empleados/empleado_confirm_delete.html` | Confirmar y eliminar |

**Nota:** `create` y `update` reutilizan la misma plantilla de formulario.

---

### Paso 6: Prueba guiada de extremo a extremo

Levanta la aplicacion:

```bash
docker compose up -d
```

Abre en navegador:

- `http://localhost:8000/empleados/`

#### Ejecuta esta secuencia exacta

1. Listar empleados existentes.
2. Crear un empleado nuevo.
3. Abrir el detalle del empleado creado.
4. Editar su nombre o estado.
5. Eliminar el empleado.
6. Confirmar que ya no aparece en el listado.

---

## 📦 Entregables

Entrega en un archivo PDF o Markdown:

### 1. Evidencia tecnica (capturas)

- Captura de `apps/empleados/urls.py` con las 5 rutas.
- Captura de `apps/empleados/views.py` con las 5 vistas.

### 2. Evidencia funcional (navegador)

- Captura de listado.
- Captura de detalle.
- Captura de formulario de creacion o edicion.
- Captura de confirmacion de eliminacion.

---

## 📊 Criterios de Evaluación

| Criterio                            | Puntos | Descripción                                          |
| ----------------------------------- | ------ | ---------------------------------------------------- |
| **Evidencia tecnica**               | 45%    | Capturas de `urls.py` y `views.py`                   |
| **Evidencia funcional**             | 45%    | Capturas de las pantallas funcionales                |
| **Evidencias y formato de entrega** | 10%    | Capturas claras, nombres correctos, entrega ordenada |

**Total:** 100 puntos

---

## 🌟 Reto Extra (Opcional)

Si terminas antes, deja preparada la base del CRUD web de prestamos con los 5 controladores basicos (sin logica de negocio).

### Paso 1: Crear o revisar `apps/prestamos/urls.py`

Define las 5 rutas base para prestamos:

```python
from django.urls import path
from . import views

urlpatterns = [
    path("", views.prestamo_list, name="prestamo_list"),
    path("<int:pk>/", views.prestamo_detail, name="prestamo_detail"),
    path("nuevo/", views.prestamo_create, name="prestamo_create"),
    path("<int:pk>/editar/", views.prestamo_update, name="prestamo_update"),
    path("<int:pk>/eliminar/", views.prestamo_delete, name="prestamo_delete"),
]
```

**Explicacion:**

- Se replica el mismo patron que en empleados.
- Solo se define el enrutamiento; aun no se implementa la logica interna.

### Paso 2: Referenciar estas rutas en el archivo global

Abre `config/urls.py` y agrega la inclusion de la app de prestamos:

```python
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("empleados/", include("apps.empleados.urls")),
    path("prestamos/", include("apps.prestamos.urls")),
    ...
]
```

**Explicacion:**

- `config/urls.py` es el enrutador principal del proyecto.
- Con `include("apps.prestamos.urls")` activas todas las rutas definidas en la app.

### Paso 3: Dejar funciones base en `apps/prestamos/views.py`

Define las 5 funciones de controladores sin logica, solo con `pass`:

```python
def prestamo_list(request):
    pass


def prestamo_detail(request, pk):
    pass


def prestamo_create(request):
    pass


def prestamo_update(request, pk):
    pass


def prestamo_delete(request, pk):
    pass
```

**Explicacion:**

- Este reto solo deja la estructura preparada.
- En la siguiente actividad se puede completar la logica de cada controlador.

### Paso 4: Validar que el proyecto reconoce las rutas

Ejecuta:

```bash
docker compose exec web python manage.py check
```

Si no hay errores, la base del modulo de prestamos queda lista para continuar.

---

## 🛠️ Troubleshooting Rapido

### Problema 1: `TemplateDoesNotExist`

**Causa comun:** nombre/ruta incorrecta del template.

**Revision:**

- Verifica que la ruta en `render(...)` coincida exactamente.
- Verifica que los archivos esten dentro de `templates/empleados/`.

### Problema 2: Error 404 en detalle/editar/eliminar

**Causa comun:** ruta con `pk` faltante o mal formada.

**Revision:**

- URL esperada: `/empleados/3/`, `/empleados/3/editar/`, `/empleados/3/eliminar/`
- Revisar que el `path("<int:pk>/...")` exista en `urls.py`.

### Problema 3: Error CSRF al guardar

**Causa comun:** falta `{% csrf_token %}` dentro del `<form method="post">`.

### Problema 4: El boton de eliminar no hace nada

**Causa comun:** envio con `GET` en lugar de `POST`.

**Regla:** eliminar debe ejecutarse solo al confirmar con `POST`.

---
