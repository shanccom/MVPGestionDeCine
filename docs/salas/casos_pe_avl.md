# Casos de Partición de Equivalencia (PE) y Análisis de Valores Límite (AVL)

## Partición de Equivalencia (PE)

### Campo: `numero`

| ID | Entrada | Clase de Equivalencia | Tipo de Excepción | Resultado Esperado |
| --- | --- | --- | --- | --- |
| PE-NUM-01 | 5 | Válida (entero positivo) | Ninguna | Acepta |
| PE-NUM-02 | -3 | Inválida (entero negativo) | `ValueError` | Rechaza |
| PE-NUM-03 | 0 | Inválida (cero) | `ValueError` | Rechaza |
| PE-NUM-04 | "Cinco" | Inválida (tipo string) | `TypeError` | Rechaza |
| PE-NUM-05 | 2.5 | Inválida (tipo float) | `TypeError` | Rechaza |
| PE-NUM-06 | None | Inválida (tipo nulo) | `TypeError` | Rechaza |

### Campo: `capacidad`

| ID | Entrada | Clase de Equivalencia | Tipo de Excepción | Resultado Esperado |
| --- | --- | --- | --- | --- |
| PE-CAP-01 | 150 | Válida (rango 1-300) | Ninguna | Acepta |
| PE-CAP-02 | 0 | Inválida (menor al límite) | `ValueError` | Rechaza |
| PE-CAP-03 | 400 | Inválida (mayor al límite) | `ValueError` | Rechaza |
| PE-CAP-04 | "Cien" | Inválida (tipo string) | `TypeError` | Rechaza |
| PE-CAP-05 | 150.5 | Inválida (tipo float) | `TypeError` | Rechaza |
| PE-CAP-06 | None | Inválida (tipo nulo) | `TypeError` | Rechaza |

## Análisis de Valores Límite (AVL)

### Campo: `numero` (Límite inferior: 1)

| ID | Valor Evaluado | Descripción de Frontera | Resultado Esperado |
| --- | --- | --- | --- |
| AVL-NUM-01 | 0 | Justo por debajo del límite mínimo | Rechaza (`ValueError`) |
| AVL-NUM-02 | 1 | Límite mínimo exacto | Acepta |
| AVL-NUM-03 | 2 | Justo por encima del límite mínimo | Acepta |

### Campo: `capacidad` (Rango: 1 a 300)

| ID | Valor Evaluado | Descripción de Frontera | Resultado Esperado |
| --- | --- | --- | --- |
| AVL-CAP-01 | 0 | Justo por debajo del límite inferior | Rechaza (`ValueError`) |
| AVL-CAP-02 | 1 | Límite inferior exacto | Acepta |
| AVL-CAP-03 | 2 | Justo por encima del límite inferior | Acepta |
| AVL-CAP-04 | 299 | Justo por debajo del límite superior | Acepta |
| AVL-CAP-05 | 300 | Límite superior exacto | Acepta |
| AVL-CAP-06 | 301 | Justo por encima del límite superior | Rechaza (`ValueError`) |
