# 03_Codigo

Código fuente del proyecto.

| Carpeta                 | Contenido                                                              |
|-------------------------|----------------------------------------------------------------------|
| `Prototipo/`            | **Aplicación principal.** Arquitectura modular (ver abajo).           |
| `Reconocimiento_manos/` | Experimentos aislados de MediaPipe/OpenCV antes de integrarlos.       |
| `Musica/`               | Experimentos de audio, mapeo gesto→nota, teoría musical.             |

## Prototipo/ — arquitectura

```
Prototipo/
├── main.py            Punto de entrada. Orquesta el bucle principal.
├── config.py          Constantes: notas, rutas, parámetros de cámara y juego.
├── vision.py          HandVision: captura, detección de mano, landmarks.
├── calibration.py     Calibrator: calibración automática, carga/guardado.
├── recognizer.py      GestureRecognizer: normaliza landmarks → gesto → nota.
├── game.py            MusicGame: dinámicas (tutorial, libre, rítmico, reacción), evaluación.
│
├── adaptive/          Sistema adaptativo (Fases 6–11)
│   ├── profile.py     ChildProfile: vector de estado S_t = (P, E, T, R, D, M).
│   ├── predictor.py   Predictor: modelo TensorFlow/Keras. P_(t+1) = f(S_t, A_t).
│   ├── optimizer.py   ActivityOptimizer: MILP con PuLP. Selección de actividad.
│   ├── environment.py HandSingKidsEnv: entorno Gymnasium.
│   └── agent.py       AdaptiveAgent: DQN con Stable-Baselines3.
│
├── digital_twin/
│   └── twin.py        DigitalTwin: simulación del estudiante.
│
├── data/              Generado en runtime (ignorado por git)
│   ├── users/         Perfiles persistidos por niño
│   ├── sessions/      Registro de cada sesión de juego
│   └── calibration/   Calibraciones guardadas por usuario
│
├── assets/            images/ · sounds/ · music/
├── models/            gesture/ · predictive/  (pesos entrenados, ignorados por git)
├── tests/             Pruebas unitarias por módulo
└── pentagrama_calibrado.json   Calibración de referencia (formas/ubicaciones de notas)
```

## Regla de evolución

El bucle objetivo (`main.py`) ya refleja la arquitectura final, pero **cada módulo empieza
como esqueleto** (`raise NotImplementedError`). Se implementan en orden de fase y se prueban
de forma aislada antes de conectarlos.

```
VISIÓN → CALIBRACIÓN AUTOMÁTICA → RECONOCIMIENTO → JUEGO
       → REGISTRO → PERFIL → ML / MILP → DQN → GEMELO DIGITAL
```
