"""Escrito final — Juliana Carrascal: aprendizaje adaptativo (del intento al dominio y al repaso)."""
import math
from ef_comun import *

LAM, GAM = 0.65, 0.40


def factor(R):
    return LAM + (1 - LAM) * R ** GAM


def contenido(e):
    resumen = ("Una secuencia fija de ejercicios trata igual a todos los niños: repite lo que uno ya domina y adelanta lo que otro aún no ha aprendido. Este trabajo presenta el modelo de aprendizaje de Hand Sing Kids, una aplicación que enseña las ocho notas de Do3 a Do4 "
               "con señas de las manos. Después de cada intento, el sistema actualiza una estimación del dominio de la nota que combina precisión, consistencia, velocidad y retención, esta última con decaimiento exponencial por los días sin practicar; programa los repasos "
               "con una adaptación del esquema SM-2 a una calidad continua; y, cuando el niño acumula 40 intentos, sustituye la fórmula fija por un predictor logístico de tres variables. Una nota pasa a dominada con un valor de 0,80 y al menos seis intentos y retrocede si baja de 0,70. "
               "Un análisis de sensibilidad de la fórmula muestra que, por la forma en que la retención multiplica al desempeño, una nota con desempeño de 0,95 deja de estar dominada cuando la retención cae por debajo de aproximadamente 0,22 y retrocede cuando cae por debajo de 0,03. "
               "Las pruebas del dominio y del predictor del repositorio pasaron; el predictor alcanza 78 % sobre sus propios datos de entrenamiento, lo que solo comprueba que el ajuste converge. No hay datos de niños: las constantes son de diseño y el efecto sobre el aprendizaje "
               "es una hipótesis. El nivel de madurez es TRL 4.")
    abstract = ("A fixed exercise sequence treats all children alike: it repeats what one child already masters and moves ahead on what another has not yet learned. This paper presents the learning model of Hand Sing Kids, an application that teaches the eight notes from C3 to C4 with hand signs. "
                "After each attempt, the system updates a mastery estimate that combines accuracy, consistency, speed and retention, the latter decaying exponentially with days without practice; schedules reviews with an adaptation of the SM-2 scheme to a continuous quality; "
                "and, once the child has 40 attempts, replaces the fixed formula with a three-variable logistic predictor. A note becomes mastered at 0.80 with at least six attempts and falls back below 0.70. A sensitivity analysis of the formula shows that, because retention multiplies performance, "
                "a note with performance 0.95 stops being mastered when retention falls below about 0.22 and falls back when it drops below 0.03. The mastery and predictor test suites passed; the predictor reaches 78 % on its own training data, which only checks that the fit converges. "
                "There are no data from children: the constants are design decisions and the effect on learning is a hypothesis. The readiness level is TRL 4.")
    titulo(e, "Carrascal", "Del intento al dominio: estimación del aprendizaje y repaso espaciado en Hand Sing Kids", resumen,
           "aprendizaje adaptativo; seguimiento del conocimiento; repaso espaciado; dominio de habilidades; educación musical infantil.", abstract,
           "adaptive learning; knowledge tracing; spaced repetition; skill mastery; children's music education.")

    e.sec("Introducción")
    e.P("Aprender las notas con las manos exige repetir, pero no cualquier repetición sirve. Un niño que ya domina el Do y el Re necesita avanzar hacia el Mi; otro que confunde el Fa con el Sol necesita volver sobre ellos. Una aplicación que ofrece siempre la misma secuencia ignora esa diferencia. "
        "Para adaptarse, el sistema tiene que responder tres preguntas después de cada intento: qué sabe el niño de cada nota, cuándo conviene volver a una nota ya aprendida y qué actividades armar para la siguiente sesión.")
    e.P("Las dos primeras preguntas tienen una larga historia en los sistemas de tutoría. El seguimiento del conocimiento estima el dominio de una habilidad como una variable oculta a partir de los aciertos y fallos observados {cite:corbett}. En paralelo, la investigación sobre práctica distribuida muestra que espaciar los repasos "
        "mejora la retención frente a concentrarlos {cite:cepeda}, y los algoritmos de repetición espaciada programan el siguiente repaso según la calidad de la respuesta anterior {cite:wozniak}. Una idea complementaria sostiene que el aprendizaje es más eficiente cuando la dificultad deja una tasa de error intermedia {cite:wilson85}.")
    e.P("En la educación musical con inteligencia artificial, la personalización suele abordarse con aprendizaje por refuerzo o profundo para trazar rutas de estudio {cite:li_hong,li_disc}, o con sistemas que consideran el estado afectivo del estudiante {cite:deng_sci,shi}. Entre los títulos revisados no apareció uno que combine un modelo de dominio por habilidad, repaso espaciado "
        "y una entrada por seña manual; no se leyeron los textos completos. El objetivo de este trabajo es describir con precisión el modelo de aprendizaje de Hand Sing Kids, analizar su comportamiento con la fórmula del código, declarar qué se verificó y qué no, y plantear las hipótesis que un piloto con niños debería poner a prueba.")

    e.sec("Contexto general")
    e.P("La capa pedagógica de Hand Sing Kids recibe de la capa perceptiva una nota confirmada y el tiempo que el niño tardó en producirla, y devuelve la actualización del dominio y la sesión siguiente. Cada intento se registra en una base local con la fecha, la nota, el resultado y el tiempo. "
        "Una habilidad corresponde a una nota; las actividades tocan una o varias habilidades.")
    e.sub("Supuestos y alcance")
    e.B(["Ninguna de las constantes del modelo proviene de datos de niños: son decisiones de diseño o ajustes apoyados en la literatura.",
         "El análisis de la fórmula es **determinista y analítico**: se calcula con las ecuaciones del código y no con intentos reales.",
         "La prueba del predictor se hizo sobre sus propios datos de entrenamiento; solo comprueba que el ajuste converge.",
         "Se adopta el valor del código cuando hay diferencia con la documentación.",
         "No se evalúa la selección de la sesión por optimización, que es objeto de otro trabajo."])

    e.sec("Modelo de aprendizaje")
    e.sub("Conjuntos, parámetros y variables")
    e.tabla("conj", "Elementos del modelo de dominio.", ["Símbolo", "Descripción"],
            [["$s\\in S$", "Habilidad (una por cada una de las ocho notas)."], ["$n_s,\\ h_s$", "Intentos y aciertos en la habilidad $s$."], ["$P_s,\\ C_s,\\ V_s$", "Precisión, consistencia y velocidad, en $[0,1]$."],
             ["$R_s$", "Retención, en $(0,1]$."], ["$\\Delta t$", "Días desde la última práctica."], ["$q$", "Calidad de una respuesta, en $[0,1]$."], ["$\\varepsilon_s,\\ I_s$", "Factor de facilidad e intervalo de repaso."], ["$\\mathcal{M}_s$", "Dominio estimado, en $[0,1]$."]],
            [2.2, 6.3])
    e.sub("Dominio de una habilidad")
    e.P("El dominio combina desempeño y retención. La retención multiplica y no suma, de modo que el desuso prolongado degrada la habilidad, mientras que $\\lambda$ evita que se desplome a cero:")
    e.eq("mastery", r"\mathcal{M}_s=\big(\lambda+(1-\lambda)R_s^{\gamma}\big)\big(w_pP_s+w_cC_s+w_vV_s\big)")
    e.P("con $w_p=0{,}55$, $w_c=0{,}25$, $w_v=0{,}20$, $\\lambda=0{,}65$ y $\\gamma=0{,}40$. La precisión se suaviza con una distribución a priori, la consistencia penaliza alternar aciertos y fallos en los últimos 8 intentos, la velocidad se mide contra un tiempo de referencia por franja de edad y la retención decae de forma exponencial:")
    e.eq("prec", r"P_s=\frac{h_s+\alpha}{n_s+\alpha+\beta},\qquad \alpha=1,\ \beta=3")
    e.eq("ret", r"R_s=\exp\!\left(-\frac{\Delta t}{\tau_s}\right)")
    e.eq("tau", r"\tau_s=\tau_0\,\varepsilon_s\,(0{,}6+\mathcal{M}_s^{-}),\qquad \tau_0=1{,}8\ \text{días}")
    e.P("Aquí $\\mathcal{M}_s^{-}$ es el dominio de la actualización anterior, que evita una definición circular. Una habilidad pasa a dominada con $\\mathcal{M}_s\\ge 0{,}80$ y al menos seis intentos, y retrocede si cae por debajo de 0,70.")
    e.sub("Repaso espaciado y predictor")
    e.P("El repaso adapta el esquema SM-2 {cite:wozniak} a una calidad continua $q$, con efecto de la práctica distribuida documentado en la literatura {cite:cepeda}:")
    e.eq("sm2", r"\varepsilon\leftarrow\operatorname{clip}\big(\varepsilon+0{,}1-(1-q)(0{,}8+(1-q)),\,1{,}3,\,2{,}8\big)")
    e.eq("int", r"I\leftarrow\begin{cases}1 & q<0{,}6\\ \max(1,I\varepsilon) & \text{en otro caso}\end{cases}")
    e.P("Cuando el niño acumula 40 intentos propios, un predictor logístico de tres variables sustituye a la fórmula fija y se reentrena cada 20 intentos nuevos, con 300 épocas de descenso de gradiente y tasa 0,35 sobre variables estandarizadas $x_1$ (precisión), $x_2$ (dificultad de la actividad) y $x_3$ (días desde la última práctica), minimizando la entropía cruzada:")
    e.eq("logit", r"p=\frac{1}{1+e^{-z}},\qquad z=w_1\,x_1+w_2\,x_2+w_3\,x_3+b")
    e.eq("loss", r"\mathcal{L}=-\frac{1}{N}\sum_{n=1}^{N}\big[y_n\ln p_n+(1-y_n)\ln(1-p_n)\big]")

    e.sec("Descripción de datos y análisis de resultados")
    e.sub("Qué se usó y qué se verificó")
    e.P("No se usaron datos de niños. El análisis emplea las ecuaciones y constantes del código y las pruebas del repositorio, ejecutadas en un solo equipo con Windows 11 y Python 3.12.10. Las baterías de prueba del dominio y del predictor, dos de las ocho del repositorio, terminaron sin fallos. "
        "La prueba unitaria del predictor mejora la predicción al azar sobre sus propios datos de entrenamiento, con 78 % de acierto; esa cifra solo comprueba que el descenso de gradiente converge y no mide capacidad predictiva.")
    e.sub("Sensibilidad del dominio a la retención")
    e.P("Como la retención multiplica al desempeño, hay un límite al dominio que cualquier nota puede mantener sin practicarse. Con $S=w_pP+w_cC+w_vV$ el desempeño combinado, el dominio es $\\mathcal{M}=S\\,[\\lambda+(1-\\lambda)R^{\\gamma}]$ y el factor entre corchetes vale 1 con $R=1$ y 0,65 en el límite $R\\to 0$. "
        "El cuadro siguiente muestra el dominio para tres niveles de desempeño y varios valores de retención.")
    Rs = (1.0, 0.8, 0.5, 0.2, 0.05)
    filas = []
    for r in Rs:
        fila = [f(r, 2)]
        for S in (0.95, 0.90, 0.85):
            M = S * factor(r)
            fila.append(f"{f(M, 3)}" + (" ✓" if M >= 0.80 else (" ↓" if M < 0.70 else "")))
        filas.append(fila)
    e.tabla("sens", "Dominio $\\mathcal{M}$ según la retención $R$ y el desempeño combinado $S$ (✓: dominada, $\\ge 0{,}80$; ↓: retrocede, $<0{,}70$).", ["$R$", "$S=0{,}95$", "$S=0{,}90$", "$S=0{,}85$"], filas, [1.2, 2.2, 2.2, 2.2], alinear=["r"] * 4)
    # umbrales
    def r_umbral(S, objetivo):
        fac = objetivo / S
        if fac <= LAM:
            return 0.0
        if fac > 1:
            return None
        return ((fac - LAM) / (1 - LAM)) ** (1 / GAM)
    r_dom = {S: r_umbral(S, 0.80) for S in (0.95, 0.90, 0.85)}
    r_ret = {S: r_umbral(S, 0.70) for S in (0.95, 0.90, 0.85)}
    e.P(f"Con $S=0{{,}}95$, la nota deja de estar dominada cuando $R$ baja de {f(r_dom[0.95], 2)} y retrocede cuando baja de {f(r_ret[0.95], 3)}; con $S=0{{,}}90$, los umbrales son {f(r_dom[0.90], 2)} y {f(r_ret[0.90], 2)}; y con $S=0{{,}}85$, {f(r_dom[0.85], 2)} y {f(r_ret[0.85], 2)} ({{fig:dom}}). "
        "Cuanto menor es el desempeño combinado, más alta debe mantenerse la retención para conservar el dominio, y con $S\le 0{,}80$ la nota no puede ser dominada ni con retención perfecta.")
    e.figura("dom", "dominio_retencion.png", "Dominio según la retención para tres niveles de desempeño combinado $S$ (curvas calculadas con la ecuación del dominio; no son datos de niños).", 8.3)
    e.sub("Tiempo hasta que una nota retrocede")
    taus = []
    for eps in (1.3, 2.8):
        tau = 1.8 * eps * (0.6 + 0.9)
        taus.append((eps, tau, -tau * math.log(r_ret[0.95]) if r_ret[0.95] else None, -tau * math.log(r_dom[0.95])))
    e.P(f"El tiempo en días depende de $\\tau_s=\\tau_0\\,\\varepsilon_s\\,(0{{,}}6+\\mathcal{{M}}_s^{{-}})$. Para una nota con $S=0{{,}}95$ y dominio previo de 0,90, con el factor de facilidad en sus extremos permitidos (1,3 y 2,8), $\\tau_s$ vale {f(taus[0][1], 1)} y {f(taus[1][1], 1)} días: "
        f"la nota deja de estar dominada tras unos {f(taus[0][3], 1)} a {f(taus[1][3], 1)} días sin practicar y retrocede tras unos {f(taus[0][2], 0)} a {f(taus[1][2], 0)} días. Son valores de la fórmula con supuestos explícitos, no observaciones, y muestran por qué un repaso programado con $\\varepsilon$ alto llega tarde si el niño olvida rápido.")
    e.sub("Limitaciones de la verificación")
    e.P("Las pruebas verifican que la fórmula se comporta como se diseñó, por ejemplo que el desuso degrade la retención sin llevarla a cero, y no que refleje cómo aprende un niño. Ninguna constante proviene de datos de niños; el cuadro de parámetros del modelo es, por eso, una lista de hipótesis de diseño.")
    e.tabla("hipo", "Hipótesis para un piloto y evidencia necesaria.", ["Hipótesis", "Evidencia necesaria"],
            [["H1: una secuencia adaptada produce mejor retención a una semana que una fija", "Dos grupos de niños, medición a una semana"], ["H2: el predictor mejora al estimador fijo tras 40 intentos", "Registros de intentos y error de predicción en datos nuevos"],
             ["H3: los repasos programados coinciden con lo que el niño olvida", "Fechas de práctica y fallos posteriores"]], [4.8, 3.7])

    e.sub("Trazabilidad de las cifras")
    e.P("Cada cifra de este trabajo puede rastrearse hasta el script, el archivo o el cálculo que la produce, como se resume en el cuadro siguiente.")
    e.tabla("traza", "Origen de las cifras principales.", ["Cifra", "Origen"], [['Constantes del dominio y del repaso', 'Código del repositorio (módulos de dominio y repaso)'], ['78 % del predictor', 'Prueba unitaria del predictor (salida_pruebas.txt)'], ['Dominio según $R$ y $S$', 'Cálculo con la ecuación del dominio (este documento)'], ['Umbrales de retención y días', 'Cálculo con supuestos explícitos (este documento)'], ['Baterías de dominio y predictor', 'salida_pruebas.txt']], [3.4, 5.1], size=8)

    e.sec("Conclusiones")
    e.P("Hand Sing Kids estima el dominio de cada nota con cuatro componentes, programa repasos con repetición espaciada y reemplaza la fórmula fija por un predictor desde los 40 intentos. El análisis de la fórmula muestra un límite estructural: al multiplicar la retención por el desempeño, una nota solo puede ser dominada si su desempeño combinado supera 0,80, "
        "y retrocede cuando la retención cae muy por debajo del umbral, lo que depende de $\\tau_s$ y, por tanto, del factor de facilidad.")
    e.P("Las pruebas del repositorio verifican que el modelo se comporta como se diseñó. No hay datos de niños y las constantes son de diseño, de modo que el efecto sobre el aprendizaje es una hipótesis. Como líneas de trabajo se identifican cuatro: registrar los intentos en un piloto y reajustar las constantes; comparar una secuencia adaptada con una fija en retención a una semana; "
        "mostrar al docente qué modelo decide y por qué; y medir el sobreajuste del predictor con datos nuevos. El nivel de madurez es TRL 4.")
    e.referencias()


if __name__ == "__main__":
    correr(contenido)
