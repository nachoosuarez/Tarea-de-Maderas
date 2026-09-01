# Semana 5 — Asignación de la clase resistente

Cubre la **Etapa 4**. Es el resultado del trabajo: media página de cálculo apoyada en todo lo
anterior.

**Entregable:** la clase resistente asignada, con la tabla de verificación de los tres
criterios y la identificación de cuál gobierna. Más el borrador del informe.

---

## Procedimiento (UNE-EN 338:2010)

Picea es conífera, así que se busca dentro de las **clases C** (C14 a C50).

Entran tres valores y tienen que cumplir **los tres a la vez**:

| Magnitud | Símbolo | Unidad |
|---|---|---|
| Resistencia característica a flexión | `f_m,k` | N/mm² |
| Módulo de elasticidad medio paralelo | `E_0,mean` | kN/mm² |
| Densidad característica | `ro_k` | kg/m³ |

Se asigna **la clase más alta cuyos tres requisitos se cumplen simultáneamente**. Alcanza con
que uno de los tres no llegue para bajar de clase.

## Formato de la verificación

| Criterio | Valor obtenido | Requisito de la clase | Relación | Cumple |
|---|---|---|---|---|
| `f_m,k` | | | | |
| `E_0,mean` | | | | |
| `ro_k` | | | | |

Y decir explícitamente **cuál de los tres gobierna**. Lo habitual es que sea el módulo de
elasticidad: la resistencia suele dar de sobra y la rigidez es la que frena.

## Checklist

- [ ] Armar la tabla de clases C de EN 338:2010 (S03E02 p.56) y verificar que se lee bien
- [ ] Verificar los tres criterios contra cada clase candidata
- [ ] Asignar la clase e identificar el criterio que gobierna
- [ ] Comentar cuánto margen queda hasta la clase siguiente
- [ ] Borrador del informe con la estructura completa

## Advertencias

- **No asignar la clase mirando solo `f_m,k`.** Es el error de cierre más común: se llega con
  la resistencia a una clase alta y se ignora que el módulo no da.
- La decisión pendiente sobre el ajuste de densidad por 1,05 (ver semanas 2-3) impacta
  directo acá. Si `ro_k` queda cerca del límite de una clase, esa decisión define el
  resultado y hay que dejarla justificada por escrito.
