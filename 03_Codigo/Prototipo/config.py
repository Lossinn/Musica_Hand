"""Configuración global de Hand Sing Kids.

Constantes compartidas por todos los módulos. Sin lógica: solo valores.
"""
from __future__ import annotations

from pathlib import Path

# ─── Rutas ───────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
USERS_DIR = DATA_DIR / "users"
SESSIONS_DIR = DATA_DIR / "sessions"
CALIBRATION_DIR = DATA_DIR / "calibration"
ASSETS_DIR = BASE_DIR / "assets"
MODELS_DIR = BASE_DIR / "models"
PENTAGRAMA_CALIBRADO = BASE_DIR / "pentagrama_calibrado.json"

# ─── Teoría musical (Fase 1) ─────────────────────────────────────────────
NOTAS: tuple[str, ...] = ("DO", "RE", "MI", "FA", "SOL", "LA", "SI")

# ─── Dinámicas de juego ──────────────────────────────────────────────────
DINAMICAS: tuple[str, ...] = ("tutorial", "libre", "ritmico", "reaccion")

# ─── Cámara / visión ─────────────────────────────────────────────────────
CAMERA_INDEX = 0
FRAME_WIDTH = 640
FRAME_HEIGHT = 480
NUM_LANDMARKS = 21          # MediaPipe Hands
LANDMARK_DIMS = 3           # (x, y, z)  ->  21 * 3 = 63 características
MAX_HANDS = 1
MIN_DETECTION_CONFIDENCE = 0.6
MIN_TRACKING_CONFIDENCE = 0.5

# ─── Juego ───────────────────────────────────────────────────────────────
FPS = 60
EDAD_MIN = 3
EDAD_MAX = 12
DIFICULTAD_MIN = 1
DIFICULTAD_MAX = 5

# ─── Perfil adaptativo: pesos de la función de recompensa (§20) ──────────
#   R_t = w1*P_t - w2*E_t - w3*T_t + w4*L_t
REWARD_WEIGHTS = {"w1": 1.0, "w2": 0.5, "w3": 0.3, "w4": 0.8}

# ─── Función objetivo MILP (§13): max Z = aL + bP + gM - dE - eT ─────────
MILP_WEIGHTS = {"alpha": 1.0, "beta": 0.7, "gamma": 0.5, "delta": 0.6, "epsilon": 0.4}
