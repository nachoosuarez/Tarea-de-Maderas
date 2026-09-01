# Planificación del trabajo

Documento de referencia: qué se hace en cada etapa, con qué fórmula, sacada de qué apartado.
El `README.md` es el resumen; esto es el detalle.

---

## 1. Marco normativo e hipótesis

Bloque que va declarado en el informe **antes** de cualquier número:

- **Normas aplicadas:**
  - **UNE-EN 408:2010** — método de ensayo (flexión a 4 puntos) y ecuaciones de `f_m` y `E_m`.
  - **UNE-EN 384:2016** — ajuste a condiciones de referencia y combinación de submuestras.
  - **UNE-EN 14358:2016** — cálculo de valores característicos.
  - **UNE-EN 338:2010** — asignación de clase resistente.
- **Cuando 384 y 14358 se pisan manda 14358** para el percentil: la propia EN 384 §5.5.1 lo
  deriva ahí. La ruta antigua de EN 384:2010 (`f_k = f_05 · k_s · k_v`, diapositiva S03E02
  p.44) **no se usa** — la letra pide explícitamente el procedimiento actualizado.
- **Clasificación visual, no mecánica.** Esto decide qué rama de EN 384 §5.5.2 se aplica:
  corresponde §5.5.2.2, que usa `k_n`, y no la rama mecánica.
- **Condiciones de referencia** (EN 384 §5.3): u_ref = 12 %, canto 150 mm, luz 18h, carga en
  los tercios.
- **G = E_m,l / 16**, impuesto por la letra del trabajo.
- **Unidades:** N, mm, N/mm², kg/m³.

---

## 2. Etapa 0 — Auditoría de los datos (hecha)

Resultados en `01-semana-01_auditoria/`. Resumen: 258 piezas válidas, n = 89/90/79 (las tres
por encima del mínimo de 40 de EN 384 §5.1), geometría de ensayo dentro de tolerancia EN 408
en las 258, humedades entre 9,8 % y 13,9 % (dentro del rango de validez 8-18 % de
EN 384 §5.4.2), sin duplicados, `P/f` confirmado en N/mm.

---

## 3. Etapa 1 — Propiedades de cada pieza (EN 408)

Dos números por viga.

**Resistencia a flexión** (S03E02 p.28):

```
f_m = 3 · F · a / (b · h²)          con F = Pmax
```

**Módulo de elasticidad local** (ecuación de S03E02 p.26, que es la del módulo global
corregida del efecto del cortante):

```
                    3·a·l² − 4·a³
E_m,l = ─────────────────────────────────────────────
        2·b·h³ · [ 2·(w2−w1)/(F2−F1) − 6a/(5·G·b·h) ]
```

Dos avisos:

1. El dato `P/f` es **(F2−F1)/(w2−w1)**, o sea el **inverso** del cociente que aparece en la
   fórmula. Es la ambigüedad que la letra advierte con *"revisar unidades en caso de duda del
   cociente suministrado"*. Confirmado: viene en N/mm.
2. Con G = E_m,l/16 la ecuación queda **implícita**. Despejando en forma cerrada:

```
E_m,l = (P/f) · (3·a·l² − 4·a³ + 38,4·a·h²) / (4·b·h³)
```

   Este despeje **está verificado**: coincide con la resolución iterativa de la ecuación
   original hasta la quinta cifra (`scripts/01_verif_despeje_modulo_local.py`).

---

## 4. Etapa 2 — Corrección a condiciones de referencia (EN 384:2016 §5.4)

EN 384 §5.4.1 exige ajustar **probeta a probeta**, no el promedio de la muestra. Es el error
más frecuente y el más caro.

| Corrección | Fórmula | Apartado |
|---|---|---|
| Humedad, módulo | `E0 = E0(u) · (1 + 0,01·(u − u_ref))` | §5.4.2, fórm. (2) |
| Humedad, densidad | `ro = ro(u) · (1 − 0,005·(u − u_ref))` | §5.4.2, fórm. (3) |
| Canto | dividir `f_m` por `k_h = mín{(150/h)^0,2 ; 1,3}` | §5.4.3, fórm. (4) |
| Luz de ensayo | dividir `f_m` por `k_l = (48h / l_et)^0,2`, con `l_et = l + 5·a_f` | §5.4.3, fórm. (5) y (6) |
| Módulo local a E0 | `E0 = E_m,local(u_ref)`, directo | §5.4.4, fórm. (8) |

**Puntos donde este trabajo se aparta del caso de manual:**

- **`k_h` solo aplica a las muestras 1 y 2.** El §5.4.3 lo condiciona a canto < 150 mm y
  densidad ≤ 700 kg/m³. La muestra 3 tiene h ≈ 190 mm, así que `k_h = 1` y no se corrige.
- **`k_l` no vale 1.** Las relaciones l/h medidas son 18,86 / 19,10 / 18,83, no 18 exacto.
  Se calcula pieza por pieza; la corrección es del orden del 1 % pero es sistemática.
- **No se usa la fórmula (7)** `E0 = 1,3·E_m,global − 2690`. Esa es para módulo global; acá
  se calcula el local, así que corresponde la (8).
- **El ajuste de densidad por 1,05 NO aplica.** El §5.3.4 lo reserva textualmente para *"las
  probetas que no se someten a ensayo hasta rotura"*. Acá las 258 se ensayaron hasta rotura
  (hay `Pmax` de todas), así que la densidad se determinó sobre probeta pequeña libre de
  defectos y ya está en la referencia correcta.
  **VERIFICAR** con el docente: el archivo no declara cómo se midió `ro`, y el 4,8 % de
  diferencia alcanza para cambiar de clase.

---

## 5. Etapa 3 — Valores característicos

### 5.a Por submuestra — EN 14358:2016, método paramétrico

Para cada una de las 3 muestras:

- **Resistencia a flexión** — distribución **log-normal**:

```
y_med = (1/n) · SUMA ln(m_i)
s_y   = máx{ raíz[ SUMA (ln m_i − y_med)² / (n−1) ] ; 0,05 }
m_k   = exp(y_med − k_s(n) · s_y)
```

- **Densidad** — distribución **normal**:

```
y_med = (1/n) · SUMA m_i
s_y   = máx{ raíz[ SUMA (m_i − y_med)² / (n−1) ] ; 0,05·y_med }
m_k   = y_med − k_s(n) · s_y
```

- **Módulo de elasticidad** — valor **medio** de la submuestra, no percentil.

`k_s(n) = (6,5n + 6) / (3,7n − 3)` según S03E02 p.51.
**VERIFICAR** contra la tabla de la EN 14358:2016 (está en `06-referencias/`) y usar la
tabla si difiere. Revisar ahí también el factor `k_tol` que menciona EN 384 §5.5.1.

### 5.b Combinación de las 3 submuestras — EN 384:2016 §5.5.2.2

Con n_s = 3, la Tabla 1 da **k_n = 0,90** para resistencias y **k_n = 0,94** para módulo y
densidad.

```
(11)  f_k      = mín{ 1,2·f_05,i,mín  ; SUMA(n_i·f_05,i)/n  } · k_n
(12)  E_0,mean = mín{ 1,1·E_i,mín     ; SUMA(n_i·E_i)/n     } · k_n / 0,95
(13)  ro_k     = mín{ 1,1·ro_05,i,mín ; SUMA(n_i·ro_05,i)/n } · k_n
```

El término del mínimo castiga que una submuestra sea mucho peor que las otras. Conviene
comentarlo en el informe: ahí se ve si la clasificación visual produjo un lote homogéneo o no.

---

## 6. Etapa 4 — Asignación de clase resistente (EN 338:2010)

Picea es conífera, así que van las **clases C**. Los tres valores —`f_m,k`, `E_0,mean` y
`ro_k`— deben cumplir **simultáneamente** los mínimos de la clase candidata; se asigna la más
alta que cumple con los tres (procedimiento de S03E02 p.54). Hay que mostrar la tabla con las
tres columnas y decir explícitamente **cuál de los tres criterios gobierna** — suele ser el
módulo de elasticidad, no la resistencia.

---

## 7. Etapa 5 — Informe

Estructura mínima que exige la letra:

**Resumen · Objetivos · Datos de partida · Análisis de datos · Resultados · Conclusiones**

El análisis de datos tiene que cubrir el tratamiento individual (pieza a pieza) y el
estadístico. Las tablas extensas y los cálculos intermedios van a **anexos**:

- **Anexo A** — Tabla completa pieza por pieza: geometría, `f_m` y `E_m,l` brutos, los
  coeficientes `k_h` y `k_l` aplicados, y los valores corregidos.
- **Anexo B** — Estadística por submuestra: n, media, desvío, CV, `f_05`, `ro_05`, `E_medio`.
- **Anexo C** — Verificación geométrica del dispositivo de ensayo contra EN 408.

Las tablas A.1 y A.3 del Anexo A (normativo) de la EN 384 son modelos de informe directamente
reutilizables como plantilla.

---

## 8. Cronograma

Hoy 31/08/2026, entrega 06/11/2026 → 9 semanas y media.

| Semana | Trabajo | Estado |
|---|---|---|
| 1 | Auditoría de datos y verificación del despeje del módulo | hecha |
| 2-3 | Etapas 1 y 2: propiedades por pieza y correcciones | |
| 4 | Etapa 3: valores característicos, leyendo la EN 14358 del PDF | |
| 5 | Etapa 4: clase resistente + borrador del informe | |
| 6-8 | Redacción, anexos, revisión cruzada | |
| 9 | Margen antes del 06/11 | |

**Reparto sugerido (3 personas):** uno toma el procesamiento por pieza (Etapas 1-2), otro la
estadística (Etapa 3), otro la redacción y los anexos. La Etapa 4 la revisan los tres, porque
es donde se juega el resultado.

---

## 9. Dónde se pierden puntos

1. Usar el percentil 5 % contando de la muestra ordenada (EN 384:**2010**) en vez del
   paramétrico de EN 14358:**2016**. Es el cambio central de la actualización y la letra lo
   pide explícito.
2. Olvidar `k_l` dando por sentado que el ensayo es normalizado. Que el archivo traiga `a` y
   `l` de cada pieza es la señal de que hay que calcularlo.
3. Aplicar `k_h` a la muestra 3, que tiene canto mayor a 150 mm.
4. Usar la fórmula (7) en vez de la (8) para pasar a E0.
5. Corregir el promedio de la muestra en lugar de corregir pieza por pieza.
6. Ajustar la densidad por 1,05 sin verificar si corresponde (acá probablemente no).
7. Asignar la clase mirando solo `f_m,k` y olvidando que los tres criterios mandan a la vez.
