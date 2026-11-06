"""Escrito final — Antolin Vitola: acceso y valor pedagógico (las manos como instrumento)."""
import math
from ef_comun import *


def n_grupo(d, alfa_z=1.959964, pot_z=0.841621):
    return 2 * ((alfa_z + pot_z) / d) ** 2


def contenido(e):
    resumen = ("Enseñar música exige instrumentos, espacios y docentes que no siempre están disponibles. Hand Sing Kids propone usar las manos, como lo hacía la enseñanza con señas manuales del siglo XIX, y una cámara que reconoce ocho señas, una por cada nota de Do3 a Do4, "
               "para que el niño reciba una respuesta inmediata sin necesidad de un instrumento. Este trabajo presenta la propuesta desde su pertinencia pedagógica y su viabilidad técnica en Montería y Córdoba, donde el DANE proyecta para 2026 una población de 535.052 habitantes, "
               "80.254 de ellos entre 3 y 12 años. La aplicación corre en un computador con cámara, guarda sus datos en una base local y no necesita conexión a internet. Se relaciona cada función de un docente de música con el componente que la imita y con la evidencia que la respalda; "
               "en laboratorio, con una calibración de una persona y perturbaciones simuladas, el sistema reconoció las 480 señas sin ruido y evitó notas falsas en la mayoría de 640 posturas que no son seña "
               f"({f(FPG['pct'])} % de errores frente a 100 % del método inicial). No hubo pruebas con niños. Se formulan tres hipótesis de impacto y un plan de piloto con tamaños de muestra aproximados; el nivel de madurez es TRL 4.")
    abstract = ("Teaching music requires instruments, spaces and teachers that are not always available. Hand Sing Kids proposes using the hands, as nineteenth-century hand-sign teaching did, and a camera that recognizes eight signs, one for each note from C3 to C4, "
                "so that the child receives immediate feedback without an instrument. This paper presents the proposal from its pedagogical relevance and technical feasibility in Montería and Córdoba, where DANE projects a 2026 population of 535,052, 80,254 of whom are between 3 and 12 years old. "
                "The application runs on a computer with a camera, stores its data locally and needs no internet connection. Each function of a music teacher is related to the component that imitates it and to the evidence supporting it; in the laboratory, with a single-person calibration and simulated perturbations, "
                f"the system recognized all 480 signs without noise and avoided false notes in most of 640 non-sign postures ({f(FPG['pct'])} % errors against 100 % for the initial method). No tests with children were done. Three impact hypotheses and a pilot plan with approximate sample sizes are stated; the readiness level is TRL 4.")
    titulo(e, "Vitola", "Las manos como instrumento: una herramienta digital de bajo requerimiento para enseñar las notas musicales a niños en Montería y Córdoba", resumen,
           "educación musical infantil; enseñanza con señas manuales; acceso a instrumentos; tecnología accesible; Montería.", abstract,
           "children's music education; hand-sign teaching; access to instruments; accessible technology; Montería.")

    e.sec("Introducción")
    e.P("Desde mediados del siglo XIX, John Curwen popularizó en el Reino Unido un sistema de señas manuales para las notas de la escala, que más tarde se difundió en la enseñanza musical infantil. La idea es simple: cada nota tiene una posición de la mano, y el niño la ve, la hace y la canta. "
        "Su fortaleza pedagógica es que no necesita ningún instrumento, solo un cuerpo y alguien que corrija. Su debilidad es esa misma: sin un docente atento, la seña se hace de cualquier manera y nadie le dice al niño si acertó.")
    e.P("Hoy una cámara y un modelo de seguimiento de manos {cite:mediapipe} pueden cumplir el papel de quien corrige. Las revisiones sobre inteligencia artificial en la primera infancia describen un campo en expansión {cite:yi}, y los estudios sobre aplicaciones móviles y realidad aumentada en música analizan su uso y su evaluación {cite:apay,barroso,leon}. "
        "En el caso del piano, la retroalimentación con IA se ha estudiado en cuanto a exactitud técnica {cite:deng_piano}. Entre los títulos revisados no apareció un trabajo con una seña manual por nota; no se leyeron los textos completos.")
    e.P("El objetivo de este trabajo es presentar Hand Sing Kids desde su pertinencia pedagógica y su viabilidad técnica en laboratorio, y formular las hipótesis y el plan de validación que permitirían probar su utilidad con niños en Montería y Córdoba. La pregunta no es si la herramienta es técnicamente posible, "
        "sino qué evidencia falta para saber si ayuda a aprender.")

    e.sec("Contexto general")
    e.sub("Acceso a instrumentos y recursos interactivos")
    e.P("En Colombia, y en Córdoba en particular, un primer obstáculo para la educación musical es práctico: pocos centros educativos cuentan con instrumentos suficientes, y una herramienta que dependa de internet o de equipos costosos tendría el mismo problema. "
        "No se aporta aquí una estadística local sobre la educación musical, porque no se encontró en las fuentes revisadas. La justificación del proyecto es de diseño.")
    e.sub("Población de referencia")
    e.P("Las proyecciones municipales del DANE para 2026 indican 535.052 habitantes en Montería, de los cuales 80.254 tienen entre 3 y 12 años {cite:dane}. Esta cifra describe el tamaño de la población en edad escolar y no la de quienes reciben educación musical.")
    e.sub("El sistema")
    e.P("Cada nota de Do3 a Do4 se asocia a una seña de las dos manos. La cámara capta las manos y MediaPipe Hands entrega 21 puntos por mano; un descriptor invariante al tamaño, la posición y el giro convierte esos puntos en un vector de 120 componentes y un clasificador decide si hay una seña y cuál es. "
        "Después, un modelo de dominio estima qué sabe el niño de cada nota y un optimizador arma la siguiente sesión ({fig:arq}). Todo se guarda en una base local SQLite.")
    e.figura("arq", "arquitectura.png", "Arquitectura funcional de Hand Sing Kids.", 8.4)
    e.sub("Supuestos y alcance")
    e.B(["La evidencia técnica es de **laboratorio**: una calibración de una persona, perturbaciones simuladas y posturas negativas construidas por interpolación y combinación.",
         "**No hubo pruebas con niños** ni con docentes; cualquier afirmación sobre aprendizaje es una hipótesis.",
         "La pertinencia en Montería y Córdoba se argumenta por diseño (computador con cámara, base local, sin internet) y no por una estadística local de educación musical.",
         "El tamaño de muestra del piloto es una **aproximación de planificación**, calculada con una fórmula normal para dos grupos; debe refinarse con un asesor estadístico.",
         "La mención histórica a Curwen es un dato general que no se respalda con una referencia verificada en este trabajo."])

    e.sec("Diseño pedagógico")
    e.sub("Qué función docente cumple cada componente")
    e.tabla("funcion", "Funciones de un docente de música que imita la herramienta y evidencia disponible.", ["Función docente", "Componente", "Evidencia"],
            [["Mostrar la seña correcta", "Calibración por niño", "Diseño; sin pruebas"], ["Decir si la seña salió bien", "Reconocedor con margen", f"Lab.: 100 % sin ruido; {f(FPG['pct'])} % de notas falsas"],
             ["Dar sonido inmediato", "Respuesta con ventana de 1 fotograma", "Latencia parcial: 0,89 ms"], ["Ajustar el ritmo al niño", "Modelo de dominio", "Pruebas unitarias; sin niños"],
             ["Elegir qué practicar", "Optimizador de sesión", "Prueba exacta; sesión en 40 ms"], ["Motivar", "Canciones y puntaje", "Diseño; sin niños"], ["Registrar el avance", "Base local de intentos", "Funciona; sin uso docente"]],
            [2.9, 2.9, 3.4], size=8)
    e.sub("Frente a la enseñanza tradicional con señas")
    e.tabla("trad", "Comparación entre la enseñanza tradicional con señas y la herramienta.", ["Aspecto", "Tradicional", "Hand Sing Kids"],
            [["Corrección", "Depende de la atención del docente", "Inmediata, por reconocimiento"], ["Ritmo", "Igual para el grupo", "Ajustado a cada niño"], ["Requisitos", "Docente formado", "Computador con cámara; sin internet"],
             ["Registro", "Observación informal", "Intentos por habilidad"], ["Riesgo", "Seña mal hecha sin corrección", "Falsos positivos y calibración de una persona"]], [1.8, 3.2, 3.5], size=8)
    e.sub("Hipótesis de impacto")
    e.B(["**H1.** Niños de 3 a 12 años aprenden a reproducir las ocho señas con calibración individual en una sesión corta.",
         "**H2.** En el aula, la tasa de notas disparadas por error es comparable a la de laboratorio o menor al ampliar la ventana.",
         "**H3.** La aplicación funciona sin conexión a internet en computadores con cámara. Es una propiedad de diseño y puede verificarse sin niños."])

    e.sec("Descripción de datos y análisis de resultados")
    e.sub("Evidencia técnica disponible")
    A0, A2, A3 = A[0]["nuevo"], A[2]["nuevo"], A[3]["nuevo"]
    e.tabla("evid", "Evidencia técnica, que no equivale a evidencia pedagógica.", ["Medida", "Resultado"],
            [["Señas válidas, sin ruido y ruido 0,03", f"{f(A0['pct'], 0)} % (480 por nivel)"], ["Señas válidas con ruido 0,06 y 0,09", f"{f(A2['pct'])} % y {f(A3['pct'])} %"],
             ["Notas falsas, 640 posturas", f"{f(FPG['pct'])} % (IC 95 %: {f(FPG['ic95_lo'])}–{f(FPG['ic95_hi'])})"], ["Método inicial, notas falsas", "100 %"], ["Baterías de prueba del repositorio", "8 de 8 sin fallos"],
             ["Niños que probaron el sistema", "0"]], [4.6, 3.9], size=8.5)
    e.P("El cuadro separa con claridad lo que se sabe de lo que no. El sistema funciona en laboratorio como se describe; si ayuda a aprender música es una pregunta abierta, porque ningún niño lo ha usado en una prueba formal. Con ruido alto el reconocimiento baja, y el sistema prefiere abstenerse: el niño repetiría la seña.")
    e.sub("Diseño del piloto")
    e.P("El plan mínimo compara, con grupos de niños de instituciones de Montería, el desempeño de quienes usan la herramienta con el de quienes aprenden con el método tradicional, midiendo antes y después el reconocimiento de las notas, y recoge la opinión del docente.")
    e.tabla("piloto", "Diseño comparativo propuesto.", ["Elemento", "Propuesta"],
            [["Grupos", "Herramienta frente a método tradicional"], ["Medida principal", "Notas reconocidas y reproducidas, antes y después"], ["Medidas secundarias", "Notas falsas con niños; señas repetidas; opinión del docente"],
             ["Condiciones previas", "Aprobación ética; consentimiento de acudientes; política de datos"], ["Duración", "Por definir con el docente y la institución"]], [2.6, 5.9], size=8.5)
    e.sub("Tamaño de muestra aproximado")
    e.P("Para comparar dos grupos con un nivel de significancia de 0,05 y potencia de 0,80, el tamaño aproximado por grupo es $n=2\\left((z_{1-\\alpha/2}+z_{1-\\beta})/d\\right)^{2}$, con $d$ el tamaño de efecto estandarizado. Es una aproximación normal, y no sustituye el cálculo de un asesor estadístico.")
    filas = []
    for d in (0.3, 0.5, 0.8):
        n = math.ceil(n_grupo(d)); filas.append([f(d, 1), str(n), str(math.ceil(n / 0.85)), str(2 * math.ceil(n / 0.85))])
    e.tabla("n", "Tamaño de muestra aproximado por grupo según el tamaño de efecto $d$ (con 15 % de pérdidas).", ["$d$", "$n$ por grupo", "Con pérdidas", "Total"], filas, [1.4, 2.4, 2.4, 2.3], alinear=["r"] * 4)
    e.P(f"Un efecto grande ($d=0{{,}}8$) requeriría unos {math.ceil(n_grupo(0.8))} niños por grupo; uno moderado ($d=0{{,}}5$), unos {math.ceil(n_grupo(0.5))}; y uno pequeño ($d=0{{,}}3$), unos {math.ceil(n_grupo(0.3))}. Como el efecto de la herramienta es desconocido, conviene planear un piloto exploratorio y calcular el tamaño definitivo con sus resultados.")
    e.sub("Riesgos y mitigaciones")
    e.tabla("riesgo", "Riesgos principales y mitigaciones.", ["Riesgo", "Mitigación"],
            [["Calibración de una sola persona", "Calibrar a cada niño; medir con varios niños"], ["Falsos positivos con niños", "Registrar las notas falsas; ampliar la ventana por niño"], ["Iluminación y cámaras del aula", "Medir en el aula antes del piloto"],
             ["Adopción por el docente", "Probar si el docente puede calibrar sin apoyo técnico"], ["Datos de menores", "Aprobación ética; consentimiento; datos mínimos"]], [3.6, 4.9], size=8.5)

    e.sec("Conclusiones")
    e.P("Hand Sing Kids lleva una idea pedagógica antigua, enseñar las notas con las manos, a una herramienta que corre en un computador con cámara y sin internet. En laboratorio reconoce las señas de su calibración y evita casi todas las notas falsas. Su utilidad para el aprendizaje en Montería y Córdoba no está demostrada y depende de un piloto con niños, "
        "con docentes y con las autorizaciones éticas correspondientes.")
    e.P("Como líneas de trabajo se identifican cuatro: diseñar el piloto comparativo con una institución y un docente aliados; medir la latencia de extremo a extremo y las condiciones de iluminación necesarias; probar si un docente puede calibrar la herramienta sin apoyo; y obtener la aprobación ética y el consentimiento informado antes de recolectar datos de menores.")
    e.referencias()


if __name__ == "__main__":
    correr(contenido)
