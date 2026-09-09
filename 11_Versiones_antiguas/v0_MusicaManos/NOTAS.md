# v0_MusicaManos

**Fecha de archivo:** 2026-09-09
**Autor original:** Cristian Javier Cano Mogollón
**Origen:** proyecto preliminar anexado por el usuario en
`03_Codigo/Prototipo/Codigo_prot/` (copia limpia — sin `.venv`, `.git` ni
assets binarios, que ya están integrados en `03_Codigo/Prototipo/assets/`).

## Qué hacía

App Pygame "Hand Sing Kids!" con cámara real. Estados: bienvenida (nombre),
menú, **calibrar** señas, **tutorial** (aprende las 8 señas), **uso libre**,
**minijuego de notas rítmicas** (secuencia que cae, tipo guitar-hero),
**juego de reacción** (imita la seña), selección de canción, resultados.

## Qué se rescató (integrado en 03_Codigo/Prototipo/)

| De aquí | Fue a |
|---|---|
| `src/vision.py` → `MediaPipeHandDetector` | `vision.py` (`HandVision`, `MediaPipeHandDetector`) |
| `src/vision.py` → `HandGestureRecognizer` (coseno, umbral 0.65) | `recognizer.py` (`GestureRecognizer`) |
| `src/vision.py` → `StaffCalibrator` | `calibration.py` (`Calibrator`, captura de 2 manos por nota) |
| `src/rhythm/{engine,detector,evaluator}.py` | `rhythm/` (ampliado con las figuras del currículo) |
| `Data/pentagrama_calibrado.json` | `pentagrama_calibrado.reference.json` (fallback de solo lectura) |
| `Data/songs.json` | `assets/music/canciones.json` |
| `Data/rhythm_patterns.json` | `assets/music/rhythm_patterns.json` |
| `assets/Images/*`, `assets/Sounds/*` | `assets/images/`, `assets/sounds/` |
| `probar_camara.py` | `tools/probar_camara.py` |
| Notas `DO3..DO4` (octava reducida, 8 señas de dos manos) | `config.NOTAS` |
| `ScoreManager` (tiers Perfect/Good/Ok/Miss, combo) | pendiente: `adaptive/profile` + `game` |
| Estados del juego | `screens.Pantalla` (reorganizados con auth + niveles) |

## Por qué se archivó

Es un monolito (`src/game.py`, ~1600 líneas) sin perfiles, sin progreso
persistente, sin adaptación de dificultad y con dificultad de canciones fija.
El proyecto nuevo lo reorganiza en módulos con contratos (ver
`03_Codigo/Prototipo/docs/`), pero **conserva su pipeline de visión y ritmo tal
cual** porque ya funciona con cámara real.

## Limitaciones conocidas heredadas

- Las plantillas de seña se solapan en coseno (MI3~FA3 ≈ 0.93). Funciona por
  argmax pero conviene endurecer (Fase 4: calibración automática, normalización
  por escala, umbrales por nota).
- El reconocedor exige **dos manos visibles**; con una sola devuelve `None`.
- `src/Screens/` y `src/Ui/` estaban vacíos (refactor no empezado).
