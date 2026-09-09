# Multimodal Automatic Music Transcription Using Piano Audio and HandSkeleton Information

- **Archivo:** `70_documentos/2026_Yamada_multimodal-transcription-piano-hand-skeleton.pdf`
- **id matriz:** 123  |  **Relacion:** A - Nucleo
- **Autor(es):** Yamada et al.  |  **Ano:** 2026  |  **Pais:** Japon
- **Tipo:** Propuesta tecnica/Modelo
- **Tecnologia / metodo:** transcripción multimodal audio + esqueleto de mano (HandSkeletonNet)
- **Dominio:** piano  |  **Poblacion:** general
- **DOI:** 10.3390/electronics15102005
- **Palabras clave:** automatic music transcription; hand pose analysis; graph neural networks; multimodal recognition

## Resumen (del articulo)

Automatic Music Transcription (AMT) for piano is difficult for audio-only systems due to dense polyphony, resonance, and reverberation, which lead to false positives and unstable onset decisions. We present a multimodal AMT framework that fuses Omnizart audio probability maps with visual cues from hand-skeleton tracking. A graph-based model called HandSkeletonNet estimates per-key onset probabilities from hand trajectories, and the two modalities are merged via a weighting-and-masking scheme or a compact CNNbased merger. Experiments show consistent improvements over the audio-only baseline on our self-compiled dataset, while evaluations with external datasets primarily improve frame-level sensitivity. The frame-level F1 score improved from 75.12% to 75.76% for the PianoYT dataset and from 54.68% to 57.57% for the PianoVAM dataset compared with the audio-only baseline. Our experiments also reveal limited onset-level gains under domain shift. Remaining errors are largely explained by timing/misalignment and note fragmentation in MIDI decoding, suggesting that robustness to missing hand detections and explicit temporal alignment are key directions.

## Relevancia para Hand Sing Kids

Transcripcion musical multimodal que fusiona audio con informacion de ESQUELETO DE MANO (HandSkeletonNet, grafo). Demuestra que las trayectorias de la mano mejoran la deteccion de notas: apoyo directo a usar landmarks de MediaPipe como senal para reconocer que nota toca el nino.

## Notas de lectura

- [ ] Leer texto completo y completar: metodo detallado, dataset, metricas, limitaciones.
- [ ] Extraer citas concretas para el Capitulo 2.
