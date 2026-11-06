"""Escrito final — Angel Quintana: optimización (la sesión como programación entera mixta)."""
import json
from ef_comun import *

D = json.loads((BASE / "generador" / "quintana_demo.json").read_text(encoding="utf-8"))
ESC = D["escenarios"]


def contenido(e):
    resumen = ("Después de cada intento, una aplicación de enseñanza debe decidir qué actividades componen la siguiente sesión, con un tiempo limitado y sin repetir lo mismo. Este trabajo formula esa decisión en Hand Sing Kids, que enseña las ocho notas de Do3 a Do4 con señas de las manos, "
               "como un problema de programación entera mixta: se maximiza una combinación de ganancia de aprendizaje, urgencia de repaso y motivación, menos la fatiga inducida, sujeta a restricciones de tiempo, tamaño de la sesión, prerrequisitos, una actividad lúdica como mínimo, dificultad media acotada, "
               "un máximo de dos actividades por habilidad y un repaso vencido. El problema se resuelve con CBC mediante PuLP y se verifica con enumeración exhaustiva mientras el número de combinaciones no supere 4×10^5; la prueba del repositorio pasó y la sesión de ejemplo se resolvió en 40 ms con valor objetivo 2,9524. "
               "Para estudiar la sensibilidad de la formulación se resolvió de forma exacta una instancia ilustrativa de 12 actividades construida para este trabajo: la sesión óptima fue estable ante cambios en los pesos del repaso y de la fatiga, cambió al duplicar el peso de la ganancia y se volvió infactible con un tiempo máximo de 16 minutos. "
               "Los pesos y las restricciones son decisiones de diseño, no se calibraron con datos de niños, y el beneficio pedagógico de la sesión óptima es una hipótesis. El nivel de madurez es TRL 4.")
    abstract = ("After each attempt, a teaching application must decide which activities make up the next session, with limited time and without repeating the same thing. This paper formulates that decision in Hand Sing Kids, which teaches the eight notes from C3 to C4 with hand signs, as a mixed-integer program: "
                "a combination of learning gain, review urgency and motivation, minus induced fatigue, is maximized subject to time, session size, prerequisites, at least one playful activity, bounded mean difficulty, at most two activities per skill and one overdue review. "
                "The problem is solved with CBC through PuLP and verified by exhaustive enumeration while the number of combinations does not exceed 4×10^5; the repository test passed and the example session was solved in 40 ms with objective value 2.9524. "
                "To study the sensitivity of the formulation, an illustrative 12-activity instance built for this paper was solved exactly: the optimal session was stable to changes in the review and fatigue weights, changed when the gain weight was doubled and became infeasible with a 16-minute time limit. "
                "Weights and constraints are design decisions, not calibrated with children's data, and the pedagogical benefit of the optimal session is a hypothesis. The readiness level is TRL 4.")
    titulo(e, "Quintana", "Elegir la sesión óptima: programación entera mixta para planificar las actividades de Hand Sing Kids", resumen,
           "programación entera mixta; optimización; planificación de sesiones; análisis de sensibilidad; educación musical infantil.", abstract,
           "mixed-integer programming; optimization; session planning; sensitivity analysis; children's music education.")

    e.sec("Introducción")
    e.P("Planificar una sesión de práctica parece sencillo hasta que se escriben las condiciones. Hay un tiempo máximo y un número fijo de actividades; algunas actividades exigen haber dominado antes una habilidad; no conviene que la sesión sea toda de actividades difíciles ni que repita tres veces la misma nota; debería incluir algo lúdico y, "
        "si hay un repaso vencido, atenderlo. Escoger a mano entre decenas de actividades con todas esas reglas es lo que la investigación de operaciones llama un problema de optimización con restricciones, y una regla simple, como elegir las actividades más rentables una por una, puede violar alguna de ellas o perder una combinación mejor.")
    e.P("En la literatura reciente de educación musical con inteligencia artificial, la planificación suele resolverse con aprendizaje por refuerzo o con redes profundas {cite:li_hong,li_peerj,tang,wang}, que aprenden la política a partir de datos. Hay también trabajos que generan material según la dificultad {cite:ramoneda} y que se apoyan en la práctica distribuida y la repetición espaciada {cite:wozniak}. "
        "En Hand Sing Kids no hay datos de niños y sí reglas pedagógicas explícitas; por eso se prefirió una formulación que el docente pueda leer y cuyo óptimo se pueda comprobar. La dificultad se concentra en un éxito esperado intermedio, coherente con la idea de que el aprendizaje es más eficiente cuando el error ni es muy raro ni muy frecuente {cite:wilson85}.")
    e.P("El objetivo es formular la selección de la sesión como un problema de programación entera mixta, mostrar cómo se verifica su óptimo, estudiar su sensibilidad con una instancia ilustrativa y declarar qué parámetros son decisiones de diseño y no datos.")

    e.sec("Contexto general")
    e.P("El optimizador pertenece a la capa pedagógica. Recibe del modelo de dominio el valor estimado de cada habilidad y la urgencia de repaso, y del catálogo las actividades candidatas, con su duración, su dificultad, las habilidades que tocan y su tipo. No necesita saber cómo se estimó el dominio. "
        "La salida es el conjunto de actividades que forman la sesión.")
    e.sub("Supuestos y alcance")
    e.B(["Los pesos, el éxito esperado de 0,75 y la dificultad media máxima de 0,72 son **decisiones de diseño**.",
         "El estudio de sensibilidad usa una **instancia ilustrativa de 12 actividades construida para este trabajo**; no es el catálogo de la aplicación ni contiene datos de niños.",
         "La verificación del repositorio cubre una sesión de ejemplo, no un barrido de casos.",
         "El tiempo de 40 ms corresponde a una ejecución en un equipo.",
         "«Óptimo» se entiende en sentido matemático: mejor valor del objetivo que cumple las restricciones."])

    e.sec("Modelo matemático")
    e.sub("Conjuntos, parámetros y variables")
    e.tabla("conj", "Conjuntos del modelo.", ["Conjunto", "Descripción"],
            [["$A$", "Actividades candidatas, indexadas por $i$."], ["$S$", "Habilidades (las ocho notas), indexadas por $s$."], ["$S_i\\subseteq S$", "Habilidades que toca la actividad $i$."],
             ["$G\\subseteq A$", "Actividades lúdicas."], ["$V\\subseteq A$", "Actividades que atienden un repaso vencido."]], [2.4, 6.1])
    e.tabla("par", "Parámetros y variable de decisión.", ["Símbolo", "Descripción"],
            [["$d_i$", "Duración de la actividad $i$ (min)."], ["$\\mathrm{dif}_i$", "Dificultad, en $[0,1]$."], ["$a_i$", "1 si los prerrequisitos están cumplidos."], ["$T_{\\max},\\ K$", "Tiempo máximo y número de actividades."],
             ["$g_i,\\ r_i,\\ m_i,\\ f_i$", "Ganancia, urgencia de repaso, motivación y fatiga."], ["$\\alpha_1,\\dots,\\alpha_4$", "Pesos del objetivo: 1,00; 0,70; 0,35; 0,55."], ["$x_i\\in\\{0,1\\}$", "Vale 1 si la actividad $i$ entra en la sesión."]], [2.8, 5.7])
    e.sub("Función objetivo")
    e.P("La probabilidad de éxito de una actividad se estima con una logística sobre la holgura entre el dominio medio $\\bar\\mu_i$ y la dificultad, y el factor $\\eta_i$ concentra el valor en una probabilidad de éxito $p^{*}=0{,}75$ ({fig:fun}):")
    e.eq("p", r"p_i=\frac{1}{1+e^{-k(\bar\mu_i-\mathrm{dif}_i)}},\quad k=6;\qquad \eta_i=\exp\!\left(-\frac{(p_i-p^{*})^2}{2\sigma_p^2}\right),\quad \sigma_p=0{,}18")
    e.figura("fun", "sesion_funciones.png", "Éxito esperado $p_i$ y factor $\\eta_i$ según la holgura entre dominio medio y dificultad (curvas calculadas con las ecuaciones del modelo).", 8.2)
    e.P("Con la ganancia $g_i=\\eta_i\\sum_{s\\in S_i}(1-\\mu_s)/\\sqrt{|S_i|}$ y la fatiga $f_i=(d_i/D)(0{,}5+\\mathrm{dif}_i)$, el problema es:")
    e.eq("obj", r"\max\ \sum_{i\in A}\big(\alpha_1g_i+\alpha_2r_i+\alpha_3m_i-\alpha_4f_i\big)\,x_i")
    e.sub("Restricciones")
    e.eq("res", r"\begin{aligned}&\sum_i d_ix_i\le T_{\max},\qquad \sum_i x_i=K,\qquad x_i\le a_i,\qquad \sum_{i\in G}x_i\ge1,\\ &\sum_i\mathrm{dif}_ix_i\le0{,}72K,\qquad \sum_{i:\,s\in S_i}x_i\le2\ \ \forall s\in S,\qquad \sum_{i\in V}x_i\ge1\end{aligned}")
    e.P("Las restricciones fijan el tiempo total, el tamaño de la sesión, los prerrequisitos, al menos una actividad lúdica, una dificultad media acotada, un máximo de dos actividades por habilidad y la inclusión de un repaso vencido si existe. El problema se resuelve con el solucionador CBC mediante PuLP y, "
        "si este no está disponible, por enumeración exhaustiva mientras $\\binom{|A|}{K}\\le 4\\times10^{5}$, lo que entrega el óptimo exacto.")

    e.sec("Descripción de datos y análisis de resultados")
    e.sub("Verificación en el repositorio")
    e.P("La batería del optimizador del repositorio terminó con código de salida 0, ejecutada en un solo equipo con Windows 11, Python 3.12.10 y PuLP 2.9.0. La prueba que compara el resultado del solucionador con la enumeración exacta pasó, y la sesión de ejemplo se resolvió con CBC en 40 ms con un valor objetivo de 2,9524. "
        "Ese tiempo es compatible con recalcular la sesión tras cada intento en un computador común, aunque no se midió con catálogos grandes ni en un equipo de aula.")
    e.sub("Instancia ilustrativa")
    e.P("Para estudiar la sensibilidad, que el repositorio no cubre, se construyó una instancia ilustrativa con 12 actividades, dominio estimado decreciente entre el Do (0,90) y el Do agudo (0,05) y urgencia de repaso en el Do y el Re, con $K=4$, $T_{\\max}=30$ min y la dificultad media máxima de 0,72. "
        "Se resolvió por enumeración exhaustiva de las $\\binom{12}{4}=495$ combinaciones; de ellas, 180 son factibles. Es una instancia de juguete que permite ver el comportamiento del modelo, no una predicción sobre la aplicación real.")
    cat = D["catalogo"]
    e.tabla("cat", "Instancia ilustrativa: actividades candidatas.", ["N.º", "Actividad", "min", "Dif.", "Habilidades"],
            [[str(a["i"]), a["nombre"], str(a["d"]), f(a["dif"], 2), ", ".join(a["hab"])] for a in cat], [0.8, 3.2, 0.8, 0.9, 3.6], size=8)
    b = ESC["Base"]
    e.P(f"La sesión óptima del caso base está formada por las actividades {', '.join(str(i) for i in b['sesion'])} ({'; '.join(b['nombres'])}), dura {b['minutos']} minutos y tiene un valor objetivo de {f(b['obj'], 4)}. Incluye las dos habilidades con repaso vencido y una actividad lúdica, y no toca más de dos veces ninguna habilidad.")
    e.sub("Análisis de sensibilidad")
    nombres_esc = ["Base", "Peso del repaso ×2", "Peso de la fatiga ×2", "Peso de la ganancia ×2", "Dificultad media máxima 0,50", "Sesión de K = 3", "Sesión de K = 5", "Sin exigir actividad lúdica", "Niño más avanzado (+0,2)", "Tiempo máximo 16 min"]
    filas = []
    for n in nombres_esc:
        r = ESC[n]
        if r.get("factible") == 0:
            filas.append([n, "Infactible", "—", "—"])
        else:
            filas.append([n, f(r["obj"], 3), ",".join(str(i) for i in r["sesion"]), str(r["factibles"])])
    e.tabla("sens", "Sensibilidad de la sesión óptima en la instancia ilustrativa.", ["Escenario", "Objetivo", "Sesión", "Factibles"], filas, [3.9, 1.5, 1.8, 1.3], alinear=["l", "r", "l", "r"], size=8)
    e.P("Tres hallazgos se desprenden del análisis. En primer lugar, la sesión es estable ante los pesos del repaso y de la fatiga: al duplicarlos cambia el valor del objetivo, pero no las actividades elegidas. Solo al duplicar el peso de la ganancia la sesión pasa a {3, 6, 9, 11}, que tiene más actividades de dificultad media y alta. "
        "En segundo lugar, las restricciones de tiempo pueden hacer el problema infactible: con 16 minutos no existe una sesión de cuatro actividades que cumpla todas las reglas, porque la combinación factible más corta dura 17 minutos. Un sistema real debería detectar esa situación y relajar una restricción, por ejemplo reducir $K$. "
        "En tercer lugar, algunas restricciones no ligan: la exigencia de una actividad lúdica no cambió la solución, porque la óptima ya la incluía, y bajar la dificultad media máxima a 0,50 solo redujo el número de combinaciones factibles de 180 a 81. Con un niño más avanzado, la sesión cambia una actividad.")
    e.sub("Qué significa «óptimo»")
    e.P("La enumeración exacta garantiza que ninguna otra combinación factible tiene mayor valor del objetivo. No garantiza que esa sesión sea la mejor para aprender: el objetivo es un modelo de lo que el equipo cree que importa, con pesos elegidos por diseño. Solo un piloto con niños puede decir si las sesiones óptimas producen mejor aprendizaje que las elegidas por un docente.")

    e.sec("Conclusiones")
    e.P("La selección de la sesión se formula como un problema de programación entera mixta con restricciones pedagógicas explícitas, se resuelve con CBC y se verifica con enumeración exacta. La prueba del repositorio pasó y la sesión de ejemplo se resolvió en 40 ms. El estudio de sensibilidad con una instancia ilustrativa mostró estabilidad ante los pesos del repaso y de la fatiga, "
        "sensibilidad al peso de la ganancia y una condición de infactibilidad por tiempo que el sistema debe manejar.")
    e.P("Los pesos y las restricciones son de diseño; el beneficio pedagógico de la sesión óptima es una hipótesis. Como líneas de trabajo se identifican cuatro: repetir el estudio de sensibilidad con el catálogo real y un barrido de casos; probar el tiempo de solución con catálogos mayores y en un equipo de aula; comparar en un piloto sesiones óptimas con sesiones elegidas por un docente; "
        "y mostrar al docente la explicación de cada actividad elegida. El nivel de madurez es TRL 4.")
    e.referencias()


if __name__ == "__main__":
    correr(contenido)
