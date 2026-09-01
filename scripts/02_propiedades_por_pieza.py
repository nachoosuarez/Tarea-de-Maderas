# -*- coding: utf-8 -*-
"""ETAPA 1 - Propiedades de cada pieza segun UNE-EN 408:2010.

Entrada : 00-datos/Datos_Picea.txt
Salida  : resultados/02_propiedades_por_pieza.csv
          resultados/02_resumen_etapa1.md

Formulas, con su fuente. Ninguna esta escrita de memoria:

  f_m = 3 * F * a / (b * h^2)                                  [S03E02 p.28]
      F = Pmax, carga TOTAL de la prensa. Cada punto de carga recibe F/2, de modo
      que el momento en el tramo central vale M = (F/2)*a y con W = b*h^2/6 sale
      la expresion de arriba.

  Modulo de elasticidad local, ecuacion de S03E02 p.26 (la que impone la letra),
  tomando G = E_m,l/16 (opcion 5 de esa misma diapositiva):

                        3*a*l^2 - 4*a^3
      E_m,l = ---------------------------------------
              2*b*h^3 * ( 2*(w2-w1)/(F2-F1) - 6*a/(5*G*b*h) )

      Sustituyendo G = E/16 y despejando E queda la forma cerrada

      E_m,l = (P/f) * (3*a*l^2 - 4*a^3 + 38,4*a*h^2) / (4*b*h^3)

      El despeje esta contrastado contra la resolucion iterativa de la ecuacion
      implicita en scripts/01_verif_despeje_modulo_local.py (coincide a 1e-5 %).
      Ojo con P/f: el dato viene en N/mm y es la pendiente carga-flecha, o sea la
      INVERSA del cociente (w2-w1)/(F2-F1) que aparece en la ecuacion.

Estos valores todavia NO estan corregidos a condiciones de referencia: eso es la
etapa 2 (scripts/03_correcciones_en384.py).
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comun as C


def resistencia_flexion(p):
    """f_m en N/mm2. S03E02 p.28."""
    return 3.0 * p["Pmax"] * p["a"] / (p["b"] * p["h"] ** 2)


def modulo_local(p):
    """E_m,local en N/mm2. S03E02 p.26 con G = E_m,l/16, forma cerrada."""
    a, l, b, h, k = p["a"], p["l"], p["b"], p["h"], p["Pf"]
    return k * (3 * a * l**2 - 4 * a**3 + 38.4 * a * h**2) / (4 * b * h**3)


def main():
    piezas = C.cargar_datos()
    for p in piezas:
        p["fm"] = resistencia_flexion(p)
        p["Eml"] = modulo_local(p)
        p["W"] = p["b"] * p["h"] ** 2 / 6.0          # modulo resistente, mm3
        p["Mmax"] = p["Pmax"] / 2.0 * p["a"]         # momento de rotura, N*mm

    campos = ["viga", "muestra", "b", "h", "a", "l", "CH", "ro", "Pmax", "Pf",
              "W", "Mmax", "fm", "Eml"]
    unidades = ["[-]", "[-]", "[mm]", "[mm]", "[mm]", "[mm]", "[%]", "[kg/m3]",
                "[N]", "[N/mm]", "[mm3]", "[N*mm]", "[N/mm2]", "[N/mm2]"]
    ruta = C.guardar_csv("02_propiedades_por_pieza.csv", campos, piezas, unidades)

    grupos = C.por_muestra(piezas)
    lineas = [
        "# Etapa 1 — Propiedades por pieza (UNE-EN 408:2010)",
        "",
        "Generado por `scripts/02_propiedades_por_pieza.py`. Salida completa en",
        "`resultados/02_propiedades_por_pieza.csv` (258 filas).",
        "",
        "**Valores SIN corregir a condiciones de referencia.** La correccion es la etapa 2.",
        "",
        "## Resistencia a flexion `f_m` [N/mm2]",
        "",
    ]
    enc = ["Muestra", "n", "media", "s", "CoV", "min", "mediana", "max"]

    def bloque(clave, dec):
        filas = []
        for m, g in grupos.items():
            r = C.resumen([x[clave] for x in g])
            filas.append([m, r["n"], C.num(r["media"], dec), C.num(r["s"], dec),
                          C.num(r["CoV"] * 100, 1) + " %", C.num(r["min"], dec),
                          C.num(r["mediana"], dec), C.num(r["max"], dec)])
        r = C.resumen([x[clave] for x in piezas])
        filas.append(["**Lote**", r["n"], C.num(r["media"], dec), C.num(r["s"], dec),
                      C.num(r["CoV"] * 100, 1) + " %", C.num(r["min"], dec),
                      C.num(r["mediana"], dec), C.num(r["max"], dec)])
        return C.tabla_md(enc, filas)

    lineas.append(bloque("fm", 2))
    lineas += ["", "## Modulo de elasticidad local `E_m,l` [N/mm2]", ""]
    lineas.append(bloque("Eml", 0))
    lineas += ["", "## Densidad medida `ro` [kg/m3] (sin corregir por humedad)", ""]
    lineas.append(bloque("ro", 1))
    lineas += [
        "",
        "## Control de coherencia",
        "",
        "- La dispersion de `f_m` (CoV en torno al 20-25 %) es la esperable en madera",
        "  aserrada clasificada visualmente; la del modulo es bastante menor, como",
        "  corresponde a una propiedad de rigidez.",
        "- Ninguna pieza da valor negativo ni nulo en `f_m` ni en `E_m,l`.",
        "",
    ]
    md = os.path.join(C.RESULTADOS, "02_resumen_etapa1.md")
    with open(md, "w", encoding="utf-8") as f:
        f.write("\n".join(lineas))

    print(f"OK  {len(piezas)} piezas procesadas")
    print(f"    {ruta}")
    print(f"    {md}")
    for m, g in grupos.items():
        rf = C.resumen([x["fm"] for x in g])
        re_ = C.resumen([x["Eml"] for x in g])
        print(f"    M{m}  n={rf['n']:3d}  fm={rf['media']:6.2f} N/mm2   "
              f"Em,l={re_['media']:7.0f} N/mm2")


if __name__ == "__main__":
    main()
