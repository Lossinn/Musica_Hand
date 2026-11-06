"""Escrito final — Isaías Petro: visión computacional (reconocer solo la seña intencional)."""
from ef_comun import *
import json


def contenido(e):
    resumen = ("Una cámara ve la mano durante todo el tiempo, también cuando el niño viaja de una seña a otra, y una aplicación que enseña notas musicales con las manos debe sonar solo cuando "
               "hubo una seña intencional. Este trabajo presenta el reconocedor de Hand Sing Kids, que asigna una seña de dos manos a cada una de las ocho notas de Do3 a Do4, y lo evalúa en laboratorio. "
               "Cada postura se describe con un vector de 120 componentes, invariante al tamaño, la posición y el giro de la mano; se clasifica por vecino más cercano y solo se acepta si la distancia, la confianza y el margen "
               "sobre la segunda nota son suficientes. Se probó con una calibración de una persona y con perturbaciones simuladas: 480 señas válidas por nivel de ruido y 640 posturas que no son seña. "
               f"El reconocimiento fue de {f(A[0]['nuevo']['pct'], 0)} % sin ruido y de {f(A[3]['nuevo']['pct'])} % con ruido de 0,09, y el método disparó una nota por error en {f(FPG['pct'])} % de las posturas negativas "
               f"(IC 95 %: {f(FPG['ic95_lo'])} a {f(FPG['ic95_hi'])} %), frente a 100 % del método inicial, que acierta siempre porque responde siempre. El error restante procede casi por completo de las transiciones. "
               "Los resultados son de laboratorio: no hubo niños, la calibración es de una sola persona y el nivel de madurez es TRL 4.")
    abstract = ("A camera sees the hand all the time, including when a child moves from one sign to another, and an application that teaches musical notes with the hands should sound only when a sign was intentional. "
                "This paper presents the recognizer of Hand Sing Kids, which maps a two-handed sign to each of the eight notes from C3 to C4, and evaluates it in the laboratory. Each posture is described by a 120-component vector invariant to hand size, "
                "position and rotation, classified by nearest neighbour and accepted only if the distance, the confidence and the margin over the second note are sufficient. It was tested with a single-person calibration and simulated perturbations: "
                f"480 valid signs per noise level and 640 non-sign postures. Recognition was {f(A[0]['nuevo']['pct'], 0)} % without noise and {f(A[3]['nuevo']['pct'])} % at noise 0.09, and the method fired a wrong note in {f(FPG['pct'])} % of negative postures "
                f"(95 % CI {f(FPG['ic95_lo'])} to {f(FPG['ic95_hi'])} %), against 100 % for the initial method, which is always right because it always answers. The remaining error comes almost entirely from transitions. "
                "Results are from the laboratory: no children were involved, the calibration comes from one person and the readiness level is TRL 4.")
    titulo(e, "Petro", "Qué mano es una seña: reconocimiento invariante y decisión por margen para las ocho notas de Hand Sing Kids",
           resumen, "visión por computador; seguimiento de manos; descriptor invariante; falsos positivos; educación musical infantil.", abstract,
           "computer vision; hand tracking; invariant descriptor; false positives; children's music education.")

    e.sec("Introducción")
    e.P("Un teclado emite una señal solo cuando alguien lo oprime; una cámara, en cambio, entrega una postura en cada fotograma. Esa diferencia hace que reconocer una seña musical sea un problema de dos partes. La primera es de "
        "clasificación: decidir a cuál de las ocho notas se parece la mano. La segunda es de decisión: saber cuándo no responder. En Hand Sing Kids, una aplicación que enseña las notas de Do3 a Do4 con señas de las dos manos, "
        "la segunda parte pesa tanto como la primera, porque entre una seña y otra la mano atraviesa posturas intermedias, a veces se cruza con la otra o se tapa.")
    e.P("MediaPipe Hands entrega 21 puntos por mano en tiempo real sobre un dispositivo común {cite:mediapipe}, y a partir de ellos se pueden construir clasificadores de naturaleza muy distinta. La literatura reciente de "
        "tecnología para la enseñanza de la música ha aplicado la visión a la detección del teclado de piano {cite:chulu} y a la retroalimentación con IA sobre la técnica del estudiante {cite:deng_piano}; las revisiones sobre IA "
        "en la primera infancia describen un campo amplio {cite:yi}, y los trabajos sobre aplicaciones musicales analizan sobre todo su uso y su evaluación {cite:apay}. En los títulos y metadatos revisados no apareció un trabajo "
        "cuya entrada sea una seña manual por nota calibrada para cada niño; no se leyeron los textos completos, así que esta observación no excluye que exista.")
    e.P("El objetivo de este trabajo es describir el reconocedor de señas de Hand Sing Kids y medir, en laboratorio, cuántas señas válidas reconoce y cuántas notas dispara por error, en comparación con el método de la versión "
        "inicial. Las contribuciones son tres: un descriptor de 120 componentes con una regla de aceptación por distancia, confianza y margen; una evaluación con señas válidas y con posturas que no son seña, con intervalos de "
        "confianza; y la declaración explícita de los límites de la evidencia.")

    e.sec("Contexto general")
    e.P("La aplicación es de escritorio, escrita en Python con interfaz en PySide6. La cámara alimenta a MediaPipe Hands; el descriptor y el clasificador convierten los 21 puntos de cada mano en una nota candidata; un estabilizador "
        "decide si la nota se confirma; y la capa pedagógica, que no se trata aquí, usa esa nota para registrar el intento y elegir la siguiente actividad ({fig:arq}). Cada nota de la escala corresponde a una seña de las dos manos.")
    e.figura("arq", "arquitectura.png", "Arquitectura funcional de Hand Sing Kids. Este trabajo estudia los bloques de percepción, hasta la confirmación de la nota.", 8.4)
    e.sub("Supuestos y alcance", "supuestos")
    e.P("Las conclusiones dependen de las condiciones siguientes, que conviene enunciar de forma explícita:", sangria=False, keep=True)
    e.B(["La calibración es de **una sola persona** y contiene las ocho señas como coordenadas de puntos de la mano, sin imágenes.",
         "Las perturbaciones son **simuladas** sobre esas coordenadas: escala entre 0,8 y 1,25, giro independiente por mano de ±18° y ruido gaussiano proporcional al tamaño de la mano.",
         "Las posturas negativas se construyeron por interpolación entre señas y por combinación de manos de señas distintas; no provienen de niños.",
         "El método inicial se evaluó con la misma calibración, de modo que la comparación es interna.",
         "No se midió el rastreo de MediaPipe, la captura de la cámara ni el dibujo en pantalla.",
         "No hubo pruebas con niños."])

    e.sec("Modelo del reconocedor")
    e.sub("Descriptor invariante")
    e.P("Sean $p_0,\\dots,p_{20}$ los 21 puntos de una mano, con $p_0$ en la muñeca. La escala de referencia es la distancia de la muñeca al nudillo del dedo medio:")
    e.eq("sigma", r"\sigma=\lVert p_9-p_0\rVert")
    e.P("La curvatura de cada dedo, con cadena de articulaciones $(a,b,c,d)$, es una razón entre longitudes y por eso no cambia con la escala, la traslación ni la rotación:")
    e.eq("kappa", r"\kappa=\operatorname{clip}\!\left(\frac{\dfrac{\lVert p_d-p_a\rVert}{\lVert p_b-p_a\rVert+\lVert p_c-p_b\rVert+\lVert p_d-p_c\rVert}-0{,}35}{0{,}65},\,0,\,1\right)")
    e.P("La apertura entre dedos contiguos usa los vectores unitarios $u_i$ del nudillo a la yema, y la distancia del pulgar a cada yema se normaliza con $\\sigma$:")
    e.eq("alpha", r"\alpha_i=\frac{1}{\pi}\arccos\langle u_i,u_{i+1}\rangle,\qquad \tau_j=\frac{1}{3}\operatorname{clip}\!\left(\frac{\lVert p_{t_j}-p_4\rVert}{\sigma},\,0,\,3\right)")
    e.P("A estas magnitudes se suman la normal del plano de la palma, la dirección de la mano en la imagen y la forma normalizada, con 20 puntos trasladados, escalados por $\\sigma$ y girados para que la mano apunte hacia arriba (40 valores). "
        "Cada mano queda en 58 valores y, con cuatro magnitudes de geometría entre las dos manos, el descriptor completo tiene $2\\times 58+4=120$ componentes. La distancia entre dos descriptores se calcula por bloques $g$ con pesos $w_g$ "
        "(curvatura 3,0; forma 2,6; pulgar 2,0; dirección 2,0; entre manos 1,6; normal 1,4; apertura 1,2), de modo que los 40 valores de la forma no dominen a los 5 de la curvatura:")
    e.eq("dist", r"d(a,b)=\sqrt{\frac{1}{\sum_g w_g}\sum_g w_g\,\frac{1}{|g|}\sum_{i\in g}(a_i-b_i)^2}")
    e.sub("Clasificación con confianza y margen")
    e.P("Cada nota $c$ conserva hasta tres muestras $S_c$ de la calibración. La distancia de una postura $x$ a la nota es la menor de sus muestras, y la confianza reparte probabilidad entre las notas con una temperatura $T$ "
        "ajustada a la separación real entre las señas:")
    e.eq("dc", r"d_c=\min_{s\in S_c}d(x,s),\qquad P(c\mid x)=\frac{\exp\!\big(-(d_c-d_{\min})/T\big)}{\sum_k\exp\!\big(-(d_k-d_{\min})/T\big)}")
    e.eq("temp", r"T=\operatorname{clip}\!\left(\tfrac{1}{2}\min_{a\neq b}d(a,b),\,0{,}05,\,0{,}20\right)")
    e.P("La nota se acepta solo si se cumplen las tres condiciones de la ecuación {eq:acepta}. La tercera, el margen, hace que el sistema se abstenga cuando dos señas empatan:")
    e.eq("acepta", r"\begin{aligned}d_{\text{best}}&\le 0{,}95\\ P_{\text{best}}&\ge 0{,}55\\ P_{\text{best}}-P_{\text{second}}&\ge 0{,}08\end{aligned}")
    e.sub("Estabilización temporal")
    e.P("Después de aceptada, la nota pasa por un estabilizador: se confirma si pasaron al menos 0,45 s desde la nota anterior (periodo refractario) y, cuando repite la última nota, solo si el niño la soltó antes. "
        "La suelta se declara cuando seis fotogramas consecutivos dan una lectura distinta. Con la configuración por defecto la ventana es de un fotograma, por lo que la nota suena en cuanto se reconoce.")

    e.sec("Descripción de datos y análisis de resultados")
    e.sub("Datos y protocolo")
    e.P("La evaluación reproduce y amplía la prueba de visión del repositorio sin modificarla. Se midieron dos cosas. Primera, la tasa de reconocimiento de señas válidas con ruido $\\sigma\\in\\{0;\\,0{,}03;\\,0{,}06;\\,0{,}09\\}$, con 60 repeticiones por nota "
        "y nivel, es decir, 480 señas por nivel. Segunda, las notas disparadas por error ante 640 posturas que no son seña: 320 transiciones a medio camino entre una nota y otra tres posiciones más adelante, y 320 combinaciones de la mano izquierda de una "
        "seña con la derecha de otra. Las proporciones llevan intervalos de Wilson al 95 % {cite:wilsonci}. La estabilidad de la tasa de falsos positivos se midió con 30 semillas distintas.")
    e.sub("Configuración experimental")
    e.P("Las mediciones se hicieron en un solo equipo con Windows 11, Python 3.12.10, NumPy 1.26.4, OpenCV 4.11.0 y MediaPipe 0.10.21. No se registraron las características del procesador ni de la memoria. El código y los scripts están en el repositorio "
        "y las cifras se leen de un archivo de resultados generado por un script con semillas fijas.")
    e.sub("Señas válidas")
    filas = []
    for a in A:
        n, v = a["nuevo"], a["v1"]
        filas.append([f(a["ruido"], 2), f"{f(n['pct'])} ({f(n['ic95_lo'])}–{f(n['ic95_hi'])})", f"{f(v['pct'])} ({f(v['ic95_lo'])}–{f(v['ic95_hi'])})"])
    e.tabla("acierto", "Señas válidas reconocidas (%), con IC de Wilson al 95 %, sobre 480 señas por nivel de ruido.", ["Ruido σ", "Descriptor propuesto", "Método inicial"], filas, [1.3, 3.6, 3.6], alinear=["l", "r", "r"])
    e.P(f"Hasta un ruido de 0,03 el descriptor propuesto reconoce todas las señas; con 0,06 llega a {f(A[2]['nuevo']['pct'])} % y con 0,09 a {f(A[3]['nuevo']['pct'])} % (IC 95 %: {f(A[3]['nuevo']['ic95_lo'])} a {f(A[3]['nuevo']['ic95_hi'])} %). "
        "El método inicial acierta siempre, y esa cifra no debe leerse como una ventaja: responde a toda postura con la nota más parecida, de modo que no puede equivocarse por omisión. El cuadro siguiente muestra el costo de ese comportamiento.")
    e.sub("Posturas que no son seña")
    e.tabla("fp", "Notas disparadas por error ante 640 posturas que no son seña (k; %; IC de Wilson al 95 %).", ["Tipo de postura", "n", "Propuesto", "Inicial"],
            [["Transiciones", "320", f"{FPT['transicion']['nuevo']['k']} ({f(FPT['transicion']['nuevo']['pct'])})", f"{FPT['transicion']['v1']['k']} (100,0)"],
             ["Manos cruzadas", "320", f"{FPT['manos_cruzadas']['nuevo']['k']} ({f(FPT['manos_cruzadas']['nuevo']['pct'])})", f"{FPT['manos_cruzadas']['v1']['k']} (100,0)"],
             ["**Total**", "**640**", f"**{FPG['k']} ({f(FPG['pct'])})**", f"**{FPV['k']} (100,0)**"]], [3.0, 1.0, 2.4, 2.1], alinear=["l", "r", "r", "r"])
    e.P(f"El descriptor propuesto disparó {FPG['k']} notas por error en {FPG['n']} posturas ({f(FPG['pct'])} %; IC 95 %: {f(FPG['ic95_lo'])} a {f(FPG['ic95_hi'])} %), frente a las 640 del método inicial. Con 30 semillas distintas la tasa media fue de {f(RB['media'])} % "
        f"(desviación estándar {f(RB['sd'], 2)}; mínimo {f(RB['min'])} %; máximo {f(RB['max'])} %), de modo que no depende de una semilla favorable. Casi todo el error viene de las transiciones ({f(FPT['transicion']['nuevo']['pct'])} %); las manos cruzadas casi no "
        f"disparan ({f(FPT['manos_cruzadas']['nuevo']['pct'])} %). Es plausible: una postura a medio camino conserva rasgos de las dos señas extremas, mientras que una mano de cada seña no se parece a ninguna.")
    e.figura("barras", "aciertos.png", "Señas válidas reconocidas según el ruido (barras: IC de Wilson al 95 %; el eje parte de 70 %).", 7.4)
    e.figura("fpbar", "falsos_positivos.png", "Notas disparadas por error ante posturas que no son seña.", 7.4)
    e.sub("Separabilidad de las señas y latencia")
    e.P(f"Con la calibración real, {MX['pares_sobre_0_65']} de los {MX['pares_ordenados']} pares ordenados de notas distintas ({MX['pares_unicos_sobre_0_65']} pares no ordenados de 28) superan una similitud coseno de 0,65, el umbral del método inicial; el par "
        f"más parecido es {MX['max_cos'][0]}–{MX['max_cos'][1]}, con {f(MX['max_cos'][2], 3)}. Con el descriptor propuesto, la distancia entre notas distintas va de {f(MX['dist_min_entre_notas'], 3)} a {f(MX['dist_max_entre_notas'], 3)}, lo que ajusta la temperatura a $T={f(MX['temperatura'], 3)}$ según la ecuación {{eq:temp}}. "
        "En el método inicial, dos nubes de puntos con forma de mano siempre se parecen, y por eso un umbral fijo de similitud no separa notas; el descriptor traslada la comparación a magnitudes que sí cambian de una seña a otra ({fig:matriz}).")
    e.figura("matriz", "matriz_similitud.png", "Matrices 8 × 8 de las señas calibradas: (a) similitud coseno del método inicial; (b) distancia por bloques del descriptor propuesto.", 16.0, ancha=True)
    e.P(f"El descriptor y el clasificador tardaron {f(LT['media_ms'], 2)} ms por fotograma en promedio (percentil 95: {f(LT['p95_ms'], 2)} ms; máximo: {f(LT['max_ms'], 2)} ms; {LT['reps']} repeticiones, un solo equipo). La cifra excluye captura, rastreo y dibujo en pantalla.")
    e.sub("Sensibilidad de los umbrales de aceptación", "sens")
    e.P("Para saber qué parte de la regla de aceptación controla el compromiso entre acertar y abstenerse, se repitió el protocolo anterior con los mismos datos y semillas variando un umbral por vez, mientras los otros dos permanecían en su valor por defecto. "
        "El caso base reproduce exactamente los resultados anteriores (86,0 % de reconocimiento con ruido 0,09 y 51 notas falsas de 640).")
    S = json.loads((BASE / "analisis" / "sensibilidad_umbrales.json").read_text(encoding="utf-8"))
    filas = [[f(r["valor"], 2), f(r["ac_006"]), f(r["ac_009"]), f(r["fp"])] for r in S["confidence_threshold"]]
    e.tabla("sensu", "Efecto del umbral de confianza (valor por defecto: 0,55) sobre el reconocimiento con ruido y sobre las notas falsas (%).", ["Confianza mínima", "Ruido 0,06", "Ruido 0,09", "Notas falsas"], filas, [2.2, 2.0, 2.0, 2.2], alinear=["l", "r", "r", "r"])
    e.P("El umbral de confianza es la perilla que mueve el compromiso ({fig:umbral}). Con 0,35 se reconocen todas las señas con ruido hasta 0,09, pero el 55,0 % de las posturas negativas dispara una nota; con 0,75 casi no hay notas falsas (0,0 %), "
        "pero solo se reconoce el 43,5 % de las señas válidas con ruido alto. El valor por defecto queda en una zona intermedia: tolera ruido moderado y limita las notas falsas a 8,0 %. En cambio, variar el umbral de distancia entre 0,65 y 1,25, o el de margen entre 0,00 y 0,16, "
        "no cambió ningún resultado con este protocolo. Para el margen hay una explicación aritmética: si la confianza de la mejor nota es al menos 0,55, la de la segunda es a lo sumo 0,45 y el margen es al menos $2\\cdot 0{,}55-1=0{,}10$, de modo que la condición de 0,08 nunca es la que decide mientras la confianza mínima sea de 0,55 o más.")
    e.figura("umbral", "umbral_confianza.png", "Compromiso entre reconocimiento con ruido 0,09 y notas falsas al variar el umbral de confianza (círculo: valor por defecto).", 8.2)
    e.sub("Costo de rechazar lo dudoso")
    e.P("El descriptor propuesto cuesta sensibilidad cuando el ruido es alto: de 100 % a 86,0 % entre ruido 0 y 0,09. El método inicial no pierde nada porque no rechaza nada. En un juego infantil el intercambio favorece al primero: pedir que se repita una seña "
        "cuesta unos segundos, mientras que una nota falsa interrumpe la actividad y puede enseñar un sonido equivocado.")

    e.sec("Conclusiones")
    e.P(f"Un descriptor invariante de 120 componentes con decisión por distancia, confianza y margen redujo las notas disparadas por error de 100 % a {f(FPG['pct'])} % en 640 posturas que no son seña, con una pérdida de sensibilidad visible solo con ruido alto. "
        "El error que queda se concentra en las transiciones, y de ahí salen dos pasos concretos: ajustar el umbral de confianza, la única perilla de la regla de aceptación que mueve el compromiso entre acertar y abstenerse, e incorporar la velocidad de la mano, que hoy no interviene en la decisión, como señal de que una postura en movimiento rápido difícilmente es una seña deliberada.")
    e.P("Los resultados describen el comportamiento del reconocedor en laboratorio, no en un aula. Como líneas de trabajo se identifican cuatro: calibrar y medir con varias personas y con niños; incluir errores reales de detección, desenfoque e iluminación; "
        "registrar las notas falsas durante un piloto en lugar de simularlas; y medir la latencia de extremo a extremo. El nivel de madurez del reconocedor es TRL 4.")
    e.referencias()


if __name__ == "__main__":
    correr(contenido)
