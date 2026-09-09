# Informe bibliométrico del corpus recolectado

**Proyecto:** Hand Sing Kids — aprendizaje musical adaptativo para niños (3–12 años)
**Fecha de análisis:** 2026-09-09
**Fuente:** 226 archivos cargados en `02_Base_de_investigacion/70_documentos/por_clasificar/`
(218 PDF sueltos + 4 ZIP de Scopus con 8 PDF).
**Corpus único:** **189 documentos** (37 archivos eran copias byte-a-byte).

---

## 0. Alcance y advertencia metodológica

Este informe describe **la colección de textos completos que se descargó a mano**: una
**muestra de conveniencia** obtenida al ejecutar las dos ecuaciones de Scopus del proyecto
(ver `07_Ecuaciones_booleanas/Scopus/ecuaciones_scopus.md`) y añadir artículos de método
(revisiones sistemáticas y estudios bibliométricos de temas contiguos).

**No es una bibliometría formal de la búsqueda.** Los indicadores clásicos —producción real
del campo, co-citación, acoplamiento bibliográfico, redes de coautoría, mapas VOSviewer/
Biblioshiny— requieren el **export CSV "All available information" + BibTeX de Scopus** con
*todos* los registros de cada ecuación, depositado en `04_Datos/bibliometria/raw/`
(hoy vacío). Los 4 ZIP solo traían PDFs, no metadatos.

Lo que sí permite este corpus: catalogar y clasificar las fuentes, describir su
composición (año, país, tipo, tecnología, dominio) y alimentar el marco teórico / estado
del arte del Capítulo 2 con lectura de texto completo.

---

## 1. Composición del corpus

| Dimensión | Resultado |
|---|---|
| Documentos únicos | 189 |
| Rango temporal | 2017–2026 (mediana 2026) |
| Idiomas | mayoría inglés; ~15 en español, algunos en indonesio/portugués/alemán |
| Acceso | casi todo open access / early-access |

### 1.1 Producción por año (`01_produccion_anio.png`)

| Año | 2017 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|---|---|---|
| Docs | 1 | 2 | 2 | 6 | 17 | 49 | **112** |

El 85 % del corpus es de 2025–2026. Refleja tanto la juventud del tema (IA en educación
musical) como el sesgo de recolección hacia lo más reciente. Varios 2026 son *in press*.

### 1.2 Tipo de documento (`02_tipo_documento.png`)

| Tipo | n | % |
|---|---|---|
| Revisión sistemática | 51 | 27.0 |
| Propuesta técnica / modelo | 44 | 23.3 |
| Empírico / experimental | 37 | 19.6 |
| Análisis bibliométrico | 33 | 17.5 |
| Scoping review | 14 | 7.4 |
| Conceptual / ensayo | 4 | 2.1 |
| Actas / ponencia / editorial | 6 | 3.2 |

**Casi la mitad del corpus (46 %) son revisiones** (sistemáticas + scoping + bibliométricas).
Útil como estado del arte de segundo orden, pero hay poca evidencia experimental con niños.

### 1.3 País de afiliación del primer autor (`04_pais.png`)

China (61; 32 %), Malasia (23), Indonesia (19), España (11), Perú (8), Tailandia (6),
Corea del Sur (6), Turquía (5). **China + Sudeste Asiático concentran ~60 %** de la
producción; la investigación iberoamericana (España, Perú, Colombia, Ecuador, México) suma
~20 % y aporta la mayor parte de los estudios empíricos escolares y en español.

### 1.4 Autores recurrentes (`07_autores_recurrentes.png`)

Apellidos de primer autor muy frecuentes (Li 9, Wang 8, Liu 7, Zhang 6) — probablemente
**personas distintas** (apellidos chinos comunes); no debe leerse como productividad
individual. Caso claro de autor real recurrente: **C. A. N. Mazlan** (Univ. Pendidikan
Sultan Idris, Malasia), 4 documentos de revisión sobre IA / microaprendizaje / turismo en
educación musical — nodo a vigilar en la bibliometría formal.

---

## 2. Contenido: tecnología y dominio

### 2.1 Categoría tecnológica dominante (`05_tecnologia.png`)

| Categoría | n | % |
|---|---|---|
| (sin tecnología específica / otro) | 52 | 27.5 |
| Método bibliométrico (VOSviewer, Biblioshiny…) | 27 | 14.3 |
| IA generativa / LLM / GAN | 18 | 9.5 |
| Deep learning (CNN / RNN / Transformer) | 17 | 9.0 |
| Apps móviles / plataformas / TIC | 17 | 9.0 |
| **Visión por computador / pose / gesto** | **14** | **7.4** |
| Realidad virtual / aumentada / XR | 11 | 5.8 |
| **Aprendizaje por refuerzo (RL / DRL)** | **8** | **4.2** |
| Multimodal / afectivo | 6 | 3.2 |
| Sistemas de recomendación / rutas / ITS | 6 | 3.2 |
| Audio / MIR / procesamiento de señal | 5 | 2.6 |
| Wearables / sensores | 4 | 2.1 |
| Gamificación / juegos serios | 4 | 2.1 |

Los dos pilares tecnológicos del proyecto **sí tienen literatura reciente propia**:
14 documentos de visión/pose/gesto aplicada a música y 8 de aprendizaje por refuerzo para
educación musical, casi todos de 2026.

### 2.2 Dominio / área (`06_dominio.png`)

| Categoría | n | % |
|---|---|---|
| Educación musical (general / superior / secundaria) | 45 | 23.8 |
| Educación general / superior (no musical) | 42 | 22.2 |
| Otro | 38 | 20.1 |
| Música tradicional / patrimonio / etnomusicología | 15 | 7.9 |
| Piano / teclado | 11 | 5.8 |
| Canto / educación vocal / coral | 10 | 5.3 |
| Música y bienestar / cognición / salud | 10 | 5.3 |
| **Educación musical infantil / preescolar** | **8** | **4.2** |
| Generación / transcripción / MIR de música | 7 | 3.7 |
| Instrumento de cuerda / arco | 3 | 1.6 |

**Brecha principal:** solo 8 documentos (4 %) tratan explícitamente educación musical
**infantil o preescolar**, y de esos muy pocos combinan niños + tecnología de interacción.
El grueso del trabajo con IA se hace en **educación superior / conservatorio** (piano,
canto, teoría). Esto confirma el hueco que el proyecto pretende ocupar.

### 2.3 Palabras clave de autor más frecuentes (`08_keywords.png`)

`music education` (26), `artificial intelligence` (19), `bibliometric analysis` (10),
`scoping review` (8), `systematic review` (7), `higher education` (6), `machine learning` (5),
`deep learning` (5), `augmented reality` (4), `creativity` (3), `AI literacy` (2).

---

## 3. Relación con el proyecto (cribado A/B/C/D)

Cada documento se etiquetó según su utilidad para Hand Sing Kids:

| Tier | Definición | n | % |
|---|---|---|---|
| **A — Núcleo** | Visión/gesto/manos + música · aprendizaje musical adaptativo con RL/ITS/gemelo digital · feedback en tiempo real de la práctica · música infantil + tecnología | **22** | 11.6 |
| **B — Relevante** | IA/tecnología en educación musical (feedback, evaluación, personalización, recomendación), apps musicales, RA/RV en música | 65 | 34.4 |
| **C — Método / contexto** | Revisiones y bibliometrías de IA en educación no musical, método bibliométrico, RV/RA/gamificación en educación general, neurociencia educativa | 61 | 32.3 |
| **D — Marginal** | Temas alejados (música y cerdos, biomecánica del tango, consultoría, TikTok, breakdance…) | 41 | 21.7 |

**87 documentos (A+B) son directamente aprovechables** para el marco teórico y el estado
del arte. Los 41 "D" pueden archivarse; entraron por la amplitud de las ecuaciones.

### 3.1 Año × relación (`10_anio_x_relacion.png`)

| Año | A | B | C | D |
|---|---|---|---|---|
| 2024 | 1 | 4 | 10 | 2 |
| 2025 | 1 | 11 | 17 | 20 |
| 2026 | 20 | 48 | 29 | 15 |

**Los 22 documentos del núcleo son casi todos de 2026** → el objeto del proyecto está en
plena emergencia; hay margen para publicar.

---

## 4. Los 22 documentos del núcleo (Tier A)

| id | Año | Autor | Tecnología | Tema |
|---|---|---|---|---|
| 032 | 2026 | Li | RL | Marco de evaluación adaptativa con RL para educación musical personalizada |
| 037 | 2026 | Cherdchoo | IA+RA+RL | THAI-MUSE: aprendizaje adaptativo de música tradicional con feedback en tiempo real |
| 038 | 2026 | Deng | IA + MediaPipe | Feedback de piano con IA: precisión técnica y autonomía (cuasi-exp. N=240) |
| 044 | 2026 | Deng | ML multimodal | Sistema de educación musical sensible a la emoción (AEMES) |
| 046 | 2026 | Shi | MoE + NeRF | Computación afectiva para música **preescolar** (120 niños) |
| 050 | 2026 | Lu | Visión por computador | Reconocimiento de postura/gesto de ejecución del guzheng (ResNet50) |
| 056 | 2026 | Rui | IA / digital | Scoping review: IA para lectura a primera vista al piano |
| 065 | 2026 | Zhang | ML multimodal (voz+música+**gesto**) | Evaluación multimodal de la enseñanza de música folclórica |
| 075 | 2026 | Li | Deep RL (MDP) | Rutas de aprendizaje musical personalizadas con DRL |
| 077 | 2026 | Li | DNN + atención | Planificación y optimización de rutas de aprendizaje musical |
| 082 | 2025 | Solórzano | Videojuegos educativos | Diseño de personajes para juegos musicales infantiles (MIDI-Musical) |
| 118 | 2026 | López Calatayud | Software de entonación en tiempo real | Motivación en viola/violín con Plectrus — **4 niños de 10–11 años** |
| 123 | 2026 | Yamada | Audio + **esqueleto de mano** | Transcripción musical multimodal de piano (HandSkeletonNet) |
| 124 | 2026 | Li | GAN multimodal audio-visual | Corrección de digitación de piano y expresividad |
| 129 | 2026 | Wang | Deep RL + RAG | Evaluación de la enseñanza musical con DRL multimodal (MMTES) |
| 144 | 2026 | Chuluunsaikhan | Deep learning / visión | Detección del teclado de piano en vídeo real |
| 152 | 2026 | Yang | Transformer multimodal | Detección fina de errores en la interpretación pianística |
| 164 | 2026 | Tang | Deep RL (PPO) + CNN | RL para la interacción en la enseñanza musical |
| 203 | 2024 | Yi | IA (robots, DL) + bibliometría | Revisión de tecnologías de IA en **educación infantil temprana** |
| 220 | 2026 | Ramoneda | Modelos de lenguaje musical | Generación de ejercicios de lectura a primera vista según dificultad |
| 222 | 2026 | Prasanna | Nanogenerador / interfaz gestual | Interfaz musical controlada por gesto (transductor mecano-eléctrico) |
| 226 | 2026 | Deng | BiLSTM + atención | IA para la expresividad emocional al piano (RCT N=290) |

Estos 22 son la **cola de lectura profunda** (ver fichas en `../../02_Base_de_investigacion/Resumenes/`).

---

## 4bis. Metadatos enriquecidos (Crossref + OpenAlex)

Se recuperaron metadatos por DOI de **167 de los 189** documentos (170 vía Crossref+OpenAlex;
14 sin DOI; 5 resueltos por título). Salidas en `04_Datos/bibliometria/processed/`
(`metadatos_enriquecidos.csv`, `corpus.bib`, `referenced_works.json`).

### 4bis.1 Revistas / fuentes (`11_revistas.png`)

| Revista | docs |
|---|---|
| Scientific Reports | 10 |
| Int. J. Computer Information Systems and Industrial Management Applications | 8 |
| Discover Artificial Intelligence | 8 |
| Acta Psychologica | 5 |
| Música Hodie · IJ ICT · Applied Sciences · SAGE Open · Frontiers in Psychology | 4 c/u |
| Discover Education · Frontiers in Education | 3 c/u |

Concentración en **mega-revistas / vías rápidas** (Scientific Reports, Discover AI, IJCISIM,
Cerebration Science Publishing): ~30 documentos. Conviene **filtrar por calidad de fuente**
(cuartil, indexación) antes de citar; varias de estas tienen dudas de rigor editorial.

### 4bis.2 Citas (`12_citas_top.csv`, `12_citas_por_tier.csv`)

- Total del corpus: **1 245 citas** (OpenAlex). **128 de 189 documentos tienen 0 citas.**
- Media 6,6 / **mediana 0** — muy sesgada por unos pocos.

| Tier | docs | citas totales | media | mediana |
|---|---|---|---|---|
| A – Núcleo | 22 | 86 | 3,9 | 0 |
| B – Relevante | 65 | 67 | 1,0 | 0 |
| C – Método/contexto | 61 | 279 | 4,6 | 0 |
| D – Marginal | 41 | **813** | 19,8 | 0 |

**El núcleo (A) casi no acumula citas porque es de 2026.** Las citas se concentran en
documentos viejos y periféricos (D): Matallaoui 2017 sobre exergamification (740),
Bosman 2024 audio en RV (83), Yi 2024 IA en educación infantil (78 — el más citado del núcleo).

### 4bis.3 Países (OpenAlex, `13_paises_openalex.png`)

CN 54 · MY 27 · ID 12 · ES 11 · TH 8 · KR 8 · US 8 · TR 6 · PE 6 · CO 4 · IT 4.
**39 documentos con colaboración internacional** (>1 país entre los autores).

### 4bis.4 Base intelectual del corpus — co-citación (`14_cocitacion_base.csv`)

43 obras están citadas por ≥3 documentos del corpus. Se dividen en:

- **Andamiaje metodológico:** *PRISMA 2020* (14 docs), *Arksey & O'Malley — scoping* (8),
  *Donthu 2021 — How to conduct a bibliometric analysis* (4), comparativas WoS/Scopus.
- **Núcleo temático (IA + educación musical):**
  - *Developments and Applications of AI in Music Education* (Technologies, 2023) — 7 docs
  - *AI-Assisted Music Education: A Critical Synthesis of Challenges and Opportunities* (Educ. Sci., 2024) — 5
  - *The Usage of AI Technology in Music Education System Under Deep Learning* (IEEE Access, 2024) — 5
  - *Zawacki-Richter et al. 2019 — AI applications in higher education: where are the educators?* — 4
  - varios *Scientific Reports* 2024-2025 sobre enseñanza musical con DL/RNN — 4 c/u

→ El corpus se apoya en **un puñado de revisiones-paraguas de 2023-2024** sobre IA en
educación musical. Son las lecturas obligadas para el marco teórico (conviene conseguirlas;
no están todas entre los 189).

### 4bis.5 Acoplamiento bibliográfico (`15_acoplamiento_edges.csv`, `15_acoplamiento_red.png`)

72 pares de documentos comparten ≥2 referencias. Clústeres visibles:

- **DRL / rutas de aprendizaje musical:** 077 ↔ 164 ↔ 055 (+ 129) — literatura que el
  proyecto debe dominar para las Fases 7-11.
- **IA en piano:** 180 ↔ 226 ↔ 057 — feedback y evaluación pianística con IA.
- **Separación de fuentes / MIR:** 031 ↔ 104.
- **Metaverso en educación:** 200 ↔ 208.

---

## 5. Hallazgos para el proyecto

1. **El tema está caliente y es nuevo.** Casi toda la literatura del núcleo es de 2026;
   el proyecto llega a tiempo.
2. **Los dos pilares técnicos están cubiertos por separado** (visión/gesto en música: 14;
   RL en educación musical: 8) pero **casi nadie los integra en un sistema completo** para
   niños. Ese es el hueco.
3. **Feedback en tiempo real de la práctica instrumental con visión/MediaPipe** ya está
   validado en piano (038, 226) y guzheng (050) — hay base metodológica y de comparación.
4. **RL para selección de actividad / evaluación adaptativa** en música: 032, 075, 077,
   129, 164 — referencias directas para las Fases 7 y 11 del proyecto.
5. **Población infantil apenas explorada** (8 docs; solo 046, 082, 118, 203 combinan niños
   + tecnología). Contribución diferencial clara.
6. **MILP / optimización matemática de la secuencia didáctica: ausente** en el corpus. El
   uso de programación entera mixta (Fase 7) sería aportación original — conviene ampliar
   la búsqueda con términos de investigación operativa + educación.
7. **Gemelo digital educativo:** solo aparece en ergonomía instrumental (105) y biomecánica
   (091), nunca como gemelo del alumno. Otro hueco.

## 6. Próximos pasos recomendados

- [x] Metadatos de los 189 recuperados de Crossref + OpenAlex (167/189) → `processed/`.
- [ ] Exportar de Scopus el **CSV completo + BibTeX** de cada ecuación → `raw/` y correr la
      bibliometría formal del *universo de la búsqueda* (Biblioshiny / VOSviewer): producción
      real del campo, co-citación completa, revistas núcleo (Bradford), redes de coautoría.
- [ ] Conseguir las 3-4 revisiones-paraguas de la base intelectual (§4bis.4) que no están
      entre los 189 y ficharlas.
- [ ] Filtrar el corpus por calidad de fuente (cuartil / indexación) antes de citar.
- [ ] Añadir una **3.ª ecuación** que cruce *(reinforcement learning OR mixed-integer OR
      "digital twin" OR "intelligent tutoring") AND ("music education" OR "instrument
      learning") AND (child* OR primary)* para el subconjunto infantil.
- [ ] Leer y fichar los 22 del Tier A (en curso) y los ~30 "B" más citables.
- [ ] Revisar y pulir los títulos autogenerados de la matriz (columna `titulo`).
- [ ] Verificar posibles solapamientos entre los 8 PDF de los ZIP y descargas sueltas por DOI.

---

## Archivos generados

| Archivo | Contenido |
|---|---|
| `../../02_Base_de_investigacion/Matriz_bibliografica/matriz_bibliografica.csv` | Matriz completa: 189 filas × (id, archivo, año, autor, país, título, tipo, tecnología, dominio, población, relación A/B/C/D, keywords, DOI, abstract) |
| `resultados/matriz_enriquecida.csv` | Igual + categorías tecnológica y de dominio |
| `resultados/0*.csv` y `0*.png` | Tablas y figuras de cada dimensión |
| `resultados/10_anio_x_relacion.*` | Cruce año × relación |
| `analisis_corpus.py` · `analisis_citas.py` | Scripts reproducibles (usan `.venv/Scripts/python.exe`) |
| `processed/metadatos_enriquecidos.csv` | Metadatos Crossref + OpenAlex (autores, afiliaciones, países, revista, ISSN, citas, referencias, licencia, financiación) |
| `processed/corpus.bib` | BibTeX del corpus para Zotero / Mendeley |
| `processed/referenced_works.json` | Obras citadas por cada documento (OpenAlex) |
| `resultados/11..15_*` | Revistas, citas, países OpenAlex, co-citación, acoplamiento |
| `../../02_Base_de_investigacion/70_documentos/por_clasificar/_duplicados_exactos/` | 37 copias exactas retiradas |
| `../../02_Base_de_investigacion/70_documentos/por_clasificar/_scopus_zips/` | 4 ZIP originales de Scopus |
