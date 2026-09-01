# Semanas 2 y 3 — Propiedades por pieza y corrección a condiciones de referencia

Cubre las **Etapas 1 y 2** de la planificación. Es la parte más larga porque son 258 piezas
por cinco operaciones, y todo lo que venga después se apoya en que esto esté bien.

**Entregable:** una tabla de 258 filas con los valores corregidos de `f_m`, `E_0` y `ro`,
lista para alimentar la estadística. Es el **Anexo A** del informe.

---

## Semana 2 — Etapa 1: propiedades de cada pieza (EN 408)

Dos números por viga, sin corregir nada todavía.

```
f_m   = 3 · Pmax · a / (b · h²)                            [S03E02 p.28]

E_m,l = (P/f) · (3·a·l² − 4·a³ + 38,4·a·h²) / (4·b·h³)     [S03E02 p.26, con G = E/16]
```

El segundo es el despeje de la ecuación implícita, ya verificado en la semana 1.

### Checklist

- [ ] Calcular `f_m` de las 258 piezas
- [ ] Calcular `E_m,l` de las 258 piezas
- [ ] Contrastar contra los rangos de la auditoría (f_m medio ~37-40, E_m,l medio ~13400-13900)
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
| 4 | Luz de ensayo | `f_m / k_l`, con `k_l = (48h/l_et)^0,2` y `l_et = l + 5·a` | §5.4.3 (5)(6) |
| 5 | Módulo local a E0 | `E0 = E_m,local(u_ref)`, directo | §5.4.4 (8) |

### Las cuatro trampas de esta etapa

1. **`k_h` NO se aplica a la muestra 3.** Condición del §5.4.3: canto < 150 mm y densidad
   ≤ 700 kg/m³. La muestra 3 tiene h ≈ 190 mm, así que ahí `k_h = 1`.
2. **`k_l` NO vale 1** en ninguna muestra: l/h medido es 18,86 / 19,10 / 18,83. Se calcula
   pieza por pieza. Ojo con el signo en `l_et = l + 5·a` — es suma, no resta.
3. **La fórmula (7)** `E0 = 1,3·E_global − 2690` **no se usa acá.** Es para módulo global;
   nosotros calculamos el local, así que va la (8) y el valor pasa directo.
4. **El ajuste de densidad por 1,05** (§5.3.4) probablemente **no corresponde**: es para
   probetas que no se ensayan hasta rotura, y acá las 258 se rompieron. **VERIFICAR** con el
   docente antes de decidir; son 4,8 % de densidad, suficiente para cambiar de clase.

### Checklist

- [ ] Corregir `E_m,l` y `ro` por humedad, pieza por pieza
- [ ] Calcular `k_h` de cada pieza, con `k_h = 1` en la muestra 3
- [ ] Calcular `k_l` de cada pieza
- [ ] Aplicar `f_m,corr = f_m / (k_h · k_l)`
- [ ] Resolver la duda del 1,05 en densidad y dejar la decisión documentada
- [ ] Exportar la tabla de 258 filas para el Anexo A
- [ ] Comparar medias antes y después de corregir, y explicar la diferencia
