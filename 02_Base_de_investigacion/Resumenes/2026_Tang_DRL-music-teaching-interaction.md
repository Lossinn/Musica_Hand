# The application of deep reinforcement learning in music teaching interaction

- **Archivo:** `70_documentos/2026_Tang_DRL-music-teaching-interaction.pdf`
- **id matriz:** 164  |  **Relacion:** A - Nucleo
- **Autor(es):** Tang et al.  |  **Ano:** 2026  |  **Pais:** China
- **Tipo:** Propuesta tecnica/Modelo
- **Tecnologia / metodo:** deep RL (PPO) + CNN
- **Dominio:** interaccion en ensenanza musical  |  **Poblacion:** learners
- **DOI:** 10.1007/s10791-026-10022-2
- **Palabras clave:** DRL, Interaction, Music teaching, Teaching adaptability, Understandability

## Resumen (del articulo)

Music teaching using computers and technological paradigms is provided through digital text and interactions. The interactions between the tutor and the learner are interpreted to understand the musical notes and thereby improve the learning ability. The inability to tailor lessons to each student’s unique needs in real time is a common problem with older music education interaction systems that rely on deep learning but lack flexibility and dynamic feedback mechanisms. Lacking the ability to dynamically adapt to specific student states, such as understanding level, engagement, and cognitive feedback, these systems often rely on preset datasets and established patterns. The article presents a new approach to overcome these restrictions by combining a reinforcement learning model based on Proximal Policy Optimization (PPO) with Convolutional Neural Networks (CNN). Using multimodal input such as audio features and behavioural signals, the CNN is trained to categorize levels of learner understanding. Meanwhile, the reinforcement learning agent learns the most effective ways to educate, such as by retaining, replacing, or modifying information, depending on ongoing feedback from the learners. Learners’ understanding and engagement are both enhanced by this hybrid approach’s realtime strategy adaptation. By comparing the suggested model to both traditional rule-based and deep learning-only baselines, experiments on a labelled music education dataset show that it improves learning

## Relevancia para Hand Sing Kids

RL (PPO) + CNN que clasifica el nivel de comprension/engagement del alumno desde audio + senales de conducta y adapta la interaccion. Referencia para el lazo percepcion->clasificacion de estado->accion adaptativa.

## Notas de lectura

- [ ] Leer texto completo y completar: metodo detallado, dataset, metricas, limitaciones.
- [ ] Extraer citas concretas para el Capitulo 2.
