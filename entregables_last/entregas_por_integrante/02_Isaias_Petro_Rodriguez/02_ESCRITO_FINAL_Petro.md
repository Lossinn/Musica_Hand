# ESCRITO FINAL — Isaías José Petro Rodríguez

**Tu hilo:** Visión computacional: distinguir la seña intencional del gesto de paso. Un descriptor invariante y una decisión por distancia, confianza y margen frente a un método que responde siempre.

**Preprint y artículo:** Tu preprint plantea la pregunta (¿cuántas notas por error dispara?) y tu artículo la responde con el detalle: descriptor de 120 componentes, clasificación con margen, estabilizador, protocolo, tablas con intervalos de Wilson y las figuras de acierto, falsos positivos y similitud.

---
## ESCRITO FINAL 1 — Preprint

**Reconocer solo la seña que el niño quiere hacer: descriptor invariante de manos para enseñar las notas musicales**

Isaías José Petro Rodríguez. Universidad Pontificia Bolivariana, seccional Montería, Ingeniería Industrial. Gestión Tecnológica, tercer corte. 6 de noviembre de 2026.

**Introducción**

Enseñar las notas musicales con las manos es una práctica antigua de la educación musical infantil: cada nota tiene una forma de la mano. Una cámara puede ver esa forma, pero también ve la mano cuando esta viaja de una seña a otra o cuando las dos manos se cruzan.

Ese es el problema técnico. Si el sistema responde siempre, acierta todas las señas válidas, pero convierte cada movimiento de paso en una nota. En un aula de Montería, con niños pequeños que se mueven mucho, eso generaría confusión y frustración.

El objetivo de este trabajo es describir y evaluar, en laboratorio, el reconocedor de señas de Hand Sing Kids, que asigna una seña de dos manos a cada una de las ocho notas, de Do3 a Do4. La pregunta es cuántas notas por error dispara frente al método de la versión inicial.

**Metodología**

El enfoque es cuantitativo, de laboratorio, sobre un prototipo escrito en Python. La evaluación no incluye niños.

Cada mano se convierte en 21 puntos con MediaPipe Hands. Con ellos se arma un vector de 120 componentes (curvatura de los dedos, apertura entre dedos, posición del pulgar, forma de la mano y relación entre las dos manos) que no cambia con el tamaño de la mano, su posición ni su giro.

La postura se clasifica por vecino más cercano, pero solo se acepta si la confianza y el margen sobre la segunda nota son suficientes, y después de aceptar una nota hay un periodo de espera de 0,45 s.

Se usó una calibración de ocho señas de una sola persona y perturbaciones simuladas de tamaño, giro y ruido. Se midieron 480 señas válidas por nivel de ruido y 640 posturas que no son seña, con intervalos de Wilson al 95 % (Wilson, 1927).

**Resultados**

Sin ruido y con ruido 0,03, el método propuesto reconoció las 480 señas (100 %). Con ruido 0,06 acertó el 96,9 % y con 0,09, el 86,0 %.

Ante las 640 posturas que no son seña, el método propuesto disparó una nota por error en el 8,0 % de los casos (51 de 640; IC 95 %: 6,1 a 10,3 %), frente al 100 % del método de la versión inicial. Las transiciones causaron más errores (13,8 %) que las manos cruzadas (2,2 %).

El método inicial acierta siempre porque responde siempre. El nuevo pierde algo de acierto con ruido alto, pero evita casi todas las notas falsas. Además, procesa un fotograma en 0,89 ms en el equipo de pruebas, sin contar la cámara.

**Cierre**

El aporte es un reconocedor que distingue la seña intencional del gesto de paso y que se evaluó con números reproducibles. Sus límites son que la calibración es de una sola persona, que el ruido es simulado y que no se probó con niños. Falta una prueba en el aula; el prototipo está en un nivel de madurez tecnológica TRL 4.

**Referencia verificada**

Zhang, F., Bazarevsky, V., Vakunov, A., Tkachenka, A., Sung, G., Chang, C.-L., & Grundmann, M. (2020). *MediaPipe Hands: On-device real-time hand tracking*. arXiv. https://doi.org/10.48550/arXiv.2006.10214

---
## ESCRITO FINAL 2 — Resumen y abstract

**Resumen.** Una cámara ve la mano todo el tiempo, también cuando el niño viaja de una seña a otra, y una aplicación que enseña notas con las manos debe sonar solo cuando hubo una seña intencional. Se describe y evalúa el reconocedor de Hand Sing Kids, que asigna una seña de dos manos a cada una de las ocho notas de Do3 a Do4. Cada postura se codifica con un vector de 120 componentes invariante al tamaño, la posición y el giro de la mano, se clasifica por vecino más cercano y se acepta solo si la distancia, la confianza y el margen sobre la segunda nota son suficientes. Con una calibración de una persona y perturbaciones simuladas, 480 señas válidas por nivel de ruido se reconocieron en 100 % sin ruido y en 86,0 % con ruido de 0,09. Ante 640 posturas que no son seña, el método propuesto disparó una nota por error en 8,0 % de los casos (IC 95 %: 6,1 a 10,3 %), frente a 100 % del método de la versión inicial, que acierta siempre porque responde siempre. El error restante viene sobre todo de las transiciones entre señas. No hubo pruebas con niños; el nivel de madurez es TRL 4 y el efecto en el aula es una hipótesis.

**Abstract.** A camera sees the hand all the time, including when a child moves from one sign to another, and an application that teaches notes with the hands should sound only when a sign was intentional. The recognizer of Hand Sing Kids, which assigns a two-handed sign to each of the eight notes from C3 to C4, is described and evaluated. Each posture is encoded as a 120-component vector invariant to hand size, position and rotation, classified by nearest neighbour and accepted only if the distance, the confidence and the margin over the second note are sufficient. With a single-person calibration and simulated perturbations, 480 valid signs per noise level were recognized at 100 % without noise and 86,0 % at noise 0.09. Over 640 postures that are not signs, the proposed method fired a wrong note in 8,0 % of cases (95 % CI 6,1 to 10,3 %), against 100 % for the initial method, which is always right because it always answers. The remaining error comes mostly from transitions between signs. No tests with children were done; the readiness level is TRL 4 and the classroom effect is a hypothesis.

---
## ESCRITO FINAL 3 — Texto del artículo

[Título art] Qué mano es una seña: descriptor invariante y decisión por margen para reconocer las ocho notas de Hand Sing Kids

[Título art] Which hand pose is a sign: invariant descriptor and margin-based decision to recognize the eight notes of Hand Sing Kids

[Nombre autores] Isaías José Petro-Rodríguez^1}^*}, Antolin De Jesús Vitola-Montes^2}, Andrés Julián Negrete-Pacheco^3}, Juliana Esther Carrascal-Hernández^4}, Angel Quintana-Jiménez^5}, Alejandro Pemberty-Vergara^6}, Juan Diego Guerra-Gómez^7}, Cristian Javier Cano-Mogollón^8}

^1} Autor 1: Isaías José Petro-Rodríguez - Universidad Pontificia Bolivariana, Seccional Montería, Córdoba, Colombia. ORCID: pendiente. Correo electrónico: isaias.petro@upb.edu.co

^2} Autor 2: Antolin De Jesús Vitola-Montes - Universidad Pontificia Bolivariana, Seccional Montería, Córdoba, Colombia. ORCID: pendiente. Correo electrónico: antolin.vitola@upb.edu.co

^3} Autor 3: Andrés Julián Negrete-Pacheco - Universidad Pontificia Bolivariana, Seccional Montería, Córdoba, Colombia. ORCID: pendiente. Correo electrónico: andresj.negretep@upb.edu.co

^4} Autor 4: Juliana Esther Carrascal-Hernández - Universidad Pontificia Bolivariana, Seccional Montería, Córdoba, Colombia. ORCID: pendiente. Correo electrónico: juliana.carrascal@upb.edu.co

^5} Autor 5: Angel Quintana-Jiménez - Universidad Pontificia Bolivariana, Seccional Montería, Córdoba, Colombia. ORCID: pendiente. Correo electrónico: angel.quintana@upb.edu.co

^6} Autor 6: Alejandro Pemberty-Vergara - Universidad Pontificia Bolivariana, Seccional Montería, Córdoba, Colombia. ORCID: pendiente. Correo electrónico: alejandro.pemberty@upb.edu.co

^7} Autor 7: Juan Diego Guerra-Gómez - Universidad Pontificia Bolivariana, Seccional Montería, Córdoba, Colombia. ORCID: pendiente. Correo electrónico: juan.guerra@upb.edu.co

^8} Co-Autor / Co-Investigador: M.Sc. Cristian Javier Cano Mogollón. Filiación: Docente Titular, Facultad de Ingeniería Industrial. Grupo de Investigación en Simulación, Logística y Gestión de Operaciones (SILOGE), Hub Industrial Solution (HIS), Universidad Pontificia Bolivariana, Seccional Montería, Colombia. ORCID: pendiente. Correo electrónico: cristian.cano@upb.edu.co

^*} Autor de correspondencia: Isaías José Petro-Rodríguez (isaias.petro@upb.edu.co).

**Resumen:

Una cámara ve la mano todo el tiempo, también cuando el niño viaja de una seña a otra, y una aplicación que enseña notas con las manos debe sonar solo cuando hubo una seña intencional. Se describe y evalúa el reconocedor de Hand Sing Kids, que asigna una seña de dos manos a cada una de las ocho notas de Do3 a Do4. Cada postura se codifica con un vector de 120 componentes invariante al tamaño, la posición y el giro de la mano, se clasifica por vecino más cercano y se acepta solo si la distancia, la confianza y el margen sobre la segunda nota son suficientes. Con una calibración de una persona y perturbaciones simuladas, 480 señas válidas por nivel de ruido se reconocieron en 100 % sin ruido y en 86,0 % con ruido de 0,09. Ante 640 posturas que no son seña, el método propuesto disparó una nota por error en 8,0 % de los casos (IC 95 %: 6,1 a 10,3 %), frente a 100 % del método de la versión inicial, que acierta siempre porque responde siempre. El error restante viene sobre todo de las transiciones entre señas. No hubo pruebas con niños; el nivel de madurez es TRL 4 y el efecto en el aula es una hipótesis.

**Palabras clave:

reconocimiento de gestos; seguimiento de manos; descriptor invariante; vecino más cercano; falsos positivos; educación musical infantil; Montería

**Abstract:

A camera sees the hand all the time, including when a child moves from one sign to another, and an application that teaches notes with the hands should sound only when a sign was intentional. The recognizer of Hand Sing Kids, which assigns a two-handed sign to each of the eight notes from C3 to C4, is described and evaluated. Each posture is encoded as a 120-component vector invariant to hand size, position and rotation, classified by nearest neighbour and accepted only if the distance, the confidence and the margin over the second note are sufficient. With a single-person calibration and simulated perturbations, 480 valid signs per noise level were recognized at 100 % without noise and 86,0 % at noise 0.09. Over 640 postures that are not signs, the proposed method fired a wrong note in 8,0 % of cases (95 % CI 6,1 to 10,3 %), against 100 % for the initial method, which is always right because it always answers. The remaining error comes mostly from transitions between signs. No tests with children were done; the readiness level is TRL 4 and the classroom effect is a hypothesis.

**Keywords:

gesture recognition; hand tracking; invariant descriptor; nearest neighbour; false positives; children's music education; Montería

# Introducción

## Responder siempre no es reconocer

Un sistema de visión por computador sobre una mano enfrenta una dificultad que no aparece en un teclado: el teclado solo emite una señal cuando alguien lo oprime, mientras que la cámara entrega una postura en cada fotograma. En Hand Sing Kids cada nota de la escala, de Do3 a Do4, corresponde a una seña de las dos manos. Entre una seña y otra la mano pasa por posiciones intermedias, y a veces las manos se cruzan o se tapan. Si el programa convierte cada postura en una nota, el niño oirá sonidos que no pidió. El problema, entonces, no es solo de exactitud sobre señas válidas, sino de saber cuándo no responder.

MediaPipe Hands entrega 21 puntos por mano en tiempo real en un dispositivo común [1], y con ellos se pueden construir clasificadores muy distintos. La pregunta de este trabajo es qué descripción de la postura y qué regla de decisión permiten rechazar lo que no es una seña sin perder las señas buenas, usando solo la calibración de una persona. Se mide con 480 señas por nivel de ruido y con 640 posturas que no son seña, con intervalos de confianza de Wilson [2].

## Antecedentes

La literatura reciente aplica visión e inteligencia artificial a la enseñanza musical de varias formas: detección visual del teclado y retroalimentación para piano [3], [4], trayectorias de aprendizaje personalizadas [5]–[9], sistemas sensibles a la emoción [10], [11], generación de partituras según dificultad [12] y aplicaciones y realidad aumentada [13]–[15]. Una revisión sobre primera infancia resume las tecnologías de IA disponibles [16]. En los títulos y metadatos revisados no apareció un trabajo que parta de una seña manual por nota calibrada para cada niño; no se leyeron los textos completos, así que esto no excluye que exista.

*Tabla 1. Decisiones que debe tomar el reconocedor y cómo las resuelve el método propuesto

*Fuente: elaboración propia a partir del código y de las pruebas del repositorio.

## Objetivo

Describir el reconocedor de señas de Hand Sing Kids y medir, en laboratorio y con perturbaciones simuladas, cuántas señas válidas reconoce y cuántas notas dispara por error, frente al método de la versión inicial.

# Métodos

## Sistema

La aplicación es de escritorio, escrita en Python. La cámara alimenta a MediaPipe Hands; el descriptor y el clasificador convierten los 21 puntos de cada mano en una nota candidata; un estabilizador decide si la nota se confirma; y la capa pedagógica usa esa nota para registrar el intento y elegir la siguiente actividad (Figura 1). Este trabajo estudia solo la parte perceptiva, hasta la confirmación de la nota.

*Figura 1. Arquitectura funcional de Hand Sing Kids; el reconocedor ocupa los primeros bloques.

## Descriptor invariante

Sean p_0,dots,p_20}inmathbb{R}^3 los 21 puntos de una mano, con p_0 en la muñeca. La escala de referencia es la distancia de la muñeca al nudillo del dedo medio:

La curvatura de cada dedo, con cadena de articulaciones (a,b,c,d), es una razón entre longitudes y por tanto invariante a escala, traslación y rotación:

La apertura entre dedos contiguos usa los vectores unitarios u_i del nudillo a la yema, y la distancia del pulgar a cada yema se normaliza con sigma:

A estas magnitudes se suman la normal del plano de la palma, la dirección de la mano en la imagen y la forma normalizada (20 puntos trasladados, escalados por sigma y girados para que la mano apunte hacia arriba, 40 valores). Cada mano queda en 58 valores y, con cuatro magnitudes de geometría entre las dos manos, el descriptor completo tiene 2times 58+4=120 componentes. Las distancias se calculan por bloques g, cada uno con su peso w_g (curvatura 3,0; forma 2,6; pulgar 2,0; dirección 2,0; entre manos 1,6; normal 1,4; apertura 1,2), para que los 40 valores de la forma no dominen a los 5 de la curvatura:

## Clasificación con confianza y margen

Cada nota c conserva hasta tres muestras S_c tomadas en la calibración del niño. La distancia de una postura x a la nota es la menor de sus muestras, y la confianza reparte probabilidad entre las notas con una temperatura T ajustada a la separación real de las señas del niño:

La nota se acepta solo si cumple las tres condiciones de la ecuación (9). La tercera, el margen, hace que el sistema se abstenga cuando dos señas empatan:

## Estabilización temporal

El estabilizador mantiene una ventana de N lecturas, con N=1 por defecto. Una nota se confirma si aparece en al menos max(1,operatorname{round}(0,62,N)) posiciones, si su confianza media alcanza 0,55, si pasaron al menos 0,45 s desde la confirmación anterior (periodo refractario) y, cuando repite la última nota, solo si el niño la soltó antes. Se considera soltada cuando R=6 fotogramas consecutivos arrojan una lectura distinta. Este valor es el del código (`release_frames = 6`); la documentación del proyecto menciona dos fotogramas en su sección 3.5 y seis en el código y en la sección 11.6, y aquí se adopta el del código.

## Protocolo de evaluación técnica

La evaluación reproduce y amplía `tests/test_vision.py` sin modificarlo. La calibración de referencia contiene las ocho señas (Do3 a Do4) de una persona, guardadas como coordenadas de puntos de la mano, sin imágenes. Las perturbaciones son simuladas sobre esas coordenadas: escala entre 0,8 y 1,25, giro independiente por mano de ±18° y ruido gaussiano proporcional al tamaño de la mano. Se miden dos cosas. Primera, la tasa de reconocimiento de señas válidas con ruido sigmain{0; 0,03; 0,06; 0,09}: 60 repeticiones por nota y nivel, 480 señas por nivel. Segunda, las notas disparadas por error en 640 posturas que no son seña: 320 transiciones a medio camino entre una nota y otra tres posiciones más adelante, y 320 combinaciones de la mano izquierda de una seña con la derecha de otra. Las tasas se acompañan de intervalos de Wilson al 95 % [2], y la estabilidad de la tasa de falsos positivos se midió con 30 semillas distintas. También se calculó la matriz de similitud entre las ocho señas con ambos métodos, la latencia del descriptor más el clasificador (2.000 repeticiones) y se ejecutaron las ocho baterías de prueba del repositorio. Los scripts están en `entrega_corte3/analisis/` y se ejecutan con una sola orden.

# Resultados

## Reconocimiento de señas válidas

*Tabla 2. Señas válidas reconocidas (%) según el ruido, con intervalo de Wilson al 95 %

*Fuente: elaboración propia (analisis/evidencia_vision.py, semilla 11).

Con ruido hasta 0,03 el descriptor propuesto reconoció todas las señas; con 0,06 llegó a 96,9 % y con 0,09 a 86,0 % (IC 95 %: 82,7 a 88,9 %). El método de la versión 1 acierta en todos los casos, pero esto se explica por lo que muestra la Tabla 3: responde siempre.

## Posturas que no son seña

*Tabla 3. Notas disparadas por error ante posturas que no son seña (k; %; IC de Wilson al 95 %)

*Fuente: elaboración propia (analisis/evidencia_vision.py, semilla 23).

El descriptor propuesto disparó 51 notas por error en 640 posturas (8,0 %, IC 95 %: 6,1 a 10,3 %), contra el 100 % del método v1. La tasa de 8 % reportada en la documentación se reproduce. Con 30 semillas distintas la tasa media fue 7,5 % (desviación estándar 0,8; mínimo 6,1 %; máximo 9,2 %), de modo que el valor no depende de una semilla favorable. El desglose no figuraba en la documentación y cambia la lectura: casi todo el error viene de las transiciones (13,8 %), mientras que las manos cruzadas casi no disparan (2,2 %). Esto es plausible porque una postura a medio camino conserva rasgos de las dos señas extremas y una mano de cada seña no se parece a ninguna.

*Figura 2. (a) Señas válidas reconocidas según el ruido (barras de error: IC de Wilson al 95 %; el eje parte de 70 %). (b) Notas disparadas por error ante posturas que no son seña, con los casos k/n.

## Separabilidad de las señas y latencia

Con la calibración real, 30 de los 56 pares ordenados de notas distintas (es decir, 15 pares no ordenados de 28) superan una similitud coseno de 0,65, el umbral del método v1. El par más parecido es SI3–DO4 con 0,902. En el descriptor propuesto, la distancia entre notas distintas va de 0,183 a 0,674, lo que ajusta la temperatura a T=0,092 según la ecuación (8). La Figura 3 muestra ambas matrices. En el método v1, dos nubes de puntos con forma de mano siempre se parecen, y por eso un umbral fijo de similitud no separa notas; el descriptor desplaza la comparación a magnitudes que sí cambian de una seña a otra.

*Figura 3. Matrices 8 × 8 de las señas calibradas: (a) similitud coseno del método v1; (b) distancia por bloques del descriptor propuesto.

El descriptor y el clasificador tardaron 0,89 ms por fotograma en promedio (percentil 95: 1,28 ms; máximo: 2,62 ms; 2000 repeticiones, un solo equipo). Esta cifra excluye la captura, el rastreo de MediaPipe y el dibujo en pantalla; la latencia de extremo a extremo, de la cámara a la pantalla, no se midió.

# Discusión

**Qué se ganó y qué se perdió.** La comparación entre métodos no debe leerse como una victoria completa. El método de la versión inicial reconoce todas las señas porque convierte toda postura en la nota más parecida, y por eso su tasa de acierto es perfecta y su tasa de notas falsas, total. El método propuesto acepta menos: con ruido de 0,09 baja a 86,0 %. Esa pérdida es el precio de rechazar lo dudoso. En un juego infantil, pedir que se repita una seña cuesta unos segundos; una nota falsa interrumpe la actividad y puede enseñar un sonido equivocado.

**Dónde está el error que queda.** Las transiciones explican casi todos los falsos positivos y las manos cruzadas casi ninguno. Una postura a medio camino hereda rasgos de las dos señas extremas y puede parecerse a una de ellas; una mano de cada seña, en cambio, no se parece a ninguna. Esto sugiere un siguiente paso concreto: usar la velocidad de la mano como señal adicional, porque una postura en movimiento rápido difícilmente es una seña deliberada. El código actual no usa velocidad en la decisión.

**Amenazas a la validez.** La calibración es de una sola persona y de ocho señas, y no se conoce la variabilidad entre niños; las perturbaciones se simularon sobre coordenadas ya extraídas, de modo que no incluyen errores de detección, desenfoque ni iluminación; las posturas negativas se construyeron por interpolación y combinación y la tasa real depende de cómo se mueven los niños; y el método inicial se evaluó con la misma calibración. Por eso los resultados describen el comportamiento del reconocedor en laboratorio y no su rendimiento en el aula.

Los demás componentes del sistema, como el seguimiento del dominio, el repaso espaciado y la selección de actividades, se tratan en otros trabajos del equipo y en la literatura sobre aprendizaje adaptativo [17]–[21].

## Madurez tecnológica

El reconocedor está en TRL 4: sus componentes funcionan integrados y se validaron en laboratorio con mediciones repetibles, pero ninguno se probó en el entorno de uso, con niños, cámaras y luz reales. El paso a TRL 5 exige un piloto en aula, cuyo protocolo está diseñado y no se ha ejecutado; el nivel final debe confirmarlo el equipo.

# Conclusiones

Un descriptor invariante de 120 componentes con decisión por distancia, confianza y margen redujo las notas disparadas por error de 100 % a 8,0 % en 640 posturas que no son seña, con un costo en sensibilidad visible solo con ruido alto (86,0 % con 0,09). El error que queda se concentra en las transiciones. El reconocedor se comporta como se describe en laboratorio; no se ha medido en niños, y el nivel de madurez es TRL 4.

# Recomendaciones

(1) Calibrar y medir con varios niños y en el aula, con iluminación y cámaras reales. (2) Incorporar la velocidad de la mano a la decisión y medir si reduce los falsos positivos de las transiciones. (3) Registrar las notas falsas durante un piloto en lugar de simularlas. (4) Medir la latencia de extremo a extremo, incluida la cámara.

## Contribución de los autores

Contribución de los autores (CRediT, por confirmar por el equipo): el primer autor planteó la evaluación del reconocedor, ejecutó las mediciones y redactó el borrador; los demás autores participaron en el desarrollo del software, la revisión bibliográfica y la revisión del texto; Cristian Javier Cano-Mogollón supervisó y revisó el manuscrito.

## Declaraciones finales

[Heading 3] Financiación

Esta investigación no recibió financiación externa. [Por confirmar por el equipo.]

[Heading 3] Conflicto de intereses

Los autores declaran que no existen conflictos de intereses relacionados con esta publicación. [Por confirmar.]

[Heading 3] Consentimiento informado

No aplica. La calibración de referencia contiene solo coordenadas de puntos de la mano de una persona, sin imágenes, y no se recolectaron datos de niños.

[Heading 3] Declaración de la Junta de Revisión Institucional

No aplica, porque el estudio es una evaluación técnica de laboratorio. Una prueba con niños requerirá aprobación ética y consentimiento de los acudientes.

[Heading 3] Disponibilidad de datos, código y materiales de investigación

El código, la calibración de referencia, las pruebas y los scripts de evaluación están en el repositorio del proyecto. Las salidas de las mediciones (resultados_vision.json) y la verificación de referencias están en la carpeta de análisis de la entrega.

[Heading 3] Uso de herramientas de inteligencia artificial

Se usó un asistente de inteligencia artificial (Claude, de Anthropic) para apoyar el análisis del código, la ejecución de las mediciones, la verificación de referencias y la redacción de borradores. Los autores revisaron el contenido y responden por él.

**Declarations (English)

Author Contributions: the first author designed the recognizer evaluation, ran the measurements and drafted the manuscript; the other authors contributed software development, literature review and text review; C. J. Cano-Mogollón supervised and reviewed. Funding: none external. No conflicts of interest. Informed consent and IRB: not applicable (laboratory evaluation). Data and code: project repository and analysis folder.

# References

[1] F. Zhang et al., “MediaPipe Hands: On-device Real-time Hand Tracking,” arXiv:2006.10214, 2020, doi: 10.48550/arXiv.2006.10214.

[2] E. B. Wilson, “Probable Inference, the Law of Succession, and Statistical Inference,” Journal of the American Statistical Association, vol. 22, no. 158, pp. 209-212, 1927, doi: 10.1080/01621459.1927.10502953.

[3] X. Deng, “AI-Based Feedback Systems in Piano Education: Effects on Technical Accuracy and Learner Autonomy,” Música Hodie, vol. 26, 2026, doi: 10.5216/mh.v26.85176.

[4] T. Chuluunsaikhan and S. H. Park, “Piano keyboard detection algorithm using deep learning,” Multimedia Tools and Applications, vol. 85, no. 5, art. 508, 2026, doi: 10.1007/s11042-026-21667-y.

[5] N. Li and Z. Hong, “Deep Reinforcement Learning for Personalised Music Learning Pathways,” Annals of Data Science, vol. 13, no. 4, pp. 1013-1032, 2026, doi: 10.1007/s40745-026-00689-1.

[6] J. Li, “A reinforcement learning-based adaptive evaluation framework for personalized music education,” PeerJ Computer Science, vol. 12, art. e3464, 2026, doi: 10.7717/peerj-cs.3464.

[7] J. Li, “Deep learning-based personalized learning path planning and optimization model for music education,” Discover Artificial Intelligence, vol. 6, no. 1, art. 434, 2026, doi: 10.1007/s44163-026-01115-4.

[8] X. Tang, “The application of deep reinforcement learning in music teaching interaction,” Discover Computing, vol. 29, no. 1, art. 131, 2026, doi: 10.1007/s10791-026-10022-2.

[9] Z. Wang, “Music teaching evaluation using multimodal deep reinforcement learning,” Discover Artificial Intelligence, vol. 6, no. 1, art. 151, 2026, doi: 10.1007/s44163-026-00832-0.

[10] X. Deng, Y. Zhou, X. Guan, and Y. Wang, “An adaptive emotion aware music education system using machine learning for personalized emotional wellbeing enhancement,” Scientific Reports, vol. 16, no. 1, art. 25833, 2026, doi: 10.1038/s41598-026-53749-0.

[11] X. Shi, “An affective computing framework for preschool music education using MoE architecture and neural radiance fields,” Discover Artificial Intelligence, vol. 6, no. 1, art. 812, 2026, doi: 10.1007/s44163-026-01858-0.

[12] P. Ramoneda, M. Suzuki, A. Maezawa, and X. Serra, “Difficulty-aware score generation for piano sight-reading,” Expert Systems with Applications, vol. 321, art. 132088, 2026, doi: 10.1016/j.eswa.2026.132088.

[13] K. Apaydinli, “Content analysis of music education studies related to augmented reality technology,” Journal of Educational Technology and Online Learning, vol. 6, no. 2, pp. 447-481, 2023, doi: 10.31681/jetol.1243501.

[14] J. Barroso-Osuna, A. León-Garrido, C. Llorente-Cejudo, and J. Ruiz-Palmero, “El impacto de las apps móviles y la carga del trabajo en la Educación Musical universitaria: un estudio experimental,” Revista de Educación a Distancia (RED), vol. 24, no. 80, 2024, doi: 10.6018/red.602301.

[15] A. León-Garrido, J. M. Barroso-Osuna, and M. C. Llorente-Cejudo, “Diseño y validación de un instrumento de evaluación para apps móviles musicales a través del juicio de expertos,” Aula Abierta, vol. 53, no. 2, pp. 169-179, 2024, doi: 10.17811/rifie.20620.

[16] H. Yi, T. Liu, and G. Lan, “The key artificial intelligence technologies in early childhood education: a review,” Artificial Intelligence Review, vol. 57, no. 1, art. 12, 2024, doi: 10.1007/s10462-023-10637-7.

[17] N. J. Cepeda, H. Pashler, E. Vul, J. T. Wixted, and D. Rohrer, “Distributed practice in verbal recall tasks: A review and quantitative synthesis.,” Psychological Bulletin, vol. 132, no. 3, pp. 354-380, 2006, doi: 10.1037/0033-2909.132.3.354.

[18] A. T. Corbett and J. R. Anderson, “Knowledge tracing: Modeling the acquisition of procedural knowledge,” User Modelling and User-Adapted Interaction, vol. 4, no. 4, pp. 253-278, 1995, doi: 10.1007/BF01099821.

[19] R. C. Wilson, A. Shenhav, M. Straccia, and J. D. Cohen, “The Eighty Five Percent Rule for optimal learning,” Nature Communications, vol. 10, no. 1, art. 4646, 2019, doi: 10.1038/s41467-019-12552-4.

[20] P. Woźniak and E. Gorzelańczyk, “Optimization of repetition spacing in the practice of learning,” Acta Neurobiologiae Experimentalis, vol. 54, no. 1, pp. 59-62, 1994, doi: 10.55782/ane-1994-1003.

[21] DANE, “Proyecciones de población municipal 2020–2035, actualización post COVID-19 (Montería, 2026),” Bogotá, Colombia. [Online]. Available: https://www.dane.gov.co/files/censo2018/proyecciones-de-poblacion/Municipal/DCD-area-sexo-edad-proypoblacion-Mun-2020-2035-ActPostCOVID-19.xlsx. Accessed: Nov. 5, 2026.

---
## Avisos

- La calibración es de **una sola persona** y el ruido es **simulado**; lo dices en el preprint y en las amenazas a la validez.
- El 8,0 % de notas falsas se concentra en las transiciones (13,8 %); las manos cruzadas casi no fallan (2,2 %). Es el hallazgo más fino de tu artículo.

## Guion de defensa

**¿Por qué el método inicial acierta 100 % y es peor?**  
Porque responde siempre: acierta toda seña válida, pero convierte toda postura en una nota, incluidas las 640 que no son seña (100 % de notas falsas).

**¿Qué es el descriptor invariante?**  
Un vector de 120 componentes (curvatura, apertura, pulgar, forma, relación entre manos) que no cambia con el tamaño, la posición ni el giro de la mano; se calcula con razones entre longitudes y vectores unitarios.

**¿Cómo decide el clasificador?**  
Vecino más cercano sobre hasta tres muestras por nota; acepta si la distancia es ≤ 0,95, la confianza ≥ 0,55 y el margen sobre la segunda nota ≥ 0,08.

**¿Por qué baja a 86,0 % con ruido 0,09?**  
Es el precio de abstenerse cuando hay duda: pedir que se repita una seña cuesta segundos; una nota falsa rompe la actividad.

**¿Qué falta?**  
Más personas y niños, errores reales de detección, iluminación, velocidad de la mano como señal adicional y latencia de extremo a extremo.
