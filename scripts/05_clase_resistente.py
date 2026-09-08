# -*- coding: utf-8 -*-
"""Etapa 4: asignacion de la clase resistente (UNE-EN 338:2010).

La letra del trabajo lo fija de forma explicita: "corresponde asignar una clase
resistente de acuerdo con la UNE-EN 338:2010. Para ello basta con las diapositivas
del curso (S03E02)". La tabla de clases se transcribio de la Tabla 1 que reproduce
la diapositiva S03E02 p.55, renderizada a 420 dpi y leida columna por columna.

Picea es CONIFERA, asi que la clase se busca dentro de las clases C. Las clases D
estan en la tabla solo para poder correr el caso de autovalidacion (el castano de
la propia diapositiva), no para asignarle una D a nuestro lote.

Regla de asignacion: se asigna la clase mas alta cuyos TRES requisitos se cumplen
simultaneamente. Alcanza con que uno no llegue para bajar de clase.

Entrada : resultados/04_valores_lote.csv
Salida  : resultados/05_verificacion_clases.csv
          resultados/05_clase_asignada.csv
          resultados/05_resumen_etapa4.md

Uso:  python scripts/05_clase_resistente.py
"""

import importlib.util
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comun as C


def _etapa3():
    """Importa el script de la etapa 3 para reusar su funcion combinar().

    El nombre empieza con un digito, asi que no se puede importar con un import
    normal. Se hace asi y no copiando la funcion aca: las formulas (11)(12)(13)
    tienen que vivir en un unico lugar, si no una correccion futura se aplica en un
    archivo y no en el otro.
    """
    ruta = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "04_valores_caracteristicos.py")
    spec = importlib.util.spec_from_file_location("etapa3", ruta)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

# --------------------------------------------------------------------------- constantes
# UNE-EN 338:2010, Tabla 1 "Clases resistentes. Valores caracteristicos", reproducida
# en la diapositiva S03E02 p.55. Solo las tres filas que intervienen en la asignacion.
#
# UNIDADES DE LA TABLA, que NO son las del resto del trabajo:
#   f_m,k      en N/mm2   <- igual que nuestros calculos
#   E_0,medio  en kN/mm2  <- OJO: nuestro E_0,mean esta en N/mm2, hay que dividir por 1000
#   ro_k       en kg/m3   <- igual que nuestros calculos
#
#                  f_m,k   E_0,medio   ro_k
EN338_CONIFERAS = {
    "C14": (14.0,  7.0,  290.0),
    "C16": (16.0,  8.0,  310.0),
    "C18": (18.0,  9.0,  320.0),
    "C20": (20.0,  9.5,  330.0),
    "C22": (22.0, 10.0,  340.0),
    "C24": (24.0, 11.0,  350.0),
    "C27": (27.0, 11.5,  370.0),
    "C30": (30.0, 12.0,  380.0),
    "C35": (35.0, 13.0,  400.0),
    "C40": (40.0, 14.0,  420.0),
    "C45": (45.0, 15.0,  440.0),
    "C50": (50.0, 16.0,  460.0),
}

# Frondosas: solo para el caso de autovalidacion. Picea no se clasifica con estas.
EN338_FRONDOSAS = {
    "D18": (18.0,  9.5, 475.0),
    "D24": (24.0, 10.0, 485.0),
    "D30": (30.0, 11.0, 530.0),
    "D35": (35.0, 12.0, 540.0),
    "D40": (40.0, 13.0, 550.0),
    "D50": (50.0, 14.0, 620.0),
    "D60": (60.0, 17.0, 700.0),
    "D70": (70.0, 20.0, 900.0),
}

# EN 384:2016 §5.3.4. Divisor de la densidad si se midio sobre pieza completa en
# lugar de sobre una probeta libre de defectos. Decision todavia abierta: hay que
# preguntarle al docente. Se evalua como escenario, no se aplica al resultado.
DIVISOR_DENSIDAD_PIEZA_COMPLETA = 1.05

MAGNITUDES = ("f_m,k", "E_0,mean", "ro_k")

# Los CSV se leen con comun.leer_csv(), que hace replace(",", ".") sobre todos los
# campos para poder convertir el decimal local. Un simbolo con coma vuelve deformado
# ("f_m,k" -> "f_m.k"), asi que en los CSV los simbolos viajan sin coma.
SIMBOLO_CSV = {"f_m,k": "fmk", "E_0,mean": "E0mean", "ro_k": "rok"}


# --------------------------------------------------------------------------- verificacion
def verificar(clase, requisitos, fmk, e0mean_kn, rok):
    """Contrasta los tres criterios contra una clase. Devuelve el detalle completo.

    e0mean_kn tiene que venir YA en kN/mm2, que es la unidad de la tabla de EN 338.
    """
    req_f, req_e, req_ro = requisitos
    filas = [
        ("f_m,k",    fmk,       req_f,  "N/mm2"),
        ("E_0,mean", e0mean_kn, req_e,  "kN/mm2"),
        ("ro_k",     rok,       req_ro, "kg/m3"),
    ]
    detalle = []
    for simbolo, obtenido, requerido, unidad in filas:
        detalle.append({
            "magnitud": simbolo,
            "obtenido": obtenido,
            "requerido": requerido,
            # Relacion obtenido/requerido: >= 1 cumple. Es el inverso de la relacion
            # demanda-capacidad de un calculo estructural, porque aca lo que tenemos
            # es la capacidad y lo que la norma pide es el minimo.
            "relacion": obtenido / requerido,
            "cumple": obtenido >= requerido,
            "unidad": unidad,
        })
    return {
        "clase": clase,
        "detalle": detalle,
        "cumple": all(d["cumple"] for d in detalle),
        # Que criterios frenan esta clase (vacio si cumple)
        "frenan": [d["magnitud"] for d in detalle if not d["cumple"]],
    }


def asignar(tabla, fmk, e0mean_kn, rok):
    """Recorre la tabla en orden y devuelve la clase mas alta que cumple las tres.

    La tabla esta ordenada de menor a mayor exigencia, asi que la ultima que cumple
    es la mas alta. No se corta en el primer fallo: EN 338 no garantiza que los tres
    requisitos crezcan de forma estrictamente monotona en todas las filas, de modo
    que una clase superior podria cumplir aunque una inferior no. Recorrer entera
    cuesta doce iteraciones y elimina la duda.
    """
    verificaciones = [verificar(c, r, fmk, e0mean_kn, rok) for c, r in tabla.items()]
    cumplen = [v for v in verificaciones if v["cumple"]]
    asignada = cumplen[-1] if cumplen else None
    return verificaciones, asignada


def gobierna(verificaciones, asignada, tabla):
    """Cual de los tres criterios impide subir a la clase siguiente."""
    clases = list(tabla)
    if asignada is None:
        return None, None
    i = clases.index(asignada["clase"])
    if i + 1 >= len(clases):
        return None, None            # ya esta en la clase mas alta
    siguiente = verificaciones[i + 1]
    return siguiente, siguiente["frenan"]


# --------------------------------------------------------------------------- autovalidacion
def autovalidacion():
    """El metodo se contrasta contra el caso resuelto en la propia diapositiva.

    S03E02 p.55: castano de procedencia espanola, f_m,k = 28 N/mm2,
    E_0,medio = 12,3 kN/mm2, ro_k = 510 kg/m3 -> la diapositiva asigna D24.
    Es frondosa, por eso va contra la tabla D. Si este contraste falla, la tabla
    transcrita o la regla de asignacion estan mal y el resultado del lote no vale.
    """
    _, asignada = asignar(EN338_FRONDOSAS, 28.0, 12.3, 510.0)
    obtenida = asignada["clase"] if asignada else "ninguna"
    return obtenida, obtenida == "D24"


# --------------------------------------------------------------------------- robustez
def robustez(fmk, e0mean_kn, rok, clase_base, clase_105, rok_ajustada):
    """Cuanto aguanta la clase asignada si se cambian las decisiones de criterio.

    Sirve para saber si el resultado del trabajo depende de una eleccion discutible.
    Recombina las submuestras con la misma funcion de la etapa 3, no con una copia.
    """
    e3 = _etapa3()
    sub = C.leer_csv("04_por_submuestra.csv")
    n_i = [int(s["n"]) for s in sub]
    kn_r = e3.k_n(len(sub), "resistencia")

    def f_con(columna):
        return e3.combinar([s[columna] for s in sub], n_i,
                           e3.TOPE_RESISTENCIA, kn_r)["valor"]

    # La 'clave' es un identificador sin comas ni acentos: comun.leer_csv() hace
    # replace(",", ".") sobre todos los campos, asi que el texto bonito se arma en
    # 90_tablas_informe.py a partir de la clave y no del texto de esta columna.
    escenarios = [
        ("base", "base: log-normal y k_s por la formula (10)", f_con("f05"), rok),
        ("ks_tabla", "k_s de la Tabla 1 en vez de la formula (10)",
         f_con("f05_tabla"), rok),
        ("normal", "distribucion normal en vez de log-normal",
         f_con("f05_normal"), rok),
        ("densidad105", "densidad dividida por 1,05 (EN 384 5.3.4)", fmk, rok_ajustada),
    ]
    salida = []
    for clave, nombre, f, ro in escenarios:
        _, a = asignar(EN338_CONIFERAS, f, e0mean_kn, ro)
        salida.append({"clave": clave, "escenario": nombre, "fmk": f, "rok": ro,
                       "clase": a["clase"] if a else "ninguna"})
    return salida


# --------------------------------------------------------------------------- main
def main():
    lote = {f["simbolo"]: f for f in C.leer_csv("04_valores_lote.csv")}
    fmk = lote["fmk"]["valor"]
    e0mean = lote["E0mean"]["valor"]        # N/mm2
    rok = lote["rok"]["valor"]
    e0mean_kn = e0mean / 1000.0             # -> kN/mm2, unidad de la tabla EN 338

    obtenida, ok = autovalidacion()
    print("Autovalidacion (castano de S03E02 p.55, esperado D24):", obtenida,
          "OK" if ok else "FALLA")
    if not ok:
        raise SystemExit("La autovalidacion fallo: no se sigue. Revisar la tabla EN338.")

    print()
    print("Valores del lote (etapa 3):")
    print("  f_m,k    = %8.2f N/mm2" % fmk)
    print("  E_0,mean = %8.0f N/mm2  = %.3f kN/mm2" % (e0mean, e0mean_kn))
    print("  ro_k     = %8.1f kg/m3" % rok)
    print()

    verificaciones, asignada = asignar(EN338_CONIFERAS, fmk, e0mean_kn, rok)
    if asignada is None:
        raise SystemExit("El lote no alcanza ni la C14. Revisar las etapas anteriores.")

    siguiente, frenan = gobierna(verificaciones, asignada, EN338_CONIFERAS)

    print("CLASE ASIGNADA:", asignada["clase"])
    for d in asignada["detalle"]:
        print("   %-9s %10.2f >= %8.2f %-7s  margen %+6.1f %%"
              % (d["magnitud"], d["obtenido"], d["requerido"], d["unidad"],
                 (d["relacion"] - 1) * 100))
    if siguiente:
        print("La frena para subir a %s: %s" % (siguiente["clase"], ", ".join(frenan)))
        for d in siguiente["detalle"]:
            if not d["cumple"]:
                falta = d["requerido"] - d["obtenido"]
                print("   falta %.2f %s de %s (%.1f %% mas)"
                      % (falta, d["unidad"], d["magnitud"],
                         falta / d["obtenido"] * 100))

    # ---------------------------------------------------------------- escenario 1,05
    rok_ajustada = rok / DIVISOR_DENSIDAD_PIEZA_COMPLETA
    _, asignada_105 = asignar(EN338_CONIFERAS, fmk, e0mean_kn, rok_ajustada)
    clase_105 = asignada_105["clase"] if asignada_105 else "ninguna"
    print()
    print("Escenario EN 384 §5.3.4 (densidad medida sobre pieza completa):")
    print("  ro_k = %.1f / 1,05 = %.1f kg/m3  ->  clase %s  (%s)"
          % (rok, rok_ajustada, clase_105,
             "no cambia" if clase_105 == asignada["clase"] else "CAMBIA"))

    # ---------------------------------------------------------------- robustez
    escenarios = robustez(fmk, e0mean_kn, rok, asignada["clase"], clase_105,
                          rok_ajustada)
    print()
    print("Robustez de la clase frente a las decisiones de criterio:")
    for e in escenarios:
        print("   %-46s f_m,k = %6.2f  ->  %-4s  %s"
              % (e["escenario"], e["fmk"], e["clase"],
                 "igual" if e["clase"] == asignada["clase"] else "CAMBIA"))

    # ---------------------------------------------------------------- salidas
    # Los simbolos van al CSV SIN coma: comun.leer_csv() hace replace(",", ".") sobre
    # todos los campos, asi que "f_m,k" volveria leido como "f_m.k". La notacion de
    # imprenta se arma en 90_tablas_informe.py a partir de estas claves.
    filas_csv = []
    for v in verificaciones:
        fila = {"clase": v["clase"], "cumple": "si" if v["cumple"] else "no",
                "frenan": " ".join(SIMBOLO_CSV[m] for m in v["frenan"])
                          if v["frenan"] else ""}
        for d in v["detalle"]:
            clave = SIMBOLO_CSV[d["magnitud"]]
            fila[clave + "_req"] = d["requerido"]
            fila[clave + "_rel"] = d["relacion"]
        filas_csv.append(fila)

    campos = ["clase", "fmk_req", "fmk_rel", "E0mean_req", "E0mean_rel",
              "rok_req", "rok_rel", "cumple", "frenan"]
    unidades = ["[-]", "[N/mm2]", "[-]", "[kN/mm2]", "[-]",
                "[kg/m3]", "[-]", "[-]", "[-]"]
    C.guardar_csv("05_verificacion_clases.csv", campos, filas_csv, unidades)

    # Lo que falta para alcanzar la clase siguiente, en la magnitud que la frena.
    falta_abs = falta_pct = ""
    if siguiente:
        d = next(x for x in siguiente["detalle"] if not x["cumple"])
        falta_abs = d["requerido"] - d["obtenido"]
        falta_pct = falta_abs / d["obtenido"] * 100

    fila_asignada = [{
        "clase": asignada["clase"],
        "gobierna": " ".join(SIMBOLO_CSV[m] for m in frenan) if frenan else "ninguno",
        "clase_siguiente": siguiente["clase"] if siguiente else "",
        "fmk": fmk,
        "fmk_req": asignada["detalle"][0]["requerido"],
        "fmk_rel": asignada["detalle"][0]["relacion"],
        "E0mean_kn": e0mean_kn,
        "E0mean_req": asignada["detalle"][1]["requerido"],
        "E0mean_rel": asignada["detalle"][1]["relacion"],
        "rok": rok,
        "rok_req": asignada["detalle"][2]["requerido"],
        "rok_rel": asignada["detalle"][2]["relacion"],
        "falta_abs": falta_abs,
        "falta_pct": falta_pct,
        "clase_con_105": clase_105,
        "rok_con_105": rok_ajustada,
    }]
    C.guardar_csv(
        "05_clase_asignada.csv",
        ["clase", "gobierna", "clase_siguiente",
         "fmk", "fmk_req", "fmk_rel", "E0mean_kn", "E0mean_req", "E0mean_rel",
         "rok", "rok_req", "rok_rel", "falta_abs", "falta_pct",
         "clase_con_105", "rok_con_105"],
        fila_asignada,
        ["[-]", "[-]", "[-]",
         "[N/mm2]", "[N/mm2]", "[-]", "[kN/mm2]", "[kN/mm2]", "[-]",
         "[kg/m3]", "[kg/m3]", "[-]", "[N/mm2]", "[%]",
         "[-]", "[kg/m3]"],
    )

    C.guardar_csv(
        "05_robustez.csv",
        ["clave", "escenario", "fmk", "rok", "clase"],
        escenarios,
        ["[-]", "[-]", "[N/mm2]", "[kg/m3]", "[-]"],
    )

    escribir_resumen(fmk, e0mean, e0mean_kn, rok, verificaciones, asignada,
                     siguiente, frenan, clase_105, rok_ajustada, obtenida,
                     escenarios)
    print()
    print("Escrito: resultados/05_verificacion_clases.csv")
    print("Escrito: resultados/05_clase_asignada.csv")
    print("Escrito: resultados/05_robustez.csv")
    print("Escrito: resultados/05_resumen_etapa4.md")


def escribir_resumen(fmk, e0mean, e0mean_kn, rok, verificaciones, asignada,
                     siguiente, frenan, clase_105, rok_ajustada, castano,
                     escenarios):
    L = []
    L.append("# Etapa 4 - Asignacion de la clase resistente")
    L.append("")
    L.append("Generado por `scripts/05_clase_resistente.py`. No editar a mano.")
    L.append("")
    L.append("Norma: **UNE-EN 338:2010**, Tabla 1, via diapositiva S03E02 p.55, que es la")
    L.append("fuente que habilita la letra del trabajo. Picea es conifera: clases **C**.")
    L.append("")
    L.append("## Autovalidacion del metodo")
    L.append("")
    L.append("El castano de la propia diapositiva (f_m,k = 28 N/mm2, E_0,medio = 12,3")
    L.append("kN/mm2, ro_k = 510 kg/m3) da **%s** con esta implementacion, y la" % castano)
    L.append("diapositiva asigna D24. Coincide, asi que la tabla transcrita y la regla")
    L.append("de asignacion estan bien.")
    L.append("")
    L.append("## Datos de entrada")
    L.append("")
    L.append(C.tabla_md(
        ["Magnitud", "Valor", "Unidad", "Origen"],
        [["f_m,k", C.num(fmk, 2), "N/mm2", "etapa 3, EN 384 form. (11)"],
         ["E_0,mean", C.num(e0mean, 0), "N/mm2", "etapa 3, EN 384 form. (12)"],
         ["E_0,mean", C.num(e0mean_kn, 3), "kN/mm2", "el mismo, en la unidad de EN 338"],
         ["ro_k", C.num(rok, 1), "kg/m3", "etapa 3, EN 384 form. (13)"]]))
    L.append("")
    L.append("## Verificacion clase por clase")
    L.append("")
    L.append("Relacion = valor obtenido / minimo exigido. Cumple si es >= 1,00.")
    L.append("")
    filas = []
    for v in verificaciones:
        d = {x["magnitud"]: x for x in v["detalle"]}
        filas.append([
            v["clase"],
            C.num(d["f_m,k"]["requerido"], 0), C.num(d["f_m,k"]["relacion"], 3),
            C.num(d["E_0,mean"]["requerido"], 1), C.num(d["E_0,mean"]["relacion"], 3),
            C.num(d["ro_k"]["requerido"], 0), C.num(d["ro_k"]["relacion"], 3),
            "SI" if v["cumple"] else "no",
        ])
    L.append(C.tabla_md(
        ["Clase", "f_m,k min", "rel.", "E_0 min", "rel.", "ro_k min", "rel.", "Cumple"],
        filas))
    L.append("")
    L.append("## Resultado")
    L.append("")
    L.append("**Clase resistente asignada: %s**" % asignada["clase"])
    L.append("")
    filas = []
    for d in asignada["detalle"]:
        filas.append([d["magnitud"], C.num(d["obtenido"], 2), C.num(d["requerido"], 2),
                      d["unidad"], C.num(d["relacion"], 3),
                      C.num((d["relacion"] - 1) * 100, 1) + " %",
                      "cumple" if d["cumple"] else "NO CUMPLE"])
    L.append(C.tabla_md(
        ["Criterio", "Obtenido", "Exigido", "Unidad", "Relacion", "Margen", "Verificacion"],
        filas))
    L.append("")
    if siguiente:
        L.append("### Que impide subir a %s" % siguiente["clase"])
        L.append("")
        L.append("Gobierna: **%s**." % ", ".join(frenan))
        L.append("")
        filas = []
        for d in siguiente["detalle"]:
            falta = d["requerido"] - d["obtenido"]
            filas.append([d["magnitud"], C.num(d["obtenido"], 2),
                          C.num(d["requerido"], 2), d["unidad"],
                          C.num(falta, 2) if falta > 0 else "-",
                          C.num(falta / d["obtenido"] * 100, 1) + " %" if falta > 0 else "-",
                          "cumple" if d["cumple"] else "NO CUMPLE"])
        L.append(C.tabla_md(
            ["Criterio", "Obtenido", "Exigido para %s" % siguiente["clase"], "Unidad",
             "Falta", "Falta rel.", "Verificacion"], filas))
    L.append("")
    L.append("## Escenario del ajuste de densidad (EN 384 §5.3.4)")
    L.append("")
    L.append("Si la densidad se hubiera medido sobre pieza completa, corresponderia")
    L.append("dividirla por 1,05:")
    L.append("")
    L.append("    ro_k = %s / 1,05 = %s kg/m3  ->  clase %s"
             % (C.num(rok, 1), C.num(rok_ajustada, 1), clase_105))
    L.append("")
    if clase_105 == asignada["clase"]:
        L.append("**La clase no cambia.** La decision pendiente sobre el 1,05 no altera el")
        L.append("resultado del trabajo, porque quien gobierna no es la densidad.")
    else:
        L.append("**ATENCION: la clase cambia.** Hay que cerrar la consulta al docente")
        L.append("antes de entregar.")
    L.append("")
    L.append("## Robustez frente a las decisiones de criterio")
    L.append("")
    L.append("Cada fila rehace la asignacion cambiando una sola decision.")
    L.append("")
    L.append(C.tabla_md(
        ["Escenario", "f_m,k", "ro_k", "Clase", "Efecto"],
        [[e["escenario"], C.num(e["fmk"], 2), C.num(e["rok"], 1), e["clase"],
          "igual" if e["clase"] == asignada["clase"] else "CAMBIA"]
         for e in escenarios]))
    L.append("")
    cambian = [e for e in escenarios if e["clase"] != asignada["clase"]]
    if cambian:
        L.append("La unica decision que mueve la clase es **%s**."
                 % cambian[0]["escenario"])
        L.append("Esta cerrada por la norma: EN 14358 §3.2.2 c) impone la log-normal")
        L.append("salvo que el analisis estadistico demuestre que la normal ajusta")
        L.append("mejor, y el contraste de Kolmogorov-Smirnov de la etapa 3 muestra lo")
        L.append("contrario en las tres submuestras. Aun asi conviene declararlo en el")
        L.append("informe, porque es el punto mas sensible del trabajo.")
    else:
        L.append("Ninguna de las decisiones de criterio evaluadas cambia la clase.")
    L.append("")
    ruta = os.path.join(C.RESULTADOS, "05_resumen_etapa4.md")
    with open(ruta, "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")


if __name__ == "__main__":
    main()
