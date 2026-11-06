# PREPRINT NUEVO 2 — Enfoque: aprendizaje adaptativo (dominio, repaso espaciado y selección de sesión)

**Estructura de referencia:** Guía 2 (tipo Guerra): encabezado, resumen, introducción con cuatro párrafos rotulados, métodos, resultados, discusión, conclusiones y referencias. Extensión: unas 650 palabras, cerca de 3 páginas manuscritas. Voz en primera persona prudente.
**Integrante:** Juliana Esther Carrascal Hernández

---

## ESCRITO FINAL (para copiar a mano)

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

## Notas para quien lo copie

- Las cifras (40 ms, 8 baterías, 78 %, 0,80/0,70/seis intentos, 0,75) salen del código y de las pruebas del repositorio; el 78 % solo es una comprobación de convergencia.
- Las cifras del DANE (535.052 y 80.254) provienen de las proyecciones municipales 2020–2035 consultadas para el artículo.
- Las dos referencias están verificadas en Crossref; léelas antes de defenderlas.
