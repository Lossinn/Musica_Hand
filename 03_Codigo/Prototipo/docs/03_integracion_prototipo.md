# Integración del prototipo previo (MusicaManos) — bloqueo resuelto

> Complementa los Entregables 1 y 2. Documenta **cómo quedó resuelta la
> correspondencia gesto → nota** y el mapa de migración del prototipo anexado.
> El prototipo limpio se archivó en
> [`11_Versiones_antiguas/v0_MusicaManos/`](../../../11_Versiones_antiguas/v0_MusicaManos/NOTAS.md).

---

## 1. El bloqueo, resuelto

La "correspondencia gesto → nota de la versión anterior" **no era una tabla**
(p. ej. "3 dedos = DO"). Es un sistema de **plantillas calibradas por el niño**:

| Pieza | Cómo funciona |
|---|---|
| **Seña** | Cada nota es una **pose estática de las DOS manos**. |
| **Vector** | landmarks de ambas manos (centrados en la muñeca), ordenados por `hand_label`, concatenados → **126 dims** (`config.GESTURE_VECTOR_DIMS`). |
| **Calibración** | El niño hace cada seña una vez; se guarda el snapshot en `data/calibration/<user_id>.json`. |
| **Reconocimiento** | Similitud **coseno** entre la pose en vivo y cada plantilla; gana la más parecida **si** supera `config.GESTURE_SIMILARITY_THRESHOLD` (0.65). Con < 2 manos o sin plantillas → `None`. |
| **gesto → nota** | **Identidad**: la plantilla ya está etiquetada con el nombre de la nota. |

**Notas:** octava reducida **`DO3 RE3 MI3 FA3 SOL3 LA3 SI3 DO4`** (8 señas).
`config.NOTAS` y `curriculum` se actualizaron a estos identificadores; `DO4`
es el "cierre de octava" (antes provisionalmente `DO8`).

Implementado y con tests (sin cámara):
[`recognizer.py`](../recognizer.py) · [`calibration.py`](../calibration.py) ·
[`tests/test_vision_stack.py`](../tests/test_vision_stack.py).

---

## 2. Mapa de migración

| Del prototipo (`v0_MusicaManos/`) | Al proyecto (`03_Codigo/Prototipo/`) | Estado |
|---|---|---|
| `src/vision.py::MediaPipeHandDetector` | `vision.py::MediaPipeHandDetector` + `HandVision` | ✅ portado (cv2/mediapipe con import perezoso) |
| `src/vision.py::HandGestureRecognizer` | `recognizer.py::GestureRecognizer` | ✅ implementado + tests |
| `src/vision.py::StaffCalibrator` | `calibration.py::Calibrator` | ✅ implementado (captura manual) + tests |
| `src/rhythm/engine.py` | `rhythm/engine.py` | ✅ ampliado con figuras del currículo |
| `src/rhythm/detector.py` (aplauso 2 manos) | `rhythm/detector.py` | ✅ portado + tests |
| `src/rhythm/evaluator.py` | `rhythm/evaluator.py` | ✅ portado + tests |
| `src/core/performance.py::ScoreManager` | → alimentará `adaptive/profile` + estrellas de `levels` | ⬜ pendiente |
| `src/core/music.py::NoteSprite` | → `game.py` (render del minijuego) | ⬜ pendiente |
| `src/game.py` (monolito de estados) | `screens.py` (grafo) + handlers | ⬜ pendiente |
| `Data/pentagrama_calibrado.json` | `pentagrama_calibrado.reference.json` (fallback RO) | ✅ copiado |
| `Data/songs.json` | `assets/music/canciones.json` | ✅ copiado |
| `Data/rhythm_patterns.json` | `assets/music/rhythm_patterns.json` | ✅ copiado |
| `assets/Images`, `assets/Sounds` | `assets/images`, `assets/sounds` | ✅ copiado (28 imgs, 12 sonidos) |
| `probar_camara.py` | `tools/probar_camara.py` | ✅ copiado |

### Reconciliación de conceptos

| Prototipo | Proyecto |
|---|---|
| `GameState.WELCOME / MAIN_MENU / …` | `screens.Pantalla` (+ `LOGIN`, `CREAR_PERFIL`, `DIAGNOSTICO`, `NIVELES`, `RESUMEN`) |
| nombre por teclado, sin contraseña | `auth.AuthService` (perfil + PIN con hash) |
| `MINIGAME` con canción de dificultad fija | `game` + `adaptive.Adaptador` (dificultad continua) |
| `TUTORIAL` (aprende las 8 señas) | Etapa 0 del currículo (`calibracion`) + Etapas 1–2 |
| `songs.json` (catálogo fijo) | catálogo base + `composer` (canciones del niño en `data/songs/`) |
| `highscores.json` por modo | `levels.ProgresoJugador` + `data/sessions/` |

---

## 3. Cámara real

`config.json` del prototipo solo tenía `{"camera_index": 0}`. El proyecto usa
`config.CAMERA_INDEX` (0 por defecto). Si la cámara no abre:

```
python -m Prototipo.tools.probar_camara     # recorre índices 0..9 y muestra vídeo
```

`HandVision.open()` lanza `VisionUnavailable` con un mensaje claro si no hay
cámara o falla la visión. **No hay modo simulado**: el proyecto es real
(decisión del usuario, 2026-09-09).

### MediaPipe: dos APIs

`MediaPipeHandDetector` funciona con las dos:

| API | Cómo | Requisito |
|---|---|---|
| **clásica** `mp.solutions.hands` (0.10.x) | preferida — la del prototipo | `pip install 'mediapipe>=0.10.14,<0.11'` |
| **Tasks** `mp.tasks.vision.HandLandmarker` (≥ 1.0) | fallback automático | `python -m Prototipo.tools.descargar_modelo` (baja `hand_landmarker.task`, ~7.6 MB, a `models/gesture/`) |

El venv actual del proyecto tiene **mediapipe 1.0.1** (solo Tasks); el modelo ya
se descargó y `python -m Prototipo.main --stage vision` abre la cámara, carga las
8 plantillas y entra al bucle de reconocimiento. ✅ verificado 2026-09-09.

### Comandos

```
python -m Prototipo.main --stage vision        # cámara -> imprime la seña reconocida
python -m Prototipo.main --stage calibration   # calibración guiada por consola
```

---

## 4. Próximos pasos del proceso de código

Orden sugerido (cada módulo se prueba aislado antes de conectar, §42):

1. **`persistence.JsonStore`** — escritura atómica real (hoy solo `MemoryStore`).
2. **`auth`** — alta/login con hash; pantalla `LOGIN` / `CREAR_PERFIL`.
3. **`game` (rebanada jugable)** — con `vision` + `recognizer` reales: modo
   "uso libre" (seña → suena la nota) y "notas rítmicas" (portar el minijuego
   con `NoteSprite` + `ScoreManager`).
4. **`diagnostics`** — dominio por nota/ritmo desde el historial de `game`.
5. **`levels`** — desbloqueo de etapas; pantalla `NIVELES`.
6. **`screens.App`** — flujo completo bienvenida → … → resumen.
7. **`composer`** — editor + grabación de canciones.
8. **`adaptive/`** — `predictor` → `optimizer` (MILP) → `environment` → `agent`
   (DQN) → `adapter` (integración del margen de acción).

---

## 5. Pendiente

- El raw dump `03_Codigo/Prototipo/Codigo_prot/` (con `.venv` de macOS, `.git`
  anidado, `.zip`, `__MACOSX`) está **gitignorado**. Se puede borrar: la copia
  limpia está en `11_Versiones_antiguas/v0_MusicaManos/`.
- Entregable 3 (especificaciones visuales) — tras el proceso de código.
