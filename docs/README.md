# Documentación del Sistema de Préstamos

Índice completo de la documentación del proyecto.

## 📖 Guías de Usuario

### Instalación y Configuración

1. **[Guía de Instalación de Docker](GUIA_INSTALACION_DOCKER.md)**
   - ✅ Instalación en Windows 11 (con WSL 2)
   - ✅ Instalación en macOS (Apple Silicon e Intel)
   - ✅ Verificación de instalación
   - ✅ Solución de problemas comunes

2. **[Guía de Docker Compose y Django](GUIA_DOCKER_COMPOSE_DJANGO.md)**
   - ✅ Creación del Dockerfile para Django
   - ✅ Configuración de docker-compose.yml
   - ✅ Archivo requirements.txt
   - ✅ Variables de entorno (.env)
   - ✅ Configuración de Django con PostgreSQL
   - ✅ Comandos útiles de Docker Compose
   - ✅ Script de inicialización (entrypoint.sh)

## 📋 Caso de Estudio

3. **[Caso de Estudio Completo](caso_estudio_prestamos.md)**
   - Descripción del negocio de Central Informática
   - Reglas de negocio para préstamos
   - Catálogos base (Puestos, Empleados)
   - Datos de ejemplo completos
   - Requerimientos funcionales (A-P)
   - Formatos de reportes esperados

## 🏗️ Modelado del Sistema

4. **[Modelado Completo del Sistema](MODELADO_SISTEMA_PRESTAMOS.md)**
   - Introducción y reglas de negocio
   - Procesos de negocio
   - Casos de uso
   - Requisitos funcionales y no funcionales
   - Modelo de clases
   - Modelo de datos
   - Validaciones y restricciones

## 📊 Diagramas PlantUML

### Diagramas de Procesos

5. **[Diagrama de Procesos de Negocio](diagrama_procesos.puml)**
   - Proceso de gestión de empleados
   - Proceso de solicitud y aprobación de préstamos
   - Proceso de gestión de abonos
   - Proceso de generación de reportes

### Diagramas de Análisis

6. **[Diagrama de Casos de Uso](diagrama_casos_uso.puml)**
   - Actores del sistema
   - Casos de uso principales
   - Relaciones include/extend
   - Validaciones y cálculos

### Diagramas de Diseño

7. **[Diagrama de Clases](diagrama_clases.puml)**
   - Clases del dominio
   - Atributos y métodos
   - Relaciones entre clases
   - Enumeraciones
   - Notas de implementación

8. **[Diagrama Entidad-Relación](diagrama_entidad_relacion.puml)**
   - Tablas de PostgreSQL
   - Tipos de datos
   - Relaciones y cardinalidades
   - Restricciones CHECK
   - Índices

## 🗄️ Base de Datos

9. **[Diccionario de Datos Completo](DICCIONARIO_DATOS.md)**
   - Tabla: puestos
   - Tabla: empleados
   - Tabla: historial_puestos
   - Tabla: prestamos
   - Tabla: abonos
   - Índices y optimización
   - Triggers recomendados
   - Vistas útiles
   - Scripts de creación
   - Mantenimiento y respaldo

10. **[Script de Datos de Prueba](datos_prueba.sql)**
    - 6 puestos de trabajo
    - 5 empleados
    - 6 historial de puestos
    - 6 préstamos (1 concluido, 5 activos)
    - 23 abonos registrados
    - Consultas de verificación

## 📐 Resumen de Arquitectura

### Entidades Principales

```
Puesto ←───────┐
               │
               ├──→ HistorialPuesto ←─── Empleado
               │                           │
Abono ←──── Prestamo ←─────────────────────┘
```

### Tecnologías

- **Framework**: Django 5.0+
- **Lenguaje**: Python 3.11
- **Base de Datos**: PostgreSQL 15
- **ORM**: Django ORM
- **Contenedores**: Docker & Docker Compose
- **Diagramas**: PlantUML

### Módulos del Sistema

1. **Gestión de Catálogos**
   - Puestos
   - Empleados
   - Historial de puestos

2. **Gestión de Préstamos**
   - Solicitudes
   - Aprobaciones
   - Validaciones de negocio

3. **Gestión de Abonos**
   - Registro de pagos
   - Cálculo de intereses
   - Actualización de saldos

4. **Reportes y Consultas**
   - Historial de préstamos
   - Detalles de abonos
   - Préstamos activos

## 🎯 Requisitos Funcionales

### Catálogo

- **RF-A**: Listar puestos
- **RF-B**: Agregar puesto
- **RF-C**: Listar empleados
- **RF-D**: Agregar empleado
- **RF-I**: Modificar empleado

### Historial

- **RF-E**: Ver historial de puestos
- **RF-F**: Cambiar puesto empleado
- **RF-G**: Ver historial de préstamos

### Préstamos

- **RF-H**: Ver detalles de préstamo
- **RF-J**: Listar todos los préstamos
- **RF-K**: Agregar nuevo préstamo
- **RF-M**: Listar préstamos detallados
- **RF-O**: Historial con estado

### Abonos y Reportes

- **RF-L**: Registrar abono
- **RF-N**: Reporte de préstamo
- **RF-P**: Préstamos activos por fecha

## 🔍 Cómo Navegar esta Documentación

### Para Empezar

1. Lee el [README principal](../README.md)
2. Revisa el [Caso de Estudio](caso_estudio_prestamos.md)
3. Sigue la [Guía de Instalación Docker](GUIA_INSTALACION_DOCKER.md)

### Para Desarrollar

1. Estudia el [Modelado del Sistema](MODELADO_SISTEMA_PRESTAMOS.md)
2. Revisa los diagramas PlantUML
3. Consulta el [Diccionario de Datos](DICCIONARIO_DATOS.md)
4. Sigue la [Guía de Docker Compose](GUIA_DOCKER_COMPOSE_DJANGO.md)

### Para Implementar la Base de Datos

1. Revisa el [Diagrama ER](diagrama_entidad_relacion.puml)
2. Consulta el [Diccionario de Datos](DICCIONARIO_DATOS.md)
3. Ejecuta el [Script de Datos de Prueba](datos_prueba.sql)

## 📝 Visualizar Diagramas PlantUML

### En VS Code

Instala la extensión **PlantUML** y abre los archivos `.puml`

### Online

1. Ve a [PlantUML Online Server](http://www.plantuml.com/plantuml/uml/)
2. Copia el contenido del archivo `.puml`
3. Pega y visualiza

### Exportar a Imagen

```bash
# Instalar PlantUML
npm install -g node-plantuml

# Generar PNG
puml generate diagrama_clases.puml -o diagrama_clases.png

# O usar Docker
docker run -v $(pwd):/data plantuml/plantuml diagrama_clases.puml
```

## 🔄 Actualizaciones

| Fecha      | Versión | Cambios                        |
| ---------- | ------- | ------------------------------ |
| 2026-02-25 | 1.0     | Documentación inicial completa |

## 📚 Próximos Pasos

1. ⏳ Implementar modelos Django
2. ⏳ Crear vistas y templates
3. ⏳ Desarrollar API REST (opcional)
4. ⏳ Implementar tests unitarios
5. ⏳ Configurar CI/CD
6. ⏳ Guía de despliegue en producción

---

**📧 Contacto**: Para dudas sobre el taller o la documentación  
**🔗 Repositorio**: [Ver en GitHub](#)  
**📅 Última actualización**: 25 de febrero de 2026
