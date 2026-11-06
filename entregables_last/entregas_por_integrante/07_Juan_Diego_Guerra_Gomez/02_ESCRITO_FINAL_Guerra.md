# ESCRITO FINAL — Juan Diego Guerra Gómez

**Tu hilo:** Lo reportado y lo medido: verificación independiente de las cifras de desempeño y regla simple para reportarlas (script, muestra, intervalo).

**Preprint y artículo:** Tu preprint reconoce que los indicadores (30 fps, 94,2 %, 38 ms) son «reportados» y que hace falta comprobarlos. Tu artículo hace esa comprobación: reproduce el 8 %, mide la latencia y el optimizador, explica por qué el 94,2 % no es reproducible y lista seis discrepancias.

---
## ESCRITO FINAL 1 — Preprint

**Hand Sing Kids: sistema inteligente adaptativo para el aprendizaje de teoría musical infantil mediante visión computacional e inteligencia artificial.**

Juan Diego Guerra Gómez. Universidad Pontificia Bolivariana, seccional Montería, Ingeniería Industrial. Proyecto integrador dos. 26 de octubre 2026.

**Resumen (Abstract)**

Hand Sing Kids es una propuesta tecnológica orientada al aprendizaje de teoría musical infantil mediante visión computacional, inteligencia artificial y gamificación. El problema que aborda es la dificultad de adaptar las actividades musicales al ritmo y desempeño de cada niño. El sistema utiliza una cámara, herramientas de reconocimiento de manos y un mecanismo de selección adaptativa de actividades, procesa imágenes a 30 fotogramas por segundo, reporta una precisión superior al 94,2 % en la clasificación de ocho gestos musicales y un tiempo promedio de 38 milisegundos para asignar actividades. El mayor aporte de Hand Sing Kids es integrar reconocimiento gestual y personalización en una misma herramienta. Su utilidad deberá comprobarse mediante pruebas con niños, evaluación de conocimientos musicales y análisis de la experiencia de usuario.

Palabras clave: educación musical, inteligencia artificial, visión computacional, gamificación, aprendizaje adaptativo.

**Introducción**

Internacional. La tecnología digital se utiliza cada vez más para apoyar actividades musicales interactivas. Cuervo et al. (2022) analizan su aplicación en la educación musical infantil. Considero que estas herramientas pueden complementar la enseñanza tradicional, siempre que tengan objetivos pedagógicos claros.

Nacional. En Colombia, los recursos digitales representan una oportunidad para diversificar la enseñanza musical. Sin embargo, su implementación puede depender de la disponibilidad de equipos, conectividad y preparación docente. Por eso, pienso que una solución tecnológica debe ser accesible y fácil de utilizar.

Local. En Córdoba, Hand Sing Kids plantea una alternativa para enseñar conceptos musicales mediante gestos y actividades adaptativas. Considero relevante explorar su aplicación en Montería, aunque se necesitan pruebas en instituciones educativas para conocer las necesidades reales de los niños de la región.

Problema y objetivo. Algunas herramientas educativas ofrecen actividades iguales para todos los usuarios. Frente a ello, el proyecto busca adaptar la experiencia a las respuestas del estudiante.

**Métodos**

Se realizó una revisión bibliográfica sobre psicología del desarrollo y aprendizaje musical infantil, complementada con observaciones en instituciones educativas de Montería y consultas iterativas con docentes expertos de la UPB. El sistema se desarrolló por etapas: primero, reconocimiento de gestos mediante cámara; después, incorporación de gamificación, una interfaz simplificada y un agente de inteligencia artificial adaptativo. Se utilizaron Python, OpenCV y MediaPipe para procesar imágenes y reconocer gestos, además de herramientas de optimización e inteligencia artificial para seleccionar actividades. El análisis se basó en la documentación técnica y los indicadores reportados por el proyecto. No se especifican el número de niños participantes ni pruebas estadísticas, y no se documenta una evaluación independiente de los resultados pedagógicos.

**Resultados**

El prototipo Hand Sing Kids alcanza una frecuencia de procesamiento de 30 fotogramas por segundo, una precisión superior al 94,2 % en el reconocimiento de ocho gestos musicales y un tiempo promedio de 38 milisegundos para asignar actividades adaptativas. Estos resultados muestran el desempeño técnico reportado del sistema y su capacidad para reconocer gestos y seleccionar actividades en tiempo real.

**Discusión**

Hand Sing Kids integra visión computacional, inteligencia artificial y optimización matemática para adaptar las actividades musicales al desempeño infantil. Esta propuesta puede hacer más dinámico el aprendizaje; sin embargo, es necesario comprobar su efectividad directamente con niños. Se recomienda realizar pruebas en el aula, comparar los conocimientos musicales antes y después de su uso y considerar las opiniones de docentes para identificar sus beneficios y aspectos por mejorar.

**Conclusiones**

Considero que Hand Sing Kids es una propuesta innovadora con potencial para complementar la educación musical infantil. Los indicadores técnicos reportados son prometedores, pero todavía es necesario comprobar su efectividad pedagógica mediante estudios con niños. Su valor no debe medirse únicamente por la rapidez o precisión del sistema, sino también por su capacidad para facilitar el aprendizaje y adaptarse a las necesidades de los estudiantes.

**Referencias**

Cuervo, L., Bonastre, C., y García-Gil, D. (2022). Tecnología digital en la educación musical infantil. Praxis & Saber, 13(32), e13201. https://doi.org/10.19053/22160159.v13.n32.2022.13201

Lam, C. K. (2024). Technology-enhanced creativity in K-12 music education: A scoping review. International Journal of Music Education, 42(4), 691-703. https://doi.org/10.1177/02557614231194073

---
## ESCRITO FINAL 2 — Resumen y abstract

**Resumen.** Los proyectos de ingeniería suelen reportar cifras de desempeño que se copian de un documento a otro sin que nadie las repita. Se contrastan las cifras que la documentación de Hand Sing Kids, una aplicación que enseña las ocho notas de Do3 a Do4 con señas de las manos, reportaba (30 fotogramas por segundo, precisión superior a 94,2 % en ocho gestos, 38 ms para asignar actividades, 8 % de notas falsas, 2,3 ms de latencia) con mediciones propias, hechas con scripts reproducibles sobre el código del repositorio. Se reprodujo el 8 % de notas falsas (8,0 %; IC 95 %: 6,1 a 10,3 %; estable en 30 semillas: media 7,5 %, desviación 0,8); la latencia del descriptor y el clasificador fue de 0,89 ms; y una sesión de ejemplo del optimizador se resolvió en 40 ms. La precisión de 94,2 % no pudo reproducirse porque el protocolo que la produjo no está documentado; con el protocolo propio, el reconocimiento fue de 100 % sin ruido y de 86,0 % con ruido de 0,09. Los 30 fotogramas por segundo no se midieron. Además se hallaron seis discrepancias entre documentación y código, que se enumeran. Se propone una regla para reportar: toda cifra debe indicar el script que la produce, el tamaño de muestra y su intervalo. No hubo pruebas con niños; el nivel de madurez es TRL 4.

**Abstract.** Engineering projects often report performance figures that are copied from one document to another without anyone repeating them. The figures that the documentation of Hand Sing Kids, an application that teaches the eight notes from C3 to C4 with hand signs, reported (30 frames per second, accuracy above 94.2 % on eight gestures, 38 ms to assign activities, 8 % false notes, 2.3 ms latency) are contrasted with our own measurements, made with reproducible scripts on the repository code. The 8 % false-note rate was reproduced (8,0 %; 95 % CI 6,1 to 10,3 %; stable across 30 seeds: mean 7,5 %, SD 0,8); descriptor and classifier latency was 0,89 ms; and an example optimizer session was solved in 40 ms. The 94.2 % accuracy could not be reproduced because the protocol that produced it is not documented; with our protocol, recognition was 100 % without noise and 86,0 % at noise 0.09. The 30 frames per second were not measured. Six discrepancies between documentation and code were also found and are listed. A reporting rule is proposed: every figure should state the script that produces it, the sample size and its interval. No tests with children were done; the readiness level is TRL 4.

---
## ESCRITO FINAL 3 — Texto del artículo

[Título art] Lo reportado y lo medido: verificación independiente de las cifras de desempeño de Hand Sing Kids

[Título art] What was reported and what was measured: independent verification of the performance figures of Hand Sing Kids

[Nombre autores] Juan Diego Guerra-Gómez^1}^*}, Antolin De Jesús Vitola-Montes^2}, Isaías José Petro-Rodríguez^3}, Andrés Julián Negrete-Pacheco^4}, Juliana Esther Carrascal-Hernández^5}, Angel Quintana-Jiménez^6}, Alejandro Pemberty-Vergara^7}, Cristian Javier Cano-Mogollón^8}

^1} Autor 1: Juan Diego Guerra-Gómez - Universidad Pontificia Bolivariana, Seccional Montería, Córdoba, Colombia. ORCID: pendiente. Correo electrónico: juan.guerra@upb.edu.co

^2} Autor 2: Antolin De Jesús Vitola-Montes - Universidad Pontificia Bolivariana, Seccional Montería, Córdoba, Colombia. ORCID: pendiente. Correo electrónico: antolin.vitola@upb.edu.co

^3} Autor 3: Isaías José Petro-Rodríguez - Universidad Pontificia Bolivariana, Seccional Montería, Córdoba, Colombia. ORCID: pendiente. Correo electrónico: isaias.petro@upb.edu.co

^4} Autor 4: Andrés Julián Negrete-Pacheco - Universidad Pontificia Bolivariana, Seccional Montería, Córdoba, Colombia. ORCID: pendiente. Correo electrónico: andresj.negretep@upb.edu.co

^5} Autor 5: Juliana Esther Carrascal-Hernández - Universidad Pontificia Bolivariana, Seccional Montería, Córdoba, Colombia. ORCID: pendiente. Correo electrónico: juliana.carrascal@upb.edu.co

^6} Autor 6: Angel Quintana-Jiménez - Universidad Pontificia Bolivariana, Seccional Montería, Córdoba, Colombia. ORCID: pendiente. Correo electrónico: angel.quintana@upb.edu.co

^7} Autor 7: Alejandro Pemberty-Vergara - Universidad Pontificia Bolivariana, Seccional Montería, Córdoba, Colombia. ORCID: pendiente. Correo electrónico: alejandro.pemberty@upb.edu.co

^8} Co-Autor / Co-Investigador: M.Sc. Cristian Javier Cano Mogollón. Filiación: Docente Titular, Facultad de Ingeniería Industrial. Grupo de Investigación en Simulación, Logística y Gestión de Operaciones (SILOGE), Hub Industrial Solution (HIS), Universidad Pontificia Bolivariana, Seccional Montería, Colombia. ORCID: pendiente. Correo electrónico: cristian.cano@upb.edu.co

^*} Autor de correspondencia: Juan Diego Guerra-Gómez (juan.guerra@upb.edu.co).

**Resumen:

Los proyectos de ingeniería suelen reportar cifras de desempeño que se copian de un documento a otro sin que nadie las repita. Se contrastan las cifras que la documentación de Hand Sing Kids, una aplicación que enseña las ocho notas de Do3 a Do4 con señas de las manos, reportaba (30 fotogramas por segundo, precisión superior a 94,2 % en ocho gestos, 38 ms para asignar actividades, 8 % de notas falsas, 2,3 ms de latencia) con mediciones propias, hechas con scripts reproducibles sobre el código del repositorio. Se reprodujo el 8 % de notas falsas (8,0 %; IC 95 %: 6,1 a 10,3 %; estable en 30 semillas: media 7,5 %, desviación 0,8); la latencia del descriptor y el clasificador fue de 0,89 ms; y una sesión de ejemplo del optimizador se resolvió en 40 ms. La precisión de 94,2 % no pudo reproducirse porque el protocolo que la produjo no está documentado; con el protocolo propio, el reconocimiento fue de 100 % sin ruido y de 86,0 % con ruido de 0,09. Los 30 fotogramas por segundo no se midieron. Además se hallaron seis discrepancias entre documentación y código, que se enumeran. Se propone una regla para reportar: toda cifra debe indicar el script que la produce, el tamaño de muestra y su intervalo. No hubo pruebas con niños; el nivel de madurez es TRL 4.

**Palabras clave:

verificación de resultados; reproducibilidad; métricas de desempeño; intervalos de confianza; trazabilidad; educación musical infantil; Montería

**Abstract:

Engineering projects often report performance figures that are copied from one document to another without anyone repeating them. The figures that the documentation of Hand Sing Kids, an application that teaches the eight notes from C3 to C4 with hand signs, reported (30 frames per second, accuracy above 94.2 % on eight gestures, 38 ms to assign activities, 8 % false notes, 2.3 ms latency) are contrasted with our own measurements, made with reproducible scripts on the repository code. The 8 % false-note rate was reproduced (8,0 %; 95 % CI 6,1 to 10,3 %; stable across 30 seeds: mean 7,5 %, SD 0,8); descriptor and classifier latency was 0,89 ms; and an example optimizer session was solved in 40 ms. The 94.2 % accuracy could not be reproduced because the protocol that produced it is not documented; with our protocol, recognition was 100 % without noise and 86,0 % at noise 0.09. The 30 frames per second were not measured. Six discrepancies between documentation and code were also found and are listed. A reporting rule is proposed: every figure should state the script that produces it, the sample size and its interval. No tests with children were done; the readiness level is TRL 4.

**Keywords:

results verification; reproducibility; performance metrics; confidence intervals; traceability; children's music education; Montería

# Introducción

## Una cifra sin origen

«Precisión superior al 94,2 %». La frase aparece en resúmenes y presentaciones de Hand Sing Kids, y suena a un resultado. Pero una cifra de desempeño solo es un resultado si se sabe con qué datos se obtuvo, cuántas pruebas fueron, cómo se contó el acierto y si alguien más puede repetirla. En los proyectos de ingeniería es común que una cifra nazca en un informe, se copie a un resumen y viaje de documento en documento perdiendo su contexto. Este trabajo propone lo contrario: tomar las cifras reportadas y comprobar, una por una, si se pueden sostener.

La literatura sobre inteligencia artificial en educación musical describe sistemas y resultados de modelos [1]–[10], con revisiones generales [11] y estudios de aplicaciones [12]–[14]. Para estimar incertidumbre de una proporción se usa el intervalo de Wilson [15]; el seguimiento de manos proviene de MediaPipe [16]. Este trabajo no discute el contenido de esos estudios: aprovecha la práctica de reportar con intervalos y la lleva a un proyecto de clase.

## Qué se reportaba

*Tabla 1. Cifras reportadas por la documentación o por documentos previos del proyecto

*Fuente: documentación del proyecto; las cifras se citan tal como aparecen allí.

## Objetivo

Contrastar con mediciones propias las cifras de desempeño de Hand Sing Kids, registrar las discrepancias entre documentación y código y proponer una regla simple para reportar cifras de forma trazable.

# Métodos

## Regla de verificación

Cada cifra reportada se clasificó en una de cuatro categorías: reproducida (se repitió con un protocolo equivalente y coincide), no comparable (se midió algo distinto), no medida (requiere un equipo del que no se dispone) o no reproducible (falta el protocolo). Las mediciones se hicieron con scripts que escriben sus salidas en un archivo estructurado y con semillas fijas, en un solo equipo con Windows 11 y Python 3.12.10.

## Protocolo propio

Se usó una calibración de ocho señas de una persona y perturbaciones simuladas de tamaño, giro y ruido. Se midió el reconocimiento de 480 señas válidas por nivel de ruido, las notas disparadas por error en 640 posturas que no son seña (320 transiciones y 320 combinaciones de manos), la estabilidad de esa tasa con 30 semillas distintas, la latencia del descriptor y el clasificador con 2.000 repeticiones y una sesión de ejemplo del optimizador. Las proporciones llevan intervalos de Wilson al 95 %.

# Resultados

## Qué se pudo sostener

*Tabla 2. Cifras reportadas frente a cifras medidas

*Fuente: elaboración propia; analisis/resultados_vision.json y salida de las pruebas del repositorio.

La tasa de notas falsas se reproduce con una precisión notable: 8,0 % frente al 8 % reportado, y no depende de una semilla favorable, porque con 30 semillas distintas la media fue de 7,5 % y el rango, de 6,1 a 9,2 %. La latencia medida, de 0,89 ms, es menor que la reportada, pero no puede decirse que la contradiga: el documento previo midió en otro equipo y no queda claro si con el mismo alcance. Ninguna de las dos incluye la captura de la cámara. El tiempo de 40 ms del optimizador es del mismo orden que el reportado, aunque proviene de una sola sesión.

La cifra de precisión merece una explicación aparte. Un 94,2 % solo tiene sentido con un protocolo: qué señas, de cuántas personas, con qué perturbaciones y cuántas pruebas. Ese protocolo no está en la documentación revisada. Con el protocolo propio, el reconocimiento fue de 100 % sin ruido y de 86,0 % con ruido de 0,09. No son cifras contradictorias, porque miden cosas distintas, y por eso no se declara que la primera sea falsa, sino que no puede reproducirse ni compararse.

*Figura 1. (a) Tasa de notas falsas medida con 30 semillas (media y rango) frente al 8 % reportado. (b) Latencia reportada y medida.

## Discrepancias entre documentación y código

*Tabla 3. Discrepancias halladas entre la documentación y el código

*Fuente: elaboración propia a partir de la revisión del código y de la documentación.

# Discusión

## Discusión

**Respuesta inmediata frente a margen.** Con ventana de un fotograma, la nota suena en cuanto el clasificador la reconoce, sin barra de aceptación. El costo es un 8 % de falsos positivos en transiciones, que antes la votación de varios fotogramas reducía a cambio de una espera perceptible. Es un cambio de compromiso y no una mejora en ambos sentidos. Para niños pequeños se prefirió la respuesta inmediata, y la ventana puede ampliarse por niño desde Ajustes. Los resultados con ruido alto (86,0 %) indican que, en la práctica, un reconocimiento que se abstiene en lugar de equivocarse cuesta una repetición de la seña, mientras que un falso positivo rompe el juego.

**La lección del sonido duplicado.** En una iteración posterior, una misma nota sostenida sonaba dos veces. La causa no estaba en el clasificador: con ventana de un fotograma, un parpadeo del rastreo (MediaPipe pierde la mano uno o dos fotogramas aunque esté quieta) se interpretaba como que el niño había soltado la seña, y la siguiente lectura repetía la nota. Con la ventana de varios fotogramas, la votación absorbía ese parpadeo; al quitarla, el mecanismo de suelta quedó como único filtro y su umbral hubo que subir de dos a seis fotogramas. Cambiar un parámetro de un módulo puede dejar a otro cargando con una función que no se había probado en solitario; la batería del estabilizador incluye ahora la prueba del parpadeo breve. También quedó documentada la corrección de que la aceleración progresiva atribuida a la versión inicial no existía: la velocidad era constante.

**Amenazas a la validez.** (i) La calibración es de una sola persona y de ocho señas; no se conoce la variabilidad entre niños. (ii) Las perturbaciones son simuladas sobre coordenadas ya extraídas: no incluyen los errores de detección de MediaPipe, el desenfoque ni la iluminación. (iii) Las posturas negativas se construyeron por interpolación y combinación, y la tasa real depende de cómo se mueven los niños. (iv) El método v1 se evaluó con la misma calibración, de modo que la comparación es interna. (v) Las constantes (pesos del dominio, umbral 0,80, p^*}=0,75, ventanas de acierto) provienen de la literatura y del ajuste sobre los datos disponibles, no de un estudio con niños. (vi) Las canciones son simplificaciones a la escala de ocho notas, sin revisión de un músico formado. (vii) No se implementó aprendizaje por refuerzo; el motor adaptativo es un conjunto de reglas, y las interfaces para aprendizaje automático y por refuerzo están documentadas sin datos reales que las alimenten. Estos límites impiden afirmar que el sistema enseñe música: solo respaldan que el reconocedor y el planificador se comportan como se describen en laboratorio.

**Una regla para reportar.** A partir de lo anterior se propone que toda cifra de desempeño que aparezca en un resumen, una presentación o un artículo indique tres cosas: el script o el procedimiento que la produce, el tamaño de la muestra y su intervalo de confianza. Con esa regla, una frase como «precisión superior al 94,2 %» no pasaría a un resumen sin su protocolo. La regla es sencilla y se puede aplicar en un proyecto de clase.

Para los componentes de aprendizaje personalizado y estimación del dominio del sistema, véanse los trabajos sobre seguimiento del conocimiento y práctica distribuida [17]–[21].

## Madurez tecnológica

Con estas verificaciones, el nivel de madurez que mejor se sostiene es TRL 4: componentes validados en laboratorio, mediciones repetibles y ningún componente probado en el entorno de uso. Las cifras que no se pudieron medir, como los fotogramas por segundo, deben medirse con la cámara real antes de hablar de TRL 5, que además exige un piloto con niños.

# Conclusiones

De cinco cifras reportadas, una se reprodujo (8 % de notas falsas), una resultó del mismo orden (38 ms), una no coincide pero se midió en otro equipo (latencia), una no pudo compararse por falta de protocolo (94,2 %) y una no se midió (30 fotogramas por segundo). Además se hallaron seis discrepancias entre documentación y código, resueltas a favor del código y de la medición. El nivel de madurez es TRL 4.

# Recomendaciones

(1) Documentar el protocolo de cualquier cifra de precisión, con su muestra. (2) Medir los fotogramas por segundo con la cámara real. (3) Repetir la medición de latencia en el equipo de aula. (4) Aplicar la regla de reporte (script, muestra, intervalo) en las presentaciones del proyecto. (5) Mantener actualizada la lista de discrepancias.

## Contribución de los autores

Contribución de los autores (CRediT, por confirmar): el primer autor contrastó las cifras reportadas con las mediciones, registró las discrepancias y redactó el borrador; los demás autores participaron en el desarrollo del software, las mediciones y la revisión; Cristian Javier Cano-Mogollón supervisó y revisó.

## Declaraciones finales

[Heading 3] Financiación

No se recibió financiación externa. [Por confirmar por el equipo.]

[Heading 3] Conflicto de intereses

Los autores declaran que no tienen conflictos de intereses. [Por confirmar.]

[Heading 3] Consentimiento informado

No aplica: no se recolectaron datos de personas.

[Heading 3] Declaración de la Junta de Revisión Institucional

No aplica a esta verificación técnica; las pruebas con niños requerirán aprobación ética y consentimiento de acudientes.

[Heading 3] Disponibilidad de datos, código y materiales de investigación

Los scripts de medición, el archivo de resultados (resultados_vision.json), la salida de las pruebas y la lista de discrepancias están en la carpeta de análisis de la entrega y en el repositorio del proyecto.

[Heading 3] Uso de herramientas de inteligencia artificial

Se usó el asistente Claude (Anthropic) para ejecutar las mediciones, contrastar documentación y código, verificar referencias y redactar borradores. Los autores revisaron todo el contenido y responden por él.

**Declarations (English)

Author Contributions: the first author contrasted reported figures with measurements, recorded the discrepancies and drafted the manuscript; the other authors contributed software, measurements and review; C. J. Cano-Mogollón supervised. No external funding. No conflicts of interest. Consent and IRB: not applicable. Data and code: analysis folder and project repository.

# References

[1] N. Li and Z. Hong, “Deep Reinforcement Learning for Personalised Music Learning Pathways,” Annals of Data Science, vol. 13, no. 4, pp. 1013-1032, 2026, doi: 10.1007/s40745-026-00689-1.

[2] J. Li, “A reinforcement learning-based adaptive evaluation framework for personalized music education,” PeerJ Computer Science, vol. 12, art. e3464, 2026, doi: 10.7717/peerj-cs.3464.

[3] J. Li, “Deep learning-based personalized learning path planning and optimization model for music education,” Discover Artificial Intelligence, vol. 6, no. 1, art. 434, 2026, doi: 10.1007/s44163-026-01115-4.

[4] X. Tang, “The application of deep reinforcement learning in music teaching interaction,” Discover Computing, vol. 29, no. 1, art. 131, 2026, doi: 10.1007/s10791-026-10022-2.

[5] Z. Wang, “Music teaching evaluation using multimodal deep reinforcement learning,” Discover Artificial Intelligence, vol. 6, no. 1, art. 151, 2026, doi: 10.1007/s44163-026-00832-0.

[6] X. Deng, Y. Zhou, X. Guan, and Y. Wang, “An adaptive emotion aware music education system using machine learning for personalized emotional wellbeing enhancement,” Scientific Reports, vol. 16, no. 1, art. 25833, 2026, doi: 10.1038/s41598-026-53749-0.

[7] X. Shi, “An affective computing framework for preschool music education using MoE architecture and neural radiance fields,” Discover Artificial Intelligence, vol. 6, no. 1, art. 812, 2026, doi: 10.1007/s44163-026-01858-0.

[8] X. Deng, “AI-Based Feedback Systems in Piano Education: Effects on Technical Accuracy and Learner Autonomy,” Música Hodie, vol. 26, 2026, doi: 10.5216/mh.v26.85176.

[9] T. Chuluunsaikhan and S. H. Park, “Piano keyboard detection algorithm using deep learning,” Multimedia Tools and Applications, vol. 85, no. 5, art. 508, 2026, doi: 10.1007/s11042-026-21667-y.

[10] P. Ramoneda, M. Suzuki, A. Maezawa, and X. Serra, “Difficulty-aware score generation for piano sight-reading,” Expert Systems with Applications, vol. 321, art. 132088, 2026, doi: 10.1016/j.eswa.2026.132088.

[11] H. Yi, T. Liu, and G. Lan, “The key artificial intelligence technologies in early childhood education: a review,” Artificial Intelligence Review, vol. 57, no. 1, art. 12, 2024, doi: 10.1007/s10462-023-10637-7.

[12] K. Apaydinli, “Content analysis of music education studies related to augmented reality technology,” Journal of Educational Technology and Online Learning, vol. 6, no. 2, pp. 447-481, 2023, doi: 10.31681/jetol.1243501.

[13] J. Barroso-Osuna, A. León-Garrido, C. Llorente-Cejudo, and J. Ruiz-Palmero, “El impacto de las apps móviles y la carga del trabajo en la Educación Musical universitaria: un estudio experimental,” Revista de Educación a Distancia (RED), vol. 24, no. 80, 2024, doi: 10.6018/red.602301.

[14] A. León-Garrido, J. M. Barroso-Osuna, and M. C. Llorente-Cejudo, “Diseño y validación de un instrumento de evaluación para apps móviles musicales a través del juicio de expertos,” Aula Abierta, vol. 53, no. 2, pp. 169-179, 2024, doi: 10.17811/rifie.20620.

[15] E. B. Wilson, “Probable Inference, the Law of Succession, and Statistical Inference,” Journal of the American Statistical Association, vol. 22, no. 158, pp. 209-212, 1927, doi: 10.1080/01621459.1927.10502953.

[16] F. Zhang et al., “MediaPipe Hands: On-device Real-time Hand Tracking,” arXiv:2006.10214, 2020, doi: 10.48550/arXiv.2006.10214.

[17] N. J. Cepeda, H. Pashler, E. Vul, J. T. Wixted, and D. Rohrer, “Distributed practice in verbal recall tasks: A review and quantitative synthesis.,” Psychological Bulletin, vol. 132, no. 3, pp. 354-380, 2006, doi: 10.1037/0033-2909.132.3.354.

[18] A. T. Corbett and J. R. Anderson, “Knowledge tracing: Modeling the acquisition of procedural knowledge,” User Modelling and User-Adapted Interaction, vol. 4, no. 4, pp. 253-278, 1995, doi: 10.1007/BF01099821.

[19] R. C. Wilson, A. Shenhav, M. Straccia, and J. D. Cohen, “The Eighty Five Percent Rule for optimal learning,” Nature Communications, vol. 10, no. 1, art. 4646, 2019, doi: 10.1038/s41467-019-12552-4.

[20] P. Woźniak and E. Gorzelańczyk, “Optimization of repetition spacing in the practice of learning,” Acta Neurobiologiae Experimentalis, vol. 54, no. 1, pp. 59-62, 1994, doi: 10.55782/ane-1994-1003.

[21] DANE, “Proyecciones de población municipal 2020–2035, actualización post COVID-19 (Montería, 2026),” Bogotá, Colombia. [Online]. Available: https://www.dane.gov.co/files/censo2018/proyecciones-de-poblacion/Municipal/DCD-area-sexo-edad-proypoblacion-Mun-2020-2035-ActPostCOVID-19.xlsx. Accessed: Nov. 5, 2026.

---
## Avisos

- Tu preprint está **fechado el 26 de octubre de 2026** y dice «Proyecto integrador dos»: corresponde al corte anterior. Si el docente exige un preprint del Corte 3 con PRISMA y formulación, conviene reescribirlo o complementarlo.
- Tus referencias (Cuervo et al., 2022; Lam, 2024) no están entre las 21 del artículo; **verifica sus DOI** antes de usarlas.
- Las cifras de 30 fps, 94,2 % y 38 ms las usas como «reportadas»; el artículo no afirma que sean falsas.

## Guion de defensa

**¿La cifra de 94,2 % es falsa?**  
No la declaro falsa: no puedo reproducirla ni compararla porque no está documentado el protocolo (qué señas, cuántas pruebas, qué perturbaciones).

**¿Qué sí pudiste reproducir?**  
El 8 % de notas falsas: 8,0 % (51 de 640), estable en 30 semillas (media 7,5 %; 6,1–9,2 %).

**¿Por qué la latencia medida difiere de 2,3 ms?**  
Medí en otro equipo y solo el descriptor y el clasificador (0,89 ms por fotograma); no sé si el 2,3 ms tenía el mismo alcance.

**¿Cuál es tu regla de reporte?**  
Toda cifra debe indicar el script que la produce, el tamaño de muestra y su intervalo de confianza.

**¿Qué discrepancias hallaste?**  
Seis: fotogramas de suelta, ventana mínima, tamaño del repositorio, pares de señas, aceleración progresiva inexistente y desglose del 8 %. Prevalece el código.
