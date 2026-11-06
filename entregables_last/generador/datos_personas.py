"""Datos individuales: preprint (nuevo o existente), hilo, defensa y notas de cada integrante."""

TRANS_VITOLA = """**Sistema inteligente adaptativo para el aprendizaje de teoría musical infantil mediante visión computacional e inteligencia artificial**

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

El aporte principal es la creación de una herramienta digital que ataca un problema real en el aprendizaje musical de los más pequeños mediante modelo matemático y equipos informáticos. La correcta aplicación del prototipo deberá ser comprobada mediante pruebas técnicas y una prueba piloto."""

TRANS_GUERRA = """**Hand Sing Kids: sistema inteligente adaptativo para el aprendizaje de teoría musical infantil mediante visión computacional e inteligencia artificial.**

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

Lam, C. K. (2024). Technology-enhanced creativity in K-12 music education: A scoping review. International Journal of Music Education, 42(4), 691-703. https://doi.org/10.1177/02557614231194073"""

TRANS_NEGRETE = """**Andrés Julián Negrete Pacheco**

La propuesta Hand Sing Kids busca mejorar la enseñanza de la teoría musical a los niños mediante el uso de tecnologías de visión computacional e inteligencia artificial. Lo principal que se busca es el desarrollo de una herramienta lúdica que permita el reconocimiento de gestos mediante el vectorizado de manos a través de una cámara y poder relacionarlos con conceptos musicales, y así poder facilitar el aprendizaje de una forma más práctica, interactiva y entretenida.

La herramienta funciona utilizando Python, OpenCV y MediaPipe Hands, que permiten identificar las manos y así poder reconocer gestos y movimientos. A partir de la información, el sistema evalúa la respuesta para los niños, puede tomar el gesto que va acorde con su respectiva nota y así poder dar una retroalimentación adecuada. El aplicativo también puede tener en cuenta el desempeño de cada usuario y así poder adaptar los niveles y facilitar su progreso.

La propuesta del aplicativo surge de la búsqueda de alternativas que existen frente a algunas dificultades presentes en la educación musical y la necesidad de implementar estrategias que incentiven el interés por el aprendizaje musical, así poder complementar los métodos tradicionales de enseñanza y una nueva experiencia de aprendizaje mediante el juego."""

# clave -> datos
PERSONAS = {
    "Vitola": dict(
        n="01", carpeta="01_Antolin_Vitola_Montes", nombre="Antolin De Jesús Vitola Montes", corto="Antolin Vitola", art="art_vitola",
        hilo="Acceso y valor pedagógico: las manos como instrumento. De la fonomimia de Curwen a una herramienta que corre sin internet en un computador con cámara; qué se sabe y qué falta para saber si ayuda a aprender.",
        preprint=dict(modo="existente", scan="Antolin_Vitola_preprint (1).pdf", trans=TRANS_VITOLA, aprox=False),
        conecta="Tu preprint habla de Curwen, del acceso limitado a instrumentos en Córdoba, de comparar niños con Hand Sing Kids frente al método tradicional y de una prueba piloto. Tu artículo desarrolla exactamente eso: justificación pedagógica, tabla comparativa con la enseñanza tradicional, hipótesis de impacto y plan de validación.",
        notas=["Tu preprint dice que la interfaz usa **Streamlit**; el código evaluado usa **PySide6** (el artículo dice PySide6). Aclara con el equipo cuál es la correcta antes de defender.",
               "En tu preprint citas a «Mallaloqui»: no está entre las referencias verificadas del artículo. Si la vas a mantener, agrégala con DOI verificado.",
               "La mención a John Curwen (fonomimia, siglo XIX) es un dato histórico general; el artículo no la respalda con una referencia verificada. Si el docente la pide, añade una fuente."],
        defensa=[("¿Qué aporta Hand Sing Kids frente a la enseñanza tradicional con señas?", "La corrección inmediata y el registro de intentos sin depender de un docente atento, más el ajuste del ritmo por niño. Lo que no se ha demostrado es que mejore el aprendizaje: eso requiere un piloto."),
                 ("¿Por qué dices que sirve para Córdoba si no hay datos locales?", "No lo afirmo: la justificación es de diseño (computador con cámara, base local, sin internet). La utilidad en la región es una hipótesis. Solo uso cifras del DANE como contexto (535.052 habitantes; 80.254 de 3 a 12 años)."),
                 ("¿Qué evidencia técnica tienes?", "480 señas por nivel de ruido: 100 % sin ruido y 86,0 % con ruido 0,09; 8,0 % de notas falsas en 640 posturas frente a 100 % del método inicial; 8 de 8 baterías de pruebas sin fallos. No hubo niños."),
                 ("¿Cuáles son tus hipótesis?", "H1: niños de 3 a 12 años aprenden las ocho señas con calibración individual en una sesión corta. H2: en aula, las notas falsas son comparables a las de laboratorio. H3: la aplicación funciona sin internet (esta es propiedad de diseño)."),
                 ("¿Cómo sería el piloto?", "Grupos de instituciones de Montería, medición de conocimientos antes y después, comparación con el método tradicional, opinión del docente, aprobación ética y consentimiento de acudientes.")]),
    "Petro": dict(
        n="02", carpeta="02_Isaias_Petro_Rodriguez", nombre="Isaías José Petro Rodríguez", corto="Isaías Petro", art="art_petro",
        hilo="Visión computacional: distinguir la seña intencional del gesto de paso. Un descriptor invariante y una decisión por distancia, confianza y margen frente a un método que responde siempre.",
        preprint=dict(modo="nuevo", md="Preprint_NUEVO_1_Vision_Reconocimiento_de_senas.md"),
        conecta="Tu preprint plantea la pregunta (¿cuántas notas por error dispara?) y tu artículo la responde con el detalle: descriptor de 120 componentes, clasificación con margen, estabilizador, protocolo, tablas con intervalos de Wilson y las figuras de acierto, falsos positivos y similitud.",
        notas=["La calibración es de **una sola persona** y el ruido es **simulado**; lo dices en el preprint y en las amenazas a la validez.",
               "El 8,0 % de notas falsas se concentra en las transiciones (13,8 %); las manos cruzadas casi no fallan (2,2 %). Es el hallazgo más fino de tu artículo."],
        defensa=[("¿Por qué el método inicial acierta 100 % y es peor?", "Porque responde siempre: acierta toda seña válida, pero convierte toda postura en una nota, incluidas las 640 que no son seña (100 % de notas falsas)."),
                 ("¿Qué es el descriptor invariante?", "Un vector de 120 componentes (curvatura, apertura, pulgar, forma, relación entre manos) que no cambia con el tamaño, la posición ni el giro de la mano; se calcula con razones entre longitudes y vectores unitarios."),
                 ("¿Cómo decide el clasificador?", "Vecino más cercano sobre hasta tres muestras por nota; acepta si la distancia es ≤ 0,95, la confianza ≥ 0,55 y el margen sobre la segunda nota ≥ 0,08."),
                 ("¿Por qué baja a 86,0 % con ruido 0,09?", "Es el precio de abstenerse cuando hay duda: pedir que se repita una seña cuesta segundos; una nota falsa rompe la actividad."),
                 ("¿Qué falta?", "Más personas y niños, errores reales de detección, iluminación, velocidad de la mano como señal adicional y latencia de extremo a extremo.")]),
    "Negrete": dict(
        n="03", carpeta="03_Andres_Negrete_Pacheco", nombre="Andrés Julián Negrete Pacheco", corto="Andrés Negrete", art="art_negrete",
        hilo="El tiempo y la retroalimentación: la nota debe sonar cuando el niño la espera, una sola vez y sin castigarlo por el retraso del reconocimiento. Estabilizador, ventana asimétrica y puntaje del módulo Canciones.",
        preprint=dict(modo="existente", scan="Preprint Andrés Negrete.pdf", trans=TRANS_NEGRETE, aprox=True),
        conecta="Tu preprint habla de reconocer gestos con la cámara, dar retroalimentación adecuada, adaptar niveles y aprender mediante el juego. Tu artículo explica cómo se logra la retroalimentación en el tiempo correcto: estabilizador, ventana de acierto y puntaje de canciones.",
        notas=["La transcripción de tu preprint es **aproximada** (letra difícil de leer); compárala con tu original.",
               "La Tabla 2 del artículo es un **cálculo derivado de la fórmula** (suponiendo que la tolerancia no limita la ventana), no una medición. Dilo así.",
               "El valor de 6 fotogramas de suelta es el del código; la documentación decía 2."],
        defensa=[("¿Por qué la ventana de acierto es asimétrica?", "Es más ancha antes de la línea (1,15·h) que después (0,85·h), para no penalizar al niño por el tiempo que el reconocimiento tarda en confirmar."),
                 ("¿Por qué una nota sonaba dos veces?", "MediaPipe pierde la mano uno o dos fotogramas aunque esté quieta; con ventana de un fotograma eso se leía como suelta y la siguiente lectura repetía la nota. Se subió el umbral de suelta de 2 a 6 fotogramas."),
                 ("¿Qué pasa con los tempos rápidos?", "Hasta unos 100 bpm la ventana depende del intervalo entre notas; desde ahí actúa el piso de 480 ms. A 120 bpm son 276 ms antes y 204 ms después de la línea."),
                 ("¿Qué mediste de verdad?", "La latencia del descriptor y clasificador (0,89 ms por fotograma en promedio, sin cámara ni pantalla) y los falsos positivos (8,0 %). La Tabla 2 es cálculo."),
                 ("¿Qué falta?", "Latencia de extremo a extremo, notas duplicadas y señas repetidas con niños reales, y ajustar constantes del puntaje con observación en el aula.")]),
    "Carrascal": dict(
        n="04", carpeta="04_Juliana_Carrascal_Hernandez", nombre="Juliana Esther Carrascal Hernández", corto="Juliana Carrascal", art="art_carrascal",
        hilo="Aprendizaje adaptativo: del intento al dominio y al repaso. Qué sabe el niño, cuándo repasar y qué constantes son diseño y no datos.",
        preprint=dict(modo="nuevo", md="Preprint_NUEVO_2_Aprendizaje_adaptativo.md"),
        conecta="Tu preprint resume el modelo (dominio de cuatro componentes, repaso espaciado, predictor) y tu artículo lo formaliza con ecuaciones, tabla de constantes y origen de cada una, y las hipótesis para un piloto.",
        notas=["El **78 %** del predictor es sobre sus propios datos de entrenamiento: solo prueba que converge.",
               "Ninguna constante viene de datos de niños: la Tabla 2 lo muestra de forma explícita."],
        defensa=[("¿Por qué el dominio multiplica la retención?", "Para que el desuso degrade el dominio; el piso de 0,65 evita que una pausa larga lo lleve a cero."),
                 ("¿Cuándo una nota está dominada?", "Con dominio ≥ 0,80 y al menos seis intentos; retrocede si baja de 0,70."),
                 ("¿Qué hace el predictor y desde cuándo?", "Logística de tres variables (precisión, dificultad, días) que sustituye a la fórmula fija desde 40 intentos y se reentrena cada 20."),
                 ("¿Cómo sabes que funciona?", "No lo sé con niños. Verifiqué que las pruebas del dominio y del predictor pasan y que el ajuste converge; el efecto en el aprendizaje es hipótesis (H1–H3)."),
                 ("¿Qué referencias respaldan la idea?", "Knowledge tracing (Corbett y Anderson, 1995), práctica distribuida (Cepeda et al., 2006), SM-2 (Woźniak y Gorzelańczyk, 1994) y la regla del 85 % (Wilson et al., 2019).")]),
    "Quintana": dict(
        n="05", carpeta="05_Angel_Quintana_Jimenez", nombre="Angel Quintana Jiménez", corto="Angel Quintana", art="art_quintana",
        hilo="Optimización: la sesión como problema de programación entera mixta con óptimo verificable y restricciones pedagógicas explícitas.",
        preprint=dict(modo="nuevo", md="Preprint_NUEVO_4_Optimizacion_de_la_sesion.md"),
        conecta="Tu preprint enuncia el modelo (variables, objetivo, restricciones) y la verificación; tu artículo lo desarrolla con la formulación completa, la comparación de enfoques, el estado de cada parámetro y los límites.",
        notas=["No se hizo análisis de sensibilidad numérico: el artículo lo dice y solo ofrece una lectura cualitativa.",
               "«Óptimo» es matemático (mejor valor del objetivo con restricciones), no «mejor sesión para aprender»."],
        defensa=[("¿Por qué programación entera mixta y no refuerzo?", "No hay datos de niños y sí reglas pedagógicas explícitas; la formulación es explicable y su óptimo se verifica."),
                 ("¿Cómo verificas el óptimo?", "Con enumeración exhaustiva de las combinaciones de K actividades mientras no pasen de 4×10^5; la prueba del repositorio compara con CBC y pasó."),
                 ("¿Qué restricciones tiene el modelo?", "Tiempo total, tamaño de sesión, prerrequisitos, al menos una actividad lúdica, dificultad media ≤ 0,72, máximo dos por habilidad y un repaso vencido."),
                 ("¿Qué significan los pesos 1,00; 0,70; 0,35; 0,55?", "Son decisiones de diseño sobre ganancia, repaso, motivación y fatiga; no se calibraron con niños."),
                 ("¿Qué falta?", "Sensibilidad a los pesos, catálogos mayores, equipo de aula y comparación en piloto con sesiones elegidas por un docente.")]),
    "Pemberty": dict(
        n="06", carpeta="06_Alejandro_Pemberty_Vergara", nombre="Alejandro Pemberty Vergara", corto="Alejandro Pemberty", art="art_pemberty",
        hilo="Ingeniería reproducible y despliegue responsable: del prototipo al aula, con la lista de condiciones técnicas y éticas antes de probar con niños.",
        preprint=dict(modo="nuevo", md="Preprint_NUEVO_3_Despliegue_responsable_y_validacion.md"),
        conecta="Tu preprint explica que la herramienta corre en un computador común y qué falta para llevarla a un aula. Tu artículo lo documenta: estado de ingeniería, reproducibilidad, tabla de condiciones, datos de menores y orden del piloto.",
        notas=["La **Ley 1581 de 2012** se menciona como marco; el equipo debe revisarla con asesoría jurídica antes del piloto.",
               "La plataforma objetivo documentada incluye macOS, que **no** se evaluó."],
        defensa=[("¿Qué significa «reproducible» aquí?", "Que cada cifra sale de un script con semilla fija que escribe un archivo estructurado; cualquiera repite la medición con una sola orden."),
                 ("¿Qué falta para ir a un aula?", "Aprobación ética, consentimiento de acudientes, política de datos de menores, latencia de extremo a extremo y protocolo de piloto con medición antes y después."),
                 ("¿Qué datos guarda la aplicación?", "Los intentos de cada niño en una base SQLite local; la calibración de referencia son solo coordenadas de la mano, sin imágenes."),
                 ("¿Qué TRL tiene y por qué?", "TRL 4: componentes validados en laboratorio; para TRL 5 hace falta un piloto en el entorno de uso."),
                 ("¿Qué diferencias encontraste entre documentación y código?", "Fotogramas de suelta (2 vs 6), tamaño del repositorio (8.599/44 vs 10.581/62), ventana mínima (380 vs 480 ms) y el desglose del 8 %. Prevalece el código.")]),
    "Guerra": dict(
        n="07", carpeta="07_Juan_Diego_Guerra_Gomez", nombre="Juan Diego Guerra Gómez", corto="Juan Diego Guerra", art="art_guerra",
        hilo="Lo reportado y lo medido: verificación independiente de las cifras de desempeño y regla simple para reportarlas (script, muestra, intervalo).",
        preprint=dict(modo="existente", scan="CamScanner 26-10-26 11.02 (1).pdf", trans=TRANS_GUERRA, aprox=False),
        conecta="Tu preprint reconoce que los indicadores (30 fps, 94,2 %, 38 ms) son «reportados» y que hace falta comprobarlos. Tu artículo hace esa comprobación: reproduce el 8 %, mide la latencia y el optimizador, explica por qué el 94,2 % no es reproducible y lista seis discrepancias.",
        notas=["Tu preprint está **fechado el 26 de octubre de 2026** y dice «Proyecto integrador dos»: corresponde al corte anterior. Si el docente exige un preprint del Corte 3 con PRISMA y formulación, conviene reescribirlo o complementarlo.",
               "Tus referencias (Cuervo et al., 2022; Lam, 2024) no están entre las 21 del artículo; **verifica sus DOI** antes de usarlas.",
               "Las cifras de 30 fps, 94,2 % y 38 ms las usas como «reportadas»; el artículo no afirma que sean falsas."],
        defensa=[("¿La cifra de 94,2 % es falsa?", "No la declaro falsa: no puedo reproducirla ni compararla porque no está documentado el protocolo (qué señas, cuántas pruebas, qué perturbaciones)."),
                 ("¿Qué sí pudiste reproducir?", "El 8 % de notas falsas: 8,0 % (51 de 640), estable en 30 semillas (media 7,5 %; 6,1–9,2 %)."),
                 ("¿Por qué la latencia medida difiere de 2,3 ms?", "Medí en otro equipo y solo el descriptor y el clasificador (0,89 ms por fotograma); no sé si el 2,3 ms tenía el mismo alcance."),
                 ("¿Cuál es tu regla de reporte?", "Toda cifra debe indicar el script que la produce, el tamaño de muestra y su intervalo de confianza."),
                 ("¿Qué discrepancias hallaste?", "Seis: fotogramas de suelta, ventana mínima, tamaño del repositorio, pares de señas, aceleración progresiva inexistente y desglose del 8 %. Prevalece el código.")]),
}
