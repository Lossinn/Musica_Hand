"""Ecuaciones largas reescritas en varias líneas para que quepan en una columna (mismo contenido matemático)."""
NL = "\\\\"
EQ_OV = {
    "kappa": r"\begin{aligned}\kappa&=\operatorname{clip}\!\left(\frac{r-0{,}35}{0{,}65},\,0,\,1\right),NL r&=\frac{\lVert p_d-p_a\rVert}{\lVert p_b-p_a\rVert+\lVert p_c-p_b\rVert+\lVert p_d-p_c\rVert}\end{aligned}",
    "dist": r"d(a,b)^2=\frac{1}{\sum_g w_g}\sum_g w_g\,\frac{1}{|g|}\sum_{i\in g}(a_i-b_i)^2",
    "prec": r"\begin{aligned}P_s&=\frac{h_s+\alpha}{n_s+\alpha+\beta},NL \alpha&=1,\ \beta=3\end{aligned}",
    "ret": r"\begin{aligned}R_s&=\exp\!\left(-\frac{\Delta t}{\tau_s}\right),NL \tau_s&=\tau_0\,\varepsilon_s\,(0{,}6+\mathcal{M}_s^{-}),NL \tau_0&=1{,}8\ \text{días}\end{aligned}",
    "sm2": r"\begin{aligned}\varepsilon&\leftarrow\operatorname{clip}\!\big(\varepsilon+0{,}1-(1-q)(0{,}8+(1-q)),NL&\qquad 1{,}3,\,2{,}8\big),NL I&\leftarrow\begin{cases}1 & q<0{,}6NL \max(1,I\varepsilon) & \text{en otro caso}\end{cases}\end{aligned}",
    "logit": r"\begin{aligned}p&=\frac{1}{1+e^{-z}},NL z&=w_1\,\mathrm{precision}+w_2\,\mathrm{dificultad}NL&\quad+w_3\,\mathrm{dias}+b\end{aligned}",
    "p": r"\begin{aligned}p_i&=\frac{1}{1+e^{-k(\bar\mu_i-\mathrm{dif}_i)}},NL k&=6\end{aligned}",
    "eta": r"\begin{aligned}\eta_i&=\exp\!\left(-\frac{(p_i-p^{*})^2}{2\sigma_p^2}\right),NL \sigma_p&=0{,}18\end{aligned}",
    "obj": r"\begin{aligned}\max\ &\sum_{i\in A}\big(\alpha_1g_i+\alpha_2r_iNL&\quad+\alpha_3m_i-\alpha_4f_i\big)x_i,NL \alpha&=(1{,}00;\ 0{,}70;\ 0{,}35;\ 0{,}55)\end{aligned}",
    "vent": r"\begin{aligned}h_i&=\frac{\max\!\big(W_{\min},\,\min(\text{tol},\,0{,}85\,g)\big)}{2},NL \text{ventana}_i&=\big[a_i-1{,}15\,h_i,\ a_i+0{,}85\,h_i\big]\end{aligned}",
}
EQ_OV = {k: v.replace("NL", NL) for k, v in EQ_OV.items()}
