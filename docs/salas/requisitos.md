# Requisitos del módulo Sala

## 1. Objetivo del módulo

Proporcionar una interfaz robusta para el registro, consulta, actualización y eliminación (Ciclo CRUD) de las salas del cine. El módulo garantiza la consistencia de los datos físicos e identificadores de las salas (`numero` y `capacidad`) mediante un blindaje sintáctico y semántico estricto, sin gestionar asientos individuales y enfocándose en la administración general del aforo.

## 2. Requisitos funcionales

- **Registrar sala**: Permitir la creación de una nueva sala ingresando su `numero` y `capacidad`. El sistema asignará automáticamente el `id_sala`.
- **Listar salas**: Mostrar un listado completo de las salas registradas, ordenado de forma ascendente por el campo `numero`.
- **Buscar sala**: Permitir la búsqueda y recuperación de una sala específica mediante la coincidencia exacta de su `numero`.
- **Ver detalle**: Visualizar la información completa de una sala (`id_sala`, `numero`, `capacidad`).
- **Editar sala**: Permitir la modificación de los campos `numero` y `capacidad` de una sala existente, reevaluando todas las validaciones y reglas de negocio.
- **Eliminar sala**: Permitir la baja de una sala del sistema, previa validación estricta de sus dependencias (funciones programadas).

## 3. Requisitos no funcionales

- **Rendimiento**: Las consultas de listado y búsqueda deben resolverse en un tiempo ≤ 2 segundos, incluso con el sistema a máxima carga.
- **Seguridad**: Solo usuarios autenticados con rol de `Administrador` o `Encargado` tendrán permisos para crear, editar o eliminar salas.
- **Usabilidad / Manejo de errores**: El sistema debe capturar excepciones técnicas (`TypeError`, `ValueError`) y traducirlas a mensajes de error claros para el usuario, indicando el campo afectado y la naturaleza del error. Ejemplo: "El número de sala debe ser un valor numérico entero".
- **Auditoría**: Debe registrarse internamente el usuario, la acción realizada (`Alta`, `Modificación`, `Baja`) y la marca de tiempo para cada operación que altere el estado de las salas.

## 4. Reglas de negocio

### 4.1 Generación de ID

- `id_sala` es administrado de manera interna e incremental por el sistema.
- No puede ser proporcionado durante la creación ni modificado posteriormente.

### 4.2 Identificador físico (`numero`)

- Es un campo obligatorio.
- Blindaje sintáctico: Debe ser estrictamente de tipo `int`.
  - Si no es `int`, se debe lanzar `TypeError`.
- Blindaje semántico: Debe ser un entero positivo (`>= 1`).
  - Si es negativo o cero, se debe lanzar `ValueError`.
- Unicidad del número: No pueden existir dos salas con el mismo `numero` en el sistema.
  - Registrar o actualizar una sala con un `numero` ya existente será rechazado.

### 4.3 Capacidad

- Es un campo obligatorio.
- Blindaje sintáctico: Debe ser estrictamente de tipo `int`.
  - Si no es `int`, se debe lanzar `TypeError`.
- Blindaje semántico: Debe estar comprendido en el rango de `1` a `300` asientos inclusive.
  - Si está fuera de ese rango, se debe lanzar `ValueError`.

### 4.4 Integridad referencial

- Está prohibido eliminar una sala que tenga funciones programadas asociadas en el sistema.
- La eliminación solo puede proceder si no existen dependencias de funciones en esa sala.
