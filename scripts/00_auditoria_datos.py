# -*- coding: utf-8 -*-
import os, statistics as st

# ruta relativa al repo: scripts/ -> 00-datos/
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
p = os.path.join(RAIZ, "00-datos", "Datos_Picea.txt")
rows=[]
with open(p, encoding="utf-8-sig") as f:
    lines=[l.rstrip("\n") for l in f]
hdr=lines[0].split("\t"); uni=lines[1].split("\t")
print("HEADER :", [c for c in hdr if c.strip()])
print("UNIDADES:", [c for c in uni if c.strip()])
bad=0
for i,l in enumerate(lines[2:], start=3):
    if not l.strip(): continue
    c=l.split("\t")
    try:
        rows.append(dict(viga=int(c[0]), m=int(c[1]), b=float(c[2]), h=float(c[3]),
                         a=float(c[4]), l=float(c[5]), CH=float(c[6]), ro=float(c[7]),
                         Pmax=float(c[8]), Pf=float(c[9])))
    except Exception as e:
        bad+=1; print("  linea",i,"no parseada:",repr(l[:60]),e)
print("\nfilas de datos OK:",len(rows)," | no parseadas:",bad)

ms=sorted({r["m"] for r in rows})
print("\nmuestras:",ms)
print(f"\n{'M':>2} {'n':>4} {'b med':>7} {'h med':>7} {'h min':>6} {'h max':>6} {'a':>8} {'l':>9} {'l/h':>6} {'a/h':>5}")
for m in ms:
    g=[r for r in rows if r["m"]==m]
    hm=st.mean(r["h"] for r in g); bm=st.mean(r["b"] for r in g)
    am=st.mean(r["a"] for r in g); lm=st.mean(r["l"] for r in g)
    print(f"{m:>2} {len(g):>4} {bm:>7.2f} {hm:>7.2f} {min(r['h'] for r in g):>6.1f} {max(r['h'] for r in g):>6.1f} {am:>8.1f} {lm:>9.1f} {lm/hm:>6.2f} {am/hm:>5.2f}")

print("\n-- control EN 408: l=18h+/-3h  (15h..21h) ; a=6h+/-1,5h (4,5h..7,5h) --")
for m in ms:
    g=[r for r in rows if r["m"]==m]
    ko_l=[r["viga"] for r in g if not (15*r["h"]<=r["l"]<=21*r["h"])]
    ko_a=[r["viga"] for r in g if not (4.5*r["h"]<=r["a"]<=7.5*r["h"])]
    print(f"  M{m}: fuera de rango l -> {len(ko_l)} ; a -> {len(ko_a)}")

print("\n-- control EN 384 5.4.2: 8% <= CH <= 18% ; y rangos --")
for m in ms:
    g=[r for r in rows if r["m"]==m]
    ch=[r["CH"] for r in g]; ro=[r["ro"] for r in g]; pm=[r["Pmax"] for r in g]; pf=[r["Pf"] for r in g]
    fuera=[r["viga"] for r in g if not (8<=r["CH"]<=18)]
    print(f"  M{m}: CH {min(ch):.1f}-{max(ch):.1f} (media {st.mean(ch):.2f}, fuera 8-18%: {len(fuera)}) | "
          f"ro {min(ro):.0f}-{max(ro):.0f} | Pmax {min(pm):.0f}-{max(pm):.0f} | P/f {min(pf):.0f}-{max(pf):.0f}")

print("\n-- chequeo de orden de magnitud (sin correcciones) --")
for m in ms:
    g=[r for r in rows if r["m"]==m]
    fm=[3*r["Pmax"]*r["a"]/(r["b"]*r["h"]**2) for r in g]
    E=[r["Pf"]*(3*r["a"]*r["l"]**2 - 4*r["a"]**3 + 38.4*r["a"]*r["h"]**2)/(4*r["b"]*r["h"]**3) for r in g]
    print(f"  M{m}: fm {min(fm):5.1f}-{max(fm):5.1f} med {st.mean(fm):5.1f} N/mm2 | "
          f"Em,l {min(E):6.0f}-{max(E):6.0f} med {st.mean(E):6.0f} N/mm2")
print("\nvigas duplicadas:", len(rows)-len({(r['m'],r['viga']) for r in rows}))
