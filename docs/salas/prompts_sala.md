# Prompt 1: Analista de Requisitos y QA (Generación de Documentación)

Actúa como Analista de Requisitos y QA.
Genera la documentación completa para el módulo de Salas de un sistema de gestión de cine, adaptando un modelo previo basado en blindaje sintáctico y semántico.

## Campos del módulo

- `id_sala`: Entero, identificador único interno, autogenerado por el sistema. No modificable.
- `numero`: Entero, número físico o comercial de la sala (Ej.: 1, 2, 3). Obligatorio, debe ser un número entero mayor o igual a 1.
- `capacidad`: Entero, número máximo de asientos disponibles. Obligatorio, rango válido de 1 a 300.

## Reglas de negocio clave

- `id_sala` se asigna automáticamente al guardar y no puede ser modificado por el usuario.
- `numero` de sala es obligatorio y debe validar estrictamente el tipo `int`; lanzar `TypeError` si no lo es y `ValueError` si es negativo o cero.
- `numero` de sala debe ser único en el sistema. No se permiten duplicados en persistencia.
- `capacidad` debe validar estrictamente el tipo `int` y estar en el rango de 1 a 300; lanzar `ValueError` en caso de violación.
- No se permite eliminar una sala si tiene funciones programadas asociadas.

## Secciones requeridas en Markdown

Genera exactamente las siguientes secciones estructuradas en Markdown:

1. Objetivo del módulo
   - Ciclo CRUD
   - Consistencia de datos
   - Sin gestión de asientos individuales
2. Requisitos funcionales
   - Registrar sala con ID automático
   - Listar salas ordenadas por `numero`
   - Buscar sala por número exacto
   - Ver detalle de una sala
   - Editar `numero` y `capacidad`
   - Eliminar sala con validación de dependencia
3. Requisitos no funcionales
   - Rendimiento: consultas en <= 2s
   - Seguridad: roles `admin` / `encargado`
   - Mensajes de error claros que indiquen tipo de error y campo
   - Auditoría de cambios
4. Reglas de negocio detalladas
5. Escenarios Gherkin en español
   - Creación exitosa
   - Error por duplicado de número
   - Error por capacidad fuera de rango
   - Bloqueo de eliminación por funciones asociadas
6. Casos de Partición de Equivalencia (PE) en formato tabla
   - Para `numero`
   - Para `capacidad`
   - Incluir tipos de datos inválidos
7. Casos de Análisis de Valores Límite (AVL) en formato tabla
   - Para fronteras de `numero`
   - Para fronteras de `capacidad`

## Archivos de salida

La documentación debe quedar lista para colocarse directamente en:

- `docs/salas/requisitos.md`
- `features/sala.feature`
- `docs/salas/casos_pe_avl.md`

# Prompt 2: QA Engineer (Generación de Tests con Pytest)

Actúa como QA Engineer experto en Pytest.
Basándote en los requisitos, reglas de negocio, tablas de PE, AVL y escenarios Gherkin del nuevo módulo de Salas (`docs/salas/*` y `features/sala.feature`), genera el archivo completo de pruebas unitarias.

## Requisitos de diseño para las pruebas

- Utilizar el framework `pytest`.
- Crear una prueba por cada caso de Partición de Equivalencia (PE).
- Crear una prueba por cada caso de Análisis de Valores Límite (AVL).
- Crear pruebas específicas para los flujos de negocio descritos en Gherkin.
- Utilizar nombres de funciones altamente descriptivos, por ejemplo: `test_crear_sala_con_capacidad_invalida_lanza_value_error`.
- Validar el blindaje sintáctico usando `pytest.raises(TypeError)` para tipos incorrectos y `pytest.raises(ValueError)` para infracciones de rango o consistencia.

## Restricciones

- No generes la implementación de la clase `Sala`.
- Solo genera de forma limpia y organizada el archivo: `tests/test_sala.py`.

# Prompt 3: Desarrollador Python Senior (Refactorización del Modelo)

Actúa como desarrollador Python senior.
Refactoriza e implementa la clase `Sala` en `models/sala.py`, basándote en la estructura previa del sistema pero adaptada al nuevo CRUD sin asientos.
Debe pasar el 100% de los tests de `tests/test_sala.py`.

## Estructura base a respetar y adaptar

```python
class Sala:
    def __init__(self, id_sala: int = None, numero: int = 0, capacidad: int = 0) -> None:
        # 1. Validaciones de Tipo (TypeError)
        # 2. Validaciones de Valores Límite (ValueError: número > 0, capacidad 1-300)
        # 3. Asignación de propiedades
```

## Requisitos adicionales

- Incluir los métodos de serialización física: `to_dict(self) -> dict` y el método estático `from_dict(data: dict) -> "Sala"`, adaptados únicamente a los campos `id_sala`, `numero` y `capacidad`.
- Asegurar tipado estricto con `Type Hinting`.
- Escribir código limpio orientado a objetos siguiendo PEP 8.

## Restricciones

- No agregues lógica de almacenamiento en archivos ni componentes de interfaz de usuario en `models/sala.py`.

# Prompt 4: Desarrollador Python (Repositorio JSON Autoincremental)

Actúa como desarrollador Python.
Diseña un componente de persistencia para el módulo de salas que controle el ciclo CRUD y la autogeneración del identificador numérico único.

- Archivo físico: `data/salas.json`

## Implementación requerida

Implementa la clase `SalaRepository` con las siguientes funciones:

- `guardar(sala)`:
  - Si la sala no tiene `id_sala`, calcula el siguiente entero autoincremental disponible y se lo asigna.
  - Valida que el `numero` de sala no esté duplicado en el JSON.
  - Escribe el registro en el archivo.
  - Si ya tiene `id_sala`, actualiza sus valores.
- `listar()`: Carga el JSON, mapea los diccionarios a instancias de `Sala` mediante `from_dict` y devuelve la lista ordenada por `numero`.
- `buscar_por_id(id_sala)`: Retorna la instancia de sala correspondiente o `None`.
- `eliminar(id_sala)`: Elimina el registro del JSON.
  - Debe simular o aceptar un parámetro para validar la regla de negocio: "No se puede eliminar si tiene funciones asociadas".
  - Lanzar `ValueError` si esta regla falla.

## Restricciones

- Utiliza la clase `Sala` previamente construida.
- Archivo resultante en: `repositories/sala_repository.py`.

# Prompt 5: Desarrollador Tkinter (Interfaz Gráfica para Salas)

Actúa como desarrollador Tkinter experto.
Genera el archivo de interfaz gráfica `ui/sala_ui.py` para la administración completa del módulo de salas.

## Requisitos de la UI

- Un componente `ttk.Treeview` que liste todas las salas mostrando columnas para: `ID Sala`, `Número de Sala` y `Capacidad Máxima`.
- Formulario integrado o ventana emergente para registrar y editar salas.
- El campo `ID` debe ser de solo lectura o estar oculto (autoincremental).
- Control de entradas de texto numéricas para que solo acepten enteros antes de enviarlos al modelo.
- Uso de ventanas de diálogo `messagebox` para:
  - Confirmar eliminaciones exitosas.
  - Mostrar alertas críticas en caso de fallos de validación (`TypeError`, `ValueError`).
- Conexión directa con `repositories/sala_repository.py`.
