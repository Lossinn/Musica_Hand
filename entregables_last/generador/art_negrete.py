"""Artículo — primer autor: Andrés Julián Negrete Pacheco. Hilo: el tiempo y la retroalimentación; que la nota suene cuando el niño la espera."""
import sys
from nucleo_hsk import *
import nucleo_hsk as N

A = R["aciertos"]; FP = R["falsos_positivos"]["global_nuevo"]; LT = R["latencia"]

TITULO_ES = ("Cuándo debe sonar la nota: estabilización temporal, ventanas de acierto y retroalimentación en el módulo de canciones de Hand Sing Kids")
TITULO_EN = ("When the note should sound: temporal stabilization, hit windows and feedback in the songs module of Hand Sing Kids")
RES_ES = ("En una aplicación que enseña notas con las manos, reconocer bien no basta: la nota debe sonar en el momento en que el niño la espera, una sola vez y sin castigarlo por el tiempo que el sistema tarda en confirmar. "
          "Se describen y analizan los mecanismos temporales de Hand Sing Kids: el estabilizador que confirma una nota con periodo refractario y detección de suelta, y el motor del módulo Canciones, que usa el reloj de la partida, "
          "una ventana de acierto asimétrica y un puntaje con combo. Se explican la ventana mínima de 480 ms, el umbral de suelta de seis fotogramas y el efecto del parpadeo del seguimiento de manos, que provocó "
          f"que una misma nota sonara dos veces. El descriptor y el clasificador tardan {f(LT['media_ms'], 2)} ms por fotograma en promedio ({f(LT['p95_ms'], 2)} ms en el percentil 95), sin contar cámara ni dibujo en pantalla. "
          f"En laboratorio, el método disparó una nota por error en {f(FP['pct'])} % de 640 posturas que no son seña. No hubo pruebas con niños; el diseño temporal es una propuesta por validar con ellos, y el nivel de madurez es TRL 4.")
RES_EN = ("In an application that teaches notes with the hands, recognizing well is not enough: the note must sound when the child expects it, once, and without penalizing the child for the time the system takes to confirm. "
          "The temporal mechanisms of Hand Sing Kids are described and analysed: the stabilizer that confirms a note with a refractory period and release detection, and the engine of the Songs module, which uses the game clock, "
          "an asymmetric hit window and a combo score. The 480 ms minimum window, the six-frame release threshold and the effect of hand-tracking flicker, which made one note sound twice, are explained. "
          f"The descriptor and classifier take {f(LT['media_ms'], 2)} ms per frame on average ({f(LT['p95_ms'], 2)} ms at the 95th percentile), excluding camera and display. "
          f"In the laboratory, the method fired a wrong note in {f(FP['pct'])} % of 640 non-sign postures. No tests with children were done; the temporal design is a proposal to be validated with them, and the readiness level is TRL 4.")
KW_ES = "retroalimentación; estabilización temporal; ventana de acierto; periodo refractario; gamificación; educación musical infantil; Montería"
KW_EN = "feedback; temporal stabilization; hit window; refractory period; gamification; children's music education; Montería"
autores = encabezado("Negrete", TITULO_ES, TITULO_EN, RES_ES, RES_EN, KW_ES, KW_EN)

H1("Introducción")
H2("El momento de la respuesta")
T("Cuando un niño hace una seña y espera oír la nota, cada décima de segundo cuenta. Si el sonido llega muy tarde, el niño no lo asocia con su gesto; si llega antes de que termine de formar la seña, suena una nota "
  "equivocada; si suena dos veces, cree que se equivocó. El problema de reconocer una seña ya es difícil por sí mismo, pero el de decidir cuándo confirmarla es distinto y, en una aplicación de juego, pesa tanto como el primero.")
T("Hand Sing Kids reconoce ocho señas de dos manos, de Do3 a Do4, con una cámara y MediaPipe Hands {c:mediapipe}. La herramienta ofrece actividades guiadas y un módulo de canciones en que el niño debe producir las notas "
  "al compás de una melodía. En el segundo caso, el sistema no espera la seña: el tiempo lo marca el reloj de la partida y el niño debe acertar dentro de una ventana. Eso obliga a decidir qué tan ancha es esa ventana y "
  "cuánto del retraso del reconocimiento se le perdona al niño.")
H2("Trabajos relacionados")
T("La retroalimentación con inteligencia artificial en la enseñanza de piano se ha estudiado en cuanto a exactitud técnica {c:deng_piano} y la detección visual del teclado con aprendizaje profundo ya existe {c:chulu}. "
  "Otros trabajos proponen trayectorias de aprendizaje personalizadas {c:li_hong,li_peerj,li_disc,tang,wang}, sistemas con emoción {c:deng_sci,shi} y análisis de aplicaciones móviles de música {c:apay,barroso,leon}. "
  "En los títulos revisados, ninguno describe el diseño temporal de una entrada por seña manual; no se leyeron los textos completos. Para la dificultad de las actividades se usa una idea conocida del aprendizaje: "
  "que la práctica es más eficiente cuando el error ni es muy raro ni muy frecuente {c:wilson85}.")
tabla("Tabla 1. Fallas temporales posibles en un juego de gestos y el mecanismo que las atiende",
      ["Falla percibida por el niño", "Causa técnica", "Mecanismo en Hand Sing Kids"],
      [["La nota suena dos veces", "El rastreo pierde la mano uno o dos fotogramas y se cree que la soltó", "Umbral de suelta de seis fotogramas consecutivos"],
       ["La nota suena muy seguido", "Lecturas repetidas de la misma seña", "Periodo refractario de 0,45 s"],
       ["Acierta pero no suma", "La confirmación llega después de la línea", "Ventana más ancha antes de la línea que después"],
       ["No puede seguir canciones rápidas", "Ventana que se encoge con el tempo", "Ventana mínima de 480 ms"],
       ["Puntaje que no refleja el esfuerzo", "Una sola categoría de acierto", "Perfecto, bien o vale, con combo hasta ×4"]],
      "Fuente: elaboración propia a partir del código y de la documentación del proyecto.", [4.5, 5.5, 6.0])
H2("Objetivo")
T("Describir con precisión los mecanismos temporales de Hand Sing Kids, mostrar qué errores previene cada uno y cuantificar, con las fórmulas del código, el efecto del tempo sobre la ventana de acierto.")

H1("Métodos")
H2("Estabilizador de notas")
T("Entre la lectura de la cámara y el sonido hay un estabilizador. Una nota se confirma si el clasificador la ve con confianza suficiente, si pasaron al menos 0,45 s desde la nota anterior (periodo refractario) y, si es la "
  "misma nota que la última, solo cuando el niño la soltó. Se considera soltada cuando seis fotogramas consecutivos arrojan una lectura distinta. En su configuración por defecto, el estabilizador usa una ventana de un fotograma, "
  "de modo que la nota suena en cuanto se reconoce, sin barra de espera.")
T("El valor de seis fotogramas merece una explicación porque cambió. La documentación del proyecto menciona dos fotogramas, y el código usa seis. La diferencia no es un descuido: con la ventana de varios fotogramas, la votación "
  "absorbía los parpadeos del rastreo; al pasar a un fotograma, el mecanismo de suelta quedó como único filtro y dos fotogramas resultaron insuficientes. Aquí se adopta el valor del código.")
bloque("canciones")
H2("Cálculo de la ventana")
T("Para estudiar el efecto del tempo se calculó, con la ecuación de la ventana, su ancho total $2h_i$ y su reparto antes y después de la línea para distintos tempos, suponiendo que la tolerancia $\\text{tol}$ no limita el valor, "
  "es decir, que $\\min(\\text{tol},0{,}85\\,g)=0{,}85\\,g$. Es un cálculo derivado de la fórmula, no una medición.")
H1("Resultados")
H2("Efecto del tempo sobre la ventana de acierto")
filas = []
for bpm in (40, 60, 80, 100, 120):
    g = 60000 / bpm; w = max(480, 0.85 * g); h = w / 2
    filas.append([str(bpm), m(g), m(0.85 * g), m(w), m(1.15 * h), m(0.85 * h)])
tabla("Tabla 2. Ventana de acierto según el tempo (ms), con tolerancia no limitante",
      ["Tempo (bpm)", "Intervalo entre notas g", "0,85·g", "Ancho de ventana", "Antes de la línea", "Después de la línea"], filas,
      "Fuente: cálculo propio con la ecuación de la ventana; W_min = 480 ms.", [2.2, 3.0, 2.2, 3.0, 2.9, 2.9])
T("Hasta unos 100 bpm la ventana depende solo del intervalo entre notas, y a partir de ahí actúa el piso de 480 ms: a 120 bpm, el 85 % del intervalo es de 425 ms y la ventana se mantiene en 480 ms, con 276 ms antes y 204 ms después de la línea. "
  "La asimetría hace que el niño tenga más margen para adelantarse que para retrasarse, lo que compensa el tiempo que tarda el reconocimiento en confirmar. En el factor de tempo más rápido del módulo (1,15), "
  "esto importa más que en el más lento (0,72).")
H2("Costo del reconocimiento en el tiempo de respuesta")
T(f"El descriptor y el clasificador tardaron {f(LT['media_ms'], 2)} ms por fotograma en promedio, con percentil 95 de {f(LT['p95_ms'], 2)} ms y máximo de {f(LT['max_ms'], 2)} ms en {LT['reps']} repeticiones, en un solo equipo. Esa cifra es una fracción "
  "pequeña de la ventana mínima de 480 ms, pero no incluye la captura de la cámara, el rastreo de MediaPipe ni el dibujo en pantalla, que no se midieron. Por eso la latencia de extremo a extremo sigue siendo una incógnita.")
H2("Falsos positivos y respuesta inmediata")
T(f"Con una ventana de un fotograma, el método disparó una nota por error en {f(FP['pct'])} % de 640 posturas que no son seña (IC 95 %: {f(FP['ic95_lo'])} a {f(FP['ic95_hi'])} %), casi todo en transiciones. Con votación de varios fotogramas, "
  "ese error se reduce, pero a cambio de una espera perceptible. Para niños pequeños se prefirió la respuesta inmediata, y la ventana puede ampliarse por niño desde los ajustes de la aplicación.")

H1("Discusión")
T("**Un caso de efecto cruzado.** Una nota sostenida sonaba dos veces. El clasificador no tenía la culpa: el rastreo de manos pierde la mano uno o dos fotogramas aunque esté quieta, y con ventana de un fotograma eso se "
  "leía como suelta, de modo que la siguiente lectura repetía la nota. Cuando se quitó la votación, el umbral de suelta, que antes casi no importaba, pasó a ser crítico. La enseñanza es que un parámetro cambiado en un módulo "
  "puede dejar a otro cargando con una función que nunca se probó por separado. Por eso la batería del estabilizador incluye ahora una prueba del parpadeo breve.")
T("**Qué se le exige al niño y qué al sistema.** Con una ventana asimétrica y un piso de 480 ms, el sistema asume parte del retraso en lugar de cargarlo al niño. El puntaje de 100, 70 o 50 puntos y el combo con tope ×4 "
  "responden a una idea sencilla: reconocer el esfuerzo sin esconder los errores. No hay evidencia de que estos valores motiven a un niño; provienen de decisiones de diseño y de la documentación del proyecto, y "
  "habría que ajustarlos con observación en el aula.")
T("**Límites.** La Tabla 2 es un cálculo, no una medición. Las constantes del estabilizador y del puntaje no se validaron con niños; la latencia de extremo a extremo no se midió; y las mediciones de falsos positivos "
  "usan posturas simuladas. Un piloto debería registrar, con niños reales, cuántas veces suena una nota dos veces, cuánto tarda el sonido desde la seña y cuántas veces el niño repite una seña porque no sonó.")
resto("Para las demás partes del sistema, como la estimación del dominio y la selección de la sesión, véanse los trabajos sobre práctica distribuida, seguimiento del conocimiento y rutas personalizadas")
H1("Conclusiones")
T("Hand Sing Kids resuelve el problema del tiempo con tres piezas: un estabilizador con periodo refractario y detección de suelta, una ventana de acierto asimétrica con piso de 480 ms y un puntaje con combo. Se explicó por qué "
  "el umbral de suelta es de seis fotogramas y cómo el tempo reparte la ventana antes y después de la línea. Las constantes provienen del diseño y no de datos de niños; el nivel de madurez es TRL 4.")
H1("Recomendaciones")
T("(1) Medir la latencia de extremo a extremo con la cámara real. (2) Registrar, en un piloto, las notas duplicadas y las señas repetidas. (3) Ajustar el piso de la ventana y el puntaje con observaciones de niños y docentes. "
  "(4) Mantener la prueba del parpadeo breve en la batería del estabilizador.")
declaraciones(dict(
    cred="Contribución de los autores (CRediT, por confirmar): el primer autor analizó los mecanismos temporales, calculó la ventana de acierto y redactó el borrador; los demás autores aportaron el desarrollo del software, "
         "las mediciones y la revisión; Cristian Javier Cano-Mogollón supervisó y revisó.",
    fin="Sin financiación externa. [Por confirmar por el equipo.]",
    conf="No hay conflictos de intereses que declarar. [Por confirmar.]",
    cons="No aplica: no se recolectaron datos de niños en este estudio.",
    irb="No aplica a esta evaluación técnica; las pruebas de aula con menores necesitarán aprobación ética y consentimiento de acudientes.",
    datos="El código, las pruebas del estabilizador y de canciones y los scripts de medición están en el repositorio del proyecto; los cálculos de la Tabla 2 se pueden reproducir con la ecuación de la ventana y los valores del código.",
    ia="Se empleó un asistente de IA (Claude, de Anthropic) para revisar el código, ejecutar las mediciones, verificar referencias y redactar borradores. Los autores revisaron y responden por el texto.",
    en="Author Contributions: the first author analysed the temporal mechanisms, computed the hit window and drafted the manuscript; the other authors contributed software, measurements and review; C. J. Cano-Mogollón supervised. No external funding. No conflicts of interest. Consent and IRB: not applicable. Data and code: project repository."))
cierre(autores, TITULO_ES, "Cuándo debe sonar la nota: tiempo y retroalimentación en Hand Sing Kids", Path(sys.argv[1]))
