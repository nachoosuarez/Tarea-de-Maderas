# Referencias — de dónde sale cada fórmula

Regla del trabajo: **ninguna fórmula, coeficiente ni límite se escribe de memoria.** Todo lo
que entra al informe tiene que poder rastrearse hasta un apartado y una página. Lo que no se
pudo leer de la fuente va marcado **VERIFICAR**.

## Fuentes

| Fuente | Para qué | Dónde está |
|---|---|---|
| **UNE-EN 408:2010** | Método de ensayo y ecuaciones de `f_m` y `E_m` | Vía diapositivas S03E02 |
| **UNE-EN 384:2016** | Ajuste a condiciones de referencia, combinación de submuestras | `LIBROS Y NORMAS\Normas para trabajo de caracterización_Madera.zip` |
| **UNE-EN 14358:2016** | Valores característicos | Mismo zip |
| **UNE-EN 338:2010** | Clases resistentes | Vía diapositivas S03E02 **p.55** (la p.56-57 es la edición 2016). **No está en el zip de AENOR** |
| **S03E02 — Madera aserrada 2** | Diapositivas del curso, 68 páginas | `01-CLAUDE\ESTRUCTURA DE MADERA\Teorico-2025\` |

> Los PDF de las normas **no se suben al repo**: son material licenciado de AENOR. Cada uno
> los tiene en su copia local del zip.

## Trazabilidad de cada fórmula

| # | Qué | Fuente y ubicación |
|---|---|---|
| 1 | Esquema de ensayo a 4 puntos, `l = 18h ± 3h`, `a = 6h ± 1,5h` | S03E02 p.16 |
| 2 | `E_m` con corrección de cortante, y las 5 opciones de `G` | S03E02 p.26 (la opción 5 es `G = E/16`, la que impone la letra) |
| 3 | `f_m = 3·F·a/(b·h²)` | S03E02 p.28 |
| 4 | Muestreo: población, muestras, mínimo de probetas | S03E02 p.30 |
| 5 | Corrección de humedad del módulo | EN 384:2016 §5.4.2 fórm. (2) — S03E02 p.38 |
| 6 | Corrección de humedad de la densidad | EN 384:2016 §5.4.2 fórm. (3) — S03E02 p.46 |
| 7 | `k_h = mín{(150/h)^0,2 ; 1,3}` | EN 384:2016 §5.4.3 fórm. (4) |
| 8 | `k_l = (48h/l_et)^0,2` y `l_et = l + 5·a_f` | EN 384:2016 §5.4.3 fórm. (5) y (6), p.11 |
| 8b | `a_f` = separación entre los dos puntos de aplicación de la carga | EN 384:2016 §5.4.3, p.11 (definición al pie de la fórm. 6) |
| 8c | La resistencia a flexión **no** se corrige por humedad | EN 384:2016 §5.4.2, p.10: la lista de magnitudes ajustables es taxativa y `f_m` no figura |
| 9 | `E0 = E_m,local(u_ref)` | EN 384:2016 §5.4.4 fórm. (8) |
| 10 | Densidad de probeta completa: dividir por 1,05 en coníferas | EN 384:2016 §5.3.4 |
| 11 | Percentiles por submuestra remitidos a EN 14358 | EN 384:2016 §5.5.1 |
| 12 | `f_k`, `E_0,mean`, `ro_k` combinando submuestras | EN 384:2016 §5.5.2.2, fórm. (11)(12)(13) |
| 13 | Factor `k_n` según número de submuestras | EN 384:2016 Tabla 1 |
| 14 | Método paramétrico: log-normal para resistencia, normal para densidad | EN 14358:2016 §3.2.2, p.7-8, fórm. (1) a (6) |
| 14b | `k_s(n) = (6,5n + 6)/(3,7n − 3)` | EN 14358:2016 §3.2.2 f), **fórmula (10)** de la propia norma, p.8, y Tabla 1 |
| 14c | El valor característico medio de una propiedad de rigidez es la media aritmética | EN 14358:2016 §3.3 d), p.10, remite a la fórm. (14) |
| 15 | Tabla 1 de clases resistentes, coníferas C14 a C50 | EN 338:2010 Tabla 1 — S03E02 **p.55**, renderizada a 420 dpi. `f_m,k` 14/16/18/20/22/24/27/30/35/40/45/50 N/mm²; `E_0,medio` 7/8/9/9,5/10/11/11,5/12/13/14/15/16 **kN/mm²**; `ro_k` 290/310/320/330/340/350/370/380/400/420/440/460 kg/m³ |
| 16 | Modelos de tabla para el informe | EN 384:2016 Anexo A (normativo), Tablas A.1 y A.3 |

## Verificado contra la norma (ya no son pendientes)

- **`k_s(n)`** — la expresión `(6,5n + 6)/(3,7n − 3)` **no es solo de la diapositiva**: es la
  fórmula (10) de la propia EN 14358:2016 §3.2.2 f), que la norma admite expresamente como
  alternativa a su Tabla 1. Valores tabulados: n=3 → 3,15; 5 → 2,46; 10 → 2,10; 15 → 1,99;
  20 → 1,93; 30 → 1,87; 50 → 1,81; 100 → 1,76; 500 → 1,69; ∞ → 1,64.
  Para n no tabulado la norma manda **tomar el valor inmediatamente mayor**.
  Con nuestros n: 89 → 1,7913 · 90 → 1,7909 · 79 → 1,7957.
  **Corrección de lo que decía antes esta ficha:** la fórmula (10) **no** es uniformemente
  del lado de la seguridad frente a la Tabla 1. Contrastada punto a punto da *menos* que la
  tabla en los n chicos (3 → 3,148 vs 3,15 · 10 → 2,088 vs 2,10 · 20 → 1,9155 vs 1,93) y
  *más* en los grandes (50 → 1,8187 vs 1,81 · 100 → 1,7875 vs 1,76). El cruce está entre
  n = 30 y n = 50. Para nuestras submuestras la fórmula queda por debajo de la Tabla 1
  (≈1,79 vs 1,81), o sea levemente del lado inseguro; el efecto está cuantificado en el
  Anexo C.2 del informe y es −0,35 % en `f_m,k` y −0,12 % en `ro_k`, sin incidencia en la
  clase.
- **`k_tol`** — **no aplica a este trabajo.** EN 384 §5.5.1 lo menciona solo para la
  evaluación **no paramétrica** de los ensayos iniciales de sistemas de clasificación **por
  máquina** (donde manda tomarlo igual a 1). La ruta no paramétrica es EN 14358 §3.2.3, y acá
  se usa clasificación visual por el método paramétrico.
- **Distribuciones** — EN 14358 §3.2.2: resistencia por log-normal salvo que los datos
  muestren que la normal ajusta mejor; **la densidad debe estimarse como normal**. El CoV no
  se puede tomar menor a 0,05 (pisos de las fórmulas 3 y 4).
- **Módulo de elasticidad** — EN 14358 §3.3 d): para propiedades de rigidez el valor
  característico medio es la media aritmética de la muestra, fórmula (14). Sin `k_s(n)`.
- **`a_f`** — EN 384 §5.4.3 lo define como la separación entre los dos puntos de aplicación de
  la carga, **no** la distancia apoyo-carga que trae el archivo en la columna `a`. Ver la
  trampa correspondiente más abajo.
- **Fórmulas (11), (12) y (13)** — leídas de EN 384:2016 §5.5.2.2, p.13-14, y **contrastadas
  contra la imagen de la página** porque el texto extraído engaña (ver trampas). La forma
  correcta es:

  ```
  (11)  f_k      = mín{ 1,2·f_05,mín  ; SUMA(n_i·f_05,i)/n  } · k_n
  (12)  E_0,mean = mín{ 1,1·E_mín     ; SUMA(n_i·E_i)/n     } · k_n / 0,95
  (13)  ro_k     = mín{ 1,1·ro_05,mín ; SUMA(n_i·ro_05,i)/n } · k_n
  ```

  `k_n` multiplica **el mínimo entero**, no solo la media ponderada.
- **Tabla 1 de EN 384** (`k_n` por número de submuestras `ns`): módulo y densidad
  0,88 / 0,91 / 0,94 / 0,97 / 1,00 para ns = 1/2/3/4/5+; resistencias paralelas a la fibra
  0,70 / 0,80 / 0,90 / 0,95 / 1,00. Con **ns = 3**: `k_n = 0,90` en resistencia y `0,94` en
  módulo y densidad.

## Valores que quedan pendientes de verificar

- **Cómo se midió `ro`** — define si corresponde el ajuste por 1,05 del §5.3.4. El archivo de
  datos no lo declara. Preguntar al docente. Ya **no es decisivo**: se evaluó por las dos vías
  en la semana 5 y la clase asignada es C22 en ambos casos.

No queda ninguna otra fórmula sin contrastar contra su fuente.

## Trampas conocidas

- **EN 338 no está en el zip de AENOR.** El zip trae solo EN 384 y EN 14358. La tabla de
  clases sale de la diapositiva, y la letra del trabajo lo autoriza expresamente: «para ello
  basta con las diapositivas del curso (S03E02)».
- **Las diapositivas traen las DOS ediciones de EN 338, sin decirlo fuerte.** La p.54-55 es la
  **2010** y la p.56-57 es la **2016**. El mismo ejemplo de castaño resuelto ahí da **D24 por
  la 2010 y D27 por la 2016**: la edición cambia la respuesta. La letra manda la **2010**.
- **La Tabla 1 de EN 338 da `E_0,medio` en kN/mm², no en N/mm².** Todo el resto del trabajo
  está en N/mm². Sin dividir por 1000, los 13 492 N/mm² del lote superan cualquier fila de la
  tabla y la clase saldría C50 por rigidez. Es el único cambio de unidades de todo el trabajo.

- **El OCR de los PDF corrompe símbolos.** Ya pasó en este trabajo: la fórmula (6) de EN 384
  se extrajo como `l_et = l − 5·a_f`, que da longitudes negativas. Contra la imagen de la
  página se confirmó que es **suma**. Ante un signo o un símbolo raro en una desigualdad,
  mirar la página renderizada, no el texto extraído.
- **El OCR movió el `k_n` de lugar en las fórmulas (11)(12)(13).** El texto extraído las
  maqueta de modo que `k_n` parece multiplicar solo la media ponderada, dentro del `mín{}`.
  Renderizando las páginas 13 y 14 a 220 dpi se ve que el `· k_n` está **fuera** del
  paréntesis. La (12) además aparece compuesta como `k_{n/0,95}`, con el 0,95 caído a
  subíndice: la lectura correcta es `· k_n` y después `/ 0,95`, coherente con la fórmula (10)
  del apartado anterior.
- **«Tomar el valor inmediatamente mayor» se refiere a `k_s`, no a `n`.** Como `k_s` decrece
  al crecer `n`, para n = 89 corresponde la entrada **n = 50 → 1,81**, no la de n = 100 →
  1,76. Ir a la entrada de n más cercano por arriba da el valor menos conservador, que es
  justo lo contrario de lo que pide la norma. Es un error fácil de escribir en el código y
  que no rompe nada.
- **La diapositiva p.44 corresponde a EN 384:2010**, la ruta vieja con `k_s` y `k_v`. No se
  usa en este trabajo.
- **`a_f` no es la `a` del archivo de datos.** Es el error silencioso más caro de la etapa 2:
  las dos son longitudes en mm y las dos dan un `k_l` con pinta razonable, así que no se cae
  nada. `a` es la distancia apoyo–punto de carga (6h ± 1,5h en el esquema de S03E02 p.26);
  `a_f` es la separación **entre los dos puntos de carga**, o sea `a_f = l − 2a` (6h nominal).
  Dos comprobaciones que lo cierran: con los datos reales `a_f` da 6,00h / 6,00h / 6,01h, y
  con la geometría de referencia `l = 18h`, `a_f = 6h` sale `l_et = 48h` y `k_l = 1` exacto,
  que es lo que la norma exige cuando el ensayo está en condiciones de referencia.
- **`re.sub` de Python interpreta los backslash del reemplazo.** Al volcar LaTeX generado al
  `INFORME.tex` hay que pasar el reemplazo por un `lambda`, si no explota con
  `bad escape \c`. Está resuelto en `scripts/90_tablas_informe.py`.
