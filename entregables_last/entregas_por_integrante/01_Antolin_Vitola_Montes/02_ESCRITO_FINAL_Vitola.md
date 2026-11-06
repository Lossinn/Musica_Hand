# ESCRITO FINAL — Antolin De Jesús Vitola Montes

**Tu hilo:** Acceso y valor pedagógico: las manos como instrumento. De la fonomimia de Curwen a una herramienta que corre sin internet en un computador con cámara; qué se sabe y qué falta para saber si ayuda a aprender.

**Preprint y artículo:** Tu preprint habla de Curwen, del acceso limitado a instrumentos en Córdoba, de comparar niños con Hand Sing Kids frente al método tradicional y de una prueba piloto. Tu artículo desarrolla exactamente eso: justificación pedagógica, tabla comparativa con la enseñanza tradicional, hipótesis de impacto y plan de validación.

---
## ESCRITO FINAL 1 — Preprint

**Sistema inteligente adaptativo para el aprendizaje de teoría musical infantil mediante visión computacional e inteligencia artificial**

**Introducción**

Desde la fononimia de John Curwen a mediados del siglo 19 agregó gestos de manos como un recurso para aumentar la facilidad del aprendizaje en las artes musicales. En la actualidad, campos de IA como la visión computacional logran una transformación en las estrategias para las experiencias interactivas en las cuales se integran el reconocimiento de los gestos y la retroalimentación.

En efecto, la educación musical en Colombia tiene muchos problemas a enfrentar relacionados con el escaso acceso a los instrumentos y la disponibilidad de recursos interactivos. En Córdoba, el proyecto enfrenta estas limitaciones usando el desarrollo de herramientas digitales accesibles.

De acuerdo a lo anterior, se propone la idea de mejorar la adaptación y retroalimentación en la enseñanza musical para los niños. Los métodos tradicionales dificultan a los niños la adaptación a los diferentes ejercicios de los diferentes ritmos de aprendizaje. El presente trabajo tiene como objetivo la aplicación y evaluación de Hand Sing Kids, un sistema el cual usa la visión computacional logrando reconocer 8 gestos musicales, optimizando la secuencia de ejercicios aplicando un modelo matemático.

**Metodología**

Se aborda la investigación desde un enfoque cuantitativo con alcance comparativo proyectado para la evaluación de una herramienta tecnológica como apoyo en el aprendizaje de la teoría musical en los niños. La propuesta contempla la comparación del desempeño de los niños que usen Hand Sing Kids y aquellos que usan el modelo tradicional.

Se proyecta trabajar con una muestra de niños de diferentes instituciones educativas de Córdoba, con una distribución de grupos con distintos participantes; la población se concentra en estudiantes con edad escolar.

El procedimiento pasa por siete etapas: video, exhibición de manos, clasificación de gestos musicales, validación, almacenamiento de las interacciones, actualización del perfil de aprendizaje y la adaptación de los ejercicios mediante un modelo de optimización matemático.

Se desarrolló el prototipo usando Python, OpenCV y MediaPipe Hands para el procesamiento visual; SQLite para almacenar registros; Streamlit para la interfaz del usuario. La implementación del prototipo deberá contemplar pruebas funcionales, la comprobación del reconocimiento gestual y la validación educativa.

**Resultados**

Se identifica la necesidad de la incorporación de herramientas interactivas digitales que logren facilitar el aprendizaje de la teoría musical frente a las limitaciones del acceso a instrumentos. Estas necesidades son la base de la creación de Hand Sing Kids.

Se establecen cuatro componentes principales: patrón de manos mediante visión computacional, respuesta audiovisual, registro del desempeño y selección adaptativa de datos.

La propuesta coincide de forma conceptual con Mallaloqui en la importancia de una enseñanza mixta entre la tecnología y el compromiso de los usuarios.

El aporte principal es la creación de una herramienta digital que ataca un problema real en el aprendizaje musical de los más pequeños mediante modelo matemático y equipos informáticos. La correcta aplicación del prototipo deberá ser comprobada mediante pruebas técnicas y una prueba piloto.

---
## ESCRITO FINAL 2 — Resumen y abstract

**Resumen.** Enseñar música exige instrumentos, espacios y docentes que no siempre están disponibles. Hand Sing Kids propone usar las manos, como lo hacía la fonomimia del siglo XIX, y una cámara que reconoce ocho señas para las notas de Do3 a Do4, de modo que el niño reciba una respuesta inmediata sin necesidad de un instrumento. Este trabajo presenta la propuesta desde su pertinencia pedagógica y su viabilidad técnica en Montería y Córdoba, donde el DANE proyecta para 2026 una población de 535.052 habitantes, 80.254 de ellos entre 3 y 12 años. La aplicación corre en un computador con cámara, guarda sus datos en una base local y no necesita conexión a internet. En laboratorio, con una calibración de una persona y perturbaciones simuladas, reconoció 480 de 480 señas sin ruido y evitó notas falsas en la mayoría de 640 posturas que no son seña (8,0 % de errores frente a 100 % del método inicial). No hubo pruebas con niños. Se formulan tres hipótesis de impacto y un plan para validarlas; el nivel de madurez es TRL 4.

**Abstract.** Teaching music requires instruments, spaces and teachers that are not always available. Hand Sing Kids proposes using the hands, as nineteenth-century hand-sign solfège did, and a camera that recognizes eight signs for the notes from C3 to C4, so that the child receives immediate feedback without an instrument. This paper presents the proposal from its pedagogical relevance and technical feasibility in Montería and Córdoba, where DANE projects a 2026 population of 535,052, of whom 80,254 are between 3 and 12 years old. The application runs on a computer with a camera, stores its data locally and needs no internet connection. In the laboratory, with a single-person calibration and simulated perturbations, it recognized 480 of 480 signs without noise and avoided false notes in most of 640 non-sign postures (8,0 % errors against 100 % for the initial method). No tests with children were done. Three impact hypotheses and a validation plan are stated; the readiness level is TRL 4.

---
## ESCRITO FINAL 3 — Texto del artículo

[Título art] Las manos como instrumento: una herramienta digital de bajo requerimiento para enseñar las notas musicales a niños en Montería y Córdoba

[Título art] Hands as an instrument: a low-requirement digital tool to teach musical notes to children in Montería and Córdoba

[Nombre autores] Antolin De Jesús Vitola-Montes^1}^*}, Isaías José Petro-Rodríguez^2}, Andrés Julián Negrete-Pacheco^3}, Juliana Esther Carrascal-Hernández^4}, Angel Quintana-Jiménez^5}, Alejandro Pemberty-Vergara^6}, Juan Diego Guerra-Gómez^7}, Cristian Javier Cano-Mogollón^8}

^1} Autor 1: Antolin De Jesús Vitola-Montes - Universidad Pontificia Bolivariana, Seccional Montería, Córdoba, Colombia. ORCID: pendiente. Correo electrónico: antolin.vitola@upb.edu.co

^2} Autor 2: Isaías José Petro-Rodríguez - Universidad Pontificia Bolivariana, Seccional Montería, Córdoba, Colombia. ORCID: pendiente. Correo electrónico: isaias.petro@upb.edu.co

^3} Autor 3: Andrés Julián Negrete-Pacheco - Universidad Pontificia Bolivariana, Seccional Montería, Córdoba, Colombia. ORCID: pendiente. Correo electrónico: andresj.negretep@upb.edu.co

^4} Autor 4: Juliana Esther Carrascal-Hernández - Universidad Pontificia Bolivariana, Seccional Montería, Córdoba, Colombia. ORCID: pendiente. Correo electrónico: juliana.carrascal@upb.edu.co

^5} Autor 5: Angel Quintana-Jiménez - Universidad Pontificia Bolivariana, Seccional Montería, Córdoba, Colombia. ORCID: pendiente. Correo electrónico: angel.quintana@upb.edu.co

^6} Autor 6: Alejandro Pemberty-Vergara - Universidad Pontificia Bolivariana, Seccional Montería, Córdoba, Colombia. ORCID: pendiente. Correo electrónico: alejandro.pemberty@upb.edu.co

^7} Autor 7: Juan Diego Guerra-Gómez - Universidad Pontificia Bolivariana, Seccional Montería, Córdoba, Colombia. ORCID: pendiente. Correo electrónico: juan.guerra@upb.edu.co

^8} Co-Autor / Co-Investigador: M.Sc. Cristian Javier Cano Mogollón. Filiación: Docente Titular, Facultad de Ingeniería Industrial. Grupo de Investigación en Simulación, Logística y Gestión de Operaciones (SILOGE), Hub Industrial Solution (HIS), Universidad Pontificia Bolivariana, Seccional Montería, Colombia. ORCID: pendiente. Correo electrónico: cristian.cano@upb.edu.co

^*} Autor de correspondencia: Antolin De Jesús Vitola-Montes (antolin.vitola@upb.edu.co).

**Resumen:

Enseñar música exige instrumentos, espacios y docentes que no siempre están disponibles. Hand Sing Kids propone usar las manos, como lo hacía la fonomimia del siglo XIX, y una cámara que reconoce ocho señas para las notas de Do3 a Do4, de modo que el niño reciba una respuesta inmediata sin necesidad de un instrumento. Este trabajo presenta la propuesta desde su pertinencia pedagógica y su viabilidad técnica en Montería y Córdoba, donde el DANE proyecta para 2026 una población de 535.052 habitantes, 80.254 de ellos entre 3 y 12 años. La aplicación corre en un computador con cámara, guarda sus datos en una base local y no necesita conexión a internet. En laboratorio, con una calibración de una persona y perturbaciones simuladas, reconoció 480 de 480 señas sin ruido y evitó notas falsas en la mayoría de 640 posturas que no son seña (8,0 % de errores frente a 100 % del método inicial). No hubo pruebas con niños. Se formulan tres hipótesis de impacto y un plan para validarlas; el nivel de madurez es TRL 4.

**Palabras clave:

educación musical infantil; fonomimia; acceso a instrumentos; aprendizaje con gestos; tecnología accesible; Montería; Córdoba

**Abstract:

Teaching music requires instruments, spaces and teachers that are not always available. Hand Sing Kids proposes using the hands, as nineteenth-century hand-sign solfège did, and a camera that recognizes eight signs for the notes from C3 to C4, so that the child receives immediate feedback without an instrument. This paper presents the proposal from its pedagogical relevance and technical feasibility in Montería and Córdoba, where DANE projects a 2026 population of 535,052, of whom 80,254 are between 3 and 12 years old. The application runs on a computer with a camera, stores its data locally and needs no internet connection. In the laboratory, with a single-person calibration and simulated perturbations, it recognized 480 of 480 signs without noise and avoided false notes in most of 640 non-sign postures (8,0 % errors against 100 % for the initial method). No tests with children were done. Three impact hypotheses and a validation plan are stated; the readiness level is TRL 4.

**Keywords:

children's music education; hand-sign solfège; access to instruments; gesture-based learning; accessible technology; Montería; Córdoba

# Introducción

## Una idea antigua, una oportunidad nueva

Desde mediados del siglo XIX, John Curwen popularizó en el Reino Unido un sistema de señas manuales para las notas de la escala, que más tarde se difundió en la enseñanza musical infantil. La idea es simple: cada nota tiene una posición de la mano, y el niño la ve, la hace y la canta. Su fortaleza pedagógica es que no necesita ningún instrumento, solo un cuerpo y alguien que corrija. Su debilidad es esa misma: sin un docente atento, la seña se hace de cualquier manera y nadie le dice al niño si acertó.

Hoy una cámara y un modelo de seguimiento de manos pueden cumplir el papel de quien corrige. La atención a la tecnología digital en la educación musical infantil es creciente, y las revisiones sobre inteligencia artificial en la primera infancia la describen como un campo en expansión [1], con trabajos sobre aplicaciones móviles y realidad aumentada en música [2]–[4]. En Colombia y en Córdoba, un primer obstáculo es práctico: pocos centros educativos tienen instrumentos suficientes, y una herramienta que dependa de internet o de equipos costosos tendría el mismo problema.

En Montería, las proyecciones municipales del DANE para 2026 indican 535.052 habitantes, de los cuales 80.254 tienen entre 3 y 12 años [5]. No se aporta aquí una estadística local sobre la educación musical: no la hay en las fuentes revisadas. La justificación del proyecto es de diseño. Hand Sing Kids se ejecuta en un computador con cámara, guarda sus datos en una base local y no necesita conexión, lo que lo hace una candidata razonable para probarse en aulas de la región. Que realmente ayude a aprender es una hipótesis que este trabajo no puede confirmar.

## Qué ofrece la propuesta frente a la enseñanza tradicional

*Tabla 1. Lo que aporta una herramienta basada en gestos frente a la enseñanza tradicional con señas

*Fuente: elaboración propia a partir del diseño del sistema; la columna final son hipótesis, no resultados.

## Objetivo

Presentar Hand Sing Kids desde su pertinencia pedagógica y su viabilidad técnica en laboratorio, y formular las hipótesis y el plan de validación que permitirían probar su utilidad con niños en Montería y Córdoba.

# Métodos

## Diseño del sistema

Cada nota de Do3 a Do4 se asocia a una seña de las dos manos. La cámara capta las manos y MediaPipe Hands entrega 21 puntos por mano [6]; un descriptor invariante al tamaño, la posición y el giro convierte esos puntos en un vector de 120 componentes, y un clasificador decide si hay una seña y cuál es. Después, un modelo de dominio estima qué sabe el niño de cada nota y un optimizador arma la siguiente sesión (Figura 1). Todo se guarda en una base SQLite local. El método de reconocimiento se detalla en otro trabajo del equipo; aquí interesa su comportamiento medido.

*Figura 1. Arquitectura funcional de Hand Sing Kids.

## Evaluación técnica

La evaluación fue de laboratorio. Se usó una calibración de las ocho señas de una persona, guardada como coordenadas sin imágenes, y perturbaciones simuladas de tamaño, giro y ruido. Se midió el reconocimiento de 480 señas válidas por nivel de ruido y las notas disparadas por error en 640 posturas que no son seña, con intervalos de Wilson al 95 % [7]. No se hicieron pruebas con niños.

# Resultados

## Lo que se midió

*Tabla 2. Evidencia técnica disponible, que no equivale a evidencia pedagógica

*Fuente: analisis/resultados_vision.json y salida de las pruebas del repositorio.

La Tabla 2 separa con claridad lo que se sabe de lo que no. El sistema funciona en laboratorio como se describe; si ayuda a aprender música es una pregunta abierta, porque ningún niño lo ha usado en una prueba formal.

## Madurez tecnológica e impacto esperado

Se propone **TRL 4**, validación de componentes en entorno de laboratorio. La evidencia a favor es que los componentes funcionan integrados en una aplicación ejecutable, con ocho baterías de prueba sin fallos y mediciones reproducibles con intervalos de confianza. La evidencia en contra de un nivel superior es que ningún componente se validó en el entorno de uso (aula, niños, iluminación y cámaras reales) ni con usuarios. El paso a TRL 5 exige un piloto con niños en aula; el protocolo está diseñado y no se ha ejecutado. El equipo debe confirmar el nivel final.

El impacto esperado en Montería y Córdoba se formula como tres hipótesis a validar: (H1) niños de 3 a 12 años aprenden a reproducir las ocho señas con calibración individual en una sesión corta; (H2) en aula, la tasa de notas disparadas por error con niños es comparable a la de laboratorio o menor al aumentar la ventana; y (H3) la aplicación funciona sin conexión a internet en computadores con cámara. Solo H3 es una propiedad de diseño (los datos se guardan en una base SQLite local); las otras dos requieren datos de campo.

# Discusión

**Un docente que no se cansa, no un reemplazo.** La propuesta no sustituye a un maestro de música: replica una función concreta, la de decirle al niño si la seña salió bien, y la ofrece en cualquier momento. Esto es coherente con la idea de que estas herramientas complementan la enseñanza tradicional y no la reemplazan, siempre que tengan objetivos pedagógicos claros. La evidencia internacional muestra el interés por estas tecnologías, pero todavía no hay estudios sobre este tipo de entrada, una seña por nota, en aulas de la región.

**El requisito más barato es el más importante.** Que no haga falta internet ni un instrumento es una decisión de diseño que se puede verificar, y es la que hace plausible llevar la herramienta a una escuela con recursos limitados. En cambio, otros requisitos todavía no se han medido: cuánta luz necesita la cámara, qué tan rápido responde de principio a fin y si un docente sin formación técnica puede calibrar la aplicación para cada niño. Son las primeras preguntas de un piloto.

**Qué haría falta para saber si funciona.** El plan mínimo es comparar, con grupos de niños de instituciones de Montería, el desempeño de quienes usan la herramienta con el de quienes aprenden con el método tradicional, midiendo antes y después el reconocimiento de las notas, y recoger la opinión del docente. Como se trabaja con menores, ese plan requiere aprobación ética, consentimiento de los acudientes y una revisión de la normativa colombiana sobre datos personales. Mientras eso no ocurra, los resultados de este trabajo son técnicos.

Los componentes de reconocimiento, estabilización, dominio y selección de sesión se apoyan en trabajos sobre aprendizaje personalizado, retroalimentación con IA, afecto y práctica distribuida [8]–[21].

# Conclusiones

Hand Sing Kids lleva una idea pedagógica antigua, enseñar las notas con las manos, a una herramienta que corre en un computador con cámara y sin internet. En laboratorio reconoce las señas de su calibración y evita casi todas las notas falsas. Su utilidad para el aprendizaje en Montería y Córdoba no está demostrada y depende de un piloto con niños, con docentes y con las autorizaciones éticas correspondientes.

# Recomendaciones

(1) Diseñar el piloto comparativo con una institución y un docente aliados. (2) Medir la latencia de extremo a extremo y las condiciones de iluminación necesarias. (3) Probar si un docente puede calibrar la herramienta sin apoyo técnico. (4) Obtener la aprobación ética y el consentimiento informado antes de cualquier recolección de datos de menores.

## Contribución de los autores

Contribución de los autores (CRediT, por confirmar): el primer autor formuló la justificación pedagógica y las hipótesis de impacto y redactó el borrador; los demás autores aportaron el desarrollo del software, las mediciones y la revisión; Cristian Javier Cano-Mogollón supervisó y revisó el manuscrito.

## Declaraciones finales

[Heading 3] Financiación

No se recibió financiación externa para este trabajo. [Por confirmar.]

[Heading 3] Conflicto de intereses

Los autores declaran no tener conflictos de intereses. [Por confirmar.]

[Heading 3] Consentimiento informado

No aplica; no se recolectaron datos de niños. La prueba piloto requerirá consentimiento informado de los acudientes.

[Heading 3] Declaración de la Junta de Revisión Institucional

No aplica para esta evaluación técnica de laboratorio; el piloto con menores requerirá aprobación de un comité de ética.

[Heading 3] Disponibilidad de datos, código y materiales de investigación

El código, la calibración de referencia (solo coordenadas, sin imágenes), las pruebas y los scripts de evaluación están en el repositorio del proyecto; las salidas numéricas están en la carpeta de análisis de la entrega.

[Heading 3] Uso de herramientas de inteligencia artificial

Se utilizó el asistente Claude (Anthropic) como apoyo en el análisis del código, la ejecución de las mediciones, la verificación de referencias y la redacción de borradores; los autores revisaron y asumen el contenido.

**Declarations (English)

Author Contributions: the first author formulated the pedagogical rationale and the impact hypotheses and drafted the manuscript; the other authors contributed software development, measurements and review; C. J. Cano-Mogollón supervised. No external funding. No conflicts of interest. Consent and IRB: not applicable to this laboratory evaluation; a pilot with minors will require both. Data and code: project repository.

# References

[1] H. Yi, T. Liu, and G. Lan, “The key artificial intelligence technologies in early childhood education: a review,” Artificial Intelligence Review, vol. 57, no. 1, art. 12, 2024, doi: 10.1007/s10462-023-10637-7.

[2] K. Apaydinli, “Content analysis of music education studies related to augmented reality technology,” Journal of Educational Technology and Online Learning, vol. 6, no. 2, pp. 447-481, 2023, doi: 10.31681/jetol.1243501.

[3] J. Barroso-Osuna, A. León-Garrido, C. Llorente-Cejudo, and J. Ruiz-Palmero, “El impacto de las apps móviles y la carga del trabajo en la Educación Musical universitaria: un estudio experimental,” Revista de Educación a Distancia (RED), vol. 24, no. 80, 2024, doi: 10.6018/red.602301.

[4] A. León-Garrido, J. M. Barroso-Osuna, and M. C. Llorente-Cejudo, “Diseño y validación de un instrumento de evaluación para apps móviles musicales a través del juicio de expertos,” Aula Abierta, vol. 53, no. 2, pp. 169-179, 2024, doi: 10.17811/rifie.20620.

[5] DANE, “Proyecciones de población municipal 2020–2035, actualización post COVID-19 (Montería, 2026),” Bogotá, Colombia. [Online]. Available: https://www.dane.gov.co/files/censo2018/proyecciones-de-poblacion/Municipal/DCD-area-sexo-edad-proypoblacion-Mun-2020-2035-ActPostCOVID-19.xlsx. Accessed: Nov. 5, 2026.

[6] F. Zhang et al., “MediaPipe Hands: On-device Real-time Hand Tracking,” arXiv:2006.10214, 2020, doi: 10.48550/arXiv.2006.10214.

[7] E. B. Wilson, “Probable Inference, the Law of Succession, and Statistical Inference,” Journal of the American Statistical Association, vol. 22, no. 158, pp. 209-212, 1927, doi: 10.1080/01621459.1927.10502953.

[8] N. Li and Z. Hong, “Deep Reinforcement Learning for Personalised Music Learning Pathways,” Annals of Data Science, vol. 13, no. 4, pp. 1013-1032, 2026, doi: 10.1007/s40745-026-00689-1.

[9] J. Li, “A reinforcement learning-based adaptive evaluation framework for personalized music education,” PeerJ Computer Science, vol. 12, art. e3464, 2026, doi: 10.7717/peerj-cs.3464.

[10] J. Li, “Deep learning-based personalized learning path planning and optimization model for music education,” Discover Artificial Intelligence, vol. 6, no. 1, art. 434, 2026, doi: 10.1007/s44163-026-01115-4.

[11] X. Deng, Y. Zhou, X. Guan, and Y. Wang, “An adaptive emotion aware music education system using machine learning for personalized emotional wellbeing enhancement,” Scientific Reports, vol. 16, no. 1, art. 25833, 2026, doi: 10.1038/s41598-026-53749-0.

[12] X. Shi, “An affective computing framework for preschool music education using MoE architecture and neural radiance fields,” Discover Artificial Intelligence, vol. 6, no. 1, art. 812, 2026, doi: 10.1007/s44163-026-01858-0.

[13] X. Deng, “AI-Based Feedback Systems in Piano Education: Effects on Technical Accuracy and Learner Autonomy,” Música Hodie, vol. 26, 2026, doi: 10.5216/mh.v26.85176.

[14] T. Chuluunsaikhan and S. H. Park, “Piano keyboard detection algorithm using deep learning,” Multimedia Tools and Applications, vol. 85, no. 5, art. 508, 2026, doi: 10.1007/s11042-026-21667-y.

[15] X. Tang, “The application of deep reinforcement learning in music teaching interaction,” Discover Computing, vol. 29, no. 1, art. 131, 2026, doi: 10.1007/s10791-026-10022-2.

[16] Z. Wang, “Music teaching evaluation using multimodal deep reinforcement learning,” Discover Artificial Intelligence, vol. 6, no. 1, art. 151, 2026, doi: 10.1007/s44163-026-00832-0.

[17] P. Ramoneda, M. Suzuki, A. Maezawa, and X. Serra, “Difficulty-aware score generation for piano sight-reading,” Expert Systems with Applications, vol. 321, art. 132088, 2026, doi: 10.1016/j.eswa.2026.132088.

[18] N. J. Cepeda, H. Pashler, E. Vul, J. T. Wixted, and D. Rohrer, “Distributed practice in verbal recall tasks: A review and quantitative synthesis.,” Psychological Bulletin, vol. 132, no. 3, pp. 354-380, 2006, doi: 10.1037/0033-2909.132.3.354.

[19] A. T. Corbett and J. R. Anderson, “Knowledge tracing: Modeling the acquisition of procedural knowledge,” User Modelling and User-Adapted Interaction, vol. 4, no. 4, pp. 253-278, 1995, doi: 10.1007/BF01099821.

[20] R. C. Wilson, A. Shenhav, M. Straccia, and J. D. Cohen, “The Eighty Five Percent Rule for optimal learning,” Nature Communications, vol. 10, no. 1, art. 4646, 2019, doi: 10.1038/s41467-019-12552-4.

[21] P. Woźniak and E. Gorzelańczyk, “Optimization of repetition spacing in the practice of learning,” Acta Neurobiologiae Experimentalis, vol. 54, no. 1, pp. 59-62, 1994, doi: 10.55782/ane-1994-1003.

---
## Avisos

- Tu preprint dice que la interfaz usa **Streamlit**; el código evaluado usa **PySide6** (el artículo dice PySide6). Aclara con el equipo cuál es la correcta antes de defender.
- En tu preprint citas a «Mallaloqui»: no está entre las referencias verificadas del artículo. Si la vas a mantener, agrégala con DOI verificado.
- La mención a John Curwen (fonomimia, siglo XIX) es un dato histórico general; el artículo no la respalda con una referencia verificada. Si el docente la pide, añade una fuente.

## Guion de defensa

**¿Qué aporta Hand Sing Kids frente a la enseñanza tradicional con señas?**  
La corrección inmediata y el registro de intentos sin depender de un docente atento, más el ajuste del ritmo por niño. Lo que no se ha demostrado es que mejore el aprendizaje: eso requiere un piloto.

**¿Por qué dices que sirve para Córdoba si no hay datos locales?**  
No lo afirmo: la justificación es de diseño (computador con cámara, base local, sin internet). La utilidad en la región es una hipótesis. Solo uso cifras del DANE como contexto (535.052 habitantes; 80.254 de 3 a 12 años).

**¿Qué evidencia técnica tienes?**  
480 señas por nivel de ruido: 100 % sin ruido y 86,0 % con ruido 0,09; 8,0 % de notas falsas en 640 posturas frente a 100 % del método inicial; 8 de 8 baterías de pruebas sin fallos. No hubo niños.

**¿Cuáles son tus hipótesis?**  
H1: niños de 3 a 12 años aprenden las ocho señas con calibración individual en una sesión corta. H2: en aula, las notas falsas son comparables a las de laboratorio. H3: la aplicación funciona sin internet (esta es propiedad de diseño).

**¿Cómo sería el piloto?**  
Grupos de instituciones de Montería, medición de conocimientos antes y después, comparación con el método tradicional, opinión del docente, aprobación ética y consentimiento de acudientes.
