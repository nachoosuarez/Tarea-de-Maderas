# Etapa 2 — Correccion a condiciones de referencia (UNE-EN 384:2016 §5.4)

Generado por `scripts/03_correcciones_en384.py`. Salida completa en
`resultados/03_valores_corregidos.csv` (258 filas).

Condiciones de referencia: `u_ref` = 12 %, canto 150 mm, luz 18h.
Piezas truncadas a u = 18 %: **0**.
Ajuste de densidad por 1,05 (§5.3.4): **NO aplicado**.

## Factores geometricos por muestra

| Muestra | n  | h medio [mm] | a_f [mm] | 48h [mm] | l_et [mm] | k_h             | k_l             |
|---------|----|--------------|----------|----------|-----------|-----------------|-----------------|
| 1       | 89 | 93,94        | 564,0    | 4509,0   | 4591,4    | 1,0934 – 1,1046 | 0,9905 – 1,0007 |
| 2       | 90 | 142,10       | 852,0    | 6820,7   | 6974,6    | 1,0065 – 1,0143 | 0,9922 – 0,9999 |
| 3       | 79 | 189,83       | 1139,9   | 9112,0   | 9273,6    | 1,0000 – 1,0000 | 0,9925 – 0,9999 |

`a_f = l - 2a` es la separacion entre los dos puntos de carga; `l_et = l + 5*a_f`.
La muestra 3 tiene canto > 150 mm, por eso ahi `k_h = 1`.

## Resistencia a flexion corregida `f_m,ref` [N/mm2]

| Muestra  | n   | media | s     | CoV    | min   | mediana | max   |
|----------|-----|-------|-------|--------|-------|---------|-------|
| 1        | 89  | 33,78 | 6,85  | 20,3 % | 16,95 | 33,19   | 58,49 |
| 2        | 90  | 38,88 | 6,67  | 17,1 % | 26,15 | 38,42   | 60,22 |
| 3        | 79  | 39,83 | 10,52 | 26,4 % | 23,57 | 37,32   | 84,60 |
| **Lote** | 258 | 37,41 | 8,50  | 22,7 % | 16,95 | 36,45   | 84,60 |

## Modulo de elasticidad `E_0` [N/mm2]

| Muestra  | n   | media | s    | CoV    | min   | mediana | max   |
|----------|-----|-------|------|--------|-------|---------|-------|
| 1        | 89  | 13706 | 1798 | 13,1 % | 8514  | 13742   | 19661 |
| 2        | 90  | 13388 | 1442 | 10,8 % | 10314 | 13236   | 17182 |
| 3        | 79  | 13839 | 1991 | 14,4 % | 9782  | 13529   | 19355 |
| **Lote** | 258 | 13636 | 1751 | 12,8 % | 8514  | 13486   | 19661 |

## Densidad corregida `ro_ref` [kg/m3]

| Muestra  | n   | media | s    | CoV   | min   | mediana | max   |
|----------|-----|-------|------|-------|-------|---------|-------|
| 1        | 89  | 450,0 | 27,0 | 6,0 % | 389,7 | 449,1   | 519,5 |
| 2        | 90  | 417,3 | 25,1 | 6,0 % | 367,8 | 415,2   | 490,7 |
| 3        | 79  | 447,3 | 30,4 | 6,8 % | 379,8 | 444,7   | 522,4 |
| **Lote** | 258 | 437,8 | 31,2 | 7,1 % | 367,8 | 436,8   | 522,4 |

## Efecto de la correccion sobre la media de cada muestra

| Muestra | f_m     | E_0     | ro      |
|---------|---------|---------|---------|
| 1       | -8,60 % | -0,03 % | 0,01 %  |
| 2       | -0,63 % | 0,07 %  | -0,03 % |
| 3       | 0,35 %  | -0,04 % | 0,02 %  |

Quien manda es `k_h`, y solo en la muestra 1: con h ~ 94 mm el factor vale 1,099 y
la resistencia media cae un 8,6 % al llevarla al canto de referencia de 150 mm. En
la muestra 2 (h ~ 142 mm) `k_h` apenas vale 1,010 y el efecto neto es del -0,6 %,
porque `k_l` empuja en sentido contrario. En la muestra 3 `k_h` no aplica y queda
solo `k_l`, con un +0,35 %.

Las correcciones por humedad son despreciables (menos del 0,1 % en media) porque la
humedad media de las tres muestras cae entre 11,96 % y 12,07 %, practicamente sobre
el 12 % de referencia. Aun asi se aplican pieza a pieza como exige el §5.4.1: a
nivel individual el rango va de 9,8 % a 13,9 % y ahi la correccion del modulo llega
al 2 %.

**Estos son los valores que entran a la etapa 3** (EN 14358:2016).
