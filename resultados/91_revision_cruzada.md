# Revisión cruzada del informe

Salida de `scripts/91_revision_cruzada.py`. Cada fila vuelve a calcular desde los datos un número que en el `INFORME.tex` está **escrito a mano**, fuera de los bloques automáticos, y lo compara con los mismos decimales con que está impreso.

**117 comprobaciones, 0 con diferencia.**

| Dónde                | Qué se comprueba                                      | En el informe                      | Recalculado | Estado |
|----------------------|-------------------------------------------------------|------------------------------------|-------------|--------|
| 2.2 tabla lote       | total de piezas                                       | 258                                | 258         | OK     |
| 2.2 tabla lote, m1   | n                                                     | 89                                 | 89          | OK     |
| 2.2 tabla lote, m1   | b medio                                               | 35,93                              | 35,93       | OK     |
| 2.2 tabla lote, m1   | h medio                                               | 93,94                              | 93,94       | OK     |
| 2.2 tabla lote, m1   | h minimo                                              | 91,2                               | 91,2        | OK     |
| 2.2 tabla lote, m1   | h maximo                                              | 96,0                               | 96,0        | OK     |
| 2.2 tabla lote, m1   | a                                                     | 603,7                              | 603,7       | OK     |
| 2.2 tabla lote, m1   | luz l                                                 | 1771,4                             | 1771,4      | OK     |
| 2.2 tabla lote, m1   | a y l constantes dentro de la muestra                 | --                                 | --          | OK     |
| 2.2 tabla lote, m2   | n                                                     | 90                                 | 90          | OK     |
| 2.2 tabla lote, m2   | b medio                                               | 44,92                              | 44,92       | OK     |
| 2.2 tabla lote, m2   | h medio                                               | 142,10                             | 142,10      | OK     |
| 2.2 tabla lote, m2   | h minimo                                              | 139,7                              | 139,7       | OK     |
| 2.2 tabla lote, m2   | h maximo                                              | 145,2                              | 145,2       | OK     |
| 2.2 tabla lote, m2   | a                                                     | 931,3                              | 931,3       | OK     |
| 2.2 tabla lote, m2   | luz l                                                 | 2714,6                             | 2714,6      | OK     |
| 2.2 tabla lote, m2   | a y l constantes dentro de la muestra                 | --                                 | --          | OK     |
| 2.2 tabla lote, m3   | n                                                     | 79                                 | 79          | OK     |
| 2.2 tabla lote, m3   | b medio                                               | 57,00                              | 57,00       | OK     |
| 2.2 tabla lote, m3   | h medio                                               | 189,83                             | 189,83      | OK     |
| 2.2 tabla lote, m3   | h minimo                                              | 186,1                              | 186,1       | OK     |
| 2.2 tabla lote, m3   | h maximo                                              | 193,1                              | 193,1       | OK     |
| 2.2 tabla lote, m3   | a                                                     | 1217,1                             | 1217,1      | OK     |
| 2.2 tabla lote, m3   | luz l                                                 | 3574,1                             | 3574,1      | OK     |
| 2.2 tabla lote, m3   | a y l constantes dentro de la muestra                 | --                                 | --          | OK     |
| anexo A, m1          | relacion l/h sobre el canto medio                     | 18,86                              | 18,86       | OK     |
| anexo A, m1          | relacion a/h sobre el canto medio                     | 6,43                               | 6,43        | OK     |
| 2.3 tabla rangos, m1 | CH minimo                                             | 10,2                               | 10,2        | OK     |
| 2.3 tabla rangos, m1 | CH maximo                                             | 13,6                               | 13,6        | OK     |
| 2.3 tabla rangos, m1 | CH medio                                              | 11,97                              | 11,97       | OK     |
| 2.3 tabla rangos, m1 | densidad minima                                       | 389                                | 389         | OK     |
| 2.3 tabla rangos, m1 | densidad maxima                                       | 519                                | 519         | OK     |
| 2.3 tabla rangos, m1 | Pmax minima                                           | 3299                               | 3299        | OK     |
| 2.3 tabla rangos, m1 | Pmax maxima                                           | 10740                              | 10740       | OK     |
| 2.3 tabla rangos, m1 | P/f minima                                            | 208                                | 208         | OK     |
| 2.3 tabla rangos, m1 | P/f maxima                                            | 457                                | 457         | OK     |
| anexo A, m2          | relacion l/h sobre el canto medio                     | 19,10                              | 19,10       | OK     |
| anexo A, m2          | relacion a/h sobre el canto medio                     | 6,55                               | 6,55        | OK     |
| 2.3 tabla rangos, m2 | CH minimo                                             | 10,7                               | 10,7        | OK     |
| 2.3 tabla rangos, m2 | CH maximo                                             | 13,9                               | 13,9        | OK     |
| 2.3 tabla rangos, m2 | CH medio                                              | 12,07                              | 12,07       | OK     |
| 2.3 tabla rangos, m2 | densidad minima                                       | 370                                | 370         | OK     |
| 2.3 tabla rangos, m2 | densidad maxima                                       | 489                                | 489         | OK     |
| 2.3 tabla rangos, m2 | Pmax minima                                           | 8710                               | 8710        | OK     |
| 2.3 tabla rangos, m2 | Pmax maxima                                           | 19673                              | 19673       | OK     |
| 2.3 tabla rangos, m2 | P/f minima                                            | 284                                | 284         | OK     |
| 2.3 tabla rangos, m2 | P/f maxima                                            | 491                                | 491         | OK     |
| anexo A, m3          | relacion l/h sobre el canto medio                     | 18,83                              | 18,83       | OK     |
| anexo A, m3          | relacion a/h sobre el canto medio                     | 6,41                               | 6,41        | OK     |
| 2.3 tabla rangos, m3 | CH minimo                                             | 9,8                                | 9,8         | OK     |
| 2.3 tabla rangos, m3 | CH maximo                                             | 13,5                               | 13,5        | OK     |
| 2.3 tabla rangos, m3 | CH medio                                              | 11,96                              | 11,96       | OK     |
| 2.3 tabla rangos, m3 | densidad minima                                       | 379                                | 379         | OK     |
| 2.3 tabla rangos, m3 | densidad maxima                                       | 523                                | 523         | OK     |
| 2.3 tabla rangos, m3 | Pmax minima                                           | 12773                              | 12773       | OK     |
| 2.3 tabla rangos, m3 | Pmax maxima                                           | 46155                              | 46155       | OK     |
| 2.3 tabla rangos, m3 | P/f minima                                            | 360                                | 360         | OK     |
| 2.3 tabla rangos, m3 | P/f maxima                                            | 699                                | 699         | OK     |
| 2.3 texto            | humedad minima del lote                               | 9,8                                | 9,8         | OK     |
| 2.3 texto            | humedad maxima del lote                               | 13,9                               | 13,9        | OK     |
| 2.3 texto            | ninguna pieza supera u = 18 %                         | --                                 | --          | OK     |
| 2.3 texto            | no hay vigas duplicadas                               | --                                 | --          | OK     |
| 4.2 texto, m1        | separacion entre cargas a_f = l - 2a                  | 564,0                              | 564,0       | OK     |
| 4.2 texto, m1        | a_f en cantos (a_f/h)                                 | 6,00                               | 6,00        | OK     |
| 4.2 texto, m2        | separacion entre cargas a_f = l - 2a                  | 852,0                              | 852,0       | OK     |
| 4.2 texto, m2        | a_f en cantos (a_f/h)                                 | 6,00                               | 6,00        | OK     |
| 4.2 texto, m3        | separacion entre cargas a_f = l - 2a                  | 1139,9                             | 1139,9      | OK     |
| 4.2 texto, m3        | a_f en cantos (a_f/h)                                 | 6,01                               | 6,01        | OK     |
| 4.2 texto            | k_h medio de la muestra 1                             | 1,098                              | 1,098       | OK     |
| 4.2 texto            | k_h = 1 en toda la muestra 3 (canto > 150 mm)         | --                                 | --          | OK     |
| 4.2 texto            | k_l distinto de 1 en las tres muestras                | --                                 | --          | OK     |
| 4.2 texto            | caida de f_m en la muestra 1                          | 8,6                                | 8,6         | OK     |
| 4.2 texto            | efecto neto en la muestra 2                           | -0,6                               | -0,6        | OK     |
| 4.2 texto            | correccion de humedad maxima sobre el modulo          | 2,2                                | 2,2         | OK     |
| 4.2 texto            | efecto del divisor 1,05 sobre la densidad             | 4,8                                | 4,8         | OK     |
| anexo A, m1          | f_m sin corregir, minima                              | 18,5                               | 18,5        | OK     |
| anexo A, m1          | f_m sin corregir, maxima                              | 64,0                               | 64,0        | OK     |
| anexo A, m1          | f_m sin corregir, media                               | 37,0                               | 37,0        | OK     |
| anexo A, m1          | E_m,l sin corregir, minimo                            | 8549                               | 8549        | OK     |
| anexo A, m1          | E_m,l sin corregir, maximo                            | 19721                              | 19721       | OK     |
| anexo A, m1          | E_m,l sin corregir, medio                             | 13709                              | 13709       | OK     |
| anexo A, m2          | f_m sin corregir, minima                              | 26,3                               | 26,3        | OK     |
| anexo A, m2          | f_m sin corregir, maxima                              | 60,6                               | 60,6        | OK     |
| anexo A, m2          | f_m sin corregir, media                               | 39,1                               | 39,1        | OK     |
| anexo A, m2          | E_m,l sin corregir, minimo                            | 10212                              | 10212       | OK     |
| anexo A, m2          | E_m,l sin corregir, maximo                            | 17286                              | 17286       | OK     |
| anexo A, m2          | E_m,l sin corregir, medio                             | 13379                              | 13379       | OK     |
| anexo A, m3          | f_m sin corregir, minima                              | 23,4                               | 23,4        | OK     |
| anexo A, m3          | f_m sin corregir, maxima                              | 84,2                               | 84,2        | OK     |
| anexo A, m3          | f_m sin corregir, media                               | 39,7                               | 39,7        | OK     |
| anexo A, m3          | E_m,l sin corregir, minimo                            | 9773                               | 9773        | OK     |
| anexo A, m3          | E_m,l sin corregir, maximo                            | 19202                              | 19202       | OK     |
| anexo A, m3          | E_m,l sin corregir, medio                             | 13844                              | 13844       | OK     |
| anexo A, m1          | forma cerrada del contraste iterativo                 | 11091,4                            | 11091,4     | OK     |
| anexo A, m2          | forma cerrada del contraste iterativo                 | 14033,3                            | 14033,3     | OK     |
| anexo A, m3          | forma cerrada del contraste iterativo                 | 13186,8                            | 13186,8     | OK     |
| 4.3 texto            | k_s(20) por la expresion (10)                         | 1,915                              | 1,915       | OK     |
| 4.3 texto            | k_s(100) por la expresion (10)                        | 1,787                              | 1,787       | OK     |
| 4.3 texto            | k_s(20) de la Tabla 1                                 | 1,93                               | 1,93        | OK     |
| 4.3 texto            | k_s(100) de la Tabla 1                                | 1,76                               | 1,76        | OK     |
| 4.3 texto            | la Tabla 1 lleva n = 79, 89 y 90 a la entrada n = 50  | --                                 | --          | OK     |
| 4.3 texto            | la sensibilidad al k_s es inferior al 0,4 %           | maxima: 0,35 %                     | --          | OK     |
| 5.2 texto            | en las tres magnitudes gobierna la media ponderada    | --                                 | --          | OK     |
| 5.1 texto            | la submuestra 1 es la mas desfavorable en resistencia | --                                 | --          | OK     |
| 6.1 texto            | el criterio que gobierna la clase es f_m,k            | fmk                                | --          | OK     |
| 6.1 texto            | el modulo cumple con mas margen que la resistencia    | --                                 | --          | OK     |
| estructura           | toda referencia cruzada tiene su etiqueta             | 16 referencias contra 25 etiquetas | --          | OK     |
| estructura           | no queda ningun \verificar en el documento            | 0 marcas                           | --          | OK     |
| estructura           | marcas \pendiente restantes (solo el autor)           | 1 marca(s)                         | --          | OK     |
| estructura           | los bloques automaticos abren y cierran               | 13 bloques                         | --          | OK     |
| sincronia            | el bloque «resumen» dice la clase del CSV             | C22                                | --          | OK     |
| sincronia            | el bloque «clase» dice la clase del CSV               | C22                                | --          | OK     |
| sincronia            | el bloque «conclusion» dice la clase del CSV          | C22                                | --          | OK     |
| sincronia            | el bloque «clase» lleva 22,88                         | 22,88                              | --          | OK     |
| sincronia            | el bloque «conclusion» lleva 22,88                    | 22,88                              | --          | OK     |
| sincronia            | el bloque «clase» lleva 365,4                         | 365,4                              | --          | OK     |
| sincronia            | el bloque «caracteristicos» lleva 13492               | 13492                              | --          | OK     |

## Lo que este script no puede comprobar

- Los valores de la tabla 1 de **UNE-EN 338:2010**: se transcribieron de la diapositiva S03E02 p.55 porque la norma no está en el zip de AENOR. Hay que contrastarlos a mano contra la fuente.
- Los **coeficientes normativos** (`k_n`, el piso de CoV, los topes 1,2 y 1,1, el divisor 0,95): se cotejan contra su apartado en `06-referencias/README.md`, no contra los datos.
- La **redacción**: que una frase diga lo que el número dice es cosa de leerla.
