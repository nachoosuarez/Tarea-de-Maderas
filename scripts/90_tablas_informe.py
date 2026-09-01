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

    with open(TEX, "w", encoding="utf-8") as f:
        f.write(tex)

    print(f"OK  INFORME.tex actualizado ({len(piezas)} piezas en los anexos)")
    for b in ("factores", "correccion", "corregidos", "anexoC", "anexoB1", "anexoB2"):
        print(f"    bloque {b}")


if __name__ == "__main__":
    main()
