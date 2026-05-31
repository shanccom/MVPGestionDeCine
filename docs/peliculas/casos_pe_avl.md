# Casos de Particion de Equivalencia (PE)

## titulo

| ID | Entrada | Clase | Resultado esperado |
| --- | --- | --- | --- |
| PE-TI-01 | "Matrix" | Valida (1-100) | Acepta |
| PE-TI-02 | "A" | Valida (minimo) | Acepta |
| PE-TI-03 | "" | Invalida (vacio) | Rechaza |
| PE-TI-04 | "   " | Invalida (solo espacios) | Rechaza |
| PE-TI-05 | 101 caracteres | Invalida (>100) | Rechaza |
| PE-TI-06 | " matrix " con existente "Matrix" | Invalida (duplicado) | Rechaza |

## genero

| ID | Entrada | Clase | Resultado esperado |
| --- | --- | --- | --- |
| PE-GE-01 | "Accion" | Valida (catalogo) | Acepta |
| PE-GE-02 | "Fantasia" | Valida (catalogo) | Acepta |
| PE-GE-03 | "Western" | Invalida (fuera de catalogo) | Rechaza |
| PE-GE-04 | "" | Invalida (vacio) | Rechaza |

## duracion

| ID | Entrada | Clase | Resultado esperado |
| --- | --- | --- | --- |
| PE-DU-01 | 90 | Valida (1-300) | Acepta |
| PE-DU-02 | 1 | Valida (minimo) | Acepta |
| PE-DU-03 | 0 | Invalida (<1) | Rechaza |
| PE-DU-04 | 301 | Invalida (>300) | Rechaza |
| PE-DU-05 | -10 | Invalida (negativo) | Rechaza |
| PE-DU-06 | 90.5 | Invalida (no entero) | Rechaza |
| PE-DU-07 | "noventa" | Invalida (no numerico) | Rechaza |


# Casos de Analisis de Valores Limite (AVL)

## titulo (longitud 1 a 100)

| ID | Longitud | Ejemplo | Resultado esperado |
| --- | --- | --- | --- |
| AVL-TI-01 | 0 | "" | Rechaza |
| AVL-TI-02 | 1 | "A" | Acepta |
| AVL-TI-03 | 100 | 100 caracteres | Acepta |
| AVL-TI-04 | 101 | 101 caracteres | Rechaza |

## duracion (rango 1 a 300)

| ID | Valor | Resultado esperado |
| --- | --- | --- |
| AVL-DU-01 | 0 | Rechaza |
| AVL-DU-02 | 1 | Acepta |
| AVL-DU-03 | 300 | Acepta |
| AVL-DU-04 | 301 | Rechaza |

## genero (catalogo)

| ID | Valor | Resultado esperado |
| --- | --- | --- |
| AVL-GE-01 | "Accion" (primero) | Acepta |
| AVL-GE-02 | "Fantasia" (ultimo) | Acepta |
| AVL-GE-03 | "Western" | Rechaza |
