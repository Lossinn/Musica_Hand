"""Configuración global de Hand Sing Music.

Constantes compartidas por todos los módulos. Sin lógica: solo valores.
"""
from __future__ import annotations

from pathlib import Path

# ─── Rutas ───────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
USERS_DIR = DATA_DIR / "users"            # perfiles + credenciales (hash)
SESSIONS_DIR = DATA_DIR / "sessions"      # registro de cada sesión de juego
CALIBRATION_DIR = DATA_DIR / "calibration"
PROGRESS_DIR = DATA_DIR / "progress"      # progreso de niveles por niño
DIAGNOSTICS_DIR = DATA_DIR / "diagnostics"  # diagnóstico general por niño
SONGS_DIR = DATA_DIR / "songs"            # canciones creadas: songs/<user_id>/<song_id>.json
ASSETS_DIR = BASE_DIR / "assets"
MODELS_DIR = BASE_DIR / "models"
MUSIC_DIR = ASSETS_DIR / "music"            # catálogos base (canciones, patrones)
IMAGES_DIR = ASSETS_DIR / "images"
SOUNDS_DIR = ASSETS_DIR / "sounds"
# Calibración: cada niño calibra la suya en data/calibration/<user_id>.json
# (ver calibration.Calibrator.path). El de REFERENCIA de la versión anterior
# (MusicaManos) queda como fallback de solo lectura cuando un niño aún no calibró.
PENTAGRAMA_REFERENCIA = BASE_DIR / "pentagrama_calibrado.reference.json"
CANCIONES_JSON = MUSIC_DIR / "canciones.json"
RHYTHM_PATTERNS_JSON = MUSIC_DIR / "rhythm_patterns.json"

# Todas las carpetas de datos que main.py crea al arrancar.
DATA_SUBDIRS = (USERS_DIR, SESSIONS_DIR, CALIBRATION_DIR, PROGRESS_DIR,
                DIAGNOSTICS_DIR, SONGS_DIR)

# ─── Teoría musical ─────────────────────────────────────────────────────
#   Octava reducida DO3..DO4 (8 señas), heredada de la versión anterior
#   (MusicaManos). Cada nombre lleva su octava; DO4 cierra la octava.
NOTAS: tuple[str, ...] = ("DO3", "RE3", "MI3", "FA3", "SOL3", "LA3", "SI3", "DO4")

# ─── Dinámicas de juego ──────────────────────────────────────────────────
DINAMICAS: tuple[str, ...] = ("tutorial", "libre", "ritmico", "reaccion")

# ─── Cámara / visión ─────────────────────────────────────────────────────
#   CADA SEÑA USA LAS DOS MANOS (versión anterior): el vector de gesto es la
#   concatenación de los landmarks de ambas manos, ordenadas por hand_label.
CAMERA_INDEX = 0
FRAME_WIDTH = 640
FRAME_HEIGHT = 480
NUM_LANDMARKS = 21          # MediaPipe Hands, por mano
LANDMARK_DIMS = 3           # (x, y, z)
HANDS_PER_GESTURE = 2       # seña = pose de dos manos
GESTURE_VECTOR_DIMS = HANDS_PER_GESTURE * NUM_LANDMARKS * LANDMARK_DIMS  # 126
MAX_HANDS = 2
MIN_DETECTION_CONFIDENCE = 0.65
MIN_TRACKING_CONFIDENCE = 0.5
#   Umbral de similitud (coseno) del reconocedor de plantillas.
GESTURE_SIMILARITY_THRESHOLD = 0.65
#   Enfriamiento entre notas repetidas (s) en modos continuos.
NOTE_COOLDOWN_S = 0.30

# ─── Juego ───────────────────────────────────────────────────────────────
FPS = 60
EDAD_MIN = 3
EDAD_MAX = 12
DIFICULTAD_MIN = 1
DIFICULTAD_MAX = 5

# ─── Pantallas (máquina de estados del flujo) ───────────────────────────
#   Ver screens.py y docs/02_arquitectura_flujo.md §3.
PANTALLAS: tuple[str, ...] = (
    "bienvenida",     # "Comenzar / Aprender / Ajustes"
    "login",          # nombre + contraseña
    "crear_perfil",   # datos del niño + contraseña
    "calibracion",    # personaje + gesto de referencia
    "diagnostico",    # prueba corta de colocación (§ diagnostics)
    "niveles",        # progreso, etapa actual, "Crea tus canciones"
    "juego",          # actividad musical adaptativa
    "compositor",     # editor de canciones (modo nivel / libre)
    "resumen",        # resumen de sesión + diagnóstico
    "ajustes",
)

# ─── Autenticación ─────────────────────────────────────────────────────
#   Contraseñas de niños: simples pero NUNCA en texto plano.
PBKDF2_ITERACIONES = 200_000
PBKDF2_HASH = "sha256"
PASSWORD_MIN_LEN = 4          # niños: PIN corto admitido

# ─── Estrellas (como las tarjetas de "Canciones" de la referencia) ─────
#   umbral de precisión -> nº de estrellas 0..3
ESTRELLAS_UMBRAL = ((0.60, 1), (0.80, 2), (0.92, 3))

# ─── Diagnóstico general ───────────────────────────────────────────────
PERFILES_APRENDIZAJE: tuple[str, ...] = ("rapido", "medio", "lento")
ESTADOS_DOMINIO: tuple[str, ...] = ("nuevo", "en_progreso", "fragil", "dominado")
#   nº de eventos de la prueba de colocación inicial
PRUEBA_DIAGNOSTICA_ITEMS = 12

# ─── Perfil adaptativo: pesos de la función de recompensa (§20) ──────────
#   R_t = w1*P_t - w2*E_t - w3*T_t + w4*L_t
REWARD_WEIGHTS = {"w1": 1.0, "w2": 0.5, "w3": 0.3, "w4": 0.8}

# ─── Función objetivo MILP (§13): max Z = aL + bP + gM - dE - eT ─────────
MILP_WEIGHTS = {"alpha": 1.0, "beta": 0.7, "gamma": 0.5, "delta": 0.6, "epsilon": 0.4}
