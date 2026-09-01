# Semanas 2 y 3 — Propiedades por pieza y corrección a condiciones de referencia

Cubre las **Etapas 1 y 2** de la planificación. Es la parte más larga porque son 258 piezas
por cinco operaciones, y todo lo que venga después se apoya en que esto esté bien.

**Entregable:** una tabla de 258 filas con los valores corregidos de `f_m`, `E_0` y `ro`,
lista para alimentar la estadística. Es el **Anexo B** del informe.

**Estado: HECHO.** Salidas en `resultados/02_*` y `resultados/03_*`, volcadas al
`INFORME.tex` (§4.1, §4.2, Anexo B y Anexo C.1) por `scripts/90_tablas_informe.py`.

---

## Semana 2 — Etapa 1: propiedades de cada pieza (EN 408)

Dos números por viga, sin corregir nada todavía.

```
f_m   = 3 · Pmax · a / (b · h²)                            [S03E02 p.28]

E_m,l = (P/f) · (3·a·l² − 4·a³ + 38,4·a·h²) / (4·b·h³)     [S03E02 p.26, con G = E/16]
```

El segundo es el despeje de la ecuación implícita, ya verificado en la semana 1.

### Resultado

| Muestra | n | `f_m` medio [N/mm²] | CoV | `E_m,l` medio [N/mm²] | CoV |
|---|---|---|---|---|---|
| 1 | 89 | 36,96 | 20,3 % | 13 709 | 13,1 % |
| 2 | 90 | 39,12 | 17,1 % | 13 379 | 10,7 % |
| 3 | 79 | 39,69 | 26,4 % | 13 844 | 14,3 % |

Detalle en [`resultados/02_resumen_etapa1.md`](../resultados/02_resumen_etapa1.md).

### Checklist

- [x] Calcular `f_m` de las 258 piezas
- [x] Calcular `E_m,l` de las 258 piezas
- [x] Contrastar contra los rangos de la auditoría (f_m medio ~37-40, E_m,l medio ~13400-13900)
- [ ] Histograma de cada variable por muestra, para detectar valores anómalos

---

## Semana 3 — Etapa 2: corrección a condiciones de referencia (EN 384:2016 §5.4)

El §5.4.1 exige ajustar **probeta a probeta**. Corregir el promedio de la muestra es el error
más frecuente de este trabajo.

| Orden | Corrección | Fórmula | Apartado |
|---|---|---|---|
| 1 | Humedad, módulo | `E0 = E0(u) · (1 + 0,01·(u − 12))` | §5.4.2 (2) |
| 2 | Humedad, densidad | `ro = ro(u) · (1 − 0,005·(u − 12))` | §5.4.2 (3) |
| 3 | Canto | `f_m / k_h`, con `k_h = mín{(150/h)^0,2 ; 1,3}` | §5.4.3 (4) |
| 4 | Luz de ensayo | `f_m / k_l`, con `k_l = (48h/l_et)^0,2` y `l_et = l + 5·a_f` | §5.4.3 (5)(6) |
| 5 | Módulo local a E0 | `E0 = E_m,local(u_ref)`, directo | §5.4.4 (8) |

### Las cinco trampas de esta etapa

1. **`a_f` NO es la columna `a` del archivo.** El §5.4.3 define `a_f` como *"la separación
   entre los dos puntos de aplicación de la carga"*; la columna `a` es la distancia
   apoyo–punto de carga. O sea **`a_f = l − 2a`**. Con los datos da 564,0 / 852,0 /
   1139,9 mm, es decir 6,00h / 6,00h / 6,01h — exactamente la separación nominal del
   esquema de S03E02 p.26. Y el chequeo que cierra: con la geometría de referencia
   `l = 18h` y `a_f = 6h` sale `l_et = 48h`, o sea `k_l = 1` exacto, que es lo que la norma
   exige. Tomando `a_f = a` no da ninguna de las dos cosas.
2. **La resistencia a flexión NO se corrige por humedad.** El §5.4.2 lista taxativamente
   qué se ajusta: compresión paralela (1), módulo (2) y densidad (3). `f_m` no está.
   Sobre `f_m` solo actúan `k_h` y `k_l`.
3. **`k_h` NO se aplica a la muestra 3.** Condición del §5.4.3: canto < 150 mm y densidad
   ≤ 700 kg/m³. La muestra 3 tiene h ≈ 190 mm, así que ahí `k_h = 1` (no se aplica
   `(150/h)^0,2` con h > 150, que daría un factor < 1 y penalizaría sin respaldo normativo).
4. **La fórmula (7)** `E0 = 1,3·E_global − 2690` **no se usa acá.** Es para módulo global,
   y la nota del §5.4.4 aclara que ese módulo se determina con G infinito. Nosotros
   calculamos el local con G = E/16, así que va la (8) y el valor pasa directo.
5. **El ajuste de densidad por 1,05** (§5.3.4) probablemente **no corresponde**: es para
   probetas que no se ensayan hasta rotura, y acá las 258 se rompieron. **VERIFICAR** con el
   docente antes de decidir; son 4,8 % de densidad, suficiente para cambiar de clase. En
   `scripts/03_correcciones_en384.py` está como la constante `AJUSTE_105 = False`: cambiarla
   a `True` y volver a correr los scripts 03 y 90 alcanza para cuantificar el efecto.

### Resultado

Factores, constantes dentro de cada muestra salvo por la dispersión del canto:

| Muestra | `a_f` [mm] | `l_et` [mm] | `48h` [mm] | `k_h` | `k_l` |
|---|---|---|---|---|---|
| 1 | 564,0 | 4591 | 4509 | 1,0934 – 1,1046 | 0,9905 – 1,0007 |
| 2 | 852,0 | 6975 | 6821 | 1,0065 – 1,0143 | 0,9922 – 0,9999 |
| 3 | 1139,9 | 9274 | 9112 | 1,0000 | 0,9925 – 0,9999 |

Valores corregidos, que son la entrada de la etapa 3:

| Muestra | n | `f_m` [N/mm²] | CoV | `E_0` [N/mm²] | CoV | `ro` [kg/m³] | CoV |
|---|---|---|---|---|---|---|---|
| 1 | 89 | 33,78 | 20,3 % | 13 706 | 13,1 % | 450,0 | 6,0 % |
| 2 | 90 | 38,88 | 17,1 % | 13 388 | 10,8 % | 417,3 | 6,0 % |
| 3 | 79 | 39,83 | 26,4 % | 13 839 | 14,4 % | 447,3 | 6,8 % |

Variación del valor medio por efecto de las correcciones: `f_m` −8,60 % / −0,63 % / +0,35 %;
`E_0` y `ro` por debajo del 0,1 % en las tres. Manda `k_h` en la muestra 1. Las correcciones
de humedad salen chicas en media porque el CH medio de las tres muestras cae entre 11,96 % y
12,07 %, pero a nivel individual el rango es 9,8 % – 13,9 % y la corrección del módulo llega
al 2,2 % en la pieza más desfavorable: por eso se aplica pieza a pieza igual.

Detalle en [`resultados/03_resumen_etapa2.md`](../resultados/03_resumen_etapa2.md) y tabla
completa en [`resultados/03_valores_corregidos.csv`](../resultados/03_valores_corregidos.csv).

**Ojo con la muestra 1:** después de corregir pasa a ser claramente la más débil (33,78 contra
38,88 y 39,83). Como la fórmula (11) de EN 384 mira el mínimo entre submuestras, es la que va
a gobernar el valor característico del lote.

### Checklist

- [x] Corregir `E_m,l` y `ro` por humedad, pieza por pieza
- [x] Calcular `k_h` de cada pieza, con `k_h = 1` en la muestra 3
- [x] Calcular `k_l` de cada pieza, con `a_f = l − 2a`
- [x] Aplicar `f_m,corr = f_m / (k_h · k_l)`
- [x] Exportar la tabla de 258 filas para el Anexo B
- [x] Comparar medias antes y después de corregir, y explicar la diferencia
- [ ] Resolver la duda del 1,05 en densidad y dejar la decisión documentada

---

## Dudas abiertas para el docente

1. **¿Cómo se midió `ro`?** Si se midió sobre pieza completa corresponde dividir por 1,05
   (§5.3.4); si se midió sobre probetas pequeñas libres de defectos, no. El archivo no lo
   declara. Es un 4,8 % y puede cambiar la clase.
