# PREPRINT NUEVO 1 — Enfoque: visión computacional (reconocer solo la seña intencional)

**Estructura de referencia:** Guía 1 (tipo Antolin Vitola): introducción en 3 párrafos, metodología en 4, resultados en 3 y un párrafo de cierre. Extensión: unas 400 palabras, cerca de 2 páginas manuscritas.
**Integrante:** Isaías José Petro Rodríguez

---

## ESCRITO FINAL (para copiar a mano)

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

## Notas para quien lo copie

- Las cifras salen de `analisis/resultados_vision.json` (480 señas por nivel; 640 posturas; 51 errores). No las cambies sin cambiarlas también en el artículo.
- La latencia de 0,89 ms es la medida en este equipo, sin captura ni dibujo en pantalla; el documento del 2.º corte decía 2,3 ms en otro equipo.
- Este preprint no trae diagrama PRISMA ni formulación completa. Si el docente exige PRISMA dibujado, complétalo con **tus propias cifras de búsqueda**; las cifras de 437/206 de las guías son de otro proyecto y no sirven aquí.
