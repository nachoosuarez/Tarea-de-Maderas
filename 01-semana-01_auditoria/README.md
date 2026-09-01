# Semana 1 — Auditoría de los datos

**Estado: hecha.**

Antes de calcular nada hay que saber si el archivo de datos es utilizable y si el ensayo
cumple lo que la norma exige. Esto no es un trámite: dos de los hallazgos de acá cambian
fórmulas de las etapas siguientes.

**Entregable:** tabla de control del lote, que después se reusa tal cual en la sección
*Datos de partida* del informe y en el Anexo C.

## Checklist

- [x] Parsear las 258 filas sin errores, confirmar separador y decimal
- [x] Contar probetas por muestra y contrastar contra el mínimo de EN 384 §5.1
- [x] Verificar la geometría de ensayo de cada pieza contra EN 408 (l = 18h ± 3h, a = 6h ± 1,5h)
- [x] Verificar que las humedades caen en el rango de validez de EN 384 §5.4.2 (8 % a 18 %)
- [x] Resolver la ambigüedad de unidades de `P/f`
- [x] Chequeo de orden de magnitud de `f_m` y `E_m,l`
- [x] Verificar el despeje de la ecuación implícita del módulo local

## Cómo reproducirlo

```bash
python scripts/00_auditoria_datos.py
python scripts/01_verif_despeje_modulo_local.py
```

## Resultados

Ver [`resultado-auditoria.md`](resultado-auditoria.md).

Los tres hallazgos que impactan en las etapas siguientes:

1. **`k_h` no se aplica a la muestra 3** (canto ≈ 190 mm > 150 mm).
2. **`k_l` no vale 1** en ninguna muestra: l/h medido es 18,86 / 19,10 / 18,83.
3. **El ajuste de densidad por 1,05 probablemente no corresponde**, porque todas las piezas
   se ensayaron hasta rotura. Queda marcado **VERIFICAR** con el docente.
