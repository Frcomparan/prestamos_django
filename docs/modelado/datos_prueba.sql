-- =====================================================
-- SCRIPT DE DATOS DE PRUEBA
-- Sistema de Gestión de Préstamos - Central Informática
-- =====================================================
-- Basado en el caso de estudio proporcionado
-- Incluye datos completos de ejemplo para el taller
-- =====================================================

-- Conectar a la base de datos
\c prestamos_db

BEGIN;

-- =====================================================
-- 1. PUESTOS (Tabla 1 del caso de estudio)
-- =====================================================
INSERT INTO puestos (id, nombre, sueldo) VALUES
(1, 'PROGRAMADOR JR', 16000.00),
(2, 'BECARIO', 10000.00),
(3, 'PROGRAMADOR MASTER', 60000.00),
(4, 'PROGRAMADOR SENIOR', 40000.00),
(5, 'ARQUITECTO DE SOFTWARE', 50000.00),
(6, 'ADMINISTRADOR DE INFRAESTRUCTURA', 55000.00);

-- Resetear secuencia
SELECT setval('puestos_id_seq', 6);

-- =====================================================
-- 2. EMPLEADOS (Tabla 2 del caso de estudio)
-- =====================================================
INSERT INTO empleados (id, nombre, fecha_ingreso, activo) VALUES
(1, 'DIANA ROBLES SALAZAR', '2010-04-01', TRUE),
(2, 'CAROLINA ESTRADA CHAVEZ', '2010-05-01', TRUE),
(3, 'PAULINA CHAVEZ RAMOS', '2010-05-16', TRUE),
(4, 'RUBEN DARIO PEREZ OCHOA', '2011-08-01', TRUE),
(5, 'JOSE EMILIO MARTINEZ GUZMAN', '2014-06-01', TRUE);

-- Resetear secuencia
SELECT setval('empleados_id_seq', 5);

-- =====================================================
-- 3. HISTORIAL DE PUESTOS (Tabla 3 del caso de estudio)
-- =====================================================
INSERT INTO historial_puestos (id, empleado_id, puesto_id, fecha_inicio, fecha_fin) VALUES
(1, 1, 1, '2010-04-01', NULL),  -- Diana: Programador Jr (actual)
(2, 2, 3, '2010-05-01', NULL),  -- Carolina: Programador Master (actual)
(3, 3, 2, '2010-05-16', NULL),  -- Paulina: Becario (actual)
(4, 4, 4, '2011-08-01', NULL),  -- Rubén: Programador Senior (actual)
(5, 5, 5, '2014-06-01', '2018-05-31'),  -- José: Arquitecto (anterior)
(6, 5, 6, '2018-06-01', NULL);  -- José: Admin Infraestructura (actual)

-- Resetear secuencia
SELECT setval('historial_puestos_id_seq', 6);

-- =====================================================
-- 4. PRÉSTAMOS (Tabla 4 del caso de estudio)
-- =====================================================

-- Préstamo 1: DIANA ROBLES SALAZAR - CONCLUIDO
INSERT INTO prestamos (
  id, empleado_id, monto, plazo_meses, fecha_solicitud, fecha_aprobacion,
  tasa_interes_mensual, pago_fijo_capital, fecha_inicio_descuento,
  fecha_fin_descuento, saldo_actual, estado
) VALUES (
  1, 1, 20000.00, 12, '2020-01-05', '2020-01-10',
  1.00, 1666.67, '2020-02-15', '2021-01-15', 0.00, 'CONCLUIDO'
);

-- Préstamo 2: JOSE EMILIO MARTINEZ GUZMAN - ACTIVO
INSERT INTO prestamos (
  id, empleado_id, monto, plazo_meses, fecha_solicitud, fecha_aprobacion,
  tasa_interes_mensual, pago_fijo_capital, fecha_inicio_descuento,
  fecha_fin_descuento, saldo_actual, estado
) VALUES (
  2, 5, 15000.00, 15, '2023-02-05', '2023-02-08',
  1.00, 1000.00, '2023-03-15', '2024-05-15', 11000.00, 'ACTIVO'
);

-- Préstamo 3: CAROLINA ESTRADA CHAVEZ - ACTIVO
INSERT INTO prestamos (
  id, empleado_id, monto, plazo_meses, fecha_solicitud, fecha_aprobacion,
  tasa_interes_mensual, pago_fijo_capital, fecha_inicio_descuento,
  fecha_fin_descuento, saldo_actual, estado
) VALUES (
  3, 2, 20000.00, 12, '2023-03-22', '2023-03-23',
  1.00, 1666.67, '2023-04-30', '2024-03-30', 14999.99, 'ACTIVO'
);

-- Préstamo 4: DIANA ROBLES SALAZAR - ACTIVO
INSERT INTO prestamos (
  id, empleado_id, monto, plazo_meses, fecha_solicitud, fecha_aprobacion,
  tasa_interes_mensual, pago_fijo_capital, fecha_inicio_descuento,
  fecha_fin_descuento, saldo_actual, estado
) VALUES (
  4, 1, 10000.00, 12, '2023-03-25', '2023-03-30',
  1.00, 833.33, '2023-04-15', '2024-03-15', 7500.00, 'ACTIVO'
);

-- Préstamo 5: RUBEN DARIO PEREZ OCHOA - ACTIVO
INSERT INTO prestamos (
  id, empleado_id, monto, plazo_meses, fecha_solicitud, fecha_aprobacion,
  tasa_interes_mensual, pago_fijo_capital, fecha_inicio_descuento,
  fecha_fin_descuento, saldo_actual, estado
) VALUES (
  5, 4, 30000.00, 24, '2023-05-18', '2023-05-20',
  1.00, 1250.00, '2023-06-30', '2025-05-30', 28750.00, 'ACTIVO'
);

-- Préstamo 6: PAULINA CHAVEZ RAMOS - ACTIVO
INSERT INTO prestamos (
  id, empleado_id, monto, plazo_meses, fecha_solicitud, fecha_aprobacion,
  tasa_interes_mensual, pago_fijo_capital, fecha_inicio_descuento,
  fecha_fin_descuento, saldo_actual, estado
) VALUES (
  6, 3, 18000.00, 12, '2023-06-02', '2023-06-14',
  1.00, 1500.00, '2023-06-30', '2024-05-30', 16500.00, 'ACTIVO'
);

-- Resetear secuencia
SELECT setval('prestamos_id_seq', 6);

-- =====================================================
-- 5. ABONOS - PRÉSTAMO 1 (Tabla 5 del caso de estudio)
-- =====================================================
-- DIANA ROBLES SALAZAR - $20,000 - CONCLUIDO

INSERT INTO abonos (prestamo_id, numero_abono, fecha, monto_capital, monto_interes, monto_cobrado, saldo_actual) VALUES
(1, 1, '2020-02-15', 1666.67, 200.00, 1866.67, 18333.33),
(1, 2, '2020-03-15', 1666.67, 183.33, 1850.00, 16666.66),
(1, 3, '2020-04-15', 1666.67, 166.66, 1833.33, 15000.00),
(1, 4, '2020-05-15', 1666.67, 150.00, 1816.67, 13333.33),
(1, 5, '2020-06-15', 1666.67, 133.33, 1800.00, 11666.67),
(1, 6, '2020-07-15', 1666.67, 116.66, 1783.33, 10000.00),
(1, 7, '2020-08-15', 1666.67, 100.00, 1766.67, 8333.33),
(1, 8, '2020-09-15', 1666.67, 83.33, 1750.00, 6666.66),
(1, 9, '2020-10-15', 1666.67, 66.66, 1733.33, 5000.00),
(1, 10, '2020-11-15', 1666.67, 50.00, 1716.67, 3333.33),
(1, 11, '2020-12-15', 1666.67, 33.00, 1699.66, 1666.66),
(1, 12, '2021-01-15', 1666.67, 16.00, 1682.67, 0.00);

-- =====================================================
-- 6. ABONOS - PRÉSTAMO 2 (Tabla 6 del caso de estudio)
-- =====================================================
-- JOSE EMILIO MARTINEZ GUZMAN - $15,000 - ACTIVO

INSERT INTO abonos (prestamo_id, numero_abono, fecha, monto_capital, monto_interes, monto_cobrado, saldo_actual) VALUES
(2, 1, '2023-03-15', 1000.00, 150.00, 1150.00, 14000.00),
(2, 2, '2023-04-15', 1000.00, 140.00, 1140.00, 13000.00),
(2, 3, '2023-05-15', 1000.00, 130.00, 1130.00, 12000.00),
(2, 4, '2023-06-15', 1000.00, 120.00, 1120.00, 11000.00);

-- =====================================================
-- 7. ABONOS - PRÉSTAMO 3 (Tabla 7 del caso de estudio)
-- =====================================================
-- CAROLINA ESTRADA CHAVEZ - $20,000 - ACTIVO

INSERT INTO abonos (prestamo_id, numero_abono, fecha, monto_capital, monto_interes, monto_cobrado, saldo_actual) VALUES
(3, 1, '2023-04-15', 1666.67, 200.00, 1866.67, 18333.33),
(3, 2, '2023-05-15', 1666.67, 183.33, 1850.00, 16666.66),
(3, 3, '2023-06-15', 1666.67, 166.66, 1833.33, 14999.99);

-- =====================================================
-- 8. ABONOS - PRÉSTAMO 4 (Tabla 8 del caso de estudio)
-- =====================================================
-- DIANA ROBLES SALAZAR - $10,000 - ACTIVO

INSERT INTO abonos (prestamo_id, numero_abono, fecha, monto_capital, monto_interes, monto_cobrado, saldo_actual) VALUES
(4, 1, '2023-04-15', 833.33, 100.00, 933.33, 9166.67),
(4, 2, '2023-05-15', 833.33, 91.66, 925.00, 8333.34),
(4, 3, '2023-06-15', 833.33, 83.33, 916.67, 7500.00);

-- =====================================================
-- 9. ABONOS - PRÉSTAMO 5 (Tabla 9 del caso de estudio)
-- =====================================================
-- RUBEN DARIO PEREZ OCHOA - $30,000 - ACTIVO

INSERT INTO abonos (prestamo_id, numero_abono, fecha, monto_capital, monto_interes, monto_cobrado, saldo_actual) VALUES
(5, 1, '2023-06-30', 1250.00, 300.00, 1550.00, 28750.00);

-- =====================================================
-- 10. ABONOS - PRÉSTAMO 6 (Caso de estudio - 1 pago)
-- =====================================================
-- PAULINA CHAVEZ RAMOS - $18,000 - ACTIVO

INSERT INTO abonos (prestamo_id, numero_abono, fecha, monto_capital, monto_interes, monto_cobrado, saldo_actual) VALUES
(6, 1, '2023-06-30', 1500.00, 180.00, 1680.00, 16500.00);

COMMIT;

-- =====================================================
-- CONSULTAS DE VERIFICACIÓN
-- =====================================================

-- Verificar puestos
SELECT '=== PUESTOS ===' AS seccion;
SELECT * FROM puestos ORDER BY id;

-- Verificar empleados con puesto actual
SELECT '=== EMPLEADOS CON PUESTO ACTUAL ===' AS seccion;
SELECT 
  e.id,
  e.nombre,
  e.fecha_ingreso,
  EXTRACT(YEAR FROM AGE(CURRENT_DATE, e.fecha_ingreso)) AS antiguedad_anios,
  p.nombre AS puesto_actual,
  p.sueldo AS sueldo_actual
FROM empleados e
LEFT JOIN historial_puestos hp ON e.id = hp.empleado_id AND hp.fecha_fin IS NULL
LEFT JOIN puestos p ON hp.puesto_id = p.id
ORDER BY e.id;

-- Verificar préstamos
SELECT '=== PRÉSTAMOS ===' AS seccion;
SELECT 
  pr.id,
  e.nombre AS empleado,
  pr.monto,
  pr.plazo_meses,
  pr.fecha_solicitud,
  pr.fecha_aprobacion,
  pr.saldo_actual,
  pr.estado
FROM prestamos pr
JOIN empleados e ON pr.empleado_id = e.id
ORDER BY pr.id;

-- Verificar total de abonos por préstamo
SELECT '=== RESUMEN DE ABONOS ===' AS seccion;
SELECT 
  pr.id AS prestamo_id,
  e.nombre AS empleado,
  pr.monto,
  COUNT(a.id) AS total_abonos,
  pr.plazo_meses,
  SUM(a.monto_capital) AS total_capital_pagado,
  SUM(a.monto_interes) AS total_interes_pagado,
  SUM(a.monto_cobrado) AS total_cobrado,
  pr.saldo_actual,
  pr.estado
FROM prestamos pr
JOIN empleados e ON pr.empleado_id = e.id
LEFT JOIN abonos a ON pr.id = a.prestamo_id
GROUP BY pr.id, e.nombre
ORDER BY pr.id;

-- Listado cronológico de abonos (Tabla 10 del caso de estudio)
SELECT '=== HISTORIAL CRONOLÓGICO DE ABONOS ===' AS seccion;
SELECT 
  a.id AS id_abono,
  a.prestamo_id,
  e.nombre AS empleado,
  a.numero_abono,
  a.fecha,
  a.monto_capital,
  a.monto_interes,
  a.monto_cobrado,
  a.saldo_actual
FROM abonos a
JOIN prestamos pr ON a.prestamo_id = pr.id
JOIN empleados e ON pr.empleado_id = e.id
ORDER BY a.fecha, a.id;

-- =====================================================
-- ESTADÍSTICAS FINALES
-- =====================================================
SELECT '=== ESTADÍSTICAS DEL SISTEMA ===' AS seccion;
SELECT 
  'Total Puestos' AS concepto,
  COUNT(*) AS cantidad
FROM puestos

UNION ALL

SELECT 
  'Total Empleados',
  COUNT(*)
FROM empleados

UNION ALL

SELECT 
  'Total Préstamos',
  COUNT(*)
FROM prestamos

UNION ALL

SELECT 
  'Préstamos Activos',
  COUNT(*)
FROM prestamos
WHERE estado = 'ACTIVO'

UNION ALL

SELECT 
  'Préstamos Concluidos',
  COUNT(*)
FROM prestamos
WHERE estado = 'CONCLUIDO'

UNION ALL

SELECT 
  'Total Abonos Registrados',
  COUNT(*)
FROM abonos;

-- =====================================================
-- FIN DEL SCRIPT
-- =====================================================
