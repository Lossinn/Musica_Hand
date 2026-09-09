# Pedro Ramoneda a,∗, Masahiro Suzuki b, Akira Maezawa b, Xavier Serra a

- **Archivo:** `70_documentos/2026_Ramoneda_difficulty-aware-score-generation-sight-reading.pdf`
- **id matriz:** 220  |  **Relacion:** A - Nucleo
- **Autor(es):** Ramoneda et al.  |  **Ano:** 2026  |  **Pais:** España
- **Tipo:** Propuesta tecnica/Modelo
- **Tecnologia / metodo:** modelos de lenguaje musical / generacion simbolica
- **Dominio:** piano (generacion de ejercicios de lectura)  |  **Poblacion:** estudiantes
- **DOI:** 10.1016/j.eswa.2026.132088
- **Palabras clave:** Music language models Music generation Automatic composition Music education technology Diﬃculty Playability Complexity

## Resumen (del articulo)

Sight-reading is a core skill in music education. It refers to the ability to play a written piece of music correctly the ﬁrst time it is seen. Developing this skill requires frequent practice with completely new musical excerpts that match the diﬃculty level of the student. However, creating new sight-reading exercises at a speciﬁc diﬃculty level requires signiﬁcant time and expert knowledge. As a result, students and teachers often rely on pieces from the existing piano literature, even though sight-reading exams typically use compositions written speciﬁcally for the exam. Generative music systems provide a promising approach for creating new sight-reading material with explicit control over performance diﬃculty. In this work, we frame the creation of sight-reading exercises as a symbolic music generation task that produces piano scores with controllable diﬃculty. Existing approaches typically rely on control tokens to guide generation, but we show that this strategy does not result in piano scores with reliably controlled diﬃculty. To address this issue, we introduce an auxiliary diﬃculty prediction objective using synthetic diﬃculty labels produced by an expert-based system, enabling scalable training. Our method improves diﬃculty conditioning accuracy from 69.3% to 92.9% compared to a baseline that conditions generation solely on diﬃculty control tokens, and reduces mean squared error from 0.30 to 0.09. A user study with expert pianists shows that the generated scores ar

## Relevancia para Hand Sing Kids

Genera ejercicios de lectura a primera vista al piano controlando la DIFICULTAD (modelos de lenguaje musical simbolico). Relevante para la generacion/seleccion automatica de actividades calibradas al nivel del nino (Fase 7).

## Notas de lectura

- [ ] Leer texto completo y completar: metodo detallado, dataset, metricas, limitaciones.
- [ ] Extraer citas concretas para el Capitulo 2.
