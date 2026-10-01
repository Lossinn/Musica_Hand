"""Rutas, constantes y preferencias persistentes de Hand Sing Kids."""

from __future__ import annotations

import json
import os
import sys
from dataclasses import dataclass, asdict, field
from pathlib import Path

APP_NAME = "Hand Sing Kids"
APP_SLUG = "handsingkids"
APP_VERSION = "2.0.0"

# --- Raíces del proyecto -------------------------------------------------

PACKAGE_DIR = Path(__file__).resolve().parent.parent
PROJECT_DIR = PACKAGE_DIR.parent
ASSETS_DIR = PACKAGE_DIR / "ui" / "assets"


def user_data_dir() -> Path:
    """Carpeta de datos del usuario, dependiente del sistema operativo."""
    if sys.platform == "darwin":
        base = Path.home() / "Library" / "Application Support"
    elif os.name == "nt":
        base = Path(os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming"))
    else:
        base = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share"))
    path = base / APP_NAME
    path.mkdir(parents=True, exist_ok=True)
    return path


# Permite redirigir todos los datos (útil en pruebas y en modo portátil).
_DATA_OVERRIDE: Path | None = None


def set_data_dir(path: Path | str | None) -> None:
    global _DATA_OVERRIDE
    _DATA_OVERRIDE = Path(path) if path is not None else None
    if _DATA_OVERRIDE is not None:
        _DATA_OVERRIDE.mkdir(parents=True, exist_ok=True)


def data_dir() -> Path:
    if _DATA_OVERRIDE is not None:
        return _DATA_OVERRIDE
    env = os.environ.get("HSK_DATA_DIR")
    if env:
        p = Path(env)
        p.mkdir(parents=True, exist_ok=True)
        return p
    return user_data_dir()


def db_path() -> Path:
    return data_dir() / "handsingkids.sqlite3"


def audio_cache_dir() -> Path:
    p = data_dir() / "audio"
    p.mkdir(parents=True, exist_ok=True)
    return p


def bundled_audio_dir() -> Path:
    """Sonidos reales incluidos con la propia aplicación (no sintetizados),
    en `handsingkids/ui/assets/audio/`. Tienen prioridad sobre el sonido
    generado por síntesis, pero por debajo de lo que una familia deje en
    `custom_audio_dir()`. Puede no existir o estar incompleta: lo que falte
    sigue sonando con la versión sintetizada, sin que eso sea un error."""
    return ASSETS_DIR / "audio"


def custom_audio_dir() -> Path:
    """Carpeta donde una familia puede dejar sus propios sonidos.

    Cualquier archivo .wav puesto aquí con el nombre correcto reemplaza al
    sonido generado, sin tocar código: 'nota_DO3.wav'..'nota_DO4.wav' para las
    notas, 'musica_inicio.wav' para la música de bienvenida, y el resto de
    nombres de docs/documento_tecnico.md o del LEEME.txt que se crea aquí.
    """
    p = data_dir() / "sonidos_personalizados"
    p.mkdir(parents=True, exist_ok=True)
    return p


def templates_path(profile_id: int) -> Path:
    p = data_dir() / "gestos"
    p.mkdir(parents=True, exist_ok=True)
    return p / f"perfil_{profile_id}.json"


def legacy_templates_path() -> Path:
    """Plantillas de la versión 1, para importación automática."""
    return PROJECT_DIR / "data" / "pentagrama_calibrado.json"


# --- Parámetros del reconocimiento --------------------------------------

@dataclass
class VisionSettings:
    """Umbrales del reconocedor. Todos son ajustables desde Zona de Padres."""

    detection_confidence: float = 0.6
    tracking_confidence: float = 0.5
    max_num_hands: int = 2

    # Clasificación
    confidence_threshold: float = 0.55   # confianza mínima aceptada
    margin_threshold: float = 0.08       # distancia mínima al segundo candidato
    require_two_hands: bool = True

    # Estabilización temporal
    window_frames: int = 1               # 1 = confirma en el primer fotograma (sin espera)
    agreement_ratio: float = 0.62        # proporción de la ventana que debe coincidir
    refractory_seconds: float = 0.45     # bloqueo tras confirmar una nota
    release_frames: int = 6              # fotogramas sin confirmación antes de repetir
                                          # (con window_frames=1, un valor bajo
                                          # deja que un parpadeo de 1-2
                                          # fotogramas del rastreo de la mano
                                          # -sin que el niño suelte la seña de
                                          # verdad- haga sonar la misma nota
                                          # dos veces; ver vision.stabilizer)

    # Cámara
    camera_index: int = 0
    frame_width: int = 960
    frame_height: int = 540
    target_fps: int = 24
    mirror: bool = True


@dataclass
class AudioSettings:
    master_volume: float = 0.8
    music_volume: float = 0.9
    effects_volume: float = 0.7
    voice_cues: bool = True


@dataclass
class LearningSettings:
    mastery_threshold: float = 0.80      # a partir de aquí la habilidad está dominada
    consolidated_threshold: float = 0.92
    session_minutes: int = 8             # presupuesto de tiempo de una mini sesión
    activities_per_session: int = 4
    use_milp: bool = True                # si falla, cae a la heurística voraz
    adaptive: bool = True


@dataclass
class Settings:
    vision: VisionSettings = field(default_factory=VisionSettings)
    audio: AudioSettings = field(default_factory=AudioSettings)
    learning: LearningSettings = field(default_factory=LearningSettings)
    fullscreen: bool = False
    show_confidence: bool = False        # modo infantil lo oculta

    # ---- persistencia ----
    @staticmethod
    def path() -> Path:
        return data_dir() / "settings.json"

    @classmethod
    def load(cls) -> "Settings":
        p = cls.path()
        if not p.exists():
            return cls()
        try:
            raw = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            return cls()
        s = cls()
        for section, klass in (("vision", VisionSettings),
                               ("audio", AudioSettings),
                               ("learning", LearningSettings)):
            data = raw.get(section, {})
            if isinstance(data, dict):
                current = asdict(getattr(s, section))
                current.update({k: v for k, v in data.items() if k in current})
                setattr(s, section, klass(**current))
        s.fullscreen = bool(raw.get("fullscreen", s.fullscreen))
        s.show_confidence = bool(raw.get("show_confidence", s.show_confidence))
        return s

    def save(self) -> None:
        payload = {
            "vision": asdict(self.vision),
            "audio": asdict(self.audio),
            "learning": asdict(self.learning),
            "fullscreen": self.fullscreen,
            "show_confidence": self.show_confidence,
        }
        self.path().write_text(json.dumps(payload, indent=2, ensure_ascii=False),
                               encoding="utf-8")


_settings: Settings | None = None


def settings() -> Settings:
    global _settings
    if _settings is None:
        _settings = Settings.load()
    return _settings


def reload_settings() -> Settings:
    global _settings
    _settings = Settings.load()
    return _settings
