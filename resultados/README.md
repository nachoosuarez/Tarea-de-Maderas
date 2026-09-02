# Resultados

Salidas generadas por los scripts. Se regeneran corriendo `scripts/`.

**No editar a mano:** cualquier corrección va en el script que la produce. Estos archivos están
versionados igual, para poder ver en el historial de git qué cambió un ajuste de criterio.

## Qué hay acá

| Archivo | Lo produce | Qué contiene |
|---|---|---|
| `02_propiedades_por_pieza.csv` | `02_propiedades_por_pieza.py` | 258 filas: datos de partida + `W`, `Mmax`, `f_m` y `E_m,local` sin corregir (EN 408) |
| `02_resumen_etapa1.md` | ídem | Estadística descriptiva por submuestra de la etapa 1 |
| `03_valores_corregidos.csv` | `03_correcciones_en384.py` | 258 filas: `a_f`, `l_et`, `k_h`, `k_l` y los valores en condiciones de referencia (EN 384 §5.4). **Es la entrada de la etapa 3** |
| `03_resumen_etapa2.md` | ídem | Factores por submuestra, efecto de cada corrección y descriptiva de los valores corregidos |
| `04_por_submuestra.csv` | `04_valores_caracteristicos.py` | 3 filas, una por submuestra: `n`, `k_s` por fórmula y por tabla, media y desvío de la transformada, si se activó el piso de CoV, `f_05` (log-normal y normal), `ro_05`, `E` medio y los estadísticos `D` de Kolmogorov-Smirnov |
| `04_valores_lote.csv` | ídem | 3 filas, una por magnitud: media ponderada, término acotado, cuál gobierna, `k_n`, divisor y el valor característico del lote |
| `04_resumen_etapa3.md` | ídem | Percentiles por submuestra, bondad de ajuste, combinación y sensibilidad al `k_s` de la Tabla 1 |

## Formato de los CSV

Pensados para abrirse con doble clic en Excel en español, sin pasar por el asistente de
importación:

- Separador **`;`**, decimal **coma**.
- Codificación **UTF-8 con BOM** (`utf-8-sig`), que es lo que Excel necesita para no romper las
  tildes.
- La **segunda fila es la de unidades**, no un dato. Al leerlos desde Python usar
  `comun.leer_csv()`, que ya la saltea.

> **Trampa:** `comun.leer_csv()` hace `replace(",", ".")` sobre **todos** los valores antes de
> intentar convertirlos a número, porque el decimal es coma. Consecuencia: un campo de texto
> con coma vuelve deformado (`f_m,k` sale como `f_m.k`). Por eso los símbolos de
> `04_valores_lote.csv` son `fmk`, `E0mean` y `rok`, sin coma, y la notación linda se arma en
> `90_tablas_informe.py`.

## De acá salen las tablas del informe

`scripts/90_tablas_informe.py` lee `03_valores_corregidos.csv`, `04_por_submuestra.csv` y
`04_valores_lote.csv`, y reescribe con ellos los bloques `% <<<AUTO:...>>>` del `INFORME.tex`:
`factores`, `correccion` y `corregidos` (las tres tablas de §4.2), `submuestras` (§5.1),
`caracteristicos` (§5.2), `anexoB1`, `anexoB2`, `anexoC` y `anexoC2`. O sea que
un número mal en un CSV aparece mal en el PDF sin que nadie lo tipee: la verificación se hace
acá, no en el `.tex`.

El `90` es **consumidor puro**: no calcula nada. Si el informe necesita un número nuevo, primero
tiene que existir en un CSV.
