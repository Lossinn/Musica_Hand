"""Artículo único del equipo en dos columnas (formato de artículo de proyecto, carta, Times 10 pt).
El texto sale de art_unico.py (misma fuente de verdad); aquí solo se cambia la maquetación,
se retiran los datos sin confirmar y se añade la descripción de la experiencia de uso.
Uso: python -X utf8 ef_equipo.py salida.docx"""
import math, re, sys, json
from pathlib import Path
from ef_comun import *            # noqa: F401,F403  (R, A, FPG, FPV, FPT, RB, LT, MX, f, m, ...)
from ef_nucleo import CLAVES

AQUI = Path(__file__).resolve().parent
SU = json.loads((BASE / "analisis" / "sensibilidad_umbrales.json").read_text(encoding="utf-8"))
QD = json.loads((AQUI / "quintana_demo.json").read_text(encoding="utf-8"))["escenarios"]
LAM, GAM = 0.65, 0.40

fuente = (AQUI / "art_unico.py").read_text(encoding="utf-8")
cab = fuente.split("autores = encabezado(")[0]
ini = cab.index("TITULO_ES = (")
datos_src = cab[ini:]
cuerpo = fuente[fuente.index('H1("Introducción")'):fuente.index("declaraciones(dict(")]

# ---- correcciones de contenido (solo lo no confirmado) y enriquecimiento
datos_src = datos_src.replace("Aprender música con las manos es una práctica antigua, pero llevarla a una aplicación obliga a resolver a la vez",
                              "Enseñar música con las manos no exige instrumento, pero llevarlo a una aplicación obliga a resolver a la vez")
datos_src = datos_src.replace("Learning music with the hands is an old practice, but taking it to an application means solving",
                              "Teaching music with the hands needs no instrument, but taking it to an application means solving")
cuerpo = cuerpo.replace("Desde mediados del siglo XIX se enseña a leer música con las manos: a cada nota de la escala le corresponde una posición, y el niño la ve, la imita y la canta. No pide instrumento ni sala, solo un cuerpo y alguien que corrija. ",
                        "Una manera de enseñar a leer música es asignar a cada nota de la escala una posición de la mano: el niño la ve, la imita y la canta. No pide instrumento ni sala, solo un cuerpo y alguien que corrija. ")
assert "mediados del siglo" not in cuerpo
cuerpo = cuerpo.replace("{c:", "{cite:")

NUEVO = '''H2("Experiencia del niño y de la familia")
T("La aplicación ofrece dos maneras de practicar que conviven. El ejercicio guiado espera, sin límite de tiempo, a que el niño haga la seña correcta antes de pasar a la siguiente, hasta un número fijo de fallos, porque no tiene sentido apurar a un niño de tres años que todavía está formando la mano. Canciones, en cambio, exige llegar a tiempo a cada nota, como en una melodía con pulso. "
  "Las mismas canciones del catálogo se pueden tocar paso a paso desde el mapa de aventura o con nota viajera desde Canciones, y las dos rutas escriben en el mismo registro de intentos, de modo que alimentan el dominio, los logros y el reentrenamiento del predictor sin ninguna ruta especial.")
T("La ayuda visual es la seña de referencia, dibujada a partir de la calibración real del niño, de modo que coincide con lo que el reconocedor espera ver. Para que resulte viva, la mano respira con una leve oscilación de escala, tiene un halo que pulsa y un brillo que recorre las puntas de los dedos. No se usaron ilustraciones externas porque el proyecto no cuenta con un banco de imágenes de gestos. "
  "La mascota es una iguana llamada Kiki, un nombre corto y fácil de pronunciar para un niño de tres años. El sonido de acierto suena una sola vez, al terminar la actividad, mientras que la respuesta visual de cada nota se conserva.")
T("El Modo Libre permite improvisar. Muestra un cronómetro desde la primera nota y un botón de silencio que inserta una pausa audible en la melodía y la dibuja en el pentagrama como un signo de silencio. Las melodías se guardan en un archivo por perfil dentro de la carpeta de datos, con su duración y el intervalo real entre notas. "
  "Una melodía grabada en Modo Libre se puntúa en pantalla (estrellas, puntaje, precisión) pero nunca llega al registro de dominio, por decisión explícita: la improvisación del niño no debe mezclarse con la práctica que el sistema usa para medir lo que sabe. Para los adultos, la Zona de Padres presenta el estado del gemelo digital en su propio registro, y el catálogo de canciones incluye «Martinillo» (nivel 5, 88 bpm).")

'''
cuerpo = cuerpo.replace('H2("Reconocimiento de señas")', NUEVO + 'H2("Reconocimiento de señas")', 1)

cuerpo = cuerpo.replace("[2.6, 7.9, 1.3, 1.4]", "[3.2, 7.4, 1.0, 1.3]").replace("[3.0, 12.0])", "[3.6, 11.4])").replace("[2.0, 3.0, 2.2, 2.4, 5.0]", "[2.2, 3.6, 2.0, 2.4, 4.8]")
cuerpo = cuerpo.replace('figura(["capturas_app.png"], 14.5,', 'figura(["capturas_app.png"], 11.0,')
CODIGO_DATOS = compile(datos_src, "datos", "exec")
CODIGO_CUERPO = compile(cuerpo, "cuerpo", "exec")


EQ_OV = {
 "kappa": r"\begin{aligned}\kappa&=\operatorname{clip}\!\left(\frac{r-0{,}35}{0{,}65},\,0,\,1\right),\ r&=\frac{\lVert p_d-p_a\rVert}{\lVert p_b-p_a\rVert+\lVert p_c-p_b\rVert+\lVert p_d-p_c\rVert}\end{aligned}",
 "dist": r"d(a,b)^2=\frac{1}{\sum_g w_g}\sum_g w_g\,\frac{1}{|g|}\sum_{i\in g}(a_i-b_i)^2",
 "prec": r"\begin{aligned}P_s&=\frac{h_s+\alpha}{n_s+\alpha+\beta},\ \alpha&=1,\ \beta=3\end{aligned}",
 "ret": r"\begin{aligned}R_s&=\exp\!\left(-\frac{\Delta t}{\tau_s}\right),\ \tau_s&=\tau_0\,\varepsilon_s\,(0{,}6+\mathcal{M}_s^{-}),\ \tau_0&=1{,}8\ \text{días}\end{aligned}",
 "sm2": r"\begin{aligned}\varepsilon&\leftarrow\operatorname{clip}\!\big(\varepsilon+0{,}1-(1-q)(0{,}8+(1-q)),\&\qquad 1{,}3,\,2{,}8\big),\ I&\leftarrow\begin{cases}1 & q<0{,}6\ \max(1,I\varepsilon) & \text{en otro caso}\end{cases}\end{aligned}",
 "logit": r"\begin{aligned}p&=\frac{1}{1+e^{-z}},\ z&=w_1\,\mathrm{precision}+w_2\,\mathrm{dificultad}\&\quad+w_3\,\mathrm{dias}+b\end{aligned}",
 "p": r"\begin{aligned}p_i&=\frac{1}{1+e^{-k(\bar\mu_i-\mathrm{dif}_i)}},\ k&=6\end{aligned}",
 "eta": r"\begin{aligned}\eta_i&=\exp\!\left(-\frac{(p_i-p^{*})^2}{2\sigma_p^2}\right),\ \sigma_p&=0{,}18\end{aligned}",
 "obj": r"\begin{aligned}\max\ &\sum_{i\in A}\big(\alpha_1g_i+\alpha_2r_i\&\quad+\alpha_3m_i-\alpha_4f_i\big)x_i,\ \alpha&=(1{,}00;\ 0{,}70;\ 0{,}35;\ 0{,}55)\end{aligned}",
 "vent": r"\begin{aligned}h_i&=\frac{\max\!\big(W_{\min},\,\min(\text{tol},\,0{,}85\,g)\big)}{2},\ \text{ventana}_i&=\big[a_i-1{,}15\,h_i,\ a_i+0{,}85\,h_i\big]\end{aligned}",
}

from ef_eq import EQ_OV  # noqa: E402  (sustituye el bloque anterior)

EQ_REF = {"{E_ACEPT}": "{eq:acepta}", "{E_TEMP}": "{eq:temp}"}


def contenido(e):
    ns = dict(globals())
    exec(CODIGO_DATOS, ns)

    def adapt(t):
        for k, v in EQ_REF.items():
            t = t.replace(k, v)
        return t

    n_t = [0]

    def H1(t): e.sec(t)
    def H2(t, *a): e.sub(t)
    def H3(t): e.sub3(t)
    def T(t): e.P(adapt(t))

    def ecuacion(k, l): e.eq(k, EQ_OV.get(k, l))

    def tabla(titulo, cab_, filas, fuente_, anchos):
        n_t[0] += 1
        cap = re.sub(r"^Tabla \d+\.\s*", "", titulo)
        e.tabla(f"t{n_t[0]}", cap, cab_, filas, anchos, size=8.5 if len(cab_) >= 4 else 9)
        e.nota(fuente_)

    def figura(archivos, ancho, pie):
        cap = re.sub(r"^Figura \d+\.\s*", "", pie)
        ancha = ancho > 8.3 or len(archivos) > 1
        e.figura(f"f{e.n_fig + 1}", archivos, cap, ancho if ancha else min(ancho, 8.3), ancha=ancha)

    def resto(frase):
        faltan = [k for k in list(CLAVES) + ["dane"] if k not in e.citadas]
        if faltan:
            e.P(frase + " {cite:" + ",".join(faltan) + "}.")

    ns.update(dict(H1=H1, H2=H2, H3=H3, T=T, ecuacion=ecuacion, tabla=tabla, figura=figura, resto=resto, SU=SU, QD=QD, LAM=LAM, GAM=GAM, math=math, adapt=adapt))
    # f-strings del cuerpo usan {{E_TEMP}}; T() ya traduce las marcas
    titulos = [ns["TITULO_ES"], ns["TITULO_EN"]]
    autores = ["Antolin De Jesús Vitola-Montes, Isaías José Petro-Rodríguez", "Andrés Julián Negrete-Pacheco, Juliana Esther Carrascal-Hernández",
               "Angel Quintana-Jiménez, Alejandro Pemberty-Vergara", "Juan Diego Guerra-Gómez, Cristian Javier Cano-Mogollón"]
    afil = ["Universidad Pontificia Bolivariana, Seccional Montería, Córdoba, Colombia · Asignatura Gestión Tecnológica",
            "Cristian Javier Cano-Mogollón: Docente Titular, Facultad de Ingeniería Industrial; Grupo de Investigación en Simulación, Logística y Gestión de Operaciones (SILOGE); Hub Industrial Solution (HIS) · cristian.cano@upb.edu.co"]
    e.titulo_bloque(titulos, autores, afil, ns["RES_ES"], ns["KW_ES"], ns["RES_EN"], ns["KW_EN"])
    exec(CODIGO_CUERPO, ns)

    e.sec_sin_numero("Declaraciones")
    e.P("**Ética y consentimiento.** No se recolectaron datos de niños: la calibración de referencia contiene únicamente coordenadas de puntos de la mano de una persona, sin imágenes. El estudio es una evaluación técnica de laboratorio; una prueba con niños requerirá aprobación ética y consentimiento informado de los acudientes.", sangria=False)
    e.P("**Datos y código.** El código, la calibración de referencia, las pruebas y los scripts de evaluación forman parte del proyecto del equipo. Las salidas de las mediciones (resultados_vision.json, sensibilidad_umbrales.json), el corpus bibliográfico y la verificación de referencias se entregan junto con este artículo.", sangria=False)
    e.P("**Uso de herramientas de inteligencia artificial.** Se utilizó un asistente de inteligencia artificial (Claude, de Anthropic) para apoyar el análisis del código, la ejecución y documentación de las mediciones, la verificación de referencias y la redacción de borradores. Los autores revisaron el contenido y asumen la responsabilidad del texto y de los resultados.", sangria=False)
    e.referencias()


if __name__ == "__main__":
    ruta = Path(sys.argv[1]); ruta.parent.mkdir(parents=True, exist_ok=True)
    e = construir(contenido, ruta)
    print("guardado", ruta.name, "| tablas", e.n_tab, "| figuras", e.n_fig, "| ecuaciones", e.n_eq, "| refs", len(set(e.citadas)))
