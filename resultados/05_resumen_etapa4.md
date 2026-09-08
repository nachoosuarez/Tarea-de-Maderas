# Etapa 4 - Asignacion de la clase resistente

Generado por `scripts/05_clase_resistente.py`. No editar a mano.

Norma: **UNE-EN 338:2010**, Tabla 1, via diapositiva S03E02 p.55, que es la
fuente que habilita la letra del trabajo. Picea es conifera: clases **C**.

## Autovalidacion del metodo

El castano de la propia diapositiva (f_m,k = 28 N/mm2, E_0,medio = 12,3
kN/mm2, ro_k = 510 kg/m3) da **D24** con esta implementacion, y la
diapositiva asigna D24. Coincide, asi que la tabla transcrita y la regla
de asignacion estan bien.

## Datos de entrada

| Magnitud | Valor  | Unidad | Origen                           |
|----------|--------|--------|----------------------------------|
| f_m,k    | 22,88  | N/mm2  | etapa 3, EN 384 form. (11)       |
| E_0,mean | 13492  | N/mm2  | etapa 3, EN 384 form. (12)       |
| E_0,mean | 13,492 | kN/mm2 | el mismo, en la unidad de EN 338 |
| ro_k     | 365,4  | kg/m3  | etapa 3, EN 384 form. (13)       |

## Verificacion clase por clase

Relacion = valor obtenido / minimo exigido. Cumple si es >= 1,00.

| Clase | f_m,k min | rel.  | E_0 min | rel.  | ro_k min | rel.  | Cumple |
|-------|-----------|-------|---------|-------|----------|-------|--------|
| C14   | 14        | 1,634 | 7,0     | 1,927 | 290      | 1,260 | SI     |
| C16   | 16        | 1,430 | 8,0     | 1,687 | 310      | 1,179 | SI     |
| C18   | 18        | 1,271 | 9,0     | 1,499 | 320      | 1,142 | SI     |
| C20   | 20        | 1,144 | 9,5     | 1,420 | 330      | 1,107 | SI     |
| C22   | 22        | 1,040 | 10,0    | 1,349 | 340      | 1,075 | SI     |
| C24   | 24        | 0,953 | 11,0    | 1,227 | 350      | 1,044 | no     |
| C27   | 27        | 0,847 | 11,5    | 1,173 | 370      | 0,987 | no     |
| C30   | 30        | 0,763 | 12,0    | 1,124 | 380      | 0,961 | no     |
| C35   | 35        | 0,654 | 13,0    | 1,038 | 400      | 0,913 | no     |
| C40   | 40        | 0,572 | 14,0    | 0,964 | 420      | 0,870 | no     |
| C45   | 45        | 0,508 | 15,0    | 0,899 | 440      | 0,830 | no     |
| C50   | 50        | 0,458 | 16,0    | 0,843 | 460      | 0,794 | no     |

## Resultado

**Clase resistente asignada: C22**

| Criterio | Obtenido | Exigido | Unidad | Relacion | Margen | Verificacion |
|----------|----------|---------|--------|----------|--------|--------------|
| f_m,k    | 22,88    | 22,00   | N/mm2  | 1,040    | 4,0 %  | cumple       |
| E_0,mean | 13,49    | 10,00   | kN/mm2 | 1,349    | 34,9 % | cumple       |
| ro_k     | 365,37   | 340,00  | kg/m3  | 1,075    | 7,5 %  | cumple       |

### Que impide subir a C24

Gobierna: **f_m,k**.

| Criterio | Obtenido | Exigido para C24 | Unidad | Falta | Falta rel. | Verificacion |
|----------|----------|------------------|--------|-------|------------|--------------|
| f_m,k    | 22,88    | 24,00            | N/mm2  | 1,12  | 4,9 %      | NO CUMPLE    |
| E_0,mean | 13,49    | 11,00            | kN/mm2 | -     | -          | cumple       |
| ro_k     | 365,37   | 350,00           | kg/m3  | -     | -          | cumple       |

## Escenario del ajuste de densidad (EN 384 §5.3.4)

Si la densidad se hubiera medido sobre pieza completa, corresponderia
dividirla por 1,05:

    ro_k = 365,4 / 1,05 = 348,0 kg/m3  ->  clase C22

**La clase no cambia.** La decision pendiente sobre el 1,05 no altera el
resultado del trabajo, porque quien gobierna no es la densidad.

## Robustez frente a las decisiones de criterio

Cada fila rehace la asignacion cambiando una sola decision.

| Escenario                                   | f_m,k | ro_k  | Clase | Efecto |
|---------------------------------------------|-------|-------|-------|--------|
| base: log-normal y k_s por la formula (10)  | 22,88 | 365,4 | C22   | igual  |
| k_s de la Tabla 1 en vez de la formula (10) | 22,80 | 365,4 | C22   | igual  |
| distribucion normal en vez de log-normal    | 20,90 | 365,4 | C20   | CAMBIA |
| densidad dividida por 1,05 (EN 384 5.3.4)   | 22,88 | 348,0 | C22   | igual  |

La unica decision que mueve la clase es **distribucion normal en vez de log-normal**.
Esta cerrada por la norma: EN 14358 §3.2.2 c) impone la log-normal
salvo que el analisis estadistico demuestre que la normal ajusta
mejor, y el contraste de Kolmogorov-Smirnov de la etapa 3 muestra lo
contrario en las tres submuestras. Aun asi conviene declararlo en el
informe, porque es el punto mas sensible del trabajo.

