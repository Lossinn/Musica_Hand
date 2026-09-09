# Comprehensive evaluation of folk music teaching effects based on multimodal machine learning

- **Archivo:** `70_documentos/2026_Zhang_folk-music-teaching-multimodal-ML.pdf`
- **id matriz:** 065  |  **Relacion:** A - Nucleo
- **Autor(es):** Zhang et al.  |  **Ano:** 2026  |  **Pais:** China
- **Tipo:** Propuesta tecnica/Modelo
- **Tecnologia / metodo:** ML multimodal (voz + música + gesto, MFCC/CNN)
- **Dominio:** música folclórica (evaluación)  |  **Poblacion:** estudiantes
- **DOI:** 10.1007/s44163-026-00923-y
- **Palabras clave:** Folk music teaching, Multimodal learning, Speech emotion recognition, Tone analysis, Gesture detection, Teaching evaluation

## Resumen (del articulo)

Folk music teaching emphasizes both cultural preservation and emotional expression, making its evaluation complex. Conventional single-modality methods, relying only on audio or textual feedback, often fail to capture the interplay between performance accuracy, tonal quality, and student engagement. To overcome these limitations, this study proposes a Hybrid Multimodal Sentiment-Tone Analysis (HMSTA) framework that integrates speech, music, and gesture analysis to provide a holistic evaluation. The framework employs wavelet filtering for noise reduction, and music notes are normalized and categorized into types for consistent tonal representation. Mel-Frequency Cepstral Coefficients (MFCCs) are extracted from audio signals and serve as feature inputs for Convolutional Neural Networks (CNNs) that classify emotions and analyze tonal patterns. For music tone evaluation, MFCCbased features are compared against reference notes to assess pitch accuracy and rhythm stability. In parallel, gesture engagement is measured using CNN-based pose estimation to capture expressive movement during teaching and learning sessions. A multimodal attention-based fusion model integrates these features to provide synchronized, real-time assessments of both teacher delivery and student response. Experimental validation on a multimodal folk music teaching dataset of 200 sessions demonstrates that HMSTA achieves high evaluation accuracy across emotion recognition, pitch analysis, and cultural authentici

## Relevancia para Hand Sing Kids

Marco multimodal que integra explicitamente analisis de voz + musica + GESTO (MFCC/CNN) para evaluar la ensenanza. Ejemplo de fusion de modalidades incluyendo gesto; util para el modulo de evaluacion.

## Notas de lectura

- [ ] Leer texto completo y completar: metodo detallado, dataset, metricas, limitaciones.
- [ ] Extraer citas concretas para el Capitulo 2.
