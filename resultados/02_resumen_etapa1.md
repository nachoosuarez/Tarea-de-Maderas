# Etapa 1 — Propiedades por pieza (UNE-EN 408:2010)

Generado por `scripts/02_propiedades_por_pieza.py`. Salida completa en
`resultados/02_propiedades_por_pieza.csv` (258 filas).

**Valores SIN corregir a condiciones de referencia.** La correccion es la etapa 2.

## Resistencia a flexion `f_m` [N/mm2]

| Muestra  | n   | media | s     | CoV    | min   | mediana | max   |
|----------|-----|-------|-------|--------|-------|---------|-------|
| 1        | 89  | 36,96 | 7,50  | 20,3 % | 18,55 | 36,31   | 64,00 |
| 2        | 90  | 39,12 | 6,71  | 17,1 % | 26,32 | 38,66   | 60,60 |
| 3        | 79  | 39,69 | 10,48 | 26,4 % | 23,41 | 37,27   | 84,15 |
| **Lote** | 258 | 38,55 | 8,34  | 21,6 % | 18,55 | 37,39   | 84,15 |

## Modulo de elasticidad local `E_m,l` [N/mm2]

| Muestra  | n   | media | s    | CoV    | min   | mediana | max   |
|----------|-----|-------|------|--------|-------|---------|-------|
| 1        | 89  | 13709 | 1800 | 13,1 % | 8549  | 13711   | 19721 |
| 2        | 90  | 13379 | 1435 | 10,7 % | 10212 | 13279   | 17286 |
| 3        | 79  | 13844 | 1985 | 14,3 % | 9773  | 13596   | 19202 |
| **Lote** | 258 | 13635 | 1749 | 12,8 % | 8549  | 13513   | 19721 |

## Densidad medida `ro` [kg/m3] (sin corregir por humedad)

| Muestra  | n   | media | s    | CoV   | min   | mediana | max   |
|----------|-----|-------|------|-------|-------|---------|-------|
| 1        | 89  | 449,9 | 27,0 | 6,0 % | 389,5 | 448,6   | 518,8 |
| 2        | 90  | 417,5 | 25,0 | 6,0 % | 369,5 | 417,1   | 489,2 |
| 3        | 79  | 447,2 | 30,5 | 6,8 % | 379,2 | 445,0   | 523,4 |
| **Lote** | 258 | 437,8 | 31,2 | 7,1 % | 369,5 | 436,4   | 523,4 |

## Control de coherencia

- La dispersion de `f_m` (CoV en torno al 20-25 %) es la esperable en madera
  aserrada clasificada visualmente; la del modulo es bastante menor, como
  corresponde a una propiedad de rigidez.
- Ninguna pieza da valor negativo ni nulo en `f_m` ni en `E_m,l`.
