# Tarea de Maderas — Caracterización de Picea

Trabajo de **Estructuras de Madera 2026** (FING, UdelaR). A partir de los resultados de
ensayo de 258 vigas de Picea clasificadas visualmente, hay que establecer la **clase
resistente** que le corresponde al lote según UNE-EN 338.

| | |
|---|---|
| **Entrega** | 06/11/2026 vía EVA |
| **Reentrega** | 02/12/2026 (solo si la nota queda entre 25 % y 50 %) |
| **Condición** | Eliminatoria: se necesita ≥ 50 % para aprobar. No hay segunda reentrega |
| **Grupo** | 2-3 estudiantes (preferentemente 3) |
| **Entregable** | Informe escrito con anexos |

---

## Qué hay que hacer

En una línea: **de 258 ensayos individuales a un trío de valores característicos, y de ahí a una clase resistente.**

- **Medir cada pieza.** Con la carga de rotura y la pendiente carga-flecha de cada viga se
  calculan su resistencia a flexión y su módulo de elasticidad local.
- **Llevar todo a condiciones de referencia.** Cada pieza se ensayó con su propia humedad,
  su propio canto y su propia luz. Antes de compararlas entre sí hay que corregirlas a un
  patrón común (12 % de humedad, canto de 150 mm, luz de 18 veces el canto).
- **Sacar los valores característicos.** No interesa la viga promedio sino la viga mala: el
  percentil 5 % de resistencia y de densidad, y el valor medio del módulo. Se calculan por
  muestra y después se combinan penalizando la dispersión entre muestras.
- **Asignar la clase.** Los tres valores tienen que cumplir simultáneamente los mínimos de
  la clase; la que gobierna suele ser la rigidez, no la resistencia.
- **Escribir el informe.** Resumen, objetivos, datos de partida, análisis, resultados y
  conclusiones. Las tablas largas van a anexos.

## Cómo se hace

Cuatro etapas normativas encadenadas. Cada una tiene su norma y ninguna se puede saltear:

| Etapa | Qué produce | Norma |
|---|---|---|
| 1 | `f_m` y `E_m,local` de cada una de las 258 piezas | **UNE-EN 408:2010** |
| 2 | Esos mismos valores corregidos a condiciones de referencia | **UNE-EN 384:2016** §5.4 |
| 3 | `f_05`, `ρ_05` y `Ē` por muestra, y su combinación en `f_k`, `ρ_k`, `E_0,mean` | **UNE-EN 14358:2016** + **EN 384:2016** §5.5 |
| 4 | La clase resistente C del lote | **UNE-EN 338:2010** |

Todo el procesamiento va por script de Python (`scripts/`), no a mano en Excel: son 258
piezas y cada corrección obliga a recalcular la cadena entera. La salida alimenta
directamente las tablas de los anexos.

## Los datos

`00-datos/Datos_Picea.txt` — 258 piezas, tabulado, decimal con punto.

| Columna | Unidad | Qué es |
|---|---|---|
| `Viga`, `Muestra` | – | Identificación y a cuál de las 3 muestras pertenece |
| `b`, `h` | mm | Ancho y canto de la sección |
| `a`, `l` | mm | Distancia entre carga y apoyo, y luz entre apoyos |
| `CH` | % | Contenido de humedad de esa pieza |
| `ro` | kg/m³ | Densidad |
| `Pmax` | N | Carga total de rotura |
| `P/f` | N/mm | Pendiente del tramo elástico de la curva carga-flecha |

Solo están las piezas que **pasaron** el criterio de clasificación visual; las rechazadas no
figuran. Las tres muestras son tres secciones transversales distintas:

| Muestra | n | Sección media |
|---|---|---|
| 1 | 89 | 36 × 94 mm |
| 2 | 90 | 45 × 142 mm |
| 3 | 79 | 57 × 190 mm |

## Estado

- [x] **Semana 1** — Auditoría de datos. Los 258 registros parsean, las 3 muestras superan
      el mínimo de 40 probetas, toda la geometría de ensayo cae dentro de tolerancia y todas
      las humedades están en el rango de validez de la norma. Ver
      [`01-semana-01_auditoria/`](01-semana-01_auditoria/).
- [ ] **Semanas 2-3** — Propiedades por pieza y corrección a condiciones de referencia.
- [ ] **Semana 4** — Valores característicos.
- [ ] **Semana 5** — Clase resistente y borrador del informe.
- [ ] **Semanas 6-8** — Redacción, anexos y revisión cruzada.

## Cómo moverse por el repo

```
INFORME.tex        <-- ARCHIVO MADRE. El informe entero, en LaTeX, para Overleaf.
PLANIFICACION.md   El plan completo con la justificación normativa de cada paso.
00-datos/          Datos crudos y la letra del trabajo. No se toca.
01-semana-01_...   Auditoría de los datos. Hecha.
02-semanas-02-03_  Etapas 1 y 2: propiedades por pieza y correcciones.
03-semana-04_...   Etapa 3: valores característicos.
04-semana-05_...   Etapa 4: asignación de clase.
05-semanas-06-08_  El informe y sus anexos.
06-referencias/    De dónde salió cada fórmula, con apartado y página.
scripts/           El procesamiento en Python.
resultados/        Salidas generadas. Se regeneran corriendo los scripts.
```

Cada carpeta tiene su propio `README.md` con la tarea concreta de esa semana, el entregable
y una checklist. La justificación completa de cada paso está en
[`PLANIFICACION.md`](PLANIFICACION.md).

## El archivo madre: `INFORME.tex`

En la raíz, fuera de las carpetas por semana, está [`INFORME.tex`](INFORME.tex): **el informe
completo en LaTeX**, en un único archivo autocontenido. Se sube tal cual a Overleaf (New
Project → Upload Project, o pegarlo en un proyecto en blanco) y compila con **pdfLaTeX** sin
tocar nada. Verificado localmente con MiKTeX: 10 páginas, sin errores ni warnings.

Sigue la estructura que pide la letra: Resumen · Objetivos · Datos de partida · Análisis de
datos · Resultados · Conclusiones, más los Anexos A, B y C.

**Cómo se lee el archivo:**

| Marca | Color en el PDF | Qué significa |
|---|---|---|
| texto normal | negro | Ya calculado y contrastado. Se puede usar |
| `\pendiente{...}` | rojo | Falta calcularlo o redactarlo |
| `\verificar{...}` | naranja | Hay un número puesto pero hay que contrastarlo contra la fuente |
| `\fuente{...}` | cursiva chica | Norma, apartado y página de donde salió lo de arriba |

**Ninguna marca naranja puede quedar en la versión que se entrega.** Las rojas se van
completando semana a semana, y son el indicador visual de cuánto falta.

## Política del repo: todo se guarda acá

Nada de resultados sueltos en el chat, en el Escritorio o en un Excel local. Cada cosa que se
produce entra al repo, en el lugar que le toca:

| Qué se produjo | Dónde va |
|---|---|
| Un número, una tabla o una conclusión | `INFORME.tex` (y, si es intermedio, el README de su semana) |
| Un cálculo | `scripts/`, nunca a mano |
| La salida de un script | `resultados/`, regenerable |
| Una fórmula nueva | `06-referencias/README.md`, con apartado y página |
| Una decisión de criterio o una duda para el docente | El README de la semana correspondiente |

El `INFORME.tex` se actualiza en el mismo commit en que se produce el resultado, no al final.
Así el estado real del trabajo se lee compilando el archivo madre y contando marcas rojas.

## Convenciones

- **Unidades:** N, mm, N/mm² (= MPa), kg/m³. Fijadas de entrada y no se cambian.
- **Ninguna fórmula se escribe de memoria.** Cada una lleva su apartado y su página. Lo que
  no se pudo leer de la fuente va marcado **VERIFICAR**.
- Los datos crudos no se editan nunca. Toda transformación ocurre en los scripts.
