# Selfsupervised multimodal transformer for finegrained detection of controlled perturbation events in piano performance

- **Archivo:** `70_documentos/2026_Yang_self-supervised-transformer-piano-errors.pdf`
- **id matriz:** 152  |  **Relacion:** A - Nucleo
- **Autor(es):** Yang et al.  |  **Ano:** 2026  |  **Pais:** China
- **Tipo:** Propuesta tecnica/Modelo
- **Tecnologia / metodo:** Transformer multimodal autosupervisado (audio+MIDI+proxy cinematico)
- **Dominio:** piano (deteccion de errores)  |  **Poblacion:** general
- **DOI:** 10.1038/s41598-026-45945-9
- **Palabras clave:** self-supervised learning, multimodal Transformer, piano performance assessment, fine-grained error detection, cross-modal attention mechanism, MIDI-derived kinematic representations

## Resumen (del articulo)

www.nature.com/scientificreports OPEN Self-supervised multimodal transformer for fine-grained detection of controlled perturbation events in piano performance Kun Yang & Jitao Chen The acquisition of piano performance skills relies on continuous practice and precise feedback, yet traditional manual evaluation is constrained by time costs and subjective variations, making it difficult to meet the demands of large-scale music education. This study proposes a self-supervised multimodal Transformer framework whose core contribution is the fusion across audio spectral features, symbolic MIDI representations, and a MIDI-derived spatial/kinematic proxy, demonstrating cross-modal attention’s ability to exploit heterogeneous representations under controlled conditions through adaptive fusion mechanisms. Since the MAESTRO dataset lacks video recordings, hand posture features are synthetically derived from MIDI parameters rather than captured from independent visual sensors, representing a kinematic proxy for validating multimodal fusion concepts under controlled conditions. The two-stage training strategy employs contrastive learning, masked prediction, and temporal reconstruction objectives to learn general-purpose music representations during the pretraining phase, and optimizes fine-grained detection capabilities for five error categories of pitch, timing, dynamics, touch, and pedal during the fine-tuning phase, significantly reducing dependence on large-scale annotated data. Exper

## Relevancia para Hand Sing Kids

Transformer multimodal autosupervisado que detecta 5 tipos de error (tono, tiempo, dinamica, articulacion, toque) fusionando audio + MIDI + un proxy cinematico de la postura de la mano. Referencia para clasificar el tipo de error del nino y dar feedback especifico.

## Notas de lectura

- [ ] Leer texto completo y completar: metodo detallado, dataset, metricas, limitaciones.
- [ ] Extraer citas concretas para el Capitulo 2.
