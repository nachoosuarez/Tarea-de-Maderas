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

- [ ] Leer la EN 14358:2016 del PDF y confirmar `k_s(n)` y `k_tol` contra la tabla
- [ ] `f_05,i` de cada muestra por el método log-normal
- [ ] `ro_05,i` de cada muestra por el método normal
- [ ] `E_i` medio de cada muestra
- [ ] Tabla estadística por submuestra: n, media, desvío, CV, percentil (Anexo B)
- [ ] Aplicar (11), (12) y (13) con los `k_n` correctos
- [ ] Anotar qué término del mínimo gobernó en cada fórmula
