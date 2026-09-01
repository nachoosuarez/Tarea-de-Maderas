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
| 15 | Asignación de clase resistente | EN 338:2010 — S03E02 p.54 y p.56 |
| 16 | Modelos de tabla para el informe | EN 384:2016 Anexo A (normativo), Tablas A.1 y A.3 |

## Verificado contra la norma (ya no son pendientes)

- **`k_s(n)`** — la expresión `(6,5n + 6)/(3,7n − 3)` **no es solo de la diapositiva**: es la
  fórmula (10) de la propia EN 14358:2016 §3.2.2 f), que la norma admite expresamente como
  alternativa a su Tabla 1. Da valores levemente mayores que la tabla, o sea del lado de la
  seguridad (n = 100: fórmula 1,788 vs tabla 1,76). Valores tabulados: n=3 → 3,15; 5 → 2,46;
  10 → 2,10; 15 → 1,99; 20 → 1,93; 30 → 1,87; 50 → 1,81; 100 → 1,76; 500 → 1,69; ∞ → 1,64.
  Para n no tabulado la norma manda **tomar el valor inmediatamente mayor**.
  Con nuestros n: 89 → 1,7913 · 90 → 1,7909 · 79 → 1,7957.
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

## Valores que quedan pendientes de verificar

- **Cómo se midió `ro`** — define si corresponde el ajuste por 1,05 del §5.3.4. El archivo de
  datos no lo declara. Preguntar al docente.
- **Tabla de clases resistentes de EN 338:2010** — todavía no leída. Es la semana 5.

## Trampas conocidas

- **El OCR de los PDF corrompe símbolos.** Ya pasó en este trabajo: la fórmula (6) de EN 384
  se extrajo como `l_et = l − 5·a_f`, que da longitudes negativas. Contra la imagen de la
  página se confirmó que es **suma**. Ante un signo o un símbolo raro en una desigualdad,
  mirar la página renderizada, no el texto extraído.
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
