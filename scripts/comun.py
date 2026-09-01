# -*- coding: utf-8 -*-
"""Utilidades compartidas por los scripts del trabajo.

Unidades fijadas para todo el trabajo: N, mm, N/mm2 (= MPa), kg/m3, % de humedad.
Ninguna funcion de este archivo aplica correcciones normativas; solo lee, escribe y
resume. Las formulas viven en el script de la etapa que corresponde.
"""

import csv
import math
import os
import statistics as st

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATOS = os.path.join(RAIZ, "00-datos", "Datos_Picea.txt")
RESULTADOS = os.path.join(RAIZ, "resultados")

# Numero de columna en el .txt -> nombre interno
COLUMNAS = ["viga", "muestra", "b", "h", "a", "l", "CH", "ro", "Pmax", "Pf"]
ENTEROS = ("viga", "muestra")


def cargar_datos():
    """Devuelve la lista de las 258 piezas como diccionarios.

    El archivo viene tabulado, con dos filas de encabezado, decimal con punto y
    terminaciones de linea de Windows. Se lee con utf-8-sig porque trae BOM.
    """
    piezas = []
    with open(DATOS, encoding="utf-8-sig") as f:
        for n, linea in enumerate(f, start=1):
            if n <= 2:
                continue
            campos = linea.rstrip("\r\n").split("\t")
            if len(campos) < len(COLUMNAS) or not campos[0].strip():
                continue
            p = {}
            for nombre, bruto in zip(COLUMNAS, campos):
                v = bruto.strip()
                p[nombre] = int(v) if nombre in ENTEROS else float(v)
            piezas.append(p)
    return piezas


def por_muestra(piezas):
    """Agrupa las piezas por numero de muestra, en orden 1, 2, 3."""
    grupos = {}
    for p in piezas:
        grupos.setdefault(p["muestra"], []).append(p)
    return {k: grupos[k] for k in sorted(grupos)}


def resumen(valores):
    """Estadistica descriptiva de una lista. NO son valores caracteristicos:
    la media y la desviacion tipica de EN 14358 se calculan en la etapa 3."""
    n = len(valores)
    media = st.fmean(valores)
    s = st.stdev(valores) if n > 1 else 0.0
    return {
        "n": n,
        "media": media,
        "s": s,
        "CoV": s / media if media else float("nan"),
        "min": min(valores),
        "max": max(valores),
        "mediana": st.median(valores),
    }


def guardar_csv(nombre, campos, filas, cabecera_unidades=None):
    """Escribe un CSV en resultados/. Separador ';' y decimal ',' para que Excel
    en configuracion regional espanola lo abra sin pasos intermedios."""
    os.makedirs(RESULTADOS, exist_ok=True)
    ruta = os.path.join(RESULTADOS, nombre)
    with open(ruta, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(campos)
        if cabecera_unidades:
            w.writerow(cabecera_unidades)
        for fila in filas:
            w.writerow([_fmt(fila[c]) for c in campos])
    return ruta


def _fmt(v):
    if isinstance(v, float):
        return f"{v:.6g}".replace(".", ",")
    return v


def leer_csv(nombre):
    """Lee un CSV generado por guardar_csv (salta la fila de unidades)."""
    ruta = os.path.join(RESULTADOS, nombre)
    filas = []
    with open(ruta, encoding="utf-8-sig", newline="") as f:
        r = csv.reader(f, delimiter=";")
        campos = next(r)
        segunda = next(r)
        if not segunda[0].startswith("["):
            filas.append(_parsear(campos, segunda))
        for fila in r:
            if fila:
                filas.append(_parsear(campos, fila))
    return filas


def _parsear(campos, fila):
    p = {}
    for nombre, bruto in zip(campos, fila):
        v = bruto.strip().replace(",", ".")
        if nombre in ENTEROS:
            p[nombre] = int(v)
        else:
            try:
                p[nombre] = float(v)
            except ValueError:
                p[nombre] = bruto
    return p


def tabla_md(encabezados, filas):
    """Arma una tabla markdown ya alineada."""
    cols = [len(h) for h in encabezados]
    filas = [[str(c) for c in f] for f in filas]
    for f in filas:
        for i, c in enumerate(f):
            cols[i] = max(cols[i], len(c))
    out = ["| " + " | ".join(h.ljust(cols[i]) for i, h in enumerate(encabezados)) + " |"]
    out.append("|" + "|".join("-" * (c + 2) for c in cols) + "|")
    for f in filas:
        out.append("| " + " | ".join(c.ljust(cols[i]) for i, c in enumerate(f)) + " |")
    return "\n".join(out)


def num(v, d=2):
    """Numero con coma decimal, para volcar a markdown y a LaTeX."""
    return f"{v:.{d}f}".replace(".", ",")
