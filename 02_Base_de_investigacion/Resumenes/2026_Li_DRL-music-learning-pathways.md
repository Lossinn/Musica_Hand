# Deep Reinforcement Learning for Personalised Music Learning Pathways

- **Archivo:** `70_documentos/2026_Li_DRL-music-learning-pathways.pdf`
- **id matriz:** 075  |  **Relacion:** A - Nucleo
- **Autor(es):** Li et al.  |  **Ano:** 2026  |  **Pais:** China
- **Tipo:** Propuesta tecnica/Modelo
- **Tecnologia / metodo:** deep reinforcement learning (MDP, curriculum-aware)
- **Dominio:** educación musical (rutas de aprendizaje)  |  **Poblacion:** learners
- **DOI:** 10.1007/s40745-026-00689-1
- **Palabras clave:** Deep reinforcement learning · Multimodal learner modelling · Adaptive computing · Human-centred AI

## Resumen (del articulo)

Personalised music education necessitates adaptive instruction that responds to each learner’s evolving skill set, emotional state, and stylistic preferences. Yet, most existing intelligent tutoring systems and AI-driven platforms are limited in their ability to address the sequential, expressive, and affective complexity inherent in music learning. This paper presents a novel Deep Reinforcement Learning (DRL) framework designed to overcome these limitations through real-time multimodal learner modelling, affect-cognitive reward optimisation, and policy adaptation via ensemble methods and curriculum-aware exploration. The proposed approach formalises the instructional process as a Markov Decision Process (MDP), utilising a rich, multidimensional learner state that encompasses musical proﬁciency, practice behaviour, affective signals (including engagement and frustration), and individual learning style. Notably, the framework intro-duces a dual-reward mechanism that balances musical task performance with emotional engagement, thereby promoting sustained learner motivation. Policy learning is further enhanced by employing an ensemble of Actor— Critic agents, coordinated by a curriculum-based scheduler to facilitate smoother skill progres-sion and improved generalisation across diverse learner proﬁles. Empirical results from both simulated environments and controlled pilot studies indicate that the proposed method signiﬁcantly outperforms baseline DRL and conventional adap-tive

## Relevancia para Hand Sing Kids

DRL sobre un MDP con estado multidimensional del alumno (competencia, practica, senales afectivas, estilo) y recompensa afecto-cognitiva, con exploracion 'curriculum-aware'. Plano casi directo para la Fase 11 (DQN) del proyecto.

## Notas de lectura

- [ ] Leer texto completo y completar: metodo detallado, dataset, metricas, limitaciones.
- [ ] Extraer citas concretas para el Capitulo 2.
