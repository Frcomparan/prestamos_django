# Modelado del Sistema de Préstamos - Central Informática

Este documento contiene el análisis y modelado completo del Sistema de Gestión de Préstamos para la caja de ahorros de Central Informática.

## Tabla de Contenidos

- [1. Introducción](#1-introducción)
- [2. Procesos de Negocio](#2-procesos-de-negocio)
- [3. Casos de Uso](#3-casos-de-uso)
- [4. Requisitos Funcionales](#4-requisitos-funcionales)
- [5. Modelo de Clases](#5-modelo-de-clases)
- [6. Modelo de Datos](#6-modelo-de-datos)
- [7. Diccionario de Datos](#7-diccionario-de-datos)

---

## 1. Introducción

### 1.1 Descripción del Sistema

El Sistema es una aplicación web desarrollada en Django que administra la caja de ahorros de los empleados. El sistema permite:

- Gestionar empleados y sus puestos de trabajo
- Procesar solicitudes de préstamos
- Calcular y registrar abonos mensuales
- Generar reportes de préstamos y pagos

### 1.2 Reglas de Negocio

#### Requisitos para Solicitar un Préstamo

1. **Antigüedad Mínima**: El empleado debe tener al menos 1 año de antigüedad
2. **Monto Máximo**: No puede superar 6 meses del sueldo actual del empleado
3. **Préstamos Simultáneos**: No debe tener ningún préstamo vigente (activo)

#### Condiciones Financieras

1. **Tasa de Interés**: 1% mensual sobre saldos insolutos
2. **Plazo Máximo**: 24 meses
3. **Cálculo de Intereses**:
   - Interés mensual = Saldo actual × 0.01
   - Pago total = Pago a capital + Interés
   - Nuevo saldo = Saldo anterior - Pago a capital

#### Fórmulas de Cálculo

```
Pago fijo a capital = Monto del préstamo / Plazo en meses
Interés del mes = Saldo insoluto × Tasa de interés (0.01)
Monto cobrado = Pago a capital + Interés del mes
Nuevo saldo = Saldo anterior - Pago a capital
```

### 1.3 Actores del Sistema

- **Empleado**: Usuario que solicita préstamos y realiza pagos
- **Administrador de Recursos Humanos**: Gestiona empleados y puestos
- **Administrador de Préstamos**: Aprueba/rechaza solicitudes y registra abonos
- **Consultor de Reportes**: Genera y consulta reportes del sistema

---

## 2. Procesos de Negocio

### 2.1 Diagrama de Procesos Principales

![Diagrama de Procesos](/docs/modelado/diagrama_procesos.svg)

Ver archivo: [diagrama_procesos.puml](diagrama_procesos.puml)

### 2.2 Descripción de Procesos

#### Proceso 1: Gestión de Empleados

1. Registro de nuevo empleado
2. Asignación de puesto inicial
3. Cambio de puesto (cuando aplique)
4. Actualización de datos del empleado

#### Proceso 2: Solicitud y Aprobación de Préstamo

1. Validación de requisitos previos
2. Cálculo de monto máximo permitido
3. Registro de solicitud
4. Evaluación y aprobación
5. Cálculo de plan de pagos

#### Proceso 3: Gestión de Abonos

1. Generación del calendario de pagos
2. Registro de abono mensual
3. Cálculo de intereses
4. Actualización de saldo
5. Verificación de finalización del préstamo

#### Proceso 4: Generación de Reportes

1. Consulta de historiales
2. Generación de reportes de préstamos
3. Reportes de abonos por periodo
4. Análisis de préstamos activos

---

## 3. Casos de Uso

### 3.1 Diagrama de Casos de Uso

![Diagrama de Casos de Uso](diagrama_casos_uso.puml)

Ver archivo: [diagrama_casos_uso.puml](diagrama_casos_uso.puml)

### 3.2 Descripción de Casos de Uso

#### CU-01: Gestionar Puestos

- **Actor**: Administrador RH
- **Descripción**: Permite listar y agregar nuevos puestos de trabajo
- **Precondiciones**: Usuario autenticado como administrador
- **Flujo Principal**:
  1. El administrador accede al módulo de puestos
  2. Puede ver listado de puestos existentes
  3. Puede agregar nuevo puesto con nombre y sueldo
- **Postcondiciones**: Puesto registrado en el sistema

#### CU-02: Gestionar Empleados

- **Actor**: Administrador RH
- **Descripción**: Administrar empleados y sus datos
- **Incluye**: Listar empleados, agregar empleado, modificar empleado

#### CU-03: Gestionar Historial de Puestos

- **Actor**: Administrador RH
- **Descripción**: Ver y actualizar historial de puestos de empleados
- **Incluye**: Ver historial, cambiar puesto

#### CU-04: Solicitar Préstamo

- **Actor**: Empleado
- **Descripción**: Crear solicitud de préstamo
- **Precondiciones**: Empleado cumple requisitos
- **Validaciones**:
  - Antigüedad >= 1 año
  - Monto <= 6 meses de sueldo
  - Sin préstamos activos

#### CU-05: Aprobar Préstamo

- **Actor**: Administrador de Préstamos
- **Descripción**: Evaluar y aprobar/rechazar solicitud

#### CU-06: Registrar Abono

- **Actor**: Administrador de Préstamos
- **Descripción**: Registrar pago mensual de préstamo
- **Cálculos**:
  - Interés del mes
  - Monto total cobrado
  - Nuevo saldo

#### CU-07: Consultar Historial de Préstamos

- **Actor**: Empleado, Administrador
- **Descripción**: Ver préstamos de un empleado

#### CU-08: Generar Reportes

- **Actor**: Consultor de Reportes
- **Descripción**: Generar diversos reportes del sistema

---

## 4. Requisitos Funcionales

### 4.1 Módulo de Puestos

| ID   | Requisito                                                | Prioridad |
| ---- | -------------------------------------------------------- | --------- |
| RF | Mostrar listado de todos los puestos con todos sus datos | Alta      |
| RF | Permitir agregar un nuevo puesto                         | Alta      |

### 4.2 Módulo de Empleados

| ID   | Requisito                                                  | Prioridad |
| ---- | ---------------------------------------------------------- | --------- |
| RF | Mostrar listado de todos los empleados con todos sus datos | Alta      |
| RF | Permitir agregar un nuevo empleado                         | Alta      |
| RF | Modificar los datos de un empleado                         | Media     |

### 4.3 Módulo de Historial de Puestos

| ID   | Requisito                                                 | Prioridad |
| ---- | --------------------------------------------------------- | --------- |
| RF | Mostrar el historial de puestos que ha tenido un empleado | Alta      |
| RF | Cambiar de puesto a un empleado                           | Alta      |

### 4.4 Módulo de Préstamos

| ID   | Requisito                                                     | Prioridad |
| ---- | ------------------------------------------------------------- | --------- |
| RF | Mostrar el historial de préstamos de un empleado              | Alta      |
| RF | Mostrar los detalles de cierto préstamo de un empleado        | Alta      |
| RF | Mostrar un listado de todos los préstamos otorgados           | Alta      |
| RF | Permitir agregar un nuevo préstamo                            | Alta      |
| RF | Mostrar listado de préstamos con datos completos              | Alta      |
| RF | Mostrar historial de préstamos con estado y acceso a detalles | Alta      |

### 4.5 Módulo de Abonos

| ID   | Requisito                                                | Prioridad |
| ---- | -------------------------------------------------------- | --------- |
| RF | Permitir agregar un nuevo abono a cierto préstamo        | Alta      |
| RF | Mostrar reporte de préstamo con detalles de abonos       | Alta      |
| RF | Mostrar listado de préstamos activos en fecha específica | Media     |

### 4.6 Requisitos No Funcionales

| ID     | Requisito                                                      | Categoría       |
| ------ | -------------------------------------------------------------- | --------------- |
| RNF | El sistema debe estar disponible 99% del tiempo                | Disponibilidad  |
| RNF | Los cálculos de intereses deben tener precisión de 2 decimales | Precisión       |
| RNF | La interfaz debe ser responsive (móvil, tablet, desktop)       | Usabilidad      |
| RNF | Debe usar PostgreSQL como base de datos                        | Tecnología      |
| RNF | Debe estar desarrollado en Django 5.0+                         | Tecnología      |
| RNF | Debe usar Docker para el despliegue                            | Infraestructura |

---

## 5. Modelo de Clases

### 5.1 Diagrama de Clases

![Diagrama de Clases](diagrama_clases.puml)

Ver archivo: [diagrama_clases.puml](diagrama_clases.puml)

### 5.2 Descripción de Clases

#### Clase: Puesto

- **Responsabilidad**: Representar un puesto de trabajo en la empresa
- **Atributos**:
  - `id`: Identificador único
  - `nombre`: Nombre del puesto
  - `sueldo`: Sueldo mensual asociado
- **Métodos**:
  - `__str__()`: Representación del puesto

#### Clase: Empleado

- **Responsabilidad**: Representar un empleado de la empresa
- **Atributos**:
  - `id`: Identificador único
  - `nombre`: Nombre completo
  - `fecha_ingreso`: Fecha de ingreso a la empresa
  - `activo`: Si el empleado está activo
- **Métodos**:
  - `calcular_antiguedad()`: Años de antigüedad
  - `obtener_puesto_actual()`: Puesto actual del empleado
  - `obtener_sueldo_actual()`: Sueldo actual
  - `puede_solicitar_prestamo()`: Valida si puede solicitar préstamo

#### Clase: HistorialPuesto

- **Responsabilidad**: Registrar el historial de puestos de un empleado
- **Atributos**:
  - `id`: Identificador único
  - `empleado`: Referencia al empleado
  - `puesto`: Referencia al puesto
  - `fecha_inicio`: Fecha de inicio en el puesto
  - `fecha_fin`: Fecha de finalización (null si es actual)
- **Métodos**:
  - `es_puesto_actual()`: Verifica si es el puesto actual

#### Clase: Prestamo

- **Responsabilidad**: Gestionar préstamos otorgados
- **Atributos**:
  - `id`: Identificador único
  - `empleado`: Referencia al empleado
  - `monto`: Monto del préstamo
  - `plazo_meses`: Duración en meses
  - `fecha_solicitud`: Fecha de solicitud
  - `fecha_aprobacion`: Fecha de aprobación
  - `tasa_interes_mensual`: Tasa de interés (default 1.0)
  - `pago_fijo_capital`: Pago mensual a capital
  - `fecha_inicio_descuento`: Primera fecha de descuento
  - `fecha_fin_descuento`: Última fecha de descuento
  - `saldo_actual`: Saldo pendiente
  - `estado`: SOLICITADO, APROBADO, ACTIVO, CONCLUIDO, RECHAZADO
- **Métodos**:
  - `calcular_pago_capital()`: Calcula el pago mensual
  - `calcular_monto_maximo_permitido()`: Valida monto máximo
  - `generar_calendario_pagos()`: Genera plan de pagos
  - `esta_concluido()`: Verifica si está pagado

#### Clase: Abono

- **Responsabilidad**: Registrar pagos de préstamos
- **Atributos**:
  - `id`: Identificador único
  - `prestamo`: Referencia al préstamo
  - `numero_abono`: Número secuencial del abono
  - `fecha`: Fecha del pago
  - `monto_capital`: Pago a capital
  - `monto_interes`: Interés cobrado
  - `monto_cobrado`: Total cobrado
  - `saldo_actual`: Saldo después del pago
- **Métodos**:
  - `calcular_interes()`: Calcula el interés del mes
  - `calcular_monto_total()`: Suma capital + interés

---

## 6. Modelo de Datos

### 6.1 Diagrama Entidad-Relación

![Diagrama ER](diagrama_entidad_relacion.puml)

Ver archivo: [diagrama_entidad_relacion.puml](diagrama_entidad_relacion.puml)

### 6.2 Descripción de Relaciones

#### Empleado → Puesto (a través de HistorialPuesto)

- **Cardinalidad**: Un empleado puede tener múltiples puestos a lo largo del tiempo
- **Tipo**: Relación muchos a muchos con historial temporal
- **Restricción**: Solo puede tener un puesto activo (fecha_fin = NULL)

#### Empleado → Prestamo

- **Cardinalidad**: Un empleado puede tener múltiples préstamos
- **Tipo**: Uno a muchos
- **Restricción**: Solo puede tener un préstamo ACTIVO a la vez

#### Prestamo → Abono

- **Cardinalidad**: Un préstamo puede tener múltiples abonos
- **Tipo**: Uno a muchos
- **Restricción**: El número de abonos no debe exceder el plazo_meses

---

## 7. Diccionario de Datos

Ver archivo completo: [DICCIONARIO_DATOS.md](DICCIONARIO_DATOS.md)

### 7.1 Resumen de Tablas

| Tabla             | Descripción                       | Registros Estimados |
| ----------------- | --------------------------------- | ------------------- |
| puestos           | Catálogo de puestos de trabajo    | 10-20               |
| empleados         | Información de empleados          | 100-500             |
| historial_puestos | Historial de puestos por empleado | 200-1000            |
| prestamos         | Préstamos otorgados               | 500-5000            |
| abonos            | Pagos realizados a préstamos      | 5000-50000          |


## 8. Validaciones y Restricciones

### 8.1 Validaciones de Negocio

#### Validación de Solicitud de Préstamo

```python
def validar_solicitud_prestamo(empleado, monto):
    # 1. Validar antigüedad
    if empleado.calcular_antiguedad() < 1:
        raise ValidationError("Requiere mínimo 1 año de antigüedad")

    # 2. Validar monto máximo
    sueldo_actual = empleado.obtener_sueldo_actual()
    monto_maximo = sueldo_actual * 6
    if monto > monto_maximo:
        raise ValidationError(f"Monto máximo permitido: {monto_maximo}")

    # 3. Validar préstamos activos
    prestamos_activos = Prestamo.objects.filter(
        empleado=empleado,
        estado='ACTIVO'
    )
    if prestamos_activos.exists():
        raise ValidationError("Ya tiene un préstamo activo")

    return True
```

### 8.2 Restricciones de Base de Datos

```sql
-- Restricción: Solo un puesto activo por empleado
CREATE UNIQUE INDEX idx_empleado_puesto_activo
ON historial_puestos(empleado_id)
WHERE fecha_fin IS NULL;

-- Restricción: Saldo no puede ser negativo
ALTER TABLE prestamos
ADD CONSTRAINT check_saldo_positivo
CHECK (saldo_actual >= 0);

-- Restricción: Plazo máximo 24 meses
ALTER TABLE prestamos
ADD CONSTRAINT check_plazo_maximo
CHECK (plazo_meses > 0 AND plazo_meses <= 24);

-- Restricción: Monto mayor a 0
ALTER TABLE prestamos
ADD CONSTRAINT check_monto_positivo
CHECK (monto > 0);
```

---

## 9. Próximos Pasos

1. ✅ Modelado completo del sistema
2. ⏳ Implementación de modelos Django
3. ⏳ Desarrollo de vistas y plantillas
4. ⏳ Implementación de lógica de negocio
5. ⏳ Desarrollo de API REST (opcional)
6. ⏳ Pruebas unitarias e integración
7. ⏳ Despliegue con Docker

---

## 10. Referencias

- [Caso de Estudio - Préstamos Central Informática](caso_estudio_prestamos.md)
- [Guía de Instalación Docker](GUIA_INSTALACION_DOCKER.md)
- [Guía Docker Compose para Django](GUIA_DOCKER_COMPOSE_DJANGO.md)
- [Django Documentation](https://docs.djangoproject.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
