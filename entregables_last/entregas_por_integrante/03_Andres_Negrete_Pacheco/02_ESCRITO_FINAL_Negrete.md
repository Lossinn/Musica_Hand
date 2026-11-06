# ESCRITO FINAL — Andrés Julián Negrete Pacheco

**Tu hilo:** El tiempo y la retroalimentación: la nota debe sonar cuando el niño la espera, una sola vez y sin castigarlo por el retraso del reconocimiento. Estabilizador, ventana asimétrica y puntaje del módulo Canciones.

**Preprint y artículo:** Tu preprint habla de reconocer gestos con la cámara, dar retroalimentación adecuada, adaptar niveles y aprender mediante el juego. Tu artículo explica cómo se logra la retroalimentación en el tiempo correcto: estabilizador, ventana de acierto y puntaje de canciones.

---
## ESCRITO FINAL 1 — Preprint

**Andrés Julián Negrete Pacheco**

La propuesta Hand Sing Kids busca mejorar la enseñanza de la teoría musical a los niños mediante el uso de tecnologías de visión computacional e inteligencia artificial. Lo principal que se busca es el desarrollo de una herramienta lúdica que permita el reconocimiento de gestos mediante el vectorizado de manos a través de una cámara y poder relacionarlos con conceptos musicales, y así poder facilitar el aprendizaje de una forma más práctica, interactiva y entretenida.

La herramienta funciona utilizando Python, OpenCV y MediaPipe Hands, que permiten identificar las manos y así poder reconocer gestos y movimientos. A partir de la información, el sistema evalúa la respuesta para los niños, puede tomar el gesto que va acorde con su respectiva nota y así poder dar una retroalimentación adecuada. El aplicativo también puede tener en cuenta el desempeño de cada usuario y así poder adaptar los niveles y facilitar su progreso.

La propuesta del aplicativo surge de la búsqueda de alternativas que existen frente a algunas dificultades presentes en la educación musical y la necesidad de implementar estrategias que incentiven el interés por el aprendizaje musical, así poder complementar los métodos tradicionales de enseñanza y una nueva experiencia de aprendizaje mediante el juego.

---
## ESCRITO FINAL 2 — Resumen y abstract

**Resumen.** En una aplicación que enseña notas con las manos, reconocer bien no basta: la nota debe sonar en el momento en que el niño la espera, una sola vez y sin castigarlo por el tiempo que el sistema tarda en confirmar. Se describen y analizan los mecanismos temporales de Hand Sing Kids: el estabilizador que confirma una nota con periodo refractario y detección de suelta, y el motor del módulo Canciones, que usa el reloj de la partida, una ventana de acierto asimétrica y un puntaje con combo. Se explican la ventana mínima de 480 ms, el umbral de suelta de seis fotogramas y el efecto del parpadeo del seguimiento de manos, que provocó que una misma nota sonara dos veces. El descriptor y el clasificador tardan 0,89 ms por fotograma en promedio (1,28 ms en el percentil 95), sin contar cámara ni dibujo en pantalla. En laboratorio, el método disparó una nota por error en 8,0 % de 640 posturas que no son seña. No hubo pruebas con niños; el diseño temporal es una propuesta por validar con ellos, y el nivel de madurez es TRL 4.

**Abstract.** In an application that teaches notes with the hands, recognizing well is not enough: the note must sound when the child expects it, once, and without penalizing the child for the time the system takes to confirm. The temporal mechanisms of Hand Sing Kids are described and analysed: the stabilizer that confirms a note with a refractory period and release detection, and the engine of the Songs module, which uses the game clock, an asymmetric hit window and a combo score. The 480 ms minimum window, the six-frame release threshold and the effect of hand-tracking flicker, which made one note sound twice, are explained. The descriptor and classifier take 0,89 ms per frame on average (1,28 ms at the 95th percentile), excluding camera and display. In the laboratory, the method fired a wrong note in 8,0 % of 640 non-sign postures. No tests with children were done; the temporal design is a proposal to be validated with them, and the readiness level is TRL 4.

---
## ESCRITO FINAL 3 — Texto del artículo

[Título art] Cuándo debe sonar la nota: estabilización temporal, ventanas de acierto y retroalimentación en el módulo de canciones de Hand Sing Kids

[Título art] When the note should sound: temporal stabilization, hit windows and feedback in the songs module of Hand Sing Kids

[Nombre autores] Andrés Julián Negrete-Pacheco^1}^*}, Antolin De Jesús Vitola-Montes^2}, Isaías José Petro-Rodríguez^3}, Juliana Esther Carrascal-Hernández^4}, Angel Quintana-Jiménez^5}, Alejandro Pemberty-Vergara^6}, Juan Diego Guerra-Gómez^7}, Cristian Javier Cano-Mogollón^8}

^1} Autor 1: Andrés Julián Negrete-Pacheco - Universidad Pontificia Bolivariana, Seccional Montería, Córdoba, Colombia. ORCID: pendiente. Correo electrónico: andresj.negretep@upb.edu.co

^2} Autor 2: Antolin De Jesús Vitola-Montes - Universidad Pontificia Bolivariana, Seccional Montería, Córdoba, Colombia. ORCID: pendiente. Correo electrónico: antolin.vitola@upb.edu.co

^3} Autor 3: Isaías José Petro-Rodríguez - Universidad Pontificia Bolivariana, Seccional Montería, Córdoba, Colombia. ORCID: pendiente. Correo electrónico: isaias.petro@upb.edu.co

^4} Autor 4: Juliana Esther Carrascal-Hernández - Universidad Pontificia Bolivariana, Seccional Montería, Córdoba, Colombia. ORCID: pendiente. Correo electrónico: juliana.carrascal@upb.edu.co

^5} Autor 5: Angel Quintana-Jiménez - Universidad Pontificia Bolivariana, Seccional Montería, Córdoba, Colombia. ORCID: pendiente. Correo electrónico: angel.quintana@upb.edu.co

^6} Autor 6: Alejandro Pemberty-Vergara - Universidad Pontificia Bolivariana, Seccional Montería, Córdoba, Colombia. ORCID: pendiente. Correo electrónico: alejandro.pemberty@upb.edu.co

^7} Autor 7: Juan Diego Guerra-Gómez - Universidad Pontificia Bolivariana, Seccional Montería, Córdoba, Colombia. ORCID: pendiente. Correo electrónico: juan.guerra@upb.edu.co

^8} Co-Autor / Co-Investigador: M.Sc. Cristian Javier Cano Mogollón. Filiación: Docente Titular, Facultad de Ingeniería Industrial. Grupo de Investigación en Simulación, Logística y Gestión de Operaciones (SILOGE), Hub Industrial Solution (HIS), Universidad Pontificia Bolivariana, Seccional Montería, Colombia. ORCID: pendiente. Correo electrónico: cristian.cano@upb.edu.co

^*} Autor de correspondencia: Andrés Julián Negrete-Pacheco (andresj.negretep@upb.edu.co).

**Resumen:

En una aplicación que enseña notas con las manos, reconocer bien no basta: la nota debe sonar en el momento en que el niño la espera, una sola vez y sin castigarlo por el tiempo que el sistema tarda en confirmar. Se describen y analizan los mecanismos temporales de Hand Sing Kids: el estabilizador que confirma una nota con periodo refractario y detección de suelta, y el motor del módulo Canciones, que usa el reloj de la partida, una ventana de acierto asimétrica y un puntaje con combo. Se explican la ventana mínima de 480 ms, el umbral de suelta de seis fotogramas y el efecto del parpadeo del seguimiento de manos, que provocó que una misma nota sonara dos veces. El descriptor y el clasificador tardan 0,89 ms por fotograma en promedio (1,28 ms en el percentil 95), sin contar cámara ni dibujo en pantalla. En laboratorio, el método disparó una nota por error en 8,0 % de 640 posturas que no son seña. No hubo pruebas con niños; el diseño temporal es una propuesta por validar con ellos, y el nivel de madurez es TRL 4.

**Palabras clave:

retroalimentación; estabilización temporal; ventana de acierto; periodo refractario; gamificación; educación musical infantil; Montería

**Abstract:

In an application that teaches notes with the hands, recognizing well is not enough: the note must sound when the child expects it, once, and without penalizing the child for the time the system takes to confirm. The temporal mechanisms of Hand Sing Kids are described and analysed: the stabilizer that confirms a note with a refractory period and release detection, and the engine of the Songs module, which uses the game clock, an asymmetric hit window and a combo score. The 480 ms minimum window, the six-frame release threshold and the effect of hand-tracking flicker, which made one note sound twice, are explained. The descriptor and classifier take 0,89 ms per frame on average (1,28 ms at the 95th percentile), excluding camera and display. In the laboratory, the method fired a wrong note in 8,0 % of 640 non-sign postures. No tests with children were done; the temporal design is a proposal to be validated with them, and the readiness level is TRL 4.

**Keywords:

feedback; temporal stabilization; hit window; refractory period; gamification; children's music education; Montería

# Introducción

## El momento de la respuesta

Cuando un niño hace una seña y espera oír la nota, cada décima de segundo cuenta. Si el sonido llega muy tarde, el niño no lo asocia con su gesto; si llega antes de que termine de formar la seña, suena una nota equivocada; si suena dos veces, cree que se equivocó. El problema de reconocer una seña ya es difícil por sí mismo, pero el de decidir cuándo confirmarla es distinto y, en una aplicación de juego, pesa tanto como el primero.

Hand Sing Kids reconoce ocho señas de dos manos, de Do3 a Do4, con una cámara y MediaPipe Hands [1]. La herramienta ofrece actividades guiadas y un módulo de canciones en que el niño debe producir las notas al compás de una melodía. En el segundo caso, el sistema no espera la seña: el tiempo lo marca el reloj de la partida y el niño debe acertar dentro de una ventana. Eso obliga a decidir qué tan ancha es esa ventana y cuánto del retraso del reconocimiento se le perdona al niño.

## Trabajos relacionados

La retroalimentación con inteligencia artificial en la enseñanza de piano se ha estudiado en cuanto a exactitud técnica [2] y la detección visual del teclado con aprendizaje profundo ya existe [3]. Otros trabajos proponen trayectorias de aprendizaje personalizadas [4]–[8], sistemas con emoción [9], [10] y análisis de aplicaciones móviles de música [11]–[13]. En los títulos revisados, ninguno describe el diseño temporal de una entrada por seña manual; no se leyeron los textos completos. Para la dificultad de las actividades se usa una idea conocida del aprendizaje: que la práctica es más eficiente cuando el error ni es muy raro ni muy frecuente [14].

*Tabla 1. Fallas temporales posibles en un juego de gestos y el mecanismo que las atiende

*Fuente: elaboración propia a partir del código y de la documentación del proyecto.

## Objetivo

Describir con precisión los mecanismos temporales de Hand Sing Kids, mostrar qué errores previene cada uno y cuantificar, con las fórmulas del código, el efecto del tempo sobre la ventana de acierto.

# Métodos

## Estabilizador de notas

Entre la lectura de la cámara y el sonido hay un estabilizador. Una nota se confirma si el clasificador la ve con confianza suficiente, si pasaron al menos 0,45 s desde la nota anterior (periodo refractario) y, si es la misma nota que la última, solo cuando el niño la soltó. Se considera soltada cuando seis fotogramas consecutivos arrojan una lectura distinta. En su configuración por defecto, el estabilizador usa una ventana de un fotograma, de modo que la nota suena en cuanto se reconoce, sin barra de espera.

El valor de seis fotogramas merece una explicación porque cambió. La documentación del proyecto menciona dos fotogramas, y el código usa seis. La diferencia no es un descuido: con la ventana de varios fotogramas, la votación absorbía los parpadeos del rastreo; al pasar a un fotograma, el mecanismo de suelta quedó como único filtro y dos fotogramas resultaron insuficientes. Aquí se adopta el valor del código.

## Módulo Canciones

El motor del módulo Canciones usa el reloj de la partida y no espera la seña. Con tempo text{bpm}, el intervalo entre notas es g=60000/text{bpm} ms, la nota i llega en a_i=a_i-1}+g con a_0=2200 ms, y su ventana de acierto es asimétrica, más ancha antes de la línea que después, para no penalizar al niño por el tiempo que el reconocimiento tarda en confirmar:

El puntaje por nota es 100, 70 o 50 puntos según el error temporal (perfecto, bien, vale) y se multiplica por min(1+0,5lfloor c/10rfloor,,4), con c el combo de aciertos seguidos. Hay tres factores de tempo (0,72; 1,0; 1,15). El catálogo tiene 19 canciones de melodía tradicional o de dominio público, simplificadas a las ocho notas.

## Cálculo de la ventana

Para estudiar el efecto del tempo se calculó, con la ecuación de la ventana, su ancho total 2h_i y su reparto antes y después de la línea para distintos tempos, suponiendo que la tolerancia text{tol} no limita el valor, es decir, que min(text{tol},0,85,g)=0,85,g. Es un cálculo derivado de la fórmula, no una medición.

# Resultados

## Efecto del tempo sobre la ventana de acierto

*Tabla 2. Ventana de acierto según el tempo (ms), con tolerancia no limitante

*Fuente: cálculo propio con la ecuación de la ventana; W_min = 480 ms.

Hasta unos 100 bpm la ventana depende solo del intervalo entre notas, y a partir de ahí actúa el piso de 480 ms: a 120 bpm, el 85 % del intervalo es de 425 ms y la ventana se mantiene en 480 ms, con 276 ms antes y 204 ms después de la línea. La asimetría hace que el niño tenga más margen para adelantarse que para retrasarse, lo que compensa el tiempo que tarda el reconocimiento en confirmar. En el factor de tempo más rápido del módulo (1,15), esto importa más que en el más lento (0,72).

*Figura 1. Reparto de la ventana de acierto antes y después de la línea de la nota, según el tempo.

## Costo del reconocimiento en el tiempo de respuesta

El descriptor y el clasificador tardaron 0,89 ms por fotograma en promedio, con percentil 95 de 1,28 ms y máximo de 2,62 ms en 2000 repeticiones, en un solo equipo. Esa cifra es una fracción pequeña de la ventana mínima de 480 ms, pero no incluye la captura de la cámara, el rastreo de MediaPipe ni el dibujo en pantalla, que no se midieron. Por eso la latencia de extremo a extremo sigue siendo una incógnita.

## Falsos positivos y respuesta inmediata

Con una ventana de un fotograma, el método disparó una nota por error en 8,0 % de 640 posturas que no son seña (IC 95 %: 6,1 a 10,3 %), casi todo en transiciones. Con votación de varios fotogramas, ese error se reduce, pero a cambio de una espera perceptible. Para niños pequeños se prefirió la respuesta inmediata, y la ventana puede ampliarse por niño desde los ajustes de la aplicación.

# Discusión

**Un caso de efecto cruzado.** Una nota sostenida sonaba dos veces. El clasificador no tenía la culpa: el rastreo de manos pierde la mano uno o dos fotogramas aunque esté quieta, y con ventana de un fotograma eso se leía como suelta, de modo que la siguiente lectura repetía la nota. Cuando se quitó la votación, el umbral de suelta, que antes casi no importaba, pasó a ser crítico. La enseñanza es que un parámetro cambiado en un módulo puede dejar a otro cargando con una función que nunca se probó por separado. Por eso la batería del estabilizador incluye ahora una prueba del parpadeo breve.

**Qué se le exige al niño y qué al sistema.** Con una ventana asimétrica y un piso de 480 ms, el sistema asume parte del retraso en lugar de cargarlo al niño. El puntaje de 100, 70 o 50 puntos y el combo con tope ×4 responden a una idea sencilla: reconocer el esfuerzo sin esconder los errores. No hay evidencia de que estos valores motiven a un niño; provienen de decisiones de diseño y de la documentación del proyecto, y habría que ajustarlos con observación en el aula.

**Límites.** La Tabla 2 es un cálculo, no una medición. Las constantes del estabilizador y del puntaje no se validaron con niños; la latencia de extremo a extremo no se midió; y las mediciones de falsos positivos usan posturas simuladas. Un piloto debería registrar, con niños reales, cuántas veces suena una nota dos veces, cuánto tarda el sonido desde la seña y cuántas veces el niño repite una seña porque no sonó.

Para las demás partes del sistema, como la estimación del dominio y la selección de la sesión, véanse los trabajos sobre práctica distribuida, seguimiento del conocimiento y rutas personalizadas [15]–[21].

# Conclusiones

Hand Sing Kids resuelve el problema del tiempo con tres piezas: un estabilizador con periodo refractario y detección de suelta, una ventana de acierto asimétrica con piso de 480 ms y un puntaje con combo. Se explicó por qué el umbral de suelta es de seis fotogramas y cómo el tempo reparte la ventana antes y después de la línea. Las constantes provienen del diseño y no de datos de niños; el nivel de madurez es TRL 4.

# Recomendaciones

(1) Medir la latencia de extremo a extremo con la cámara real. (2) Registrar, en un piloto, las notas duplicadas y las señas repetidas. (3) Ajustar el piso de la ventana y el puntaje con observaciones de niños y docentes. (4) Mantener la prueba del parpadeo breve en la batería del estabilizador.

## Contribución de los autores

Contribución de los autores (CRediT, por confirmar): el primer autor analizó los mecanismos temporales, calculó la ventana de acierto y redactó el borrador; los demás autores aportaron el desarrollo del software, las mediciones y la revisión; Cristian Javier Cano-Mogollón supervisó y revisó.

## Declaraciones finales

[Heading 3] Financiación

Sin financiación externa. [Por confirmar por el equipo.]

[Heading 3] Conflicto de intereses

No hay conflictos de intereses que declarar. [Por confirmar.]

[Heading 3] Consentimiento informado

No aplica: no se recolectaron datos de niños en este estudio.

[Heading 3] Declaración de la Junta de Revisión Institucional

No aplica a esta evaluación técnica; las pruebas de aula con menores necesitarán aprobación ética y consentimiento de acudientes.

[Heading 3] Disponibilidad de datos, código y materiales de investigación

El código, las pruebas del estabilizador y de canciones y los scripts de medición están en el repositorio del proyecto; los cálculos de la Tabla 2 se pueden reproducir con la ecuación de la ventana y los valores del código.

[Heading 3] Uso de herramientas de inteligencia artificial

Se empleó un asistente de IA (Claude, de Anthropic) para revisar el código, ejecutar las mediciones, verificar referencias y redactar borradores. Los autores revisaron y responden por el texto.

**Declarations (English)

Author Contributions: the first author analysed the temporal mechanisms, computed the hit window and drafted the manuscript; the other authors contributed software, measurements and review; C. J. Cano-Mogollón supervised. No external funding. No conflicts of interest. Consent and IRB: not applicable. Data and code: project repository.

# References

[1] F. Zhang et al., “MediaPipe Hands: On-device Real-time Hand Tracking,” arXiv:2006.10214, 2020, doi: 10.48550/arXiv.2006.10214.

[2] X. Deng, “AI-Based Feedback Systems in Piano Education: Effects on Technical Accuracy and Learner Autonomy,” Música Hodie, vol. 26, 2026, doi: 10.5216/mh.v26.85176.

[3] T. Chuluunsaikhan and S. H. Park, “Piano keyboard detection algorithm using deep learning,” Multimedia Tools and Applications, vol. 85, no. 5, art. 508, 2026, doi: 10.1007/s11042-026-21667-y.

[4] N. Li and Z. Hong, “Deep Reinforcement Learning for Personalised Music Learning Pathways,” Annals of Data Science, vol. 13, no. 4, pp. 1013-1032, 2026, doi: 10.1007/s40745-026-00689-1.

[5] J. Li, “A reinforcement learning-based adaptive evaluation framework for personalized music education,” PeerJ Computer Science, vol. 12, art. e3464, 2026, doi: 10.7717/peerj-cs.3464.

[6] J. Li, “Deep learning-based personalized learning path planning and optimization model for music education,” Discover Artificial Intelligence, vol. 6, no. 1, art. 434, 2026, doi: 10.1007/s44163-026-01115-4.

[7] X. Tang, “The application of deep reinforcement learning in music teaching interaction,” Discover Computing, vol. 29, no. 1, art. 131, 2026, doi: 10.1007/s10791-026-10022-2.

[8] Z. Wang, “Music teaching evaluation using multimodal deep reinforcement learning,” Discover Artificial Intelligence, vol. 6, no. 1, art. 151, 2026, doi: 10.1007/s44163-026-00832-0.

[9] X. Deng, Y. Zhou, X. Guan, and Y. Wang, “An adaptive emotion aware music education system using machine learning for personalized emotional wellbeing enhancement,” Scientific Reports, vol. 16, no. 1, art. 25833, 2026, doi: 10.1038/s41598-026-53749-0.

[10] X. Shi, “An affective computing framework for preschool music education using MoE architecture and neural radiance fields,” Discover Artificial Intelligence, vol. 6, no. 1, art. 812, 2026, doi: 10.1007/s44163-026-01858-0.

[11] K. Apaydinli, “Content analysis of music education studies related to augmented reality technology,” Journal of Educational Technology and Online Learning, vol. 6, no. 2, pp. 447-481, 2023, doi: 10.31681/jetol.1243501.

[12] J. Barroso-Osuna, A. León-Garrido, C. Llorente-Cejudo, and J. Ruiz-Palmero, “El impacto de las apps móviles y la carga del trabajo en la Educación Musical universitaria: un estudio experimental,” Revista de Educación a Distancia (RED), vol. 24, no. 80, 2024, doi: 10.6018/red.602301.

[13] A. León-Garrido, J. M. Barroso-Osuna, and M. C. Llorente-Cejudo, “Diseño y validación de un instrumento de evaluación para apps móviles musicales a través del juicio de expertos,” Aula Abierta, vol. 53, no. 2, pp. 169-179, 2024, doi: 10.17811/rifie.20620.

[14] R. C. Wilson, A. Shenhav, M. Straccia, and J. D. Cohen, “The Eighty Five Percent Rule for optimal learning,” Nature Communications, vol. 10, no. 1, art. 4646, 2019, doi: 10.1038/s41467-019-12552-4.

[15] H. Yi, T. Liu, and G. Lan, “The key artificial intelligence technologies in early childhood education: a review,” Artificial Intelligence Review, vol. 57, no. 1, art. 12, 2024, doi: 10.1007/s10462-023-10637-7.

[16] P. Ramoneda, M. Suzuki, A. Maezawa, and X. Serra, “Difficulty-aware score generation for piano sight-reading,” Expert Systems with Applications, vol. 321, art. 132088, 2026, doi: 10.1016/j.eswa.2026.132088.

[17] N. J. Cepeda, H. Pashler, E. Vul, J. T. Wixted, and D. Rohrer, “Distributed practice in verbal recall tasks: A review and quantitative synthesis.,” Psychological Bulletin, vol. 132, no. 3, pp. 354-380, 2006, doi: 10.1037/0033-2909.132.3.354.

[18] A. T. Corbett and J. R. Anderson, “Knowledge tracing: Modeling the acquisition of procedural knowledge,” User Modelling and User-Adapted Interaction, vol. 4, no. 4, pp. 253-278, 1995, doi: 10.1007/BF01099821.

[19] E. B. Wilson, “Probable Inference, the Law of Succession, and Statistical Inference,” Journal of the American Statistical Association, vol. 22, no. 158, pp. 209-212, 1927, doi: 10.1080/01621459.1927.10502953.

[20] P. Woźniak and E. Gorzelańczyk, “Optimization of repetition spacing in the practice of learning,” Acta Neurobiologiae Experimentalis, vol. 54, no. 1, pp. 59-62, 1994, doi: 10.55782/ane-1994-1003.

[21] DANE, “Proyecciones de población municipal 2020–2035, actualización post COVID-19 (Montería, 2026),” Bogotá, Colombia. [Online]. Available: https://www.dane.gov.co/files/censo2018/proyecciones-de-poblacion/Municipal/DCD-area-sexo-edad-proypoblacion-Mun-2020-2035-ActPostCOVID-19.xlsx. Accessed: Nov. 5, 2026.

---
## Avisos

- La transcripción de tu preprint es **aproximada** (letra difícil de leer); compárala con tu original.
- La Tabla 2 del artículo es un **cálculo derivado de la fórmula** (suponiendo que la tolerancia no limita la ventana), no una medición. Dilo así.
- El valor de 6 fotogramas de suelta es el del código; la documentación decía 2.

## Guion de defensa

**¿Por qué la ventana de acierto es asimétrica?**  
Es más ancha antes de la línea (1,15·h) que después (0,85·h), para no penalizar al niño por el tiempo que el reconocimiento tarda en confirmar.

**¿Por qué una nota sonaba dos veces?**  
MediaPipe pierde la mano uno o dos fotogramas aunque esté quieta; con ventana de un fotograma eso se leía como suelta y la siguiente lectura repetía la nota. Se subió el umbral de suelta de 2 a 6 fotogramas.

**¿Qué pasa con los tempos rápidos?**  
Hasta unos 100 bpm la ventana depende del intervalo entre notas; desde ahí actúa el piso de 480 ms. A 120 bpm son 276 ms antes y 204 ms después de la línea.

**¿Qué mediste de verdad?**  
La latencia del descriptor y clasificador (0,89 ms por fotograma en promedio, sin cámara ni pantalla) y los falsos positivos (8,0 %). La Tabla 2 es cálculo.

**¿Qué falta?**  
Latencia de extremo a extremo, notas duplicadas y señas repetidas con niños reales, y ajustar constantes del puntaje con observación en el aula.
