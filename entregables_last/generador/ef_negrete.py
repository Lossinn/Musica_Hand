"""Escrito final — Andrés Negrete: tiempo y retroalimentación."""
from ef_comun import *


def ventana(bpm, wmin):
    g = 60000 / bpm
    w = max(wmin, 0.85 * g)
    return g, w, 1.15 * w / 2, 0.85 * w / 2


def contenido(e):
    resumen = ("En una aplicación que enseña notas con las manos, reconocer bien la seña no basta: la nota debe sonar en el momento en que el niño la espera, una sola vez, y sin castigarlo por el tiempo que el sistema tarda en confirmarla. "
               "Este trabajo describe y analiza los mecanismos temporales de Hand Sing Kids: un estabilizador que confirma la nota con periodo refractario y detección de suelta, y el motor del módulo Canciones, que usa el reloj de la partida, "
               "una ventana de acierto asimétrica con piso de 480 ms y un puntaje con combo. Se explica por qué el umbral de suelta es de seis fotogramas y cómo el tempo reparte la ventana antes y después de la línea de la nota, y se hace un análisis "
               "de sensibilidad del piso de la ventana, que la documentación fijaba en 380 ms y el código en 480 ms. El descriptor y el clasificador tardan "
               f"{f(LT['media_ms'], 2)} ms por fotograma (percentil 95: {f(LT['p95_ms'], 2)} ms), sin contar cámara ni pantalla, y el método dispara una nota por error en {f(FPG['pct'])} % de 640 posturas que no son seña. "
               "Las constantes del puntaje y de la ventana son decisiones de diseño y no se validaron con niños; el nivel de madurez es TRL 4.")
    abstract = ("In an application that teaches notes with the hands, recognizing the sign is not enough: the note must sound when the child expects it, once, and without penalizing the child for the time the system takes to confirm it. "
                "This paper describes and analyses the temporal mechanisms of Hand Sing Kids: a stabilizer that confirms the note with a refractory period and release detection, and the engine of the Songs module, which uses the game clock, "
                "an asymmetric hit window with a 480 ms floor and a combo score. It explains why the release threshold is six frames and how tempo splits the window before and after the note line, and presents a sensitivity analysis of the window floor, "
                f"which the documentation set at 380 ms and the code at 480 ms. The descriptor and classifier take {f(LT['media_ms'], 2)} ms per frame (95th percentile: {f(LT['p95_ms'], 2)} ms), excluding camera and display, and the method fires a wrong note in {f(FPG['pct'])} % of 640 non-sign postures. "
                "Window and score constants are design decisions not validated with children; the readiness level is TRL 4.")
    titulo(e, "Negrete", "Cuándo debe sonar la nota: estabilización, ventana de acierto y retroalimentación en Hand Sing Kids", resumen,
           "retroalimentación; estabilización temporal; ventana de acierto; gamificación; educación musical infantil.", abstract,
           "feedback; temporal stabilization; hit window; gamification; children's music education.")

    e.sec("Introducción")
    e.P("Cuando un niño hace una seña y espera oír la nota, cada décima de segundo cuenta. Si el sonido llega tarde, el niño no lo asocia con su gesto; si llega antes de que termine de formar la seña, suena una nota equivocada; si suena dos veces, "
        "cree que se equivocó. Hand Sing Kids reconoce ocho señas de las dos manos, de Do3 a Do4, con una cámara y MediaPipe Hands {cite:mediapipe}, y ofrece actividades guiadas y un módulo de canciones en que el niño debe producir las notas al compás de una melodía. "
        "En el segundo caso el sistema no espera la seña: el tiempo lo marca el reloj de la partida y el niño debe acertar dentro de una ventana.")
    e.P("Reconocer una seña y decidir cuándo confirmarla son problemas distintos. El primero se resuelve con un clasificador; el segundo, con reglas de tiempo que deben equilibrar tres riesgos: perder una seña correcta, duplicar una nota y penalizar al niño por el retraso del sistema. "
        "La literatura sobre retroalimentación con IA en la enseñanza del piano se ocupa sobre todo de la exactitud técnica {cite:deng_piano}, y los trabajos sobre trayectorias personalizadas {cite:li_peerj,tang} y sobre evaluación de la enseñanza musical {cite:wang} "
        "tratan la decisión pedagógica; en los títulos revisados no apareció el diseño temporal de una entrada por seña manual. Para la dificultad de las actividades se usa la idea de que la práctica es más eficiente con una tasa de error intermedia {cite:wilson85}.")
    e.P("El objetivo es describir con precisión los mecanismos temporales de Hand Sing Kids, mostrar qué falla previene cada uno y cuantificar, con las fórmulas del código, el efecto del tempo y del piso de la ventana sobre el margen que se le da al niño.")

    e.sec("Contexto general")
    e.P("El módulo Canciones tiene 19 melodías tradicionales o de dominio público, simplificadas a las ocho notas de la escala, y tres factores de tempo (0,72; 1,0 y 1,15). Durante una partida, la nota $i$ llega en un instante fijado por el reloj, "
        "y la aplicación abre una ventana alrededor de ese instante en la que la seña cuenta como acierto. La lectura de la cámara pasa antes por un estabilizador que decide si la nota se confirma.")
    e.sub("Supuestos y alcance")
    e.B(["Las constantes del estabilizador, de la ventana y del puntaje son **decisiones de diseño**; no se calibraron con niños.",
         "El análisis de la ventana (cuadro de sensibilidad) es un **cálculo derivado de la fórmula**, suponiendo que la tolerancia del tipo de actividad no limita el ancho; no es una medición.",
         "La latencia medida cubre solo el descriptor y el clasificador, en un equipo; excluye la cámara, el rastreo de MediaPipe y el dibujo en pantalla.",
         "Las posturas que no son seña son simuladas por interpolación y combinación de manos, no provienen de niños.",
         "Se adopta el valor del código cuando hay diferencia con la documentación."])

    e.sec("Modelo temporal")
    e.sub("Estabilizador de notas")
    e.P("Entre la lectura de la cámara y el sonido hay un estabilizador. Una nota se confirma si el clasificador la reconoce con confianza suficiente, si pasaron al menos 0,45 s desde la nota anterior (periodo refractario) y, cuando es la misma que la última, solo si el niño "
        "la soltó antes. Se considera soltada cuando seis fotogramas consecutivos arrojan una lectura distinta. Con la configuración por defecto la ventana de votación es de un fotograma, de modo que la nota suena en cuanto se reconoce.")
    e.P("El valor de seis fotogramas cambió durante el desarrollo. La documentación menciona dos, el código usa seis. Con votación de varios fotogramas, el parpadeo del seguimiento, en que MediaPipe pierde la mano uno o dos fotogramas aunque esté quieta, "
        "quedaba absorbido por la votación; al pasar a un fotograma, la suelta quedó como único filtro y dos fotogramas resultaron insuficientes: una nota sostenida sonaba dos veces. Aquí se adopta el valor del código.")
    e.sub("Ventana de acierto")
    e.P("Con tempo $\\text{bpm}$, el intervalo entre notas es $g=60000/\\text{bpm}$ ms y la nota $i$ llega en $a_i=a_{i-1}+g$, con $a_0=2200$ ms. La ventana es asimétrica, más ancha antes de la línea que después, para no penalizar al niño por el tiempo que tarda el reconocimiento en confirmar:")
    e.eq("vent", r"h_i=\frac{\max\!\big(W_{\min},\,\min(\text{tol},\,0{,}85\,g)\big)}{2}")
    e.eq("vent2", r"\text{ventana}_i=\big[a_i-1{,}15\,h_i,\ a_i+0{,}85\,h_i\big]")
    e.P("El ancho total es $2h_i$, con piso $W_{\\min}$ en el código de 480 ms; antes de la línea hay $1{,}15\\,h_i$ y después $0{,}85\\,h_i$, lo que da un 57,5 % del ancho antes y un 42,5 % después.")
    e.sub("Puntaje y combo")
    e.P("El puntaje por nota es de 100, 70 o 50 puntos según el error temporal (perfecto, bien o vale) y se multiplica por un factor de combo con tope:")
    e.eq("combo", r"\text{puntos}_i=b_i\cdot\min\!\left(1+0{,}5\left\lfloor \frac{c}{10}\right\rfloor,\ 4\right),\qquad b_i\in\{100,70,50\}")
    e.P("donde $c$ es el número de aciertos seguidos. El factor llega al tope ×4 con 60 aciertos consecutivos.")
    e.tabla("param", "Parámetros del motor temporal.", ["Parámetro", "Valor", "Origen"],
            [["Periodo refractario", "0,45 s", "Código"], ["Suelta", "6 fotogramas", "Código (doc.: 2)"], ["Ventana de votación", "1 fotograma", "Por defecto"],
             ["Piso de la ventana $W_{\\min}$", "480 ms", "Código (doc.: 380)"], ["Fracción de $g$ en la ventana", "0,85", "Código"], ["Reparto antes/después", "1,15 y 0,85", "Código"],
             ["Primera nota $a_0$", "2200 ms", "Código"], ["Factores de tempo", "0,72; 1,0; 1,15", "Código"], ["Puntaje por nota", "100; 70; 50", "Código"], ["Tope del combo", "×4", "Código"]],
            [4.0, 2.2, 2.3])

    e.sec("Descripción de datos y análisis de resultados")
    e.sub("Datos y configuración experimental")
    e.P("No se recolectaron datos de niños. Se usaron dos fuentes: las fórmulas y constantes del código, con las que se calculó la ventana de acierto, y las mediciones de laboratorio del reconocedor (480 señas válidas por nivel de ruido; 640 posturas que no son seña), "
        "hechas en un solo equipo con Windows 11, Python 3.12.10, NumPy 1.26.4, OpenCV 4.11.0 y MediaPipe 0.10.21. No se registraron las características del procesador.")
    e.sub("Efecto del tempo sobre la ventana")
    filas = []
    for bpm in (40, 60, 80, 100, 120):
        g, w, a, d = ventana(bpm, 480)
        filas.append([str(bpm), m(g), m(0.85 * g), m(w), m(a), m(d)])
    e.tabla("tempo", "Ventana de acierto según el tempo (ms), con $W_{\\min}=480$ ms y tolerancia no limitante.", ["bpm", "$g$", "$0{,}85\\,g$", "Ancho", "Antes", "Después"], filas, [1.2, 1.6, 1.8, 1.6, 1.6, 1.8], alinear=["r"] * 6)
    e.P("Hasta unos 100 bpm la ventana depende solo del intervalo entre notas; a partir de ahí actúa el piso de 480 ms. A 120 bpm, el 85 % del intervalo es de 425 ms, la ventana se mantiene en 480 ms y deja 276 ms antes y 204 ms después de la línea ({fig:ventana}). "
        "La asimetría da más margen para adelantarse que para retrasarse, lo que compensa el tiempo que tarda el reconocimiento en confirmar.")
    e.figura("ventana", "ventana_tempo.png", "Reparto de la ventana de acierto antes (azul) y después (verde) de la línea de la nota, según el tempo.", 8.3)
    e.sub("Análisis de sensibilidad del piso de la ventana")
    e.P("La documentación del proyecto fijaba el piso en 380 ms y el código lo fija en 480 ms. Para ver cuánto importa esa diferencia se calculó el ancho de la ventana con tres valores del piso en cuatro tempos.")
    filas = []
    for bpm in (80, 100, 120, 140):
        g = 60000 / bpm
        filas.append([str(bpm), m(0.85 * g)] + [m(max(w, 0.85 * g)) for w in (380, 480, 580)])
    e.tabla("sens", "Ancho de la ventana (ms) según el piso $W_{\\min}$.", ["bpm", "$0{,}85\\,g$", "380", "480", "580"], filas, [1.2, 1.8, 1.6, 1.6, 1.6], alinear=["r"] * 5)
    e.P("A 80 bpm el piso no interviene en ninguno de los tres casos. A 100 bpm solo interviene el de 580 ms; a 120 bpm, los de 480 y 580 ms, mientras que con 380 ms la ventana sigue siendo la de 425 ms que fija el intervalo; y a 140 bpm intervienen los tres, con ventanas de 380, 480 y 580 ms. "
        "Cuando el piso decide, una diferencia de 100 ms en el piso se traduce directamente en 100 ms más de tolerancia total. El piso de 480 ms se apoya en el tiempo que necesitan el reconocimiento y el niño; uno menor haría muy exigentes los tempos rápidos, aunque esa afirmación debe confirmarse con niños.")
    e.sub("Costo del reconocimiento en el tiempo de respuesta")
    e.P(f"El descriptor y el clasificador tardaron {f(LT['media_ms'], 2)} ms por fotograma en promedio, con percentil 95 de {f(LT['p95_ms'], 2)} ms y máximo de {f(LT['max_ms'], 2)} ms en {LT['reps']} repeticiones. Es una fracción pequeña de la ventana mínima, pero no incluye la captura de la cámara, el rastreo ni el dibujo en pantalla, "
        "de modo que la latencia de extremo a extremo sigue sin medirse. La versión inicial de la documentación reportaba 2,3 ms en otro equipo; no puede decirse que las dos cifras se contradigan, porque no consta que tuvieran el mismo alcance.")
    e.sub("Respuesta inmediata y falsas notas")
    e.P(f"Con ventana de un fotograma, el método disparó una nota por error en {f(FPG['pct'])} % de 640 posturas que no son seña (IC 95 %: {f(FPG['ic95_lo'])} a {f(FPG['ic95_hi'])} %), casi todo en transiciones ({f(FPT['transicion']['nuevo']['pct'])} %). "
        "Con votación de varios fotogramas ese error se reduce, pero a cambio de una espera perceptible. Para niños pequeños se prefirió la respuesta inmediata, y la ventana puede ampliarse por niño desde los ajustes de la aplicación.")
    e.sub("Un caso de efecto cruzado")
    e.P("La nota que sonaba dos veces ilustra un riesgo general: cambiar un parámetro en un módulo puede dejar a otro cargando con una función que nunca se probó por separado. Al quitar la votación, el umbral de suelta, que antes casi no importaba, pasó a ser crítico. "
        "Por eso la batería del estabilizador incluye ahora una prueba del parpadeo breve de la mano.")

    e.sec("Conclusiones")
    e.P("Hand Sing Kids resuelve el problema del tiempo con tres piezas: un estabilizador con periodo refractario y detección de suelta, una ventana de acierto asimétrica con piso de 480 ms y un puntaje con combo. Se explicó por qué el umbral de suelta es de seis fotogramas y cómo "
        "el tempo y el piso reparten la ventana. El análisis de sensibilidad muestra que el piso empieza a decidir entre 100 y 140 bpm según su valor, y que entonces cada 100 ms de piso son 100 ms de tolerancia total.")
    e.P("Las constantes del puntaje y de la ventana provienen del diseño y no de datos de niños; el nivel de madurez es TRL 4. Como líneas de trabajo se identifican cuatro: medir la latencia de extremo a extremo con la cámara real; registrar en un piloto las notas duplicadas y las señas repetidas; "
        "ajustar el piso y el puntaje con observaciones de niños y docentes; y mantener la prueba del parpadeo breve en la batería del estabilizador.")
    e.referencias()


if __name__ == "__main__":
    correr(contenido)
