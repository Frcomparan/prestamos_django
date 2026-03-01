# Sistema de Gestión de Préstamos - Central Informática

Sistema web desarrollado en Django para la gestión de préstamos de la caja de ahorros de empleados de Central Informática.

## 📋 Descripción

Este proyecto forma parte de un taller de Django donde se implementa un sistema completo de gestión de préstamos que permite:

- **Gestionar empleados y puestos de trabajo**
- **Procesar solicitudes de préstamos** con validaciones de negocio
- **Calcular y registrar abonos mensuales** con cálculo automático de intereses
- **Generar reportes** detallados de préstamos y pagos
- **Mantener historial** de puestos y préstamos por empleado

## 🎯 Caso de Estudio

El sistema se basa en el caso de estudio real de Central Informática, donde:

- Cada mes se descuenta un porcentaje del pago mensual de empleados
- El patrón aporta la misma cantidad
- Los fondos se usan para otorgar préstamos a empleados

### Reglas de Negocio Principales

✅ **Para solicitar un préstamo:**

- Mínimo 1 año de antigüedad
- Monto máximo: 6 meses de sueldo
- Sin préstamos activos vigentes

✅ **Condiciones financieras:**

- Tasa de interés: 1% mensual sobre saldos insolutos
- Plazo máximo: 24 meses
- Descuento mensual automático

📄 Ver detalles completos: [docs/caso_estudio_prestamos.md](docs/caso_estudio_prestamos.md)

## 🏗️ Arquitectura y Tecnologías

### Stack Tecnológico

- **Backend**: Django 5.0+ (Python 3.11)
- **Base de Datos**: PostgreSQL 15
- **Containerización**: Docker & Docker Compose
- **ORM**: Django ORM
- **Frontend**: Django Templates + Bootstrap

### Patrones y Principios

- MVC (Model-View-Controller)
- Django Apps modulares
- Separación de concerns
- Validaciones a nivel de modelo y base de datos

## 📚 Documentación

### Guías de Instalación y Configuración

1. **[Guía de Instalación de Docker](docs/GUIA_INSTALACION_DOCKER.md)**
   - Instalación en Windows 11
   - Instalación en macOS (Apple Silicon e Intel)
   - Verificación y troubleshooting

2. **[Guía de Docker Compose para Django](docs/GUIA_DOCKER_COMPOSE_DJANGO.md)**
   - Creación del Dockerfile
   - Configuración de docker-compose.yml
   - Integración Django + PostgreSQL
   - Variables de entorno
   - Comandos útiles

### Modelado y Análisis

3. **[Modelado del Sistema](docs/MODELADO_SISTEMA_PRESTAMOS.md)**
   - Procesos de negocio
   - Casos de uso
   - Requisitos funcionales y no funcionales
   - Modelo de clases
   - Modelo de datos

4. **[Caso de Estudio Completo](docs/caso_estudio_prestamos.md)**
   - Descripción detallada del negocio
   - Datos de ejemplo
   - Requerimientos funcionales A-P
   - Formatos de reportes

### Diagramas PlantUML

Todos los diagramas están en formato PlantUML para fácil edición:

- **[Diagrama de Procesos de Negocio](docs/diagrama_procesos.puml)**
- **[Diagrama de Casos de Uso](docs/diagrama_casos_uso.puml)**
- **[Diagrama de Clases](docs/diagrama_clases.puml)**
- **[Diagrama Entidad-Relación](docs/diagrama_entidad_relacion.puml)**

### Base de Datos

5. **[Diccionario de Datos](docs/DICCIONARIO_DATOS.md)**
   - Descripción detallada de todas las tablas
   - Tipos de datos para PostgreSQL
   - Restricciones y validaciones
   - Índices y optimizaciones
   - Triggers recomendados
   - Vistas útiles

## 🚀 Inicio Rápido

### Prerrequisitos

- Docker Desktop instalado ([ver guía](docs/GUIA_INSTALACION_DOCKER.md))
- Git
- Editor de código (VS Code recomendado)

### Instalación

```bash
# 1. Clonar el repositorio
git clone <url-del-repositorio>
cd aplicacion_prestamos

# 2. Copiar archivo de variables de entorno
cp .env.example .env

# 3. Construir e iniciar los contenedores
docker compose up --build -d

# 4. Ejecutar migraciones
docker compose exec web python manage.py migrate

# 5. Cargar datos de prueba
docker compose exec web python manage.py loaddata datos_prueba

# 6. Crear superusuario
docker compose exec web python manage.py createsuperuser

# 7. Acceder a la aplicación
# http://localhost:8000
```

### Comandos Útiles

```bash
# Ver logs
docker compose logs -f web

# Detener servicios
docker compose down

# Reiniciar servicios
docker compose restart

# Ejecutar tests
docker compose exec web python manage.py test

# Acceder a la shell de Django
docker compose exec web python manage.py shell

# Acceder a PostgreSQL
docker compose exec db psql -U prestamos_user -d prestamos_db
```

## 📊 Modelo de Datos

### Entidades Principales

```
┌─────────────┐     ┌──────────────────┐     ┌──────────┐
│  Empleado   │────<│ HistorialPuesto  │>────│  Puesto  │
└─────────────┘     └──────────────────┘     └──────────┘
       │
       │ 1:N
       │
       ▼
┌─────────────┐
│  Prestamo   │
└─────────────┘
       │
       │ 1:N
       │
       ▼
┌─────────────┐
│    Abono    │
└─────────────┘
```

## 🎓 Contenido del Taller

### Sesión 1: Fundamentos

- ✅ Instalación de Docker
- ✅ Configuración de Django + PostgreSQL
- ✅ Modelado del sistema
- ⏳ Creación de modelos Django

### Sesión 2: Desarrollo Backend

- ⏳ Implementación de modelos
- ⏳ Validaciones de negocio
- ⏳ API con Django REST Framework (opcional)
- ⏳ Tests unitarios

### Sesión 3: Frontend y Reportes

- ⏳ Templates y vistas
- ⏳ Formularios
- ⏳ Generación de reportes
- ⏳ Interfaz de usuario

### Sesión 4: Despliegue

- ⏳ Configuración para producción
- ⏳ Despliegue en cloud (opcional)

## 📋 Requisitos Funcionales

El sistema debe cumplir con los siguientes requisitos (según caso de estudio):

### Gestión de Catálogos

- [x] RF: Listar todos los puestos
- [x] RF: Agregar nuevo puesto
- [x] RF: Listar todos los empleados
- [x] RF: Agregar nuevo empleado
- [x] RF: Modificar datos de empleado

### Gestión de Historial

- [x] RF: Ver historial de puestos de un empleado
- [x] RF: Cambiar puesto de un empleado
- [x] RF: Ver historial de préstamos de un empleado

### Gestión de Préstamos

- [x] RF: Ver detalles de cierto préstamo
- [x] RF: Listar todos los préstamos otorgados
- [x] RF: Agregar nuevo préstamo
- [x] RF: Listar préstamos con datos detallados
- [x] RF: Historial de préstamos con estado

### Gestión de Abonos y Reportes

- [x] RF: Registrar nuevo abono
- [x] RF: Reporte de préstamo con abonos
- [x] RF: Préstamos activos por fecha

> ✅ Modelado completo | ⏳ Implementación pendiente

## 🔧 Configuración de Desarrollo

### Variables de Entorno (.env)

```env
# Django
DEBUG=True
SECRET_KEY=tu-clave-secreta-aqui
ALLOWED_HOSTS=localhost,127.0.0.1

# PostgreSQL
POSTGRES_DB=prestamos_db
POSTGRES_USER=prestamos_user
POSTGRES_PASSWORD=prestamos_password
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

### Estructura del Proyecto (Planeada)

```
aplicacion_prestamos/
├── docker-compose.yml
├── Dockerfile
├── .env
├── .dockerignore
├── requirements.txt
├── manage.py
├── README.md
│
├── docs/                              # Documentación
│   ├── GUIA_INSTALACION_DOCKER.md
│   ├── GUIA_DOCKER_COMPOSE_DJANGO.md
│   ├── MODELADO_SISTEMA_PRESTAMOS.md
│   ├── DICCIONARIO_DATOS.md
│   ├── caso_estudio_prestamos.md
│   ├── diagrama_*.puml
│   └── datos_prueba.sql
│
├── config/                            # Configuración Django
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── apps/                              # Aplicaciones Django
│   ├── empleados/                     # App de empleados
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── tests.py
│   │
│   ├── prestamos/                     # App de préstamos
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── tests.py
│   │
│   └── reportes/                      # App de reportes
│       ├── views.py
│       └── urls.py
│
└── templates/                         # Templates HTML
    └── base.html
```


## 📝 Contribuir al Taller

Este proyecto es parte de un taller educativo. Las contribuciones son bienvenidas:

1. Fork del repositorio
2. Crear rama feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit de cambios (`git commit -am 'Agregar funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

## 📖 Recursos Adicionales

### Documentación Oficial

- [Django Documentation](https://docs.djangoproject.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Docker Documentation](https://docs.docker.com/)
- [PlantUML Guide](https://plantuml.com/)

### Tutoriales Relacionados

- [Django for Beginners](https://djangoforbeginners.com/)
- [Two Scoops of Django](https://www.feldroy.com/books/two-scoops-of-django-3-x)
- [Real Python - Django Tutorials](https://realpython.com/tutorials/django/)

## 📄 Licencia

Este proyecto es material educativo para el taller de Django.
