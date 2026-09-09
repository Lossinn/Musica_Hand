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
├── main.py            Punto de entrada. --stage {vision,calibration,profile,adaptive,app,full}
├── config.py          Constantes: notas, rutas, pantallas, auth, umbrales.
├── curriculum.py      Ruta de aprendizaje musical (Entregable 1). Fuente de verdad del contenido.
│
├── screens.py         Máquina de estados del flujo: Pantalla, TRANSICIONES, App.
├── auth.py            Perfil, AuthService: alta / login (hash PBKDF2).
├── persistence.py     Store: JsonStore (disco, atómico) | MemoryStore (tests).
├── diagnostics.py     Diagnostico, Diagnosticador: "diagnóstico general" del niño.
├── levels.py          ProgresoJugador, GestorNiveles: desbloqueo dinámico de etapas.
├── composer.py        Cancion, Editor: crear canciones (modo nivel / libre), grabar, guardar.
│
├── vision.py          HandVision: cámara real (OpenCV) + MediaPipe (2 manos).           [impl]
├── calibration.py     Calibrator: captura la seña de 2 manos por nota, guarda/carga.   [impl]
├── recognizer.py      GestureRecognizer: pose de 2 manos → similitud coseno → nota.    [impl]
├── rhythm/            engine (TA/TITI→tiempos) · detector (aplauso) · evaluator.        [impl]
├── game.py            MusicGame: Activity/ActivityResult, dinámicas, evaluación nota + tiempo.
│
├── adaptive/          Sistema adaptativo (Fases 7–11)
│   ├── profile.py     ChildProfile: vector de estado S_t = (P, E, T, R, D, M).
│   ├── adapter.py     Adaptador: MargenAccion + ParametrosActividad (el "margen de acción").
│   ├── predictor.py   Predictor: modelo TensorFlow/Keras. P_(t+1) = f(S_t, A_t).
│   ├── optimizer.py   ActivityOptimizer: MILP con PuLP. Selección de actividad.
│   ├── environment.py HandSingMusicEnv: entorno Gymnasium.
│   └── agent.py       AdaptiveAgent: DQN con Stable-Baselines3.
│
├── digital_twin/
│   └── twin.py        DigitalTwin: simulación del estudiante.
│
├── docs/              Entregables de diseño (ruta, arquitectura, integración del prototipo).
├── tools/             probar_camara.py — recorre índices de cámara.
│
├── data/              Generado en runtime (ignorado por git)
│   ├── users/ progress/ diagnostics/ sessions/ calibration/ songs/
│
├── assets/            images/ · sounds/ · music/
├── models/            gesture/ · predictive/  (pesos entrenados, ignorados por git)
├── tests/             Pruebas unitarias por módulo
└── pentagrama_calibrado.json   Calibración de referencia (formas/ubicaciones de notas)
```

Diseño detallado en [`Prototipo/docs/`](Prototipo/docs/):
`01_ruta_aprendizaje_musical.md` · `02_arquitectura_flujo.md` ·
`03_integracion_prototipo.md`.

`[impl]` = implementado y con tests. El resto son contratos (`NotImplementedError`).
Notas: octava reducida `DO3..DO4` (8 señas de dos manos), heredada de
`11_Versiones_antiguas/v0_MusicaManos/`.

## Regla de evolución

El bucle objetivo (`main.py`) ya refleja la arquitectura final, pero **cada módulo empieza
como esqueleto** (`raise NotImplementedError`). Se implementan en orden de fase y se prueban
de forma aislada antes de conectarlos.

```
VISIÓN → CALIBRACIÓN AUTOMÁTICA → RECONOCIMIENTO → JUEGO
       → REGISTRO → PERFIL → ML / MILP → DQN → GEMELO DIGITAL
```
