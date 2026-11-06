# Prompt para Antigravity: Cierre del Proyecto, Corte 3 (Gestión Tecnológica)

## Antes de pegar (completar y borrar esta sección)

1. Abrir en Antigravity la carpeta del proyecto `HandSingKids` (la que contiene `docs/documento_tecnico.md`, `tests/` y `handsingkids/`). El agente debe leer el código y los documentos desde ahí, no desde lo que resume este prompt.
2. Completar los campos entre corchetes en la sección "Datos del equipo". Sin la transcripción del preprint y las cifras PRISMA, el agente no puede garantizar coherencia entre el manuscrito a mano y el artículo.
3. Dejar en la misma carpeta (por ejemplo `entrega_corte3/insumos/`): el escaneo del preprint, los cuatro documentos del corte (rúbrica, guía, instrucciones y publicación de Teams) y, si ya la tienen, la plantilla de la revista.

---

## PROMPT (copiar desde aquí)

### 0. Rol y objetivo

Actúa como asistente de investigación en ingeniería industrial y gestión tecnológica. Vas a preparar, junto conmigo, los entregables finales del Tercer Corte de la asignatura Gestión Tecnológica (código 8830 0048 0), UPB Seccional Montería, periodo 2026-2, docente M.Sc. Cristian Javier Cano Mogollón.

El resultado final es un artículo científico maquetado en la plantilla de una revista indexada, más la documentación de soporte, empaquetado según las reglas de entrega. Trabaja por fases, deja un plan revisable antes de ejecutar y detente en los puntos de control indicados.

### 1. Datos del equipo (completar)

- Equipo: `[NN]`
- Integrantes (nombre completo, correo institucional, ORCID si tienen): `[...]`
- Fecha límite de entrega en Teams: `[...]`
- Revista objetivo, si ya hay una elegida: `[...]` (si está vacío, la eliges tú en la Fase 1 con mi aprobación)
- Idioma del artículo: el que exija la revista; por defecto español con resumen en inglés.
- Transcripción del preprint manuscrito (ya está hecho y escaneado, no hay que rehacerlo): `[pegar aquí el texto, o apuntar al PDF en entrega_corte3/insumos/]`
- Cifras del flujo PRISMA del preprint (registros identificados, duplicados eliminados, cribados, excluidos, evaluados a texto completo, incluidos; bases de datos y ecuación booleana): `[...]`

El artículo debe ser coherente con el preprint en título, problema, formulación y cifras PRISMA. Si encuentras una discrepancia entre el preprint y el código o la documentación, no la resuelvas por tu cuenta: repórtala.

### 2. Qué se evalúa (resumen de la rúbrica)

Componente 1, 60% del corte. Los criterios que te competen son estos:

| Criterio | Peso | Lo que cuenta como excelente |
|---|---|---|
| Preprint manuscrito + PRISMA | 15% | Ya entregado por el equipo. No lo toques. |
| Certificado Turnitin | 15% | Similitud ≤ 15% (el corte aprobatorio es ≤ 20%), sin bloques extensos de una misma fuente (máximo 2% por fuente), excluyendo bibliografía y citas textuales. |
| Artículo maquetado y co-autoría | 20% | Plantilla oficial de la revista, estructura IMRyD impecable, docente incluido como co-autor con la filiación exacta. |
| Constancia de envío | 10% | Acuse oficial del portal editorial (OJS, Editorial Manager o ScholarOne) con radicado, fecha, título y autores. |

Condición de habilitación: no se puede enviar a la revista sin el Turnitin aprobado (≤ 20%) y sin la revisión del docente sobre su vinculación. El orden es: artículo, Turnitin, visto bueno del docente, envío.

Componente 2 (40%) es una prueba presencial individual tipo Saber Pro sobre la lectura "Transformación Digital en las PYMES de Montería, Colombia: Retos, Avances y Perspectivas" (Llanos Ayola, 2025). No es parte de este trabajo, salvo la fase opcional 8.

### 3. Reglas innegociables

1. **No fabricar evidencia.** El Turnitin y la constancia de envío los genera un tercero (la institución y la revista). Tú no los produces, no los simulas ni dejas archivos que parezcan serlo. Para esos dos entregables preparas únicamente guías, metadatos y marcadores de posición claramente rotulados "PENDIENTE: lo emite Turnitin / lo emite la revista".
2. **No inventar resultados.** Toda cifra del artículo sale de una ejecución que tú hagas sobre el código del repositorio, o de la documentación del proyecto citando la sección. El sistema no se ha probado con niños reales; el artículo debe decirlo en las limitaciones, no insinuar lo contrario.
3. **No inventar referencias.** Cada referencia se verifica por DOI o URL (Crossref, Scopus, Google Scholar o el sitio de la revista) antes de entrar a la bibliografía. Si no la puedes verificar, no la incluyas. Entrega un archivo `verificacion_referencias.csv` con la fuente de verificación de cada una.
4. **No inventar datos de contexto regional.** Para Montería y Córdoba usa solo fuentes que puedas abrir y citar (DANE, MinEducación, MinTIC, secretarías, estudios publicados). Si no hay un dato verificable, formula la motivación como justificación del equipo, sin estadísticas.
5. **No afirmar la indexación de una revista de memoria.** Verifica categoría vigente en Publindex/MinCiencias o cuartil en Scopus/SCImago el mismo día, y guarda la captura o el enlace como evidencia en la ficha.
6. **Honestidad técnica.** Si algo del sistema no está implementado, o está implementado pero sin validar, se describe así.

### 4. Dossier del proyecto: Hand Sing Kids

Fuente primaria: `docs/documento_tecnico.md` y el código. Lo siguiente es solo el mapa; confírmalo contra el repositorio.

**Qué es.** Aplicación de escritorio en Python (PySide6, OpenCV, MediaPipe) que enseña música a niños pequeños mediante señas de las manos (una seña por nota, Do3 a Do4, ocho notas, dos manos, calibración por niño). Corre en macOS, Python 3.10 a 3.12.

**Tamaño y pruebas (primera entrega).** 8.599 líneas en 44 módulos más 999 de pruebas; doce pantallas; cinco baterías de prueba. Desde entonces hubo ocho iteraciones de ajustes (ver `docs/documento_tecnico.md`, secciones 11.1 a 11.7). Vuelve a contar y vuelve a ejecutar; no copies estas cifras sin comprobarlas.

**Componentes.**

- **Visión.** Descriptor invariante de 120 componentes (curvatura de dedos, apertura, distancias del pulgar, normal de la palma, dirección, forma normalizada, geometría entre manos); clasificador por vecino más cercano con confianza calibrada y margen; estabilizador temporal con periodo refractario (`vision.stabilizer`, ventana por defecto de un fotograma, `release_frames = 6`).
- **Música.** Notas y efectos sintetizados con numpy; tres capas de sonido con prioridad (sintetizado, `ui/assets/audio/`, `sonidos_personalizados/`).
- **Aprendizaje.** Dominio en cuatro componentes; repaso espaciado tipo SM-2; motor adaptativo por reglas con escalera de ayuda; `MasteryPredictor` logístico que pasa a entrenarse por descenso de gradiente con los intentos propios de cada niño desde unos 40 intentos y se reentrena cada 20; generador de actividades dirigidas a las notas más débiles.
- **Optimización.** Selección de la sesión como problema entero mixto (MILP), resuelto con CBC y, como respaldo, enumeración exhaustiva (óptimo exacto).
- **Módulo Canciones.** Motor por reloj de pared (`learning/rhythm.py`, `RhythmRunner`) con ventana de acierto asimétrica, tres velocidades, combo (+0,5 cada 10 aciertos, techo 4,0), tolerancia a la seña equivocada con reintento dentro de la ventana, 19 canciones (melodías tradicionales o de dominio público, solo la melodía, nunca la letra).
- **Interfaz.** Sistema de diseño traducido a Qt, mascota vectorial (nombre "Kiki", aún sin confirmar), ilustraciones de gestos y señas del propio niño.

**Hallazgos medidos que sustentan el artículo (verificar re-ejecutando `tests/test_vision.py` y compañía).**

- El método de la versión 1 (similitud coseno sobre coordenadas crudas, umbral 0,65) dispara una nota en el 100% de las posturas que no son seña (transiciones, manos cruzadas). El método nuevo lo baja al 8%.
- Con la calibración real del proyecto, 30 de los 56 pares de notas distintas superan el umbral de la v1; Si y Do agudo llegan a 0,902 de similitud.
- Corrección documentada: el sonido duplicado de la séptima iteración se debía a que, con ventana de un fotograma, un parpadeo del rastreo hacía que el mecanismo de "soltar" liberara la seña y la misma nota sonara otra vez.
- Corrección documentada: la aceleración progresiva atribuida a la v0 nunca existió (velocidad constante en `NoteSprite`).

**Limitaciones que el artículo debe declarar.**

- No se ha probado con niños; todo es evaluación técnica de laboratorio.
- El reconocimiento se probó con una sola calibración de ocho señas.
- Las constantes (pesos del dominio, umbral 0,80, p\* = 0,75, ventanas de acierto) vienen de la literatura y del ajuste sobre datos disponibles, no de un estudio con niños.
- El reconocimiento instantáneo acepta un 8% de falsos positivos en posturas de transición, un compromiso a favor de la respuesta inmediata.
- Las canciones son transcripciones simplificadas a escala diatónica en el rango de ocho notas.
- No hay aprendizaje por refuerzo; las interfaces para ML y RL son documentadas pero sin datos reales que las alimenten.

**Nivel de madurez (TRL).** Propón y justifica un TRL con evidencia del repositorio. Mi hipótesis de partida es TRL 4 (validación de componentes en laboratorio), porque no hay validación con usuarios reales. Si la evidencia dice otra cosa, dilo; el equipo confirma el nivel final.

**Marco regional.** El proyecto debe enmarcarse como solución de base tecnológica con pertinencia para Montería y Córdoba (educación musical y tecnología educativa en primera infancia). Antes de redactar la introducción, confírmame con una pregunta corta que esta es la EBT que el equipo va a presentar; si el equipo tiene otra EBT, detente.

### 5. Fases

**Fase 0. Lectura y plan (punto de control 1).**
Lee los cuatro documentos del corte, el preprint y el repositorio. Entrega un plan en un artefacto con: inventario de lo que encontraste, huecos de información, discrepancias, y el cronograma hacia atrás desde la fecha límite (considera que el Turnitin y la revisión docente son pasos secuenciales antes del envío). Espera mi aprobación.

**Fase 1. Selección de revista y ficha técnica (punto de control 2).**
1. Con navegador, identifica 3 candidatas indexadas en Publindex (A1, A2, B o C) o Scopus/WoS (Q1 a Q4) cuyo alcance (aims and scope) cubra gestión tecnológica, ingeniería con enfoque educativo o tecnología para educación. La guía menciona como ejemplos Revista UIS Ingenierías, TecnoLógicas, DYNA e Ingeniería y Competitividad; úsalas solo si el alcance realmente encaja, y no te limites a ellas.
2. Para cada candidata: categoría o cuartil vigente con evidencia, alcance, idioma, tipos de artículo, extensión máxima, estilo de referencias, política de preprints, costos de procesamiento (APC) y si cobra por enviar, tiempos medios de revisión, plataforma de envío, enlace a la guía para autores y a la plantilla.
3. Recomienda una con justificación y descarta explícitamente las otras. Espera mi confirmación.
4. Con la elegida, descarga la plantilla oficial y guarda las guías en `entrega_corte3/revista/`.
5. Genera `Ficha_Revista_Indexada_Equipo[NN].pdf`: enlace oficial, indexación con fecha de consulta, alcance, políticas editoriales y justificación de la elección.

**Fase 2. Evidencia técnica reproducible.**
1. Ejecuta todas las pruebas del repositorio y registra salidas y versiones (Python, librerías, sistema).
2. Reproduce las mediciones del apartado de hallazgos con scripts guardados en `entrega_corte3/analisis/`. Para cada tasa (por ejemplo el 8%) reporta el tamaño de muestra y un intervalo de confianza de Wilson al 95%. Si el tamaño de muestra no permite concluir mucho, dilo.
3. Genera una matriz de similitud 8 × 8 de la calibración real, con la comparación entre el método de la v1 y el actual.
4. Reporta cualquier prueba que falle o cualquier cifra que no coincida con la documentación.

**Fase 3. Revisión sistemática y marco conceptual.**
Reconstruye el flujo PRISMA con las cifras del preprint, como diagrama vectorial limpio (Figura PRISMA, formato 2020 adaptado a las cuatro fases: identificación, cribado, elegibilidad, inclusión). No cambies ninguna cifra. Con los artículos incluidos, construye una tabla comparativa de trabajos relacionados (reconocimiento de gestos de mano en educación musical, solfeo con manos tipo Curwen-Kodály, sistemas tutoriales adaptativos, repaso espaciado, juegos rítmicos). Si el equipo no entregó la lista de artículos incluidos, pídela; no la reconstruyas por tu cuenta.

**Fase 4. Redacción del artículo (punto de control 3: borrador para revisión).**
Estructura IMRyD, ajustada a lo que pida la revista:

1. Título (español e inglés), resumen estructurado (≈150 a 250 palabras según la revista), palabras clave.
2. Introducción: problema, brecha identificada en la revisión, objetivo y contribuciones (máximo tres, verificables).
3. Revisión de literatura / trabajos relacionados (apoyada en PRISMA).
4. Método:
   - Arquitectura del sistema (figura).
   - Formulación matemática, con definición de variables e índices: descriptor de 120 componentes, clasificador con confianza y margen, estabilizador con periodo refractario, modelo de dominio y SM-2, predictor logístico con su función de pérdida y actualización por gradiente, MILP de selección de sesión (conjuntos, parámetros, variables de decisión, función objetivo y restricciones), ventana de acierto y puntaje del módulo Canciones. Toma las expresiones de `documento_tecnico.md` y verifícalas contra el código; si difieren, manda el código y repórtalo.
   - Protocolo de evaluación técnica (qué se mide, con qué datos, cuántas repeticiones).
5. Resultados: solo lo reproducido en la Fase 2, con tablas y figuras numeradas.
6. Discusión: qué significan los resultados, el compromiso de la respuesta inmediata (ventana de un fotograma y 8% de falsos positivos), la lección del sonido duplicado, amenazas a la validez y comparación con la literatura incluida. Incluye el análisis de madurez tecnológica (TRL) con evidencia y el impacto esperado para Montería y Córdoba formulado como hipótesis a validar.
7. Conclusiones y trabajo futuro (pruebas con niños, otras calibraciones, aprendizaje por refuerzo, señas de una mano).
8. Agradecimientos, declaración de uso de herramientas de IA (según exija la revista), conflicto de intereses, disponibilidad de datos y código.
9. Referencias.

**Fase 5. Maquetación en la plantilla oficial.**
- Pasa todo a la plantilla de la revista (`.docx` o LaTeX), con márgenes, tipografía, estilos de título, figuras, tablas, ecuaciones numeradas y estilo de referencias exigidos.
- Ecuaciones en notación matemática estándar (LaTeX u OMML), nunca con etiquetas HTML como `<sub>`.
- Bloque de autoría exacto:

```
Autor 1: [Nombre] - Universidad Pontificia Bolivariana, Seccional Montería
Autor 2: [Nombre] - Universidad Pontificia Bolivariana, Seccional Montería
...
Co-Autor / Co-Investigador: M.Sc. Cristian Javier Cano Mogollón
Filiación: Docente Titular, Facultad de Ingeniería Industrial.
Grupo de Investigación en Simulación, Logística y Gestión de Operaciones (SILOGE),
Hub Industrial Solution (HIS), Universidad Pontificia Bolivariana, Seccional Montería, Colombia.
Correo: cristian.cano@upb.edu.co
```

- Si la revista exige otro formato de autoría (orden, ORCID, autor de correspondencia, contribución CRediT), adáptalo sin perder los datos del docente. Pregúntame el orden de autores si no está definido.
- Exporta a PDF y revisa visualmente cada página: figuras legibles, ecuaciones sin cortes, tablas dentro de margen.
- Guarda también el archivo editable (`.docx` o `.tex` con sus fuentes).

**Fase 6. Preparación para Turnitin (sin generarlo).**
1. Revisa el texto buscando coincidencias largas con `documento_tecnico.md`, la documentación del repositorio y las fuentes citadas. Entrega un informe con los fragmentos que debo reescribir. Esto no sustituye a Turnitin; es un filtro previo.
2. Reescribe en voz propia lo que corresponda, sin parafrasear de forma mecánica ni cambiar el sentido técnico.
3. Entrega una guía de una página para quien suba el documento: configuración (excluir bibliografía, excluir citas textuales, no excluir fuentes menores) y qué guardar (reporte PDF con desglose de fuentes, nombrado `Certificado_Turnitin_Equipo[NN].pdf`).
4. Crea un marcador de posición en la carpeta de entrega con el rótulo "PENDIENTE: lo emite Turnitin". No debe parecer un certificado.

**Fase 7. Paquete de envío (sin enviar) y ZIP.**
1. Prepara, en `entrega_corte3/envio/`, todo lo que pide el portal: título en español e inglés, resumen, palabras clave, lista de autores con filiaciones, carta de presentación (cover letter), declaraciones requeridas y archivo anonimizado si la revista es de doble ciego.
2. Entrega una lista de pasos para crear la cuenta de autor y radicar, y qué capturar como constancia (acuse con fecha, título, autores y radicado). Marcador "PENDIENTE: lo emite la revista".
3. Ensambla el ZIP `02_GT_Corte3_CierreProyecto_Equipo[NN].zip` con esta estructura:
   - `Preprint_Manuscrito_Equipo[NN].pdf` (copiar el escaneo existente, sin modificarlo)
   - `Certificado_Turnitin_Equipo[NN].pdf` (PENDIENTE hasta que exista el real)
   - `Ficha_Revista_Indexada_Equipo[NN].pdf`
   - `Articulo_Maquetado_Equipo[NN].pdf`
   - `Constancia_Envio_Revista_Equipo[NN].pdf` (PENDIENTE hasta que exista la real)
4. Verifica que los nombres coincidan exactamente y que los dos pendientes se sustituyan por los archivos reales antes de subir a Teams.

**Fase 8 (opcional, solo si lo pido).** Guía de estudio para la prueba tipo Saber Pro a partir del material de `05_Tarea_tercer_corte/prueba_tipo_Ecaes/` y la lectura de Llanos Ayola (2025): mapa conceptual de adopción tecnológica, escalas TRL, innovación abierta y modelos de negocio EBT, y un banco de preguntas SMUR de práctica. Usa únicamente el material que yo adjunte.

### 6. Estilo de escritura

- Español con ortografía impecable. Si el artículo va en inglés, inglés técnico claro.
- Normas APA 7 por defecto en documentos propios; en el artículo, el estilo que fije la revista.
- Jerarquía de títulos clara, citas en el texto con su referencia correspondiente.
- Prosa directa, concreta y sin adornos. Evita valoraciones del tipo "considerable riqueza", "innovador enfoque" o "paisaje cada vez más complejo", adjetivos sin respaldo y frases de relleno. Cada párrafo avanza la idea y no la repite.
- Mantén la voz natural del equipo: oraciones de longitud variada, sin muletillas de redacción automática (tríadas forzadas, "es importante destacar que", cierres de párrafo que repiten lo dicho). La tarea busca autoría reflexiva y el texto debe sonar a persona que conoce su sistema.
- Las cifras llevan unidades y tamaño de muestra. Las afirmaciones causales se sostienen con evidencia o se formulan como hipótesis.

### 7. Verificación final (antes de darme el paquete)

Comprueba y reporta, con evidencia, cada punto:

- Los títulos, el problema, la formulación y las cifras PRISMA coinciden con el preprint.
- Cada cifra del artículo tiene un script o una salida de prueba que la respalda.
- Las ecuaciones del artículo coinciden con el código.
- Cada referencia está verificada (archivo CSV) y cada cita en el texto tiene su referencia, y viceversa.
- El artículo cumple la plantilla y los límites de la revista (extensión, resumen, figuras).
- El bloque de coautoría del docente está completo y exacto.
- Los nombres de archivo coinciden con la nomenclatura del curso.
- Quedan solo dos pendientes y están claramente rotulados.

### 8. Formato de tus reportes

Al terminar cada fase, entrega un resumen corto: qué hiciste, dónde quedó cada archivo, qué decisiones necesitas de mí y qué riesgos detectaste. Sin recapitular los pasos internos.
