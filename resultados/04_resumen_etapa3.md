# Etapa 3 — Valores caracteristicos (EN 14358:2016 + EN 384:2016 §5.5)

Generado por `scripts/04_valores_caracteristicos.py`. No editar a mano.

## Percentiles por submuestra (EN 14358 §3.2.2 y §3.3)

| Muestra | n  | k_s(n) | f_05 [N/mm2] | ro_05 [kg/m3] | E medio [N/mm2] |
|---------|----|--------|--------------|---------------|-----------------|
| 1       | 89 | 1,7913 | 22,97        | 401,6         | 13706           |
| 2       | 90 | 1,7909 | 28,29        | 372,3         | 13388           |
| 3       | 79 | 1,7957 | 24,90        | 392,8         | 13839           |

## Chequeo de la distribucion adoptada para la resistencia

EN 14358 §3.2.2 c) manda log-normal salvo que el analisis demuestre que la normal es mas adecuada. D de Kolmogorov-Smirnov, menor es mejor ajuste:

| Muestra | D log-normal | D normal | Mejor ajuste | f_05 log-normal | f_05 normal |
|---------|--------------|----------|--------------|-----------------|-------------|
| 1       | 0,0520       | 0,0859   | log-normal   | 22,97           | 21,50       |
| 2       | 0,0382       | 0,0643   | log-normal   | 28,29           | 26,94       |
| 3       | 0,0848       | 0,1300   | log-normal   | 24,90           | 20,94       |

## Combinacion de las submuestras (EN 384 §5.5.2.2)

`ns = 3` submuestras, `n = 258` probetas. De la Tabla 1: `k_n = 0.90` para resistencias paralelas a la fibra y `k_n = 0.94` para modulo y densidad.

| Magnitud         | Media ponderada | Tope sobre la peor | Gobierna        | k_n  | Valor caracteristico |
|------------------|-----------------|--------------------|-----------------|------|----------------------|
| f_m,k [N/mm2]    | 25,42           | 27,56              | media ponderada | 0,90 | 22,88                |
| E_0,mean [N/mm2] | 13636           | 14727              | media ponderada | 0,94 | 13492                |
| rho_k [kg/m3]    | 388,7           | 409,6              | media ponderada | 0,94 | 365,4                |

El modulo lleva ademas el divisor 0.95 de la formula (12).

## Sensibilidad al k_s(n) adoptado

El calculo usa la formula (10). La Tabla 1 no tabula n = 89/90/79, y su regla es tomar el valor de k_s inmediatamente mayor, que para los tres es el de la entrada n = 50, o sea 1,81. Rehaciendo la cadena entera con ese valor:

| Magnitud      | Con formula (10) | Con Tabla 1 (k_s = 1,81) | Diferencia |
|---------------|------------------|--------------------------|------------|
| f_m,k [N/mm2] | 22,88            | 22,80                    | -0,35 %    |
| rho_k [kg/m3] | 365,4            | 364,9                    | -0,12 %    |

El modulo no aparece porque su valor caracteristico es la media de la muestra (§3.3 d) y no depende de k_s.
