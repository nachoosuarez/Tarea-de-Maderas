# -*- coding: utf-8 -*-
"""Etapa 3: valores caracteristicos del lote.

Dos normas encadenadas:

  UNE-EN 14358:2016 §3  -> percentil del 5 % de cada submuestra y valor medio de rigidez
  UNE-EN 384:2016  §5.5 -> combinacion de las submuestras en f_k, E_0,mean y ro_k

Entrada : resultados/03_valores_corregidos.csv (valores ya en condiciones de referencia)
Salida  : resultados/04_por_submuestra.csv
          resultados/04_resumen_etapa3.md

Uso:  python scripts/04_valores_caracteristicos.py
"""

import math
import os
import statistics as st
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comun as C

# --------------------------------------------------------------------------- constantes
# EN 14358:2016 §3.2.2 d), formulas (3) y (4), p.7: el coeficiente de variacion de la
# muestra no se puede tomar menor que 0,05. En log-normal el piso cae sobre s_y directo;
# en normal, sobre 0,05*media.
PISO_COV = 0.05

# EN 384:2016 Tabla 1, p.13. Factor de ajuste segun el numero de submuestras.
K_N_RESISTENCIA = {1: 0.70, 2: 0.80, 3: 0.90, 4: 0.95}   # paralelas a la fibra
K_N_RIGIDEZ = {1: 0.88, 2: 0.91, 3: 0.94, 4: 0.97}       # modulo y densidad
# 5 submuestras o mas -> 1,00 en ambas filas

# EN 384:2016 §5.5.2.2, formulas (11)(12)(13), p.13-14. Topes sobre la peor submuestra.
TOPE_RESISTENCIA = 1.2   # formula (11)
TOPE_RIGIDEZ = 1.1       # formulas (12) y (13)

# EN 384:2016 formula (12), p.14: el modulo combinado se divide por 0,95. Mismo divisor
# que la formula (10) del apartado anterior para clasificacion por maquina.
DIVISOR_MODULO = 0.95

# EN 14358:2016 Tabla 1, p.8. k_s(n) para propiedades de resistencia, p = 5 %, alfa = 75 %.
TABLA_KS = [(3, 3.15), (5, 2.46), (10, 2.10), (15, 1.99), (20, 1.93),
            (30, 1.87), (50, 1.81), (100, 1.76), (500, 1.69)]
KS_INFINITO = 1.64


# --------------------------------------------------------------------------- EN 14358
def k_s(n):
    """Formula (10) de EN 14358:2016 §3.2.2 f), p.8.

    Es la expresion simplificada que la propia norma admite como alternativa a su
    Tabla 1, calculada con el n real de la submuestra.
    """
    return (6.5 * n + 6.0) / (3.7 * n - 3.0)


def k_s_tabla(n):
    """Valor conservador de la Tabla 1: 'para numeros de probetas no indicados se
    deberia tomar el valor inmediatamente mayor' (EN 14358 §3.2.2 f), p.8).

    Lo que hay que tomar mayor es k_s, no n. Y como k_s DECRECE al crecer n, el k_s
    inmediatamente mayor para un n intermedio es el de la entrada tabulada ANTERIOR:
    para n = 89 corresponde la entrada n = 50 -> 1,81, no la de n = 100 -> 1,76.
    Solo se usa para acotar la sensibilidad del resultado; el calculo va por (10).
    """
    valor = TABLA_KS[0][1]
    for n_tab, k in TABLA_KS:
        if n < n_tab:
            return valor
        valor = k
    return valor if n < 500 else KS_INFINITO


def percentil5(valores, distribucion, ks=None):
    """Percentil del 5 % de una submuestra, EN 14358:2016 §3.2.2, p.7-8.

    log-normal : formulas (1) y (3) para y y s_y, formula (5) para m_k
    normal     : formulas (2) y (4) para y y s_y, formula (6) para m_k

    `ks` permite forzar otro k_s(n) para estudiar la sensibilidad; por defecto usa la
    formula (10).
    """
    n = len(valores)
    if ks is None:
        ks = k_s(n)
    if distribucion == "log-normal":
        muestra = [math.log(v) for v in valores]
        y = st.fmean(muestra)
        s_bruta = st.stdev(muestra)
        s_y = max(s_bruta, PISO_COV)                  # piso de la formula (3)
        mk = math.exp(y - ks * s_y)                   # formula (5)
    elif distribucion == "normal":
        y = st.fmean(valores)
        s_bruta = st.stdev(valores)
        s_y = max(s_bruta, PISO_COV * y)              # piso de la formula (4)
        mk = y - ks * s_y                             # formula (6)
    else:
        raise ValueError(distribucion)
    return {"n": n, "ks": ks, "y": y, "s_bruta": s_bruta, "s_y": s_y,
            "piso_activo": s_y > s_bruta, "mk": mk}


def media_rigidez(valores):
    """Valor caracteristico medio de una propiedad de rigidez.

    EN 14358:2016 §3.3 d), p.10: 'para las propiedades de rigidez, el valor
    caracteristico medio debe determinarse como valor medio de la muestra y tal como
    se indica en la formula (14)'. Sin k_s(n): el §3.3 e) solo lo introduce cuando se
    necesitan intervalos de confianza, que no es el caso.
    """
    return st.fmean(valores)


def ks_bondad(valores, distribucion):
    """Estadistico D de Kolmogorov-Smirnov contra la distribucion ajustada por maxima
    verosimilitud. Es un chequeo informativo del §3.2.2 c) ('log-normal excepto si el
    analisis estadistico demuestra que la normal es mas adecuada'), no una prueba de
    hipotesis formal: D menor = mejor ajuste.
    """
    muestra = sorted(math.log(v) for v in valores) if distribucion == "log-normal" \
        else sorted(valores)
    n = len(muestra)
    mu, sigma = st.fmean(muestra), st.stdev(muestra)
    dist = st.NormalDist(mu, sigma)
    d = 0.0
    for i, x in enumerate(muestra, start=1):
        f = dist.cdf(x)
        d = max(d, abs(f - (i - 1) / n), abs(i / n - f))
    return d


# --------------------------------------------------------------------------- EN 384
def k_n(ns, tipo):
    tabla = K_N_RESISTENCIA if tipo == "resistencia" else K_N_RIGIDEZ
    return tabla.get(ns, 1.00)


def combinar(valores_i, n_i, tope, factor, divisor=1.0):
    """Formulas (11)(12)(13) de EN 384:2016 §5.5.2.2, p.13-14.

        X_k = min( tope * X_min ; suma(n_i * X_i) / n ) * k_n / divisor

    Ojo: el k_n multiplica el minimo ya resuelto, no solo la media ponderada. El texto
    extraido del PDF sugiere lo contrario; contra la pagina renderizada se confirma que
    el '* k_n' esta fuera del parentesis del min.
    """
    n_total = sum(n_i)
    ponderada = sum(ni * xi for ni, xi in zip(n_i, valores_i)) / n_total
    acotado = tope * min(valores_i)
    gobierna = "media ponderada" if ponderada <= acotado else "submuestra mas debil"
    return {"ponderada": ponderada, "acotado": acotado, "min_i": min(valores_i),
            "gobierna": gobierna, "valor": min(ponderada, acotado) * factor / divisor}


# --------------------------------------------------------------------------- main
def main():
    piezas = C.leer_csv("03_valores_corregidos.csv")
    grupos = C.por_muestra(piezas)
    ns = len(grupos)

    filas, res = [], {}
    for m, g in grupos.items():
        fm = [p["fm_ref"] for p in g]
        ro = [p["ro_ref"] for p in g]
        e0 = [p["E0"] for p in g]

        # Resistencia: log-normal por defecto normativo (§3.2.2 c).
        f_ln = percentil5(fm, "log-normal")
        f_no = percentil5(fm, "normal")
        # Densidad: la norma obliga a normal, sin alternativa (§3.2.2 c).
        r_no = percentil5(ro, "normal")
        # Modulo: media aritmetica (§3.3 d).
        e_media = media_rigidez(e0)
        # Sensibilidad: los mismos percentiles con el k_s conservador de la Tabla 1.
        ks_t = k_s_tabla(len(g))
        f_tab = percentil5(fm, "log-normal", ks_t)
        r_tab = percentil5(ro, "normal", ks_t)

        res[m] = {"n": len(g), "f05": f_ln["mk"], "ro05": r_no["mk"], "E": e_media,
                  "f05_tab": f_tab["mk"], "ro05_tab": r_tab["mk"]}
        filas.append({
            "muestra": m, "n": len(g),
            "ks_formula": f_ln["ks"], "ks_tabla": k_s_tabla(len(g)),
            "fm_y": f_ln["y"], "fm_sy": f_ln["s_y"], "fm_piso": "si" if f_ln["piso_activo"] else "no",
            "f05": f_ln["mk"], "f05_normal": f_no["mk"], "f05_tabla": f_tab["mk"],
            "D_lognormal": ks_bondad(fm, "log-normal"), "D_normal": ks_bondad(fm, "normal"),
            "ro_y": r_no["y"], "ro_sy": r_no["s_y"], "ro_piso": "si" if r_no["piso_activo"] else "no",
            "ro05": r_no["mk"], "ro05_tabla": r_tab["mk"],
            "E_media": e_media,
        })

    C.guardar_csv(
        "04_por_submuestra.csv",
        ["muestra", "n", "ks_formula", "ks_tabla",
         "fm_y", "fm_sy", "fm_piso", "f05", "f05_normal", "f05_tabla",
         "D_lognormal", "D_normal",
         "ro_y", "ro_sy", "ro_piso", "ro05", "ro05_tabla", "E_media"],
        filas,
        ["[-]", "[-]", "[-]", "[-]",
         "[ln(N/mm2)]", "[ln(N/mm2)]", "[-]", "[N/mm2]", "[N/mm2]", "[N/mm2]",
         "[-]", "[-]",
         "[kg/m3]", "[kg/m3]", "[-]", "[kg/m3]", "[kg/m3]", "[N/mm2]"])

    orden = list(grupos)
    n_i = [res[m]["n"] for m in orden]
    fk = combinar([res[m]["f05"] for m in orden], n_i,
                  TOPE_RESISTENCIA, k_n(ns, "resistencia"))
    ek = combinar([res[m]["E"] for m in orden], n_i,
                  TOPE_RIGIDEZ, k_n(ns, "rigidez"), DIVISOR_MODULO)
    rk = combinar([res[m]["ro05"] for m in orden], n_i,
                  TOPE_RIGIDEZ, k_n(ns, "rigidez"))

    # Variante conservadora: mismos pasos con el k_s de la Tabla 1 en lugar de la (10).
    fk_t = combinar([res[m]["f05_tab"] for m in orden], n_i,
                    TOPE_RESISTENCIA, k_n(ns, "resistencia"))
    rk_t = combinar([res[m]["ro05_tab"] for m in orden], n_i,
                    TOPE_RIGIDEZ, k_n(ns, "rigidez"))

    # El 90 es consumidor puro: todo lo que necesita el informe tiene que estar en CSV.
    C.guardar_csv(
        "04_valores_lote.csv",
        ["magnitud", "simbolo", "ponderada", "acotado", "gobierna", "kn", "divisor",
         "valor", "valor_ks_tabla"],
        [{"magnitud": "Resistencia característica a flexión", "simbolo": "fmk",
          "ponderada": fk["ponderada"], "acotado": fk["acotado"], "gobierna": fk["gobierna"],
          "kn": k_n(ns, "resistencia"), "divisor": 1.0, "valor": fk["valor"],
          "valor_ks_tabla": fk_t["valor"]},
         {"magnitud": "Módulo de elasticidad medio", "simbolo": "E0mean",
          "ponderada": ek["ponderada"], "acotado": ek["acotado"], "gobierna": ek["gobierna"],
          "kn": k_n(ns, "rigidez"), "divisor": DIVISOR_MODULO, "valor": ek["valor"],
          "valor_ks_tabla": ek["valor"]},
         {"magnitud": "Densidad característica", "simbolo": "rok",
          "ponderada": rk["ponderada"], "acotado": rk["acotado"], "gobierna": rk["gobierna"],
          "kn": k_n(ns, "rigidez"), "divisor": 1.0, "valor": rk["valor"],
          "valor_ks_tabla": rk_t["valor"]}],
        ["[-]", "[-]", "[unidad de la magnitud]", "[unidad de la magnitud]", "[-]", "[-]",
         "[-]", "[unidad de la magnitud]", "[unidad de la magnitud]"])

    # ---------------------------------------------------------------- por pantalla
    print(f"Submuestras: {ns}   n total: {sum(n_i)}")
    print(f"k_n = {k_n(ns,'resistencia'):.2f} (resistencia) / "
          f"{k_n(ns,'rigidez'):.2f} (modulo y densidad)   [EN 384 Tabla 1]")
    for f in filas:
        print(f"  M{f['muestra']} n={f['n']:3d}  ks={f['ks_formula']:.4f}  "
              f"f05={f['f05']:6.2f}  ro05={f['ro05']:6.1f}  E={f['E_media']:7.0f}   "
              f"D_logn={f['D_lognormal']:.4f} D_norm={f['D_normal']:.4f}")
    for nombre, c, d in (("f_m,k    ", fk, 2), ("E_0,mean ", ek, 0), ("rho_k    ", rk, 1)):
        print(f"  {nombre} = {c['valor']:.{d}f}   (pond. {c['ponderada']:.{d}f} / "
              f"tope {c['acotado']:.{d}f} -> gobierna {c['gobierna']})")
    print(f"  sensibilidad con k_s de Tabla 1:  f_m,k = {fk_t['valor']:.2f}  "
          f"({100*(fk_t['valor']/fk['valor']-1):+.2f} %)   "
          f"rho_k = {rk_t['valor']:.1f}  ({100*(rk_t['valor']/rk['valor']-1):+.2f} %)")

    # ---------------------------------------------------------------- resumen .md
    out = ["# Etapa 3 — Valores caracteristicos (EN 14358:2016 + EN 384:2016 §5.5)", "",
           f"Generado por `scripts/{os.path.basename(__file__)}`. "
           "No editar a mano.", "",
           "## Percentiles por submuestra (EN 14358 §3.2.2 y §3.3)", "",
           C.tabla_md(
               ["Muestra", "n", "k_s(n)", "f_05 [N/mm2]", "ro_05 [kg/m3]", "E medio [N/mm2]"],
               [[f["muestra"], f["n"], C.num(f["ks_formula"], 4), C.num(f["f05"], 2),
                 C.num(f["ro05"], 1), f"{f['E_media']:.0f}"] for f in filas]),
           "",
           "## Chequeo de la distribucion adoptada para la resistencia", "",
           "EN 14358 §3.2.2 c) manda log-normal salvo que el analisis demuestre que la "
           "normal es mas adecuada. D de Kolmogorov-Smirnov, menor es mejor ajuste:", "",
           C.tabla_md(
               ["Muestra", "D log-normal", "D normal", "Mejor ajuste",
                "f_05 log-normal", "f_05 normal"],
               [[f["muestra"], C.num(f["D_lognormal"], 4), C.num(f["D_normal"], 4),
                 "log-normal" if f["D_lognormal"] <= f["D_normal"] else "normal",
                 C.num(f["f05"], 2), C.num(f["f05_normal"], 2)] for f in filas]),
           "",
           "## Combinacion de las submuestras (EN 384 §5.5.2.2)", "",
           f"`ns = {ns}` submuestras, `n = {sum(n_i)}` probetas. De la Tabla 1: "
           f"`k_n = {k_n(ns,'resistencia'):.2f}` para resistencias paralelas a la fibra y "
           f"`k_n = {k_n(ns,'rigidez'):.2f}` para modulo y densidad.", "",
           C.tabla_md(
               ["Magnitud", "Media ponderada", "Tope sobre la peor", "Gobierna",
                "k_n", "Valor caracteristico"],
               [["f_m,k [N/mm2]", C.num(fk["ponderada"], 2), C.num(fk["acotado"], 2),
                 fk["gobierna"], C.num(k_n(ns, "resistencia"), 2), C.num(fk["valor"], 2)],
                ["E_0,mean [N/mm2]", f"{ek['ponderada']:.0f}", f"{ek['acotado']:.0f}",
                 ek["gobierna"], C.num(k_n(ns, "rigidez"), 2), f"{ek['valor']:.0f}"],
                ["rho_k [kg/m3]", C.num(rk["ponderada"], 1), C.num(rk["acotado"], 1),
                 rk["gobierna"], C.num(k_n(ns, "rigidez"), 2), C.num(rk["valor"], 1)]]),
           "",
           f"El modulo lleva ademas el divisor {DIVISOR_MODULO} de la formula (12).", "",
           "## Sensibilidad al k_s(n) adoptado", "",
           "El calculo usa la formula (10). La Tabla 1 no tabula n = 89/90/79, y su regla es "
           "tomar el valor de k_s inmediatamente mayor, que para los tres es el de la entrada "
           "n = 50, o sea 1,81. Rehaciendo la cadena entera con ese valor:", "",
           C.tabla_md(
               ["Magnitud", "Con formula (10)", "Con Tabla 1 (k_s = 1,81)", "Diferencia"],
               [["f_m,k [N/mm2]", C.num(fk["valor"], 2), C.num(fk_t["valor"], 2),
                 C.num(100 * (fk_t["valor"] / fk["valor"] - 1), 2) + " %"],
                ["rho_k [kg/m3]", C.num(rk["valor"], 1), C.num(rk_t["valor"], 1),
                 C.num(100 * (rk_t["valor"] / rk["valor"] - 1), 2) + " %"]]),
           "",
           "El modulo no aparece porque su valor caracteristico es la media de la muestra "
           "(§3.3 d) y no depende de k_s.", ""]
    ruta = os.path.join(C.RESULTADOS, "04_resumen_etapa3.md")
    with open(ruta, "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    print(f"\nOK  {ruta}")


if __name__ == "__main__":
    main()
