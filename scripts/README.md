# Scripts

Todo el procesamiento va por acá. Los datos de `00-datos/` no se editan nunca; las salidas se
escriben en `resultados/` y se regeneran corriendo los scripts.

Python 3.12. Sin dependencias externas por ahora (solo librería estándar); si más adelante
hace falta exportar a Excel, se agrega `openpyxl`.

| Script | Qué hace | Estado |
|---|---|---|
| `comun.py` | Módulo compartido: lectura del archivo de datos, agrupado por muestra, estadística descriptiva, lectura y escritura de CSV en formato local (`;` y coma decimal) | hecho |
| `00_auditoria_datos.py` | Etapa 0: parseo, conteo por muestra, control geométrico EN 408, rangos de humedad, chequeo de orden de magnitud | hecho |
| `01_verif_despeje_modulo_local.py` | Contrasta el despeje cerrado de `E_m,l` contra la resolución iterativa de la ecuación implícita | hecho |
| `02_propiedades_por_pieza.py` | Etapa 1: `f_m` y `E_m,l` de las 258 piezas | hecho |
| `03_correcciones_en384.py` | Etapa 2: humedad, `k_h`, `k_l`, paso a `E0` | hecho |
| `04_valores_caracteristicos.py` | Etapa 3: EN 14358 por submuestra (log-normal / normal, `k_s(n)`) y combinación EN 384 §5.5.2.2 | hecho |
| `05_clase_resistente.py` | Etapa 4: verificación de los tres criterios contra las clases C de EN 338:2010, asignación, escenario del divisor 1,05 y análisis de robustez | hecho |
| `90_tablas_informe.py` | Vuelca los resultados a los bloques `% <<<AUTO:...>>>` del `INFORME.tex` | hecho |

## Cómo correrlos

Desde la raíz del repo:

```bash
python scripts/00_auditoria_datos.py
```

El orden importa: cada script lee el CSV que dejó el anterior. Cadena completa hasta hoy:

```bash
python scripts/02_propiedades_por_pieza.py && python scripts/03_correcciones_en384.py && python scripts/04_valores_caracteristicos.py && python scripts/05_clase_resistente.py && python scripts/90_tablas_informe.py
```

`90_tablas_informe.py` va **siempre al final**: es el que sincroniza el archivo madre con lo
que acaba de calcularse. Si no se corre, el `INFORME.tex` queda mostrando números viejos sin
avisar.

## Convenciones

- **Unidades:** N, mm, N/mm², kg/m³. No se mezclan y no se cambian a mitad de camino.
- Cada script imprime lo que calcula por pantalla y, cuando corresponde, escribe su salida en
  `resultados/`.
- Cada fórmula lleva en un comentario el apartado o la página de donde salió.
- Nada de valores mágicos: los coeficientes normativos van en constantes con nombre y su cita.
- Las decisiones de criterio que todavía no están cerradas van como **constante con nombre** en
  la cabecera del script, no enterradas en una fórmula. Hoy hay una:
  `AJUSTE_105 = False` en `03_correcciones_en384.py` (el divisor 1,05 de densidad del §5.3.4).
  Cambiarla y volver a correr 03 y 90 alcanza para cuantificar el efecto en el informe entero.
  `05_clase_resistente.py` además la evalúa como escenario sin necesidad de tocar nada:
  **no cambia la clase asignada.**
- **Los símbolos van a los CSV sin coma.** `comun.leer_csv()` hace `replace(",", ".")` sobre
  todos los campos para poder convertir el decimal local, así que `f_m,k` volvería leído como
  `f_m.k`. En los CSV viajan `fmk`, `E0mean` y `rok`, y `90_tablas_informe.py` arma la notación
  de imprenta. Lo mismo con las etiquetas de texto: `05_robustez.csv` lleva una columna
  `clave` (`base`, `ks_tabla`, `normal`, `densidad105`) y el 90 traduce cada clave a su
  etiqueta en LaTeX.
- **Antes de aplicar una tabla normativa, validar el procedimiento contra un caso resuelto.**
  `05_clase_resistente.py` corre de entrada la asignación del ejemplo de castaño de la propia
  diapositiva y aborta con `SystemExit` si no devuelve D24.
