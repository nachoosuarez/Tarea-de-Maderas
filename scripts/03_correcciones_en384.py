# -*- coding: utf-8 -*-
"""ETAPA 2 - Correccion a condiciones de referencia, UNE-EN 384:2016 apartado 5.4.

Entrada : resultados/02_propiedades_por_pieza.csv
Salida  : resultados/03_valores_corregidos.csv
          resultados/03_resumen_etapa2.md

EN 384:2016 §5.4.1 (p.10): "Cada resultado de ensayo debe ajustarse PROBETA A PROBETA
respecto a las condiciones de referencia indicadas en el apartado 5.3." Por eso todo lo
de abajo se aplica pieza por pieza y recien despues se hace estadistica.

QUE SE CORRIGE Y QUE NO
-----------------------
§5.4.2 (p.10) enumera taxativamente que se ajusta por humedad: resistencia a compresion
paralela (formula 1), modulo de elasticidad paralelo (formula 2) y densidad (formula 3).
La RESISTENCIA A FLEXION NO figura en esa lista: no se corrige por humedad. Solo recibe
los factores geometricos k_h y k_l del §5.4.3.

  (2)  E0 = E0(u) * (1 + 0,01*(u - uref))        modulo, uref = 12 %
  (3)  ro = ro(u) * (1 - 0,005*(u - uref))       densidad
       Validez 8 % <= u <= 18 %. Con u > 18 % se toma u = 18 %. En este lote las 258
       piezas caen dentro del rango (auditoria de la semana 1), asi que no se trunca
       ninguna.

§5.4.3 (p.11), factores geometricos, ambos DIVIDEN a la resistencia:

  (4)  k_h = Min{ (150/h)^0,2 ; 1,3 }
       Solo para canto h < 150 mm y densidad <= 700 kg/m3. Fuera de esa condicion el
       ajuste no aplica y se toma k_h = 1 (no se aplica (150/h)^0,2 con h > 150, que
       daria un factor < 1 y penalizaria la pieza sin respaldo normativo).

  (5)  k_l = (48h / l_et)^0,2
  (6)  l_et = l + 5*a_f
       "l_et es la longitud real de ensayo; l es la luz del dispositivo de ensayo;
        a_f es la separacion entre los DOS PUNTOS DE APLICACION DE LA CARGA".
       ATENCION: a_f NO es la columna `a` del archivo de datos. La columna `a` es la
       distancia de apoyo a punto de carga (6h +- 1,5h en el esquema de S03E02 p.26);
       la separacion interior entre los dos puntos de carga es a_f = l - 2*a.
       Comprobacion de consistencia: con el esquema nominal l = 18h y a_f = 6h sale
       l_et = 18h + 30h = 48h y por tanto k_l = 1 exacto, que es lo que la norma dice
       que tiene que pasar cuando el ensayo esta en la geometria de referencia.
       El ajuste se aplica porque la luz real no es 18h exacto (18,86h / 19,10h /
       18,83h segun la auditoria).

§5.4.4 (p.12), formula (8): E0 = E_m,local(uref). Se toma el modulo local, ya corregido
por humedad, directamente como modulo paralelo a la fibra. NO corresponde la formula (7)
(E0 = 1,3*E_m,global - 2690), que es para el modulo GLOBAL medido con G infinito (nota
del §5.4.4); la letra de este trabajo pide el modulo local con G = E/16.

§5.3.4 (p.10), ajuste de densidad dividiendo por 1,05: se aplica a "las probetas que no
se someten a ensayo hasta rotura" cuando la densidad se saca de la pieza completa. Las
258 piezas de este lote se ensayaron hasta rotura, asi que por el texto literal NO
corresponde. Queda como interruptor AJUSTE_105 para poder cuantificar el efecto si el
docente confirma que la densidad se midio sobre pieza completa.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comun as C

U_REF = 12.0        # % , EN 384:2016 §5.3.1 y §5.4.2
U_MIN, U_MAX = 8.0, 18.0
RO_LIMITE_KH = 700.0   # kg/m3, condicion del §5.4.3
H_LIMITE_KH = 150.0    # mm
AJUSTE_105 = False     # §5.3.4. Ver encabezado. VERIFICAR con el docente.


def k_h(p):
    """Factor de canto, EN 384:2016 §5.4.3 formula (4). Divide a f_m."""
    if p["h"] < H_LIMITE_KH and p["ro"] <= RO_LIMITE_KH:
        return min((150.0 / p["h"]) ** 0.2, 1.3)
    return 1.0


def a_f(p):
    """Separacion entre los dos puntos de aplicacion de la carga, en mm."""
    return p["l"] - 2.0 * p["a"]


def l_et(p):
    """Longitud real de ensayo, EN 384:2016 §5.4.3 formula (6)."""
    return p["l"] + 5.0 * a_f(p)


def k_l(p):
    """Factor de longitud de ensayo, formula (5). Divide a f_m."""
    return (48.0 * p["h"] / l_et(p)) ** 0.2


def main():
    piezas = C.leer_csv("02_propiedades_por_pieza.csv")

    truncadas = 0
    for p in piezas:
        u = p["CH"]
        if u > U_MAX:
            u = U_MAX
            truncadas += 1
        p["u_usado"] = u
        p["fuera_rango"] = 1 if (p["CH"] < U_MIN or p["CH"] > U_MAX) else 0

        p["af"] = a_f(p)
        p["let"] = l_et(p)
        p["kh"] = k_h(p)
        p["kl"] = k_l(p)

        # Resistencia a flexion: solo factores geometricos, sin humedad (§5.4.2)
        p["fm_ref"] = p["fm"] / (p["kh"] * p["kl"])

        # Modulo: humedad (2) y luego (8) E0 = Em,local(uref)
        p["Eml_ref"] = p["Eml"] * (1.0 + 0.01 * (u - U_REF))
        p["E0"] = p["Eml_ref"]

        # Densidad: humedad (3) y, si corresponde, el 1,05 del §5.3.4
        p["ro_ref"] = p["ro"] * (1.0 - 0.005 * (u - U_REF))
        if AJUSTE_105:
            p["ro_ref"] /= 1.05

    campos = ["viga", "muestra", "b", "h", "a", "l", "af", "let", "CH", "u_usado",
              "Pmax", "Pf", "kh", "kl", "fm", "fm_ref", "Eml", "Eml_ref", "E0",
              "ro", "ro_ref"]
    unidades = ["[-]", "[-]", "[mm]", "[mm]", "[mm]", "[mm]", "[mm]", "[mm]", "[%]",
                "[%]", "[N]", "[N/mm]", "[-]", "[-]", "[N/mm2]", "[N/mm2]", "[N/mm2]",
                "[N/mm2]", "[N/mm2]", "[kg/m3]", "[kg/m3]"]
    ruta = C.guardar_csv("03_valores_corregidos.csv", campos, piezas, unidades)

    grupos = C.por_muestra(piezas)
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

    # Tabla de factores: son constantes dentro de cada muestra salvo por el canto
    filas_k = []
    for m, g in grupos.items():
        kh = C.resumen([x["kh"] for x in g])
        kl = C.resumen([x["kl"] for x in g])
        hh = C.resumen([x["h"] for x in g])
        filas_k.append([
            m, len(g), C.num(hh["media"], 2),
            C.num(g[0]["af"], 1), C.num(48 * hh["media"], 1), C.num(C.resumen([x["let"] for x in g])["media"], 1),
            f'{C.num(kh["min"], 4)} – {C.num(kh["max"], 4)}',
            f'{C.num(kl["min"], 4)} – {C.num(kl["max"], 4)}',
        ])

    delta_f = []
    delta_E = []
    delta_ro = []
    for m, g in grupos.items():
        delta_f.append((m, 100 * (C.resumen([x["fm_ref"] for x in g])["media"] /
                                  C.resumen([x["fm"] for x in g])["media"] - 1)))
        delta_E.append((m, 100 * (C.resumen([x["E0"] for x in g])["media"] /
                                  C.resumen([x["Eml"] for x in g])["media"] - 1)))
        delta_ro.append((m, 100 * (C.resumen([x["ro_ref"] for x in g])["media"] /
                                   C.resumen([x["ro"] for x in g])["media"] - 1)))

    lineas = [
        "# Etapa 2 — Correccion a condiciones de referencia (UNE-EN 384:2016 §5.4)",
        "",
        "Generado por `scripts/03_correcciones_en384.py`. Salida completa en",
        "`resultados/03_valores_corregidos.csv` (258 filas).",
        "",
        f"Condiciones de referencia: `u_ref` = {C.num(U_REF,0)} %, canto 150 mm, luz 18h.",
        f"Piezas truncadas a u = 18 %: **{truncadas}**.",
        f"Ajuste de densidad por 1,05 (§5.3.4): **{'aplicado' if AJUSTE_105 else 'NO aplicado'}**.",
        "",
        "## Factores geometricos por muestra",
        "",
        C.tabla_md(["Muestra", "n", "h medio [mm]", "a_f [mm]", "48h [mm]",
                    "l_et [mm]", "k_h", "k_l"], filas_k),
        "",
        "`a_f = l - 2a` es la separacion entre los dos puntos de carga; `l_et = l + 5*a_f`.",
        "La muestra 3 tiene canto > 150 mm, por eso ahi `k_h = 1`.",
        "",
        "## Resistencia a flexion corregida `f_m,ref` [N/mm2]",
        "",
        bloque("fm_ref", 2),
        "",
        "## Modulo de elasticidad `E_0` [N/mm2]",
        "",
        bloque("E0", 0),
        "",
        "## Densidad corregida `ro_ref` [kg/m3]",
        "",
        bloque("ro_ref", 1),
        "",
        "## Efecto de la correccion sobre la media de cada muestra",
        "",
        C.tabla_md(["Muestra", "f_m", "E_0", "ro"],
                   [[m, C.num(df, 2) + " %", C.num(dE, 2) + " %", C.num(dr, 2) + " %"]
                    for (m, df), (_, dE), (_, dr) in zip(delta_f, delta_E, delta_ro)]),
        "",
        "Quien manda es `k_h`, y solo en la muestra 1: con h ~ 94 mm el factor vale 1,099 y",
        "la resistencia media cae un 8,6 % al llevarla al canto de referencia de 150 mm. En",
        "la muestra 2 (h ~ 142 mm) `k_h` apenas vale 1,010 y el efecto neto es del -0,6 %,",
        "porque `k_l` empuja en sentido contrario. En la muestra 3 `k_h` no aplica y queda",
        "solo `k_l`, con un +0,35 %.",
        "",
        "Las correcciones por humedad son despreciables (menos del 0,1 % en media) porque la",
        "humedad media de las tres muestras cae entre 11,96 % y 12,07 %, practicamente sobre",
        "el 12 % de referencia. Aun asi se aplican pieza a pieza como exige el §5.4.1: a",
        "nivel individual el rango va de 9,8 % a 13,9 % y ahi la correccion del modulo llega",
        "al 2 %.",
        "",
        "**Estos son los valores que entran a la etapa 3** (EN 14358:2016).",
        "",
    ]
    md = os.path.join(C.RESULTADOS, "03_resumen_etapa2.md")
    with open(md, "w", encoding="utf-8") as f:
        f.write("\n".join(lineas))

    print(f"OK  {len(piezas)} piezas corregidas, {truncadas} truncadas a u=18%")
    print(f"    {ruta}")
    print(f"    {md}")
    for m, g in grupos.items():
        print(f"    M{m}  kh={g[0]['kh']:.4f}  kl={g[0]['kl']:.4f}  af={g[0]['af']:.1f}  "
              f"fm_ref={C.resumen([x['fm_ref'] for x in g])['media']:6.2f}  "
              f"E0={C.resumen([x['E0'] for x in g])['media']:7.0f}  "
              f"ro_ref={C.resumen([x['ro_ref'] for x in g])['media']:6.1f}")


if __name__ == "__main__":
    main()
