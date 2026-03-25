# Sesión 3: Frontend - Templates, Vistas y Reportes

**Duración estimada:** 3-4 horas  
**Nivel:** Intermedio  
**Prerequisito:** Sesiones 1 y 2 completadas

## 🎯 Objetivos de la Sesión

Al finalizar esta sesión, podrás:

- ✅ Crear vistas con el sistema de templates de Django
- ✅ Implementar formularios para solicitar préstamos
- ✅ Mostrar listas de empleados y préstamos
- ✅ Generar reportes con detalles de pagos
- ✅ Aplicar estilos básicos con Bootstrap

---

## 📚 Parte 0: Vistas y Controladores

Las **vistas (views)** son funciones Python que conectan los **modelos** (datos) con los **templates** (HTML).

### Concepto: CRUD Operations

CRUD = Create, Read, Update, Delete

```python
# Ejemplo de operación READ
def empleado_list(request):
    empleados = Empleado.objects.all()
    return render(request, 'empleados/lista.html', {'empleados': empleados})
```

**Flujo:**

1. Usuario entra a `/empleados/`
2. Django llama a `empleado_list(request)`
3. Vista obtiene todos los empleados
4. Vista renderiza `lista.html` pasando los empleados
5. El usuario ve la lista en el navegador

### Las 5 Operaciones Básicas

#### 1. READ - Listar todos

```python
def empleado_list(request):
    empleados = Empleado.objects.all().order_by('nombre')
    return render(request, 'empleados/lista.html', {'empleados': empleados})
```

#### 2. READ - Ver detalle

```python
def empleado_detail(request, pk):
    empleado = get_object_or_404(Empleado, pk=pk)
    historial = empleado.historial_puestos.all()
    prestamos = empleado.prestamos.all()

    context = {
        'empleado': empleado,
        'historial': historial,
        'prestamos': prestamos,
    }
    return render(request, 'empleados/detalle.html', context)
```

**Nota:** `get_object_or_404` lanza error 404 si no existe en lugar de retornar None.

#### 3. CREATE - Crear nuevo

```python
def empleado_create(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        fecha_ingreso = request.POST.get('fecha_ingreso')
        activo = request.POST.get('activo') == 'on'

        Empleado.objects.create(
            nombre=nombre,
            fecha_ingreso=fecha_ingreso,
            activo=activo,
        )
        return redirect('empleados:lista')

    return render(request, 'empleados/formulario.html')
```

**GET** = Mostrar formulario vacío  
**POST** = Procesar datos y crear

#### 4. UPDATE - Editar

```python
def empleado_update(request, pk):
    empleado = get_object_or_404(Empleado, pk=pk)

    if request.method == 'POST':
        empleado.nombre = request.POST.get('nombre')
        empleado.fecha_ingreso = request.POST.get('fecha_ingreso')
        empleado.activo = request.POST.get('activo') == 'on'
        empleado.save()
        return redirect('empleados:lista')

    # GET: mostrar formulario precompletado
    return render(request, 'empleados/formulario.html', {'empleado': empleado})
```

#### 5. DELETE - Eliminar

```python
def empleado_delete(request, pk):
    empleado = get_object_or_404(Empleado, pk=pk)

    if request.method == 'POST':
        empleado.delete()
        return redirect('empleados:lista')

    # GET: pedir confirmación
    return render(request, 'empleados/confirmar_delete.html', {'empleado': empleado})
```

### Configurar URLs

Crea `empleados/urls.py`:

```python
from django.urls import path
from . import views

app_name = 'empleados'

urlpatterns = [
    path('', views.empleado_list, name='lista'),
    path('<int:pk>/', views.empleado_detail, name='detalle'),
    path('nuevo/', views.empleado_create, name='crear'),
    path('<int:pk>/editar/', views.empleado_update, name='actualizar'),
    path('<int:pk>/eliminar/', views.empleado_delete, name='eliminar'),
]
```

En `config/urls.py`:

```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('empleados/', include('empleados.urls')),
    path('prestamos/', include('prestamos.urls')),
]
```

### Usar {% url %} en Templates

En lugar de escribir URLs manualmente:

```django
<!-- ❌ MAL - Hardcodeado -->
<a href="/empleados/{{ empleado.id }}/">Ver</a>

<!-- ✅ BIEN - Dinámico -->
<a href="{% url 'empleados:detalle' empleado.id %}">Ver</a>
```

Si cambias la URL en `urls.py`, automáticamente se actualiza en todos los templates.

### Validación con full_clean()

Para validaciones del modelo en la vista:

```python
def empleado_create(request):
    if request.method == 'POST':
        try:
            empleado = Empleado(
                nombre=request.POST.get('nombre'),
                fecha_ingreso=request.POST.get('fecha_ingreso'),
                activo=request.POST.get('activo') == 'on'
            )
            empleado.full_clean()  # Ejecuta todas las validaciones
            empleado.save()
            return redirect('empleados:lista')

        except ValidationError as e:
            context = {'errores': e.messages}
            return render(request, 'empleados/formulario.html', context)

    return render(request, 'empleados/formulario.html')
```

En el template:

```django
{% if errores %}
    <div class="alert alert-danger">
        <ul>
        {% for error in errores %}
            <li>{{ error }}</li>
        {% endfor %}
        </ul>
    </div>
{% endif %}
```

---

## 📚 Parte 1: Introducción a Templates

### ¿Qué es el Frontend?

**Frontend** = La parte visual que ve el usuario  
**Backend** = La lógica y datos (que ya hicimos)

**Analogía:**

- **Backend** = Motor del carro
- **Frontend** = Interior, tablero, volante (lo que el conductor ve y usa)

### Sistema de Templates de Django

Django usa el patrón **MTV:**

- **M**odel = Datos (✅ ya lo hicimos)
- **T**emplate = HTML (lo que vamos a hacer)
- **V**iew = Controlador que conecta Model y Template

### Paso 1: Estructura de Carpetas

Crea estas carpetas:

```bash
empleados/
    templates/
        empleados/
            lista.html
            detalle.html
prestamos/
    templates/
        prestamos/
            lista.html
            solicitar.html
            detalle.html
            reporte.html
        base.html
```

**¿Por qué doble carpeta?** (ej: `templates/empleados/`)  
Django busca templates en todas las apps. Si dos apps tienen `lista.html`, habría conflicto. Por eso usamos subcarpetas.

### Paso 2: Template Base

Crea `prestamos/templates/base.html`:

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{% block title %}Sistema de Préstamos{% endblock %}</title>

    <!-- Bootstrap CSS -->
    <link
      href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css"
      rel="stylesheet"
    />

    {% block extra_css %}{% endblock %}
  </head>
  <body>
    <!-- Navbar -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
      <div class="container-fluid">
        <a class="navbar-brand" href="/">Sistema de Préstamos</a>
        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarNav"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav">
            <li class="nav-item">
              <a class="nav-link" href="{% url 'empleados:lista' %}"
                >Empleados</a
              >
            </li>
            <li class="nav-item">
              <a class="nav-link" href="{% url 'prestamos:lista' %}"
                >Préstamos</a
              >
            </li>
            <li class="nav-item">
              <a class="nav-link" href="{% url 'prestamos:solicitar' %}"
                >Solicitar Préstamo</a
              >
            </li>
            <li class="nav-item">
              <a class="nav-link" href="/admin/">Admin</a>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <!-- Contenido -->
    <div class="container mt-4">
      {% if messages %} {% for message in messages %}
      <div
        class="alert alert-{{ message.tags }} alert-dismissible fade show"
        role="alert"
      >
        {{ message }}
        <button
          type="button"
          class="btn-close"
          data-bs-dismiss="alert"
        ></button>
      </div>
      {% endfor %} {% endif %} {% block content %} {% endblock %}
    </div>

    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    {% block extra_js %}{% endblock %}
  </body>
</html>
```

**Conceptos nuevos:**

#### {% block %}

```django
{% block title %}Sistema de Préstamos{% endblock %}
```

- Define una sección que otros templates pueden sobrescribir
- Como un "espacio en blanco" que otros llenan

#### {% url %}

```django
<a href="{% url 'empleados:lista' %}">Empleados</a>
```

- Genera URLs dinámicamente
- Si cambias la URL, no hay que actualizar todos los templates

#### {% if %} y {% for %}

```django
{% if messages %}
    {% for message in messages %}
        ...
    {% endfor %}
{% endif %}
```

- Condicionales y loops igual que en Python
- Pero con sintaxis de template

### Paso 3: Template de Lista de Empleados

Crea `empleados/templates/empleados/lista.html`:

```html
{% extends 'base.html' %} {% block title %}Empleados - {{ block.super }}{%
endblock %} {% block content %}
<div class="row">
  <div class="col-12">
    <h1>Lista de Empleados</h1>
    <hr />

    {% if empleados %}
    <table class="table table-striped table-hover">
      <thead class="table-dark">
        <tr>
          <th>ID</th>
          <th>Nombre</th>
          <th>Fecha Ingreso</th>
          <th>Antigüedad</th>
          <th>Puesto Actual</th>
          <th>Estado</th>
          <th>Acciones</th>
        </tr>
      </thead>
      <tbody>
        {% for empleado in empleados %}
        <tr>
          <td>{{ empleado.id }}</td>
          <td>{{ empleado.nombre }}</td>
          <td>{{ empleado.fecha_ingreso|date:"d/m/Y" }}</td>
          <td>{{ empleado.calcular_antiguedad|floatformat:1 }} años</td>
          <td>
            {% if empleado.obtener_puesto_actual %} {{
            empleado.obtener_puesto_actual.nombre }} {% else %}
            <span class="text-muted">Sin puesto</span>
            {% endif %}
          </td>
          <td>
            {% if empleado.activo %}
            <span class="badge bg-success">Activo</span>
            {% else %}
            <span class="badge bg-secondary">Inactivo</span>
            {% endif %}
          </td>
          <td>
            <a
              href="{% url 'empleados:detalle' empleado.id %}"
              class="btn btn-sm btn-info"
              >Ver</a
            >
          </td>
        </tr>
        {% endfor %}
      </tbody>
    </table>
    {% else %}
    <div class="alert alert-warning">No hay empleados registrados.</div>
    {% endif %}
  </div>
</div>
{% endblock %}
```

**Conceptos nuevos:**

#### {% extends %}

```django
{% extends 'base.html' %}
```

- Hereda de otro template
- Usa la estructura de `base.html` y llena los `blocks`

#### {{ variable }}

```django
{{ empleado.nombre }}
```

- Imprime el valor de una variable
- Equivalente a `print()` en Python

#### Filtros |

```django
{{ empleado.fecha_ingreso|date:"d/m/Y" }}
```

- Transforma el valor antes de mostrarlo
- `date` formatea fechas
- `floatformat:1` redondea a 1 decimal

#### {{ block.super }}

```django
{% block title %}Empleados - {{ block.super }}{% endblock %}
```

- Incluye el contenido del bloque padre
- Resultado: "Empleados - Sistema de Préstamos"

---

## 🎨 Parte 2: Vistas (Views)

Las **vistas** conectan el backend con los templates.

### Paso 1: Lista de Empleados

Edita `empleados/views.py`:

```python
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Empleado

class EmpleadoListView(ListView):
    model = Empleado
    template_name = 'empleados/lista.html'
    context_object_name = 'empleados'

    def get_queryset(self):
        """Personalizar la consulta."""
        return Empleado.objects.filter(activo=True).order_by('nombre')

class EmpleadoDetailView(DetailView):
    model = Empleado
    template_name = 'empleados/detalle.html'
    context_object_name = 'empleado'
```

**Explicación:**

#### ListView

- Vista genérica para mostrar listas
- `model` = qué modelo mostrar
- `template_name` = qué template usar
- `context_object_name` = nombre de la variable en el template

#### get_queryset()

- Personaliza qué registros mostrar
- Aquí: solo activos, ordenados por nombre

### Paso 2: Detalle de Empleado

Crea `empleados/templates/empleados/detalle.html`:

```html
{% extends 'base.html' %} {% block title %}{{ empleado.nombre }} - {{
block.super }}{% endblock %} {% block content %}
<div class="row">
  <div class="col-md-8">
    <h1>{{ empleado.nombre }}</h1>
    <hr />

    <div class="card">
      <div class="card-body">
        <h5 class="card-title">Información General</h5>
        <table class="table">
          <tr>
            <th>Fecha de Ingreso:</th>
            <td>{{ empleado.fecha_ingreso|date:"d/m/Y" }}</td>
          </tr>
          <tr>
            <th>Antigüedad:</th>
            <td>{{ empleado.calcular_antiguedad|floatformat:1 }} años</td>
          </tr>
          <tr>
            <th>Estado:</th>
            <td>
              {% if empleado.activo %}
              <span class="badge bg-success">Activo</span>
              {% else %}
              <span class="badge bg-secondary">Inactivo</span>
              {% endif %}
            </td>
          </tr>
          <tr>
            <th>Puesto Actual:</th>
            <td>
              {% with puesto=empleado.obtener_puesto_actual %} {% if puesto %}
              {{ puesto.nombre }} - ${{ puesto.sueldo|floatformat:2 }} {% else
              %}
              <span class="text-muted">Sin puesto asignado</span>
              {% endif %} {% endwith %}
            </td>
          </tr>
        </table>
      </div>
    </div>

    <!-- Historial de Puestos -->
    <div class="card mt-3">
      <div class="card-body">
        <h5 class="card-title">Historial de Puestos</h5>
        <table class="table table-sm">
          <thead>
            <tr>
              <th>Puesto</th>
              <th>Fecha Inicio</th>
              <th>Fecha Fin</th>
            </tr>
          </thead>
          <tbody>
            {% for historial in empleado.historial_puestos.all %}
            <tr>
              <td>{{ historial.puesto.nombre }}</td>
              <td>{{ historial.fecha_inicio|date:"d/m/Y" }}</td>
              <td>
                {% if historial.fecha_fin %} {{ historial.fecha_fin|date:"d/m/Y"
                }} {% else %}
                <span class="badge bg-success">Actual</span>
                {% endif %}
              </td>
            </tr>
            {% empty %}
            <tr>
              <td colspan="3" class="text-center text-muted">Sin historial</td>
            </tr>
            {% endfor %}
          </tbody>
        </table>
      </div>
    </div>

    <!-- Préstamos -->
    <div class="card mt-3">
      <div class="card-body">
        <h5 class="card-title">Préstamos</h5>
        {% if empleado.prestamos.exists %}
        <table class="table table-sm">
          <thead>
            <tr>
              <th>ID</th>
              <th>Monto</th>
              <th>Estado</th>
              <th>Saldo</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            {% for prestamo in empleado.prestamos.all %}
            <tr>
              <td>{{ prestamo.id }}</td>
              <td>${{ prestamo.monto|floatformat:2 }}</td>
              <td>
                <span
                  class="badge bg-{% if prestamo.estado == 'ACTIVO' %}primary{% elif prestamo.estado == 'CONCLUIDO' %}success{% else %}secondary{% endif %}"
                >
                  {{ prestamo.get_estado_display }}
                </span>
              </td>
              <td>${{ prestamo.saldo_actual|floatformat:2 }}</td>
              <td>
                <a
                  href="{% url 'prestamos:detalle' prestamo.id %}"
                  class="btn btn-sm btn-info"
                  >Ver</a
                >
              </td>
            </tr>
            {% endfor %}
          </tbody>
        </table>
        {% else %}
        <p class="text-muted">Sin préstamos</p>
        {% endif %}
      </div>
    </div>
  </div>

  <div class="col-md-4">
    <div class="card">
      <div class="card-body">
        <h5 class="card-title">Acciones</h5>
        <a
          href="{% url 'prestamos:solicitar' %}?empleado={{ empleado.id }}"
          class="btn btn-primary w-100 mb-2"
        >
          Solicitar Préstamo
        </a>
        <a href="{% url 'empleados:lista' %}" class="btn btn-secondary w-100">
          Volver a Lista
        </a>
      </div>
    </div>

    {% with puede, mensaje = empleado.puede_solicitar_prestamo %}
    <div class="card mt-3">
      <div class="card-body">
        <h5 class="card-title">Estado de Elegibilidad</h5>
        {% if puede %}
        <div class="alert alert-success">✅ Puede solicitar préstamo</div>
        {% else %}
        <div class="alert alert-warning">⚠️ {{ mensaje }}</div>
        {% endif %}
      </div>
    </div>
    {% endwith %}
  </div>
</div>
{% endblock %}
```

**Conceptos nuevos:**

#### {% with %}

```django
{% with puesto=empleado.obtener_puesto_actual %}
    {{ puesto.nombre }}
{% endwith %}
```

- Crea una variable temporal
- Útil para no repetir código

#### {% empty %}

```django
{% for item in lista %}
    {{ item }}
{% empty %}
    <p>Lista vacía</p>
{% endfor %}
```

- Se ejecuta si el loop no tiene elementos

### Paso 3: Configurar URLs

Crea `empleados/urls.py`:

```python
from django.urls import path
from .views import EmpleadoListView, EmpleadoDetailView

app_name = 'empleados'

urlpatterns = [
    path('', EmpleadoListView.as_view(), name='lista'),
    path('<int:pk>/', EmpleadoDetailView.as_view(), name='detalle'),
]
```

Edita `config/urls.py`:

```python
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('empleados.urls')),  # API (ya existía)
    path('api/', include('prestamos.urls')),  # API (ya existía)
    path('empleados/', include('empleados.urls')),  # ← Nuevo
    path('prestamos/', include('prestamos.urls')),  # ← Agregaremos esto después
    path('', RedirectView.as_view(url='/empleados/')),  # Redirigir raíz
]
```

✅ **Checkpoint:** Abre `http://localhost:8000/empleados/` y verás la lista de empleados.

---

## 📝 Parte 3: Formularios

### Paso 1: Formulario para Solicitar Préstamo

Crea `prestamos/forms.py`:

```python
from django import forms
from django.core.exceptions import ValidationError
from .models import Prestamo
from empleados.models import Empleado

class PrestamoSolicitudForm(forms.ModelForm):
    """
    Formulario para solicitar un préstamo.
    """

    class Meta:
        model = Prestamo
        fields = ['empleado', 'monto', 'plazo_meses']
        widgets = {
            'empleado': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'monto': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 20000',
                'step': '0.01',
                'min': '0.01'
            }),
            'plazo_meses': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Máximo 24 meses',
                'min': '1',
                'max': '24'
            }),
        }
        labels = {
            'empleado': 'Empleado Solicitante',
            'monto': 'Monto Solicitado ($)',
            'plazo_meses': 'Plazo (meses)',
        }
        help_texts = {
            'monto': 'Máximo 6 meses de sueldo',
            'plazo_meses': 'Entre 1 y 24 meses',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Solo mostrar empleados activos
        self.fields['empleado'].queryset = Empleado.objects.filter(activo=True)

    def clean(self):
        """
        Validaciones personalizadas del formulario.
        """
        cleaned_data = super().clean()
        empleado = cleaned_data.get('empleado')
        monto = cleaned_data.get('monto')

        if empleado and monto:
            # Crear objeto temporal para validar
            prestamo_temp = Prestamo(
                empleado=empleado,
                monto=monto,
                plazo_meses=cleaned_data.get('plazo_meses', 1)
            )

            # Verificar elegibilidad
            puede, mensaje = prestamo_temp.puede_solicitar_prestamo()
            if not puede:
                raise ValidationError(mensaje)

        return cleaned_data
```

**Conceptos:**

#### ModelForm

- Crea un formulario automáticamente desde un modelo
- Ya sabe qué campos y tipos de datos usar

#### widgets

- Controlan cómo se ve el campo en HTML
- `attrs` agrega clases CSS y atributos HTML

#### clean()

- Validaciones personalizadas
- Se ejecuta cuando se envía el formulario

### Paso 2: Vista para Solicitar Préstamo

Edita `prestamos/views.py`:

```python
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
from django.contrib import messages
from django.urls import reverse_lazy
from .models import Prestamo, Abono
from .forms import PrestamoSolicitudForm

class PrestamoListView(ListView):
    model = Prestamo
    template_name = 'prestamos/lista.html'
    context_object_name = 'prestamos'
    paginate_by = 10

    def get_queryset(self):
        return Prestamo.objects.select_related('empleado').order_by('-fecha_solicitud')

class PrestamoCreateView(CreateView):
    model = Prestamo
    form_class = PrestamoSolicitudForm
    template_name = 'prestamos/solicitar.html'
    success_url = reverse_lazy('prestamos:lista')

    def form_valid(self, form):
        """Se ejecuta cuando el formulario es válido."""
        response = super().form_valid(form)
        messages.success(
            self.request,
            f'Préstamo solicitado exitosamente. ID: {self.object.id}'
        )
        return response

    def form_invalid(self, form):
        """Se ejecuta cuando hay errores."""
        messages.error(
            self.request,
            'Hay errores en el formulario. Por favor revisa los campos.'
        )
        return super().form_invalid(form)

class PrestamoDetailView(DetailView):
    model = Prestamo
    template_name = 'prestamos/detalle.html'
    context_object_name = 'prestamo'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['abonos'] = self.object.abonos.all()
        return context
```

**Conceptos:**

#### CreateView

- Vista genérica para crear objetos
- Maneja GET (mostrar formulario) y POST (guardar)

#### form_valid()

- Se ejecuta si el formulario es válido
- Aquí agregamos el mensaje de éxito

#### messages

- Sistema de mensajes de Django
- Muestra notificaciones al usuario

### Paso 3: Template para Solicitar

Crea `prestamos/templates/prestamos/solicitar.html`:

```html
{% extends 'base.html' %} {% block title %}Solicitar Préstamo - {{ block.super
}}{% endblock %} {% block content %}
<div class="row justify-content-center">
  <div class="col-md-8">
    <div class="card">
      <div class="card-header bg-primary text-white">
        <h4 class="mb-0">Solicitar Préstamo</h4>
      </div>
      <div class="card-body">
        <form method="post" novalidate>
          {% csrf_token %}

          <!-- Errores generales del formulario -->
          {% if form.non_field_errors %}
          <div class="alert alert-danger">{{ form.non_field_errors }}</div>
          {% endif %}

          <!-- Campo: Empleado -->
          <div class="mb-3">
            <label for="{{ form.empleado.id_for_label }}" class="form-label">
              {{ form.empleado.label }}
            </label>
            {{ form.empleado }} {% if form.empleado.errors %}
            <div class="text-danger">{{ form.empleado.errors }}</div>
            {% endif %} {% if form.empleado.help_text %}
            <small class="form-text text-muted">
              {{ form.empleado.help_text }}
            </small>
            {% endif %}
          </div>

          <!-- Campo: Monto -->
          <div class="mb-3">
            <label for="{{ form.monto.id_for_label }}" class="form-label">
              {{ form.monto.label }}
            </label>
            {{ form.monto }} {% if form.monto.errors %}
            <div class="text-danger">{{ form.monto.errors }}</div>
            {% endif %} {% if form.monto.help_text %}
            <small class="form-text text-muted">
              {{ form.monto.help_text }}
            </small>
            {% endif %}
          </div>

          <!-- Campo: Plazo -->
          <div class="mb-3">
            <label for="{{ form.plazo_meses.id_for_label }}" class="form-label">
              {{ form.plazo_meses.label }}
            </label>
            {{ form.plazo_meses }} {% if form.plazo_meses.errors %}
            <div class="text-danger">{{ form.plazo_meses.errors }}</div>
            {% endif %} {% if form.plazo_meses.help_text %}
            <small class="form-text text-muted">
              {{ form.plazo_meses.help_text }}
            </small>
            {% endif %}
          </div>

          <hr />

          <div class="d-grid gap-2">
            <button type="submit" class="btn btn-primary btn-lg">
              Enviar Solicitud
            </button>
            <a href="{% url 'prestamos:lista' %}" class="btn btn-secondary">
              Cancelar
            </a>
          </div>
        </form>
      </div>
    </div>

    <!-- Información adicional -->
    <div class="card mt-3">
      <div class="card-body">
        <h5 class="card-title">Requisitos para Solicitar</h5>
        <ul>
          <li>Mínimo 1 año de antigüedad</li>
          <li>No tener préstamo activo</li>
          <li>Monto máximo: 6 meses de sueldo</li>
          <li>Plazo máximo: 24 meses</li>
          <li>Tasa de interés: 1% mensual</li>
        </ul>
      </div>
    </div>
  </div>
</div>
{% endblock %}
```

**Conceptos:**

#### {% csrf_token %}

```django
<form method="post">
    {% csrf_token %}
    ...
</form>
```

- Protección contra ataques CSRF
- OBLIGATORIO en todos los formularios POST

#### form.errors

```django
{% if form.monto.errors %}
    {{ form.monto.errors }}
{% endif %}
```

- Muestra errores de validación
- Django los genera automáticamente

### Paso 4: Lista de Préstamos

Crea `prestamos/templates/prestamos/lista.html`:

```html
{% extends 'base.html' %} {% block title %}Préstamos - {{ block.super }}{%
endblock %} {% block content %}
<div class="row">
  <div class="col-12">
    <div class="d-flex justify-content-between align-items-center mb-3">
      <h1>Lista de Préstamos</h1>
      <a href="{% url 'prestamos:solicitar' %}" class="btn btn-primary">
        + Nuevo Préstamo
      </a>
    </div>
    <hr />

    {% if prestamos %}
    <div class="table-responsive">
      <table class="table table-striped table-hover">
        <thead class="table-dark">
          <tr>
            <th>ID</th>
            <th>Empleado</th>
            <th>Monto</th>
            <th>Plazo</th>
            <th>Saldo</th>
            <th>Estado</th>
            <th>Fecha Solicitud</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          {% for prestamo in prestamos %}
          <tr>
            <td>{{ prestamo.id }}</td>
            <td>{{ prestamo.empleado.nombre }}</td>
            <td>${{ prestamo.monto|floatformat:2 }}</td>
            <td>{{ prestamo.plazo_meses }} meses</td>
            <td>${{ prestamo.saldo_actual|floatformat:2 }}</td>
            <td>
              {% if prestamo.estado == 'SOLICITADO' %}
              <span class="badge bg-warning text-dark"
                >{{ prestamo.get_estado_display }}</span
              >
              {% elif prestamo.estado == 'APROBADO' %}
              <span class="badge bg-info"
                >{{ prestamo.get_estado_display }}</span
              >
              {% elif prestamo.estado == 'ACTIVO' %}
              <span class="badge bg-primary"
                >{{ prestamo.get_estado_display }}</span
              >
              {% elif prestamo.estado == 'CONCLUIDO' %}
              <span class="badge bg-success"
                >{{ prestamo.get_estado_display }}</span
              >
              {% else %}
              <span class="badge bg-danger"
                >{{ prestamo.get_estado_display }}</span
              >
              {% endif %}
            </td>
            <td>{{ prestamo.fecha_solicitud|date:"d/m/Y" }}</td>
            <td>
              <a
                href="{% url 'prestamos:detalle' prestamo.id %}"
                class="btn btn-sm btn-info"
              >
                Ver Detalle
              </a>
            </td>
          </tr>
          {% endfor %}
        </tbody>
      </table>
    </div>

    <!-- Paginación -->
    {% if is_paginated %}
    <nav>
      <ul class="pagination justify-content-center">
        {% if page_obj.has_previous %}
        <li class="page-item">
          <a class="page-link" href="?page=1">Primera</a>
        </li>
        <li class="page-item">
          <a class="page-link" href="?page={{ page_obj.previous_page_number }}"
            >Anterior</a
          >
        </li>
        {% endif %}

        <li class="page-item active">
          <span class="page-link">
            Página {{ page_obj.number }} de {{ page_obj.paginator.num_pages }}
          </span>
        </li>

        {% if page_obj.has_next %}
        <li class="page-item">
          <a class="page-link" href="?page={{ page_obj.next_page_number }}"
            >Siguiente</a
          >
        </li>
        <li class="page-item">
          <a class="page-link" href="?page={{ page_obj.paginator.num_pages }}"
            >Última</a
          >
        </li>
        {% endif %}
      </ul>
    </nav>
    {% endif %} {% else %}
    <div class="alert alert-warning">
      No hay préstamos registrados.
      <a href="{% url 'prestamos:solicitar' %}">Solicitar el primero</a>
    </div>
    {% endif %}
  </div>
</div>
{% endblock %}
```

### Paso 5: Configurar URLs de Préstamos

Crea `prestamos/urls.py`:

```python
from django.urls import path
from .views import PrestamoListView, PrestamoCreateView, PrestamoDetailView

app_name = 'prestamos'

urlpatterns = [
    path('', PrestamoListView.as_view(), name='lista'),
    path('solicitar/', PrestamoCreateView.as_view(), name='solicitar'),
    path('<int:pk>/', PrestamoDetailView.as_view(), name='detalle'),
]
```

✅ **Checkpoint:** Prueba solicitar un préstamo desde `http://localhost:8000/prestamos/solicitar/`

---

## 📊 Parte 4: Reportes

### Paso 1: Vista de Detalle y Reporte

Edita `prestamos/views.py` y agrega:

```python
from django.http import HttpResponse
from django.template.loader import render_to_string

def reporte_prestamo(request, pk):
    """
    Genera un reporte imprimible del préstamo con todos sus abonos.
    """
    prestamo = get_object_or_404(Prestamo, pk=pk)
    abonos = prestamo.abonos.all()

    # Calcular totales
    total_pagado = sum(a.monto_cobrado for a in abonos)
    total_interes = sum(a.monto_interes for a in abonos)
    total_capital = sum(a.monto_capital for a in abonos)

    context = {
        'prestamo': prestamo,
        'abonos': abonos,
        'total_pagado': total_pagado,
        'total_interes': total_interes,
        'total_capital': total_capital,
        'abonos_realizados': abonos.count(),
        'abonos_pendientes': prestamo.plazo_meses - abonos.count(),
    }

    return render(request, 'prestamos/reporte.html', context)
```

### Paso 2: Template del Reporte

Crea `prestamos/templates/prestamos/reporte.html`:

```html
{% extends 'base.html' %} {% block title %}Reporte Préstamo #{{ prestamo.id }} -
{{ block.super }}{% endblock %} {% block extra_css %}
<style>
  @media print {
    .navbar,
    .no-print {
      display: none;
    }
  }
</style>
{% endblock %} {% block content %}
<div class="row">
  <div class="col-12">
    <div class="card">
      <div class="card-header bg-primary text-white">
        <h3 class="mb-0">Reporte de Préstamo #{{ prestamo.id }}</h3>
      </div>
      <div class="card-body">
        <!-- Información del Empleado -->
        <h5>Información del Empleado</h5>
        <table class="table table-bordered">
          <tr>
            <th width="30%">Nombre:</th>
            <td>{{ prestamo.empleado.nombre }}</td>
          </tr>
          <tr>
            <th>Puesto:</th>
            <td>
              {% if prestamo.empleado.obtener_puesto_actual %} {{
              prestamo.empleado.obtener_puesto_actual.nombre }} {% else %} N/A
              {% endif %}
            </td>
          </tr>
          <tr>
            <th>Antigüedad:</th>
            <td>
              {{ prestamo.empleado.calcular_antiguedad|floatformat:1 }} años
            </td>
          </tr>
        </table>

        <hr />

        <!-- Detalles del Préstamo -->
        <h5>Detalles del Préstamo</h5>
        <div class="row">
          <div class="col-md-6">
            <table class="table table-bordered">
              <tr>
                <th>Monto Solicitado:</th>
                <td class="text-end">${{ prestamo.monto|floatformat:2 }}</td>
              </tr>
              <tr>
                <th>Plazo:</th>
                <td class="text-end">{{ prestamo.plazo_meses }} meses</td>
              </tr>
              <tr>
                <th>Tasa Interés:</th>
                <td class="text-end">
                  {{ prestamo.tasa_interes_mensual }}% mensual
                </td>
              </tr>
              <tr>
                <th>Pago Fijo Capital:</th>
                <td class="text-end">
                  ${{ prestamo.pago_fijo_capital|floatformat:2 }}
                </td>
              </tr>
            </table>
          </div>
          <div class="col-md-6">
            <table class="table table-bordered">
              <tr>
                <th>Fecha Solicitud:</th>
                <td>{{ prestamo.fecha_solicitud|date:"d/m/Y" }}</td>
              </tr>
              <tr>
                <th>Fecha Aprobación:</th>
                <td>
                  {% if prestamo.fecha_aprobacion %} {{
                  prestamo.fecha_aprobacion|date:"d/m/Y" }} {% else %} Pendiente
                  {% endif %}
                </td>
              </tr>
              <tr>
                <th>Estado:</th>
                <td>
                  <span
                    class="badge bg-{% if prestamo.estado == 'ACTIVO' %}primary{% elif prestamo.estado == 'CONCLUIDO' %}success{% else %}warning{% endif %}"
                  >
                    {{ prestamo.get_estado_display }}
                  </span>
                </td>
              </tr>
              <tr>
                <th>Saldo Actual:</th>
                <td class="text-end">
                  <strong>${{ prestamo.saldo_actual|floatformat:2 }}</strong>
                </td>
              </tr>
            </table>
          </div>
        </div>

        <hr />

        <!-- Tabla de Amortización -->
        <h5>Tabla de Amortización</h5>
        {% if abonos %}
        <div class="table-responsive">
          <table class="table table-striped table-bordered">
            <thead class="table-dark">
              <tr>
                <th class="text-center">#</th>
                <th class="text-center">Fecha</th>
                <th class="text-end">Pago Capital</th>
                <th class="text-end">Interés</th>
                <th class="text-end">Total Cobrado</th>
                <th class="text-end">Saldo Restante</th>
              </tr>
            </thead>
            <tbody>
              {% for abono in abonos %}
              <tr>
                <td class="text-center">{{ abono.numero_abono }}</td>
                <td class="text-center">{{ abono.fecha|date:"d/m/Y" }}</td>
                <td class="text-end">
                  ${{ abono.monto_capital|floatformat:2 }}
                </td>
                <td class="text-end">
                  ${{ abono.monto_interes|floatformat:2 }}
                </td>
                <td class="text-end">
                  <strong>${{ abono.monto_cobrado|floatformat:2 }}</strong>
                </td>
                <td class="text-end">
                  ${{ abono.saldo_actual|floatformat:2 }}
                </td>
              </tr>
              {% endfor %}
            </tbody>
            <tfoot class="table-secondary">
              <tr>
                <th colspan="2" class="text-end">TOTALES:</th>
                <th class="text-end">${{ total_capital|floatformat:2 }}</th>
                <th class="text-end">${{ total_interes|floatformat:2 }}</th>
                <th class="text-end">${{ total_pagado|floatformat:2 }}</th>
                <th></th>
              </tr>
            </tfoot>
          </table>
        </div>
        {% else %}
        <div class="alert alert-info">
          No se han registrado abonos para este préstamo.
        </div>
        {% endif %}

        <!-- Resumen -->
        <div class="row mt-4">
          <div class="col-md-4">
            <div class="card bg-light">
              <div class="card-body text-center">
                <h6 class="text-muted">Abonos Realizados</h6>
                <h3>{{ abonos_realizados }} / {{ prestamo.plazo_meses }}</h3>
              </div>
            </div>
          </div>
          <div class="col-md-4">
            <div class="card bg-light">
              <div class="card-body text-center">
                <h6 class="text-muted">Total Pagado</h6>
                <h3>${{ total_pagado|floatformat:2 }}</h3>
              </div>
            </div>
          </div>
          <div class="col-md-4">
            <div class="card bg-light">
              <div class="card-body text-center">
                <h6 class="text-muted">Saldo Pendiente</h6>
                <h3>${{ prestamo.saldo_actual|floatformat:2 }}</h3>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Botones de acción -->
    <div class="mt-3 no-print">
      <button onclick="window.print()" class="btn btn-primary">Imprimir</button>
      <a
        href="{% url 'prestamos:detalle' prestamo.id %}"
        class="btn btn-secondary"
        >Volver</a
      >
    </div>
  </div>
</div>
{% endblock %}
```

### Paso 3: Detalle del Préstamo

Crea `prestamos/templates/prestamos/detalle.html`:

```html
{% extends 'base.html' %} {% block title %}Préstamo #{{ prestamo.id }} - {{
block.super }}{% endblock %} {% block content %}
<div class="row">
  <div class="col-md-8">
    <h1>Préstamo #{{ prestamo.id }}</h1>
    <hr />

    <div class="card">
      <div class="card-body">
        <h5 class="card-title">Información General</h5>
        <div class="row">
          <div class="col-md-6">
            <p><strong>Empleado:</strong> {{ prestamo.empleado.nombre }}</p>
            <p><strong>Monto:</strong> ${{ prestamo.monto|floatformat:2 }}</p>
            <p><strong>Plazo:</strong> {{ prestamo.plazo_meses }} meses</p>
            <p><strong>Tasa:</strong> {{ prestamo.tasa_interes_mensual }}%</p>
          </div>
          <div class="col-md-6">
            <p>
              <strong>Estado:</strong>
              <span
                class="badge bg-{% if prestamo.estado == 'ACTIVO' %}primary{% elif prestamo.estado == 'CONCLUIDO' %}success{% else %}warning{% endif %}"
              >
                {{ prestamo.get_estado_display }}
              </span>
            </p>
            <p>
              <strong>Saldo:</strong> ${{ prestamo.saldo_actual|floatformat:2 }}
            </p>
            <p>
              <strong>Fecha Solicitud:</strong> {{
              prestamo.fecha_solicitud|date:"d/m/Y" }}
            </p>
            <p>
              <strong>Pago Mensual:</strong> ~${{
              prestamo.pago_fijo_capital|add:prestamo.monto|divide:prestamo.plazo_meses|floatformat:2
              }}
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- Lista de Abonos -->
    <div class="card mt-3">
      <div class="card-body">
        <h5 class="card-title">Abonos Realizados ({{ abonos.count }})</h5>
        {% if abonos %}
        <div class="table-responsive">
          <table class="table table-sm table-striped">
            <thead>
              <tr>
                <th>#</th>
                <th>Fecha</th>
                <th>Capital</th>
                <th>Interés</th>
                <th>Total</th>
                <th>Saldo</th>
              </tr>
            </thead>
            <tbody>
              {% for abono in abonos %}
              <tr>
                <td>{{ abono.numero_abono }}</td>
                <td>{{ abono.fecha|date:"d/m/Y" }}</td>
                <td>${{ abono.monto_capital|floatformat:2 }}</td>
                <td>${{ abono.monto_interes|floatformat:2 }}</td>
                <td>
                  <strong>${{ abono.monto_cobrado|floatformat:2 }}</strong>
                </td>
                <td>${{ abono.saldo_actual|floatformat:2 }}</td>
              </tr>
              {% endfor %}
            </tbody>
          </table>
        </div>
        {% else %}
        <p class="text-muted">No hay abonos registrados aún.</p>
        {% endif %}
      </div>
    </div>
  </div>

  <div class="col-md-4">
    <div class="card">
      <div class="card-body">
        <h5 class="card-title">Acciones</h5>
        <a
          href="{% url 'prestamos:reporte' prestamo.id %}"
          class="btn btn-primary w-100 mb-2"
        >
          Ver Reporte Completo
        </a>
        <a href="{% url 'prestamos:lista' %}" class="btn btn-secondary w-100">
          Volver a Lista
        </a>
      </div>
    </div>

    <!-- Progreso -->
    <div class="card mt-3">
      <div class="card-body">
        <h5 class="card-title">Progreso</h5>
        {% widthratio abonos.count prestamo.plazo_meses 100 as porcentaje %}
        <div class="progress mb-2" style="height: 25px;">
          <div
            class="progress-bar"
            role="progressbar"
            style="width: {{ porcentaje }}%;"
            aria-valuenow="{{ porcentaje }}"
            aria-valuemin="0"
            aria-valuemax="100"
          >
            {{ porcentaje }}%
          </div>
        </div>
        <p class="small text-muted">
          {{ abonos.count }} de {{ prestamo.plazo_meses }} pagos realizados
        </p>
      </div>
    </div>
  </div>
</div>
{% endblock %}
```

### Paso 4: Actualizar URLs

Edita `prestamos/urls.py`:

```python
from django.urls import path
from .views import (
    PrestamoListView,
    PrestamoCreateView,
    PrestamoDetailView,
    reporte_prestamo
)

app_name = 'prestamos'

urlpatterns = [
    path('', PrestamoListView.as_view(), name='lista'),
    path('solicitar/', PrestamoCreateView.as_view(), name='solicitar'),
    path('<int:pk>/', PrestamoDetailView.as_view(), name='detalle'),
    path('<int:pk>/reporte/', reporte_prestamo, name='reporte'),  # ← Nuevo
]
```

✅ **Checkpoint:** Prueba el reporte completo de un préstamo.

---

## ✅ Ejercicio Final

Crea una página de inicio (`home.html`) que muestre:

1. Total de empleados activos
2. Total de préstamos activos
3. Suma de todos los saldos pendientes
4. Enlaces rápidos a las secciones principales

**Pista:**

```python
# views.py
from django.views.generic import TemplateView
from django.db.models import Sum

class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_empleados'] = Empleado.objects.filter(activo=True).count()
        context['total_prestamos'] = Prestamo.objects.filter(estado='ACTIVO').count()
        context['saldo_total'] = Prestamo.objects.filter(
            estado='ACTIVO'
        ).aggregate(Sum('saldo_actual'))['saldo_actual__sum'] or 0
        return context
```

---

## 🎯 Checklist de la Sesión

- [ ] Templates base creado
- [ ] Lista de empleados funcionaing
- [ ] Detalle de empleado con historial
- [ ] Formulario para solicitar préstamo
- [ ] Lista de préstamos con paginación
- [ ] Detalle de préstamo
- [ ] Reporte imprimible
- [ ] Bootstrap aplicado correctamente

---

## 📖 Para la Próxima Sesión

Prepárate para:

- Configurar el proyecto para producción
- DEBUG=False y configuraciones de seguridad
- Servir archivos estáticos
- Opciones de despliegue (DigitalOcean, AWS, Azure)

---

**¡Felicidades!** Ya tienes una aplicación web completa y funcional. 🎉
