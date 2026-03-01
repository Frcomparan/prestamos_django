# Diccionario de Datos - Sistema de Préstamos

**Base de Datos:** PostgreSQL 15+  
**Esquema:** public  
**Charset:** UTF-8  
**Fecha de creación:** $(date)

---

## Tabla de Contenidos

1. [Resumen de Tablas](#resumen-de-tablas)
2. [Tabla: puestos](#tabla-puestos)
3. [Tabla: empleados](#tabla-empleados)
4. [Tabla: historial_puestos](#tabla-historial_puestos)
5. [Tabla: prestamos](#tabla-prestamos)
6. [Tabla: abonos](#tabla-abonos)
7. [Índices](#índices)
8. [Restricciones y Triggers](#restricciones-y-triggers)
9. [Vistas Recomendadas](#vistas-recomendadas)
10. [Scripts SQL](#scripts-sql)

---

## Resumen de Tablas

| Tabla             | Descripción                    | Registros Estimados | Tamaño Estimado |
| ----------------- | ------------------------------ | ------------------- | --------------- |
| puestos           | Catálogo de puestos de trabajo | 10-20               | < 1 MB          |
| empleados         | Información de empleados       | 100-500             | < 5 MB          |
| historial_puestos | Historial temporal de puestos  | 200-1,000           | < 10 MB         |
| prestamos         | Préstamos otorgados            | 500-5,000           | < 50 MB         |
| abonos            | Pagos realizados a préstamos   | 5,000-50,000        | < 100 MB        |

**Total estimado:** < 166 MB

---

## Tabla: puestos

### Descripción

Catálogo de puestos de trabajo disponibles con sus respectivos sueldos mensuales.

### Estructura

| Columna | Tipo          | Nulo | Default   | Descripción                         |
| ------- | ------------- | ---- | --------- | ----------------------------------- |
| **id**  | SERIAL        | NO   | nextval() | Identificador único del puesto (PK) |
| nombre  | VARCHAR(100)  | NO   | -         | Nombre del puesto de trabajo        |
| sueldo  | NUMERIC(10,2) | NO   | -         | Sueldo mensual en pesos mexicanos   |

### Restricciones

| Tipo        | Nombre                | Descripción |
| ----------- | --------------------- | ----------- |
| PRIMARY KEY | puestos_pkey          | id          |
| UNIQUE      | puestos_nombre_unique | nombre      |
| CHECK       | puestos_sueldo_check  | sueldo > 0  |

### Ejemplo de Datos

```sql
INSERT INTO puestos (nombre, sueldo) VALUES
('PROGRAMADOR JR', 16000.00),
('BECARIO', 10000.00),
('PROGRAMADOR MASTER', 60000.00),
('PROGRAMADOR SENIOR', 40000.00),
('ARQUITECTO DE SOFTWARE', 50000.00),
('ADMINISTRADOR DE INFRAESTRUCTURA', 55000.00);
```

---

## Tabla: empleados

### Descripción

Información personal y laboral de los empleados.

### Estructura

| Columna       | Tipo         | Nulo | Default   | Descripción                           |
| ------------- | ------------ | ---- | --------- | ------------------------------------- |
| **id**        | SERIAL       | NO   | nextval() | Identificador único del empleado (PK) |
| nombre        | VARCHAR(200) | NO   | -         | Nombre completo del empleado          |
| fecha_ingreso | DATE         | NO   | -         | Fecha de ingreso a la empresa         |
| activo        | BOOLEAN      | NO   | TRUE      | Indica si el empleado está activo     |

### Restricciones

| Tipo        | Nombre                        | Descripción                   |
| ----------- | ----------------------------- | ----------------------------- |
| PRIMARY KEY | empleados_pkey                | id                            |
| CHECK       | empleados_fecha_ingreso_check | fecha_ingreso <= CURRENT_DATE |

### Ejemplo de Datos

```sql
INSERT INTO empleados (nombre, fecha_ingreso, activo) VALUES
('DIANA ROBLES SALAZAR', '2010-04-01', TRUE),
('CAROLINA ESTRADA CHAVEZ', '2010-05-01', TRUE),
('PAULINA CHAVEZ RAMOS', '2010-05-16', TRUE),
('RUBEN DARIO PEREZ OCHOA', '2011-08-01', TRUE),
('JOSE EMILIO MARTINEZ GUZMAN', '2014-06-01', TRUE);
```

### Observaciones

- La fecha de ingreso no puede ser futura
- Por defecto los empleados se crean activos

---

## Tabla: historial_puestos

### Descripción

Registro histórico de los puestos que ha ocupado cada empleado a lo largo del tiempo.

### Estructura

| Columna      | Tipo    | Nulo | Default   | Descripción                                  |
| ------------ | ------- | ---- | --------- | -------------------------------------------- |
| **id**       | SERIAL  | NO   | nextval() | Identificador único del registro (PK)        |
| empleado_id  | INTEGER | NO   | -         | Referencia al empleado (FK)                  |
| puesto_id    | INTEGER | NO   | -         | Referencia al puesto (FK)                    |
| fecha_inicio | DATE    | NO   | -         | Fecha de inicio en el puesto                 |
| fecha_fin    | DATE    | YES  | NULL      | Fecha de finalización (NULL = puesto actual) |

### Restricciones

| Tipo        | Nombre                  | Descripción                                   |
| ----------- | ----------------------- | --------------------------------------------- |
| PRIMARY KEY | historial_puestos_pkey  | id                                            |
| FOREIGN KEY | historial_empleado_fkey | empleado_id → empleados(id)                   |
| FOREIGN KEY | historial_puesto_fkey   | puesto_id → puestos(id)                       |
| CHECK       | historial_fechas_check  | fecha_fin IS NULL OR fecha_fin > fecha_inicio |

### Ejemplo de Datos

```sql
INSERT INTO historial_puestos (empleado_id, puesto_id, fecha_inicio, fecha_fin) VALUES
(1, 1, '2010-04-01', NULL),  -- Diana: Programador Jr (actual)
(2, 3, '2010-05-01', NULL),  -- Carolina: Programador Master (actual)
(3, 2, '2010-05-16', NULL),  -- Paulina: Becario (actual)
(4, 4, '2011-08-01', NULL),  -- Rubén: Programador Senior (actual)
(5, 5, '2014-06-01', '2018-05-31'),  -- José: Arquitecto (anterior)
(5, 6, '2018-06-01', NULL);  -- José: Admin Infra (actual)
```

### Observaciones

- Solo puede existir un registro con fecha_fin = NULL por empleado (puesto actual)
- La fecha_fin debe ser posterior a fecha_inicio si no es NULL

---

## Tabla: prestamos

### Descripción

Registro de todos los préstamos solicitados y otorgados a empleados.

### Estructura

| Columna                | Tipo          | Nulo | Default      | Descripción                           |
| ---------------------- | ------------- | ---- | ------------ | ------------------------------------- |
| **id**                 | SERIAL        | NO   | nextval()    | Identificador único del préstamo (PK) |
| empleado_id            | INTEGER       | NO   | -            | Referencia al empleado (FK)           |
| monto                  | NUMERIC(12,2) | NO   | -            | Monto total del préstamo              |
| plazo_meses            | INTEGER       | NO   | -            | Duración del préstamo en meses        |
| fecha_solicitud        | DATE          | NO   | -            | Fecha de solicitud del préstamo       |
| fecha_aprobacion       | DATE          | YES  | NULL         | Fecha de aprobación del préstamo      |
| tasa_interes_mensual   | NUMERIC(5,2)  | NO   | 1.00         | Tasa de interés mensual (%)           |
| pago_fijo_capital      | NUMERIC(12,2) | NO   | -            | Pago mensual fijo a capital           |
| fecha_inicio_descuento | DATE          | YES  | NULL         | Primera fecha de descuento            |
| fecha_fin_descuento    | DATE          | YES  | NULL         | Última fecha de descuento             |
| saldo_actual           | NUMERIC(12,2) | NO   | -            | Saldo pendiente del préstamo          |
| estado                 | VARCHAR(20)   | NO   | 'SOLICITADO' | Estado actual del préstamo            |

### Restricciones

| Tipo        | Nombre                           | Descripción                                                          |
| ----------- | -------------------------------- | -------------------------------------------------------------------- |
| PRIMARY KEY | prestamos_pkey                   | id                                                                   |
| FOREIGN KEY | prestamos_empleado_fkey          | empleado_id → empleados(id)                                          |
| CHECK       | prestamos_monto_check            | monto > 0                                                            |
| CHECK       | prestamos_plazo_check            | plazo_meses > 0 AND plazo_meses <= 24                                |
| CHECK       | prestamos_saldo_check            | saldo_actual >= 0                                                    |
| CHECK       | prestamos_estado_check           | estado IN ('SOLICITADO','APROBADO','ACTIVO','CONCLUIDO','RECHAZADO') |
| CHECK       | prestamos_fecha_aprobacion_check | fecha_aprobacion IS NULL OR fecha_aprobacion >= fecha_solicitud      |
| CHECK       | prestamos_tasa_check             | tasa_interes_mensual >= 0                                            |

### Estados del Préstamo

| Estado     | Descripción                                         |
| ---------- | --------------------------------------------------- |
| SOLICITADO | Préstamo recién solicitado, pendiente de aprobación |
| APROBADO   | Préstamo aprobado, pendiente de iniciar descuentos  |
| ACTIVO     | Préstamo con descuentos en curso                    |
| CONCLUIDO  | Préstamo totalmente pagado (saldo = 0)              |
| RECHAZADO  | Préstamo rechazado por el administrador             |

### Ejemplo de Datos

```sql
INSERT INTO prestamos (
  empleado_id, monto, plazo_meses, fecha_solicitud, fecha_aprobacion,
  tasa_interes_mensual, pago_fijo_capital, fecha_inicio_descuento,
  fecha_fin_descuento, saldo_actual, estado
) VALUES
(1, 20000.00, 12, '2020-01-05', '2020-01-10', 1.00, 1666.67,
 '2020-02-15', '2021-01-15', 0.00, 'CONCLUIDO'),
(5, 15000.00, 15, '2023-02-05', '2023-02-08', 1.00, 1000.00,
 '2023-03-15', '2024-05-15', 11000.00, 'ACTIVO');
```

### Fórmulas de Cálculo

```sql
-- Pago fijo a capital
pago_fijo_capital = monto / plazo_meses

-- Monto máximo permitido (validación)
monto_maximo = sueldo_actual * 6

-- Fecha fin descuento
fecha_fin_descuento = fecha_inicio_descuento + (plazo_meses - 1) MONTHS
```

### Observaciones

- El saldo_actual se inicializa con el monto total
- El plazo máximo es de 24 meses
- La tasa de interés por defecto es 1% mensual
- Solo puede haber un préstamo ACTIVO por empleado

---

## Tabla: abonos

### Descripción

Registro de cada pago mensual realizado a un préstamo.

### Estructura

| Columna       | Tipo          | Nulo | Default   | Descripción                              |
| ------------- | ------------- | ---- | --------- | ---------------------------------------- |
| **id**        | SERIAL        | NO   | nextval() | Identificador único del abono (PK)       |
| prestamo_id   | INTEGER       | NO   | -         | Referencia al préstamo (FK)              |
| numero_abono  | INTEGER       | NO   | -         | Número secuencial del abono (1, 2, 3...) |
| fecha         | DATE          | NO   | -         | Fecha del pago                           |
| monto_capital | NUMERIC(12,2) | NO   | -         | Pago aplicado a capital                  |
| monto_interes | NUMERIC(12,2) | NO   | -         | Interés cobrado del mes                  |
| monto_cobrado | NUMERIC(12,2) | NO   | -         | Total cobrado (capital + interés)        |
| saldo_actual  | NUMERIC(12,2) | NO   | -         | Saldo restante después del pago          |

### Restricciones

| Tipo        | Nombre                        | Descripción                                   |
| ----------- | ----------------------------- | --------------------------------------------- |
| PRIMARY KEY | abonos_pkey                   | id                                            |
| FOREIGN KEY | abonos_prestamo_fkey          | prestamo_id → prestamos(id) ON DELETE CASCADE |
| UNIQUE      | abonos_prestamo_numero_unique | (prestamo_id, numero_abono)                   |
| CHECK       | abonos_numero_check           | numero_abono > 0                              |
| CHECK       | abonos_monto_capital_check    | monto_capital >= 0                            |
| CHECK       | abonos_monto_interes_check    | monto_interes >= 0                            |
| CHECK       | abonos_monto_cobrado_check    | monto_cobrado >= 0                            |
| CHECK       | abonos_saldo_check            | saldo_actual >= 0                             |
| CHECK       | abonos_calculo_check          | monto_cobrado = monto_capital + monto_interes |

### Ejemplo de Datos

```sql
INSERT INTO abonos (
  prestamo_id, numero_abono, fecha, monto_capital, monto_interes,
  monto_cobrado, saldo_actual
) VALUES
(1, 1, '2020-02-15', 1666.67, 200.00, 1866.67, 18333.33),
(1, 2, '2020-03-15', 1666.67, 183.33, 1850.00, 16666.66),
(1, 3, '2020-04-15', 1666.67, 166.66, 1833.33, 15000.00);
```

### Fórmulas de Cálculo

```sql
-- Cálculo del interés del mes
monto_interes = saldo_anterior * (tasa_interes_mensual / 100)

-- En este caso con tasa 1%:
monto_interes = saldo_anterior * 0.01

-- Monto total cobrado
monto_cobrado = monto_capital + monto_interes

-- Nuevo saldo
saldo_actual = saldo_anterior - monto_capital
```

### Observaciones

- El número de abono es secuencial por préstamo (1, 2, 3...)
- El saldo_actual del último abono debe ser 0
- La combinación (prestamo_id, numero_abono) es única
- Si se elimina un préstamo, se eliminan todos sus abonos (CASCADE)

---

## Restricciones y Triggers

### Trigger 1: Cerrar Puesto Anterior

```sql
-- Trigger para cerrar automáticamente el puesto anterior
-- cuando se asigna un nuevo puesto

CREATE OR REPLACE FUNCTION cerrar_puesto_anterior()
RETURNS TRIGGER AS $$
BEGIN
  -- Si es un puesto nuevo (fecha_fin IS NULL)
  IF NEW.fecha_fin IS NULL THEN
    -- Cerrar cualquier puesto anterior del mismo empleado
    UPDATE historial_puestos
    SET fecha_fin = NEW.fecha_inicio - INTERVAL '1 day'
    WHERE empleado_id = NEW.empleado_id
      AND fecha_fin IS NULL
      AND id != NEW.id;
  END IF;

  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_cerrar_puesto_anterior
  BEFORE INSERT OR UPDATE ON historial_puestos
  FOR EACH ROW
  EXECUTE FUNCTION cerrar_puesto_anterior();
```

### Trigger 2: Validar Monto Cobrado

```sql
-- Trigger para validar que monto_cobrado = capital + interés

CREATE OR REPLACE FUNCTION validar_monto_cobrado()
RETURNS TRIGGER AS $$
BEGIN
  -- Validar cálculo
  IF ABS(NEW.monto_cobrado - (NEW.monto_capital + NEW.monto_interes)) > 0.01 THEN
    RAISE EXCEPTION 'Monto cobrado debe ser capital + interés';
  END IF;

  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_validar_monto_cobrado
  BEFORE INSERT OR UPDATE ON abonos
  FOR EACH ROW
  EXECUTE FUNCTION validar_monto_cobrado();
```

### Trigger 3: Actualizar Estado Préstamo

```sql
-- Trigger para actualizar estado del préstamo cuando saldo = 0

CREATE OR REPLACE FUNCTION actualizar_estado_prestamo()
RETURNS TRIGGER AS $$
BEGIN
  -- Si el saldo llega a 0, marcar como CONCLUIDO
  IF NEW.saldo_actual = 0 THEN
    UPDATE prestamos
    SET estado = 'CONCLUIDO',
        saldo_actual = 0
    WHERE id = NEW.prestamo_id;
  END IF;

  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_actualizar_estado_prestamo
  AFTER INSERT OR UPDATE ON abonos
  FOR EACH ROW
  EXECUTE FUNCTION actualizar_estado_prestamo();
```

### Trigger 4: Validar Número de Abono Consecutivo

```sql
-- Trigger para validar que los números de abono sean consecutivos

CREATE OR REPLACE FUNCTION validar_numero_abono()
RETURNS TRIGGER AS $$
DECLARE
  ultimo_abono INTEGER;
BEGIN
  -- Obtener el último número de abono del préstamo
  SELECT COALESCE(MAX(numero_abono), 0)
  INTO ultimo_abono
  FROM abonos
  WHERE prestamo_id = NEW.prestamo_id;

  -- Validar que sea consecutivo
  IF NEW.numero_abono != ultimo_abono + 1 THEN
    RAISE EXCEPTION 'Número de abono debe ser consecutivo. Esperado: %, Recibido: %',
      ultimo_abono + 1, NEW.numero_abono;
  END IF;

  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_validar_numero_abono
  BEFORE INSERT ON abonos
  FOR EACH ROW
  EXECUTE FUNCTION validar_numero_abono();
```

---

## Vistas Recomendadas

### Vista 1: Empleados con Puesto Actual

```sql
CREATE OR REPLACE VIEW v_empleados_puesto_actual AS
SELECT
  e.id,
  e.nombre,
  e.fecha_ingreso,
  EXTRACT(YEAR FROM AGE(CURRENT_DATE, e.fecha_ingreso)) AS antiguedad_anios,
  e.activo,
  p.nombre AS puesto_actual,
  p.sueldo AS sueldo_actual,
  hp.fecha_inicio AS fecha_inicio_puesto
FROM empleados e
LEFT JOIN historial_puestos hp ON e.id = hp.empleado_id AND hp.fecha_fin IS NULL
LEFT JOIN puestos p ON hp.puesto_id = p.id;
```

### Vista 2: Préstamos con Información del Empleado

```sql
CREATE OR REPLACE VIEW v_prestamos_detalle AS
SELECT
  pr.id,
  e.nombre AS empleado,
  pr.monto,
  pr.plazo_meses,
  pr.fecha_solicitud,
  pr.fecha_aprobacion,
  pr.tasa_interes_mensual,
  pr.pago_fijo_capital,
  pr.fecha_inicio_descuento,
  pr.fecha_fin_descuento,
  pr.saldo_actual,
  pr.estado,
  COUNT(a.id) AS total_abonos,
  COALESCE(SUM(a.monto_capital), 0) AS total_pagado_capital,
  COALESCE(SUM(a.monto_interes), 0) AS total_pagado_interes,
  COALESCE(SUM(a.monto_cobrado), 0) AS total_pagado
FROM prestamos pr
JOIN empleados e ON pr.empleado_id = e.id
LEFT JOIN abonos a ON pr.id = a.prestamo_id
GROUP BY pr.id, e.nombre;
```

### Vista 3: Resumen de Abonos por Préstamo

```sql
CREATE OR REPLACE VIEW v_abonos_resumen AS
SELECT
  pr.id AS prestamo_id,
  e.nombre AS empleado,
  pr.monto AS monto_prestamo,
  COUNT(a.id) AS abonos_realizados,
  pr.plazo_meses,
  COALESCE(SUM(a.monto_capital), 0) AS total_capital_pagado,
  COALESCE(SUM(a.monto_interes), 0) AS total_interes_pagado,
  pr.saldo_actual,
  pr.estado
FROM prestamos pr
JOIN empleados e ON pr.empleado_id = e.id
LEFT JOIN abonos a ON pr.id = a.prestamo_id
GROUP BY pr.id, e.nombre;
```

### Vista 4: Préstamos Activos

```sql
CREATE OR REPLACE VIEW v_prestamos_activos AS
SELECT
  e.nombre AS empleado,
  pr.id AS prestamo_id,
  pr.monto AS monto_prestado,
  pr.pago_fijo_capital,
  pr.saldo_actual,
  COUNT(a.id) AS pagos_realizados,
  pr.plazo_meses - COUNT(a.id) AS pagos_pendientes
FROM prestamos pr
JOIN empleados e ON pr.empleado_id = e.id
LEFT JOIN abonos a ON pr.id = a.prestamo_id
WHERE pr.estado = 'ACTIVO'
GROUP BY e.nombre, pr.id;
```

---

## Scripts SQL

### Script de Creación Completo

```sql
-- =====================================================
-- SCRIPT DE CREACIÓN DE BASE DE DATOS
-- Sistema de Gestión de Préstamos - Central Informática
-- =====================================================

-- Crear base de datos
CREATE DATABASE prestamos_db
  WITH ENCODING = 'UTF8'
  LC_COLLATE = 'es_MX.UTF-8'
  LC_CTYPE = 'es_MX.UTF-8'
  TEMPLATE = template0;

\c prestamos_db

-- Habilitar extensión para búsqueda de texto
CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- =====================================================
-- TABLA: puestos
-- =====================================================
CREATE TABLE puestos (
  id SERIAL PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL UNIQUE,
  sueldo NUMERIC(10,2) NOT NULL,
  CONSTRAINT puestos_sueldo_check CHECK (sueldo > 0)
);

COMMENT ON TABLE puestos IS 'Catálogo de puestos de trabajo';
COMMENT ON COLUMN puestos.id IS 'Identificador único del puesto';
COMMENT ON COLUMN puestos.nombre IS 'Nombre del puesto de trabajo';
COMMENT ON COLUMN puestos.sueldo IS 'Sueldo mensual en pesos mexicanos';

-- =====================================================
-- TABLA: empleados
-- =====================================================
CREATE TABLE empleados (
  id SERIAL PRIMARY KEY,
  nombre VARCHAR(200) NOT NULL,
  fecha_ingreso DATE NOT NULL,
  activo BOOLEAN NOT NULL DEFAULT TRUE,
  CONSTRAINT empleados_fecha_ingreso_check CHECK (fecha_ingreso <= CURRENT_DATE)
);

COMMENT ON TABLE empleados IS 'Información de empleados de la empresa';
COMMENT ON COLUMN empleados.id IS 'Identificador único del empleado';
COMMENT ON COLUMN empleados.nombre IS 'Nombre completo del empleado';
COMMENT ON COLUMN empleados.fecha_ingreso IS 'Fecha de ingreso a la empresa';
COMMENT ON COLUMN empleados.activo IS 'Indica si el empleado está activo';

-- =====================================================
-- TABLA: historial_puestos
-- =====================================================
CREATE TABLE historial_puestos (
  id SERIAL PRIMARY KEY,
  empleado_id INTEGER NOT NULL REFERENCES empleados(id),
  puesto_id INTEGER NOT NULL REFERENCES puestos(id),
  fecha_inicio DATE NOT NULL,
  fecha_fin DATE NULL,
  CONSTRAINT historial_fechas_check CHECK (fecha_fin IS NULL OR fecha_fin > fecha_inicio)
);

COMMENT ON TABLE historial_puestos IS 'Historial temporal de puestos por empleado';

-- Índice único parcial: solo un puesto activo por empleado
CREATE UNIQUE INDEX historial_empleado_puesto_activo
ON historial_puestos(empleado_id)
WHERE fecha_fin IS NULL;

-- =====================================================
-- TABLA: prestamos
-- =====================================================
CREATE TABLE prestamos (
  id SERIAL PRIMARY KEY,
  empleado_id INTEGER NOT NULL REFERENCES empleados(id),
  monto NUMERIC(12,2) NOT NULL,
  plazo_meses INTEGER NOT NULL,
  fecha_solicitud DATE NOT NULL,
  fecha_aprobacion DATE NULL,
  tasa_interes_mensual NUMERIC(5,2) NOT NULL DEFAULT 1.00,
  pago_fijo_capital NUMERIC(12,2) NOT NULL,
  fecha_inicio_descuento DATE NULL,
  fecha_fin_descuento DATE NULL,
  saldo_actual NUMERIC(12,2) NOT NULL,
  estado VARCHAR(20) NOT NULL DEFAULT 'SOLICITADO',
  CONSTRAINT prestamos_monto_check CHECK (monto > 0),
  CONSTRAINT prestamos_plazo_check CHECK (plazo_meses > 0 AND plazo_meses <= 24),
  CONSTRAINT prestamos_saldo_check CHECK (saldo_actual >= 0),
  CONSTRAINT prestamos_tasa_check CHECK (tasa_interes_mensual >= 0),
  CONSTRAINT prestamos_estado_check CHECK (
    estado IN ('SOLICITADO','APROBADO','ACTIVO','CONCLUIDO','RECHAZADO')
  ),
  CONSTRAINT prestamos_fecha_aprobacion_check CHECK (
    fecha_aprobacion IS NULL OR fecha_aprobacion >= fecha_solicitud
  )
);

COMMENT ON TABLE prestamos IS 'Registro de préstamos otorgados a empleados';

-- =====================================================
-- TABLA: abonos
-- =====================================================
CREATE TABLE abonos (
  id SERIAL PRIMARY KEY,
  prestamo_id INTEGER NOT NULL REFERENCES prestamos(id) ON DELETE CASCADE,
  numero_abono INTEGER NOT NULL,
  fecha DATE NOT NULL,
  monto_capital NUMERIC(12,2) NOT NULL,
  monto_interes NUMERIC(12,2) NOT NULL,
  monto_cobrado NUMERIC(12,2) NOT NULL,
  saldo_actual NUMERIC(12,2) NOT NULL,
  CONSTRAINT abonos_prestamo_numero_unique UNIQUE (prestamo_id, numero_abono),
  CONSTRAINT abonos_numero_check CHECK (numero_abono > 0),
  CONSTRAINT abonos_monto_capital_check CHECK (monto_capital >= 0),
  CONSTRAINT abonos_monto_interes_check CHECK (monto_interes >= 0),
  CONSTRAINT abonos_monto_cobrado_check CHECK (monto_cobrado >= 0),
  CONSTRAINT abonos_saldo_check CHECK (saldo_actual >= 0),
  CONSTRAINT abonos_calculo_check CHECK (
    ABS(monto_cobrado - (monto_capital + monto_interes)) < 0.01
  )
);

COMMENT ON TABLE abonos IS 'Registro de pagos mensuales de préstamos';

-- =====================================================
-- ÍNDICES
-- =====================================================
CREATE INDEX idx_empleados_activo ON empleados(activo);
CREATE INDEX idx_empleados_nombre ON empleados(nombre);
CREATE INDEX idx_historial_empleado ON historial_puestos(empleado_id);
CREATE INDEX idx_historial_puesto ON historial_puestos(puesto_id);
CREATE INDEX idx_historial_fecha_fin ON historial_puestos(fecha_fin);
CREATE INDEX idx_prestamos_empleado ON prestamos(empleado_id);
CREATE INDEX idx_prestamos_estado ON prestamos(estado);
CREATE INDEX idx_prestamos_fecha_solicitud ON prestamos(fecha_solicitud);
CREATE INDEX idx_abonos_prestamo ON abonos(prestamo_id);
CREATE INDEX idx_abonos_fecha ON abonos(fecha);

-- =====================================================
-- SCRIPT COMPLETO
-- =====================================================
```

### Script de Datos de Prueba

Ver archivo: [datos_prueba.sql](datos_prueba.sql)

---

## Mantenimiento y Respaldo

### Respaldo Diario

```bash
# Respaldo completo
pg_dump -U prestamos_user -d prestamos_db -F c -f backup_$(date +%Y%m%d).dump

# Respaldo solo datos
pg_dump -U prestamos_user -d prestamos_db -F c -a -f backup_data_$(date +%Y%m%d).dump
```

### Restauración

```bash
# Restaurar desde backup
pg_restore -U prestamos_user -d prestamos_db -c backup_20260225.dump
```

---

**Última actualización:** 26 de febrero de 2026  
**Autor:** Equipo de Desarrollo - Central Informática
