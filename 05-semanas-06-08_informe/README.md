# Semanas 6 a 8 — Informe

Cubre la **Etapa 5**. Tres semanas para redactar, más una cuarta de margen antes del
**06/11/2026**.

**Entregable:** el informe completo con sus anexos. Es lo único que se entrega y lo único que
se corrige.

> **Estado: cerrado.** El informe está redactado, compilado y revisado. Vive en
> [`../INFORME.tex`](../INFORME.tex), en la raíz del repo: **27 páginas, compilado con
> pdfLaTeX en tres pasadas, 0 errores y 0 avisos `LaTeX Warning`**. Lo único que falta es
> **poner los nombres del grupo** en `\author{}`: es la única marca roja que queda en el PDF.

---

## Estructura exigida por la letra

Es un mínimo, no una sugerencia. Así quedó resuelta:

| Sección de la letra | Dónde está en el informe |
|---|---|
| **Resumen** | Portada. Los tres valores y la clase salen generados del CSV, no tipeados |
| **Objetivos** | §1 |
| **Datos de partida** | §2, con la composición del lote y la verificación previa |
| **Análisis de datos** | §4: §4.1 individual (pieza a pieza), §4.2 correcciones, §4.3 estadístico |
| **Resultados** | §5: valores por submuestra, característicos del lote, asignación y robustez |
| **Conclusiones** | §6: criterio gobernante, homogeneidad del lote, limitaciones |

Además se agregaron dos cosas que la letra no pide y el informe necesitaba:

- **§3.3 Trazabilidad y verificación del cálculo** — cómo se encadenan las cuatro etapas, que
  las tablas se generan y no se transcriben, y que los números redactados a mano se cotejaron
  automáticamente contra los datos.
- **Referencias** — las cuatro normas con apartado por apartado, más la aclaración de que
  UNE-EN 408 y UNE-EN 338 no se consultaron en su texto íntegro sino por las diapositivas.

Las tablas extensas y los cálculos intermedios **van a anexos**, no al cuerpo. La letra lo
pide explícito.

## Anexos

| Anexo | Contenido | De dónde sale |
|---|---|---|
| **A** | Verificación geométrica del ensayo contra EN 408, contraste de la forma cerrada de `E_m,l` y comprobación de órdenes de magnitud | Semana 1 |
| **B** | Tabla pieza por pieza (258 filas × 2 tablas): datos brutos y propiedades sin corregir, y factores `k_h`, `k_l` con los valores corregidos | Semanas 2-3 |
| **C** | Parámetros del ajuste estadístico por submuestra: `ȳ`, `s_y`, piso de CoV, `k_s`, bondad de ajuste y sensibilidad al `k_s` | Semana 4 |
| **D** | Verificación de los tres valores frente a las doce clases C de EN 338:2010 | Semana 5 |

> Ojo si se compara con versiones viejas de este README: **la letra de los anexos cambió**.
> Antes decía A = pieza a pieza, B = estadística, C = geometría; el informe quedó ordenado al
> revés, siguiendo el orden en que aparecen citados en el cuerpo.

Las tablas **A.1** y **A.3** del Anexo A (normativo) de la EN 384 son modelos de informe de
la propia norma y sirvieron de plantilla directa para B y C.

## El bloque de hipótesis

Va al principio del análisis, antes de cualquier número. Está en **§3.2**:

- Normas aplicadas y edición de cada una, y cuál manda cuando se pisan (§3.1)
- Que la clasificación es **visual**, y por lo tanto que aplica EN 384 §5.5.2.2
- Condiciones de referencia adoptadas (u = 12 %, canto 150 mm, luz 18h)
- `G = E_m,l/16`, impuesto por la letra
- Que es caracterización de material y no verificación estructural: no hay coeficientes
  parciales ni combinaciones de acciones
- Unidades de cada magnitud

## La revisión cruzada

El punto de la checklist que más trabajo dio. Las tablas del informe se generan solas desde
los CSV, así que ahí no hay nada que cotejar; el riesgo estaba en **los números redactados a
mano en el texto corrido**. Para eso está [`scripts/91_revision_cruzada.py`](../scripts/91_revision_cruzada.py):
recalcula cada uno desde los datos crudos y lo compara **con los mismos decimales con que
está impreso**, exigiendo además que la cadena LaTeX exacta siga presente en el `.tex`.

**117 comprobaciones, 0 diferencias.** En la primera corrida encontró cuatro cosas reales:

| Qué | Estaba | Es |
|---|---|---|
| `k_h` medio de la muestra 1 | 1,099 | **1,098** |
| `k_s(20)` por la fórmula (10) | 1,916 | **1,915** |
| `k_s(100)` por la fórmula (10) | 1,788 | **1,787** |
| El contraste iterativo del anexo A | «iteración sobre piezas de las tres muestras» | son **tres geometrías representativas** con `P/f` redondeada, no probetas concretas |

Lo que el script **no** puede comprobar está listado en
[`resultados/91_revision_cruzada.md`](../resultados/91_revision_cruzada.md): la transcripción
de la tabla 1 de EN 338:2010, los coeficientes normativos y la redacción en sí.

## Checklist

- [x] Bloque de hipótesis redactado — §3.2
- [x] Datos de partida con la tabla del lote — §2.2
- [x] Análisis individual: las fórmulas de EN 408 y las correcciones de EN 384, con apartado y página
- [x] Análisis estadístico: EN 14358 y la combinación de submuestras — §4.3
- [x] Resultados con la tabla de verificación de los tres criterios — §5.3
- [x] Conclusiones, incluida la decisión sobre el ajuste de densidad — §6
- [x] Anexos A, B, C y D armados
- [x] Revisión cruzada: cada fórmula con su cita de apartado, y los 117 números del texto
      recalculados contra los datos
- [x] Chequeo de unidades en todas las tablas — todas las cabeceras llevan la unidad entre corchetes
- [x] Sección de Referencias
- [ ] **Nombres del grupo en `\author{}`** — lo único que falta, y no lo puedo poner yo
- [ ] Entrega por EVA antes del 06/11/2026

## Para contrastar antes de entregar

- Los valores de la **tabla 1 de UNE-EN 338:2010** se transcribieron desde la reproducción de
  la diapositiva S03E02 p.55, no desde la norma. Están en
  [`06-referencias/README.md`](../06-referencias/README.md) para poder cotejarlos.
- Queda por preguntarle al docente **cómo se midió `ρ`** (probeta completa o probeta libre de
  defectos), que es lo que decide si aplica el divisor 1,05 de EN 384 §5.3.4. Ya está
  cuantificado: **no cambia la clase**, así que no bloquea la entrega.
