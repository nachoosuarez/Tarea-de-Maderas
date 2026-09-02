# Semana 4 — Valores característicos

Cubre la **Etapa 3**. Se pasa de 258 valores individuales a tres números que representan al
lote entero. Son dos pasos encadenados y cada uno usa una norma distinta.

**Entregable:** `f_m,k`, `E_0,mean` y `ro_k` del lote, más la tabla estadística por submuestra
que va como **Anexo B**.

---

## Paso 1 — Por submuestra (UNE-EN 14358:2016, método paramétrico)

La letra pide explícitamente el **procedimiento paramétrico actualizado**. La ruta vieja de
EN 384:2010 (ordenar la muestra y contar el 5 %, con `k_s` y `k_v`, diapositiva p.44) **no se
usa**: es justamente el cambio que introdujo la actualización de 2016.

Para cada una de las 3 muestras:

**Resistencia a flexión — log-normal**
```
y_med = (1/n) · SUMA ln(m_i)
s_y   = máx{ raíz[ SUMA (ln m_i − y_med)² / (n−1) ] ; 0,05 }
m_k   = exp(y_med − k_s(n) · s_y)
```

**Densidad — normal**
```
y_med = (1/n) · SUMA m_i
s_y   = máx{ raíz[ SUMA (m_i − y_med)² / (n−1) ] ; 0,05 · y_med }
m_k   = y_med − k_s(n) · s_y
```

**Módulo de elasticidad** — valor **medio** de la submuestra. No es percentil.

`k_s(n) = (6,5n + 6) / (3,7n − 3)`, según S03E02 p.51.
**VERIFICAR** contra la tabla de la norma antes de usarlo, y revisar ahí también el factor
`k_tol` que EN 384 §5.5.1 menciona.

> Con n del orden de 80-90 por muestra, `k_s(n)` queda cerca de 1,8. Conviene calcularlo, no
> tomarlo de tabla redondeada.

## Paso 2 — Combinación de las 3 submuestras (EN 384:2016 §5.5.2.2)

Como la clasificación es **visual**, corresponde el §5.5.2.2 con el factor `k_n` de la
**Tabla 1**. Con n_s = 3 submuestras: **k_n = 0,90** para resistencias, **k_n = 0,94** para
módulo y densidad.

```
(11)  f_m,k    = mín{ 1,2·f_05,i,mín  ; SUMA(n_i·f_05,i)/n  } · 0,90
(12)  E_0,mean = mín{ 1,1·E_i,mín     ; SUMA(n_i·E_i)/n     } · 0,94 / 0,95
(13)  ro_k     = mín{ 1,1·ro_05,i,mín ; SUMA(n_i·ro_05,i)/n } · 0,94
```

El término del mínimo penaliza que una submuestra sea mucho peor que las otras. **Hay que
decir en el informe cuál de los dos términos gobernó en cada caso**: si gobierna el
`1,2 · mínimo`, significa que el lote no es homogéneo y la clasificación visual dejó pasar
una muestra floja.

## Checklist

- [x] Leer la EN 14358:2016 del PDF y confirmar `k_s(n)` y `k_tol` contra la tabla
- [x] `f_05,i` de cada muestra por el método log-normal
- [x] `ro_05,i` de cada muestra por el método normal
- [x] `E_i` medio de cada muestra
- [x] Tabla estadística por submuestra: n, media, desvío, CV, percentil (§5.1 y Anexo C)
- [x] Aplicar (11), (12) y (13) con los `k_n` correctos
- [x] Anotar qué término del mínimo gobernó en cada fórmula

---

# Resultado

Lo produce `scripts/04_valores_caracteristicos.py`, que lee
`resultados/03_valores_corregidos.csv` y escribe `04_por_submuestra.csv`,
`04_valores_lote.csv` y `04_resumen_etapa3.md`. Después hay que correr el `90` para que el
informe se entere:

```bash
python scripts/04_valores_caracteristicos.py && python scripts/90_tablas_informe.py
```

## Por submuestra

| Muestra | n | `k_s(n)` | `f_05` [N/mm²] | `ro_05` [kg/m³] | `E` medio [N/mm²] |
|---|---|---|---|---|---|
| 1 | 89 | 1,7913 | 22,97 | 401,6 | 13 706 |
| 2 | 90 | 1,7909 | 28,29 | 372,3 | 13 388 |
| 3 | 79 | 1,7957 | 24,90 | 392,8 | 13 839 |

## Del lote

| Magnitud | Media ponderada | Tope sobre la peor | Gobierna | `k_n` | **Valor** |
|---|---|---|---|---|---|
| `f_m,k` [N/mm²] | 25,42 | 27,56 | media ponderada | 0,90 | **22,88** |
| `E_0,mean` [N/mm²] | 13 636 | 14 727 | media ponderada | 0,94 | **13 492** |
| `ro_k` [kg/m³] | 388,7 | 409,6 | media ponderada | 0,94 | **365,4** |

En las tres **gobierna la media ponderada**, no el término acotado por la submuestra más
floja: el lote es razonablemente homogéneo pese a las tres escuadrías.

## Decisiones que se tomaron y por qué

- **Distribución de la resistencia: log-normal.** Es la que impone §3.2.2 c) salvo prueba en
  contrario. Se contrastó igual con el estadístico `D` de Kolmogorov-Smirnov y la log-normal
  ajusta mejor en las tres submuestras (0,052 / 0,038 / 0,085 contra 0,086 / 0,064 / 0,130),
  así que no hay motivo para apartarse. Vale saber que la normal habría dado bastante menos
  (21,50 / 26,94 / 20,94 contra 22,97 / 28,29 / 24,90).
- **`k_s(n)` por la fórmula (10) y no por la Tabla 1.** Los n no están tabulados. La
  diferencia se calculó: con el 1,81 de tabla, `f_m,k` baja a 22,80 (−0,35 %) y `ro_k` a
  364,9 (−0,12 %). No cambia nada.
- **El piso de CoV del 0,05 no se activó** en ninguna submuestra ni en ninguna variable.

## Lo que esto anticipa de la semana 5

`f_m,k = 22,88 N/mm²` no llega a los 24 que pide la C24, mientras que `E_0,mean` y `ro_k`
quedan muy por encima de lo que exigiría cualquier clase de ese entorno. O sea que
**gobierna la resistencia**, no la rigidez. **VERIFICAR** contra la tabla de EN 338:2010,
que todavía no se leyó — es la tarea de la semana que viene.

## Duda abierta para el docente

Sigue sin resolverse **cómo se midió la densidad**. Si fue sobre pieza completa corresponde
dividir por 1,05 (EN 384 §5.3.4) y `ro_k` bajaría a ≈348 kg/m³. Con el margen que hay hoy
no parece que cambie la clase, pero hay que preguntarlo igual.
