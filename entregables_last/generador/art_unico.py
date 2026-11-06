"""Artículo único del equipo: todo el proyecto Hand Sing Kids presentado como artículo científico (plantilla Revista UIS Ingenierías)."""
import json, math, sys
from nucleo_hsk import *
import nucleo_hsk as N

A = R["aciertos"]; FPG = R["falsos_positivos"]["global_nuevo"]; FPV = R["falsos_positivos"]["global_v1"]; FPT = R["falsos_positivos"]["por_tipo"]
RB = R["robustez_fp_nuevo"]; LT = R["latencia"]; MX = R["matrices"]
SU = json.loads((BASE / "analisis" / "sensibilidad_umbrales.json").read_text(encoding="utf-8"))
QD = json.loads((BASE / "generador" / "quintana_demo.json").read_text(encoding="utf-8"))["escenarios"]
LAM, GAM = 0.65, 0.40

TITULO_ES = ("Hand Sing Kids: señas de las manos, aprendizaje adaptativo y selección de actividades para enseñar música a niños. "
             "Diseño, evaluación de laboratorio y camino hacia el aula en Montería")
TITULO_EN = ("Hand Sing Kids: hand signs, adaptive learning and activity selection to teach music to children. "
             "Design, laboratory evaluation and the road to the classroom in Montería")

RES_ES = ("Aprender música con las manos es una práctica antigua, pero llevarla a una aplicación obliga a resolver a la vez tres problemas: reconocer cuándo el niño hizo de verdad una seña, estimar lo que sabe y decidir qué debe practicar después. "
          "Este artículo presenta Hand Sing Kids, una aplicación de escritorio en Python que asigna una seña de las dos manos a cada nota de Do3 a Do4 y funciona con cámara y base local, sin internet. "
          "El reconocedor describe cada postura con un vector de 120 componentes invariante al tamaño, la posición y el giro de la mano y acepta una nota solo si la distancia, la confianza y el margen lo permiten; el modelo de aprendizaje combina precisión, consistencia, velocidad y retención con repaso espaciado; "
          "y la sesión se elige con un problema entero mixto que tiene respaldo exacto. De 189 documentos únicos reunidos, 87 resultaron aprovechables y solo ocho trataban la música infantil. "
          f"En laboratorio, con una calibración de una persona y perturbaciones simuladas, el reconocimiento fue de {f(A[0]['nuevo']['pct'], 0)} % sin ruido y de {f(A[3]['nuevo']['pct'])} % con ruido de 0,09, y ante 640 posturas que no son seña el método disparó una nota por error en {f(FPG['pct'])} % de los casos, frente a 100 % del método inicial. "
          "No hubo pruebas con niños: el nivel de madurez es TRL 4 y el efecto sobre el aprendizaje en Montería y Córdoba se plantea como hipótesis, con un plan de piloto.")
RES_EN = ("Learning music with the hands is an old practice, but taking it to an application means solving three problems at once: recognizing when a child really made a sign, estimating what the child knows and deciding what to practise next. "
          "This paper presents Hand Sing Kids, a desktop application in Python that assigns a two-handed sign to each note from C3 to C4 and works with a camera and a local database, with no internet. "
          "The recognizer describes each posture with a 120-component vector invariant to hand size, position and rotation and accepts a note only if distance, confidence and margin allow it; the learning model combines accuracy, consistency, speed and retention with spaced repetition; "
          "and the session is chosen with a mixed-integer problem that has an exact fallback. Of 189 unique documents gathered, 87 proved useful and only eight dealt with children's music. "
          f"In the laboratory, with a single-person calibration and simulated perturbations, recognition was {f(A[0]['nuevo']['pct'], 0)} % without noise and {f(A[3]['nuevo']['pct'])} % at noise 0.09, and over 640 non-sign postures the method fired a wrong note in {f(FPG['pct'])} % of cases, against 100 % for the initial method. "
          "No tests with children were done: the readiness level is TRL 4 and the effect on learning in Montería and Córdoba is stated as a hypothesis, with a pilot plan.")
KW_ES = "educación musical infantil; reconocimiento de gestos; seguimiento de manos; aprendizaje adaptativo; repaso espaciado; programación entera mixta; madurez tecnológica; Montería"
KW_EN = "children's music education; gesture recognition; hand tracking; adaptive learning; spaced repetition; mixed-integer programming; technology readiness; Montería"

autores = encabezado("Vitola", TITULO_ES, TITULO_EN, RES_ES, RES_EN, KW_ES, KW_EN, corresp_clave="Pemberty")

# ======================================================================= 1. INTRODUCCIÓN
H1("Introducción")
H2("El problema")
T("Desde mediados del siglo XIX se enseña a leer música con las manos: a cada nota de la escala le corresponde una posición, y el niño la ve, la imita y la canta. No pide instrumento ni sala, solo un cuerpo y alguien que corrija. "
  "Esa última condición es la frágil. Sin un docente atento la seña se hace de cualquier manera y nadie le dice al niño si acertó. Una cámara y un modelo de seguimiento de manos pueden ocupar ese lugar, pero trasladar la práctica a una aplicación "
  "no es solo asunto de visión por computador. Hay que resolver tres cosas que se condicionan entre sí.")
T("La primera es perceptiva. La cámara mira la mano todo el tiempo, también cuando el niño viaja de una seña a otra o cuando las dos manos se cruzan, y la aplicación solo debería sonar cuando hubo una seña intencional. Un método que responde siempre "
  "acierta todas las señas válidas, pero convierte cada movimiento de paso en una nota. La segunda es de estimación: después de cada intento hace falta saber qué domina el niño, qué olvidó y cuándo conviene volver sobre una nota. "
  "La tercera es de decisión, porque con ese conocimiento hay que armar la siguiente sesión con un tiempo limitado, sin repetir lo mismo y sin abrumar.")
T("Hand Sing Kids es nuestra respuesta conjunta a esas tres cosas. Es una aplicación de escritorio en Python, pensada para niños de 3 a 12 años, que enseña las ocho notas de Do3 a Do4. Funciona en un computador con cámara y guarda sus datos en una base local, por lo que no depende de internet. "
  "En Montería, las proyecciones municipales del DANE para 2026 indican 535.052 habitantes, de los cuales 80.254 tienen entre 3 y 12 años {c:dane}. No encontramos una estadística local sobre educación musical y no la inventamos: la razón para pensar en las aulas de Montería y Córdoba es de diseño "
  "(un equipo común, sin conexión), y que realmente ayude a aprender es una hipótesis que este trabajo no puede confirmar.")

H2("Lo que dice la literatura")
T("La combinación de inteligencia artificial y educación musical es un campo joven y muy activo. Para ubicarnos reunimos y clasificamos las fuentes con un procedimiento descrito en la sección 2.1 y resumido en la Figura 1. "
  "De 226 archivos obtenidos con dos ecuaciones de búsqueda en Scopus y con artículos de método quedaron 189 documentos únicos, y 87 de ellos resultaron directamente aprovechables. Es una muestra de conveniencia, no una revisión sistemática completa, y la tomamos como lo que es: "
  "un mapa para orientarnos.")
figura(["prisma_hsk.png"], 11.5, "Figura 1. Flujo de la búsqueda bibliográfica según PRISMA 2020 {c:prisma}, con las cifras del corpus del proyecto (informe del 9 de septiembre de 2026). No se registró el número de resultados de cada ecuación en Scopus.")
T("El corpus es reciente (el 85 % es de 2025 y 2026) y está dominado por revisiones: sistemáticas, de alcance y bibliométricas suman casi la mitad. China y el sudeste asiático concentran cerca del 60 % de la producción, mientras que lo iberoamericano, alrededor del 20 %, aporta buena parte de los estudios empíricos escolares. "
  "Lo que más nos importó está en el núcleo de 22 documentos. Allí aparecen rutas de aprendizaje musical personalizadas con aprendizaje por refuerzo o profundo {c:li_hong,li_peerj,li_disc,tang,wang}, sistemas que atienden el estado afectivo del estudiante {c:deng_sci,shi}, "
  "retroalimentación con IA y detección visual del teclado en el piano {c:deng_piano,chulu}, generación de ejercicios según la dificultad {c:ramoneda} y una revisión sobre tecnologías de IA en la primera infancia {c:yi}, además de estudios sobre aplicaciones y realidad aumentada {c:apay,barroso,leon}. "
  "Para el seguimiento de la mano casi todos usan MediaPipe Hands {c:mediapipe}.")
tabla("Tabla 1. Relación de los 189 documentos únicos con el proyecto",
      ["Categoría", "Criterio", "n", "%"],
      [["A. Núcleo", "Visión o gesto de manos con música; aprendizaje musical adaptativo; retroalimentación en tiempo real; música infantil con tecnología", "22", "11,6"],
       ["B. Relevante", "IA o tecnología en educación musical: retroalimentación, evaluación, personalización, apps, realidad aumentada", "65", "34,4"],
       ["C. Método o contexto", "Revisiones y bibliometrías de IA en educación no musical, método bibliométrico, gamificación general", "61", "32,3"],
       ["D. Marginal", "Temas alejados que entraron por la amplitud de las ecuaciones", "41", "21,7"]],
      "Fuente: informe bibliométrico del corpus del proyecto, 9 de septiembre de 2026.", [2.6, 7.9, 1.3, 1.4])
T("Dos hallazgos del corpus justifican este trabajo. Solo ocho documentos, el 4,2 %, tratan explícitamente la educación musical infantil o preescolar, y muy pocos combinan niños con tecnología de interacción; el grueso se hace en educación superior y conservatorio. "
  "Además, hay poca evidencia experimental con niños. En los títulos y resúmenes revisados no apareció un trabajo cuya entrada sea una seña manual por nota, calibrada para cada niño, con una decisión de sesión resuelta de forma exacta; no leímos todos los textos completos, así que esto no excluye que exista.")

H2("Objetivo y aportes")
T("El objetivo es describir Hand Sing Kids como sistema, evaluarlo técnicamente en laboratorio y dejar planteado, con honestidad, qué falta para saber si sirve en el aula. Los aportes son cuatro. "
  "Un reconocedor de señas que distingue la seña intencional del gesto de paso. Un modelo de aprendizaje y de repaso que se puede explicar a un docente. Una selección de la sesión como problema de optimización con respaldo exacto. "
  "Y una evaluación reproducible, con intervalos de confianza, un contraste entre lo que la documentación decía y lo que se midió, y una declaración explícita de los límites.")

# ======================================================================= 2. MÉTODOS
H1("Métodos")
H2("Búsqueda y clasificación de la literatura", )
T("Se ejecutaron dos ecuaciones en Scopus sobre título, resumen y palabras clave. La primera combina términos de educación musical (por ejemplo *music education*, *music learning*, *music teaching*) con términos de inteligencia artificial y tecnología educativa (*machine learning*, *adaptive learning*, *gamification*, *mobile app*, entre otros). "
  "La segunda combina términos de gesto y visión (*hand gesture*, *hand tracking*, *pose estimation*, *computer vision*) con términos de música. Los textos completos se descargaron a mano y se añadieron artículos de método. No se anotó el número de resultados de cada ecuación, por lo que no podemos informarlo.")
T("Los 226 archivos (218 PDF sueltos y 4 ZIP con 8 PDF) incluían 37 copias idénticas. Cada uno de los 189 documentos únicos se clasificó según su utilidad para el proyecto en cuatro categorías (Tabla 1). Se excluyeron los marginales, se apartaron los de método o contexto y se incluyeron en la síntesis los de las categorías A y B. "
  "Para 167 de los 189 documentos se recuperaron metadatos por DOI en Crossref y OpenAlex. Las referencias de este artículo se verificaron una por una contra Crossref y DataCite.")

H2("Arquitectura del sistema")
T("Nuestra primera versión era directa: tomaba los puntos que entregaba la cámara, los comparaba con una plantilla guardada y daba la nota por buena si el parecido pasaba de un umbral. Servía para una demostración, pero cargaba con toda la variabilidad de la escena (qué tan lejos está el niño, cuánto inclina la muñeca, qué tan grande es su mano) y concentraba la cámara, la música, el puntaje y el dibujo en un único archivo de 1.740 líneas, donde cualquier cambio obligaba a tocar todo. La versión que evaluamos reparte el trabajo en cinco capas que solo se comunican hacia abajo, con un bus de eventos para que las de arriba sepan qué ocurre sin depender de las de abajo (Figura 2). Ninguna pantalla importa MediaPipe, ninguna pieza de visión sabe qué es una nota y el evaluador no sabe dibujar. Gracias a eso las pruebas corren sin cámara y sin ventana.")
figura(["arquitectura.png"], 15.0, "Figura 2. Arquitectura funcional de Hand Sing Kids: percepción (cámara, descriptor, clasificador, estabilizador) y aprendizaje y decisión (dominio, repaso, predictor, optimizador, actividades).")
tabla("Tabla 2. Capas del sistema y su función",
      ["Capa", "Función"],
      [["Interfaz", "Pantallas y componentes: perfiles, aventura, calibración, ejercicio, canciones, modo libre, progreso, zona de padres, ajustes"],
       ["Aplicación", "Contexto, navegación y sesión"], ["Dominio", "Entidades, notas y evaluación de cada intento"],
       ["Inteligencia", "Modelo de dominio, repaso, motor adaptativo, predictor y optimizador MILP"], ["Infraestructura", "Cámara, audio y base de datos SQLite"]],
      "Fuente: documento técnico del proyecto, versión 2.0.", [3.0, 12.0])
T("Un intento recorre el sistema así: la cámara entrega los puntos de las manos, el descriptor y el clasificador proponen una nota, el estabilizador decide si se confirma, el motor musical la hace sonar, el evaluador comprueba si era la esperada, y el resultado alimenta la retroalimentación, el registro y el gemelo digital del aprendiz, "
  "que a su vez usan el motor adaptativo y el optimizador para decidir lo siguiente. La Figura 3 muestra cuatro de las doce pantallas de la aplicación.")
figura(["capturas_app.png"], 14.5, "Figura 3. Pantallas de la aplicación: (a) calibración de las señas del niño, (b) ejercicio guiado, (c) catálogo de canciones, (d) progreso del niño.")

H2("Reconocimiento de señas")
H3("Descriptor invariante")
T("Sean $p_0,\\dots,p_{20}\\in\\mathbb{R}^3$ los 21 puntos de una mano que entrega MediaPipe {c:mediapipe}, con $p_0$ en la muñeca. Todo se mide respecto a una escala propia de la mano, la distancia de la muñeca al nudillo del dedo medio:")
ecuacion("sigma", r"\sigma=\lVert p_9-p_0\rVert")
T("La curvatura de cada dedo, con cadena de articulaciones $(a,b,c,d)$, es una razón entre longitudes y por eso no cambia con la escala, la traslación ni la rotación:")
ecuacion("kappa", r"\kappa=\operatorname{clip}\!\left(\frac{\dfrac{\lVert p_d-p_a\rVert}{\lVert p_b-p_a\rVert+\lVert p_c-p_b\rVert+\lVert p_d-p_c\rVert}-0{,}35}{0{,}65},\,0,\,1\right)")
T("La apertura entre dedos contiguos usa los vectores unitarios $u_i$ del nudillo a la yema, y la distancia del pulgar a cada yema se normaliza con $\\sigma$:")
ecuacion("alpha", r"\alpha_i=\frac{1}{\pi}\arccos\langle u_i,u_{i+1}\rangle,\quad i=1,\dots,4")
ecuacion("tau", r"\tau_j=\frac{1}{3}\operatorname{clip}\!\left(\frac{\lVert p_{t_j}-p_4\rVert}{\sigma},\,0,\,3\right)")
T("A eso se suman la normal del plano de la palma, la dirección de la mano en la imagen y la forma normalizada, con 20 puntos trasladados, escalados por $\\sigma$ y girados para que la mano apunte hacia arriba (40 valores). Cada mano queda en 58 valores y, con cuatro magnitudes de geometría entre las dos manos, "
  "el descriptor completo tiene $2\\times 58+4=120$ componentes. La distancia entre dos descriptores se calcula por bloques $g$ con pesos $w_g$ (curvatura 3,0; forma 2,6; pulgar 2,0; dirección 2,0; entre manos 1,6; normal 1,4; apertura 1,2), para que los 40 valores de la forma no aplasten a los cinco de la curvatura:")
ecuacion("dist", r"d(a,b)=\sqrt{\frac{1}{\sum_g w_g}\sum_g w_g\,\frac{1}{|g|}\sum_{i\in g}(a_i-b_i)^2}")
H3("Clasificación con confianza y margen")
T("Cada nota $c$ conserva hasta tres muestras $S_c$ tomadas en la calibración del niño. La distancia de una postura $x$ a la nota es la menor de las distancias a sus muestras, y la confianza reparte probabilidad entre las notas con una temperatura $T$ que se ajusta a la separación real de las señas de ese niño:")
ecuacion("dc", r"d_c=\min_{s\in S_c}d(x,s)")
ecuacion("softmax", r"P(c\mid x)=\frac{\exp\!\big(-(d_c-d_{\min})/T\big)}{\sum_k\exp\!\big(-(d_k-d_{\min})/T\big)}")
ecuacion("temp", r"T=\operatorname{clip}\!\left(\tfrac{1}{2}\min_{a\neq b}d(a,b),\,0{,}05,\,0{,}20\right)")
T("La nota se acepta solo si se cumplen las tres condiciones de la ecuación {E_ACEPT}. La tercera, el margen, hace que el sistema se abstenga cuando dos señas empatan:")
ecuacion("acepta", r"\begin{aligned}d_{\text{best}}&\le 0{,}95\\ P_{\text{best}}&\ge 0{,}55\\ P_{\text{best}}-P_{\text{second}}&\ge 0{,}08\end{aligned}")
H3("Estabilizador")
T("Una nota aceptada pasa por un estabilizador con dos reglas que no dependen del tamaño de su ventana de votación. La primera es un periodo refractario de 0,45 s tras cada confirmación. La segunda exige que, para repetir la misma nota, el niño la haya soltado antes, y se considera soltada cuando seis fotogramas consecutivos arrojan una lectura distinta. "
  "En su configuración por defecto la ventana de votación es de un solo fotograma, por lo que la nota suena en cuanto el clasificador la reconoce. Antes eran ocho fotogramas con un acuerdo de 0,62, es decir, cinco coincidencias, algo menos de un cuarto de segundo que los niños percibían como espera. "
  "La ventana sigue siendo ajustable desde Ajustes, de 1 a 16 fotogramas.")

H2("Modelo de aprendizaje")
T("Una habilidad corresponde a una nota, y su dominio combina desempeño y retención. La retención multiplica en lugar de sumar. En una primera formulación entraba como un cuarto sumando de peso 0,20, y al probarla apareció el problema: un mes sin practicar bajaba el dominio a lo sumo 0,20, y una habilidad olvidada seguía figurando como dominada. Multiplicando, "
  "el desuso prolongado sí la degrada, y el término $\\lambda$ evita que unos días de pausa borren todo lo aprendido:")
ecuacion("mastery", r"\mathcal{M}_s=\big(\lambda+(1-\lambda)R_s^{\gamma}\big)\big(w_pP_s+w_cC_s+w_vV_s\big)")
T("con $w_p=0{,}55$, $w_c=0{,}25$, $w_v=0{,}20$, $\\lambda=0{,}65$ y $\\gamma=0{,}40$. La precisión $P_s$ usa un suavizado bayesiano con el que el sistema parte de la duda: sin práctica vale 0,25, y cuatro aciertos de cuatro dan 0,625 y no 1. La consistencia $C_s$ mira los últimos $K=8$ intentos y penaliza alternar aciertos y fallos, "
  "que es la firma de quien todavía no sabe. La velocidad $V_s$ se mide contra un tiempo de referencia que depende de la franja de edad (5.200 ms de 3 a 5 años, 4.000 ms de 6 a 8 y 3.200 ms de 9 a 12). La retención decae con los días $\\Delta t$ desde la última práctica:")
ecuacion("prec", r"P_s=\frac{h_s+\alpha}{n_s+\alpha+\beta},\qquad \alpha=1,\ \beta=3")
ecuacion("ret", r"R_s=\exp\!\left(-\frac{\Delta t}{\tau_s}\right),\qquad \tau_s=\tau_0\,\varepsilon_s\,(0{,}6+\mathcal{M}_s^{-}),\qquad \tau_0=1{,}8\ \text{días}")
T("Aquí $h_s$ y $n_s$ son aciertos e intentos, $\\varepsilon_s$ el factor de facilidad y $\\mathcal{M}_s^{-}$ el dominio de la actualización anterior; usar el previo y no el actual evita una definición circular. Una habilidad pasa a dominada con $\\mathcal{M}_s\\ge 0{,}80$ y al menos seis intentos, y retrocede si cae por debajo de 0,70. "
  "Los repasos se programan con una adaptación del esquema SM-2 {c:wozniak} a una calidad continua $q\\in[0,1]$, apoyada en la evidencia sobre práctica distribuida {c:cepeda}:")
ecuacion("sm2", r"\varepsilon\leftarrow\operatorname{clip}\!\big(\varepsilon+0{,}1-(1-q)(0{,}8+(1-q)),\,1{,}3,\,2{,}8\big),\qquad I\leftarrow\begin{cases}1 & q<0{,}6\\ \max(1,I\varepsilon) & \text{en otro caso}\end{cases}")
T("La idea de seguir el dominio como una variable estimada a partir de los intentos viene del seguimiento del conocimiento {c:corbett}. Cuando un niño acumula 40 intentos propios, un predictor logístico de tres variables sustituye a la fórmula fija y se reentrena cada 20 intentos nuevos, "
  "con 300 épocas de descenso de gradiente y tasa 0,35 sobre variables estandarizadas, minimizando la entropía cruzada. Las variables son la precisión previa de la nota, la dificultad de la actividad y los días desde la última práctica, recortados a 14 para que una pausa de meses no domine el ajuste:")
ecuacion("logit", r"p=\frac{1}{1+e^{-z}},\qquad z=w_1\,\mathrm{precision}+w_2\,\mathrm{dificultad}+w_3\,\mathrm{dias}+b")
T("Hay un detalle que conviene contar. El estado de una habilidad guarda el dominio actual, no su historia, así que entrenar con ese valor sobre intentos de hace semanas habría filtrado información del futuro hacia el pasado. Por eso las variables se reconstruyen dos veces de la misma manera: en el entrenamiento, recorriendo la tabla de intentos en orden cronológico y acumulando solo lo ya ocurrido, "
  "y en la predicción, desde el estado vigente. Tampoco se entrena con datos sintéticos; el modelo solo se activa con los intentos reales de cada niño.")

H2("Motor adaptativo y gemelo digital")
T("El motor adaptativo no dibuja pantallas; toma una decisión. Para ello mira cómo está el niño en ese momento: el dominio de cada habilidad, la precisión de la última actividad, los fallos seguidos, los repasos vencidos y una estimación de fatiga que mezcla cuánto ha jugado (actividades $n$ sobre un máximo $N$) y cuánto tiempo lleva (tiempo $t$ sobre un máximo $T_s$):")
ecuacion("fatiga", r"F=\operatorname{clip}\!\left(\tfrac{1}{2}\,\frac{n}{N}+\tfrac{1}{2}\,\frac{t}{T_s}\right)")
T("Las reglas se evalúan en orden y la primera que se cumple decide. Con $F\\ge1$, descansar, porque cerrar en alto vale más que insistir. Con fallos consecutivos y precisión menor de 55 %, la escalera de ayuda. Con $F\\ge0{,}7$ y sin juegos en las dos últimas actividades, jugar. Si hay repasos vencidos, repasar el de menor dominio. "
  "Con precisión de al menos 88 % y una habilidad lista para abrirse, introducirla, y si no, subir la dificultad. Ante una debilidad clara, reforzar con un ejercicio dirigido, y en otro caso, mantener.")
T("Cuando algo va mal, repetir lo mismo más veces no ayuda. La escalera de ayuda retira una exigencia distinta en cada peldaño (Tabla 3). Cuando el problema es una nota concreta, el ejercicio dirigido no la repite sola: la intercala con una nota que el niño ya domina, por ejemplo Mi, Do, Mi, Do, Mi, Mi, "
  "porque alternar obliga a distinguir las dos señas, que es justo lo que falla cuando se confunden.")
tabla("Tabla 3. Escalera de ayuda",
      ["Peldaño", "Qué se retira", "Tempo", "Longitud", "Ayuda visual"],
      [["1", "Tiempo", "×0,80", "Igual", "Igual"], ["2", "Longitud", "×0,80", "×0,6", "Igual"], ["3", "Memoria", "×0,75", "×0,6", "Siempre visible"], ["4", "Secuencia", "×0,75", "×0,5", "Siempre visible, nota aislada"]],
      "Fuente: documento técnico del proyecto, versión 2.0.", [2.0, 3.0, 2.2, 2.4, 5.0])
T("Con el nombre de gemelo digital del aprendiz llamamos a la fotografía del estado de aprendizaje de un niño en un instante. Tiene tres caras. Una por habilidad, con el dominio, la precisión, la consistencia, la velocidad, la retención, los días sin practicar y la fecha del próximo repaso. Otra de conducta, con las notas que confunde, su tiempo de reacción y el número de intentos. Y una de evolución, con los minutos por semana, las actividades hechas y la tendencia. Cada vez que se consulta, el modelo descuenta primero el olvido acumulado desde la última práctica, así que quien mira el progreso dos semanas después ve el estado real y no el de la última sesión. Del gemelo se alimentan el motor adaptativo, el optimizador y la zona de padres.")

H2("Selección de la sesión como problema de optimización")
T("Sean $A$ el conjunto de actividades candidatas, $S$ el de habilidades, $S_i\\subseteq S$ las que toca la actividad $i$, $G\\subseteq A$ las lúdicas y $V\\subseteq A$ las que atienden un repaso vencido. La decisión es $x_i\\in\\{0,1\\}$. La probabilidad de éxito se estima con una logística sobre la holgura entre el dominio medio $\\bar\\mu_i$ y la dificultad, "
  "y el factor $\\eta_i$ concentra el valor en $p^{*}=0{,}75$, una dificultad intermedia coherente con la idea de que el aprendizaje es más eficiente cuando el error no es ni muy raro ni muy frecuente {c:wilson85}:")
ecuacion("p", r"p_i=\frac{1}{1+e^{-k(\bar\mu_i-\mathrm{dif}_i)}},\qquad k=6")
ecuacion("eta", r"\eta_i=\exp\!\left(-\frac{(p_i-p^{*})^2}{2\sigma_p^2}\right),\qquad \sigma_p=0{,}18")
T("Con la ganancia $g_i=\\eta_i\\sum_{s\\in S_i}(1-\\mu_s)/\\sqrt{|S_i|}$, la urgencia de repaso $r_i$, la motivación $m_i$ y la fatiga inducida $f_i=(d_i/D)(0{,}5+\\mathrm{dif}_i)$, el problema es:")
ecuacion("obj", r"\max\ \sum_{i\in A}\big(\alpha_1g_i+\alpha_2r_i+\alpha_3m_i-\alpha_4f_i\big)\,x_i,\qquad \alpha=(1{,}00;\ 0{,}70;\ 0{,}35;\ 0{,}55)")
T("Las restricciones fijan el tiempo total ($\\sum_i d_ix_i\\le T_{\\max}$), el tamaño de la sesión ($\\sum_i x_i=K$), los prerrequisitos ($x_i\\le a_i$), una actividad lúdica como mínimo ($\\sum_{i\\in G}x_i\\ge1$), una dificultad media acotada ($\\sum_i\\mathrm{dif}_ix_i\\le0{,}72K$), "
  "un máximo de dos actividades por habilidad y un repaso vencido si existe ($\\sum_{i\\in V}x_i\\ge1$). La resolución tiene tres niveles y el sistema informa cuál usó. Primero MILP con CBC a través de PuLP. Si CBC no está disponible, enumeración exhaustiva mientras $\\binom{|A|}{K}\\le 4\\times10^{5}$, "
  "que da el óptimo exacto: con 24 candidatas y $K=4$ son 10.626 combinaciones, cuestión de milisegundos. Y una heurística voraz solo si el catálogo creciera tanto que la enumeración dejara de ser viable. Esta redundancia nació de un problema práctico: el CBC que trae PuLP para macOS está compilado para Intel y en un Mac con Apple Silicon necesita Rosetta 2.")
T("Para que el catálogo no se agote, un generador procedural propone cada vez hasta seis actividades nuevas por nivel, con secuencias de notas elegidas entre las que el niño tiene abiertas y más peso para las que le cuestan. De cada borrador se generan tres variantes y se elige la que el predictor sitúa más cerca de $p^{*}$. "
  "Esas candidatas se suman al catálogo fijo, de unas sesenta actividades escritas a mano, antes de puntuar y resolver, y solo las que resultan elegidas se guardan. Conviene decirlo con claridad: esto es aprendizaje supervisado sobre un problema de clasificación binaria, no aprendizaje por refuerzo. "
  "Otros trabajos del corpus resuelven la planificación con refuerzo {c:li_hong,tang}; nosotros no tenemos datos de niños para entrenar una política y preferimos reglas explícitas, cuyo óptimo se pueda verificar y explicar a un docente.")

H2("Canciones, sonido y retroalimentación")
T("El módulo Canciones recupera la mecánica de nota viajera de la primera versión: las notas viajan hacia una línea de impacto y solo cuenta la seña hecha justo cuando la nota la cruza. El sistema no espera la seña; el tiempo lo marca el reloj de la partida. Con tempo $\\text{bpm}$, el intervalo entre notas es $g=60000/\\text{bpm}$ ms, "
  "la nota $i$ llega en $a_i=a_{i-1}+g$ con $a_0=2200$ ms, y su ventana de acierto es asimétrica, más ancha antes de la línea que después, para no penalizar al niño por el tiempo que tarda en confirmarse el reconocimiento:")
ecuacion("vent", r"h_i=\frac{\max\!\big(W_{\min},\,\min(\text{tol},\,0{,}85\,g)\big)}{2},\qquad \text{ventana}_i=\big[a_i-1{,}15\,h_i,\ a_i+0{,}85\,h_i\big]")
T("El piso $W_{\\min}$ es de 480 ms en el código. Subió de 380 ms cuando se pasó al reconocimiento instantáneo, porque el niño dejó de tener el margen adicional que daba la antigua votación. El puntaje es de 100, 70 o 50 puntos según el error temporal (perfecto, bien o vale) y se multiplica por $\\min(1+0{,}5\\lfloor c/10\\rfloor,\\,4)$, con $c$ el número de aciertos seguidos. "
  "Hay tres factores de tempo (0,72; 1,0 y 1,15) y un catálogo de 19 melodías tradicionales o de dominio público, simplificadas a las ocho notas, de las que solo se codifica la línea melódica y nunca la letra. Una nota que cruza su ventana sin acierto se registra como intento fallido y la canción sigue sin detenerse.")
T("El sonido de cada nota tiene tres niveles de prioridad: primero lo que la familia deje en una carpeta personalizada, luego las grabaciones incluidas con la aplicación y por último el timbre sintetizado. La música de fondo se confina a las pantallas que no usan la cámara para que no compita con el sonido de la nota que el niño necesita oír con claridad.")

H2("Protocolo de evaluación técnica")
T("La evaluación reproduce y amplía la prueba de visión del repositorio sin modificarla. La calibración de referencia contiene las ocho señas (Do3 a Do4) de una sola persona, guardadas como coordenadas, sin imágenes. Las perturbaciones se simulan sobre esas coordenadas: escala entre 0,8 y 1,25, giro independiente de ±18° por mano y ruido gaussiano proporcional al tamaño de la mano. "
  "Se midieron dos cosas. La primera, el reconocimiento de señas válidas con ruido $\\sigma\\in\\{0;\\,0{,}03;\\,0{,}06;\\,0{,}09\\}$, con 60 repeticiones por nota y nivel, es decir, 480 señas por nivel. La segunda, las notas disparadas por error ante 640 posturas que no son seña: 320 transiciones a medio camino entre una nota y otra tres posiciones más adelante, "
  "y 320 combinaciones de la mano izquierda de una seña con la derecha de otra. Las proporciones llevan intervalos de Wilson al 95 % {c:wilsonci}, y la estabilidad de la tasa de falsos positivos se comprobó con 30 semillas distintas. También se midió la latencia del descriptor y el clasificador con 2.000 repeticiones y se compararon las ocho señas entre sí con ambos métodos.")
T("Para saber qué parte de la regla de aceptación mueve el compromiso entre acertar y abstenerse, se repitió el protocolo con las mismas semillas variando un umbral por vez (distancia máxima, confianza mínima y margen) mientras los otros dos permanecían en su valor por defecto. "
  "Para la ventana de Canciones y para la fórmula del dominio se hicieron cálculos de sensibilidad con las ecuaciones del código, que son derivados y no mediciones. Y para ver cómo se comporta el optimizador, que el repositorio solo comprueba con una sesión de ejemplo, se resolvió de forma exacta una instancia ilustrativa de 12 actividades que construimos para este trabajo y que no es el catálogo real.")
T("Las mediciones se hicieron en un solo equipo con Windows 11, Python 3.12.10, NumPy 1.26.4, OpenCV 4.11.0, MediaPipe 0.10.21, PySide6 6.11.2 y PuLP 2.9.0. No registramos el procesador ni la memoria. El repositorio evaluado tiene 62 módulos y 10.581 líneas (8.613 de código efectivo) y 9 archivos de pruebas con 1.746 líneas, organizados en ocho baterías "
  "(audio, integración, dominio, optimizador, predictor, canciones, estabilizador y visión). La documentación del proyecto declara además como plataforma objetivo macOS con Python 3.10 a 3.12; esa plataforma no se usó aquí. Todas las cifras de este artículo salen de scripts con semillas fijas que escriben un archivo estructurado.")

# ======================================================================= 3. RESULTADOS
H1("Resultados")
H2("Verificación del software")
T("Las ocho baterías terminaron con código de salida 0. En el optimizador, la prueba que compara el solucionador con la enumeración exacta pasó, y la sesión de ejemplo se resolvió con CBC en 40 ms con valor objetivo 2,9524. Con datos reales del proyecto ambos métodos devolvieron el mismo valor y el mismo conjunto de actividades. "
  "La prueba del predictor muestra un 78 % de acierto sobre sus propios datos de entrenamiento; esa cifra solo comprueba que el descenso de gradiente converge y no mide capacidad predictiva, porque no hay datos de niños. En la primera ejecución, en la consola de Windows con su codificación predeterminada, dos errores de impresión de caracteres especiales impidieron terminar; no eran de lógica, y con la salida en UTF-8 las ocho pasaron.")
T("Las pruebas sirvieron para algo más que confirmar lo esperado: dos fallos reales salieron de ellas y no de revisar el código a ojo. En el estabilizador, el contador de suelta volvía a cero apenas la nota reaparecía, y por eso un niño nunca podía repetir la misma nota. En la recalibración, entrar a la pantalla vaciaba las plantillas de la memoria antes de capturar nada, de manera que quien salía a mitad de camino se quedaba sin sus señas.")

H2("Reconocimiento de señas válidas")
filas_a = []
for a in A:
    n, v = a["nuevo"], a["v1"]
    filas_a.append([f(a["ruido"], 2), str(a["n"]), f"{f(n['pct'])} ({f(n['ic95_lo'])}–{f(n['ic95_hi'])})", f"{f(v['pct'])} ({f(v['ic95_lo'])}–{f(v['ic95_hi'])})"])
tabla("Tabla 4. Señas válidas reconocidas (%) según el ruido, con intervalo de Wilson al 95 %",
      ["Ruido σ", "n", "Descriptor propuesto", "Método inicial"], filas_a, "Fuente: elaboración propia (analisis/evidencia_vision.py, semilla 11).", [2.5, 2.0, 5.0, 5.0])
T(f"Hasta un ruido de 0,03 el descriptor propuesto reconoció todas las señas; con 0,06 llegó a {f(A[2]['nuevo']['pct'])} % y con 0,09 a {f(A[3]['nuevo']['pct'])} % (IC 95 %: {f(A[3]['nuevo']['ic95_lo'])} a {f(A[3]['nuevo']['ic95_hi'])} %). "
  "El método inicial acierta siempre, y esa cifra no debe leerse como ventaja: responde a toda postura con la nota más parecida y por eso no puede equivocarse por omisión. El costo de ese comportamiento aparece en el siguiente apartado.")

H2("Posturas que no son seña")
def fila_fp(nombre, d):
    n, v = d["nuevo"], d["v1"]
    return [nombre, str(n["n"]), f"{n['k']} ({f(n['pct'])}; {f(n['ic95_lo'])}–{f(n['ic95_hi'])})", f"{v['k']} ({f(v['pct'])}; {f(v['ic95_lo'])}–{f(v['ic95_hi'])})"]
tabla("Tabla 5. Notas disparadas por error ante posturas que no son seña (k; %; IC de Wilson al 95 %)",
      ["Tipo de postura", "n", "Descriptor propuesto", "Método inicial"],
      [fila_fp("Transiciones a medio camino", FPT["transicion"]), fila_fp("Manos cruzadas", FPT["manos_cruzadas"]), fila_fp("Total", {"nuevo": FPG, "v1": FPV})],
      "Fuente: elaboración propia (semilla 23).", [4.5, 1.5, 5.3, 5.3])
T(f"El descriptor propuesto disparó {FPG['k']} notas por error en {FPG['n']} posturas ({f(FPG['pct'])} %; IC 95 %: {f(FPG['ic95_lo'])} a {f(FPG['ic95_hi'])} %), contra las 640 del método inicial. Con 30 semillas distintas la tasa media fue de {f(RB['media'])} % "
  f"(desviación estándar {f(RB['sd'], 2)}; mínimo {f(RB['min'])} %; máximo {f(RB['max'])} %), de modo que el valor no depende de una semilla favorable. El desglose cambia la lectura: casi todo el error viene de las transiciones ({f(FPT['transicion']['nuevo']['pct'])} %), "
  f"mientras que las manos cruzadas casi no disparan ({f(FPT['manos_cruzadas']['nuevo']['pct'])} %). Es plausible, porque una postura a medio camino conserva rasgos de las dos señas extremas y una mano de cada seña no se parece a ninguna.")
figura(["aciertos.png", "falsos_positivos.png"], 7.9, "Figura 4. (a) Señas válidas reconocidas según el ruido (barras de error: IC de Wilson al 95 %; el eje parte de 70 %). (b) Notas disparadas por error ante posturas que no son seña, con los casos k/n.")

H2("Sensibilidad de los umbrales de aceptación")
filas = [[f(r["valor"], 2), f(r["ac_006"]), f(r["ac_009"]), f(r["fp"])] for r in SU["confidence_threshold"]]
tabla("Tabla 6. Efecto del umbral de confianza (valor por defecto: 0,55) sobre el reconocimiento con ruido y sobre las notas falsas (%)",
      ["Confianza mínima", "Ruido 0,06", "Ruido 0,09", "Notas falsas"], filas, "Fuente: elaboración propia (analisis/sensibilidad_umbrales.py).", [3.5, 3.0, 3.0, 3.0])
T("El caso base reproduce exactamente los resultados anteriores. El umbral de confianza es la perilla que mueve el compromiso: con 0,35 se reconocen todas las señas con ruido hasta 0,09, pero el 55,0 % de las posturas negativas dispara una nota, y con 0,75 casi no hay notas falsas (0,0 %), pero solo se reconoce el 43,5 % de las señas válidas con ruido alto. "
  "El valor por defecto queda en una zona intermedia. En cambio, variar el umbral de distancia entre 0,65 y 1,25, o el de margen entre 0,00 y 0,16, no cambió ningún resultado con este protocolo. Para el margen hay una explicación aritmética: si la confianza de la mejor nota es al menos 0,55, la de la segunda es a lo sumo 0,45 "
  "y el margen es al menos $2\\cdot0{,}55-1=0{,}10$, de modo que la condición de 0,08 nunca decide mientras la confianza mínima sea de 0,55 o más.")

H2("Separabilidad de las señas y latencia")
T(f"Con la calibración real, {MX['pares_sobre_0_65']} de los {MX['pares_ordenados']} pares ordenados de notas distintas ({MX['pares_unicos_sobre_0_65']} pares no ordenados de 28) superan una similitud coseno de 0,65, el umbral del método inicial; el par más parecido es {MX['max_cos'][0]}–{MX['max_cos'][1]}, con {f(MX['max_cos'][2], 3)}. "
  f"Con el descriptor propuesto, la distancia entre notas distintas va de {f(MX['dist_min_entre_notas'], 3)} a {f(MX['dist_max_entre_notas'], 3)}, lo que ajusta la temperatura a $T={f(MX['temperatura'], 3)}$ según la ecuación {{E_TEMP}}. En el método inicial, dos nubes de puntos con forma de mano siempre se parecen, "
  "y por eso un umbral fijo de similitud no separa notas; el descriptor traslada la comparación a magnitudes que sí cambian de una seña a otra (Figura 5).")
figura(["matriz_similitud.png"], 15.5, "Figura 5. Matrices 8 × 8 de las señas calibradas: (a) similitud coseno del método inicial; (b) distancia por bloques del descriptor propuesto.")
T(f"El descriptor y el clasificador tardaron {f(LT['media_ms'], 2)} ms por fotograma en promedio (percentil 95: {f(LT['p95_ms'], 2)} ms; máximo: {f(LT['max_ms'], 2)} ms; {LT['reps']} repeticiones, un solo equipo). La cifra excluye la captura, el rastreo de MediaPipe y el dibujo en pantalla; la latencia de extremo a extremo no se midió.")

H2("Ventana de acierto en Canciones")
def ventana(bpm, wmin):
    g = 60000 / bpm; w = max(wmin, 0.85 * g)
    return g, w, 1.15 * w / 2, 0.85 * w / 2
filas = []
for bpm in (40, 60, 80, 100, 120):
    g, w, a_, d_ = ventana(bpm, 480); filas.append([str(bpm), m(g), m(0.85 * g), m(w), m(a_), m(d_)])
tabla("Tabla 7. Ventana de acierto según el tempo (ms), con $W_{\\min}=480$ ms y tolerancia no limitante",
      ["bpm", "g", "0,85 g", "Ancho", "Antes de la línea", "Después de la línea"], filas, "Fuente: cálculo propio con la ecuación de la ventana; no es una medición.", [1.5, 2.0, 2.0, 2.0, 3.2, 3.2])
T("Hasta unos 100 bpm la ventana depende solo del intervalo entre notas, y a partir de ahí actúa el piso de 480 ms. A 120 bpm el 85 % del intervalo es de 425 ms, la ventana se mantiene en 480 ms y deja 276 ms antes y 204 ms después de la línea. "
  "La asimetría da más margen para adelantarse que para retrasarse, lo que compensa el tiempo que tarda el reconocimiento en confirmar. Sobre el piso, repetimos el cálculo con 380, 480 y 580 ms: a 80 bpm no interviene en ninguno de los tres casos, a 100 bpm solo con 580 ms, a 120 bpm con 480 y 580 ms, y a 140 bpm con los tres. "
  "Cuando el piso decide, cada 100 ms de piso son 100 ms más de tolerancia total.")

H2("Comportamiento del modelo de aprendizaje")
def factor(R_):
    return LAM + (1 - LAM) * R_ ** GAM
filas = []
for r_ in (1.0, 0.8, 0.5, 0.2, 0.05):
    fila = [f(r_, 2)]
    for S_ in (0.95, 0.90, 0.85):
        M_ = S_ * factor(r_); fila.append(f(M_, 3) + (" ✓" if M_ >= 0.80 else (" ↓" if M_ < 0.70 else "")))
    filas.append(fila)
tabla("Tabla 8. Dominio según la retención $R$ y el desempeño combinado $S$ (✓: dominada, ≥ 0,80; ↓: retrocede, < 0,70)",
      ["R", "S = 0,95", "S = 0,90", "S = 0,85"], filas, "Fuente: cálculo propio con la ecuación del dominio; no son datos de niños.", [2.0, 3.5, 3.5, 3.5])
def r_um(S_, obj):
    fac = obj / S_
    return 0.0 if fac <= LAM else ((fac - LAM) / (1 - LAM)) ** (1 / GAM)
T(f"Como la retención multiplica al desempeño, una nota solo puede ser dominada si su desempeño combinado supera 0,80, y cuanto menor es, más alta debe mantenerse la retención. Con $S=0{{,}}95$ la nota deja de estar dominada cuando $R$ baja de {f(r_um(0.95, 0.8), 2)} y retrocede cuando baja de {f(r_um(0.95, 0.7), 3)}; "
  f"con $S=0{{,}}90$ los umbrales son {f(r_um(0.90, 0.8), 2)} y {f(r_um(0.90, 0.7), 2)}, y con $S=0{{,}}85$, {f(r_um(0.85, 0.8), 2)} y {f(r_um(0.85, 0.7), 2)}. En días, con $S=0{{,}}95$, dominio previo de 0,90 y el factor de facilidad en sus extremos (1,3 y 2,8), $\\tau_s$ vale 3,5 y 7,6 días: "
  f"la nota deja de estar dominada tras unos {f(-3.51 * math.log(r_um(0.95, 0.8)), 1)} a {f(-7.56 * math.log(r_um(0.95, 0.8)), 1)} días sin practicar. Son valores de la fórmula con supuestos explícitos, no observaciones.")

H2("Comportamiento del optimizador en una instancia ilustrativa")
T("La instancia tiene 12 actividades, un dominio estimado decreciente entre el Do (0,90) y el Do agudo (0,05), urgencia de repaso en Do y Re, $K=4$, $T_{\\max}=30$ min y la dificultad media máxima de 0,72. Se resolvió por enumeración exhaustiva de las 495 combinaciones, de las cuales 180 son factibles. "
  f"La sesión óptima del caso base está formada por las actividades {', '.join(str(i) for i in QD['Base']['sesion'])} ({'; '.join(QD['Base']['nombres'])}), dura {QD['Base']['minutos']} minutos y tiene un valor objetivo de {f(QD['Base']['obj'], 4)}.")
nombres_esc = ["Base", "Peso del repaso ×2", "Peso de la fatiga ×2", "Peso de la ganancia ×2", "Dificultad media máxima 0,50", "Sesión de K = 3", "Sesión de K = 5", "Niño más avanzado (+0,2)", "Tiempo máximo 16 min"]
filas = []
for n_ in nombres_esc:
    r_ = QD[n_]
    filas.append([n_, "Infactible", "—", "—"] if r_.get("factible") == 0 else [n_, f(r_["obj"], 3), ",".join(str(i) for i in r_["sesion"]), str(r_["factibles"])])
tabla("Tabla 9. Sensibilidad de la sesión óptima en la instancia ilustrativa", ["Escenario", "Objetivo", "Sesión", "Combinaciones factibles"], filas, "Fuente: elaboración propia (generador/quintana_demo.py); instancia de juguete, no el catálogo de la aplicación.", [5.5, 2.5, 3.0, 4.0])
T("La sesión es estable ante los pesos del repaso y de la fatiga: al duplicarlos cambia el valor del objetivo pero no las actividades. Solo al duplicar el peso de la ganancia pasa a {3, 6, 9, 11}, con más actividades de dificultad media y alta. Las restricciones de tiempo pueden dejar el problema sin solución: con 16 minutos no hay una sesión de cuatro actividades que cumpla todas las reglas, "
  "porque la combinación factible más corta dura 17. Un sistema real debería detectar esa situación y relajar una restricción, por ejemplo reducir $K$. La exigencia de una actividad lúdica no cambió la solución porque la óptima ya la incluía, y bajar la dificultad media máxima a 0,50 solo redujo las combinaciones factibles de 180 a 81.")

H2("Lo reportado y lo medido")
T("La documentación previa del proyecto reportaba cifras que no habían sido repetidas por nadie del equipo. Las contrastamos con nuestras mediciones (Tabla 10). La tasa de 8 % de notas falsas se reproduce; la latencia medida es menor que la reportada, pero se midió en otro equipo y no consta que con el mismo alcance; "
  "el tiempo de 40 ms del optimizador es del mismo orden que los 38 ms reportados, aunque viene de una sola sesión; la precisión superior a 94,2 % no pudo reproducirse porque el protocolo que la produjo no está documentado, y con el nuestro el reconocimiento fue de 100 % a 86,0 % según el ruido, de modo que no son cifras comparables; y los 30 fotogramas por segundo no se midieron porque requieren la cámara.")
tabla("Tabla 10. Cifras reportadas frente a cifras medidas",
      ["Cifra", "Reportado", "Medido en esta evaluación", "Estado"],
      [["Notas falsas ante posturas que no son seña", "8 %", f"{f(FPG['pct'])} % (51 de 640); 30 semillas: media {f(RB['media'])} %", "Reproducida"], ["Latencia del descriptor y el clasificador", "2,3 ms", f"{f(LT['media_ms'], 2)} ms (percentil 95: {f(LT['p95_ms'], 2)} ms)", "No coincide; otro equipo"],
       ["Tiempo para asignar actividades", "38 ms", "40 ms (una sesión de ejemplo)", "Mismo orden"], ["Precisión en ocho gestos", "> 94,2 %", f"{f(A[0]['nuevo']['pct'], 0)} % a {f(A[3]['nuevo']['pct'])} % según el ruido", "No comparable"], ["Fotogramas por segundo", "30", "No medido", "No medida"]],
      "Fuente: documentación del proyecto y elaboración propia.", [4.8, 2.2, 5.5, 3.2])
T("Además encontramos discrepancias entre la documentación y el código, y en todos los casos adoptamos el valor del código o de la medición. Los fotogramas para considerar soltada una seña eran 2 en el texto y 6 en el código. La ventana mínima de Canciones era 380 ms en una sección y 480 ms en otra que la actualizaba. "
  "El repositorio medía 8.599 líneas y 44 módulos en un recuento anterior y mide 10.581 líneas y 62 módulos. «30 de 56 pares» de señas similares eran pares ordenados, es decir, 15 de 28 pares no ordenados. La aceleración progresiva atribuida al método inicial no existía; la velocidad era constante. "
  "Y el desglose del 8 % de notas falsas (13,8 % en transiciones y 2,2 % en manos cruzadas) no estaba documentado.")

# ======================================================================= 4. DISCUSIÓN
H1("Discusión")
T("Respuesta inmediata frente a margen. Con ventana de un fotograma, la nota suena en cuanto el clasificador la reconoce y no hay barra de espera. El costo es el 8 % de falsos positivos en transiciones que antes la votación de varios fotogramas reducía a cambio de una espera perceptible. Es un cambio de compromiso y no una mejora en ambos sentidos. "
  "Para niños pequeños se prefirió la respuesta inmediata, y la ventana puede ampliarse por niño desde Ajustes. El análisis de umbrales añade algo que no esperábamos: de las tres condiciones de aceptación, solo la confianza decide, y por eso ajustar ese valor por niño parece una forma más directa de recuperar margen que tocar los otros dos. "
  "Los resultados con ruido alto (86,0 %) indican que un reconocimiento que se abstiene en lugar de equivocarse cuesta una repetición de la seña, mientras que un falso positivo rompe el juego.")
T("Una nota que sonaba dos veces. En una iteración posterior, una misma nota sostenida sonaba dos veces y el clasificador no tenía la culpa. MediaPipe pierde la mano uno o dos fotogramas aunque esté quieta; con la ventana de votación, eso quedaba absorbido, pero al reducirla a un fotograma se interpretaba como que el niño había soltado la seña, y la lectura siguiente repetía la nota. "
  "Hubo que subir el umbral de suelta de dos a seis fotogramas. La lección es general: cambiar un parámetro en un módulo puede dejar a otro cargando con una función que nunca se probó por separado, y por eso la batería del estabilizador incluye ahora una prueba del parpadeo breve.")
T("Qué sostiene la propuesta y qué no. El corpus muestra que los dos pilares del proyecto tienen literatura reciente propia: catorce documentos de visión o gesto aplicados a música y ocho de aprendizaje por refuerzo para educación musical, casi todos de 2026. Pero también muestra la escasez de evidencia con niños, y nuestro propio trabajo comparte ese límite. "
  "Lo que aportamos es un sistema explicable, con cada decisión rastreable, y una evaluación que dice con claridad lo que mide. No logramos, ni pretendemos, demostrar que enseñe música.")
T("Amenazas a la validez. La calibración es de una sola persona y de ocho señas, de modo que no se conoce la variabilidad entre niños. Las perturbaciones se simulan sobre coordenadas ya extraídas y no incluyen errores de detección de MediaPipe, desenfoque ni iluminación. Las posturas negativas se construyeron por interpolación y combinación, y la tasa real depende de cómo se mueven los niños. "
  "El método inicial se evaluó con la misma calibración, por lo que la comparación es interna. Las constantes (pesos del dominio, umbral de 0,80, $p^{*}=0{,}75$, ventanas de acierto) vienen de la literatura y del ajuste sobre los datos disponibles, no de un estudio con niños. Las canciones son simplificaciones a la escala de ocho notas, sin revisión de un músico formado. "
  "El modelo de predicción es lineal y de tres coeficientes a propósito, y no hay aprendizaje por refuerzo: el motor adaptativo es un conjunto de reglas, y la interfaz para sustituirlo por un agente existe sin datos que la alimenten. La búsqueda bibliográfica es una muestra de conveniencia y no registró el número de resultados de cada ecuación. "
  "Y la instancia ilustrativa del optimizador es una instancia de juguete.")
T("Madurez tecnológica. Proponemos TRL 4, validación de componentes en entorno de laboratorio. A favor está que los componentes funcionan integrados en una aplicación ejecutable, con ocho baterías sin fallos y mediciones reproducibles con intervalos de confianza. En contra de un nivel superior, ningún componente se validó en el entorno de uso, con niños, cámaras y luz reales. "
  "El paso a TRL 5 exige un piloto en el aula, cuyo protocolo está diseñado y no se ha ejecutado. El equipo debe confirmar el nivel final.")
T("Impacto esperado en Montería y Córdoba. Lo formulamos como tres hipótesis. H1: niños de 3 a 12 años aprenden a reproducir las ocho señas con calibración individual en una sesión corta. H2: en el aula, la tasa de notas disparadas por error es comparable a la de laboratorio o menor al ampliar la ventana. "
  "H3: la aplicación funciona sin internet en computadores con cámara; esta es una propiedad de diseño, ya que los datos se guardan en SQLite local, y es la única que puede verificarse sin niños. Un piloto exploratorio compararía grupos de instituciones de Montería, uno con la herramienta y otro con el método tradicional, midiendo antes y después el reconocimiento de las notas, "
  "y recogería la opinión del docente. Como se trabaja con menores, requiere aprobación de un comité de ética, consentimiento de los acudientes y una revisión de la normativa colombiana sobre datos personales. Con un nivel de significancia de 0,05 y potencia de 0,80, una aproximación normal da unos 63 niños por grupo para un efecto moderado (d = 0,5) y unos 25 para uno grande (d = 0,8); "
  "como el efecto es desconocido, conviene un piloto exploratorio y calcular el tamaño definitivo con sus resultados.")
resto("Otros trabajos del corpus que no discutimos aquí abordan la personalización de rutas, la medición del afecto y la generación de material según la dificultad")

# ======================================================================= 5. CONCLUSIONES
H1("Conclusiones")
T("Hand Sing Kids integra en una aplicación de escritorio, sin internet, un reconocedor de señas de las manos, un modelo de aprendizaje con repaso espaciado, un motor adaptativo y una selección de sesión por optimización con respaldo exacto. En laboratorio, el descriptor invariante con decisión por distancia, confianza y margen redujo las notas disparadas por error de 100 % a "
  f"{f(FPG['pct'])} % en 640 posturas que no son seña, con una pérdida de sensibilidad visible solo con ruido alto, y el umbral de confianza resultó ser la única condición de aceptación que mueve ese compromiso. Ocho baterías de pruebas terminaron sin fallos y las cifras que la documentación reportaba se contrastaron con mediciones propias: una se reprodujo, una resultó del mismo orden, "
  "una no coincidió pero se midió en otro equipo, una no pudo compararse y una no se midió.")
T("Los resultados describen el comportamiento del sistema en laboratorio, con una calibración de una persona, perturbaciones simuladas y constantes de diseño. Ningún niño lo ha usado en una prueba formal, así que su efecto sobre el aprendizaje en Montería y Córdoba es una hipótesis, y el nivel de madurez es TRL 4.")

H1("Recomendaciones")
T("Antes de entrar a un aula recomendamos, en este orden: obtener la aprobación ética y la autorización de una institución aliada; redactar la política de datos de menores con asesoría jurídica; medir la latencia de extremo a extremo y la iluminación del aula con el equipo real; probar la instalación en un equipo limpio y en macOS; y diseñar el piloto con grupo de comparación. "
  "En lo técnico, proponemos calibrar y medir con varios niños, ajustar el umbral de confianza por niño, incorporar la velocidad de la mano como señal para rechazar posturas en movimiento rápido, repetir el análisis de sensibilidad del optimizador con el catálogo real, y reajustar las constantes del modelo con los intentos registrados en el piloto. "
  "El aprendizaje por refuerzo queda como el paso siguiente natural, pero solo cuando existan datos de niños con los que entrenarlo.")

declaraciones(dict(
    cred="Contribución de los autores (taxonomía CRediT; por confirmar por el equipo antes del envío): los estudiantes autores participaron en conceptualización, desarrollo de software, investigación, análisis formal y redacción del borrador original, cada uno con un frente propio (reconocimiento, tiempo y retroalimentación, aprendizaje adaptativo, optimización, ingeniería y despliegue, verificación de cifras y justificación pedagógica); "
         "Cristian Javier Cano-Mogollón realizó la supervisión y la revisión y edición del manuscrito. Los autores leyeron y aprobaron la versión final.",
    fin="Esta investigación no recibió financiación externa. [Por confirmar por el equipo.]",
    conf="Los autores declaran que no existen conflictos de intereses relacionados con la presente publicación. [Por confirmar por el equipo.]",
    cons="No aplica. No se recolectaron datos de niños; la calibración de referencia contiene únicamente coordenadas de puntos de la mano de una persona, sin imágenes.",
    irb="No aplica, dado que el estudio es una evaluación técnica de laboratorio sin participantes en riesgo. Una prueba con niños requerirá aprobación ética y consentimiento de los acudientes.",
    datos="El código, la calibración de referencia, las pruebas y los scripts de evaluación están en el repositorio del proyecto. Las salidas de las mediciones (resultados_vision.json, sensibilidad_umbrales.json), el corpus bibliográfico y la verificación de referencias están en las carpetas de análisis y de datos de la entrega. El repositorio público está por definir.",
    ia="Se utilizó un asistente de inteligencia artificial (Claude, de Anthropic) para apoyar el análisis del código, la ejecución y documentación de las mediciones, la verificación de referencias y la redacción de borradores. Los autores revisaron el contenido y asumen la responsabilidad del texto y de los resultados.",
    en="Author Contributions: the student authors contributed to conceptualization, software, investigation, formal analysis and writing of the original draft, each with their own front (recognition, timing and feedback, adaptive learning, optimization, engineering and deployment, verification of figures and pedagogical rationale); C. J. Cano-Mogollón contributed supervision and review and editing. Funding: none external. Conflicts of interest: none. Informed consent and IRB: not applicable (laboratory evaluation). Data and code: project repository and analysis folders."))
cierre(autores, TITULO_ES, "Hand Sing Kids: enseñanza de notas musicales con señas de las manos", Path(sys.argv[1]), esperadas=22)
