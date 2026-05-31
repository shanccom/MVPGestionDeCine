# Casos PE y AVL del modulo Funciones

## Particion de Equivalencia

| Campo | Caso valido | Caso invalido |
| --- | --- | --- |
| Pelicula | `1` | `None` |
| Sala | `1` | `None` |
| Fecha | `2026-06-01` | cadena vacia |
| Hora | `18:30` | cadena vacia |
| Precio | `15.00` | `0` o `-1` |

## Analisis de Valores Limite

| Campo | Limite valido | Justo fuera del limite |
| --- | --- | --- |
| Precio | `0.01` | `0` |
| Fecha | `1900-01-01` y `9999-12-31` | formato `2026/06/01` |
| Hora | `00:00` y `23:59` | `24:00` |

## Ejemplos de pruebas

- Registrar una funcion con pelicula `1`, sala `1`, fecha `2026-06-01`, hora `18:30` y precio `15.00`.
- Rechazar una funcion sin pelicula.
- Rechazar una funcion sin sala.
- Rechazar una funcion sin fecha u hora.
- Rechazar precios menores o iguales a cero.
- Aceptar horas limite `00:00` y `23:59`.
