# Sesión 4: Preparación para Despliegue y Mejores Prácticas

**Duración estimada:** 3-4 horas  
**Nivel:** Intermedio-Avanzado  
**Prerequisito:** Sesiones 1, 2 y 3 completadas

## 🎯 Objetivos de la Sesión

Al finalizar esta sesión, podrás:

- ✅ Configurar el proyecto para producción
- ✅ Manejar archivos estáticos correctamente
- ✅ Configurar variables de entorno seguras
- ✅ Conocer opciones de despliegue
- ✅ Implementar mejores prácticas de seguridad

---

## 🔒 Parte 1: Seguridad y Configuración de Producción

### ¿Desarrollo vs Producción?

**Desarrollo** = Tu computadora, donde programas  
**Producción** = Servidor en internet, donde usuarios reales acceden

| Aspecto            | Desarrollo             | Producción             |
| ------------------ | ---------------------- | ---------------------- |
| DEBUG              | True (muestra errores) | False (oculta errores) |
| SECRET_KEY         | Puede estar en código  | NUNCA en código        |
| Base de datos      | SQLite local           | PostgreSQL, MySQL      |
| Archivos estáticos | Django los sirve       | Nginx, CDN             |
| HTTPS              | No necesario           | Obligatorio            |

### Paso 1: Archivo .env

**Nunca hagas esto:**

```python
# ❌ MAL - Expones información sensible
SECRET_KEY = 'abc123supersecreta'
DEBUG = True
DATABASE_PASSWORD = 'mipassword123'
```

**Haz esto:**

Crea `.env` en la raíz del proyecto:

```env
# .env - NO INCLUIR EN GIT
SECRET_KEY=tu-clave-secreta-super-larga-y-aleatoria-aqui
DEBUG=False
ALLOWED_HOSTS=midominio.com,www.midominio.com
DATABASE_URL=postgresql://usuario:password@localhost:5432/prestamos_db

# Configuraciones específicas de producción
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

**Explicación:**

- `SECRET_KEY` = Clave para encriptar sesiones y tokens
- `DEBUG` = False en producción (no mostrar errores detallados)
- `ALLOWED_HOSTS` = Dominios permitidos
- `SECURE_SSL_REDIRECT` = Forzar HTTPS

### Paso 2: Leer Variables de Entorno

Edita `config/settings.py`:

```python
from decouple import config
import dj_database_url

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1').split(',')

# Database
if DEBUG:
    # Desarrollo: SQLite
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    # Producción: PostgreSQL desde DATABASE_URL
    DATABASES = {
        'default': dj_database_url.config(
            default=config('DATABASE_URL')
        )
    }
```

### Paso 3: Configuraciones de Seguridad

Agrega al final de `settings.py`:

```python
# Configuraciones de seguridad para producción
if not DEBUG:
    # HTTPS
    SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=True, cast=bool)
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

    # HSTS (HTTP Strict Transport Security)
    SECURE_HSTS_SECONDS = 31536000  # 1 año
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

    # Otras configuraciones de seguridad
    X_FRAME_OPTIONS = 'DENY'
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True
```

**Explicación:**

- `SECURE_SSL_REDIRECT` = Redirige HTTP → HTTPS
- `SESSION_COOKIE_SECURE` = Cookies solo por HTTPS
- `CSRF_COOKIE_SECURE` = Token CSRF solo por HTTPS
- `SECURE_HSTS_SECONDS` = Navegador solo usa HTTPS por 1 año
- `X_FRAME_OPTIONS` = Previene clickjacking
- `SECURE_CONTENT_TYPE_NOSNIFF` = Previene ataques MIME

### Paso 4: Generar SECRET_KEY Segura

```python
# En la terminal de Django shell:
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

Copia el resultado a tu archivo `.env`:

```env
SECRET_KEY=django-insecure-g6n_1234567890abcdefghijklmnopqrstuvwxyz
```

### Paso 5: Actualizar .gitignore

Asegúrate de que `.gitignore` incluye:

```gitignore
# Variables de entorno
.env
.env.local
.env.production

# Base de datos local
db.sqlite3
*.db

# Python
__pycache__/
*.py[cod]
*$py.class
*.so

# Django
*.log
local_settings.py

# Static files
/static/
/staticfiles/
/media/

# IDE
.vscode/
.idea/
*.swp
*.swo
```

✅ **Checkpoint:** Verifica que `.env` NO aparece en `git status`.

---

## 📁 Parte 2: Archivos Estáticos

### ¿Qué son archivos estáticos?

- **Estáticos** = CSS, JavaScript, imágenes, fuentes
- **No cambian** por usuario
- En desarrollo: Django los sirve
- En producción: Nginx, Apache, o CDN

### Paso 1: Configurar STATIC_ROOT

Edita `settings.py`:

```python
import os

# URL para acceder a archivos estáticos
STATIC_URL = '/static/'

# Directorio donde se recopilan todos los estáticos en producción
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Directorios adicionales con estáticos
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Configuración de archivos subidos por usuarios
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

**Explicación:**

- `STATIC_URL` = URL para acceder (`/static/css/style.css`)
- `STATIC_ROOT` = Donde Django recopila todos los estáticos con `collectstatic`
- `STATICFILES_DIRS` = Carpetas adicionales con estáticos
- `MEDIA_ROOT` = Archivos subidos por usuarios (fotos, documentos)

### Paso 2: Crear Estructura de Static

```bash
mkdir -p static/css static/js static/img
```

Crea `static/css/custom.css`:

```css
/* Estilos personalizados del proyecto */
:root {
  --primary-color: #0d6efd;
  --secondary-color: #6c757d;
}

.navbar-brand {
  font-weight: bold;
  font-size: 1.5rem;
}

.card {
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s;
}

.card:hover {
  transform: translateY(-5px);
}

.table-hover tbody tr:hover {
  background-color: rgba(0, 0, 0, 0.03);
  cursor: pointer;
}

/* Estilos para impresión */
@media print {
  .no-print {
    display: none !important;
  }
}
```

### Paso 3: Usar Estáticos en Templates

Edita `base.html`:

```html
{% load static %}
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <title>{% block title %}Sistema de Préstamos{% endblock %}</title>

    <!-- Bootstrap CSS -->
    <link
      href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css"
      rel="stylesheet"
    />

    <!-- CSS Personalizado -->
    <link rel="stylesheet" href="{% static 'css/custom.css' %}" />

    {% block extra_css %}{% endblock %}
  </head>
  <body>
    <!-- ... contenido ... -->

    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>

    <!-- JavaScript personalizado -->
    <script src="{% static 'js/main.js' %}"></script>

    {% block extra_js %}{% endblock %}
  </body>
</html>
```

**Conceptos:**

#### {% load static %}

```django
{% load static %}
<img src="{% static 'img/logo.png' %}">
```

- Carga el sistema de archivos estáticos
- `{% static %}` genera la URL correcta

### Paso 4: Recopilar Archivos Estáticos

```bash
# Recopila todos los estáticos en STATIC_ROOT
docker compose exec web python manage.py collectstatic

# Responde 'yes' cuando pregunte
```

**¿Qué hace?**

- Busca archivos estáticos en todas las apps
- Los copia a `staticfiles/`
- En producción, Nginx sirve desde esta carpeta

### Paso 5: WhiteNoise (Opcional)

WhiteNoise sirve archivos estáticos directamente desde Django (útil en Heroku, Railway).

Agrega a `requirements.txt`:

```txt
whitenoise==6.6.0
```

Configura en `settings.py`:

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # ← Después de SecurityMiddleware
    'django.contrib.sessions.middleware.SessionMiddleware',
    # ... resto de middlewares
]

# Configuración de WhiteNoise
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

---

## 🚀 Parte 3: Preparación de Base de Datos

### Paso 1: Migraciones en Producción

**Antes de desplegar:**

```bash
# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Verificar que no hay pendientes
python manage.py migrate --plan
```

### Paso 2: Fixtures para Datos Iniciales

Crea datos de ejemplo que se puedan cargar en producción:

```bash
# Exportar datos actuales
python manage.py dumpdata empleados.Puesto --indent 2 > fixtures/puestos.json
python manage.py dumpdata auth.User --indent 2 > fixtures/users.json
```

Crea `fixtures/puestos.json`:

```json
[
  {
    "model": "empleados.puesto",
    "pk": 1,
    "fields": {
      "nombre": "Gerente General",
      "sueldo": "15000.00"
    }
  },
  {
    "model": "empleados.puesto",
    "pk": 2,
    "fields": {
      "nombre": "Jefe de Área",
      "sueldo": "10000.00"
    }
  },
  {
    "model": "empleados.puesto",
    "pk": 3,
    "fields": {
      "nombre": "Empleado",
      "sueldo": "6000.00"
    }
  }
]
```

Cargar fixtures:

```bash
python manage.py loaddata fixtures/puestos.json
```

### Paso 3: Crear Superusuario

```bash
# En producción, crear admin:
python manage.py createsuperuser
```

**Automatizar con variables de entorno:**

```python
# En un script de deployment
from django.contrib.auth import get_user_model
User = get_user_model()

if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password=os.environ.get('DJANGO_SUPERUSER_PASSWORD')
    )
```

---

## 🌐 Parte 4: Opciones de Despliegue

### Opción 1: Railway (Más Fácil)

**Ventajas:**

- Deployment automático desde GitHub
- PostgreSQL integrado
- SSL gratis
- Plan gratuito disponible

**Pasos:**

1. **Crear `Procfile`:**

```procfile
web: gunicorn config.wsgi --log-file -
release: python manage.py migrate
```

2. **Crear `railway.json`:**

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "gunicorn config.wsgi:application --bind 0.0.0.0:$PORT",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

3. **Variables de entorno en Railway:**

```
SECRET_KEY=tu-clave-aqui
DEBUG=False
ALLOWED_HOSTS=nombreapp.railway.app
DATABASE_URL=postgresql://...  # Railway lo genera
```

4. **Conectar GitHub y desplegar:**
   - Ve a railway.app
   - Connect con GitHub
   - Selecciona el repo
   - Deploy automático

### Opción 2: DigitalOcean App Platform

**Ventajas:**

- Fácil de configurar
- Escalable
- Base de datos administrada

**Pasos:**

1. **Crear `app.yaml`:**

```yaml
name: sistema-prestamos
services:
  - name: web
    github:
      repo: tu-usuario/tu-repo
      branch: main
    build_command: |
      pip install -r requirements.txt
      python manage.py collectstatic --noinput
    run_command: gunicorn config.wsgi:application
    envs:
      - key: SECRET_KEY
        scope: RUN_TIME
        value: ${SECRET_KEY}
      - key: DEBUG
        scope: RUN_TIME
        value: 'False'
    http_port: 8000

databases:
  - name: prestamos-db
    engine: PG
    version: '15'
```

### Opción 3: Heroku

```bash
# Instalar Heroku CLI
# Windows: https://devcenter.heroku.com/articles/heroku-cli
# Mac: brew install heroku/brew/heroku

# Login
heroku login

# Crear app
heroku create nombre-app

# Agregar PostgreSQL
heroku addons:create heroku-postgresql:mini

# Configurar variables
heroku config:set SECRET_KEY=tu-clave
heroku config:set DEBUG=False

# Deploy
git push heroku main

# Migrar
heroku run python manage.py migrate

# Crear superuser
heroku run python manage.py createsuperuser
```

### Opción 4: VPS (DigitalOcean Droplet, AWS EC2)

**Más complejo, más control**

**Stack recomendado:**

- Ubuntu 22.04 LTS
- Nginx (servidor web)
- Gunicorn (WSGI server)
- PostgreSQL
- Supervisor (mantener Gunicorn corriendo)

**Pasos breves:**

1. **Instalar dependencias:**

```bash
apt update
apt install python3-pip python3-venv postgresql nginx
```

2. **Configurar PostgreSQL:**

```bash
sudo -u postgres psql
CREATE DATABASE prestamos_db;
CREATE USER prestamos_user WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE prestamos_db TO prestamos_user;
```

3. **Configurar Gunicorn:**

```bash
pip install gunicorn
gunicorn config.wsgi:application --bind 127.0.0.1:8000
```

4. **Configurar Nginx:**

```nginx
server {
    listen 80;
    server_name tu-dominio.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static/ {
        alias /path/to/staticfiles/;
    }

    location /media/ {
        alias /path/to/media/;
    }
}
```

5. **Configurar Supervisor:**

```ini
[program:prestamos]
command=/path/to/venv/bin/gunicorn config.wsgi:application --bind 127.0.0.1:8000
directory=/path/to/project
user=www-data
autostart=true
autorestart=true
```

---

## ✅ Parte 5: Checklist de Despliegue

### Antes de Desplegar

- [ ] `DEBUG = False`
- [ ] `SECRET_KEY` en variable de entorno
- [ ] `ALLOWED_HOSTS` configurado
- [ ] Todas las migraciones aplicadas
- [ ] `requirements.txt` actualizado
- [ ] `.gitignore` incluye `.env`
- [ ] Archivos estáticos recopilados
- [ ] Tests pasando (si tienes)

### Configuraciones de Producción

- [ ] HTTPS configurado
- [ ] SECURE_SSL_REDIRECT = True
- [ ] SESSION_COOKIE_SECURE = True
- [ ] CSRF_COOKIE_SECURE = True
- [ ] Base de datos externa (PostgreSQL)
- [ ] Backups automatizados
- [ ] Logging configurado

### Después de Desplegar

- [ ] Migrar base de datos
- [ ] Crear superusuario
- [ ] Cargar fixtures (datos iniciales)
- [ ] Probar funcionalidad principal
- [ ] Verificar SSL con SSL Labs
- [ ] Configurar dominio personalizado
- [ ] Monitoreo (Sentry, New Relic)

---

## 🧪 Parte 6: Testing Básico

### ¿Por qué Tests?

- Detectar bugs antes de producción
- Asegurar que cambios no rompan funcionalidad
- Documentación automática

### Test de Modelo

Crea `prestamos/tests.py`:

```python
from django.test import TestCase
from django.core.exceptions import ValidationError
from empleados.models import Empleado, Puesto, HistorialPuesto
from prestamos.models import Prestamo, Abono
from datetime import date, timedelta

class PrestamoModelTest(TestCase):
    def setUp(self):
        """Configuración inicial para todos los tests."""
        # Crear puesto
        self.puesto = Puesto.objects.create(
            nombre="Empleado",
            sueldo=5000
        )

        # Crear empleado con > 1 año de antigüedad
        self.empleado = Empleado.objects.create(
            nombre="Juan Pérez",
            fecha_ingreso=date.today() - timedelta(days=400)
        )

        # Asignar puesto
        HistorialPuesto.objects.create(
            empleado=self.empleado,
            puesto=self.puesto,
            fecha_inicio=self.empleado.fecha_ingreso
        )

    def test_calculo_monto_maximo(self):
        """Prueba que el monto máximo sea 6 meses de sueldo."""
        prestamo = Prestamo(
            empleado=self.empleado,
            monto=10000,
            plazo_meses=12
        )
        monto_maximo = prestamo.calcular_monto_maximo()

        self.assertEqual(monto_maximo, 30000)  # 5000 * 6

    def test_validacion_antiguedad(self):
        """Empleado con < 1 año no puede solicitar."""
        empleado_nuevo = Empleado.objects.create(
            nombre="María López",
            fecha_ingreso=date.today() - timedelta(days=180)  # 6 meses
        )

        prestamo = Prestamo(
            empleado=empleado_nuevo,
            monto=5000,
            plazo_meses=12
        )

        puede, mensaje = prestamo.puede_solicitar_prestamo()
        self.assertFalse(puede)
        self.assertIn("antigüedad", mensaje.lower())

    def test_calculo_abono(self):
        """Prueba cálculo automático de abono."""
        prestamo = Prestamo.objects.create(
            empleado=self.empleado,
            monto=12000,
            plazo_meses=12,
            tasa_interes_mensual=1.00
        )

        # Primer abono
        abono = Abono.objects.create(
            prestamo=prestamo,
            numero_abono=1,
            fecha=date.today()
        )

        # Verificar cálculos
        self.assertEqual(abono.monto_capital, 1000)  # 12000 / 12
        self.assertEqual(abono.monto_interes, 120)   # 12000 * 0.01
        self.assertEqual(abono.monto_cobrado, 1120)  # 1000 + 120
        self.assertEqual(abono.saldo_actual, 11000)  # 12000 - 1000
```

### Ejecutar Tests

```bash
# Todos los tests
docker compose exec web python manage.py test

# Tests de una app
docker compose exec web python manage.py test prestamos

# Un test específico
docker compose exec web python manage.py test prestamos.tests.PrestamoModelTest.test_calculo_abono

# Con más detalle
docker compose exec web python manage.py test --verbosity=2
```

### Test de Vista (Opcional)

```python
class PrestamoViewTest(TestCase):
    def test_lista_prestamos(self):
        """Prueba que la lista de préstamos carga correctamente."""
        response = self.client.get('/prestamos/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Lista de Préstamos')

    def test_formulario_solicitud(self):
        """Prueba envío de formulario."""
        response = self.client.post('/prestamos/solicitar/', {
            'empleado': self.empleado.id,
            'monto': 20000,
            'plazo_meses': 12
        })
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertEqual(Prestamo.objects.count(), 1)
```

---

## 📊 Parte 7: Monitoreo y Mantenimiento

### Logging

Configura en `settings.py`:

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs/django.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
}
```

Usar en código:

```python
import logging
logger = logging.getLogger(__name__)

def mi_vista(request):
    logger.info(f"Usuario {request.user} accedió a la vista")
    try:
        # ... código ...
    except Exception as e:
        logger.error(f"Error en mi_vista: {e}", exc_info=True)
```

### Sentry (Monitoreo de Errores)

1. **Registrarse en sentry.io**

2. **Instalar:**

```bash
pip install sentry-sdk
```

3. **Configurar en `settings.py`:**

```python
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn=config('SENTRY_DSN', default=''),
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,
    send_default_pii=True
)
```

### Health Check Endpoint

Crea `config/views.py`:

```python
from django.http import JsonResponse
from django.db import connection

def health_check(request):
    """Endpoint para verificar que la aplicación está funcionando."""
    try:
        # Verificar conexión a BD
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")

        return JsonResponse({
            'status': 'healthy',
            'database': 'connected'
        })
    except Exception as e:
        return JsonResponse({
            'status': 'unhealthy',
            'error': str(e)
        }, status=500)
```

Agrega a `urls.py`:

```python
from .views import health_check

urlpatterns = [
    # ...
    path('health/', health_check, name='health_check'),
]
```

---

## ✅ Ejercicio Final: Deploy Completo

**Objetivo:** Desplegar la aplicación en Railway

1. **Preparar el proyecto:**
   - [ ] Actualizar `requirements.txt`
   - [ ] Crear `Procfile`
   - [ ] Configurar `.env.example`
   - [ ] Verificar `.gitignore`

2. **Configurar Railway:**
   - [ ] Crear cuenta en railway.app
   - [ ] Conectar con GitHub
   - [ ] Agregar PostgreSQL
   - [ ] Configurar variables de entorno

3. **Deploy:**
   - [ ] Push a GitHub
   - [ ] Esperar deployment
   - [ ] Migrar base de datos
   - [ ] Crear superusuario

4. **Verificar:**
   - [ ] Abrir la URL
   - [ ] Probar login al admin
   - [ ] Crear un empleado
   - [ ] Solicitar un préstamo

---

## 🎯 Checklist Final de la Sesión

- [ ] Variables de entorno configuradas
- [ ] Archivos estáticos funcionando
- [ ] Configuraciones de seguridad aplicadas
- [ ] Tests básicos creados
- [ ] Conocimiento de opciones de deploy
- [ ] Logging configurado

---

## 🚀 Próximos Pasos

**Mejoras futuras:**

1. Autenticación de usuarios (login/logout)
2. Permisos por rol (empleado, gerente, admin)
3. Notificaciones por email
4. Integración con sistemas de nómina
5. App móvil con la API REST
6. Dashboard con gráficas (Chart.js)
7. Exportar reportes a PDF/Excel
8. CI/CD con GitHub Actions

---

**¡Felicidades por completar el taller!** 🎉  
Ahora tienes los conocimientos para desarrollar y desplegar aplicaciones web con Django.
