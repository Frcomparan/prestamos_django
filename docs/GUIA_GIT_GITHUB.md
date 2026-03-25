# Guía Rápida de Git y GitHub

Esta guía te ayudará a dominar los conceptos básicos del control de versiones con Git y a conectar tus proyectos locales con repositorios en la nube usando GitHub.

## Tabla de Contenidos

- [Conceptos Básicos](#conceptos-básicos)
- [Configuración Inicial](#configuración-inicial)
- [El Flujo de Trabajo Básico (Local)](#el-flujo-de-trabajo-básico-local)
- [Manejo de Ramas (Branches)](#manejo-de-ramas-branches)
- [Conexión con GitHub (Remoto)](#conexión-con-github-remoto)
- [Solución de Problemas Comunes](#solución-de-problemas-comunes)
- [Recursos Adicionales](#recursos-adicionales)

---

## Conceptos Básicos

Antes de empezar, es importante entender la diferencia:
* **Git**: Es la herramienta (el motor) que instalas en tu computadora para rastrear los cambios en tu código a lo largo del tiempo.
* **GitHub**: Es una plataforma en línea (la nube) que aloja tus repositorios de Git para que puedas tener respaldos, compartir tu código y colaborar con otros.

---

## Configuración Inicial

Si es la primera vez que usas Git en tu computadora, necesitas configurarlo con tu nombre y correo (debe ser el mismo correo que uses para tu cuenta de GitHub).

Abre tu terminal (o Git Bash en Windows) y ejecuta:

```bash
# Configura tu nombre
git config --global user.name "Tu Nombre o Nickname"

# Configura tu correo electrónico
git config --global user.email "tu_correo@ejemplo.com"

# Verifica tu configuración
git config --list
```

---

## El Flujo de Trabajo Básico (Local)

### 1. Iniciar un Repositorio

Para que Git empiece a rastrear un proyecto, debes inicializarlo. Navega a la carpeta de tu proyecto en la terminal y ejecuta:

```bash
# Inicializa el repositorio en la carpeta actual
git init
```

### 2. Revisar el Estado

El comando más utilizado en Git. Te dirá qué archivos han sido modificados, cuáles están listos para guardarse y cuáles no están siendo rastreados.

```bash
git status
```

### 3. Preparar Cambios (Stage)

Antes de guardar un cambio, debes moverlo al "área de preparación" (Stage). 

```bash
# Preparar un archivo específico
git add index.html

# Preparar TODOS los archivos modificados y nuevos (lo más común)
git add .
```

### 4. Guardar Cambios (Commit)

Un *commit* es como tomar una "fotografía" del estado actual de tu proyecto. Siempre debe llevar un mensaje claro y descriptivo.

```bash
git commit -m "Añade estructura básica del HTML y estilos iniciales"
```

### 5. Ver el Historial

Para ver la lista de *commits* (fotografías) que has hecho a lo largo del tiempo:

```bash
# Muestra el historial completo
git log

# Muestra un historial resumido en una sola línea por commit
git log --oneline
```

---

## Manejo de Ramas (Branches)

Las ramas te permiten trabajar en nuevas características o experimentar sin afectar el código principal (generalmente llamado `main` o `master`).

### Comandos de Ramas

```bash
# Ver todas las ramas locales (la rama con un * es la actual)
git branch

# Crear una nueva rama
git branch nombre-de-la-rama

# Cambiarte a una rama existente
git checkout nombre-de-la-rama
# Nota: En versiones recientes de Git, también puedes usar: git switch nombre-de-la-rama

# Crear una nueva rama y cambiarte a ella en un solo paso
git checkout -b nueva-caracteristica

# Fusionar (Merge): Une los cambios de otra rama a la rama en la que estás actualmente
# Ejemplo: Estando en 'main', quieres traer los cambios de 'nueva-caracteristica'
git merge nueva-caracteristica

# Eliminar una rama que ya no necesitas
git branch -d nombre-de-la-rama
```

---

## Conexión con GitHub (Remoto)

Esta es la parte crucial para subir tu código local a la nube.

### Paso 1: Crear el repositorio en GitHub
1. Ve a [GitHub](https://github.com/) e inicia sesión.
2. Haz clic en el botón **"New"** (Nuevo repositorio).
3. Ponle un nombre, déjalo público o privado, y **NO** marques la casilla "Add a README file" (para que el repositorio nazca completamente vacío).
4. Haz clic en **"Create repository"**.

### Paso 2: Vincular y Subir tu Código Local

GitHub te mostrará unas instrucciones. Los comandos clave que debes ejecutar en tu terminal local son:

```bash
# 1. Renombrar tu rama principal a 'main' (por convención actual)
git branch -M main

# 2. Vincular tu repo local con el de GitHub (cambia la URL por la tuya)
git remote add origin [https://github.com/tu-usuario/nombre-del-repo.git](https://github.com/tu-usuario/nombre-del-repo.git)

# 3. Subir tu código a GitHub por primera vez
git push -u origin main
```
*Nota: La bandera `-u` solo se usa la primera vez para establecer la conexión. En el futuro, solo necesitarás escribir `git push`.*

### Descargar Cambios de GitHub (Pull)

Si hiciste cambios directamente en GitHub o estás trabajando en equipo, necesitas descargar esos cambios a tu computadora local:

```bash
# Descarga e integra los cambios del remoto a tu rama local
git pull origin main
```

### Clonar un Repositorio Existente

Si quieres descargar un proyecto de GitHub a tu computadora por primera vez (no necesitas hacer `git init` en este caso):

```bash
git clone [https://github.com/usuario/repo.git](https://github.com/usuario/repo.git)
```

---

## Solución de Problemas Comunes

**Error: "Updates were rejected because the remote contains work that you do not have locally"**
* **Causa**: Alguien más (o tú mismo desde otra PC) subió cambios a GitHub y tu repositorio local está desactualizado.
* **Solución**: Descarga los cambios primero antes de intentar subir los tuyos.
  ```bash
  git pull origin main
  git push origin main
  ```

**Error: "fatal: refusing to merge unrelated histories"**
* **Causa**: Intentas hacer un `pull` de un repositorio en GitHub que ya tenía archivos (como un README) hacia un repositorio local que ya tiene sus propios commits, y Git no sabe cómo conectarlos.
* **Solución**: Fuerzalo indicando que sabes que son historias separadas.
  ```bash
  git pull origin main --allow-unrelated-histories
  ```

**Me equivoqué de mensaje en el último commit**
* **Solución**: Puedes reescribir el mensaje del *último* commit fácilmente (siempre y cuando no le hayas hecho `push` todavía).
  ```bash
  git commit --amend -m "Nuevo mensaje corregido"
  ```

**Ignorar archivos (.gitignore)**
Nunca debes subir carpetas como `node_modules/`, entornos virtuales de Python o archivos `.env`. 
* **Solución**: Crea un archivo llamado `.gitignore` en la raíz de tu proyecto y escribe dentro los nombres de los archivos o carpetas que Git debe ignorar por completo.

---

## Comandos de referencia rápida

### Configuración

```bash
git config --global user.name "Tu Nombre"
git config --global user.email "tu_correo@ejemplo.com"
```

### Crear repositorio local

```bash
git init
```

### Estado del repositorio

```bash
git status
```

### Agregar cambios

```bash
git add .
```

### Crear commit

```bash
git commit -m "Mensaje del commit"
```

### Ver historial

```bash
git log --oneline
```

### Trabajar con ramas

```bash
git branch
git checkout -b nueva-rama
git checkout main
git merge nueva-rama
```

### Conectar con GitHub

```bash
git remote add origin URL_DEL_REPOSITORIO
git remote -v
```

### Subir cambios

```bash
git push -u origin main
git push
```

### Descargar cambios

```bash
git pull
```

---

## Buenas prácticas

* Escribir mensajes de commit claros y breves.
* Hacer commits pequeños y frecuentes.
* Revisar `git status` antes de hacer commit.
* Usar ramas para nuevas funcionalidades o pruebas.
* Hacer `pull` antes de comenzar a trabajar si el repositorio es compartido.
* No subir archivos innecesarios o sensibles al repositorio.

---


## Recursos Adicionales

- [Documentación oficial de Git](https://git-scm.com/doc)
- [GitHub Skills](https://skills.github.com/) - Cursos interactivos gratuitos.
- [Aprende Git Branching](https://learngitbranching.js.org/?locale=es_ES) - Un excelente juego visual para entender cómo funcionan las ramas en Git.


