def sub(path, pairs):
    s = open(path, encoding="utf-8").read()
    for a, b in pairs:
        assert a in s, (path, a[:70])
        s = s.replace(a, b, 1)
    open(path, "w", encoding="utf-8").write(s)


sub("ef_carrascal.py", [
    (r'''e.eq("prec", r"P_s=\frac{h_s+\alpha}{n_s+\alpha+\beta},\quad \alpha=1,\ \beta=3;\qquad R_s=\exp\!\left(-\frac{\Delta t}{\tau_s}\right),\quad \tau_s=\tau_0\,\varepsilon_s\,(0{,}6+\mathcal{M}_s^{-}),\quad \tau_0=1{,}8\ \text{días}")''',
     r'''e.eq("prec", r"P_s=\frac{h_s+\alpha}{n_s+\alpha+\beta},\qquad \alpha=1,\ \beta=3")
    e.eq("ret", r"R_s=\exp\!\left(-\frac{\Delta t}{\tau_s}\right)")
    e.eq("tau", r"\tau_s=\tau_0\,\varepsilon_s\,(0{,}6+\mathcal{M}_s^{-}),\qquad \tau_0=1{,}8\ \text{días}")'''),
    (r'''e.eq("logit", r"p=\frac{1}{1+e^{-z}},\quad z=w_1\,\mathrm{precision}+w_2\,\mathrm{dificultad}+w_3\,\mathrm{dias}+b;\qquad \mathcal{L}=-\frac{1}{N}\sum_{n=1}^{N}\big[y_n\ln p_n+(1-y_n)\ln(1-p_n)\big]")''',
     r'''e.eq("logit", r"p=\frac{1}{1+e^{-z}},\qquad z=w_1\,x_1+w_2\,x_2+w_3\,x_3+b")
    e.eq("loss", r"\mathcal{L}=-\frac{1}{N}\sum_{n=1}^{N}\big[y_n\ln p_n+(1-y_n)\ln(1-p_n)\big]")'''),
    (r'''e.eq("sm2", r"\varepsilon\leftarrow\operatorname{clip}\big(\varepsilon+0{,}1-(1-q)(0{,}8+(1-q)),\,1{,}3,\,2{,}8\big),\qquad I\leftarrow\begin{cases}1 & q<0{,}6\\ \max(1,I\varepsilon) & \text{en otro caso}\end{cases}")''',
     r'''e.eq("sm2", r"\varepsilon\leftarrow\operatorname{clip}\big(\varepsilon+0{,}1-(1-q)(0{,}8+(1-q)),\,1{,}3,\,2{,}8\big)")
    e.eq("int", r"I\leftarrow\begin{cases}1 & q<0{,}6\\ \max(1,I\varepsilon) & \text{en otro caso}\end{cases}")'''),
    ("sustituye a la fórmula fija y se reentrena cada 20 intentos nuevos, con 300 épocas de descenso de gradiente y tasa 0,35 sobre variables estandarizadas:",
     "sustituye a la fórmula fija y se reentrena cada 20 intentos nuevos, con 300 épocas de descenso de gradiente y tasa 0,35 sobre variables estandarizadas $x_1$ (precisión), $x_2$ (dificultad de la actividad) y $x_3$ (días desde la última práctica), minimizando la entropía cruzada:"),
])
sub("ef_quintana.py", [
    (r'''e.eq("p", r"p_i=\frac{1}{1+e^{-k(\bar\mu_i-\mathrm{dif}_i)}},\quad k=6;\qquad \eta_i=\exp\!\left(-\frac{(p_i-p^{*})^2}{2\sigma_p^2}\right),\quad \sigma_p=0{,}18")''',
     r'''e.eq("p", r"p_i=\frac{1}{1+e^{-k(\bar\mu_i-\mathrm{dif}_i)}},\qquad k=6")
    e.eq("eta", r"\eta_i=\exp\!\left(-\frac{(p_i-p^{*})^2}{2\sigma_p^2}\right),\qquad \sigma_p=0{,}18")'''),
    (r'''e.eq("res", r"\begin{aligned}&\sum_i d_ix_i\le T_{\max},\qquad \sum_i x_i=K,\qquad x_i\le a_i,\qquad \sum_{i\in G}x_i\ge1,\\ &\sum_i\mathrm{dif}_ix_i\le0{,}72K,\qquad \sum_{i:\,s\in S_i}x_i\le2\ \ \forall s\in S,\qquad \sum_{i\in V}x_i\ge1\end{aligned}")''',
     r'''e.eq("res", r"\begin{aligned}\sum_i d_ix_i&\le T_{\max}\\ \sum_i x_i&=K\\ x_i&\le a_i\\ \sum_{i\in G}x_i&\ge1\\ \sum_i\mathrm{dif}_ix_i&\le0{,}72K\\ \sum_{i:\,s\in S_i}x_i&\le2\quad\forall s\in S\\ \sum_{i\in V}x_i&\ge1\end{aligned}")'''),
])
sub("ef_petro.py", [
    (r'''e.eq("alpha", r"\alpha_i=\frac{1}{\pi}\arccos\langle u_i,u_{i+1}\rangle,\qquad \tau_j=\frac{1}{3}\operatorname{clip}\!\left(\frac{\lVert p_{t_j}-p_4\rVert}{\sigma},\,0,\,3\right)")''',
     r'''e.eq("alpha", r"\alpha_i=\frac{1}{\pi}\arccos\langle u_i,u_{i+1}\rangle")
    e.eq("tau", r"\tau_j=\frac{1}{3}\operatorname{clip}\!\left(\frac{\lVert p_{t_j}-p_4\rVert}{\sigma},\,0,\,3\right)")'''),
    (r'''e.eq("dc", r"d_c=\min_{s\in S_c}d(x,s),\qquad P(c\mid x)=\frac{\exp\!\big(-(d_c-d_{\min})/T\big)}{\sum_k\exp\!\big(-(d_k-d_{\min})/T\big)}")''',
     r'''e.eq("dc", r"d_c=\min_{s\in S_c}d(x,s)")
    e.eq("softmax", r"P(c\mid x)=\frac{\exp\!\big(-(d_c-d_{\min})/T\big)}{\sum_k\exp\!\big(-(d_k-d_{\min})/T\big)}")'''),
])
sub("ef_negrete.py", [
    (r'''e.eq("vent", r"h_i=\frac{\max\!\big(W_{\min},\,\min(\text{tol},\,0{,}85\,g)\big)}{2},\qquad \text{ventana}_i=\big[a_i-1{,}15\,h_i,\ a_i+0{,}85\,h_i\big]")''',
     r'''e.eq("vent", r"h_i=\frac{\max\!\big(W_{\min},\,\min(\text{tol},\,0{,}85\,g)\big)}{2}")
    e.eq("vent2", r"\text{ventana}_i=\big[a_i-1{,}15\,h_i,\ a_i+0{,}85\,h_i\big]")'''),
])
sub("ef_guerra.py", [(r'''r"\hat p\ \text{(Wilson)}=\frac{''', r'''r"\mathrm{IC}_{95\,\%}=\frac{''')])
print("ok")
