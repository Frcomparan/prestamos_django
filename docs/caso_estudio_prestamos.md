# Caso de estudio: Préstamos (Central Informática)

Central Informática cuenta con una **caja de ahorros** propia de los empleados.  
Cada mes se descuenta a cada empleado un porcentaje de su pago mensual y el patrón aporta la misma cantidad.  
Estos recursos se integran en un fondo del que se proporcionan **préstamos a los empleados**. 

---

## A. Condiciones del préstamo  

Para que un empleado pueda solicitar un préstamo:

- Debe tener **mínimo 1 año** de antigüedad en la empresa.
- El **monto** del préstamo **no puede superar 6 meses** de su sueldo.
- **No debe tener ningún préstamo vigente**. 

Condiciones financieras:

- Se cobra una **tasa de interés mensual del 1%** sobre **saldos insolutos**  
  (saldo insoluto = saldo de la deuda actual).
- El **plazo máximo** para pagarlo es de **24 meses**.
- Cada mes se debe realizar el **descuento** correspondiente. 

### Datos que debe registrar el sistema (préstamo)

- Nombre del empleado
- Monto del préstamo
- Fecha inicio del descuento
- Fecha fin del descuento
- Duración en meses
- Tasa de interés mensual 

### Datos que debe registrar el sistema (abonos / pagos parciales)

Por cada abono:

- Fecha
- Pago a capital
- Interés
- Monto (cobrado)
- Saldo actual 

### Catálogos / entidades base

- **Puestos**: nombre, sueldo
- **Empleados**: nombre, fecha de ingreso, activo 

---

## B. Consideraciones del contexto (datos de ejemplo)

### Tabla 1. Puestos de trabajo (Central Informática)

| ID | Nombre                          | Sueldo |
|---:|---------------------------------|-------:|
| 1  | PROGRAMADOR JR                  | 16000  |
| 2  | BECARIO                         | 10000  |
| 3  | PROGRAMADOR MASTER              | 60000  |
| 4  | PROGRAMADOR SENIOR              | 40000  |
| 5  | ARQUITECTO DE SOFTWARE          | 50000  |
| 6  | ADMINISTRADOR DE INFRAESTRUCTURA| 55000  |



### Tabla 2. Empleados

| ID | Nombre                         | Fecha de ingreso | Activo |
|---:|--------------------------------|-----------------|:------:|
| 1  | DIANA ROBLES SALAZAR           | 2010-04-01      |   1    |
| 2  | CAROLINA ESTRADA CHAVEZ        | 2010-05-01      |   1    |
| 3  | PAULINA CHAVEZ RAMOS           | 2010-05-16      |   1    |
| 4  | RUBEN DARIO PEREZ OCHOA        | 2011-08-01      |   1    |
| 5  | JOSE EMILIO MARTINEZ GUZMAN    | 2014-06-01      |   1    |



### Tabla 3. Historial de puestos por empleado

> Se observa que **JOSE EMILIO MARTINEZ GUZMAN** es el único que ha cambiado de puesto.

| ID | Empleado                      | Puesto                           | Fecha inicio | Fecha fin   |
|---:|-------------------------------|----------------------------------|-------------|------------|
| 1  | DIANA ROBLES SALAZAR          | PROGRAMADOR JR                   | 2010-04-01  | NULL       |
| 2  | CAROLINA ESTRADA CHAVEZ       | PROGRAMADOR MASTER               | 2010-05-01  | NULL       |
| 3  | PAULINA CHAVEZ RAMOS          | BECARIO                          | 2010-05-16  | NULL       |
| 4  | RUBEN DARIO PEREZ OCHOA       | PROGRAMADOR SENIOR               | 2011-08-01  | NULL       |
| 5  | JOSE EMILIO MARTINEZ GUZMAN   | ARQUITECTO DE SOFTWARE           | 2014-06-01  | 2018-05-31 |
| 6  | JOSE EMILIO MARTINEZ GUZMAN   | ADMINISTRADOR DE INFRAESTRUCTURA | 2018-06-01  | NULL       |



---

## Préstamos aprobados (Tabla 4)

Observaciones por préstamo (según el documento):

- **DIANA ROBLES SALAZAR** solicitó el **2020-01-05** por **$20,000** a **12 meses**; aprobado **2020-01-10**; tasa **1% mensual**.  
  Pago fijo a capital: **$1,666.67**. Descuento: **2020-02-15** a **2021-01-15**.
- **JOSE EMILIO MARTINEZ GUZMAN** solicitó el **2023-02-05** por **$15,000** a **15 meses**; aprobado **2023-02-08**; tasa **1% mensual**.  
  Pago fijo a capital: **$1,000.00**. Descuento: **2023-03-15** a **2024-05-15**.
- **CAROLINA ESTRADA CHAVEZ** solicitó el **2023-03-22** por **$20,000** a **12 meses**; aprobado **2023-03-23**; tasa **1% mensual**.  
  Pago fijo a capital: **$1,666.67**. Descuento: **2023-04-30** a **2024-03-30**.
- **DIANA ROBLES SALAZAR** solicitó el **2023-03-25** por **$10,000** a **12 meses**; aprobado **2023-03-30**; tasa **1% mensual**.  
  Pago fijo a capital: **$833.33**. Descuento: **2023-04-15** a **2024-03-15**.
- **RUBEN DARIO PEREZ OCHOA** solicitó el **2023-05-18** por **$30,000** a **24 meses**; aprobado **2023-05-20**; tasa **1% mensual**.  
  Pago fijo a capital: **$1,250.00**. Descuento: **2023-06-30** a **2025-05-30**.
- **PAULINA CHAVEZ RAMOS** solicitó el **2023-06-02** por **$18,000** a **12 meses**; aprobado **2023-06-14**; tasa **1% mensual**.  
  Pago fijo a capital: **$1,500.00**. Descuento: **2023-06-30** a **2024-05-30**.



### Tabla 4. Relación de empleados con préstamos aprobados

| ID | Empleado                    | Fecha solicitud | Monto | Plazo | Fecha aprob | Tasa mensual | Pago fijo capital | Fecha ini desc | Fecha fin desc | Saldo | Estado   |
|---:|-----------------------------|---------------|------:|------:|------------|------------:|-----------------:|---------------|---------------|------:|----------|
| 1  | DIANA ROBLES SALAZAR        | 2020-01-05    | 20000 | 12    | 2020-01-10 | 1           | 1,666.67         | 2020-02-15    | 2021-01-15    | 20000 | APROBADO |
| 2  | JOSE EMILIO MARTINEZ GUZMAN | 2023-02-05    | 15000 | 15    | 2023-02-08 | 1           | 1,000.00         | 2023-03-15    | 2024-05-15    | 15000 | APROBADO |
| 3  | CAROLINA ESTRADA CHAVEZ     | 2023-03-22    | 20000 | 12    | 2023-03-23 | 1           | 1,666.67         | 2023-04-30    | 2024-03-30    | 20000 | APROBADO |
| 4  | DIANA ROBLES SALAZAR        | 2023-03-25    | 10000 | 12    | 2023-03-30 | 1           | 833.33           | 2023-04-15    | 2024-03-15    | 10000 | APROBADO |
| 5  | RUBEN DARIO PEREZ OCHOA     | 2023-05-18    | 30000 | 24    | 2023-05-20 | 1           | 1,250.00         | 2023-06-30    | 2025-05-30    | 30000 | APROBADO |
| 6  | PAULINA CHAVEZ RAMOS        | 2023-06-02    | 18000 | 12    | 2023-06-14 | 1           | 1,500.00         | 2023-06-30    | 2024-05-30    | 30000 | APROBADO |

> Nota: el documento contiene algunas inconsistencias tipográficas (p. ej., saldo/fechas en ciertos renglones).  
> Esta tabla se transcribió respetando el contenido visible. 

---

## Abonos considerados (hasta el 30 de junio de 2023)

Para efectos del caso de estudio, en todos los préstamos se consideran los abonos realizados **hasta el 30 de junio del 2023**. 

### Tabla 5. Abonos del préstamo 1 (DIANA ROBLES SALAZAR, $20,000)

| ID préstamo | Num abono | Fecha       | Monto capital | Monto interés | Monto cobrado | Saldo actual |
|-----------:|----------:|------------|--------------:|--------------:|--------------:|------------:|
| 1 | 1  | 2020-02-15 | 1666.67 | 200.00 | 1,866.67 | 18,333.33 |
| 1 | 2  | 2020-03-15 | 1666.67 | 183.33 | 1,850.00 | 16,666.66 |
| 1 | 3  | 2020-04-15 | 1666.67 | 166.66 | 1,833.33 | 15,000.00 |
| 1 | 4  | 2020-05-15 | 1666.67 | 150.00 | 1,816.67 | 13,333.33 |
| 1 | 5  | 2020-06-15 | 1666.67 | 133.33 | 1,800.00 | 11,666.67 |
| 1 | 6  | 2020-07-15 | 1666.67 | 116.66 | 1,783.33 | 10,000.00 |
| 1 | 7  | 2020-08-15 | 1666.67 | 100.00 | 1,766.67 | 8,333.33 |
| 1 | 8  | 2020-09-15 | 1666.67 | 83.33  | 1,750.00 | 6,666.66 |
| 1 | 9  | 2020-10-15 | 1666.67 | 66.66  | 1,733.33 | 5,000.00 |
| 1 | 10 | 2020-11-15 | 1666.67 | 50.00  | 1,716.67 | 3,333.33 |
| 1 | 11 | 2020-12-15 | 1666.67 | 33.00  | 1,699.66 | 1,666.66 |
| 1 | 12 | 2021-01-15 | 1666.67 | 16.00  | 1,682.67 | 0 |



### Tabla 6. Abonos del préstamo 2 (JOSE EMILIO MARTINEZ GUZMAN, $15,000)

| ID préstamo | Num abono | Fecha       | Monto capital | Monto interés | Monto cobrado | Saldo actual |
|-----------:|----------:|------------|--------------:|--------------:|--------------:|------------:|
| 2 | 1 | 2023-03-15 | 1000.00 | 150.00 | 1,150.00 | 14,000.00 |
| 2 | 2 | 2023-04-15 | 1000.00 | 140.00 | 1,140.00 | 13,000.00 |
| 2 | 3 | 2023-05-15 | 1000.00 | 130.00 | 1,130.00 | 12,000.00 |
| 2 | 4 | 2023-06-15 | 1000.00 | 120.00 | 1,120.00 | 11,000.00 |



### Tabla 7. Abonos del préstamo 3 (CAROLINA ESTRADA CHAVEZ, $20,000)

| ID préstamo | Num abono | Fecha       | Monto capital | Monto interés | Monto cobrado | Saldo actual |
|-----------:|----------:|------------|--------------:|--------------:|--------------:|------------:|
| 3 | 1 | 2023-04-15 | 1666.67 | 200.00 | 1,866.67 | 18,333.33 |
| 3 | 2 | 2023-05-15 | 1666.67 | 183.33 | 1,850.00 | 16,666.66 |
| 3 | 3 | 2023-06-15 | 1666.67 | 166.66 | 1,833.33 | 14,999.99 |



### Tabla 8. Abonos del préstamo 4 (DIANA ROBLES SALAZAR, $10,000) *(parcial)*

> En el documento solo se alcanzan a ver 3 abonos en la tabla correspondiente a este préstamo.

| ID préstamo | Num abono | Fecha       | Monto capital | Monto interés | Monto cobrado | Saldo actual |
|-----------:|----------:|------------|--------------:|--------------:|--------------:|------------:|
| 4 | 1 | 2020-04-15 | 833.33 | 100.00 | 933.33 | 9,166.67 |
| 4 | 2 | 2020-05-15 | 833.33 | 91.66  | 925.00 | 8,333.34 |
| 4 | 3 | 2020-06-15 | 833.33 | 83.33  | 916.67 | 7,500.00 |



### Tabla 9. Abonos del préstamo 5 (RUBEN DARIO PEREZ OCHOA, $30,000) *(1 pago)*

| ID préstamo | Num abono | Fecha       | Monto capital | Monto interés | Monto cobrado | Saldo actual |
|-----------:|----------:|------------|--------------:|--------------:|--------------:|------------:|
| 5 | 1 | 2023-06-30 | 1250.00 | 300.00 | 1,550.00 | 28,750.00 |



### Préstamo 6 (PAULINA CHÁVEZ RAMOS)

El documento indica que se ha realizado **un pago mensual**, pero no muestra la tabla completa en el texto extraído. 

---

## Tabla 10. Resumen cronológico de abonos

El documento incluye un resumen cronológico (Tabla 10) con los abonos registrados a los diversos préstamos, con columnas:

- ID abono
- ID préstamo
- Num abono
- Fecha
- Monto capital
- Monto interés
- Monto cobrado
- Saldo actual 

*(Por extensión, se sugiere usar directamente la Tabla 10 del PDF como dataset de pruebas.)*

---

## Requerimientos funcionales del sistema (A–P)

Además, el sistema debe: 

A. Mostrar un listado de todos los puestos considerando todos los datos registrados.  
B. Permitir agregar un nuevo puesto.  
C. Mostrar un listado de todos los empleados, considerando todos los datos registrados.  
D. Permitir agregar un nuevo empleado.  
E. Mostrar el historial de puestos que ha tenido un empleado.  
F. Cambiar de puesto a un empleado.  
G. Mostrar el historial de préstamos de un empleado.  
H. Mostrar los detalles de cierto préstamo de un empleado.  
I. Modificar los datos de un empleado.  
J. Mostrar un listado de todos los préstamos que se han otorgado.  
K. Permitir agregar un nuevo préstamo.  
L. Permitir agregar un nuevo abono a cierto préstamo.  
M. Mostrar un listado de todos los préstamos, especificando el nombre del empleado y todos los datos registrados en el préstamo (como en Tabla 4).  
N. Mostrar un reporte de cierto préstamo, especificando el nombre del empleado, el id del préstamo, la fecha de aprobación y monto del préstamo, además detallando los datos de los abonos realizados.  
O. Mostrar el historial de préstamos de un empleado, especificando: nombre, id préstamo, monto, fecha inicio, fecha fin, estado y acceso a detalles.  
P. Mostrar un listado de préstamos activos en una fecha específica, con: nombre empleado, número de préstamo, monto prestado, pago a capital, pago de interés y monto cobrado (deducido).

---

## Formatos de salida solicitados (ejemplos)

### N) Reporte de cierto préstamo (ejemplo)

**EMPLEADO:** DIANA ROBLES SALAZAR  
**ID PRESTAMO:** 4  
**FECHA APROB.:** 2023/03/30  
**MONTO PRESTADO:** 10000

| ID abono | Num abono | Fecha       | Monto capital | Monto interés | Monto cobrado | Saldo pendiente |
|--------:|----------:|------------|--------------:|--------------:|--------------:|----------------:|
| 16 | 1 | 2023-04-15 | 833.33 | 100.00 | 933.33 | 9,166.67 |
| 19 | 2 | 2023-04-15 | 833.33 | 91.67  | 925.00 | 8,333.34 |
| 22 | 3 | 2023-04-15 | 833.33 | 83.33  | 916.66 | 7,500.0 |



### O) Historial de préstamos de un empleado (ejemplo)

**EMPLEADO:** DIANA ROBLES SALAZAR

| ID | Monto | Fecha inicio | Fecha fin   | Estado     | Detalles |
|---:|------:|-------------|------------|------------|----------|
| 1  | 20000 | 2020-02-15  | 2021-01-15 | CONCLUIDO  | DETALLES |
| 4  | 10000 | 2023-04-15  | 2024-03-15 | ACTIVO     | DETALLES |



---

## Entregable solicitado (modelado con herramienta CASE)

Utilizando una herramienta CASE, se solicita elaborar el modelado del sistema:

- Procesos de negocio
- Casos de uso
- Requisitos
- Clases
- Datos
- Interfaces
- Componentes
- Despliegue

e incorporar los modelos en un **reporte técnico**, apoyándose en la rúbrica correspondiente. 
