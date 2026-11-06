# ESCRITO FINAL — Juliana Esther Carrascal Hernández

**Tu hilo:** Aprendizaje adaptativo: del intento al dominio y al repaso. Qué sabe el niño, cuándo repasar y qué constantes son diseño y no datos.

**Preprint y artículo:** Tu preprint resume el modelo (dominio de cuatro componentes, repaso espaciado, predictor) y tu artículo lo formaliza con ecuaciones, tabla de constantes y origen de cada una, y las hipótesis para un piloto.

---
## ESCRITO FINAL 1 — Preprint

**Qué practicar después: estimación del dominio y selección de sesiones en Hand Sing Kids**

Juliana Esther Carrascal Hernández. Universidad Pontificia Bolivariana, seccional Montería, Ingeniería Industrial. Gestión Tecnológica, tercer corte. 6 de noviembre de 2026.

**Resumen.** Hand Sing Kids enseña las ocho notas de Do3 a Do4 con señas de las manos. Este trabajo describe la parte que decide qué practica el niño después de cada intento. El sistema estima el dominio de cada nota con un modelo de cuatro componentes (precisión, consistencia, velocidad y retención), programa los repasos con un esquema de repetición espaciada y elige la sesión resolviendo un problema de programación entera mixta. Las pruebas del repositorio pasaron y el problema de ejemplo se resolvió en 40 ms con el óptimo exacto. No hay datos de niños, así que lo que se afirma sobre el aprendizaje es una hipótesis. Falta una prueba en el aula.

**Palabras clave:** aprendizaje adaptativo, repaso espaciado, seguimiento del conocimiento, programación entera mixta, educación musical infantil.

**Introducción**

*Internacional.* Los sistemas de tutoría estiman lo que sabe el estudiante a partir de sus intentos; el seguimiento del conocimiento es el ejemplo clásico (Corbett y Anderson, 1995). También se sabe que repartir la práctica en el tiempo mejora la retención frente a concentrarla (Cepeda et al., 2006). Pienso que ambas ideas son útiles para una aplicación infantil, siempre que se expliquen de forma sencilla.

*Nacional.* En Colombia, muchas aulas dependen del equipo disponible y de la preparación del docente. Por eso considero que una herramienta así debe funcionar en un computador común y mostrar al docente por qué propone cada actividad.

*Local.* Según las proyecciones municipales del DANE, Montería tiene 535.052 habitantes en 2026 y 80.254 de ellos tienen entre 3 y 12 años. No tengo una cifra local sobre educación musical; el valor de Hand Sing Kids en Córdoba es una hipótesis por probar.

*Problema y objetivo.* Una secuencia fija trata igual a todos los niños: repite lo que uno ya domina y adelanta lo que otro no ha aprendido. El objetivo es describir cómo Hand Sing Kids estima el dominio y elige la sesión, y verificar que lo haga de forma correcta.

**Métodos**

El dominio de cada nota combina cuatro componentes: precisión suavizada, consistencia en los últimos 8 intentos, velocidad frente a un tiempo de referencia y retención, que decae de forma exponencial con los días sin practicar. Una nota pasa a dominada con un valor de 0,80 y al menos seis intentos, y retrocede si baja de 0,70. Los repasos se programan con una adaptación del esquema SM-2. Cuando el niño acumula 40 intentos, un predictor logístico sustituye a la fórmula fija.

La sesión se elige con programación entera mixta: se maximizan la ganancia de aprendizaje, la urgencia de repaso y la motivación, y se resta la fatiga, con restricciones de tiempo, número de actividades, prerrequisitos, al menos una actividad lúdica y un máximo de dos por nota. Se resuelve con PuLP y, si no está disponible, por enumeración exhaustiva, que da el óptimo exacto. La dificultad se concentra en un éxito esperado de 0,75.

Verifiqué el código ejecutando las ocho baterías de pruebas del repositorio y comparando el resultado del optimizador con la enumeración exacta.

**Resultados**

No hay resultados medidos con niños. Lo verificado es técnico: las ocho baterías terminaron sin fallos, el optimizador coincidió con la enumeración exacta y la sesión de ejemplo se resolvió en 40 ms. La prueba del predictor muestra un 78 % de acierto sobre sus propios datos de entrenamiento; solo confirma que el ajuste converge y no mide capacidad de predicción. La hipótesis por validar es que una secuencia adaptada produce mejor retención que una fija.

**Discusión**

El valor está en combinar en una sola herramienta la lectura de la seña, la estimación del dominio y la decisión de la sesión, de modo que cada pieza se pueda explicar al docente. Las limitaciones son claras: las constantes del modelo vienen de decisiones de diseño y no de datos de niños, y el predictor no se ha probado fuera de su entrenamiento. Sugiero registrar los intentos en un piloto, ajustar las constantes con esos datos y comparar contra una secuencia fija.

**Conclusiones**

Considero que el enfoque adaptativo es correcto técnicamente y razonable pedagógicamente, pero su efecto sobre el aprendizaje no se ha medido. Su valor también está en que cada decisión se puede reproducir y explicar, no solo en un porcentaje de mejora.

**Referencias**

Cepeda, N. J., Pashler, H., Vul, E., Wixted, J. T., & Rohrer, D. (2006). Distributed practice in verbal recall tasks: A review and quantitative synthesis. *Psychological Bulletin, 132*(3), 354–380. https://doi.org/10.1037/0033-2909.132.3.354

Corbett, A. T., & Anderson, J. R. (1995). Knowledge tracing: Modeling the acquisition of procedural knowledge. *User Modeling and User-Adapted Interaction, 4*(4), 253–278. https://doi.org/10.1007/BF01099821

---
## ESCRITO FINAL 2 — Resumen y abstract

**Resumen.** Una secuencia fija de ejercicios trata igual a todos los niños: repite lo que uno ya domina y adelanta lo que otro aún no ha aprendido. Se describe el modelo de aprendizaje de Hand Sing Kids, una aplicación que enseña las ocho notas de Do3 a Do4 con señas de las manos. Después de cada intento, el sistema actualiza una estimación del dominio de la nota que combina cuatro componentes, precisión, consistencia, velocidad y retención, esta última con decaimiento exponencial por los días sin practicar; programa los repasos con una adaptación del esquema SM-2 a una calidad continua; y, cuando el niño acumula 40 intentos, sustituye la fórmula fija por un predictor logístico de tres variables. Una nota pasa a dominada con un valor de 0,80 y al menos seis intentos, y retrocede si cae por debajo de 0,70. Las baterías de prueba del dominio y del predictor del repositorio terminaron sin fallos; el predictor alcanza 78 % sobre sus propios datos de entrenamiento, lo que solo comprueba que el ajuste converge. No hay datos de niños: las constantes son decisiones de diseño y el efecto sobre el aprendizaje es una hipótesis por validar. El nivel de madurez es TRL 4.

**Abstract.** A fixed exercise sequence treats all children alike: it repeats what one child already masters and moves ahead on what another has not yet learned. The learning model of Hand Sing Kids, an application that teaches the eight notes from C3 to C4 with hand signs, is described. After each attempt the system updates a mastery estimate for the note that combines four components, accuracy, consistency, speed and retention, the latter decaying exponentially with days without practice; schedules reviews with an adaptation of the SM-2 scheme to a continuous quality; and, once the child has 40 attempts, replaces the fixed formula with a three-variable logistic predictor. A note becomes mastered at 0.80 with at least six attempts and falls back below 0.70. The mastery and predictor test suites of the repository ran without failures; the predictor reaches 78 % on its own training data, which only checks that the fit converges. There are no data from children: the constants are design decisions and the effect on learning is a hypothesis to be validated. The readiness level is TRL 4.

---
## ESCRITO FINAL 3 — Texto del artículo

[Título art] Del intento al dominio: estimación del aprendizaje y repaso espaciado en Hand Sing Kids para la enseñanza de las notas musicales a niños

[Título art] From attempt to mastery: learning estimation and spaced repetition in Hand Sing Kids for teaching musical notes to children

[Nombre autores] Juliana Esther Carrascal-Hernández^1}^*}, Antolin De Jesús Vitola-Montes^2}, Isaías José Petro-Rodríguez^3}, Andrés Julián Negrete-Pacheco^4}, Angel Quintana-Jiménez^5}, Alejandro Pemberty-Vergara^6}, Juan Diego Guerra-Gómez^7}, Cristian Javier Cano-Mogollón^8}

^1} Autor 1: Juliana Esther Carrascal-Hernández - Universidad Pontificia Bolivariana, Seccional Montería, Córdoba, Colombia. ORCID: pendiente. Correo electrónico: juliana.carrascal@upb.edu.co

^2} Autor 2: Antolin De Jesús Vitola-Montes - Universidad Pontificia Bolivariana, Seccional Montería, Córdoba, Colombia. ORCID: pendiente. Correo electrónico: antolin.vitola@upb.edu.co

^3} Autor 3: Isaías José Petro-Rodríguez - Universidad Pontificia Bolivariana, Seccional Montería, Córdoba, Colombia. ORCID: pendiente. Correo electrónico: isaias.petro@upb.edu.co

^4} Autor 4: Andrés Julián Negrete-Pacheco - Universidad Pontificia Bolivariana, Seccional Montería, Córdoba, Colombia. ORCID: pendiente. Correo electrónico: andresj.negretep@upb.edu.co

^5} Autor 5: Angel Quintana-Jiménez - Universidad Pontificia Bolivariana, Seccional Montería, Córdoba, Colombia. ORCID: pendiente. Correo electrónico: angel.quintana@upb.edu.co

^6} Autor 6: Alejandro Pemberty-Vergara - Universidad Pontificia Bolivariana, Seccional Montería, Córdoba, Colombia. ORCID: pendiente. Correo electrónico: alejandro.pemberty@upb.edu.co

^7} Autor 7: Juan Diego Guerra-Gómez - Universidad Pontificia Bolivariana, Seccional Montería, Córdoba, Colombia. ORCID: pendiente. Correo electrónico: juan.guerra@upb.edu.co

^8} Co-Autor / Co-Investigador: M.Sc. Cristian Javier Cano Mogollón. Filiación: Docente Titular, Facultad de Ingeniería Industrial. Grupo de Investigación en Simulación, Logística y Gestión de Operaciones (SILOGE), Hub Industrial Solution (HIS), Universidad Pontificia Bolivariana, Seccional Montería, Colombia. ORCID: pendiente. Correo electrónico: cristian.cano@upb.edu.co

^*} Autor de correspondencia: Juliana Esther Carrascal-Hernández (juliana.carrascal@upb.edu.co).

**Resumen:

Una secuencia fija de ejercicios trata igual a todos los niños: repite lo que uno ya domina y adelanta lo que otro aún no ha aprendido. Se describe el modelo de aprendizaje de Hand Sing Kids, una aplicación que enseña las ocho notas de Do3 a Do4 con señas de las manos. Después de cada intento, el sistema actualiza una estimación del dominio de la nota que combina cuatro componentes, precisión, consistencia, velocidad y retención, esta última con decaimiento exponencial por los días sin practicar; programa los repasos con una adaptación del esquema SM-2 a una calidad continua; y, cuando el niño acumula 40 intentos, sustituye la fórmula fija por un predictor logístico de tres variables. Una nota pasa a dominada con un valor de 0,80 y al menos seis intentos, y retrocede si cae por debajo de 0,70. Las baterías de prueba del dominio y del predictor del repositorio terminaron sin fallos; el predictor alcanza 78 % sobre sus propios datos de entrenamiento, lo que solo comprueba que el ajuste converge. No hay datos de niños: las constantes son decisiones de diseño y el efecto sobre el aprendizaje es una hipótesis por validar. El nivel de madurez es TRL 4.

**Palabras clave:

aprendizaje adaptativo; seguimiento del conocimiento; repaso espaciado; dominio de habilidades; predictor logístico; educación musical infantil; Montería

**Abstract:

A fixed exercise sequence treats all children alike: it repeats what one child already masters and moves ahead on what another has not yet learned. The learning model of Hand Sing Kids, an application that teaches the eight notes from C3 to C4 with hand signs, is described. After each attempt the system updates a mastery estimate for the note that combines four components, accuracy, consistency, speed and retention, the latter decaying exponentially with days without practice; schedules reviews with an adaptation of the SM-2 scheme to a continuous quality; and, once the child has 40 attempts, replaces the fixed formula with a three-variable logistic predictor. A note becomes mastered at 0.80 with at least six attempts and falls back below 0.70. The mastery and predictor test suites of the repository ran without failures; the predictor reaches 78 % on its own training data, which only checks that the fit converges. There are no data from children: the constants are design decisions and the effect on learning is a hypothesis to be validated. The readiness level is TRL 4.

**Keywords:

adaptive learning; knowledge tracing; spaced repetition; skill mastery; logistic predictor; children's music education; Montería

# Introducción

## Qué practicar después

Aprender las notas con las manos exige repetir, pero no cualquier repetición sirve. Un niño que ya domina el Do y el Re necesita avanzar hacia el Mi; otro que confunde el Fa con el Sol necesita volver sobre ellos. Una aplicación que ofrece siempre la misma secuencia ignora esa diferencia. Para adaptarse, el sistema tiene que responder tres preguntas después de cada intento: qué sabe el niño de cada nota, cuándo conviene volver a una nota ya aprendida y qué actividades armar para la siguiente sesión.

Estas preguntas tienen una larga historia en los sistemas de tutoría. El seguimiento del conocimiento estima el dominio de una habilidad como una variable oculta a partir de los aciertos y fallos observados [1]. En paralelo, la investigación sobre práctica distribuida muestra que espaciar los repasos mejora la retención frente a concentrarlos [2], y los algoritmos de repetición espaciada programan el siguiente repaso según la calidad de la respuesta anterior [3]. Una idea complementaria sostiene que el aprendizaje es más eficiente cuando la dificultad deja una tasa de error intermedia [4].

## Trabajos recientes en educación musical

En música, la personalización se ha abordado con aprendizaje por refuerzo y profundo para trazar rutas de estudio [5]–[9], con sistemas que consideran el estado afectivo del estudiante [10], [11] y con generación de partituras según su dificultad [12]. Hay además estudios de retroalimentación con IA en piano [13], [14], y revisiones sobre IA en la primera infancia [15] y sobre aplicaciones móviles musicales [16]–[18]. Entre los títulos revisados no apareció uno que combine un modelo de dominio por habilidad, repaso espaciado y una selección de sesión resuelta de forma exacta para una entrada por seña manual; no se leyeron los textos completos.

*Tabla 1. Idea de la literatura, adaptación en Hand Sing Kids y estado de validación

*Fuente: elaboración propia.

## Objetivo

Describir con precisión el modelo de aprendizaje de Hand Sing Kids, declarar qué se verificó y qué no, y dejar planteadas las hipótesis que un piloto con niños debería poner a prueba.

# Métodos

## Enfoque

El trabajo es un análisis de diseño y de verificación técnica sobre el código del sistema. La capa pedagógica recibe de la capa perceptiva una nota confirmada y el tiempo que el niño tardó en producirla, y devuelve la actualización del dominio y la siguiente sesión (Figura 1). No se usaron datos de niños.

*Figura 1. Arquitectura funcional de Hand Sing Kids; la capa pedagógica es la que se describe aquí.

## Dominio, repaso espaciado y predictor

El dominio de una habilidad s combina desempeño y retención. La retención multiplica, no suma, de modo que el desuso prolongado sí degrada una habilidad, mientras que lambda evita que se desplome a cero:

con w_p=0,55, w_c=0,25, w_v=0,20, lambda=0,65 y gamma=0,40. La precisión P_s se suaviza con una distribución a priori, la consistencia C_s penaliza alternar aciertos y fallos en los últimos K=8 intentos, la velocidad V_s se mide contra un tiempo de referencia por franja de edad, y la retención decae de forma exponencial:

Aquí h_s son los aciertos, n_s los intentos, Delta t los días desde la última práctica y M_s^-} el dominio de la actualización anterior, que evita una definición circular. El repaso espaciado adapta el esquema SM-2 [3] a una calidad continua qin[0,1] (el beneficio de la práctica distribuida está documentado en [2]):

Una habilidad pasa a dominada con M_sge 0,80 y al menos seis intentos, y retrocede si cae de 0,70. La idea de seguir el dominio como una variable estimada a partir de los intentos proviene del seguimiento del conocimiento [1]. Cuando el niño acumula 40 intentos propios, un predictor logístico de tres variables sustituye a la fórmula fija y se reentrena cada 20 intentos nuevos, con 300 épocas de descenso de gradiente y tasa 0,35 sobre variables estandarizadas:

donde mathrm{precision} es la precisión suavizada de la nota, mathrm{dificultad} la de la actividad y mathrm{dias} los días desde la última práctica. Los pesos minimizan la entropía cruzada por descenso de gradiente:

# Resultados

## Qué se verificó

Las baterías de prueba del dominio y del predictor, dos de las ocho del repositorio, terminaron sin fallos. La prueba unitaria del predictor mejora a la predicción al azar sobre sus propios datos de entrenamiento, con 78 % de acierto. Esa cifra solo comprueba que el descenso de gradiente converge; no mide capacidad predictiva, porque no hay datos de niños con los que probarlo. Del mismo modo, las pruebas del dominio verifican que la fórmula se comporte como se espera, por ejemplo, que el desuso prolongado degrade la retención sin llevarla a cero, y no que esa fórmula refleje cómo aprende un niño.

*Tabla 2. Constantes del modelo de aprendizaje y su origen

*Fuente: código del repositorio.

La Tabla 2 muestra el límite central del trabajo: ninguna de las constantes proviene de datos de niños. El modelo es defendible como diseño, pero cualquier afirmación de que acierta al estimar lo que sabe un niño sería prematura.

# Discusión

**Por qué el dominio multiplica la retención.** Si la retención sumara al desempeño, un niño que practicó muy bien hace semanas aparecería con un dominio alto aunque hubiera olvidado la seña. Al multiplicarla, el desuso degrada el dominio. El piso de 0,65 evita que una pausa larga lo lleve a cero, lo que sería injusto con un niño que sí aprendió. Es una decisión de diseño razonable, pero deberá contrastarse con curvas de olvido reales.

**Del conocimiento experto a los datos.** El modelo parte de una fórmula fija porque al comenzar no hay datos. Cuando el niño acumula 40 intentos, el predictor logístico aprende con ellos. Ese cambio es una idea útil: permite que el sistema empiece con reglas explicables y se personalice con el uso. Pero también exige cuidado: con pocos intentos el predictor puede sobreajustarse, y el docente debería poder ver cuál de los dos modelos está decidiendo.

**Hipótesis para un piloto.** (H1) Una secuencia adaptada produce mejor retención a una semana que una secuencia fija. (H2) El predictor logístico mejora al estimador fijo después de 40 intentos. (H3) Los repasos programados por el sistema coinciden con las notas que el niño efectivamente olvida. Para probarlas hacen falta niños, un docente y registros de intentos con fechas; la aplicación ya los guarda en una base local.

Para el reconocimiento de las señas, la estabilización y la selección de la sesión por optimización, véanse los trabajos sobre seguimiento de manos, aprendizaje por refuerzo y evaluación de aplicaciones musicales [19]–[21].

# Conclusiones

Hand Sing Kids estima el dominio de cada nota con cuatro componentes, programa repasos con repetición espaciada y reemplaza la fórmula fija por un predictor desde los 40 intentos. El código y las pruebas verifican que el modelo se comporta como se diseñó. No hay datos de niños y las constantes son de diseño, de modo que el efecto sobre el aprendizaje es una hipótesis. El nivel de madurez es TRL 4.

# Recomendaciones

(1) Registrar los intentos en un piloto y reajustar las constantes con ellos. (2) Comparar una secuencia adaptada con una fija en retención a una semana. (3) Mostrar al docente qué modelo decide y por qué. (4) Medir el sobreajuste del predictor con datos nuevos y no con los de entrenamiento.

## Contribución de los autores

Contribución de los autores (CRediT, por confirmar): la primera autora analizó y formalizó el modelo de aprendizaje, revisó las pruebas y redactó el borrador; los demás autores participaron en el desarrollo del software, las mediciones y la revisión; Cristian Javier Cano-Mogollón supervisó y revisó.

## Declaraciones finales

[Heading 3] Financiación

No hubo financiación externa para este trabajo. [Por confirmar por el equipo.]

[Heading 3] Conflicto de intereses

Los autores no declaran conflictos de intereses. [Por confirmar.]

[Heading 3] Consentimiento informado

No aplica; el estudio no incluyó datos de personas.

[Heading 3] Declaración de la Junta de Revisión Institucional

No aplica en este análisis técnico; el piloto con niños se someterá a un comité de ética y a consentimiento informado.

[Heading 3] Disponibilidad de datos, código y materiales de investigación

El código del modelo de dominio, del repaso y del predictor y sus pruebas están en el repositorio del proyecto. Las salidas de las pruebas y la verificación de referencias están en la carpeta de análisis de la entrega.

[Heading 3] Uso de herramientas de inteligencia artificial

Un asistente de inteligencia artificial (Claude, de Anthropic) apoyó la lectura del código, la ejecución de las pruebas, la verificación de las referencias y la redacción de borradores. Las autoras y los autores revisaron el contenido y responden por él.

**Declarations (English)

Author Contributions: the first author analysed and formalized the learning model, reviewed the tests and drafted the manuscript; the other authors contributed software, measurements and review; C. J. Cano-Mogollón supervised. No external funding. No conflicts of interest. Consent and IRB: not applicable to this technical analysis. Data and code: project repository.

# References

[1] A. T. Corbett and J. R. Anderson, “Knowledge tracing: Modeling the acquisition of procedural knowledge,” User Modelling and User-Adapted Interaction, vol. 4, no. 4, pp. 253-278, 1995, doi: 10.1007/BF01099821.

[2] N. J. Cepeda, H. Pashler, E. Vul, J. T. Wixted, and D. Rohrer, “Distributed practice in verbal recall tasks: A review and quantitative synthesis.,” Psychological Bulletin, vol. 132, no. 3, pp. 354-380, 2006, doi: 10.1037/0033-2909.132.3.354.

[3] P. Woźniak and E. Gorzelańczyk, “Optimization of repetition spacing in the practice of learning,” Acta Neurobiologiae Experimentalis, vol. 54, no. 1, pp. 59-62, 1994, doi: 10.55782/ane-1994-1003.

[4] R. C. Wilson, A. Shenhav, M. Straccia, and J. D. Cohen, “The Eighty Five Percent Rule for optimal learning,” Nature Communications, vol. 10, no. 1, art. 4646, 2019, doi: 10.1038/s41467-019-12552-4.

[5] N. Li and Z. Hong, “Deep Reinforcement Learning for Personalised Music Learning Pathways,” Annals of Data Science, vol. 13, no. 4, pp. 1013-1032, 2026, doi: 10.1007/s40745-026-00689-1.

[6] J. Li, “A reinforcement learning-based adaptive evaluation framework for personalized music education,” PeerJ Computer Science, vol. 12, art. e3464, 2026, doi: 10.7717/peerj-cs.3464.

[7] J. Li, “Deep learning-based personalized learning path planning and optimization model for music education,” Discover Artificial Intelligence, vol. 6, no. 1, art. 434, 2026, doi: 10.1007/s44163-026-01115-4.

[8] X. Tang, “The application of deep reinforcement learning in music teaching interaction,” Discover Computing, vol. 29, no. 1, art. 131, 2026, doi: 10.1007/s10791-026-10022-2.

[9] Z. Wang, “Music teaching evaluation using multimodal deep reinforcement learning,” Discover Artificial Intelligence, vol. 6, no. 1, art. 151, 2026, doi: 10.1007/s44163-026-00832-0.

[10] X. Deng, Y. Zhou, X. Guan, and Y. Wang, “An adaptive emotion aware music education system using machine learning for personalized emotional wellbeing enhancement,” Scientific Reports, vol. 16, no. 1, art. 25833, 2026, doi: 10.1038/s41598-026-53749-0.

[11] X. Shi, “An affective computing framework for preschool music education using MoE architecture and neural radiance fields,” Discover Artificial Intelligence, vol. 6, no. 1, art. 812, 2026, doi: 10.1007/s44163-026-01858-0.

[12] P. Ramoneda, M. Suzuki, A. Maezawa, and X. Serra, “Difficulty-aware score generation for piano sight-reading,” Expert Systems with Applications, vol. 321, art. 132088, 2026, doi: 10.1016/j.eswa.2026.132088.

[13] X. Deng, “AI-Based Feedback Systems in Piano Education: Effects on Technical Accuracy and Learner Autonomy,” Música Hodie, vol. 26, 2026, doi: 10.5216/mh.v26.85176.

[14] T. Chuluunsaikhan and S. H. Park, “Piano keyboard detection algorithm using deep learning,” Multimedia Tools and Applications, vol. 85, no. 5, art. 508, 2026, doi: 10.1007/s11042-026-21667-y.

[15] H. Yi, T. Liu, and G. Lan, “The key artificial intelligence technologies in early childhood education: a review,” Artificial Intelligence Review, vol. 57, no. 1, art. 12, 2024, doi: 10.1007/s10462-023-10637-7.

[16] K. Apaydinli, “Content analysis of music education studies related to augmented reality technology,” Journal of Educational Technology and Online Learning, vol. 6, no. 2, pp. 447-481, 2023, doi: 10.31681/jetol.1243501.

[17] J. Barroso-Osuna, A. León-Garrido, C. Llorente-Cejudo, and J. Ruiz-Palmero, “El impacto de las apps móviles y la carga del trabajo en la Educación Musical universitaria: un estudio experimental,” Revista de Educación a Distancia (RED), vol. 24, no. 80, 2024, doi: 10.6018/red.602301.

[18] A. León-Garrido, J. M. Barroso-Osuna, and M. C. Llorente-Cejudo, “Diseño y validación de un instrumento de evaluación para apps móviles musicales a través del juicio de expertos,” Aula Abierta, vol. 53, no. 2, pp. 169-179, 2024, doi: 10.17811/rifie.20620.

[19] F. Zhang et al., “MediaPipe Hands: On-device Real-time Hand Tracking,” arXiv:2006.10214, 2020, doi: 10.48550/arXiv.2006.10214.

[20] E. B. Wilson, “Probable Inference, the Law of Succession, and Statistical Inference,” Journal of the American Statistical Association, vol. 22, no. 158, pp. 209-212, 1927, doi: 10.1080/01621459.1927.10502953.

[21] DANE, “Proyecciones de población municipal 2020–2035, actualización post COVID-19 (Montería, 2026),” Bogotá, Colombia. [Online]. Available: https://www.dane.gov.co/files/censo2018/proyecciones-de-poblacion/Municipal/DCD-area-sexo-edad-proypoblacion-Mun-2020-2035-ActPostCOVID-19.xlsx. Accessed: Nov. 5, 2026.

---
## Avisos

- El **78 %** del predictor es sobre sus propios datos de entrenamiento: solo prueba que converge.
- Ninguna constante viene de datos de niños: la Tabla 2 lo muestra de forma explícita.

## Guion de defensa

**¿Por qué el dominio multiplica la retención?**  
Para que el desuso degrade el dominio; el piso de 0,65 evita que una pausa larga lo lleve a cero.

**¿Cuándo una nota está dominada?**  
Con dominio ≥ 0,80 y al menos seis intentos; retrocede si baja de 0,70.

**¿Qué hace el predictor y desde cuándo?**  
Logística de tres variables (precisión, dificultad, días) que sustituye a la fórmula fija desde 40 intentos y se reentrena cada 20.

**¿Cómo sabes que funciona?**  
No lo sé con niños. Verifiqué que las pruebas del dominio y del predictor pasan y que el ajuste converge; el efecto en el aprendizaje es hipótesis (H1–H3).

**¿Qué referencias respaldan la idea?**  
Knowledge tracing (Corbett y Anderson, 1995), práctica distribuida (Cepeda et al., 2006), SM-2 (Woźniak y Gorzelańczyk, 1994) y la regla del 85 % (Wilson et al., 2019).
