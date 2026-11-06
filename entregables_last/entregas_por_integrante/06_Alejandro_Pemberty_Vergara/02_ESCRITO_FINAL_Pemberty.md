# ESCRITO FINAL — Alejandro Pemberty Vergara

**Tu hilo:** Ingeniería reproducible y despliegue responsable: del prototipo al aula, con la lista de condiciones técnicas y éticas antes de probar con niños.

**Preprint y artículo:** Tu preprint explica que la herramienta corre en un computador común y qué falta para llevarla a un aula. Tu artículo lo documenta: estado de ingeniería, reproducibilidad, tabla de condiciones, datos de menores y orden del piloto.

---
## ESCRITO FINAL 1 — Preprint

**Hand Sing Kids en el aula de Montería: una herramienta que corre en un computador común y qué falta para probarla con niños**

Alejandro Pemberty Vergara. Universidad Pontificia Bolivariana, seccional Montería, Ingeniería Industrial. Gestión Tecnológica, tercer corte. 6 de noviembre de 2026.

Hand Sing Kids es una aplicación de escritorio que enseña a los niños las ocho notas musicales de Do3 a Do4 con señas de las dos manos. Una cámara capta las manos, el sistema reconoce la seña y responde con sonido, y después decide qué actividad sigue según lo que el niño ya domina. Lo que me interesa destacar es que todo esto funciona en un computador con cámara y guarda sus datos en una base local, sin depender de una conexión a internet. Por eso creo que es una candidata realista para probarse en aulas de Montería y Córdoba, donde no siempre hay buena conectividad.

El prototipo está hecho en Python, con una interfaz en PySide6 y el seguimiento de las manos con MediaPipe. Tiene 62 módulos y unas 10.500 líneas de código, organizados en ocho baterías de pruebas, y un catálogo de 19 canciones sencillas. Las revisiones recientes de inteligencia artificial en la educación de la primera infancia muestran que el interés por estas tecnologías es grande (Yi et al., 2024), pero entre los trabajos que encontré, ninguno combina una seña manual por nota, una calibración para cada niño y una decisión de sesión resuelta de forma exacta. Esa combinación es el espacio de esta propuesta.

La evaluación hasta ahora es técnica y de laboratorio. Con una calibración de una sola persona y perturbaciones simuladas, el reconocimiento llegó a 100 % sin ruido y a 86,0 % con ruido alto. Ante 640 posturas que no son seña, disparó una nota por error en el 8,0 % de los casos, frente al 100 % del método de la versión inicial. Las ocho baterías de pruebas del repositorio terminaron sin fallos y los scripts para repetir las mediciones se pueden ejecutar con una sola orden. No se hicieron pruebas con niños, así que no puedo afirmar nada sobre el aprendizaje; el nivel de madurez tecnológica es TRL 4.

Antes de entrar a un aula hay tareas pendientes que considero tan importantes como el código. Hay que medir la latencia de extremo a extremo, incluyendo la cámara; conseguir la aprobación ética y el consentimiento de los acudientes, porque se trabaja con menores; revisar la normativa colombiana sobre tratamiento de datos personales, y decidir qué se guarda de cada niño. Propongo un piloto pequeño con un docente, medir los conocimientos antes y después, registrar las notas disparadas por error con niños reales en lugar de simularlas y recoger la opinión del docente. El valor del proyecto no depende de una cifra de precisión, sino de que sea fácil de usar, honesto sobre lo que ya probó y repetible por otros.

**Referencia verificada**

Yi, H., Liu, T., & Lan, G. (2024). The key artificial intelligence technologies in early childhood education: A review. *Artificial Intelligence Review, 57*(1), Article 12. https://doi.org/10.1007/s10462-023-10637-7

---
## ESCRITO FINAL 2 — Resumen y abstract

**Resumen.** Un prototipo educativo que funciona en el computador de sus desarrolladores no está listo para un aula. Se documenta el estado de ingeniería de Hand Sing Kids, una aplicación de escritorio en Python que enseña las ocho notas de Do3 a Do4 con señas de las manos, y se definen las condiciones para llevarla a una prueba con niños en Montería. El repositorio evaluado tiene 62 módulos y 10.581 líneas, con ocho baterías de prueba que terminaron sin fallos, y las mediciones del reconocedor se pueden repetir con un solo comando y con semillas fijas. En laboratorio, el reconocimiento fue de 100 % sin ruido y de 86,0 % con ruido de 0,09, y el método disparó una nota por error en 8,0 % de 640 posturas que no son seña. Los datos se guardan en una base local y la aplicación no necesita internet. Para pasar al aula faltan, en orden, la aprobación ética y el consentimiento de los acudientes, el tratamiento de datos de menores conforme a la normativa colombiana, la medición de la latencia de extremo a extremo y un protocolo de piloto con medición antes y después. El nivel de madurez es TRL 4; el paso a TRL 5 exige ese piloto.

**Abstract.** An educational prototype that works on its developers' computer is not ready for a classroom. The engineering status of Hand Sing Kids, a desktop application in Python that teaches the eight notes from C3 to C4 with hand signs, is documented, and the conditions for taking it to a test with children in Montería are defined. The evaluated repository has 62 modules and 10,581 lines, with eight test suites that ran without failures, and the recognizer measurements can be repeated with a single command and fixed seeds. In the laboratory, recognition was 100 % without noise and 86,0 % at noise 0.09, and the method fired a wrong note in 8,0 % of 640 non-sign postures. Data are stored locally and the application needs no internet. Before moving to the classroom, the following are missing, in order: ethical approval and guardians' consent, handling of minors' data under Colombian regulation, end-to-end latency measurement and a pilot protocol with before-and-after measurement. The readiness level is TRL 4; reaching TRL 5 requires that pilot.

---
## ESCRITO FINAL 3 — Texto del artículo

[Título art] De un prototipo a un aula: ingeniería reproducible y condiciones de despliegue responsable de Hand Sing Kids en Montería

[Título art] From a prototype to a classroom: reproducible engineering and responsible deployment conditions for Hand Sing Kids in Montería

[Nombre autores] Alejandro Pemberty-Vergara^1}^*}, Antolin De Jesús Vitola-Montes^2}, Isaías José Petro-Rodríguez^3}, Andrés Julián Negrete-Pacheco^4}, Juliana Esther Carrascal-Hernández^5}, Angel Quintana-Jiménez^6}, Juan Diego Guerra-Gómez^7}, Cristian Javier Cano-Mogollón^8}

^1} Autor 1: Alejandro Pemberty-Vergara - Universidad Pontificia Bolivariana, Seccional Montería, Córdoba, Colombia. ORCID: pendiente. Correo electrónico: alejandro.pemberty@upb.edu.co

^2} Autor 2: Antolin De Jesús Vitola-Montes - Universidad Pontificia Bolivariana, Seccional Montería, Córdoba, Colombia. ORCID: pendiente. Correo electrónico: antolin.vitola@upb.edu.co

^3} Autor 3: Isaías José Petro-Rodríguez - Universidad Pontificia Bolivariana, Seccional Montería, Córdoba, Colombia. ORCID: pendiente. Correo electrónico: isaias.petro@upb.edu.co

^4} Autor 4: Andrés Julián Negrete-Pacheco - Universidad Pontificia Bolivariana, Seccional Montería, Córdoba, Colombia. ORCID: pendiente. Correo electrónico: andresj.negretep@upb.edu.co

^5} Autor 5: Juliana Esther Carrascal-Hernández - Universidad Pontificia Bolivariana, Seccional Montería, Córdoba, Colombia. ORCID: pendiente. Correo electrónico: juliana.carrascal@upb.edu.co

^6} Autor 6: Angel Quintana-Jiménez - Universidad Pontificia Bolivariana, Seccional Montería, Córdoba, Colombia. ORCID: pendiente. Correo electrónico: angel.quintana@upb.edu.co

^7} Autor 7: Juan Diego Guerra-Gómez - Universidad Pontificia Bolivariana, Seccional Montería, Córdoba, Colombia. ORCID: pendiente. Correo electrónico: juan.guerra@upb.edu.co

^8} Co-Autor / Co-Investigador: M.Sc. Cristian Javier Cano Mogollón. Filiación: Docente Titular, Facultad de Ingeniería Industrial. Grupo de Investigación en Simulación, Logística y Gestión de Operaciones (SILOGE), Hub Industrial Solution (HIS), Universidad Pontificia Bolivariana, Seccional Montería, Colombia. ORCID: pendiente. Correo electrónico: cristian.cano@upb.edu.co

^*} Autor de correspondencia: Alejandro Pemberty-Vergara (alejandro.pemberty@upb.edu.co).

**Resumen:

Un prototipo educativo que funciona en el computador de sus desarrolladores no está listo para un aula. Se documenta el estado de ingeniería de Hand Sing Kids, una aplicación de escritorio en Python que enseña las ocho notas de Do3 a Do4 con señas de las manos, y se definen las condiciones para llevarla a una prueba con niños en Montería. El repositorio evaluado tiene 62 módulos y 10.581 líneas, con ocho baterías de prueba que terminaron sin fallos, y las mediciones del reconocedor se pueden repetir con un solo comando y con semillas fijas. En laboratorio, el reconocimiento fue de 100 % sin ruido y de 86,0 % con ruido de 0,09, y el método disparó una nota por error en 8,0 % de 640 posturas que no son seña. Los datos se guardan en una base local y la aplicación no necesita internet. Para pasar al aula faltan, en orden, la aprobación ética y el consentimiento de los acudientes, el tratamiento de datos de menores conforme a la normativa colombiana, la medición de la latencia de extremo a extremo y un protocolo de piloto con medición antes y después. El nivel de madurez es TRL 4; el paso a TRL 5 exige ese piloto.

**Palabras clave:

reproducibilidad; ingeniería de software; despliegue responsable; datos de menores; madurez tecnológica; educación musical infantil; Montería

**Abstract:

An educational prototype that works on its developers' computer is not ready for a classroom. The engineering status of Hand Sing Kids, a desktop application in Python that teaches the eight notes from C3 to C4 with hand signs, is documented, and the conditions for taking it to a test with children in Montería are defined. The evaluated repository has 62 modules and 10,581 lines, with eight test suites that ran without failures, and the recognizer measurements can be repeated with a single command and fixed seeds. In the laboratory, recognition was 100 % without noise and 86,0 % at noise 0.09, and the method fired a wrong note in 8,0 % of 640 non-sign postures. Data are stored locally and the application needs no internet. Before moving to the classroom, the following are missing, in order: ethical approval and guardians' consent, handling of minors' data under Colombian regulation, end-to-end latency measurement and a pilot protocol with before-and-after measurement. The readiness level is TRL 4; reaching TRL 5 requires that pilot.

**Keywords:

reproducibility; software engineering; responsible deployment; minors' data; technology readiness; children's music education; Montería

# Introducción

## El trecho entre «funciona» y «se puede usar»

Un prototipo educativo suele demostrarse con su autor al lado: él sabe cómo iluminar la escena, qué cámara usar y cuándo reiniciar el programa. Un aula no tiene esa persona. Entre la demostración y el uso hay un trecho de ingeniería que rara vez se documenta: instalación, pruebas, medición reproducible, manejo de datos y condiciones éticas. Este trabajo describe ese trecho para Hand Sing Kids, una aplicación de escritorio que enseña las ocho notas de la escala con señas de las dos manos, con una cámara y seguimiento de manos [1].

La literatura sobre IA en educación musical presenta sobre todo resultados de modelos: trayectorias personalizadas [2]–[6], sistemas con emoción [7], [8], retroalimentación en piano [9], [10], partituras según dificultad [11], revisiones [12] y análisis de aplicaciones [13]–[15]. En los títulos revisados no aparece el detalle del despliegue en un aula concreta; no se leyeron los textos completos, por lo que esa ausencia debe tomarse con cautela.

En Montería, las proyecciones municipales del DANE para 2026 indican 535.052 habitantes, con 80.254 entre 3 y 12 años [16]. No se aporta una estadística local de educación musical; la razón para llevar la herramienta a un aula de la región es de diseño: funciona sin internet, en un computador con cámara.

*Tabla 1. Lista de condiciones antes de una prueba con niños

*Fuente: elaboración propia.

## Objetivo

Documentar el estado de ingeniería de Hand Sing Kids, demostrar que sus mediciones son repetibles y definir las condiciones técnicas y éticas para una prueba piloto con niños.

# Métodos

## Sistema y entorno de evaluación

Hand Sing Kids es una aplicación de escritorio en Python con interfaz en PySide6. El repositorio evaluado contiene 62 módulos con 10.581 líneas (8.613 de código efectivo, sin líneas en blanco ni comentarios) y 9 archivos de pruebas con 1.746 líneas, organizados en ocho baterías. Las mediciones se hicieron en Windows 11, con Python 3.12.10, NumPy 1.26.4, OpenCV 4.11.0, MediaPipe 0.10.21, PySide6 6.11.2 y PuLP 2.9.0. La documentación del proyecto declara como objetivo macOS y Python 3.10 a 3.12; esa plataforma no se usó en esta evaluación. La arquitectura se muestra en la Figura 1.

*Figura 1. Arquitectura funcional de Hand Sing Kids.

## Reproducibilidad

Las mediciones del reconocedor están en scripts que se ejecutan con una sola orden, con semillas fijas, y que escriben sus resultados en un archivo estructurado del que el artículo lee sus cifras. La verificación de las referencias se hizo contra Crossref y DataCite, con fecha de consulta, y no a mano. Cualquier cifra del texto se puede rastrear hasta el script que la produce.

# Resultados

## Verificación del repositorio

Las ocho baterías (audio, integración, dominio, optimizador, predictor, canciones, estabilizador y visión) terminaron con código de salida 0. En el optimizador, la prueba que compara el MILP con la enumeración exacta pasó, y la sesión de ejemplo se resolvió con CBC en 40 ms con valor objetivo 2,9524. El predictor, en su prueba unitaria, mejora al azar sobre sus propios datos de entrenamiento (78 %); esa cifra es una verificación de que el ajuste converge y no una medida de capacidad predictiva, porque no hay datos de niños. La primera ejecución de las baterías, en la consola con la codificación predeterminada de Windows, produjo dos errores de impresión de caracteres especiales y no de lógica; con la salida en UTF-8 las ocho pasaron.

## Desempeño en laboratorio

El reconocimiento de señas válidas fue de 100 % sin ruido y de 86,0 % con ruido de 0,09, sobre 480 señas por nivel. Ante 640 posturas que no son seña, el método disparó una nota por error en 8,0 % de los casos (IC 95 %: 6,1 a 10,3 %). La calibración es de una sola persona y el ruido es simulado; estos números describen el reconocedor en laboratorio, no en un aula.

# Discusión

**Lo que la repetibilidad permite.** Que cada cifra salga de un script permite que otra persona del equipo, o un revisor, repita la medición y compruebe el resultado. También permitió encontrar diferencias entre la documentación del proyecto y el código: el número de fotogramas de la suelta, el tamaño del repositorio y el desglose del error entre transiciones y manos cruzadas. En todos los casos prevalece el código, y las diferencias quedan registradas.

**Datos de menores.** La aplicación guarda los intentos de cada niño en una base local. Eso evita enviar datos a un servicio externo, pero no resuelve el problema de qué se guarda y por cuánto tiempo. La Ley 1581 de 2012 de Colombia regula el tratamiento de datos personales; el equipo debe revisarla con un asesor jurídico antes del piloto y decidir qué es indispensable guardar, con identificadores que no revelen la identidad del niño. La calibración de referencia del estudio contiene solo coordenadas de puntos de la mano, sin imágenes, precisamente para que no haya fotografías de personas.

**Orden del piloto.** (1) Aprobación del comité de ética y autorización de la institución. (2) Consentimiento de los acudientes y asentimiento de los niños. (3) Medición de latencia y de iluminación en el aula con el equipo real. (4) Medición inicial de conocimientos de notas, sesiones con la herramienta y medición final, con un grupo que aprenda por el método tradicional como comparación. (5) Registro de las notas falsas y de las señas repetidas con niños reales. (6) Opinión del docente. Con ese diseño se podría pasar de TRL 4 a TRL 5, y solo entonces hablar de efecto sobre el aprendizaje.

**Límites.** Esta lista de condiciones es una propuesta del equipo, no un protocolo aprobado; la plataforma objetivo documentada incluye macOS, que no se evaluó; y la validez de las mediciones depende de una calibración de una persona y de perturbaciones simuladas.

Los componentes de aprendizaje adaptativo del sistema, como el seguimiento del dominio y el repaso espaciado, se fundamentan en trabajos sobre práctica distribuida, seguimiento del conocimiento y estimación estadística [17]–[21].

# Conclusiones

Hand Sing Kids tiene un estado de ingeniería verificable: ocho baterías de prueba sin fallos y mediciones repetibles con una sola orden. Eso no basta para llevarlo a un aula. Antes hacen falta la aprobación ética, el consentimiento de los acudientes, la política de datos de menores, la medición de la latencia de extremo a extremo y un protocolo de piloto con medición antes y después. Hasta entonces, la herramienta está en TRL 4.

# Recomendaciones

(1) Gestionar la aprobación ética y la autorización de una institución aliada. (2) Redactar la política de datos de menores con asesoría jurídica. (3) Medir la latencia de extremo a extremo y la iluminación en el aula. (4) Probar la instalación en un equipo limpio y en la plataforma macOS documentada. (5) Diseñar el piloto con grupo de comparación.

## Contribución de los autores

Contribución de los autores (CRediT, por confirmar): el primer autor revisó la ingeniería del repositorio, ejecutó las pruebas y las mediciones, y redactó el borrador; los demás autores participaron en la conceptualización, el desarrollo del software y la revisión; Cristian Javier Cano-Mogollón supervisó y revisó.

## Declaraciones finales

[Heading 3] Financiación

Esta investigación no recibió financiación externa. [Por confirmar por el equipo.]

[Heading 3] Conflicto de intereses

Los autores declaran que no existen conflictos de intereses. [Por confirmar.]

[Heading 3] Consentimiento informado

No aplica en este estudio; la calibración de referencia contiene solo coordenadas de puntos de la mano de una persona. El piloto con menores requerirá consentimiento informado de los acudientes.

[Heading 3] Declaración de la Junta de Revisión Institucional

No aplica a esta evaluación técnica; el piloto requerirá aprobación de un comité de ética institucional.

[Heading 3] Disponibilidad de datos, código y materiales de investigación

El código, las pruebas, los scripts de medición, los resultados estructurados y la verificación de referencias están en el repositorio del proyecto y en la carpeta de análisis de la entrega. El repositorio público está por definir.

[Heading 3] Uso de herramientas de inteligencia artificial

Se utilizó un asistente de inteligencia artificial (Claude, de Anthropic) para revisar el código, ejecutar las pruebas y mediciones, verificar las referencias y redactar borradores. Los autores revisaron el contenido y asumen la responsabilidad del texto y de los resultados.

**Declarations (English)

Author Contributions: the first author reviewed the repository engineering, ran the tests and measurements and drafted the manuscript; the other authors contributed conceptualization, software and review; C. J. Cano-Mogollón supervised. No external funding. No conflicts of interest. Consent and IRB: not applicable to this technical study; the pilot will require both. Data and code: project repository and analysis folder.

# References

[1] F. Zhang et al., “MediaPipe Hands: On-device Real-time Hand Tracking,” arXiv:2006.10214, 2020, doi: 10.48550/arXiv.2006.10214.

[2] N. Li and Z. Hong, “Deep Reinforcement Learning for Personalised Music Learning Pathways,” Annals of Data Science, vol. 13, no. 4, pp. 1013-1032, 2026, doi: 10.1007/s40745-026-00689-1.

[3] J. Li, “A reinforcement learning-based adaptive evaluation framework for personalized music education,” PeerJ Computer Science, vol. 12, art. e3464, 2026, doi: 10.7717/peerj-cs.3464.

[4] J. Li, “Deep learning-based personalized learning path planning and optimization model for music education,” Discover Artificial Intelligence, vol. 6, no. 1, art. 434, 2026, doi: 10.1007/s44163-026-01115-4.

[5] X. Tang, “The application of deep reinforcement learning in music teaching interaction,” Discover Computing, vol. 29, no. 1, art. 131, 2026, doi: 10.1007/s10791-026-10022-2.

[6] Z. Wang, “Music teaching evaluation using multimodal deep reinforcement learning,” Discover Artificial Intelligence, vol. 6, no. 1, art. 151, 2026, doi: 10.1007/s44163-026-00832-0.

[7] X. Deng, Y. Zhou, X. Guan, and Y. Wang, “An adaptive emotion aware music education system using machine learning for personalized emotional wellbeing enhancement,” Scientific Reports, vol. 16, no. 1, art. 25833, 2026, doi: 10.1038/s41598-026-53749-0.

[8] X. Shi, “An affective computing framework for preschool music education using MoE architecture and neural radiance fields,” Discover Artificial Intelligence, vol. 6, no. 1, art. 812, 2026, doi: 10.1007/s44163-026-01858-0.

[9] X. Deng, “AI-Based Feedback Systems in Piano Education: Effects on Technical Accuracy and Learner Autonomy,” Música Hodie, vol. 26, 2026, doi: 10.5216/mh.v26.85176.

[10] T. Chuluunsaikhan and S. H. Park, “Piano keyboard detection algorithm using deep learning,” Multimedia Tools and Applications, vol. 85, no. 5, art. 508, 2026, doi: 10.1007/s11042-026-21667-y.

[11] P. Ramoneda, M. Suzuki, A. Maezawa, and X. Serra, “Difficulty-aware score generation for piano sight-reading,” Expert Systems with Applications, vol. 321, art. 132088, 2026, doi: 10.1016/j.eswa.2026.132088.

[12] H. Yi, T. Liu, and G. Lan, “The key artificial intelligence technologies in early childhood education: a review,” Artificial Intelligence Review, vol. 57, no. 1, art. 12, 2024, doi: 10.1007/s10462-023-10637-7.

[13] K. Apaydinli, “Content analysis of music education studies related to augmented reality technology,” Journal of Educational Technology and Online Learning, vol. 6, no. 2, pp. 447-481, 2023, doi: 10.31681/jetol.1243501.

[14] J. Barroso-Osuna, A. León-Garrido, C. Llorente-Cejudo, and J. Ruiz-Palmero, “El impacto de las apps móviles y la carga del trabajo en la Educación Musical universitaria: un estudio experimental,” Revista de Educación a Distancia (RED), vol. 24, no. 80, 2024, doi: 10.6018/red.602301.

[15] A. León-Garrido, J. M. Barroso-Osuna, and M. C. Llorente-Cejudo, “Diseño y validación de un instrumento de evaluación para apps móviles musicales a través del juicio de expertos,” Aula Abierta, vol. 53, no. 2, pp. 169-179, 2024, doi: 10.17811/rifie.20620.

[16] DANE, “Proyecciones de población municipal 2020–2035, actualización post COVID-19 (Montería, 2026),” Bogotá, Colombia. [Online]. Available: https://www.dane.gov.co/files/censo2018/proyecciones-de-poblacion/Municipal/DCD-area-sexo-edad-proypoblacion-Mun-2020-2035-ActPostCOVID-19.xlsx. Accessed: Nov. 5, 2026.

[17] N. J. Cepeda, H. Pashler, E. Vul, J. T. Wixted, and D. Rohrer, “Distributed practice in verbal recall tasks: A review and quantitative synthesis.,” Psychological Bulletin, vol. 132, no. 3, pp. 354-380, 2006, doi: 10.1037/0033-2909.132.3.354.

[18] A. T. Corbett and J. R. Anderson, “Knowledge tracing: Modeling the acquisition of procedural knowledge,” User Modelling and User-Adapted Interaction, vol. 4, no. 4, pp. 253-278, 1995, doi: 10.1007/BF01099821.

[19] R. C. Wilson, A. Shenhav, M. Straccia, and J. D. Cohen, “The Eighty Five Percent Rule for optimal learning,” Nature Communications, vol. 10, no. 1, art. 4646, 2019, doi: 10.1038/s41467-019-12552-4.

[20] E. B. Wilson, “Probable Inference, the Law of Succession, and Statistical Inference,” Journal of the American Statistical Association, vol. 22, no. 158, pp. 209-212, 1927, doi: 10.1080/01621459.1927.10502953.

[21] P. Woźniak and E. Gorzelańczyk, “Optimization of repetition spacing in the practice of learning,” Acta Neurobiologiae Experimentalis, vol. 54, no. 1, pp. 59-62, 1994, doi: 10.55782/ane-1994-1003.

---
## Avisos

- La **Ley 1581 de 2012** se menciona como marco; el equipo debe revisarla con asesoría jurídica antes del piloto.
- La plataforma objetivo documentada incluye macOS, que **no** se evaluó.

## Guion de defensa

**¿Qué significa «reproducible» aquí?**  
Que cada cifra sale de un script con semilla fija que escribe un archivo estructurado; cualquiera repite la medición con una sola orden.

**¿Qué falta para ir a un aula?**  
Aprobación ética, consentimiento de acudientes, política de datos de menores, latencia de extremo a extremo y protocolo de piloto con medición antes y después.

**¿Qué datos guarda la aplicación?**  
Los intentos de cada niño en una base SQLite local; la calibración de referencia son solo coordenadas de la mano, sin imágenes.

**¿Qué TRL tiene y por qué?**  
TRL 4: componentes validados en laboratorio; para TRL 5 hace falta un piloto en el entorno de uso.

**¿Qué diferencias encontraste entre documentación y código?**  
Fotogramas de suelta (2 vs 6), tamaño del repositorio (8.599/44 vs 10.581/62), ventana mínima (380 vs 480 ms) y el desglose del 8 %. Prevalece el código.
