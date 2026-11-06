"""Artículo — primer autor: Angel Quintana Jiménez. Hilo: optimización; la sesión como problema de programación entera mixta con óptimo exacto."""
import sys
from nucleo_hsk import *
import nucleo_hsk as N

TITULO_ES = ("Elegir la sesión óptima: programación entera mixta con verificación exacta para planificar las actividades de Hand Sing Kids")
TITULO_EN = ("Choosing the optimal session: mixed-integer programming with exact verification to plan the activities of Hand Sing Kids")
RES_ES = ("Después de cada intento, una aplicación de enseñanza debe decidir qué actividades componen la siguiente sesión, con un tiempo limitado y sin repetir lo mismo. Se formula esa decisión en Hand Sing Kids, que enseña las ocho notas de "
          "Do3 a Do4 con señas de las manos, como un problema de programación entera mixta: se maximiza una combinación de ganancia de aprendizaje, urgencia de repaso y motivación, menos la fatiga inducida, sujeta a restricciones "
          "de tiempo total, tamaño de la sesión, prerrequisitos, al menos una actividad lúdica, dificultad media acotada, un máximo de dos actividades por habilidad y la inclusión de un repaso vencido. La ganancia concentra el valor en una "
          "probabilidad de éxito esperada de 0,75. El problema se resuelve con el solucionador CBC mediante PuLP y, si este no está disponible, por enumeración exhaustiva mientras el número de combinaciones no supere 4×10^5, lo que "
          "entrega el óptimo exacto. La prueba del repositorio que compara ambos métodos pasó, y la sesión de ejemplo se resolvió en 40 ms con valor objetivo 2,9524. Los pesos y las restricciones son decisiones de diseño, no se calibraron con "
          "datos de niños, y el beneficio pedagógico de la sesión óptima es una hipótesis. El nivel de madurez es TRL 4.")
RES_EN = ("After each attempt, a teaching application must decide which activities make up the next session, with limited time and without repeating the same thing. This decision is formulated in Hand Sing Kids, which teaches the eight notes from "
          "C3 to C4 with hand signs, as a mixed-integer program: a combination of learning gain, review urgency and motivation, minus induced fatigue, is maximized subject to total time, session size, prerequisites, at least one playful activity, "
          "bounded mean difficulty, at most two activities per skill and the inclusion of an overdue review. The gain concentrates value on an expected success probability of 0.75. The problem is solved with the CBC solver through PuLP and, if it is "
          "unavailable, by exhaustive enumeration while the number of combinations does not exceed 4×10^5, which gives the exact optimum. The repository test comparing both methods passed, and the example session was solved in 40 ms with objective value 2.9524. "
          "Weights and constraints are design decisions, not calibrated with children's data, and the pedagogical benefit of the optimal session is a hypothesis. The readiness level is TRL 4.")
KW_ES = "programación entera mixta; optimización; planificación de sesiones; aprendizaje adaptativo; educación musical infantil; solucionador CBC; Montería"
KW_EN = "mixed-integer programming; optimization; session planning; adaptive learning; children's music education; CBC solver; Montería"
autores = encabezado("Quintana", TITULO_ES, TITULO_EN, RES_ES, RES_EN, KW_ES, KW_EN)

H1("Introducción")
H2("Una decisión con restricciones")
T("Planificar una sesión de práctica parece sencillo hasta que se escriben las condiciones. Hay un tiempo máximo; hay un número fijo de actividades; algunas actividades exigen haber dominado antes una habilidad; no conviene que una sesión "
  "sea toda de actividades difíciles ni que repita tres veces la misma nota; debería incluir algo lúdico y, si hay un repaso vencido, atenderlo. Escoger a mano entre decenas de actividades con todas esas reglas es lo que en la "
  "investigación de operaciones se llama un problema de optimización con restricciones, y una regla heurística simple, como elegir las actividades más rentables una por una, puede violar alguna de ellas o perder una combinación mejor.")
T("En la literatura reciente de educación musical con inteligencia artificial, la planificación suele resolverse con aprendizaje por refuerzo o con redes profundas {c:li_hong,li_peerj,li_disc,tang,wang}, que aprenden la política a partir "
  "de datos. Aquí no hay datos de niños, y el equipo prefirió una formulación explícita, cuyas reglas el docente puede leer y cuyo óptimo se puede comprobar. Otros trabajos incorporan emoción {c:deng_sci,shi}, retroalimentación en piano {c:deng_piano,chulu} "
  "o dificultad de la partitura {c:ramoneda}; las revisiones generales {c:yi} y los estudios de aplicaciones {c:apay,barroso,leon} completan el panorama.")
H2("Lo que aporta una formulación exacta")
tabla("Tabla 1. Comparación de enfoques para planificar la sesión",
      ["Enfoque", "Necesita datos de niños", "Explicable al docente", "Garantiza óptimo", "Estado en Hand Sing Kids"],
      [["Regla heurística (codiciosa)", "No", "Sí", "No", "No se usa"],
       ["Aprendizaje por refuerzo", "Sí", "Difícil", "No", "Interfaz documentada, sin datos"],
       ["Programación entera mixta (CBC)", "No", "Sí, restricciones legibles", "Sí", "Implementado"],
       ["Enumeración exhaustiva", "No", "Sí", "Sí, si hay pocas combinaciones", "Respaldo y verificación"]],
      "Fuente: elaboración propia a partir del diseño del sistema; no es una revisión de la literatura.", [4.0, 2.8, 3.2, 2.6, 3.4])
H2("Objetivo")
T("Formular la selección de la sesión de Hand Sing Kids como un problema de programación entera mixta, mostrar cómo se verifica su óptimo y declarar qué parámetros son decisiones de diseño y no datos.")

H1("Métodos")
H2("Entradas del optimizador")
T("El optimizador recibe, del modelo de dominio, el valor estimado de cada habilidad y la urgencia de repaso, y recibe del catálogo las actividades candidatas, con su duración, su dificultad, las habilidades que toca y su tipo. "
  "No necesita saber cómo se estimó el dominio: ese es el trabajo de la capa anterior (Figura 1). La salida es el conjunto de actividades que forman la sesión.")
figura(["arquitectura.png"], 14.0, "Figura 1. Arquitectura de Hand Sing Kids; el optimizador está en la capa pedagógica.")
bloque("milp")
H2("Verificación")
T("El solucionador CBC se invoca mediante PuLP. Como respaldo, y como forma de verificar, el sistema enumera todas las combinaciones de $K$ actividades cuando su número no supera $4\\times10^{5}$ y toma la de mayor valor que "
  "cumple las restricciones. La prueba del repositorio compara ambos resultados sobre una sesión de ejemplo.")

H1("Resultados")
H2("Coincidencia con la enumeración exacta")
T("La batería del optimizador terminó con código de salida 0. La prueba que compara el resultado del solucionador con la enumeración exacta pasó, y la sesión de ejemplo se resolvió con CBC en 40 ms con un valor objetivo de 2,9524. "
  "Un tiempo de 40 ms es compatible con recalcular la sesión tras cada intento en un computador común, aunque no se midió en un equipo de aula ni con catálogos grandes.")
tabla("Tabla 2. Parámetros del problema y su estado",
      ["Parámetro", "Valor", "Estado"],
      [["Pesos del objetivo (ganancia, repaso, motivación, fatiga)", "1,00; 0,70; 0,35; 0,55", "Decisión de diseño"],
       ["Éxito esperado y dispersión", "0,75 y 0,18", "Decisión de diseño con apoyo en la literatura {c:wilson85}"],
       ["Pendiente de la logística de éxito", "6", "Decisión de diseño"],
       ["Dificultad media máxima", "0,72 por actividad", "Decisión de diseño"],
       ["Máximo de actividades por habilidad", "2", "Decisión de diseño"],
       ["Umbral para enumeración exacta", "4×10^5 combinaciones", "Decisión de ingeniería"]],
      "Fuente: código del repositorio.", [7.0, 4.0, 5.0])
H2("Sensibilidad a los pesos: qué se puede decir")
T("No se hizo un análisis de sensibilidad numérico del optimizador, y por tanto no se reportan cifras sobre cómo cambia la sesión al mover los pesos. Se puede afirmar algo cualitativo a partir de la estructura: "
  "un peso mayor en la urgencia de repaso favorece las actividades que atienden notas vencidas; un peso mayor en la fatiga favorece actividades cortas y fáciles; y las restricciones duras, como incluir al menos una actividad lúdica, "
  "se cumplen sin importar los pesos mientras exista una solución factible.")

H1("Discusión")
T("**Por qué una formulación y no un algoritmo de aprendizaje.** En este problema no hay datos de niños y sí hay reglas pedagógicas explícitas. Con un modelo exacto, el docente puede preguntar por qué se eligió una actividad y obtener "
  "una respuesta en términos de las restricciones y del objetivo. Si en el futuro hay datos, el contexto ya está definido para que un método de refuerzo lo use sin cambiar el resto del sistema; esa interfaz está documentada, pero "
  "no implementada.")
T("**Qué significa «óptimo».** La palabra tiene sentido matemático: es la solución de mayor valor del objetivo que satisface las restricciones, y la enumeración exacta lo verifica sobre el problema de ejemplo. No significa que sea "
  "la mejor sesión para aprender. El objetivo es un modelo de lo que el equipo cree que importa, con pesos elegidos por diseño, y solo un piloto con niños puede decir si las sesiones óptimas producen mejor aprendizaje que las "
  "no óptimas.")
T("**Límites.** La verificación cubre una sesión de ejemplo, no un barrido de casos. El tiempo de 40 ms es de una ejecución. No se probó con catálogos más grandes que el actual, de 19 canciones y las actividades guiadas, y la "
  "enumeración exacta deja de ser aplicable cuando el número de combinaciones supera el umbral. Hay que decidir qué hacer entonces: confiar en CBC, que sí da el óptimo, o acotar el catálogo.")
resto("Los demás componentes del sistema, como el seguimiento de manos, la estimación del dominio y el repaso espaciado, se apoyan en trabajos sobre seguimiento del conocimiento, práctica distribuida y estimación estadística")
H1("Conclusiones")
T("La selección de la sesión se formula como un problema de programación entera mixta con restricciones pedagógicas explícitas y se resuelve con CBC, con la enumeración exacta como respaldo y como verificación. La prueba "
  "de coincidencia pasó y la sesión de ejemplo se resolvió en 40 ms. Los pesos y las restricciones son de diseño; el beneficio pedagógico de la sesión óptima es una hipótesis por validar. El nivel de madurez es TRL 4.")
H1("Recomendaciones")
T("(1) Hacer un análisis de sensibilidad a los pesos con un barrido de casos. (2) Probar el tiempo de solución con catálogos mayores y en un equipo de aula. (3) Comparar en un piloto sesiones óptimas con sesiones elegidas por un docente. "
  "(4) Mostrar al docente la explicación de cada actividad elegida.")
declaraciones(dict(
    cred="Contribución de los autores (CRediT, por confirmar): el primer autor formuló y verificó el problema de optimización y redactó el borrador; los demás autores participaron en el desarrollo del software, "
         "las mediciones y la revisión; Cristian Javier Cano-Mogollón supervisó y revisó.",
    fin="No se recibió financiación externa. [Por confirmar.]",
    conf="Los autores no tienen conflictos de intereses que declarar. [Por confirmar.]",
    cons="No aplica: no hubo participantes humanos.",
    irb="No aplica a esta verificación técnica; el piloto con niños requerirá aprobación ética y consentimiento de acudientes.",
    datos="El código del optimizador, sus pruebas y la sesión de ejemplo están en el repositorio del proyecto; la salida de las pruebas y la verificación de referencias están en la carpeta de análisis de la entrega.",
    ia="Se usó un asistente de inteligencia artificial (Claude, de Anthropic) para leer el código, ejecutar las pruebas, verificar referencias y redactar borradores; los autores revisaron el contenido y responden por él.",
    en="Author Contributions: the first author formulated and verified the optimization problem and drafted the manuscript; the other authors contributed software, measurements and review; C. J. Cano-Mogollón supervised. No external funding. No conflicts of interest. Consent and IRB: not applicable. Data and code: project repository."))
cierre(autores, TITULO_ES, "Elegir la sesión óptima: programación entera mixta en Hand Sing Kids", Path(sys.argv[1]))
