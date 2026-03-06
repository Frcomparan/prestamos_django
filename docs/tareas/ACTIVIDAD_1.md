# Actividad para Casa 1: Configuración Inicial del Proyecto Django

**Curso:** Taller de Django  
**Tipo:** Actividad individual
**Tiempo estimado:** 45-60 minutos

---

## 🎯 Objetivo

Completar la configuración inicial del proyecto Django con Docker, creando y levantando el proyecto por primera vez.

---

## 📋 Prerrequisitos

Antes de iniciar, asegúrate de tener:

- ✅ Docker Desktop instalado y funcionando
- ✅ Docker Compose configurado
- ✅ Archivos creados en clase:
  - `requirements.txt`
  - `Dockerfile`
  - `docker-compose.yml`
- ✅ Carpeta del proyecto: `sistema_prestamos` o como la hayas nombrado

**⚠️ Importante:** Si no completaste los pasos 1-3 en clase, consulta la [guía](../guias/GUIA_1_EST.md) completa de la Sesión 1 antes de continuar.

---

## 📝 Instrucciones de la Actividad

### Paso 4: Iniciar Docker y Crear Proyecto Django

#### 4.1 Construir las imágenes de Docker

Abre tu terminal en la carpeta del proyecto y ejecuta:

```bash
docker compose build
```

**¿Qué hace este comando?**

- Lee el `Dockerfile`
- Descarga la imagen de Python 3.11
- Instala las dependencias de `requirements.txt`
- Crea una imagen personalizada para tu proyecto

**Tiempo aproximado:** 3-5 minutos (dependiendo de tu conexión a internet)

**✅ Verificación:** Deberías ver mensajes como:

```
[+] Building 45.2s (12/12) FINISHED
Successfully built abc123def456
Successfully tagged sistema_prestamos_web:latest
```

#### 4.2 Crear el proyecto Django

Una vez construida la imagen, crea el proyecto Django:

```bash
docker compose run web django-admin startproject config .
```

**⚠️ Nota importante:**

- El punto (`.`) al final es crucial, indica que el proyecto se crea en el directorio actual
- Este comando solo se ejecuta **UNA VEZ**

**¿Qué hace este comando?**

- Ejecuta Django dentro del contenedor
- Crea la estructura del proyecto en la carpeta actual
- Genera archivos de configuración

**✅ Verificación:** Deberías ver nuevos archivos creados:

```bash
ls
# Debes ver:
# manage.py
# config/
# requirements.txt
# Dockerfile
# docker-compose.yml
```

#### 4.3 Verificar la estructura creada

Confirma que tienes esta estructura:

```
sistema_prestamos/
├── config/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py    ← Archivo importante
│   ├── urls.py
│   └── wsgi.py
├── manage.py           ← Archivo importante
├── requirements.txt
├── Dockerfile
└── docker-compose.yml
```

---

### Paso 5: Configurar la Base de Datos

#### 5.1 Editar settings.py

Abre el archivo `config/settings.py` y busca la sección `DATABASES` (aproximadamente línea 75).

**Antes (configuración por defecto con SQLite):**

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

**Después (configuración para PostgreSQL):**

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'prestamos_db',
        'USER': 'prestamos_user',
        'PASSWORD': 'prestamos_password',
        'HOST': 'db',
        'PORT': '5432',
    }
}
```

**Explicación de los parámetros:**

- `ENGINE`: Motor de base de datos (PostgreSQL en lugar de SQLite)
- `NAME`: Nombre de la base de datos (debe coincidir con `docker-compose.yml`)
- `USER` y `PASSWORD`: Credenciales (deben coincidir con `docker-compose.yml`)
- `HOST`: Nombre del servicio de base de datos (`db` en nuestro caso)
- `PORT`: Puerto de PostgreSQL (5432 es el estándar)

#### 5.2 Configurar idioma y zona horaria

En el mismo archivo `config/settings.py`, busca estas líneas (aproximadamente línea 106):

**Cambiar de:**

```python
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
```

**A:**

```python
LANGUAGE_CODE = 'es-mx'
TIME_ZONE = 'America/Mexico_City'
```

**¿Por qué es importante?**

- Las fechas se mostrarán en formato mexicano
- Los mensajes del admin estarán en español
- Las fechas se guardarán en zona horaria correcta

#### 5.3 Guardar los cambios

Guarda el archivo `config/settings.py` con los dos cambios realizados.

---

### Paso 6: Levantar el Proyecto

#### 6.1 Iniciar los contenedores

Ejecuta en la terminal:

```bash
docker compose up
```

**¿Qué hace este comando?**

- Inicia el contenedor de PostgreSQL (`db`)
- Inicia el contenedor de Django (`web`)
- Muestra los logs de ambos en tiempo real

**✅ Verificación:** Deberías ver mensajes como:

```
db_1   | database system is ready to accept connections
web_1  | Starting development server at http://0.0.0.0:8000/
web_1  | Quit the server with CONTROL-C.
```

**⚠️ Si ves errores:** Revisa la sección de troubleshooting al final de este documento.

#### 6.2 Verificar en el navegador

1. Abre tu navegador web
2. Ve a: **http://localhost:8000**
3. Deberías ver la página de bienvenida de Django con un cohete 🚀

**Aspecto de la página:**

- Fondo azul
- Mensaje: "The install worked successfully! Congratulations!"
- Lista de pasos siguientes

#### 6.3 Detener los contenedores

Para detener los contenedores:

1. En la terminal donde están corriendo, presiona: **Ctrl + C**
2. Espera a que los contenedores se detengan
3. Opcionalmente, ejecuta: `docker compose down` para eliminar los contenedores

---

## 📦 Entregables

Para comprobar que completaste la actividad correctamente, debes entregar:

### 1. Captura de pantalla de la terminal

**Nombre del archivo:** `terminal_docker.png` o `terminal_docker.jpg`

**Debe mostrar:**

- El comando `docker compose up` ejecutado
- Los mensajes de éxito:
  - `database system is ready to accept connections`
  - `Starting development server at http://0.0.0.0:8000/`

**Ejemplo:**

```
Crear captura que incluya la terminal completa con estos mensajes visibles
```

### 2. Captura de pantalla del navegador

**Nombre del archivo:** `navegador_django.png` o `navegador_django.jpg`

**Debe mostrar:**

- La URL: `http://localhost:8000` en la barra de direcciones
- La página de bienvenida de Django
- El mensaje "The install worked successfully!"

### 3. Captura de pantalla de la estructura de archivos

**Nombre del archivo:** `estructura_archivos.png` o `estructura_archivos.jpg`

**Debe mostrar:**

- El explorador de archivos o terminal con el comando `ls -la` o `dir`
- La estructura del proyecto mostrando:
  - `manage.py`
  - Carpeta `config/`
  - Archivo `config/settings.py`

## 📨 Forma de Entrega

**Fecha límite:** Lunes 9 de Marzo de 2026 a las 09:59 PM

**Medio de entrega:** Classroom

**Formato:**

- Crea una carpeta con tu nombre: `Apellido_Nombre_Actividad1`
- Incluye los 3 archivos de evidencia
- Comprime en formato ZIP
- Nombra el archivo: `NoControl_Apellido_Nombre_A1.zip`

**Ejemplo:**

```
19460000_Garcia_Juan_A1.zip
├── terminal_docker.png
├── navegador_django.png
├── estructura_archivos.png
```

---

## 🔧 Troubleshooting (Solución de Problemas)

### Problema 1: "docker: command not found"

**Causa:** Docker Desktop no está instalado o no está en el PATH.

**Solución:**

1. Verifica que Docker Desktop esté instalado
2. Reinicia tu computadora
3. Verifica con: `docker --version`

### Problema 2: "port 8000 is already allocated"

**Causa:** El puerto 8000 ya está en uso por otra aplicación.

**Solución:**

```bash
# Opción 1: Detener el proceso que usa el puerto
# Windows:
netstat -ano | findstr :8000
taskkill /PID [número_del_proceso] /F

# Mac/Linux:
lsof -i :8000
kill -9 [PID]

# Opción 2: Cambiar el puerto en docker-compose.yml
# Cambiar "8000:8000" a "8001:8000"
```

### Problema 3: "no configuration file provided: not found"

**Causa:** Estás ejecutando el comando en la carpeta incorrecta.

**Solución:**

```bash
# Verifica que estás en la carpeta correcta
pwd  # Mac/Linux
cd   # Windows

# Deberías estar en: sistema_prestamos/ o como hayas nombrado tu proyecto
# Verifica que existe docker-compose.yml
ls docker-compose.yml  # Mac/Linux
dir docker-compose.yml  # Windows
```

### Problema 4: "could not translate host name 'db' to address"

**Causa:** El contenedor de Django intenta conectarse a PostgreSQL antes de que esté listo.

**Solución:**

```bash
# Detén los contenedores
docker compose down

# Vuelve a iniciarlos
docker compose up
```

### Problema 5: "django.db.utils.OperationalError: could not connect to server"

**Causa:** La configuración de DATABASES en settings.py no coincide con docker-compose.yml.

**Solución:**

1. Verifica que los valores en `settings.py` sean:
   - NAME: 'prestamos_db'
   - USER: 'prestamos_user'
   - PASSWORD: 'prestamos_password'
   - HOST: 'db'
   - PORT: '5432'

2. Verifica que coincidan con `docker-compose.yml`:

```yaml
environment:
  - POSTGRES_DB=prestamos_db
  - POSTGRES_USER=prestamos_user
  - POSTGRES_PASSWORD=prestamos_password
```

### Problema 6: No veo la página de Django en el navegador

**Solución:**

1. Verifica que los contenedores estén corriendo:

   ```bash
   docker compose ps
   ```

   Deberías ver ambos servicios con estado "Up"

2. Verifica los logs:

   ```bash
   docker compose logs web
   ```

   Busca el mensaje: "Starting development server at"

3. Prueba con:
   - http://localhost:8000
   - http://127.0.0.1:8000

---

## 📚 Recursos Adicionales

Si quieres profundizar:

- [Documentación oficial de Django](https://docs.djangoproject.com/es/5.0/)
- [Tutorial de Docker Compose](https://docs.docker.com/compose/gettingstarted/)
- [Guía de PostgreSQL](https://www.postgresql.org/docs/15/index.html)

---

## 📊 Criterios de Evaluación

Tu actividad será evaluada con los siguientes criterios:

| Criterio                    | Puntos | Descripción                                          |
| --------------------------- | ------ | ---------------------------------------------------- |
| **Evidencia de terminal**   | 30%    | Captura clara mostrando `docker compose up` exitoso  |
| **Evidencia del navegador** | 30%    | Captura mostrando página de Django en localhost:8000 |
| **Estructura de archivos**  | 30%    | Captura mostrando manage.py y carpeta config/        |
| **Formato de entrega**      | 10%    | Archivos nombrados correctamente, entrega en ZIP     |

**Total:** 100 puntos

---
