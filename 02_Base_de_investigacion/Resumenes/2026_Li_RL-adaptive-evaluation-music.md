# A reinforcement learningbased adaptive evaluation framework for personalized music education

- **Archivo:** `70_documentos/2026_Li_RL-adaptive-evaluation-music.pdf`
- **id matriz:** 032  |  **Relacion:** A - Nucleo
- **Autor(es):** Li et al.  |  **Ano:** 2026  |  **Pais:** China
- **Tipo:** Propuesta tecnica/Modelo
- **Tecnologia / metodo:** aprendizaje por refuerzo
- **Dominio:** educación musical (evaluación)  |  **Poblacion:** estudiantes
- **DOI:** 10.7717/peerj-cs.3464
- **Palabras clave:** Music education, Adaptive teaching framework, Deep Q-Network (DQN), Task recommendation system, Personalized learning, Educational data mining

## Resumen (del articulo)

Evaluation of student performance in music education is recognized as a persistent challenge. The current methods of assessment, such as peer feedback, instructor observations, and rubric-based grading, are subjective and fail to deliver prompt and personalized feedback. Previous approaches have largely relied on static evaluation schemes like standardized grading rubrics and subjective instructor judgments like qualitative assessments without real-time feedback, but they failed to accommodate individual learning differences and dynamic adjustment of instructional strategies based on a student’s evolving abilities. To address these limitations, this study demonstrates a reinforcement learning-based adaptive evaluation framework designed for personalized music education. To optimize teaching interventions and customize learning experiences, the framework incorporates a task-selecting evaluation agent, a dynamic student model, and a continuous feedback mechanism. A Deep Q-Network (DQN) agent processes performance metrics like technical proﬁciency, expressiveness, sight-reading ability, and interpretative skills in real-time to suggest appropriate tasks and provide personalized feedback. A simulated dataset of students was used to train and test the model with different hyperparameters. These parameters are optimized through grid search and validation techniques. The results demonstrate that the proposed framework signiﬁcantly outperforms baseline models, which include Q-learnin

## Relevancia para Hand Sing Kids

Formaliza la evaluacion del desempeno como problema de RL con seleccion de tarea segun la habilidad cambiante del alumno. Referencia directa para la Fase 7 (MILP) y Fase 11 (DQN): muestra estado del alumno, recompensa y politica de adaptacion. Contrastar su funcion de recompensa con la que use el proyecto.

## Notas de lectura

- [ ] Leer texto completo y completar: metodo detallado, dataset, metricas, limitaciones.
- [ ] Extraer citas concretas para el Capitulo 2.
