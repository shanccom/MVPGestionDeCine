# Pruebas AVL - Venta de Entradas

## Objetivo
Validar el modulo de venta de entradas usando Analisis de Valores Límite (AVL).

## Variables a validar
- Cantidad de entradas por compra: mínimo 1, máximo 10
- Capacidad de sala: mínimo 20, máximo 300

## AVL para cantidad de entradas

| Valor | Resultado esperado |
|---:|---|
| 0 | Inválido |
| 1 | Válido |
| 2 | Válido |
| 9 | Válido |
| 10 | Válido |
| 11 | Inválido |

## AVL para capacidad de sala

| Valor | Resultado esperado |
|---:|---|
| 19 | Inválido |
| 20 | Válido |
| 21 | Válido |
| 299 | Válido |
| 300 | Válido |
| 301 | Inválido |

## Escenarios combinados recomendados

1. Sala con capacidad 20 y compra de 1 entrada: válido.
2. Sala con capacidad 20 y compra de 10 entradas: válido si no supera el aforo disponible.
3. Sala con capacidad 20 y compra de 11 entradas: inválido por cantidad.
4. Sala con capacidad 19 y compra de 1 entrada: inválido por capacidad.
5. Sala con capacidad 300 y compra de 10 entradas: válido si el aforo disponible lo permite.
6. Sala con capacidad 301 y compra de 1 entrada: inválido por capacidad.

## Observaciones
Si ya existen ventas activas para una función, el límite real se calcula como:

capacidad disponible = capacidad de sala - entradas vendidas activas

Por eso, aunque la cantidad esté en rango, la venta puede fallar por control de aforo.
