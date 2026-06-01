# Modulo Funciones

## Descripcion funcional

El modulo Funciones permite registrar, listar, actualizar, buscar y eliminar funciones de cine. Cada funcion relaciona una pelicula y una sala mediante sus IDs, junto con fecha, hora y precio.

## Responsabilidades del modelo

- Representar la entidad Funcion.
- Validar pelicula, sala, fecha, hora y precio.
- Convertir la entidad a diccionario para JSON.
- Reconstruir la entidad desde un diccionario.

## Responsabilidades del repository

- Crear el archivo JSON si no existe.
- Leer y escribir funciones en `src/storage/funciones/funciones.json`.
- Mantener la plantilla con `comentario` e `items`.
- Generar `id_funcion` automaticamente.
- Convertir entre objetos Funcion y diccionarios.
- Buscar, actualizar y eliminar funciones por ID.

## Responsabilidades del servicio

- Exponer las operaciones del modulo a la interfaz y pruebas.
- Crear funciones usando el modelo de dominio.
- Obtener todas las funciones.
- Buscar por ID.
- Actualizar y eliminar funciones existentes.

## Responsabilidades de la interfaz

- Mostrar un formulario para registrar y editar funciones.
- Mostrar una tabla con las funciones registradas.
- Permitir seleccionar una fila para editar o eliminar.
- Mostrar mensajes de exito o error usando los mismos componentes Tkinter del proyecto.

## Flujo de almacenamiento JSON

1. La interfaz envia los datos al servicio.
2. El servicio construye una instancia de Funcion.
3. El repository asigna el siguiente `id_funcion` si corresponde.
4. La funcion se convierte a diccionario.
5. El diccionario se guarda dentro de `items` en el archivo JSON.


# Correcciones de interfaz

Necesito realizar algunos ajustes en la interfaz del módulo **Funciones**.

Analiza cómo se muestran actualmente los datos y aplica únicamente las siguientes correcciones:

## 1. Selección de película

Actualmente se utiliza el ID de la película.

Modificar la interfaz para que el usuario pueda seleccionar una película desde una lista de películas existentes.

Requisitos:

* Cargar las películas registradas en el sistema.
* Mostrar el nombre/título de la película al usuario.
* Mantener internamente la referencia que utiliza la arquitectura actual del proyecto.
* No solicitar que el usuario escriba manualmente el ID.

---

## 2. Selección de sala

Actualmente se utiliza el ID de la sala.

Modificar la interfaz para que el usuario pueda seleccionar una sala desde una lista de salas existentes.

Requisitos:

* Cargar las salas registradas en el sistema.
* Mostrar un nombre descriptivo de la sala.
* Mantener internamente la referencia utilizada por el sistema.
* No solicitar que el usuario escriba manualmente el ID.

---

## 3. Campo fecha

Mejorar la experiencia de ingreso de fecha.

Requisitos:

* Mostrar una ayuda visual o placeholder con el formato esperado.
* Utilizar el formato:

yyyy-mm-dd

Ejemplo:

2026-07-15

No modificar la lógica de almacenamiento existente.

---

## 4. Campo hora

Mejorar la experiencia de ingreso de hora.

Requisitos:

* Mostrar una ayuda visual o placeholder con el formato esperado.
* Utilizar el formato:

hh:mm

Ejemplo:

19:30

No modificar la lógica de almacenamiento existente.

---

## Restricciones

1. No modificar la arquitectura del módulo.
2. No modificar repositories ni modelos salvo que sea estrictamente necesario.
3. Limitar los cambios principalmente a la capa de interfaz.
4. Mantener el mismo estilo visual utilizado por los demás módulos.
5. No agregar nuevas funcionalidades distintas a las solicitadas.
