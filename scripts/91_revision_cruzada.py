# -*- coding: utf-8 -*-
"""Revision cruzada del INFORME.tex. Etapa 5 (semanas 6-8).

Que hace
--------
El 90 escribe las tablas automaticas y nadie las tipea. Pero la redaccion a mano
que vive fuera de los bloques % <<<AUTO:...>>> si tiene numeros escritos a mano:
los rangos de la tabla del lote, las relaciones l/h, el 8,6 % de la muestra 1, el
k_h medio, los valores sin corregir del anexo A. Este script los vuelve a calcular
de los datos y los coteja uno por uno.

Como coteja
-----------
Cada afirmacion lleva:
  - la cadena literal tal como esta escrita en el INFORME.tex, que tiene que
    seguir apareciendo en el archivo (si alguien edita el texto, el chequeo falla
    en vez de quedar comparando contra un numero que ya no esta);
  - el valor recalculado desde los datos o desde el CSV que corresponda.
La comparacion es sobre el numero ya formateado con los mismos decimales con que
esta impreso, no sobre el float: se verifica lo que el lector va a leer.

Ninguna formula normativa se reescribe aca. Las que hacen falta se importan de
los scripts 03 y 04, que son su unico lugar.

Ademas hace tres controles estructurales:
  - que ningun \\ref apunte a una etiqueta inexistente;
  - que no quede ningun \\verificar en el documento;
  - que los bloques automaticos esten sincronizados con los CSV.

Uso:  python scripts/91_revision_cruzada.py
Sale con codigo 1 si algo no cuadra.
"""

import importlib.util
import os
import re
import statistics as st
import sys

DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, DIR)
import comun as C

TEX = os.path.join(C.RAIZ, "INFORME.tex")


def _importar(archivo):
    """Importa un script cuyo nombre arranca con digito (no es identificador)."""
    ruta = os.path.join(DIR, archivo)
    spec = importlib.util.spec_from_file_location(archivo[:-3].replace("-", "_"), ruta)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ---------------------------------------------------------------- cotejo
class Cotejo:
    def __init__(self, tex):
        self.tex = tex
        self.filas = []

    def num(self, donde, que, cadena, calculado):
        """Coteja un numero. 'cadena' es el literal que esta en el .tex y de el
        se deduce con cuantos decimales esta impreso."""
        # La cadena viene envuelta en LaTeX (\num{...}, \SI{...}{...}, 6{,}00):
        # primero se extrae el literal numerico y de el salen los decimales.
        plano = cadena.replace("{,}", ",")
        hallado = re.search(r"-?\d+(?:[.,]\d+)?", plano)
        if not hallado:
            raise SystemExit(f"ERROR: no hay numero en la cadena {cadena!r}")
        crudo = hallado.group(0).replace(",", ".")
        dec = len(crudo.split(".")[1]) if "." in crudo else 0
        impreso = f"{calculado:.{dec}f}"
        coincide = impreso == crudo
        presente = cadena in self.tex
        self.filas.append({
            "donde": donde, "que": que,
            "informe": crudo.replace(".", ","),
            "recalculado": impreso.replace(".", ","),
            "estado": "OK" if (coincide and presente) else
                      ("NO ESTA EN EL .TEX" if not presente else "DIFIERE"),
        })

    def texto(self, donde, que, condicion, detalle=""):
        self.filas.append({
            "donde": donde, "que": que, "informe": detalle or "--",
            "recalculado": "--", "estado": "OK" if condicion else "DIFIERE",
        })

    @property
    def fallas(self):
        return [f for f in self.filas if f["estado"] != "OK"]


def main():
    with open(TEX, encoding="utf-8") as f:
        tex = f.read()

    m02 = _importar("02_propiedades_por_pieza.py")
    m03 = _importar("03_correcciones_en384.py")
    m04 = _importar("04_valores_caracteristicos.py")

    piezas = C.cargar_datos()
    grupos = C.por_muestra(piezas)
    corr = C.leer_csv("03_valores_corregidos.csv")
    corr_g = {m: [x for x in corr if x["muestra"] == m] for m in (1, 2, 3)}
    lote = {x["simbolo"]: x for x in C.leer_csv("04_valores_lote.csv")}
    asig = C.leer_csv("05_clase_asignada.csv")[0]

    k = Cotejo(tex)

    # --- 2.2 Composicion del lote ------------------------------------------
    k.num("2.2 tabla lote", "total de piezas", r"\num{258}", float(len(piezas)))
    esperado_lote = {
        1: ("89", "35.93", "93.94", "91,2", "96,0", "603.7", "1771.4"),
        2: ("90", "44.92", "142.10", "139,7", "145,2", "931.3", "2714.6"),
        3: ("79", "57.00", "189.83", "186,1", "193,1", "1217.1", "3574.1"),
    }
    for m, (n_, bm, hm, hmin, hmax, a_, l_) in esperado_lote.items():
        g = grupos[m]
        k.num(f"2.2 tabla lote, m{m}", "n", n_, float(len(g)))
        k.num(f"2.2 tabla lote, m{m}", "b medio", bm, st.fmean(x["b"] for x in g))
        k.num(f"2.2 tabla lote, m{m}", "h medio", hm, st.fmean(x["h"] for x in g))
        k.num(f"2.2 tabla lote, m{m}", "h minimo", hmin, min(x["h"] for x in g))
        k.num(f"2.2 tabla lote, m{m}", "h maximo", hmax, max(x["h"] for x in g))
        k.num(f"2.2 tabla lote, m{m}", "a", a_, st.fmean(x["a"] for x in g))
        k.num(f"2.2 tabla lote, m{m}", "luz l", l_, st.fmean(x["l"] for x in g))
        k.texto(f"2.2 tabla lote, m{m}", "a y l constantes dentro de la muestra",
                len({x["a"] for x in g}) == 1 and len({x["l"] for x in g}) == 1)

    # --- 2.3 Verificacion previa y anexo A ----------------------------------
    esperado_rangos = {
        1: ("18,86", "6,43", "10,2", "13,6", "11,97", "389", "519",
            "3299", "10740", "208", "457"),
        2: ("19,10", "6,55", "10,7", "13,9", "12,07", "370", "489",
            "8710", "19673", "284", "491"),
        3: ("18,83", "6,41", "9,8", "13,5", "11,96", "379", "523",
            "12773", "46155", "360", "699"),
    }
    for m, v in esperado_rangos.items():
        g = grupos[m]
        lh, ah, chmin, chmax, chmed, romin, romax, pmin, pmax, pfmin, pfmax = v
        # l y a son constantes en la muestra: la relacion se da sobre el canto
        # medio, no como media de las relaciones pieza a pieza (difieren en la
        # segunda decimal).
        k.num(f"anexo A, m{m}", "relacion l/h sobre el canto medio", lh,
              st.fmean(x["l"] for x in g) / st.fmean(x["h"] for x in g))
        k.num(f"anexo A, m{m}", "relacion a/h sobre el canto medio", ah,
              st.fmean(x["a"] for x in g) / st.fmean(x["h"] for x in g))
        k.num(f"2.3 tabla rangos, m{m}", "CH minimo", chmin, min(x["CH"] for x in g))
        k.num(f"2.3 tabla rangos, m{m}", "CH maximo", chmax, max(x["CH"] for x in g))
        k.num(f"2.3 tabla rangos, m{m}", "CH medio", chmed, st.fmean(x["CH"] for x in g))
        k.num(f"2.3 tabla rangos, m{m}", "densidad minima", romin, min(x["ro"] for x in g))
        k.num(f"2.3 tabla rangos, m{m}", "densidad maxima", romax, max(x["ro"] for x in g))
        k.num(f"2.3 tabla rangos, m{m}", "Pmax minima", pmin, min(x["Pmax"] for x in g))
        k.num(f"2.3 tabla rangos, m{m}", "Pmax maxima", pmax, max(x["Pmax"] for x in g))
        k.num(f"2.3 tabla rangos, m{m}", "P/f minima", pfmin, min(x["Pf"] for x in g))
        k.num(f"2.3 tabla rangos, m{m}", "P/f maxima", pfmax, max(x["Pf"] for x in g))

    k.num("2.3 texto", "humedad minima del lote", r"\SI{9,8}{\percent}",
          min(x["CH"] for x in piezas))
    k.num("2.3 texto", "humedad maxima del lote", r"\SI{13,9}{\percent}",
          max(x["CH"] for x in piezas))
    k.texto("2.3 texto", "ninguna pieza supera u = 18 %",
            max(x["CH"] for x in piezas) <= 18.0)
    k.texto("2.3 texto", "no hay vigas duplicadas",
            len({x["viga"] for x in piezas}) == len(piezas))

    # --- 4.2 Interpretacion de a_f -----------------------------------------
    for m, (af_, rel_) in {1: (r"\num{564,0}", "6{,}00"),
                           2: (r"\num{852,0}", "6{,}00"),
                           3: (r"\SI{1139,9}{\milli\meter}", "6{,}01")}.items():
        g = grupos[m]
        k.num(f"4.2 texto, m{m}", "separacion entre cargas a_f = l - 2a", af_,
              st.fmean(m03.a_f(x) for x in g))
        k.num(f"4.2 texto, m{m}", "a_f en cantos (a_f/h)", rel_,
              st.fmean(m03.a_f(x) / x["h"] for x in g))

    # --- 4.2 Factores y efecto de las correcciones --------------------------
    k.num("4.2 texto", "k_h medio de la muestra 1", r"\num{1,098}",
          st.fmean(x["kh"] for x in corr_g[1]))
    k.texto("4.2 texto", "k_h = 1 en toda la muestra 3 (canto > 150 mm)",
            all(x["kh"] == 1.0 for x in corr_g[3]))
    k.texto("4.2 texto", "k_l distinto de 1 en las tres muestras",
            all(any(x["kl"] != 1.0 for x in corr_g[m]) for m in (1, 2, 3)))
    k.num("4.2 texto", "caida de f_m en la muestra 1", r"\SI{8,6}{\percent}",
          abs(st.fmean(x["fm_ref"] for x in corr_g[1]) /
              st.fmean(x["fm"] for x in corr_g[1]) - 1) * 100)
    k.num("4.2 texto", "efecto neto en la muestra 2", r"\SI{-0,6}{\percent}",
          (st.fmean(x["fm_ref"] for x in corr_g[2]) /
           st.fmean(x["fm"] for x in corr_g[2]) - 1) * 100)
    k.num("4.2 texto", "correccion de humedad maxima sobre el modulo",
          r"\SI{2,2}{\percent}",
          max(abs(x["CH"] - m03.U_REF) for x in piezas))
    k.num("4.2 texto", "efecto del divisor 1,05 sobre la densidad",
          r"\SI{4,8}{\percent}",
          (asig["rok"] - asig["rok_con_105"]) / asig["rok"] * 100)

    # --- Anexo A, valores sin corregir --------------------------------------
    esperado_bruto = {
        1: ("18,5", "64,0", "37,0", "8549", "19721", "13709"),
        2: ("26,3", "60,6", "39,1", "10212", "17286", "13379"),
        3: ("23,4", "84,2", "39,7", "9773", "19202", "13844"),
    }
    # Se recalculan de los datos crudos con las funciones del 02 y no del CSV:
    # el CSV guarda 6 cifras significativas y en los maximos de E eso ya mueve
    # el ultimo digito impreso.
    for m, (fmin, fmax, fmed, emin, emax, emed) in esperado_bruto.items():
        g = grupos[m]
        fs = [m02.resistencia_flexion(x) for x in g]
        es = [m02.modulo_local(x) for x in g]
        k.num(f"anexo A, m{m}", "f_m sin corregir, minima", fmin, min(fs))
        k.num(f"anexo A, m{m}", "f_m sin corregir, maxima", fmax, max(fs))
        k.num(f"anexo A, m{m}", "f_m sin corregir, media", fmed, st.fmean(fs))
        k.num(f"anexo A, m{m}", "E_m,l sin corregir, minimo", emin, min(es))
        k.num(f"anexo A, m{m}", "E_m,l sin corregir, maximo", emax, max(es))
        k.num(f"anexo A, m{m}", "E_m,l sin corregir, medio", emed, st.fmean(es))

    # Tabla del contraste con la resolucion iterativa (anexo A). No son piezas
    # del lote: son la geometria representativa de cada muestra con una pendiente
    # redonda, tal como las define 01_verif_despeje_modulo_local.py. Al calcular
    # aca la columna «cerrada» con la funcion del 02 se contrastan ademas dos
    # implementaciones independientes de la misma formula.
    casos = [(1, dict(b=36.0, h=93.4, a=603.7, l=1771.4, Pf=260.0), "11091.4"),
             (2, dict(b=44.9, h=142.1, a=931.3, l=2714.6, Pf=400.0), "14033.3"),
             (3, dict(b=57.0, h=189.8, a=1217.1, l=3574.1, Pf=500.0), "13186.8")]
    for m, caso, cadena in casos:
        k.num(f"anexo A, m{m}", "forma cerrada del contraste iterativo",
              cadena, m02.modulo_local(caso))

    # --- 4.3 Factor k_s ------------------------------------------------------
    k.num("4.3 texto", "k_s(20) por la expresion (10)", r"\num{1,915}", m04.k_s(20))
    k.num("4.3 texto", "k_s(100) por la expresion (10)", r"\num{1,787}", m04.k_s(100))
    k.num("4.3 texto", "k_s(20) de la Tabla 1", r"\num{1,93}", m04.k_s_tabla(20))
    k.num("4.3 texto", "k_s(100) de la Tabla 1", r"\num{1,76}", m04.k_s_tabla(100))
    k.texto("4.3 texto", "la Tabla 1 lleva n = 79, 89 y 90 a la entrada n = 50",
            all(m04.k_s_tabla(n_) == 1.81 for n_ in (79, 89, 90)))
    peor_ks = max(abs(lote[s]["valor_ks_tabla"] / lote[s]["valor"] - 1) * 100
                  for s in ("fmk", "rok"))
    k.texto("4.3 texto", "la sensibilidad al k_s es inferior al 0,4 %",
            peor_ks < 0.4, f"maxima: {C.num(peor_ks, 2)} %")

    # --- 5 Resultados: la prosa contra los CSV -------------------------------
    k.texto("5.2 texto", "en las tres magnitudes gobierna la media ponderada",
            all(lote[s]["gobierna"] == "media ponderada"
                for s in ("fmk", "E0mean", "rok")))
    k.texto("5.1 texto", "la submuestra 1 es la mas desfavorable en resistencia",
            min(C.leer_csv("04_por_submuestra.csv"),
                key=lambda x: x["f05"])["muestra"] == 1)
    k.texto("6.1 texto", "el criterio que gobierna la clase es f_m,k",
            str(asig["gobierna"]).strip() == "fmk", str(asig["gobierna"]))
    k.texto("6.1 texto", "el modulo cumple con mas margen que la resistencia",
            asig["E0mean_rel"] > asig["fmk_rel"])

    # --- Controles estructurales del .tex ------------------------------------
    etiquetas = set(re.findall(r"\\label\{([^}]+)\}", tex))
    referencias = set(re.findall(r"\\(?:eq)?ref\{([^}]+)\}", tex))
    huerfanas = sorted(referencias - etiquetas)
    k.texto("estructura", "toda referencia cruzada tiene su etiqueta",
            not huerfanas, ", ".join(huerfanas) if huerfanas else
            f"{len(referencias)} referencias contra {len(etiquetas)} etiquetas")

    n_verif = len(re.findall(r"\\verificar\{", tex)) - tex.count(r"\newcommand{\verificar}")
    k.texto("estructura", "no queda ningun \\verificar en el documento",
            n_verif == 0, f"{n_verif} marcas")

    n_pend = len(re.findall(r"\\pendiente\{", tex)) - tex.count(r"\newcommand{\pendiente}")
    k.texto("estructura", "marcas \\pendiente restantes (solo el autor)",
            n_pend <= 1, f"{n_pend} marca(s)")

    abiertos = re.findall(r"% <<<AUTO:([a-zA-Z0-9]+)>>>", tex)
    cerrados = re.findall(r"% <<<END:([a-zA-Z0-9]+)>>>", tex)
    k.texto("estructura", "los bloques automaticos abren y cierran",
            abiertos == cerrados, f"{len(abiertos)} bloques")

    # --- Sincronia del .tex con los CSV --------------------------------------
    bloques = dict(re.findall(r"% <<<AUTO:([a-zA-Z0-9]+)>>>(.*?)% <<<END:",
                              tex, re.DOTALL))
    clase = str(asig["clase"])
    for nombre in ("resumen", "clase", "conclusion"):
        k.texto("sincronia", f"el bloque «{nombre}» dice la clase del CSV",
                clase in bloques.get(nombre, ""), clase)
    for nombre, valor, dec in (("clase", asig["fmk"], 2),
                               ("conclusion", asig["fmk"], 2),
                               ("clase", asig["rok"], 1),
                               ("caracteristicos", lote["E0mean"]["valor"], 0)):
        k.texto("sincronia", f"el bloque «{nombre}» lleva {C.num(valor, dec)}",
                C.num(valor, dec) in bloques.get(nombre, ""), C.num(valor, dec))

    # ------------------------------------------------------------------ salida
    fallas = k.fallas
    print(f"Revision cruzada del INFORME.tex: {len(k.filas)} comprobaciones, "
          f"{len(fallas)} con diferencia.")
    for f in fallas:
        print(f"  [{f['estado']}] {f['donde']} - {f['que']}: "
              f"informe {f['informe']} / recalculado {f['recalculado']}")

    md = ["# Revisión cruzada del informe", "",
          "Salida de `scripts/91_revision_cruzada.py`. Cada fila vuelve a calcular "
          "desde los datos un número que en el `INFORME.tex` está **escrito a mano**, "
          "fuera de los bloques automáticos, y lo compara con los mismos decimales "
          "con que está impreso.", "",
          f"**{len(k.filas)} comprobaciones, {len(fallas)} con diferencia.**", "",
          C.tabla_md(["Dónde", "Qué se comprueba", "En el informe", "Recalculado", "Estado"],
                     [[f["donde"], f["que"], f["informe"], f["recalculado"], f["estado"]]
                      for f in k.filas]), "",
          "## Lo que este script no puede comprobar", "",
          "- Los valores de la tabla 1 de **UNE-EN 338:2010**: se transcribieron de la "
          "diapositiva S03E02 p.55 porque la norma no está en el zip de AENOR. Hay que "
          "contrastarlos a mano contra la fuente.",
          "- Los **coeficientes normativos** (`k_n`, el piso de CoV, los topes 1,2 y 1,1, "
          "el divisor 0,95): se cotejan contra su apartado en `06-referencias/README.md`, "
          "no contra los datos.",
          "- La **redacción**: que una frase diga lo que el número dice es cosa de leerla.",
          ]
    ruta = os.path.join(C.RESULTADOS, "91_revision_cruzada.md")
    with open(ruta, "w", encoding="utf-8") as f:
        f.write("\n".join(md) + "\n")
    print(f"OK  {ruta}")

    if fallas:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
