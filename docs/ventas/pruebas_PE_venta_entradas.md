# Pruebas PE - Venta de Entradas

## Objetivo
Validar el modulo de venta de entradas usando Particion de Equivalencia (PE) para la cantidad de entradas, capacidad de sala y control de aforo.

## Regla principal
- Cantidad de entradas por compra: 1 a 10
- Capacidad de sala: 20 a 300
- No se debe vender mas entradas que la capacidad disponible

## PE para cantidad de entradas

| Clase | Valor de entrada | Resultado esperado |
|---|---:|---|
| Válida | 5 | Acepta la venta |
| Inválida | 0 | Rechaza la venta |
| Inválida | 15 | Rechaza la venta |

## PE para capacidad de sala

| Clase | Valor de entrada | Resultado esperado |
|---|---:|---|
| Válida | 100 | Permite evaluar la venta |
| Inválida | 10 | Rechaza por capacidad fuera de rango |
| Inválida | 500 | Rechaza por capacidad fuera de rango |

## PE para control de aforo

| Clase | Escenario | Resultado esperado |
|---|---|---|
| Válida | Sala de 100 asientos, ya vendidas 40, compra de 5 | Registra la venta |
| Inválida | Sala de 100 asientos, ya vendidas 98, compra de 5 | No registra la venta |
| Inválida | Sala de 20 asientos, ya vendidas 20, compra de 1 | No registra la venta |

## Casos sugeridos

1. Venta válida con 3 entradas en una sala con capacidad 100 y 0 ventas previas.
2. Venta inválida con 0 entradas.
3. Venta inválida con 15 entradas.
4. Venta inválida cuando el aforo disponible es menor que la cantidad solicitada.
5. Cancelación de una venta registrada y verificacion de que el estado cambie a CANCELADA.

## Criterio de aceptación
La venta solo se registra cuando la cantidad solicitada está entre 1 y 10 y la suma de ventas activas no supera la capacidad de la sala.
