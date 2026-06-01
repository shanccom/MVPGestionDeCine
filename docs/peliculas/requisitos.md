# Requisitos del modulo Pelicula

## Objetivo del modulo
Permitir el registro, consulta, actualizacion y baja de peliculas con datos consistentes (id_pelicula, titulo, genero y duracion) para habilitar su uso en la programacion de funciones y operaciones del cine.

## Campos del modulo

| Campo | Tipo | Descripcion | Reglas clave |
| --- | --- | --- | --- |
| id_pelicula | Entero | Identificador unico | Autogenerado |
| titulo | Texto | Nombre comercial de la pelicula | Obligatorio, 1 a 100 caracteres |
| genero | Texto (catalogo) | Categoria de la pelicula | Obligatorio, valor del catalogo: Accion, Comedia, Drama, Terror, Animacion, Ciencia Ficcion, Documental, Romance, Aventura, Fantasia |
| duracion | Entero (min) | Duracion en minutos | Obligatorio, 60 a 240 |

## Requisitos funcionales
1. Registrar una pelicula con los campos definidos y asignar id_pelicula automaticamente.
2. Consultar el listado de peliculas con paginacion y orden por titulo.
4. Visualizar el detalle de una pelicula.
5. Editar una pelicula existente.
6. Eliminar una pelicula cuando no tenga funciones asociadas.
7. Validar reglas de negocio y mostrar mensajes de error claros al usuario.

## Requisitos no funcionales
1. Rendimiento: el listado y filtros deben responder en <= 2 s con hasta 10,000 peliculas.
3. Usabilidad: mensajes de validacion deben indicar el campo y la causa del error.

## Reglas de negocio
1. id_pelicula se asigna automaticamente y no puede ser modificado.
2. El titulo es obligatorio, se recortan espacios laterales y no se aceptan cadenas vacias.
3. La duracion es un entero en minutos dentro del rango 60 a 240.
4. El genero debe pertenecer al catalogo permitido.
5. No se permite eliminar una pelicula que tenga funciones asociadas.