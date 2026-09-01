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

## Formato de los CSV

Pensados para abrirse con doble clic en Excel en español, sin pasar por el asistente de
importación:

- Separador **`;`**, decimal **coma**.
- Codificación **UTF-8 con BOM** (`utf-8-sig`), que es lo que Excel necesita para no romper las
  tildes.
- La **segunda fila es la de unidades**, no un dato. Al leerlos desde Python usar
  `comun.leer_csv()`, que ya la saltea.

## De acá salen las tablas del informe

`scripts/90_tablas_informe.py` lee `03_valores_corregidos.csv` y reescribe con él los bloques
`% <<<AUTO:...>>>` del `INFORME.tex` (las tres tablas de §4.2, el Anexo B.1, el Anexo B.2 y el
Anexo C.1). O sea que
un número mal en un CSV aparece mal en el PDF sin que nadie lo tipee: la verificación se hace
acá, no en el `.tex`.
