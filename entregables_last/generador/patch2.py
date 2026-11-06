def sub(path, pairs):
    s = open(path, encoding="utf-8").read()
    for a, b in pairs:
        assert a in s, (path, a[:80])
        s = s.replace(a, b, 1)
    open(path, "w", encoding="utf-8").write(s)


sub("ef_petro.py", [
    (r'''e.eq("kappa", r"\kappa=\operatorname{clip}\!\left(\frac{\dfrac{\lVert p_d-p_a\rVert}{\lVert p_b-p_a\rVert+\lVert p_c-p_b\rVert+\lVert p_d-p_c\rVert}-0{,}35}{0{,}65},\,0,\,1\right)")''',
     r'''e.eq("ratio", r"\rho_f=\frac{\lVert p_d-p_a\rVert}{\lVert p_b-p_a\rVert+\lVert p_c-p_b\rVert+\lVert p_d-p_c\rVert}")
    e.eq("kappa", r"\kappa=\operatorname{clip}\!\left(\frac{\rho_f-0{,}35}{0{,}65},\,0,\,1\right)")'''),
    ('''    e.figura("matriz", "matriz_similitud.png", "Matrices 8 × 8 de las señas calibradas: (a) similitud coseno del método inicial; (b) distancia por bloques del descriptor propuesto.", 16.0, ancha=True)''',
     '''    e.figura("matriz", "matriz_cos.png", "(a) Similitud coseno entre las ocho señas calibradas, método inicial.", 7.8)
    e.figura("matriz2", "matriz_dist.png", "(b) Distancia por bloques entre las ocho señas calibradas, descriptor propuesto.", 7.8)'''),
    ("({fig:matriz}).\")", "({fig:matriz} y {fig:matriz2}).\")"),
    ("filas, [1.3, 3.6, 3.6]", "filas, [1.9, 3.3, 3.3]"),
])
sub("ef_quintana.py", [
    (r'''    e.eq("res", r"\begin{aligned}\sum_i d_ix_i&\le T_{\max}\\ \sum_i x_i&=K\\ x_i&\le a_i\\ \sum_{i\in G}x_i&\ge1\\ \sum_i\mathrm{dif}_ix_i&\le0{,}72K\\ \sum_{i:\,s\in S_i}x_i&\le2\quad\forall s\in S\\ \sum_{i\in V}x_i&\ge1\end{aligned}")''',
     r'''    e.B([r"Tiempo total: $\sum_i d_i x_i\le T_{\max}$.", r"Tamaño de la sesión: $\sum_i x_i=K$.", r"Prerrequisitos: $x_i\le a_i$ para toda actividad $i$.", r"Una actividad lúdica como mínimo: $\sum_{i\in G}x_i\ge 1$.",
         r"Dificultad media acotada: $\sum_i \mathrm{dif}_i x_i\le 0{,}72\,K$.", r"A lo sumo dos actividades por habilidad: $\sum_{i:\,s\in S_i}x_i\le 2$ para toda $s\in S$.", r"Un repaso vencido: $\sum_{i\in V}x_i\ge 1$."])'''),
    ("Las restricciones fijan el tiempo total, el tamaño de la sesión, los prerrequisitos, al menos una actividad lúdica, una dificultad media acotada, un máximo de dos actividades por habilidad y la inclusión de un repaso vencido si existe. El problema se resuelve",
     "Las restricciones anteriores fijan el tiempo total, el tamaño de la sesión, los prerrequisitos, una actividad lúdica como mínimo, una dificultad media acotada, un máximo de dos actividades por habilidad y la inclusión de un repaso vencido si existe. El problema se resuelve"),
    ('''["N.º", "Actividad", "min", "Dif.", "Habilidades"],
            [[str(a["i"]), a["nombre"], str(a["d"]), f(a["dif"], 2), ", ".join(a["hab"])] for a in cat], [0.8, 3.2, 0.8, 0.9, 3.6], size=8)''',
     '''["N.º", "Actividad", "min", "Dif.", "Habilidades"],
            [[str(a["i"]), a["nombre"], str(a["d"]), f(a["dif"], 2), ", ".join(a["hab"])] for a in cat], [0.9, 3.0, 0.9, 1.0, 2.7], size=8)'''),
    ('''["Escenario", "Objetivo", "Sesión", "Factibles"], filas, [3.9, 1.5, 1.8, 1.3]''', '''["Escenario", "Objetivo", "Sesión", "Factibles"], filas, [3.3, 1.4, 1.7, 1.6]'''),
])
sub("ef_negrete.py", [
    (r'''e.eq("combo", r"\text{puntos}_i=b_i\cdot\min\!\left(1+0{,}5\left\lfloor \frac{c}{10}\right\rfloor,\ 4\right),\qquad b_i\in\{100,70,50\}")''',
     r'''e.eq("combo", r"\text{puntos}_i=b_i\cdot\min\!\left(1+0{,}5\left\lfloor \frac{c}{10}\right\rfloor,\ 4\right)")'''),
    ("donde $c$ es el número de aciertos seguidos.", "donde $b_i$ toma los valores 100, 70 o 50 y $c$ es el número de aciertos seguidos."),
])
sub("ef_carrascal.py", [
    (r'''e.eq("sm2", r"\varepsilon\leftarrow\operatorname{clip}\big(\varepsilon+0{,}1-(1-q)(0{,}8+(1-q)),\,1{,}3,\,2{,}8\big)")''',
     r'''e.eq("dsm", r"\Delta\varepsilon=0{,}1-(1-q)\big(0{,}8+(1-q)\big)")
    e.eq("sm2", r"\varepsilon\leftarrow\operatorname{clip}\big(\varepsilon+\Delta\varepsilon,\,1{,}3,\,2{,}8\big)")'''),
    (r'''e.eq("logit", r"p=\frac{1}{1+e^{-z}},\qquad z=w_1\,x_1+w_2\,x_2+w_3\,x_3+b")''',
     r'''e.eq("logit", r"p=\frac{1}{1+e^{-z}}")
    e.eq("zeta", r"z=w_1\,x_1+w_2\,x_2+w_3\,x_3+b")'''),
])
sub("ef_guerra.py", [("[2.7, 1.3, 2.6, 1.9], size=8)", "[2.5, 1.5, 2.5, 2.0], size=8)")])
sub("ef_pemberty.py", [("[0.9, 3.0, 3.2, 1.4], size=8)", "[1.0, 2.7, 3.0, 1.8], size=8)"), ("[0.9, 5.3, 2.3], size=8)", "[1.1, 5.0, 2.4], size=8)"),
                       ("Condiciones previas al piloto, en orden. Verde: cumplido; naranja: pendiente.", "Condiciones previas al piloto, en orden. Verde: cumplida; naranja: pendientes.")])
print("ok")
