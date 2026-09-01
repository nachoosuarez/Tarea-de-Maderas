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
| **UNE-EN 338:2010** | Clases resistentes | Vía diapositivas S03E02 p.54-56 |
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
| 8 | `k_l = (48h/l_et)^0,2` y `l_et = l + 5·a_f` | EN 384:2016 §5.4.3 fórm. (5) y (6) |
| 9 | `E0 = E_m,local(u_ref)` | EN 384:2016 §5.4.4 fórm. (8) |
| 10 | Densidad de probeta completa: dividir por 1,05 en coníferas | EN 384:2016 §5.3.4 |
| 11 | Percentiles por submuestra remitidos a EN 14358 | EN 384:2016 §5.5.1 |
| 12 | `f_k`, `E_0,mean`, `ro_k` combinando submuestras | EN 384:2016 §5.5.2.2, fórm. (11)(12)(13) |
| 13 | Factor `k_n` según número de submuestras | EN 384:2016 Tabla 1 |
| 14 | Método paramétrico log-normal y normal, `k_s(n)` | EN 14358:2016 — S03E02 p.51 |
| 15 | Asignación de clase resistente | EN 338:2010 — S03E02 p.54 y p.56 |
| 16 | Modelos de tabla para el informe | EN 384:2016 Anexo A (normativo), Tablas A.1 y A.3 |

## Valores que quedan pendientes de verificar

- **`k_s(n)`** — la expresión `(6,5n + 6)/(3,7n − 3)` viene de la diapositiva p.51.
  Contrastar contra la tabla de la EN 14358:2016 antes de usarla.
- **`k_tol`** — EN 384 §5.5.1 lo menciona; hay que leer en la EN 14358 qué es y si aplica.
- **Cómo se midió `ro`** — define si corresponde el ajuste por 1,05 del §5.3.4. El archivo de
  datos no lo declara. Preguntar al docente.

## Trampas conocidas

- **El OCR de los PDF corrompe símbolos.** Ya pasó en este trabajo: la fórmula (6) de EN 384
  se extrajo como `l_et = l − 5·a_f`, que da longitudes negativas. Contra la imagen de la
  página se confirmó que es **suma**. Ante un signo o un símbolo raro en una desigualdad,
  mirar la página renderizada, no el texto extraído.
- **La diapositiva p.44 corresponde a EN 384:2010**, la ruta vieja con `k_s` y `k_v`. No se
  usa en este trabajo.
