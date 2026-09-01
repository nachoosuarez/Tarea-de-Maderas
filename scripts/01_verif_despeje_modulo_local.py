# -*- coding: utf-8 -*-
# Contraste: forma cerrada despejada  vs  resolucion iterativa de la ec. implicita (G = Em,l/16)
casos=[ (36.0, 93.4, 603.7, 1771.4, 260.0),
        (44.9,142.1, 931.3, 2714.6, 400.0),
        (57.0,189.8,1217.1,3574.1, 500.0) ]
print(f"{'b':>6}{'h':>7}{'cerrada':>12}{'iterativa':>12}{'dif %':>9}")
for b,h,a,l,k in casos:
    N = 3*a*l**2 - 4*a**3
    S = 1.0/k                      # (w2-w1)/(F2-F1)
    Ec = k*(N + 38.4*a*h**2)/(4*b*h**3)      # forma cerrada
    E = 12000.0
    for _ in range(200):           # iterativa sobre la ecuacion de la diapo p.26
        G = E/16.0
        E = N / (2*b*h**3*(2*S - 6*a/(5*G*b*h)))
    print(f"{b:>6.1f}{h:>7.1f}{Ec:>12.1f}{E:>12.1f}{100*(Ec-E)/E:>9.5f}")
