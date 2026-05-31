# Requisitos del modulo Pelicula

## Objetivo del modulo
Permitir el registro, consulta, actualizacion y baja de peliculas con datos consistentes (titulo, genero, duracion y clasificacion) para habilitar su uso en la programacion de funciones y operaciones del cine.

## Campos del modulo

| Campo | Tipo | Descripcion | Reglas clave |
| --- | --- | --- | --- |
| titulo | Texto | Nombre comercial de la pelicula | Obligatorio, 1 a 100 caracteres, unico (sin distinguir mayusculas) |
| genero | Texto (catalogo) | Categoria de la pelicula | Obligatorio, valor del catalogo: Accion, Comedia, Drama, Terror, Animacion, Ciencia Ficcion, Documental, Romance, Aventura, Fantasia |
| duracion | Entero (min) | Duracion en minutos | Obligatorio, 1 a 300 |
| clasificacion | Texto (catalogo) | Restriccion de edad | Obligatorio, valor del catalogo: APT, 14+, 18+ |

## Requisitos funcionales
1. Registrar una pelicula con los cuatro campos definidos.
2. Consultar el listado de peliculas con paginacion y orden por titulo.
3. Buscar peliculas por titulo (coincidencia parcial) y filtrar por genero y clasificacion.
4. Visualizar el detalle de una pelicula.
5. Editar una pelicula existente.
6. Eliminar una pelicula cuando no tenga funciones asociadas.
7. Validar reglas de negocio y mostrar mensajes de error claros al usuario.
8. Evitar duplicidad de titulo (sin distinguir mayusculas y con espacios recortados).

## Requisitos no funcionales
1. Rendimiento: el listado y filtros deben responder en <= 2 s con hasta 10,000 peliculas.
2. Seguridad: solo usuarios con rol administrador o encargado pueden crear, editar o eliminar peliculas.
3. Usabilidad: mensajes de validacion deben indicar el campo y la causa del error.
4. Disponibilidad: el modulo debe estar disponible al menos 99.5% del tiempo mensual.
5. Auditoria: registrar fecha, usuario y accion para alta, edicion y eliminacion.

## Reglas de negocio
1. El titulo es obligatorio, se recortan espacios laterales y no se aceptan cadenas vacias.
2. El titulo debe ser unico sin distinguir mayusculas.
3. La duracion es un entero en minutos dentro del rango 1 a 300.
4. El genero debe pertenecer al catalogo permitido.
5. La clasificacion debe pertenecer al catalogo permitido.
6. No se permite eliminar una pelicula que tenga funciones asociadas.
