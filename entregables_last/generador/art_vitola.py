"""Artículo — primer autor: Antolin De Jesús Vitola Montes. Hilo: acceso y valor pedagógico; la fonomimia llevada a la pantalla (hipótesis de impacto en Córdoba)."""
import sys
from nucleo_hsk import *
import nucleo_hsk as N

A = R["aciertos"]; FP = R["falsos_positivos"]["global_nuevo"]

TITULO_ES = ("Las manos como instrumento: una herramienta digital de bajo requerimiento para enseñar las notas musicales a niños en Montería y Córdoba")
TITULO_EN = ("Hands as an instrument: a low-requirement digital tool to teach musical notes to children in Montería and Córdoba")
RES_ES = ("Enseñar música exige instrumentos, espacios y docentes que no siempre están disponibles. Hand Sing Kids propone usar las manos, como lo hacía la fonomimia del siglo XIX, y una cámara que reconoce ocho señas "
          "para las notas de Do3 a Do4, de modo que el niño reciba una respuesta inmediata sin necesidad de un instrumento. Este trabajo presenta la propuesta desde su pertinencia pedagógica y su viabilidad técnica en "
          "Montería y Córdoba, donde el DANE proyecta para 2026 una población de 535.052 habitantes, 80.254 de ellos entre 3 y 12 años. La aplicación corre en un computador con cámara, guarda sus datos en una base local y "
          "no necesita conexión a internet. En laboratorio, con una calibración de una persona y perturbaciones simuladas, reconoció 480 de 480 señas sin ruido y evitó notas falsas en la mayoría de 640 posturas "
          f"que no son seña ({f(FP['pct'])} % de errores frente a 100 % del método inicial). No hubo pruebas con niños. Se formulan tres hipótesis de impacto y un plan para validarlas; el nivel de madurez es TRL 4.")
RES_EN = ("Teaching music requires instruments, spaces and teachers that are not always available. Hand Sing Kids proposes using the hands, as nineteenth-century hand-sign solfège did, and a camera that recognizes eight signs "
          "for the notes from C3 to C4, so that the child receives immediate feedback without an instrument. This paper presents the proposal from its pedagogical relevance and technical feasibility in Montería and Córdoba, "
          "where DANE projects a 2026 population of 535,052, of whom 80,254 are between 3 and 12 years old. The application runs on a computer with a camera, stores its data locally and needs no internet connection. "
          "In the laboratory, with a single-person calibration and simulated perturbations, it recognized 480 of 480 signs without noise and avoided false notes in most of 640 non-sign postures "
          f"({f(FP['pct'])} % errors against 100 % for the initial method). No tests with children were done. Three impact hypotheses and a validation plan are stated; the readiness level is TRL 4.")
KW_ES = "educación musical infantil; fonomimia; acceso a instrumentos; aprendizaje con gestos; tecnología accesible; Montería; Córdoba"
KW_EN = "children's music education; hand-sign solfège; access to instruments; gesture-based learning; accessible technology; Montería; Córdoba"
autores = encabezado("Vitola", TITULO_ES, TITULO_EN, RES_ES, RES_EN, KW_ES, KW_EN)

H1("Introducción")
H2("Una idea antigua, una oportunidad nueva")
T("Desde mediados del siglo XIX, John Curwen popularizó en el Reino Unido un sistema de señas manuales para las notas de la escala, que más tarde se difundió en la enseñanza musical infantil. La idea es simple: "
  "cada nota tiene una posición de la mano, y el niño la ve, la hace y la canta. Su fortaleza pedagógica es que no necesita ningún instrumento, solo un cuerpo y alguien que corrija. Su debilidad es esa misma: "
  "sin un docente atento, la seña se hace de cualquier manera y nadie le dice al niño si acertó.")
T("Hoy una cámara y un modelo de seguimiento de manos pueden cumplir el papel de quien corrige. La atención a la tecnología digital en la educación musical infantil es creciente, y las revisiones sobre inteligencia "
  "artificial en la primera infancia la describen como un campo en expansión {c:yi}, con trabajos sobre aplicaciones móviles y realidad aumentada en música {c:apay,barroso,leon}. En Colombia y en Córdoba, un "
  "primer obstáculo es práctico: pocos centros educativos tienen instrumentos suficientes, y una herramienta que dependa de internet o de equipos costosos tendría el mismo problema.")
T("En Montería, las proyecciones municipales del DANE para 2026 indican 535.052 habitantes, de los cuales 80.254 tienen entre 3 y 12 años {c:dane}. No se aporta aquí una estadística local sobre la educación "
  "musical: no la hay en las fuentes revisadas. La justificación del proyecto es de diseño. Hand Sing Kids se ejecuta en un computador con cámara, guarda sus datos en una base local y no necesita conexión, "
  "lo que lo hace una candidata razonable para probarse en aulas de la región. Que realmente ayude a aprender es una hipótesis que este trabajo no puede confirmar.")
H2("Qué ofrece la propuesta frente a la enseñanza tradicional")
tabla("Tabla 1. Lo que aporta una herramienta basada en gestos frente a la enseñanza tradicional con señas",
      ["Aspecto", "Enseñanza tradicional con señas", "Hand Sing Kids", "Qué falta demostrar"],
      [["Corrección de la seña", "Depende de la atención del docente", "Respuesta inmediata por reconocimiento", "Que la corrección sea comprensible para el niño"],
       ["Ritmo de avance", "Igual para todo el grupo", "Se ajusta al dominio de cada niño", "Que mejore la retención frente a una secuencia fija"],
       ["Motivación", "Canto y juego del docente", "Canciones y retroalimentación sonora", "Que mantenga la atención en sesiones reales"],
       ["Requisitos", "Docente formado", "Computador con cámara; sin internet", "Que el docente la adopte y pueda calibrarla"],
       ["Registro", "Observación informal", "Registro de intentos por habilidad", "Uso del registro por el docente, con consentimiento"]],
      "Fuente: elaboración propia a partir del diseño del sistema; la columna final son hipótesis, no resultados.", [3.0, 4.2, 4.4, 4.4])
H2("Objetivo")
T("Presentar Hand Sing Kids desde su pertinencia pedagógica y su viabilidad técnica en laboratorio, y formular las hipótesis y el plan de validación que permitirían probar su utilidad con niños en Montería y Córdoba.")

H1("Métodos")
H2("Diseño del sistema")
T("Cada nota de Do3 a Do4 se asocia a una seña de las dos manos. La cámara capta las manos y MediaPipe Hands entrega 21 puntos por mano {c:mediapipe}; un descriptor invariante al tamaño, la posición y el giro "
  "convierte esos puntos en un vector de 120 componentes, y un clasificador decide si hay una seña y cuál es. Después, un modelo de dominio estima qué sabe el niño de cada nota y un optimizador arma la siguiente "
  "sesión (Figura 1). Todo se guarda en una base SQLite local. El método de reconocimiento se detalla en otro trabajo del equipo; aquí interesa su comportamiento medido.")
figura(["arquitectura.png"], 14.5, "Figura 1. Arquitectura funcional de Hand Sing Kids.")
H2("Evaluación técnica")
T("La evaluación fue de laboratorio. Se usó una calibración de las ocho señas de una persona, guardada como coordenadas sin imágenes, y perturbaciones simuladas de tamaño, giro y ruido. Se midió el reconocimiento de "
  "480 señas válidas por nivel de ruido y las notas disparadas por error en 640 posturas que no son seña, con intervalos de Wilson al 95 % {c:wilsonci}. No se hicieron pruebas con niños.")
H1("Resultados")
H2("Lo que se midió")
tabla("Tabla 2. Evidencia técnica disponible, que no equivale a evidencia pedagógica",
      ["Medida", "Resultado", "Qué dice sobre el uso en el aula"],
      [["Señas válidas reconocidas, sin ruido y ruido 0,03", f"{f(A[0]['nuevo']['pct'], 0)} % (480 de 480 por nivel)", "El reconocedor distingue las ocho señas de la calibración"],
       ["Señas válidas con ruido 0,06 y 0,09", f"{f(A[2]['nuevo']['pct'])} % y {f(A[3]['nuevo']['pct'])} %", "Con mucha variación, el sistema prefiere abstenerse; el niño repetiría la seña"],
       ["Notas disparadas por error, 640 posturas", f"{f(FP['pct'])} % (IC 95 %: {f(FP['ic95_lo'])}–{f(FP['ic95_hi'])})", "Pocas notas que el niño no pidió; frente a 100 % del método inicial"],
       ["Baterías de prueba del repositorio", "8 de 8 sin fallos", "El software se comporta como está especificado"],
       ["Niños que probaron el sistema", "0", "No se puede afirmar nada sobre aprendizaje"]],
      "Fuente: analisis/resultados_vision.json y salida de las pruebas del repositorio.", [5.0, 4.6, 6.4])
T("La Tabla 2 separa con claridad lo que se sabe de lo que no. El sistema funciona en laboratorio como se describe; si ayuda a aprender música es una pregunta abierta, porque ningún niño lo ha usado en una prueba formal.")
bloque("trl")

H1("Discusión")
T("**Un docente que no se cansa, no un reemplazo.** La propuesta no sustituye a un maestro de música: replica una función concreta, la de decirle al niño si la seña salió bien, y la ofrece en cualquier momento. Esto es "
  "coherente con la idea de que estas herramientas complementan la enseñanza tradicional y no la reemplazan, siempre que tengan objetivos pedagógicos claros. La evidencia internacional muestra el interés por estas tecnologías, "
  "pero todavía no hay estudios sobre este tipo de entrada, una seña por nota, en aulas de la región.")
T("**El requisito más barato es el más importante.** Que no haga falta internet ni un instrumento es una decisión de diseño que se puede verificar, y es la que hace plausible llevar la herramienta a una escuela con "
  "recursos limitados. En cambio, otros requisitos todavía no se han medido: cuánta luz necesita la cámara, qué tan rápido responde de principio a fin y si un docente sin formación técnica puede calibrar la aplicación "
  "para cada niño. Son las primeras preguntas de un piloto.")
T("**Qué haría falta para saber si funciona.** El plan mínimo es comparar, con grupos de niños de instituciones de Montería, el desempeño de quienes usan la herramienta con el de quienes aprenden con el método "
  "tradicional, midiendo antes y después el reconocimiento de las notas, y recoger la opinión del docente. Como se trabaja con menores, ese plan requiere aprobación ética, consentimiento de los acudientes y una revisión "
  "de la normativa colombiana sobre datos personales. Mientras eso no ocurra, los resultados de este trabajo son técnicos.")
resto("Los componentes de reconocimiento, estabilización, dominio y selección de sesión se apoyan en trabajos sobre aprendizaje personalizado, retroalimentación con IA, afecto y práctica distribuida")

H1("Conclusiones")
T("Hand Sing Kids lleva una idea pedagógica antigua, enseñar las notas con las manos, a una herramienta que corre en un computador con cámara y sin internet. En laboratorio reconoce las señas de su calibración y evita casi todas las "
  "notas falsas. Su utilidad para el aprendizaje en Montería y Córdoba no está demostrada y depende de un piloto con niños, con docentes y con las autorizaciones éticas correspondientes.")
H1("Recomendaciones")
T("(1) Diseñar el piloto comparativo con una institución y un docente aliados. (2) Medir la latencia de extremo a extremo y las condiciones de iluminación necesarias. (3) Probar si un docente puede calibrar la herramienta sin apoyo técnico. "
  "(4) Obtener la aprobación ética y el consentimiento informado antes de cualquier recolección de datos de menores.")
declaraciones(dict(
    cred="Contribución de los autores (CRediT, por confirmar): el primer autor formuló la justificación pedagógica y las hipótesis de impacto y redactó el borrador; los demás autores aportaron el desarrollo del software, "
         "las mediciones y la revisión; Cristian Javier Cano-Mogollón supervisó y revisó el manuscrito.",
    fin="No se recibió financiación externa para este trabajo. [Por confirmar.]",
    conf="Los autores declaran no tener conflictos de intereses. [Por confirmar.]",
    cons="No aplica; no se recolectaron datos de niños. La prueba piloto requerirá consentimiento informado de los acudientes.",
    irb="No aplica para esta evaluación técnica de laboratorio; el piloto con menores requerirá aprobación de un comité de ética.",
    datos="El código, la calibración de referencia (solo coordenadas, sin imágenes), las pruebas y los scripts de evaluación están en el repositorio del proyecto; las salidas numéricas están en la carpeta de análisis de la entrega.",
    ia="Se utilizó el asistente Claude (Anthropic) como apoyo en el análisis del código, la ejecución de las mediciones, la verificación de referencias y la redacción de borradores; los autores revisaron y asumen el contenido.",
    en="Author Contributions: the first author formulated the pedagogical rationale and the impact hypotheses and drafted the manuscript; the other authors contributed software development, measurements and review; C. J. Cano-Mogollón supervised. No external funding. No conflicts of interest. Consent and IRB: not applicable to this laboratory evaluation; a pilot with minors will require both. Data and code: project repository."))
cierre(autores, TITULO_ES, "Las manos como instrumento: Hand Sing Kids en Montería y Córdoba", Path(sys.argv[1]))
