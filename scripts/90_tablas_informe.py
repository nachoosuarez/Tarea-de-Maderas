# -*- coding: utf-8 -*-
"""Vuelca los resultados de los scripts al archivo madre INFORME.tex.

El .tex tiene bloques delimitados asi:

    % <<<AUTO:nombre>>>
    ... contenido generado ...
    % <<<END:nombre>>>

Este script reemplaza el interior de cada bloque y deja intacto todo lo demas, de modo
que la redaccion a mano y las tablas automaticas conviven en el mismo archivo. Correrlo
cada vez que cambie un resultado: es lo que hace cumplible la politica del repo de
actualizar el informe en el mismo commit que el calculo.

Uso:  python scripts/90_tablas_informe.py
"""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comun as C

TEX = os.path.join(C.RAIZ, "INFORME.tex")


# --------------------------------------------------------------------------- util
def n(v, d=2):
    return C.num(v, d)


def sustituir(texto, nombre, contenido):
    ini = f"% <<<AUTO:{nombre}>>>"
    fin = f"% <<<END:{nombre}>>>"
    patron = re.compile(re.escape(ini) + r".*?" + re.escape(fin), re.DOTALL)
    if not patron.search(texto):
        raise SystemExit(f"ERROR: no se encontro el bloque {nombre} en INFORME.tex")
    nuevo = ini + "\n" + contenido.rstrip() + "\n" + fin
    # lambda y no el string directo: re.sub interpreta los backslash del reemplazo
    # y el contenido esta lleno de comandos LaTeX
    return patron.sub(lambda _: nuevo, texto)


def tabla(caption, colspec, cabecera, filas, ancla="H"):
    out = [r"\begin{table}[" + ancla + "]", r"\centering",
           r"\caption{" + caption + "}",
           r"\begin{tabular}{" + colspec + "}", r"\toprule"]
    out += cabecera
    out.append(r"\midrule")
    for f in filas:
        out.append(" & ".join(f) + r" \\")
    out += [r"\bottomrule", r"\end{tabular}", r"\end{table}"]
    return "\n".join(out)


def longtable(caption, etiqueta, colspec, cabecera, filas):
    cab = "\n".join(cabecera)
    out = [r"{\footnotesize",
           r"\begin{longtable}{" + colspec + "}",
           r"\caption{" + caption + r"}\label{" + etiqueta + r"}\\",
           r"\toprule", cab, r"\midrule", r"\endfirsthead",
           r"\multicolumn{" + str(colspec.count("r") + colspec.count("c") + colspec.count("l")) +
           r"}{l}{\footnotesize\itshape " + caption + r" (continuación)}\\",
           r"\toprule", cab, r"\midrule", r"\endhead",
           r"\midrule \multicolumn{" + str(colspec.count("r") + colspec.count("c") + colspec.count("l")) +
           r"}{r}{\footnotesize\itshape continúa en la página siguiente}\\",
           r"\endfoot", r"\bottomrule", r"\endlastfoot"]
    for f in filas:
        out.append(" & ".join(f) + r" \\")
    out += [r"\end{longtable}", r"}"]
    return "\n".join(out)


def descriptiva(grupos, todas, clave, dec):
    """Filas de una tabla n / media / s / CoV / min / max."""
    filas = []
    for m, g in grupos.items():
        r = C.resumen([x[clave] for x in g])
        filas.append([str(m), str(r["n"]), n(r["media"], dec), n(r["s"], dec),
                      n(r["CoV"] * 100, 1), n(r["min"], dec), n(r["max"], dec)])
    r = C.resumen([x[clave] for x in todas])
    filas.append([r"\textbf{Lote}", str(r["n"]), n(r["media"], dec), n(r["s"], dec),
                  n(r["CoV"] * 100, 1), n(r["min"], dec), n(r["max"], dec)])
    return filas


# --------------------------------------------------------------------------- main
def main():
    piezas = C.leer_csv("03_valores_corregidos.csv")
    grupos = C.por_muestra(piezas)

    with open(TEX, encoding="utf-8") as f:
        tex = f.read()

    # --- Bloque: factores geometricos ---------------------------------------
    filas = []
    for m, g in grupos.items():
        h = C.resumen([x["h"] for x in g])
        kh = C.resumen([x["kh"] for x in g])
        kl = C.resumen([x["kl"] for x in g])
        le = C.resumen([x["let"] for x in g])
        filas.append([
            str(m), str(len(g)), n(h["media"], 2), n(g[0]["af"], 1),
            n(48 * h["media"], 0), n(le["media"], 0),
            n(kh["min"], 4) + "--" + n(kh["max"], 4),
            n(kl["min"], 4) + "--" + n(kl["max"], 4),
        ])
    cab = [r"\textbf{Muestra} & \textbf{$n$} & \textbf{$h$ medio} & \textbf{$a_{f}$} & "
           r"\textbf{$48h$} & \textbf{$\lonet$} & \textbf{$k_{h}$} & \textbf{$k_{\ell}$} \\",
           r" & & [mm] & [mm] & [mm] & [mm] & [--] & [--] \\"]
    tex = sustituir(tex, "factores", tabla(
        "Factores de corrección geométrica por submuestra (UNE-EN 384:2016, "
        r"\S5.4.3). Los rangos de $k_{h}$ y $k_{\ell}$ recogen la variación "
        "pieza a pieza dentro de cada submuestra",
        "c c r r r r c c", cab, filas))

    # --- Bloque: efecto de la correccion ------------------------------------
    filas = []
    for m, g in grupos.items():
        df = 100 * (C.resumen([x["fm_ref"] for x in g])["media"] /
                    C.resumen([x["fm"] for x in g])["media"] - 1)
        dE = 100 * (C.resumen([x["E0"] for x in g])["media"] /
                    C.resumen([x["Eml"] for x in g])["media"] - 1)
        dr = 100 * (C.resumen([x["ro_ref"] for x in g])["media"] /
                    C.resumen([x["ro"] for x in g])["media"] - 1)
        filas.append([str(m)] + [r"\num{" + n(v, 2) + "}" for v in (df, dE, dr)])
    cab = [r"\textbf{Muestra} & \textbf{$\fm$} & \textbf{$\Ecero$} & \textbf{$\rho$} \\",
           r" & [\%] & [\%] & [\%] \\"]
    tex = sustituir(tex, "correccion", tabla(
        "Variación del valor medio de cada submuestra por efecto de las correcciones",
        "c r r r", cab, filas))

    # --- Bloque: valores corregidos por submuestra --------------------------
    bloques = []
    for clave, dec, titulo, unidad in (
        ("fm_ref", 2, r"Resistencia a flexión corregida $\fm$",
         r"\si{\newton\per\square\milli\meter}"),
        ("E0", 0, r"Módulo de elasticidad $\Ecero$",
         r"\si{\newton\per\square\milli\meter}"),
        ("ro_ref", 1, r"Densidad corregida $\rho$",
         r"\si{\kilo\gram\per\cubic\meter}"),
    ):
        cab = [r"\textbf{Muestra} & \textbf{$n$} & \textbf{media} & \textbf{$s$} & "
               r"\textbf{CoV} & \textbf{mín.} & \textbf{máx.} \\",
               r" & & \multicolumn{2}{c}{[" + unidad + r"]} & [\si{\percent}] & "
               r"\multicolumn{2}{c}{[" + unidad + r"]} \\"]
        bloques.append(tabla(titulo + " tras la corrección a condiciones de referencia",
                             "c c r r r r r", cab,
                             descriptiva(grupos, piezas, clave, dec)))
    tex = sustituir(tex, "corregidos", "\n\n".join(bloques))

    # --- Bloque: Anexo C, misma descriptiva ---------------------------------
    tex = sustituir(tex, "anexoC", "\n\n".join(bloques))

    # --- Bloque: Anexo B.1 ---------------------------------------------------
    cab = [r"\textbf{Viga} & \textbf{M} & \textbf{$b$} & \textbf{$h$} & \textbf{$CH$} & "
           r"\textbf{$\rho$} & \textbf{$P_{max}$} & \textbf{$P/f$} & \textbf{$\fm$} & "
           r"\textbf{$\Eml$} \\",
           r" & & \multicolumn{2}{c}{[mm]} & [\%] & [kg/m$^{3}$] & [N] & [N/mm] & "
           r"\multicolumn{2}{c}{[N/mm$^{2}$]} \\"]
    filas = [[str(p["viga"]), str(p["muestra"]), n(p["b"], 1), n(p["h"], 1),
              n(p["CH"], 1), n(p["ro"], 2), f'{int(round(p["Pmax"]))}',
              f'{int(round(p["Pf"]))}', n(p["fm"], 2), f'{p["Eml"]:.0f}']
             for p in piezas]
    tex = sustituir(tex, "anexoB1", longtable(
        "Datos de partida y propiedades sin corregir (UNE-EN 408:2010)",
        "tab:anexoB1", "r c r r r r r r r r", cab, filas))

    # --- Bloque: Anexo B.2 ---------------------------------------------------
    cab = [r"\textbf{Viga} & \textbf{M} & \textbf{$a_{f}$} & \textbf{$\lonet$} & "
           r"\textbf{$k_{h}$} & \textbf{$k_{\ell}$} & \textbf{$\fm$} & "
           r"\textbf{$\Ecero$} & \textbf{$\rho$} \\",
           r" & & \multicolumn{2}{c}{[mm]} & \multicolumn{2}{c}{[--]} & "
           r"\multicolumn{2}{c}{[N/mm$^{2}$]} & [kg/m$^{3}$] \\"]
    filas = [[str(p["viga"]), str(p["muestra"]), n(p["af"], 1), n(p["let"], 1),
              n(p["kh"], 4), n(p["kl"], 4), n(p["fm_ref"], 2),
              f'{p["E0"]:.0f}', n(p["ro_ref"], 1)]
             for p in piezas]
    tex = sustituir(tex, "anexoB2", longtable(
        "Factores de corrección y valores en condiciones de referencia "
        r"(UNE-EN 384:2016, \S5.4)",
        "tab:anexoB2", "r c r r r r r r r", cab, filas))

    # =========================================================================
    # Etapa 3. Los produce 04_valores_caracteristicos.py
    # =========================================================================
    sub = C.leer_csv("04_por_submuestra.csv")
    lote = C.leer_csv("04_valores_lote.csv")

    # --- Bloque: valores por submuestra (5.1) --------------------------------
    cab = [r"\textbf{Muestra} & \textbf{$n$} & \textbf{$f_{05,i}$} & "
           r"\textbf{$\bar{E}_{i}$} & \textbf{$\rho_{05,i}$} & \textbf{$k_{s}(n)$} \\",
           r" & & [\si{\newton\per\square\milli\meter}] & "
           r"[\si{\newton\per\square\milli\meter}] & "
           r"[\si{\kilo\gram\per\cubic\meter}] & [--] \\"]
    filas = [[str(int(s["muestra"])), str(int(s["n"])), n(s["f05"], 2),
              f'{s["E_media"]:.0f}', n(s["ro05"], 1), n(s["ks_formula"], 4)]
             for s in sub]
    tex = sustituir(tex, "submuestras", tabla(
        "Valores estadísticos por submuestra (UNE-EN 14358:2016). "
        r"$f_{05}$ por ajuste log-normal, $\rho_{05}$ por ajuste normal y $\bar{E}$ "
        r"como media aritmética (\S3.3 d)",
        "c c r r r r", cab, filas))

    # --- Bloque: valores caracteristicos del lote (5.2) ----------------------
    DEC = {"fmk": 2, "E0mean": 0, "rok": 1}
    SIM = {"fmk": r"$f_{m,k}$", "E0mean": r"$E_{0,mean}$", "rok": r"$\rho_{k}$"}
    UNI = {"fmk": r"\si{\newton\per\square\milli\meter}",
           "E0mean": r"\si{\newton\per\square\milli\meter}",
           "rok": r"\si{\kilo\gram\per\cubic\meter}"}
    cab = [r"\textbf{Magnitud} & \textbf{Unidad} & \textbf{Media pond.} & "
           r"\textbf{Tope} & \textbf{$k_{n}$} & \textbf{Valor} & \textbf{Gobierna} \\"]
    filas = []
    for r in lote:
        s = r["simbolo"]
        d = DEC[s]
        filas.append([SIM[s], "[" + UNI[s] + "]", n(r["ponderada"], d),
                      n(r["acotado"], d), n(r["kn"], 2), r"\textbf{" + n(r["valor"], d) + "}",
                      r["gobierna"]])
    tex = sustituir(tex, "caracteristicos", tabla(
        "Valores característicos del lote (UNE-EN 384:2016, expresiones (11), (12) "
        r"y (13)). El término «tope» es $1{,}2\,f_{05,\min}$ para la resistencia y "
        r"$1{,}1\,X_{\min}$ para módulo y densidad; el módulo lleva además el "
        r"divisor $0{,}95$ de la expresión (12)",
        "l c r r c r l", cab, filas))

    # --- Bloque: Anexo C.2, parametros del ajuste ---------------------------
    cab = [r"\textbf{Muestra} & \textbf{$n$} & \textbf{$\bar{y}$} & \textbf{$s_{y}$} & "
           r"\textbf{piso} & \textbf{$k_{s}$ (14358-10)} & \textbf{$k_{s}$ Tabla 1} & "
           r"\textbf{$m_{k}$} \\"]
    fila_r = [[str(int(s["muestra"])), str(int(s["n"])), n(s["fm_y"], 4), n(s["fm_sy"], 4),
               s["fm_piso"], n(s["ks_formula"], 4), n(s["ks_tabla"], 2), n(s["f05"], 2)]
              for s in sub]
    fila_d = [[str(int(s["muestra"])), str(int(s["n"])), n(s["ro_y"], 1), n(s["ro_sy"], 1),
               s["ro_piso"], n(s["ks_formula"], 4), n(s["ks_tabla"], 2), n(s["ro05"], 1)]
              for s in sub]
    t1 = tabla(r"Resistencia a flexión: parámetros del ajuste log-normal. $\bar{y}$ y "
               r"$s_{y}$ en logaritmos naturales; $m_{k} = f_{05}$ en "
               r"\si{\newton\per\square\milli\meter}",
               "c c r r c r r r", cab, fila_r)
    t2 = tabla(r"Densidad: parámetros del ajuste normal. $\bar{y}$, $s_{y}$ y "
               r"$m_{k} = \rho_{05}$ en \si{\kilo\gram\per\cubic\meter}",
               "c c r r c r r r", cab, fila_d)

    cab = [r"\textbf{Muestra} & \textbf{$D$ log-normal} & \textbf{$D$ normal} & "
           r"\textbf{Mejor ajuste} & \textbf{$f_{05}$ log-normal} & "
           r"\textbf{$f_{05}$ normal} \\",
           r" & \multicolumn{2}{c}{[--]} & & "
           r"\multicolumn{2}{c}{[\si{\newton\per\square\milli\meter}]} \\"]
    filas = [[str(int(s["muestra"])), n(s["D_lognormal"], 4), n(s["D_normal"], 4),
              "log-normal" if s["D_lognormal"] <= s["D_normal"] else "normal",
              n(s["f05"], 2), n(s["f05_normal"], 2)] for s in sub]
    t3 = tabla("Contraste de la distribución adoptada para la resistencia. Estadístico "
               "$D$ de Kolmogorov-Smirnov frente a la distribución ajustada; "
               "un valor menor indica mejor ajuste",
               "c r r c r r", cab, filas)

    cab = [r"\textbf{Magnitud} & \textbf{Con (14358-10)} & "
           r"\textbf{Con Tabla 1 ($k_{s} = 1{,}81$)} & \textbf{Diferencia} \\"]
    filas = []
    for r in lote:
        if r["simbolo"] == "E0mean":
            continue          # la media de submuestra no depende de k_s
        d = DEC[r["simbolo"]]
        filas.append([SIM[r["simbolo"]], n(r["valor"], d), n(r["valor_ks_tabla"], d),
                      n(100 * (r["valor_ks_tabla"] / r["valor"] - 1), 2) + r" \%"])
    t4 = tabla("Sensibilidad de los valores característicos al $k_{s}(n)$ adoptado. "
               "El módulo no figura por caracterizarse mediante la media de submuestra, "
               "que no depende de $k_{s}$",
               "l r r r", cab, filas)
    tex = sustituir(tex, "anexoC2", "\n\n".join([t1, t2, t3, t4]))

    with open(TEX, "w", encoding="utf-8") as f:
        f.write(tex)

    print(f"OK  INFORME.tex actualizado ({len(piezas)} piezas en los anexos)")
    for b in ("factores", "correccion", "corregidos", "anexoC", "anexoB1", "anexoB2",
              "submuestras", "caracteristicos", "anexoC2"):
        print(f"    bloque {b}")


if __name__ == "__main__":
    main()
