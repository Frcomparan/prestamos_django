# Guía: Dockerfile y Docker Compose para Django

Esta guía te enseñará cómo crear un `Dockerfile` para tu aplicación Django y configurar `docker-compose.yml` para orquestar múltiples servicios (Django + PostgreSQL).

## Tabla de Contenidos

- [Estructura del Proyecto](#estructura-del-proyecto)
- [Creación del Dockerfile](#creación-del-dockerfile)
- [Archivo requirements.txt](#archivo-requirementstxt)
- [Configuración de Docker Compose](#configuración-de-docker-compose)
- [Variables de Entorno](#variables-de-entorno)
- [Configuración de Django](#configuración-de-django)
- [Comandos de Docker Compose](#comandos-de-docker-compose)
- [Solución de Problemas](#solución-de-problemas)

---

## Estructura del Proyecto

Antes de comenzar, tu proyecto Django debería tener una estructura similar a esta:

```
aplicacion_prestamos/
│
├── docker-compose.yml          # Configuración de servicios Docker
├── Dockerfile                  # Instrucciones para construir la imagen Django
├── .env                        # Variables de entorno (NO subir a Git)
├── .dockerignore              # Archivos a ignorar al construir la imagen
├── requirements.txt           # Dependencias de Python
│
├── manage.py                  # Script de gestión de Django
│
├── app/                       # Tu aplicación Django principal
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
└── prestamos/                 # Tu app de préstamos (ejemplo)
    ├── __init__.py
    ├── models.py
    ├── views.py
    └── ...
```

---

## Creación del Dockerfile

El `Dockerfile` contiene las instrucciones para construir la imagen de Docker para tu aplicación Django.

### Paso 1: Crear el Dockerfile

Crea un archivo llamado `Dockerfile` en la raíz de tu proyecto (sin extensión):

```dockerfile
# Usa Python 3.11 como imagen base
FROM python:3.11-slim

# Establece variables de entorno
# Previene que Python escriba archivos .pyc
ENV PYTHONDONTWRITEBYTECODE=1
# Previene que Python almacene en buffer stdout y stderr
ENV PYTHONUNBUFFERED=1

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Instala dependencias del sistema necesarias para PostgreSQL
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copia el archivo de requisitos
COPY requirements.txt /app/

# Instala las dependencias de Python
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copia el código del proyecto
COPY . /app/

# Expone el puerto 8000 (puerto por defecto de Django)
EXPOSE 8000

# Comando por defecto para ejecutar el servidor de desarrollo
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

### Explicación del Dockerfile

- **FROM python:3.11-slim**: Usa una imagen base de Python 3.11 (versión ligera)
- **ENV**: Define variables de entorno para optimizar Python en contenedores
- **WORKDIR /app**: Establece `/app` como directorio de trabajo
- **RUN apt-get**: Instala dependencias del sistema para PostgreSQL
- **COPY requirements.txt**: Copia solo el archivo de requisitos primero (para aprovechar el caché de Docker)
- **RUN pip install**: Instala las dependencias de Python
- **COPY . /app/**: Copia todo el código del proyecto
- **EXPOSE 8000**: Documenta que el contenedor escucha en el puerto 8000
- **CMD**: Comando que se ejecuta cuando el contenedor inicia

---

## Archivo requirements.txt

El archivo `requirements.txt` lista todas las dependencias de Python que necesita tu proyecto.

### Paso 2: Crear requirements.txt

Crea un archivo `requirements.txt` en la raíz de tu proyecto:

```txt
# Framework Django
Django==5.0.2

# Adaptador de PostgreSQL para Python
psycopg2-binary==2.9.9

# Variables de entorno
python-decouple==3.8

# Django REST Framework (opcional, para APIs)
djangorestframework==3.14.0

# Herramientas de desarrollo
django-debug-toolbar==4.3.0

# Manejo de archivos estáticos en producción (opcional)
whitenoise==6.6.0
```

### Dependencias Explicadas

- **Django**: El framework web
- **psycopg2-binary**: Adaptador para conectar Django con PostgreSQL
- **python-decouple**: Para manejar variables de entorno de forma segura
- **djangorestframework**: Para crear APIs REST (opcional)
- **django-debug-toolbar**: Herramienta de depuración (solo desarrollo)
- **whitenoise**: Para servir archivos estáticos eficientemente

---

## Configuración de Docker Compose

Docker Compose permite definir y ejecutar aplicaciones Docker multi-contenedor.

### Paso 3: Crear docker-compose.yml

Crea un archivo `docker-compose.yml` en la raíz de tu proyecto:

```yaml
version: '3.8'

services:
  # Servicio de base de datos PostgreSQL
  db:
    image: postgres:15-alpine
    container_name: prestamos_db
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=prestamos_db
      - POSTGRES_USER=prestamos_user
      - POSTGRES_PASSWORD=prestamos_password
    ports:
      - '5432:5432'
    healthcheck:
      test: ['CMD-SHELL', 'pg_isready -U prestamos_user -d prestamos_db']
      interval: 10s
      timeout: 5s
      retries: 5

  # Servicio de la aplicación Django
  web:
    build: .
    container_name: prestamos_web
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/app
    ports:
      - '8000:8000'
    environment:
      - DEBUG=True
      - DATABASE_URL=postgresql://prestamos_user:prestamos_password@db:5432/prestamos_db
      - SECRET_KEY=tu-clave-secreta-desarrollo
    depends_on:
      db:
        condition: service_healthy
    stdin_open: true
    tty: true

# Volúmenes para persistencia de datos
volumes:
  postgres_data:
```

### Explicación de docker-compose.yml

#### Servicio `db` (PostgreSQL)

- **image**: Usa la imagen oficial de PostgreSQL 15 (versión Alpine, más ligera)
- **container_name**: Nombre del contenedor
- **volumes**: Persiste los datos de PostgreSQL en un volumen
- **environment**: Variables de entorno para configurar PostgreSQL
  - `POSTGRES_DB`: Nombre de la base de datos
  - `POSTGRES_USER`: Usuario de la base de datos
  - `POSTGRES_PASSWORD`: Contraseña del usuario
- **ports**: Mapea el puerto 5432 del contenedor al puerto 5432 del host
- **healthcheck**: Verifica que PostgreSQL esté listo antes de iniciar otros servicios

#### Servicio `web` (Django)

- **build**: Construye la imagen desde el Dockerfile en el directorio actual
- **command**: Sobrescribe el CMD del Dockerfile para ejecutar el servidor de desarrollo
- **volumes**: Monta el directorio actual en `/app` (permite edición en vivo)
- **ports**: Mapea el puerto 8000 del contenedor al puerto 8000 del host
- **environment**: Variables de entorno para Django
- **depends_on**: Espera a que la base de datos esté saludable antes de iniciar
- **stdin_open** y **tty**: Permiten interacción con el contenedor

---

## Variables de Entorno

Para mayor seguridad, es recomendable usar un archivo `.env` para las variables de entorno.

### Paso 4: Crear archivo .env

Crea un archivo `.env` en la raíz de tu proyecto:

```env
# Django
DEBUG=True
SECRET_KEY=tu-clave-secreta-muy-segura-cambiar-en-produccion
ALLOWED_HOSTS=localhost,127.0.0.1

# PostgreSQL
POSTGRES_DB=prestamos_db
POSTGRES_USER=prestamos_user
POSTGRES_PASSWORD=prestamos_password
POSTGRES_HOST=db
POSTGRES_PORT=5432

# URL de conexión a la base de datos
DATABASE_URL=postgresql://prestamos_user:prestamos_password@db:5432/prestamos_db
```

### Paso 5: Actualizar docker-compose.yml para usar .env

Modifica el `docker-compose.yml` para usar el archivo `.env`:

```yaml
version: '3.8'

services:
  db:
    image: postgres:15-alpine
    container_name: prestamos_db
    volumes:
      - postgres_data:/var/lib/postgresql/data
    env_file:
      - .env
    ports:
      - '5432:5432'
    healthcheck:
      test: ['CMD-SHELL', 'pg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DB}']
      interval: 10s
      timeout: 5s
      retries: 5

  web:
    build: .
    container_name: prestamos_web
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/app
    ports:
      - '8000:8000'
    env_file:
      - .env
    depends_on:
      db:
        condition: service_healthy
    stdin_open: true
    tty: true

volumes:
  postgres_data:
```

### Paso 6: Crear archivo .dockerignore

Crea un archivo `.dockerignore` para excluir archivos innecesarios al construir la imagen:

```
# Git
.git
.gitignore

# Python
__pycache__
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.venv

# Django
*.log
db.sqlite3
media/
staticfiles/

# IDEs
.vscode/
.idea/
*.swp
*.swo

# Docker
Dockerfile
docker-compose.yml
.dockerignore

# Entorno
.env
.env.local

# Documentación
README.md
docs/
```

---

## Configuración de Django

Ahora necesitas configurar Django para usar PostgreSQL y las variables de entorno.

### Paso 7: Actualizar settings.py

Abre tu archivo `settings.py` y actualiza la configuración de la base de datos:

```python
# settings.py
from pathlib import Path
from decouple import config
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='insecure-key-for-development')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1').split(',')

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

# Opción 1: Usando DATABASE_URL
DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL')
    )
}

# Opción 2: Configuración manual (alternativa)
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': config('POSTGRES_DB'),
#         'USER': config('POSTGRES_USER'),
#         'PASSWORD': config('POSTGRES_PASSWORD'),
#         'HOST': config('POSTGRES_HOST', default='db'),
#         'PORT': config('POSTGRES_PORT', default='5432'),
#     }
# }
```

**Nota**: Si usas la Opción 1, necesitas instalar `dj-database-url`:

```txt
# Agregar a requirements.txt
dj-database-url==2.1.0
```

---

## Comandos de Docker Compose

Una vez configurado todo, usa estos comandos para gestionar tus contenedores.

### Construcción e Inicio

```bash
# Construir las imágenes
docker compose build

# Iniciar los servicios (modo detached)
docker compose up -d

# Iniciar los servicios (ver logs en tiempo real)
docker compose up

# Construir e iniciar en un solo comando
docker compose up --build
```

### Gestión de Servicios

```bash
# Ver servicios en ejecución
docker compose ps

# Ver logs de todos los servicios
docker compose logs

# Ver logs de un servicio específico
docker compose logs web
docker compose logs db

# Seguir logs en tiempo real
docker compose logs -f web

# Detener servicios
docker compose stop

# Detener y eliminar contenedores
docker compose down

# Detener y eliminar contenedores, volúmenes y redes
docker compose down -v
```

### Comandos de Django en Docker

```bash
# Ejecutar migraciones
docker compose exec web python manage.py migrate

# Crear migraciones
docker compose exec web python manage.py makemigrations

# Crear superusuario
docker compose exec web python manage.py createsuperuser

# Abrir shell de Django
docker compose exec web python manage.py shell

# Recolectar archivos estáticos
docker compose exec web python manage.py collectstatic

# Ejecutar tests
docker compose exec web python manage.py test

# Abrir bash dentro del contenedor web
docker compose exec web bash

# Abrir psql en el contenedor de base de datos
docker compose exec db psql -U prestamos_user -d prestamos_db
```

### Flujo de Trabajo Completo

```bash
# 1. Construir las imágenes
docker compose build

# 2. Iniciar los servicios
docker compose up -d

# 3. Ejecutar migraciones iniciales
docker compose exec web python manage.py migrate

# 4. Crear un superusuario
docker compose exec web python manage.py createsuperuser

# 5. Ver la aplicación en el navegador
# Abre http://localhost:8000
```

---

## Script de Inicialización (Opcional)

Puedes crear un script para automatizar la inicialización del proyecto.

### entrypoint.sh

Crea un archivo `entrypoint.sh` en la raíz del proyecto:

```bash
#!/bin/bash

# Esperar a que PostgreSQL esté listo
echo "Esperando a PostgreSQL..."
while ! nc -z db 5432; do
  sleep 0.1
done
echo "PostgreSQL está listo!"

# Ejecutar migraciones
echo "Ejecutando migraciones..."
python manage.py migrate --noinput

# Recolectar archivos estáticos
echo "Recolectando archivos estáticos..."
python manage.py collectstatic --noinput

# Crear superusuario si no existe (solo para desarrollo)
# echo "Creando superusuario..."
# python manage.py createsuperuser --noinput

# Iniciar servidor
echo "Iniciando servidor Django..."
exec "$@"
```

### Actualizar Dockerfile para usar entrypoint.sh

```dockerfile
# ... (código anterior del Dockerfile)

# Copiar y dar permisos al script de entrada
COPY entrypoint.sh /app/
RUN chmod +x /app/entrypoint.sh

# Establecer el entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]

# Comando por defecto
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

### Actualizar docker-compose.yml

```yaml
web:
  build: .
  container_name: prestamos_web
  command: python manage.py runserver 0.0.0.0:8000
  volumes:
    - .:/app
  ports:
    - '8000:8000'
  env_file:
    - .env
  depends_on:
    db:
      condition: service_healthy
  stdin_open: true
  tty: true
```

---

## Solución de Problemas

### Problema: "Port is already allocated"

**Error**: El puerto 8000 o 5432 ya está en uso.

**Solución**:

```bash
# Ver qué está usando el puerto 8000
# Windows
netstat -ano | findstr :8000

# Mac/Linux
lsof -i :8000

# Cambiar el puerto en docker-compose.yml
ports:
  - "8001:8000"  # Ahora accede en http://localhost:8001
```

### Problema: "No migrations to apply"

**Causa**: Las migraciones no se han creado o no se detectan cambios.

**Solución**:

```bash
# Crear migraciones
docker compose exec web python manage.py makemigrations

# Aplicar migraciones
docker compose exec web python manage.py migrate
```

### Problema: "could not connect to server: Connection refused"

**Causa**: Django intenta conectarse a PostgreSQL antes de que esté listo.

**Solución**: El `healthcheck` en docker-compose.yml debería resolver esto. Si persiste:

```bash
# Reiniciar servicios
docker compose restart

# O verificar logs de la base de datos
docker compose logs db
```

### Problema: Cambios en el código no se reflejan

**Causa**: El contenedor no está usando volúmenes correctamente.

**Solución**:

```bash
# Verificar que los volúmenes estén montados
docker compose config

# Reiniciar el servicio web
docker compose restart web
```

### Problema: "permission denied" en archivos

**Causa**: Problemas de permisos entre el host y el contenedor.

**Solución (Linux/Mac)**:

```bash
# Dar permisos al usuario
sudo chown -R $USER:$USER .
```

### Limpiar y reiniciar todo

Si tienes problemas persistentes, puedes limpiar completamente:

```bash
# Detener y eliminar todo (¡CUIDADO: elimina datos!)
docker compose down -v

# Eliminar imágenes
docker compose down --rmi all

# Reconstruir desde cero
docker compose build --no-cache
docker compose up
```

---

## Mejores Prácticas

1. **Usa .env para variables sensibles**: Nunca subas `.env` a Git
2. **Agrega .env a .gitignore**:

   ```
   # .gitignore
   .env
   .env.local
   *.env
   ```

3. **Crea un .env.example**: Para documentar las variables necesarias

   ```env
   # .env.example
   DEBUG=True
   SECRET_KEY=your-secret-key-here
   POSTGRES_DB=your_db_name
   POSTGRES_USER=your_db_user
   POSTGRES_PASSWORD=your_db_password
   ```

4. **Usa volúmenes nombrados**: Para persistir datos importantes
5. **Healthchecks**: Asegura que los servicios estén listos antes de conectarse
6. **Multi-stage builds**: Para imágenes de producción más pequeñas

---

## Recursos Adicionales

- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/)
- [PostgreSQL Docker Hub](https://hub.docker.com/_/postgres)
- [Best practices for writing Dockerfiles](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)

---
