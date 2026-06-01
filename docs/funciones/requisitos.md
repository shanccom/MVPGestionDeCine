# Requisitos del modulo Funciones

## Objetivo

Gestionar las funciones de cine disponibles, relacionando una pelicula con una sala, fecha, hora y precio.

## Entidad

La entidad Funcion representa una programacion concreta dentro del cine.

## Campos

| Campo | Tipo | Restriccion |
| --- | --- | --- |
| id_funcion | Integer | Autogenerado |
| pelicula | Integer | Obligatorio, referencia a pelicula |
| sala | Integer | Obligatorio, referencia a sala |
| fecha | String | Obligatorio, formato YYYY-MM-DD |
| hora | String | Obligatorio, formato HH:MM |
| precio | Float | Obligatorio, mayor a 0 |

## Reglas de negocio MVP

- Toda funcion debe tener pelicula y sala asociadas por ID.
- La fecha y la hora son obligatorias.
- El precio debe ser mayor a cero.
- El identificador de funcion se genera automaticamente al guardar.

## Casos de uso basicos

- Registrar una funcion.
- Listar funciones registradas.
- Buscar una funcion por ID.
- Actualizar los datos de una funcion.
- Eliminar una funcion existente.
