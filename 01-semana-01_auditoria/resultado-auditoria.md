# Resultado de la auditoría — `Datos_Picea.txt`

Generado con `scripts/00_auditoria_datos.py` el 31/08/2026.

## Integridad del archivo

- 258 filas de datos, **0 no parseadas**, **0 vigas duplicadas**.
- Separador: tabulador. Decimal: punto. Dos filas de encabezado.
- Unidades declaradas en el propio archivo: `b h a l` en mm, `CH` en %, `ro` en kg/m³,
  `Pmax` en N, **`P/f` en N/mm**.

## Composición del lote

| Muestra | n | b medio [mm] | h medio [mm] | h mín–máx [mm] | a [mm] | l [mm] | l/h | a/h |
|---|---|---|---|---|---|---|---|---|
| 1 | 89 | 35,93 | 93,94 | 91,2 – 96,0 | 603,7 | 1771,4 | 18,86 | 6,43 |
| 2 | 90 | 44,92 | 142,10 | 139,7 – 145,2 | 931,3 | 2714,6 | 19,10 | 6,55 |
| 3 | 79 | 57,00 | 189,83 | 186,1 – 193,1 | 1217,1 | 3574,1 | 18,83 | 6,41 |

**Tamaño de muestra — EN 384 §5.1:** exige un mínimo de 40 probetas por muestra para
clasificación visual. Las tres cumplen (89 / 90 / 79). No hay desvío que reportar.

## Geometría de ensayo — EN 408

Tolerancias: `l = 18h ± 3h` (o sea 15h a 21h) y `a = 6h ± 1,5h` (4,5h a 7,5h).

| Muestra | Piezas fuera de rango en `l` | Piezas fuera de rango en `a` |
|---|---|---|
| 1 | 0 | 0 |
| 2 | 0 | 0 |
| 3 | 0 | 0 |

Las 258 piezas cumplen. **Pero l/h no es 18 exacto** (18,86 / 19,10 / 18,83), así que el
coeficiente `k_l` de EN 384 §5.4.3 no vale 1 y hay que calcularlo pieza por pieza.

## Rangos medidos

| Muestra | CH [%] | CH medio | Fuera de 8–18 % | ro [kg/m³] | Pmax [N] | P/f [N/mm] |
|---|---|---|---|---|---|---|
| 1 | 10,2 – 13,6 | 11,97 | 0 | 389 – 519 | 3299 – 10740 | 208 – 457 |
| 2 | 10,7 – 13,9 | 12,07 | 0 | 370 – 489 | 8710 – 19673 | 284 – 491 |
| 3 | 9,8 – 13,5 | 11,96 | 0 | 379 – 523 | 12773 – 46155 | 360 – 699 |

**Humedad — EN 384 §5.4.2:** la corrección solo es válida para 8 % ≤ u ≤ 18 %. Las 258 piezas
están dentro, así que no hay que truncar ninguna a u = 18 %. Las medias quedan muy cerca de
u_ref = 12 %, con lo cual la corrección por humedad va a ser chica — pero se aplica igual,
pieza por pieza, porque hay dispersión individual.

## Chequeo de orden de magnitud

Valores **sin corregir**, calculados solo para validar unidades y descartar errores de
factor 10 o 1000:

| Muestra | f_m mín–máx [N/mm²] | f_m medio | E_m,l mín–máx [N/mm²] | E_m,l medio |
|---|---|---|---|---|
| 1 | 18,5 – 64,0 | 37,0 | 8549 – 19721 | 13709 |
| 2 | 26,3 – 60,6 | 39,1 | 10212 – 17286 | 13379 |
| 3 | 23,4 – 84,2 | 39,7 | 9773 – 19202 | 13844 |

Ambos rangos son coherentes con Picea. Esto confirma que la interpretación de `P/f` en N/mm
como pendiente carga-flecha es la correcta: con la unidad equivocada el módulo se iría varios
órdenes de magnitud.

**No son valores de resultado.** Les falta toda la Etapa 2.

## Verificación del despeje del módulo local

`scripts/01_verif_despeje_modulo_local.py` contrasta la forma cerrada contra la resolución
iterativa de la ecuación implícita de S03E02 p.26 con G = E_m,l/16:

| b [mm] | h [mm] | Forma cerrada [N/mm²] | Iterativa [N/mm²] | Diferencia |
|---|---|---|---|---|
| 36,0 | 93,4 | 11091,4 | 11091,4 | 0,00000 % |
| 44,9 | 142,1 | 14033,3 | 14033,3 | −0,00000 % |
| 57,0 | 189,8 | 13186,8 | 13186,8 | 0,00000 % |

El despeje queda validado y se puede usar directamente:

```
E_m,l = (P/f) · (3·a·l² − 4·a³ + 38,4·a·h²) / (4·b·h³)
```

## Consecuencias para las etapas siguientes

1. **`k_h` (EN 384 §5.4.3) solo aplica a las muestras 1 y 2.** La condición es canto < 150 mm;
   la muestra 3 tiene h ≈ 190 mm, así que ahí `k_h = 1`.
2. **`k_l` se calcula en las tres muestras**, pieza por pieza.
3. **El ajuste de densidad por 1,05 de EN 384 §5.3.4 probablemente no corresponde.** El
   apartado lo reserva para *"las probetas que no se someten a ensayo hasta rotura"*, y acá
   las 258 se ensayaron hasta rotura. **VERIFICAR** con el docente cómo se midió `ro`: el
   4,8 % de diferencia puede cambiar la clase resistente final.
