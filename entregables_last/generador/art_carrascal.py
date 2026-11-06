"""Artículo — primera autora: Juliana Esther Carrascal Hernández. Hilo: aprendizaje adaptativo; del intento al dominio y al repaso."""
import sys
from nucleo_hsk import *
import nucleo_hsk as N

TITULO_ES = ("Del intento al dominio: estimación del aprendizaje y repaso espaciado en Hand Sing Kids para la enseñanza de las notas musicales a niños")
TITULO_EN = ("From attempt to mastery: learning estimation and spaced repetition in Hand Sing Kids for teaching musical notes to children")
RES_ES = ("Una secuencia fija de ejercicios trata igual a todos los niños: repite lo que uno ya domina y adelanta lo que otro aún no ha aprendido. Se describe el modelo de aprendizaje de Hand Sing Kids, una aplicación que "
          "enseña las ocho notas de Do3 a Do4 con señas de las manos. Después de cada intento, el sistema actualiza una estimación del dominio de la nota que combina cuatro componentes, precisión, consistencia, velocidad y "
          "retención, esta última con decaimiento exponencial por los días sin practicar; programa los repasos con una adaptación del esquema SM-2 a una calidad continua; y, cuando el niño acumula 40 intentos, sustituye la fórmula "
          "fija por un predictor logístico de tres variables. Una nota pasa a dominada con un valor de 0,80 y al menos seis intentos, y retrocede si cae por debajo de 0,70. Las baterías de prueba del dominio y del predictor del repositorio "
          "terminaron sin fallos; el predictor alcanza 78 % sobre sus propios datos de entrenamiento, lo que solo comprueba que el ajuste converge. No hay datos de niños: las constantes son decisiones de diseño y el efecto sobre "
          "el aprendizaje es una hipótesis por validar. El nivel de madurez es TRL 4.")
RES_EN = ("A fixed exercise sequence treats all children alike: it repeats what one child already masters and moves ahead on what another has not yet learned. The learning model of Hand Sing Kids, an application that "
          "teaches the eight notes from C3 to C4 with hand signs, is described. After each attempt the system updates a mastery estimate for the note that combines four components, accuracy, consistency, speed and "
          "retention, the latter decaying exponentially with days without practice; schedules reviews with an adaptation of the SM-2 scheme to a continuous quality; and, once the child has 40 attempts, replaces the fixed formula "
          "with a three-variable logistic predictor. A note becomes mastered at 0.80 with at least six attempts and falls back below 0.70. The mastery and predictor test suites of the repository ran without failures; the predictor reaches "
          "78 % on its own training data, which only checks that the fit converges. There are no data from children: the constants are design decisions and the effect on learning is a hypothesis to be validated. The readiness level is TRL 4.")
KW_ES = "aprendizaje adaptativo; seguimiento del conocimiento; repaso espaciado; dominio de habilidades; predictor logístico; educación musical infantil; Montería"
KW_EN = "adaptive learning; knowledge tracing; spaced repetition; skill mastery; logistic predictor; children's music education; Montería"
autores = encabezado("Carrascal", TITULO_ES, TITULO_EN, RES_ES, RES_EN, KW_ES, KW_EN)

H1("Introducción")
H2("Qué practicar después")
T("Aprender las notas con las manos exige repetir, pero no cualquier repetición sirve. Un niño que ya domina el Do y el Re necesita avanzar hacia el Mi; otro que confunde el Fa con el Sol necesita volver sobre ellos. "
  "Una aplicación que ofrece siempre la misma secuencia ignora esa diferencia. Para adaptarse, el sistema tiene que responder tres preguntas después de cada intento: qué sabe el niño de cada nota, cuándo conviene "
  "volver a una nota ya aprendida y qué actividades armar para la siguiente sesión.")
T("Estas preguntas tienen una larga historia en los sistemas de tutoría. El seguimiento del conocimiento estima el dominio de una habilidad como una variable oculta a partir de los aciertos y fallos observados {c:corbett}. "
  "En paralelo, la investigación sobre práctica distribuida muestra que espaciar los repasos mejora la retención frente a concentrarlos {c:cepeda}, y los algoritmos de repetición espaciada programan el siguiente repaso "
  "según la calidad de la respuesta anterior {c:wozniak}. Una idea complementaria sostiene que el aprendizaje es más eficiente cuando la dificultad deja una tasa de error intermedia {c:wilson85}.")
H2("Trabajos recientes en educación musical")
T("En música, la personalización se ha abordado con aprendizaje por refuerzo y profundo para trazar rutas de estudio {c:li_hong,li_peerj,li_disc,tang,wang}, con sistemas que consideran el estado afectivo del "
  "estudiante {c:deng_sci,shi} y con generación de partituras según su dificultad {c:ramoneda}. Hay además estudios de retroalimentación con IA en piano {c:deng_piano,chulu}, y revisiones sobre IA en la primera infancia {c:yi} "
  "y sobre aplicaciones móviles musicales {c:apay,barroso,leon}. Entre los títulos revisados no apareció uno que combine un modelo de dominio por habilidad, repaso espaciado y una selección de sesión resuelta de forma exacta "
  "para una entrada por seña manual; no se leyeron los textos completos.")
tabla("Tabla 1. Idea de la literatura, adaptación en Hand Sing Kids y estado de validación",
      ["Idea", "Fuente", "Cómo se adapta", "Validación"],
      [["Dominio como variable estimada", cita("corbett"), "Dominio de cuatro componentes por nota", "Pruebas unitarias; sin datos de niños"],
       ["Repaso espaciado", cita("wozniak,cepeda"), "SM-2 con calidad continua entre 0 y 1", "Pruebas unitarias; sin datos de niños"],
       ["Dificultad intermedia", cita("wilson85"), "Éxito esperado de 0,75 al elegir actividades", "Constante de diseño"],
       ["Predictor del éxito", "—", "Logística de tres variables desde 40 intentos", "Convergencia comprobada; 78 % sobre su entrenamiento"]],
      "Fuente: elaboración propia.", [3.8, 2.4, 5.2, 4.6])
H2("Objetivo")
T("Describir con precisión el modelo de aprendizaje de Hand Sing Kids, declarar qué se verificó y qué no, y dejar planteadas las hipótesis que un piloto con niños debería poner a prueba.")

H1("Métodos")
H2("Enfoque")
T("El trabajo es un análisis de diseño y de verificación técnica sobre el código del sistema. La capa pedagógica recibe de la capa perceptiva una nota confirmada y el tiempo que el niño tardó en producirla, y devuelve "
  "la actualización del dominio y la siguiente sesión (Figura 1). No se usaron datos de niños.")
figura(["arquitectura.png"], 14.0, "Figura 1. Arquitectura funcional de Hand Sing Kids; la capa pedagógica es la que se describe aquí.")
bloque("dominio")

H1("Resultados")
H2("Qué se verificó")
T("Las baterías de prueba del dominio y del predictor, dos de las ocho del repositorio, terminaron sin fallos. La prueba unitaria del predictor mejora a la predicción al azar sobre sus propios datos de entrenamiento, con "
  "78 % de acierto. Esa cifra solo comprueba que el descenso de gradiente converge; no mide capacidad predictiva, porque no hay datos de niños con los que probarlo. Del mismo modo, las pruebas del dominio verifican que la fórmula "
  "se comporte como se espera, por ejemplo, que el desuso prolongado degrade la retención sin llevarla a cero, y no que esa fórmula refleje cómo aprende un niño.")
tabla("Tabla 2. Constantes del modelo de aprendizaje y su origen",
      ["Constante", "Valor", "Origen"],
      [["Pesos del dominio (precisión, consistencia, velocidad)", "0,55; 0,25; 0,20", "Decisión de diseño"],
       ["Piso de retención y exponente", "0,65 y 0,40", "Decisión de diseño"],
       ["Umbral de dominada y de retroceso", "0,80 y 0,70", "Decisión de diseño"],
       ["Intentos mínimos para dominar", "6", "Decisión de diseño"],
       ["Intentos para activar el predictor y reentrenamiento", "40 y cada 20", "Decisión de diseño"],
       ["Éxito esperado de las actividades", "0,75", "Literatura {c:wilson85} y diseño"]],
      "Fuente: código del repositorio.", [7.0, 3.5, 5.5])
T("La Tabla 2 muestra el límite central del trabajo: ninguna de las constantes proviene de datos de niños. El modelo es defendible como diseño, pero cualquier afirmación de que acierta al estimar lo que sabe un niño sería prematura.")

H1("Discusión")
T("**Por qué el dominio multiplica la retención.** Si la retención sumara al desempeño, un niño que practicó muy bien hace semanas aparecería con un dominio alto aunque hubiera olvidado la seña. Al multiplicarla, el desuso "
  "degrada el dominio. El piso de 0,65 evita que una pausa larga lo lleve a cero, lo que sería injusto con un niño que sí aprendió. Es una decisión de diseño razonable, pero deberá contrastarse con curvas de olvido reales.")
T("**Del conocimiento experto a los datos.** El modelo parte de una fórmula fija porque al comenzar no hay datos. Cuando el niño acumula 40 intentos, el predictor logístico aprende con ellos. Ese cambio es una idea útil: "
  "permite que el sistema empiece con reglas explicables y se personalice con el uso. Pero también exige cuidado: con pocos intentos el predictor puede sobreajustarse, y el docente debería poder ver cuál de los dos "
  "modelos está decidiendo.")
T("**Hipótesis para un piloto.** (H1) Una secuencia adaptada produce mejor retención a una semana que una secuencia fija. (H2) El predictor logístico mejora al estimador fijo después de 40 intentos. (H3) Los repasos programados "
  "por el sistema coinciden con las notas que el niño efectivamente olvida. Para probarlas hacen falta niños, un docente y registros de intentos con fechas; la aplicación ya los guarda en una base local.")
resto("Para el reconocimiento de las señas, la estabilización y la selección de la sesión por optimización, véanse los trabajos sobre seguimiento de manos, aprendizaje por refuerzo y evaluación de aplicaciones musicales")

H1("Conclusiones")
T("Hand Sing Kids estima el dominio de cada nota con cuatro componentes, programa repasos con repetición espaciada y reemplaza la fórmula fija por un predictor desde los 40 intentos. El código y las pruebas "
  "verifican que el modelo se comporta como se diseñó. No hay datos de niños y las constantes son de diseño, de modo que el efecto sobre el aprendizaje es una hipótesis. El nivel de madurez es TRL 4.")
H1("Recomendaciones")
T("(1) Registrar los intentos en un piloto y reajustar las constantes con ellos. (2) Comparar una secuencia adaptada con una fija en retención a una semana. (3) Mostrar al docente qué modelo decide y por qué. "
  "(4) Medir el sobreajuste del predictor con datos nuevos y no con los de entrenamiento.")
from decl_personas import DECL
declaraciones(DECL["carrascal"])
cierre(autores, TITULO_ES, "Del intento al dominio: aprendizaje adaptativo en Hand Sing Kids", Path(sys.argv[1]))
