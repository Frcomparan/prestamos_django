# Actividad 6: Sistema de Abonos para Préstamos

**Curso:** Taller de Django  
**Tipo:** Actividad individual
**Tiempo estimado:** 120-150 minutos

---

## 🎯 Objetivo

Implementar un sistema funcional de **abonos para préstamos activos** que permita:

1. **Registrar abonos** en préstamos que estén en estado ACTIVO
2. **Visualizar el historial de abonos** asociados a un préstamo específico
3. **Actualizar automáticamente el estado** del préstamo a CONCLUIDO cuando se haya pagado la totalidad del saldo

El desafío está en que **no hay un enfoque único prescrito**. Tienes libertad para arquitectar la solución de la forma que consideres más lógica y usable.

---

## 📋 Prerrequisitos

Antes de iniciar, asegúrate de tener:

- ✅ Proyecto Django con Docker funcionando
- ✅ App `apps.empleados` con sus vistas web (CRUD de empleados)
- ✅ App `apps.prestamos` creada con los modelos `Prestamo` y `Abono`
- ✅ Migraciones aplicadas correctamente
- ✅ Al menos un préstamo en estado ACTIVO en la base de datos
- ✅ Plantillas base (`base.html`, componentes) ya disponibles

---

## 📖 Contexto del Problema

Actualmente, el sistema tiene:

- Un modelo `Prestamo` que guarda monto total, plazo, saldo actual y estado
- Un modelo `Abono` que registra pagos parciales a un préstamo
- Rutas y vistas de empleados completamente funcionales

Lo que **falta** es la interfaz web para:

- Permitir al usuario registrar un nuevo abono a un préstamo
- Ver el historial de abonos que un préstamo ha recibido
- Validar que solo préstamos ACTIVOS puedan recibir abonos
- Actualizar el estado del préstamo a CONCLUIDO cuando esté completamente pagado

---

## 🎨 Requisitos Funcionales

### RF1: Registrar un Abono

El usuario debe poder crear un nuevo abono asociado a un préstamo activo.

**Criterios de aceptación:**

- Solo se pueden crear abonos para préstamos en estado ACTIVO
- El sistema debe validar esta condición y mostrar un mensaje si el préstamo no es elegible
- Al crear un abono, los campos como `monto_interes`, `monto_capital` y `saldo_actual` deben calcularse automáticamente (según la lógica del modelo)
- El saldo del préstamo debe actualizarse después de registrar el abono
- Si el nuevo saldo es ≤ 0, el préstamo debe cambiar a estado CONCLUIDO

### RF2: Visualizar Abonos de un Préstamo

El usuario debe poder ver el historial completo de abonos que se han registrado para un préstamo específico.

**Criterios de aceptación:**

- Mostrar una tabla o lista con los abonos del préstamo
- Incluir columnas relevantes: número de abono, fecha, monto pagado, interés, saldo restante
- Indicar información del préstamo (empleado, monto original, plazo)
- Ser accesible desde algún punto de la navegación o desde el detalle del préstamo

### RF3: Validaciones de Negocio

El sistema debe respetar las reglas del negocio:

- **Solo préstamos ACTIVO**: No permitir crear abonos en préstamos en otros estados
- **Saldo no negativo**: No permitir un abono que exceda el saldo actual del préstamo
- **Actualizar estado**: Cambiar a CONCLUIDO cuando saldo = 0

---

## 💡 Sugerencias de Implementación

No estás limitado a una única forma de resolver esto. Aquí hay algunas opciones:

### Opción A: Botón "Abonar" en Detalle del Préstamo

1. Crear una vista de detalle para préstamos (`prestamo_detail`)
2. Mostrar información del préstamo: empleado, monto, saldo, estado
3. **Si el préstamo está ACTIVO**: mostrar un botón "Abonar"
4. El botón redirige a una vista `crear_abono` que:
   - Muestra un formulario para registrar el abono (quizá solo el monto, si otros campos se calculan)
   - Valida que el préstamo esté ACTIVO
   - Guarda el abono y actualiza el préstamo
   - Redirige de vuelta al detalle del préstamo
5. En el mismo detalle, mostrar una **sección de abonos** con el historial

**Ventaja:** Flujo intuitivo, todo en un mismo lugar

### Opción B: CRUD Separado de Abonos

1. Crear vistas independientes para abonos:
   - `abono_list`: lista de todos los abonos (con filtro por préstamo)
   - `abono_create`: crear abono (requiere seleccionar préstamo)
   - `abono_detail`: ver detalles de un abono específico
2. En la vista de empleados, agregar un enlace a los abonos de sus préstamos

**Ventaja:** Mayor modularidad, reutilizable

### Opción C: Híbrida

1. Mantener una vista general de abonos (abono_list)
2. Agregar botón "Abonar" en el detalle del préstamo
3. Usar el mismo formulario en ambos contextos

**Ventaja:** Flexibilidad

---

## 📝 Notas Técnicas

### Campo de Entrada del Formulario

Recuerda que en el modelo `Abono`, muchos campos se calculan automáticamente en el método `save()`:

- `monto_interes` = saldo_actual × (tasa_mensual / 100)
- `monto_capital` = pago_fijo_capital (del préstamo)
- `monto_cobrado` = monto_interes + monto_capital
- `numero_abono` = consecutivo automático

**Por lo tanto**, el formulario podría mostrar solo:

- Una referencia al préstamo (dropdown o lectura)
- Quizá un botón "Registrar Abono" que calcula todo automáticamente

---

## 🛠️ Consideraciones de Diseño

### Rutas Sugeridas

Dependiendo de tu enfoque, considera (No estas limitado a estas dos opciones):

**Opción A (botón en detalle):**

```
/prestamos/              → lista de préstamos
/prestamos/<id>/         → detalle del préstamo + sección de abonos
/prestamos/<id>/abonar/  → crear abono para ese préstamo
```

**Opción B (CRUD separado):**

```
/prestamos/              → lista de préstamos
/prestamos/<id>/         → detalle del préstamo
/abonos/                 → lista de abonos
/abonos/nuevo/           → crear abono
/abonos/<id>/            → detalle del abono
```

### Plantillas

Reutiliza la estructura de `base.html` y componentes existentes. Puedes:

- Crear `prestamos/prestamo_detail.html`
- Crear `abonos/abono_list.html` y `abono_form.html` (si usas CRUD separado)
- O una sección dentro de `prestamo_detail.html` que muestre abonos

No necesitas diseñar CSS nuevo; adapta los estilos existentes.

---

## 📊 Criterios de Evaluación

| Criterio                        | Puntos | Descripción                                             |
| ------------------------------- | ------ | ------------------------------------------------------- |
| **Crear abonos funcionalmente** | 35%    | Formulario y lógica para registrar abonos en BD         |
| **Validaciones correctas**      | 20%    | Solo ACTIVO, saldo no negativo, actualización de estado |
| **Visualizar abonos**           | 35%    | Historial visible y bien presentado                     |
| **Entrega**                     | 10%    | Video de demostración entregado en tiempo y forma       |

**Total:** 100 puntos

---

## 📦 Entregables

Entrega un **Video breve** (max 5 minutos) que incluya:

### 1. Demostración Funcional

- Muestra la creación de un abono en un préstamo ACTIVO
- Muestra el historial de abonos para ese préstamo

## ⚠️ Notas Importantes

### No Hard-codees

- No escribas préstamo_id = 1 en el código
- Siempre obtén los IDs de la URL o del contexto actual

### Manejo de Errores

- Usa `get_object_or_404()` si necesitas obtener un préstamo por ID
- Valida en la vista (lógica) antes de intentar guardar

### Prueba Completamente

- Crea varios préstamos en diferentes estados
- Intenta abonar a cada uno
- Verifica que el saldo se actualice correctamente
- Comprueba que CONCLUIDO se asigne cuando saldo = 0

### Reutiliza el Diseño Existente

- No diseñes CSS nuevo; usa los estilos de `base.html`
- Mantén consistencia visual con empleados

---

## 📚 Recursos Útiles

- Documentación de modelos con relaciones: https://docs.djangoproject.com/es/5.0/ref/models/fields/#foreignkey
- Manejo de formularios: https://docs.djangoproject.com/es/5.0/topics/forms/
- Vistas genéricas: https://docs.djangoproject.com/es/5.0/ref/class-based-views/

---
