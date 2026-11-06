"""Artículo — primer autor: Isaías José Petro Rodríguez. Hilo: visión computacional; distinguir la seña intencional del gesto de paso."""
import sys
from nucleo_hsk import *
import nucleo_hsk as N

A = R["aciertos"]; FP = R["falsos_positivos"]["global_nuevo"]

TITULO_ES = ("Qué mano es una seña: descriptor invariante y decisión por margen para reconocer las ocho notas de Hand Sing Kids")
TITULO_EN = ("Which hand pose is a sign: invariant descriptor and margin-based decision to recognize the eight notes of Hand Sing Kids")
RES_ES = ("Una cámara ve la mano todo el tiempo, también cuando el niño viaja de una seña a otra, y una aplicación que enseña notas con las manos debe sonar solo cuando "
          "hubo una seña intencional. Se describe y evalúa el reconocedor de Hand Sing Kids, que asigna una seña de dos manos a cada una de las ocho notas de Do3 a Do4. "
          "Cada postura se codifica con un vector de 120 componentes invariante al tamaño, la posición y el giro de la mano, se clasifica por vecino más cercano y se acepta solo si "
          "la distancia, la confianza y el margen sobre la segunda nota son suficientes. Con una calibración de una persona y perturbaciones simuladas, 480 señas válidas por nivel de ruido "
          f"se reconocieron en {f(A[0]['nuevo']['pct'], 0)} % sin ruido y en {f(A[3]['nuevo']['pct'])} % con ruido de 0,09. Ante 640 posturas que no son seña, el método propuesto disparó una nota por error en "
          f"{f(FP['pct'])} % de los casos (IC 95 %: {f(FP['ic95_lo'])} a {f(FP['ic95_hi'])} %), frente a 100 % del método de la versión inicial, que acierta siempre porque responde siempre. "
          "El error restante viene sobre todo de las transiciones entre señas. No hubo pruebas con niños; el nivel de madurez es TRL 4 y el efecto en el aula es una hipótesis.")
RES_EN = ("A camera sees the hand all the time, including when a child moves from one sign to another, and an application that teaches notes with the hands should sound only when "
          "a sign was intentional. The recognizer of Hand Sing Kids, which assigns a two-handed sign to each of the eight notes from C3 to C4, is described and evaluated. "
          "Each posture is encoded as a 120-component vector invariant to hand size, position and rotation, classified by nearest neighbour and accepted only if the distance, "
          "the confidence and the margin over the second note are sufficient. With a single-person calibration and simulated perturbations, 480 valid signs per noise level were recognized at "
          f"{f(A[0]['nuevo']['pct'], 0)} % without noise and {f(A[3]['nuevo']['pct'])} % at noise 0.09. Over 640 postures that are not signs, the proposed method fired a wrong note in "
          f"{f(FP['pct'])} % of cases (95 % CI {f(FP['ic95_lo'])} to {f(FP['ic95_hi'])} %), against 100 % for the initial method, which is always right because it always answers. "
          "The remaining error comes mostly from transitions between signs. No tests with children were done; the readiness level is TRL 4 and the classroom effect is a hypothesis.")
KW_ES = "reconocimiento de gestos; seguimiento de manos; descriptor invariante; vecino más cercano; falsos positivos; educación musical infantil; Montería"
KW_EN = "gesture recognition; hand tracking; invariant descriptor; nearest neighbour; false positives; children's music education; Montería"
autores = encabezado("Petro", TITULO_ES, TITULO_EN, RES_ES, RES_EN, KW_ES, KW_EN)

H1("Introducción")
H2("Responder siempre no es reconocer")
T("Un sistema de visión por computador sobre una mano enfrenta una dificultad que no aparece en un teclado: el teclado solo emite una señal cuando alguien lo oprime, mientras que la cámara "
  "entrega una postura en cada fotograma. En Hand Sing Kids cada nota de la escala, de Do3 a Do4, corresponde a una seña de las dos manos. Entre una seña y otra la mano pasa por posiciones intermedias, "
  "y a veces las manos se cruzan o se tapan. Si el programa convierte cada postura en una nota, el niño oirá sonidos que no pidió. El problema, entonces, no es solo de exactitud sobre señas "
  "válidas, sino de saber cuándo no responder.")
T("MediaPipe Hands entrega 21 puntos por mano en tiempo real en un dispositivo común {c:mediapipe}, y con ellos se pueden construir clasificadores muy distintos. La pregunta de este trabajo es qué "
  "descripción de la postura y qué regla de decisión permiten rechazar lo que no es una seña sin perder las señas buenas, usando solo la calibración de una persona. Se mide con 480 señas por nivel de ruido y "
  "con 640 posturas que no son seña, con intervalos de confianza de Wilson {c:wilsonci}.")
H2("Antecedentes")
T("La literatura reciente aplica visión e inteligencia artificial a la enseñanza musical de varias formas: detección visual del teclado y retroalimentación para piano {c:deng_piano,chulu}, trayectorias de "
  "aprendizaje personalizadas {c:li_hong,li_peerj,li_disc,tang,wang}, sistemas sensibles a la emoción {c:deng_sci,shi}, generación de partituras según dificultad {c:ramoneda} y aplicaciones y realidad "
  "aumentada {c:apay,barroso,leon}. Una revisión sobre primera infancia resume las tecnologías de IA disponibles {c:yi}. En los títulos y metadatos revisados no apareció un trabajo que parta de una seña "
  "manual por nota calibrada para cada niño; no se leyeron los textos completos, así que esto no excluye que exista.")
tabla("Tabla 1. Decisiones que debe tomar el reconocedor y cómo las resuelve el método propuesto",
      ["Situación", "Qué ocurre con la cámara", "Respuesta deseada", "Mecanismo"],
      [["Seña intencional", "Postura estable y parecida a la calibrada", "Sonar la nota", "Distancia, confianza y margen aceptables"],
       ["Mano en tránsito", "Postura intermedia entre dos señas", "No sonar", "Margen insuficiente entre notas"],
       ["Manos cruzadas", "Una mano de cada seña", "No sonar", "Distancia alta a todas las notas"],
       ["Seña sostenida", "Misma postura durante varios fotogramas", "Sonar una vez", "Periodo refractario y suelta"],
       ["Parpadeo del rastreo", "La mano se pierde 1 o 2 fotogramas", "No repetir", "Umbral de suelta de 6 fotogramas"]],
      "Fuente: elaboración propia a partir del código y de las pruebas del repositorio.", [3.0, 4.6, 3.3, 5.1])
H2("Objetivo")
T("Describir el reconocedor de señas de Hand Sing Kids y medir, en laboratorio y con perturbaciones simuladas, cuántas señas válidas reconoce y cuántas notas dispara por error, frente al método de la versión inicial.")

H1("Métodos")
H2("Sistema")
T("La aplicación es de escritorio, escrita en Python. La cámara alimenta a MediaPipe Hands; el descriptor y el clasificador convierten los 21 puntos de cada mano en una nota candidata; un estabilizador decide "
  "si la nota se confirma; y la capa pedagógica usa esa nota para registrar el intento y elegir la siguiente actividad (Figura 1). Este trabajo estudia solo la parte perceptiva, hasta la confirmación de la nota.")
figura(["arquitectura.png"], 14.0, "Figura 1. Arquitectura funcional de Hand Sing Kids; el reconocedor ocupa los primeros bloques.")
bloque("descriptor")
bloque("estabilizacion")
bloque("protocolo")

H1("Resultados")
bloque("res_aciertos")
bloque("res_fp")
bloque("res_separ")

H1("Discusión")
T("**Qué se ganó y qué se perdió.** La comparación entre métodos no debe leerse como una victoria completa. El método de la versión inicial reconoce todas las señas porque convierte toda postura en la nota más parecida, y por eso "
  "su tasa de acierto es perfecta y su tasa de notas falsas, total. El método propuesto acepta menos: con ruido de 0,09 baja a 86,0 %. Esa pérdida es el precio de rechazar lo dudoso. En un juego infantil, "
  "pedir que se repita una seña cuesta unos segundos; una nota falsa interrumpe la actividad y puede enseñar un sonido equivocado.")
T("**Dónde está el error que queda.** Las transiciones explican casi todos los falsos positivos y las manos cruzadas casi ninguno. Una postura a medio camino hereda rasgos de las dos señas extremas y puede parecerse "
  "a una de ellas; una mano de cada seña, en cambio, no se parece a ninguna. Esto sugiere un siguiente paso concreto: usar la velocidad de la mano como señal adicional, porque una postura en movimiento rápido "
  "difícilmente es una seña deliberada. El código actual no usa velocidad en la decisión.")
T("**Amenazas a la validez.** La calibración es de una sola persona y de ocho señas, y no se conoce la variabilidad entre niños; las perturbaciones se simularon sobre coordenadas ya extraídas, de modo que no incluyen "
  "errores de detección, desenfoque ni iluminación; las posturas negativas se construyeron por interpolación y combinación y la tasa real depende de cómo se mueven los niños; y el método inicial se evaluó con "
  "la misma calibración. Por eso los resultados describen el comportamiento del reconocedor en laboratorio y no su rendimiento en el aula.")
resto("Los demás componentes del sistema, como el seguimiento del dominio, el repaso espaciado y la selección de actividades, se tratan en otros trabajos del equipo y en la literatura sobre aprendizaje adaptativo")
bloque("trl")

H1("Conclusiones")
T(f"Un descriptor invariante de 120 componentes con decisión por distancia, confianza y margen redujo las notas disparadas por error de 100 % a {f(FP['pct'])} % en 640 posturas que no son seña, "
  f"con un costo en sensibilidad visible solo con ruido alto ({f(A[3]['nuevo']['pct'])} % con 0,09). El error que queda se concentra en las transiciones. El reconocedor se comporta como se describe en laboratorio; "
  "no se ha medido en niños, y el nivel de madurez es TRL 4.")
H1("Recomendaciones")
T("(1) Calibrar y medir con varios niños y en el aula, con iluminación y cámaras reales. (2) Incorporar la velocidad de la mano a la decisión y medir si reduce los falsos positivos de las transiciones. "
  "(3) Registrar las notas falsas durante un piloto en lugar de simularlas. (4) Medir la latencia de extremo a extremo, incluida la cámara.")
declaraciones(dict(
    cred="Contribución de los autores (CRediT, por confirmar por el equipo): el primer autor planteó la evaluación del reconocedor, ejecutó las mediciones y redactó el borrador; los demás autores participaron en el desarrollo del "
         "software, la revisión bibliográfica y la revisión del texto; Cristian Javier Cano-Mogollón supervisó y revisó el manuscrito.",
    fin="Esta investigación no recibió financiación externa. [Por confirmar por el equipo.]",
    conf="Los autores declaran que no existen conflictos de intereses relacionados con esta publicación. [Por confirmar.]",
    cons="No aplica. La calibración de referencia contiene solo coordenadas de puntos de la mano de una persona, sin imágenes, y no se recolectaron datos de niños.",
    irb="No aplica, porque el estudio es una evaluación técnica de laboratorio. Una prueba con niños requerirá aprobación ética y consentimiento de los acudientes.",
    datos="El código, la calibración de referencia, las pruebas y los scripts de evaluación están en el repositorio del proyecto. Las salidas de las mediciones (resultados_vision.json) y la verificación de referencias están en la carpeta de análisis de la entrega.",
    ia="Se usó un asistente de inteligencia artificial (Claude, de Anthropic) para apoyar el análisis del código, la ejecución de las mediciones, la verificación de referencias y la redacción de borradores. Los autores revisaron el contenido y responden por él.",
    en="Author Contributions: the first author designed the recognizer evaluation, ran the measurements and drafted the manuscript; the other authors contributed software development, literature review and text review; C. J. Cano-Mogollón supervised and reviewed. Funding: none external. No conflicts of interest. Informed consent and IRB: not applicable (laboratory evaluation). Data and code: project repository and analysis folder."))
cierre(autores, TITULO_ES, "Qué mano es una seña: reconocimiento en Hand Sing Kids", Path(sys.argv[1]))
