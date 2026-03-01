# Guía de Instalación de Docker

Esta guía te ayudará a instalar Docker Desktop en Windows 11 y macOS para el taller de Django.

## Tabla de Contenidos

- [Instalación en Windows 11](#instalación-en-windows-11)
- [Instalación en macOS](#instalación-en-macos)
- [Verificación de la Instalación](#verificación-de-la-instalación)
- [Primeros Pasos](#primeros-pasos)

---

## Instalación en Windows 11

### Requisitos Previos

- **Sistema Operativo**: Windows 11 64-bit
- **Hardware**: Virtualización habilitada en BIOS
- **RAM**: Mínimo 4GB (recomendado 8GB o más)
- **Espacio en disco**: Mínimo 20GB disponibles

### Paso 1: Habilitar WSL 2 (Windows Subsystem for Linux)

Docker Desktop en Windows utiliza WSL 2 como backend.

1. Abre **PowerShell como Administrador** (clic derecho en el menú Inicio → "Windows PowerShell (Admin)")

2. Ejecuta el siguiente comando para instalar WSL:

   ```powershell
   wsl --install
   ```

3. Este comando hará lo siguiente:
   - Habilitar la característica opcional WSL
   - Descargar e instalar el kernel de Linux más reciente
   - Establecer WSL 2 como versión predeterminada
   - Descargar e instalar Ubuntu (distribución predeterminada)

4. **Reinicia tu computadora** cuando se te solicite.

5. Después del reinicio, abre PowerShell nuevamente y verifica la instalación:
   ```powershell
   wsl --version
   ```

### Paso 2: Descargar Docker Desktop

1. Visita la página oficial de Docker:
   [https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)

2. Haz clic en **"Download for Windows"**

3. Se descargará el archivo `Docker Desktop Installer.exe`

### Paso 3: Instalar Docker Desktop

1. Ejecuta el instalador `Docker Desktop Installer.exe` que descargaste

2. En la ventana de configuración, asegúrate de que estén marcadas las siguientes opciones:
   - ✅ **Use WSL 2 instead of Hyper-V** (recomendado)
   - ✅ **Add shortcut to desktop** (opcional)

3. Haz clic en **"Ok"** para continuar

4. Espera a que se complete la instalación (puede tomar varios minutos)

5. Haz clic en **"Close and restart"** cuando termine

### Paso 4: Iniciar Docker Desktop

1. Después del reinicio, busca **"Docker Desktop"** en el menú Inicio y ábrelo

2. Acepta los términos del servicio si aparecen

3. Puedes omitir el registro de cuenta por ahora (opcional)

4. Espera a que Docker Desktop inicie completamente. Verás un ícono de Docker en la bandeja del sistema cuando esté listo

### Paso 5: Configuración Recomendada

1. Haz clic en el ícono de Docker en la bandeja del sistema

2. Selecciona **Settings** (⚙️)

3. En la sección **Resources**:
   - **Memory**: Asigna al menos 4GB (recomendado 6-8GB)
   - **CPUs**: Asigna al menos 2 CPUs
   - **Disk image size**: Al menos 60GB

4. Haz clic en **"Apply & Restart"**

---

## Instalación en macOS

### Requisitos Previos

- **Sistema Operativo**: macOS 11 (Big Sur) o superior
- **Hardware**:
  - Para **Mac con chip Apple (M1/M2/M3)**: Chip Apple Silicon
  - Para **Mac con Intel**: Procesador Intel de 64 bits
- **RAM**: Mínimo 4GB (recomendado 8GB o más)
- **Espacio en disco**: Mínimo 20GB disponibles

### Paso 1: Identificar tu tipo de Mac

1. Haz clic en el menú (Apple) en la esquina superior izquierda

2. Selecciona **"About This Mac"** o **"Acerca de este Mac"**

3. Verifica el tipo de procesador:
   - Si dice **"Chip Apple M1"**, **"M2"** o **"M3"**: Tienes un Mac con Apple Silicon
   - Si dice **"Intel Core"**: Tienes un Mac con procesador Intel

### Paso 2: Descargar Docker Desktop

1. Visita la página oficial de Docker:
   [https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)

2. Haz clic en **"Download for Mac"**

3. Selecciona la versión correcta según tu procesador:
   - **Mac with Apple chip**: Para M1/M2/M3
   - **Mac with Intel chip**: Para procesadores Intel

4. Se descargará el archivo `Docker.dmg`

### Paso 3: Instalar Docker Desktop

1. Abre el archivo `Docker.dmg` que descargaste

2. Arrastra el ícono de **Docker** a la carpeta **Applications**

3. Abre **Finder** → **Applications**

4. Busca y haz doble clic en **Docker**

5. macOS puede mostrar un mensaje de seguridad. Si aparece:
   - Ve a **System Preferences** → **Security & Privacy**
   - Haz clic en **"Open Anyway"** para Docker
   - O haz clic derecho en Docker.app y selecciona **"Open"**

### Paso 4: Configurar Docker Desktop

1. Docker Desktop se iniciará y pedirá permisos privilegiados

2. Ingresa tu contraseña de macOS cuando se solicite

3. Acepta los términos del servicio

4. Puedes omitir el registro de cuenta (es opcional)

5. Espera a que Docker Desktop complete la inicialización. Verás el ícono de Docker en la barra de menú superior cuando esté listo

### Paso 5: Configuración Recomendada

1. Haz clic en el ícono de Docker en la barra de menú superior

2. Selecciona **Preferences** o **Settings** (⚙️)

3. En la sección **Resources**:
   - **Memory**: Asigna al menos 4GB (recomendado 6-8GB)
   - **CPUs**: Asigna al menos 2 CPUs
   - **Disk image size**: Al menos 60GB

4. Haz clic en **"Apply & Restart"**

---

## Verificación de la Instalación

Una vez completada la instalación en cualquier sistema operativo, verifica que Docker esté funcionando correctamente.

### Abrir Terminal

- **Windows**: Abre **PowerShell** o **Command Prompt**
- **macOS**: Abre **Terminal** (puedes encontrarla en Applications → Utilities)

### Ejecutar Comandos de Verificación

1. **Verificar la versión de Docker**:

   ```bash
   docker --version
   ```

   Deberías ver algo como: `Docker version 24.x.x, build xxxxx`

2. **Verificar la versión de Docker Compose**:

   ```bash
   docker compose version
   ```

   Deberías ver algo como: `Docker Compose version v2.x.x`

3. **Ejecutar un contenedor de prueba**:

   ```bash
   docker run hello-world
   ```

   Este comando:
   - Descarga la imagen `hello-world` si no existe localmente
   - Crea un contenedor desde esa imagen
   - Ejecuta el contenedor
   - Muestra un mensaje de confirmación

   Si ves un mensaje que comienza con **"Hello from Docker!"**, ¡la instalación fue exitosa! 🎉

4. **Verificar que Docker está corriendo**:
   ```bash
   docker ps
   ```
   Este comando muestra los contenedores en ejecución. Inicialmente estará vacío.

---

## Primeros Pasos

### Comandos Básicos de Docker

Aquí algunos comandos útiles para comenzar:

```bash
# Ver todas las imágenes descargadas
docker images

# Ver todos los contenedores (incluyendo los detenidos)
docker ps -a

# Eliminar un contenedor
docker rm <container_id>

# Eliminar una imagen
docker rmi <image_name>

# Detener un contenedor en ejecución
docker stop <container_id>

# Iniciar un contenedor detenido
docker start <container_id>

# Ver logs de un contenedor
docker logs <container_id>
```

### Preparación para el Taller de Django

Para el taller de Django, estaremos utilizando Docker para:

1. **Base de datos PostgreSQL**: Ejecutaremos PostgreSQL en un contenedor
2. **Python y Django**: Utilizaremos un contenedor con Python para el desarrollo

No es necesario instalar PostgreSQL, Python o Django directamente en tu sistema. Todo se ejecutará dentro de contenedores Docker.

### Próximos Pasos

En las siguientes guías del taller aprenderás a:

- Crear un archivo `Dockerfile` para tu aplicación Django
- Configurar `docker-compose.yml` para orquestar múltiples servicios
- Conectar Django con PostgreSQL usando Docker
- Desarrollar y probar tu aplicación web

---

## Solución de Problemas Comunes

### Windows 11

**Error: "WSL 2 installation is incomplete"**

- Solución: Ejecuta `wsl --update` en PowerShell como administrador y reinicia

**Error: "Hardware assisted virtualization and data execution protection must be enabled in the BIOS"**

- Solución: Reinicia tu PC, entra al BIOS (generalmente con F2, F10 o DEL) y habilita VT-x o AMD-V

**Docker Desktop no inicia**

- Solución: Verifica que el servicio de Docker esté corriendo:
  ```powershell
  Get-Service -Name "com.docker.service"
  ```

### macOS

**Error: "Docker.app is damaged and can't be opened"**

- Solución: Abre Terminal y ejecuta:
  ```bash
  xattr -d com.apple.quarantine /Applications/Docker.app
  ```

**Docker se ejecuta lento en Mac con Intel**

- Solución: Asegúrate de haber asignado suficiente memoria y CPUs en las preferencias

**No puedes abrir Docker por restricciones de seguridad**

- Solución: Ve a System Preferences → Security & Privacy y permite la aplicación

---

## Recursos Adicionales

- [Documentación oficial de Docker](https://docs.docker.com/)
- [Docker Hub](https://hub.docker.com/) - Repositorio de imágenes de Docker
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Docker for Django Tutorial](https://docs.docker.com/samples/django/)

---

## Soporte

Si encuentras problemas durante la instalación que no se cubren en esta guía:

1. Consulta la [documentación oficial de Docker](https://docs.docker.com/get-docker/)
2. Revisa los [foros de la comunidad Docker](https://forums.docker.com/)
3. Contacta al instructor del taller

---
