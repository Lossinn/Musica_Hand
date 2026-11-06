# PREPRINT NUEVO 3 — Enfoque: ingeniería de software, accesibilidad y camino hacia la validación en aula

**Estructura de referencia:** el preprint de Andrés Negrete: texto corrido en párrafos, sin secciones rotuladas, con título propio. Aquí se agrega una referencia al final. Extensión: unas 450 palabras, cerca de 2 páginas manuscritas.
**Integrante:** [por asignar]

---

## ESCRITO FINAL (para copiar a mano)

**Hand Sing Kids en el aula de Montería: una herramienta que corre en un computador común y qué falta para probarla con niños**

Hand Sing Kids es una aplicación de escritorio que enseña a los niños las ocho notas musicales de Do3 a Do4 con señas de las dos manos. Una cámara capta las manos, el sistema reconoce la seña y responde con sonido, y después decide qué actividad sigue según lo que el niño ya domina. Lo que me interesa destacar es que todo esto funciona en un computador con cámara y guarda sus datos en una base local, sin depender de una conexión a internet. Por eso creo que es una candidata realista para probarse en aulas de Montería y Córdoba, donde no siempre hay buena conectividad.

El prototipo está hecho en Python, con una interfaz en PySide6 y el seguimiento de las manos con MediaPipe. Tiene 62 módulos y unas 10.500 líneas de código, organizados en ocho baterías de pruebas, y un catálogo de 19 canciones sencillas. Las revisiones recientes de inteligencia artificial en la educación de la primera infancia muestran que el interés por estas tecnologías es grande (Yi et al., 2024), pero entre los trabajos que encontré, ninguno combina una seña manual por nota, una calibración para cada niño y una decisión de sesión resuelta de forma exacta. Esa combinación es el espacio de esta propuesta.

La evaluación hasta ahora es técnica y de laboratorio. Con una calibración de una sola persona y perturbaciones simuladas, el reconocimiento llegó a 100 % sin ruido y a 86,0 % con ruido alto. Ante 640 posturas que no son seña, disparó una nota por error en el 8,0 % de los casos, frente al 100 % del método de la versión inicial. Las ocho baterías de pruebas del repositorio terminaron sin fallos y los scripts para repetir las mediciones se pueden ejecutar con una sola orden. No se hicieron pruebas con niños, así que no puedo afirmar nada sobre el aprendizaje; el nivel de madurez tecnológica es TRL 4.

Antes de entrar a un aula hay tareas pendientes que considero tan importantes como el código. Hay que medir la latencia de extremo a extremo, incluyendo la cámara; conseguir la aprobación ética y el consentimiento de los acudientes, porque se trabaja con menores; revisar la normativa colombiana sobre tratamiento de datos personales, y decidir qué se guarda de cada niño. Propongo un piloto pequeño con un docente, medir los conocimientos antes y después, registrar las notas disparadas por error con niños reales en lugar de simularlas y recoger la opinión del docente. El valor del proyecto no depende de una cifra de precisión, sino de que sea fácil de usar, honesto sobre lo que ya probó y repetible por otros.

**Referencia verificada**

Yi, H., Liu, T., & Lan, G. (2024). The key artificial intelligence technologies in early childhood education: A review. *Artificial Intelligence Review, 57*(1), Article 12. https://doi.org/10.1007/s10462-023-10637-7

---

## Notas para quien lo copie

- Las cifras salen del artículo y de `analisis/resultados_vision.json`; 62 módulos y 10.581 líneas son del repositorio medido el 5 de noviembre.
- La frase «entre los trabajos que encontré, ninguno…» está limitada a lo que se leyó en títulos y metadatos; no la presentes como afirmación sobre toda la literatura.
- Si el docente pide más extensión, amplía el último párrafo con el protocolo del piloto.
