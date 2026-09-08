# Semana 5 — Asignación de la clase resistente

Cubre la **Etapa 4**. Es el resultado del trabajo: media página de cálculo apoyada en todo lo
anterior.

**Entregable:** la clase resistente asignada, con la tabla de verificación de los tres
criterios y la identificación de cuál gobierna. Más el borrador del informe.

**Estado: hecha.** Lo produce [`scripts/05_clase_resistente.py`](../scripts/05_clase_resistente.py).

---

# Resultado

## **Clase resistente del lote: C22** (UNE-EN 338:2010)

| Criterio | Obtenido | Exigido por C22 | Relación | Margen | Cumple |
|---|---|---|---|---|---|
| `f_m,k` [N/mm²] | **22,88** | 22,0 | 1,040 | +4,0 % | sí |
| `E_0,mean` [kN/mm²] | **13,492** | 10,0 | 1,349 | +34,9 % | sí |
| `ro_k` [kg/m³] | **365,4** | 340 | 1,075 | +7,5 % | sí |

**Gobierna `f_m,k`**, y es el único de los tres que impide subir a C24: para alcanzarla
faltan **1,12 N/mm²**, un 4,9 % por encima del valor obtenido. Los otros dos criterios de la
C24 se cumplen (`E_0,mean` rel. 1,227 y `ro_k` rel. 1,044).

La verificación completa contra las doce clases C está en `resultados/05_verificacion_clases.csv`
y en el **anexo D** del informe.

## Decisiones que se tomaron y por qué

**La edición importa, y no es un detalle formal.** Las diapositivas del curso traen las dos:
S03E02 p.54-55 es EN 338:**2010** y p.56-57 es EN 338:**2016**. El mismo ejemplo de castaño
resuelto en la diapositiva da **D24 por la 2010 y D27 por la 2016**. La letra del trabajo
manda expresamente la **2010**, que es la que se aplicó.

**Trampa de unidades.** La tabla 1 de EN 338 da `E_0,medio` en **kN/mm²**, y todo el cálculo
de las etapas 1 a 3 está en N/mm². La comparación se hace sobre `E_0,mean/1000` = 13,492. Sin
dividir, los 13 492 superan cualquier fila de la tabla y la clase saldría C50 por rigidez.

**De dónde salió la tabla.** EN 338 **no está** en el zip de normas de AENOR (ahí solo hay
EN 384 y EN 14358). La tabla se leyó de la diapositiva S03E02 p.55, renderizada a 420 dpi para
poder distinguir los dígitos. No es una fuente improvisada: la letra dice textualmente que
«para ello basta con las diapositivas del curso (S03E02)».

**Se validó el procedimiento antes de usarlo.** El ejemplo de castaño de la propia diapositiva
(`f_m,k` = 28 · `E_0,medio` = 12,3 · `ro_k` = 510) tiene que dar D24 por la 2010. El script lo
corre como autovalidación al arrancar y aborta si no coincide. Da D24, y da D27 al cambiarle
la tabla por la de 2016 — los dos resultados que muestra la diapositiva.

**Se recorre la tabla entera, no se corta en el primer incumplimiento.** Los tres requisitos
crecen juntos al subir de clase, pero no de forma proporcional entre sí, así que la
monotonía del cumplimiento no está garantizada de antemano. Cuesta doce iteraciones y evita
tener que suponerlo.

## Robustez: qué decisión podría cambiar la clase

Se rehízo la asignación completa cambiando una decisión por vez:

| Decisión alternativa | `f_m,k` | `ro_k` | Clase | Efecto |
|---|---|---|---|---|
| base: log-normal y `k_s` por la fórmula (10) | 22,88 | 365,4 | C22 | — |
| `k_s` de la Tabla 1 de EN 14358 | 22,80 | 365,4 | C22 | sin efecto |
| **distribución normal en vez de log-normal** | **20,90** | 365,4 | **C20** | **cambia** |
| densidad dividida por 1,05 (EN 384 §5.3.4) | 22,88 | 348,0 | C22 | sin efecto |

Dos conclusiones que hay que decir en el informe:

1. **La duda del 1,05 dejó de ser decisiva.** 348,0 sigue por encima de los 340 que pide la
   C22. Igual conviene preguntarle al docente cómo se midió `ρ` para dejar el dato cerrado,
   pero ya no puede cambiar el resultado del trabajo.
2. **La elección de la distribución es el punto más sensible de todo el trabajo.** Es lo único
   que mueve la clase. No es discrecional —EN 14358 §3.2.2 prescribe log-normal para
   resistencia y normal para densidad, y el estadístico D de Kolmogorov-Smirnov confirma que
   la log-normal ajusta mejor en las tres submuestras— pero hay que declararla explícitamente.

## Lo que contradice la expectativa

El README de esta carpeta decía, antes de calcular, que «lo habitual es que gobierne el
módulo de elasticidad: la resistencia suele dar de sobra y la rigidez es la que frena».
**En este lote pasa exactamente lo contrario:** el módulo sobra un 35 % y es la resistencia
la que frena, con apenas un 4 % de margen. El lote es rígido en relación con su resistencia.

Consecuencia práctica, que va a las conclusiones: subir de clase pasa por **reducir la
dispersión de la resistencia**, no por seleccionar piezas más rígidas. Un criterio visual más
severo sobre nudos —que son los que gobiernan la cola inferior— tendría más efecto que
cualquier cosa que se haga sobre la rigidez.

## Checklist

- [x] Armar la tabla de clases C de EN 338:2010 (S03E02 **p.55**, no p.56 que es la de 2016)
      y verificar que se lee bien
- [x] Verificar los tres criterios contra cada clase candidata
- [x] Asignar la clase e identificar el criterio que gobierna
- [x] Comentar cuánto margen queda hasta la clase siguiente
- [x] Borrador del informe con la estructura completa

## Advertencias

- **No asignar la clase mirando solo `f_m,k`.** Es el error de cierre más común: se llega con
  la resistencia a una clase alta y se ignora que el módulo no da. Acá el riesgo era el
  simétrico y también se evitó: el módulo daba para C40 y no alcanza.
- **Convertir `E_0,mean` a kN/mm² antes de comparar.** Es el único punto de todo el trabajo
  donde cambian las unidades.
- La decisión sobre el ajuste de densidad por 1,05 (ver semanas 2-3) se evaluó como escenario
  y **no cambia la clase**. Queda documentada igual, porque el informe tiene que decir qué se
  hizo ante un dato no declarado.

## Duda abierta para el docente

Se mantiene la de la semana 4, ya sin capacidad de alterar el resultado:

> ¿La densidad `ro` del archivo de datos se midió sobre probeta pequeña libre de defectos, o
> sobre la pieza completa? En el segundo caso corresponde el divisor 1,05 del §5.3.4 de
> EN 384:2016. Se calculó por las dos vías: la clase asignada es C22 en ambos casos.
