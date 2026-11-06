# PREPRINT NUEVO 4 — Enfoque: optimización (la sesión como problema de programación entera mixta)

**Estructura de referencia:** formato corto con resumen, introducción, formulación del modelo, resultados, límites y cierre, con las variables y restricciones definidas (la rúbrica pide formulación matemática). Extensión: unas 480 palabras, cerca de 2 páginas manuscritas.
**Integrante:** Angel Quintana Jiménez

---

## ESCRITO FINAL (para copiar a mano)

**Elegir la sesión óptima: programación entera mixta para planificar las actividades de Hand Sing Kids**

Angel Quintana Jiménez. Universidad Pontificia Bolivariana, seccional Montería, Ingeniería Industrial. Gestión Tecnológica, tercer corte. 6 de noviembre de 2026.

**Resumen.** Después de cada intento, Hand Sing Kids debe decidir qué actividades forman la siguiente sesión de práctica de las ocho notas, de Do3 a Do4. Planteamos esa decisión como un problema de programación entera mixta: se maximiza una mezcla de ganancia de aprendizaje, urgencia de repaso y motivación, menos la fatiga, sujeta a restricciones pedagógicas. Se resuelve con el solucionador CBC y se verifica con una enumeración exacta. La prueba pasó y la sesión de ejemplo se resolvió en 40 ms. Los pesos son decisiones de diseño y no hay datos de niños.

**Introducción.** Armar una sesión no es elegir las actividades más atractivas una por una. Hay un tiempo máximo, un número fijo de actividades, prerrequisitos entre habilidades, y conviene que haya algo lúdico y que se atienda un repaso vencido. Una regla simple puede romper alguna de esas condiciones o perder una combinación mejor. En la literatura de educación musical con IA, estas decisiones suelen aprenderse con refuerzo a partir de datos; nosotros no tenemos datos de niños y preferimos una formulación que el docente pueda leer.

**Modelo.** Sea A el conjunto de actividades candidatas, S el de habilidades, G ⊆ A las actividades lúdicas y V ⊆ A las que atienden un repaso vencido. La variable de decisión es x_i ∈ {0, 1}: vale 1 si la actividad i entra en la sesión.
Objetivo: máx Σ (α1·g_i + α2·r_i + α3·m_i − α4·f_i)·x_i, donde g es la ganancia, r la urgencia de repaso, m la motivación y f la fatiga, con α = 1,00; 0,70; 0,35 y 0,55.
Restricciones: Σ d_i·x_i ≤ T_máx (tiempo); Σ x_i = K (tamaño); x_i ≤ a_i (prerrequisitos); Σ_G x_i ≥ 1 (una lúdica); Σ dif_i·x_i ≤ 0,72·K (dificultad media); a lo sumo dos actividades por habilidad; y Σ_V x_i ≥ 1 (un repaso vencido).
La ganancia concentra el valor en un éxito esperado p* = 0,75, con p_i = 1 / (1 + e^(−6(μ_i − dif_i))).

**Resultados.** El problema se resuelve con CBC mediante PuLP. Como respaldo y verificación, el sistema enumera todas las combinaciones de K actividades mientras no pasen de 4×10^5, y toma la mejor que cumple las restricciones. La prueba del repositorio que compara ambos métodos pasó. La sesión de ejemplo se resolvió con CBC en 40 ms, con valor objetivo 2,9524. La batería del optimizador terminó sin fallos.

**Discusión y límites.** «Óptimo» significa la mejor solución del objetivo que cumple las restricciones, no necesariamente la mejor sesión para aprender. Los pesos, el 0,75 y el 0,72 son decisiones de diseño y no se calibraron con niños. No hicimos un análisis de sensibilidad numérico, y la verificación cubre una sesión de ejemplo, no un barrido de casos. Si el número de combinaciones supera el umbral, la enumeración exacta deja de aplicar y queda CBC.

**Cierre.** El aporte es una selección de sesión explicable y verificable, con restricciones pedagógicas explícitas. Falta comprobar con niños si las sesiones óptimas enseñan mejor que las elegidas por un docente. Nivel de madurez: TRL 4.

**Referencia verificada**

Wilson, R. C., Shenhav, A., Straccia, M., & Cohen, J. D. (2019). The Eighty Five Percent Rule for optimal learning. *Nature Communications, 10*(1), Article 4646. https://doi.org/10.1038/s41467-019-12552-4

---

## Notas para quien lo copie

- Las cifras (40 ms, 2,9524, 0,75, 0,72, pesos, 4×10^5) salen del código y de las pruebas del repositorio.
- El 85 % de Wilson et al. da apoyo a la idea de una dificultad intermedia; el 0,75 del código es una constante de diseño, no un resultado de ese artículo.
- Lee la referencia completa antes de defenderla.
