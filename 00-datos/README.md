# 00 — Datos de partida

Contenido **inmutable**. Nada de acá se edita: toda transformación ocurre en `scripts/` y se
escribe en `resultados/`.

| Archivo | Qué es |
|---|---|
| `Datos_Picea.txt` | Resultados de ensayo, 258 piezas. Tabulado, decimal con punto, dos filas de encabezado (nombres y unidades) |
| `Trabajo_EM_2026_Caracterizacion_Letra.pdf` | La letra del trabajo |

## Estructura del archivo de datos

| Columna | Unidad | Descripción |
|---|---|---|
| `Viga` | – | Identificador dentro de la muestra |
| `Muestra` | – | 1, 2 o 3 |
| `b` | mm | Ancho de la sección |
| `h` | mm | Canto de la sección |
| `a` | mm | Distancia entre punto de carga y apoyo |
| `l` | mm | Luz entre apoyos |
| `CH` | % | Contenido de humedad de la pieza |
| `ro` | kg/m³ | Densidad |
| `Pmax` | N | Carga total de rotura |
| `P/f` | N/mm | Pendiente del tramo elástico de la curva carga-flecha |

## Qué hay que tener presente

- **Solo están las piezas que pasaron la clasificación visual.** Las rechazadas no figuran en
  el archivo, así que el lote caracterizado es el ya clasificado.
- **`P/f` es la pendiente, no su inversa.** La ecuación del módulo de EN 408 usa
  `(w2−w1)/(F2−F1)`, que es el recíproco de este dato. Ver `PLANIFICACION.md` §3.
- **Las tres muestras son tres secciones transversales distintas**, no tres repeticiones de
  lo mismo. Eso es lo que habilita el tratamiento por submuestras de EN 384 §5.5.2.2.
