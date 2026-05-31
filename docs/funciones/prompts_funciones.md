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
