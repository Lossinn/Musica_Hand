"""Sistema de diseño *Playful Tactile Wonderland* traducido a Qt.

Los valores provienen del sistema de diseño del prototipo: superficies cálidas
color porcelana, acentos saturados, bordes gruesos, curvatura máxima y biseles
inferiores que imitan un juguete de plástico.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from PySide6.QtGui import QColor, QFont, QFontDatabase

from ..core.config import ASSETS_DIR


# ---------------------------------------------------------------- colores

@dataclass(frozen=True)
class Palette:
    # Superficies
    surface: str = "#FFF8F4"
    surface_low: str = "#FFF1E4"
    surface_container: str = "#FFEBD4"
    surface_high: str = "#FAE5CD"
    surface_highest: str = "#F4DFC8"
    surface_dim: str = "#EBD7BF"
    white: str = "#FFFFFF"

    # Texto
    on_surface: str = "#241A0B"
    on_surface_variant: str = "#4E4633"
    cocoa: str = "#736451"
    outline: str = "#7F7661"
    outline_variant: str = "#D1C5AD"

    # Acentos de marca
    sun: str = "#FFD13B"
    sun_bevel: str = "#D8A50B"
    sun_soft: str = "#FFE08A"

    sky: str = "#38B6FF"
    sky_bevel: str = "#1C88C7"
    sky_soft: str = "#CAE6FF"

    bubblegum: str = "#FF6B8B"
    bubblegum_bevel: str = "#D94263"
    bubblegum_soft: str = "#FFD9DD"

    mint: str = "#2EC4B6"
    mint_bevel: str = "#1E8F85"
    mint_soft: str = "#C9F2ED"

    tangerine: str = "#FF9F1C"
    tangerine_bevel: str = "#C97400"

    violet: str = "#7A5CFA"
    violet_bevel: str = "#5638C4"
    violet_soft: str = "#E2DAFF"

    error: str = "#BA1A1A"
    error_soft: str = "#FFDAD6"

    def q(self, name: str) -> QColor:
        return QColor(getattr(self, name))


PALETTE = Palette()
C = PALETTE  # alias corto

# Colores asignados a cada nota, de grave a agudo (arcoíris cálido).
NOTE_COLORS = {
    "DO3": "#FF6B8B",
    "RE3": "#FF9F1C",
    "MI3": "#FFD13B",
    "FA3": "#2EC4B6",
    "SOL3": "#38B6FF",
    "LA3": "#7A5CFA",
    "SI3": "#C94FD0",
    "DO4": "#FF4F7B",
}


# ------------------------------------------------------------------ formas

@dataclass(frozen=True)
class Radius:
    sm: int = 8
    md: int = 16
    lg: int = 24
    xl: int = 32
    xxl: int = 48
    pill: int = 999


R = Radius()


@dataclass(frozen=True)
class Space:
    xs: int = 8
    sm: int = 12
    md: int = 20
    lg: int = 32
    xl: int = 48
    gutter: int = 24
    margin: int = 32


S = Space()


# --------------------------------------------------------------- tipografía

# Cadena de respaldo: si el usuario instala Comfortaa/Quicksand se usan; si no,
# se recurre a las redondeadas que macOS trae de fábrica.
DISPLAY_STACK = ["Comfortaa", "Baloo 2", "Fredoka", "Arial Rounded MT Bold",
                 "SF Pro Rounded", "Poppins", "Avenir Next", "Helvetica Neue",
                 "Sans Serif"]
BODY_STACK = ["Quicksand", "Nunito", "Poppins", "Avenir Next", "SF Pro Text",
              "Helvetica Neue", "Sans Serif"]

_resolved: dict[str, str] = {}


def format_duration(seconds: float) -> str:
    """Formatea una duración en minutos:segundos, para mostrar al lado de
    canciones y actividades ('1:05')."""
    total = max(0, int(round(seconds)))
    m, s = divmod(total, 60)
    return f"{m}:{s:02d}"


def load_bundled_fonts() -> list[str]:
    """Carga cualquier .ttf/.otf que el usuario deje en ui/assets/fonts."""
    loaded: list[str] = []
    folder = Path(ASSETS_DIR) / "fonts"
    if not folder.exists():
        return loaded
    for f in sorted(folder.glob("*")):
        if f.suffix.lower() in (".ttf", ".otf"):
            fid = QFontDatabase.addApplicationFont(str(f))
            if fid != -1:
                loaded.extend(QFontDatabase.applicationFontFamilies(fid))
    return loaded


def _resolve(stack: list[str], key: str) -> str:
    if key in _resolved:
        return _resolved[key]
    available = set(QFontDatabase.families())
    for family in stack:
        if family in available:
            _resolved[key] = family
            return family
    _resolved[key] = stack[-1]
    return _resolved[key]


def display_family() -> str:
    return _resolve(DISPLAY_STACK, "display")


def body_family() -> str:
    return _resolve(BODY_STACK, "body")


def font(size: int, *, display: bool = False, bold: bool = True) -> QFont:
    f = QFont(display_family() if display else body_family())
    f.setPixelSize(size)
    f.setWeight(QFont.Weight.Bold if bold else QFont.Weight.DemiBold)
    if display:
        f.setLetterSpacing(QFont.SpacingType.PercentageSpacing, 101)
    return f


# Escalas del sistema de diseño.
def display_lg() -> QFont: return font(46, display=True)
def headline_lg() -> QFont: return font(32, display=True)
def headline_md() -> QFont: return font(24, display=True)
def headline_sm() -> QFont: return font(20, display=True)
def label_lg() -> QFont: return font(18, display=True)
def label_md() -> QFont: return font(15, display=True)
def label_sm() -> QFont: return font(12, display=True)
def body_lg() -> QFont: return font(19, bold=False)
def body_md() -> QFont: return font(16, bold=False)
def body_sm() -> QFont: return font(13, bold=False)


# ------------------------------------------------------------- hoja global

def global_stylesheet() -> str:
    return f"""
    QWidget {{
        color: {C.on_surface};
        font-family: "{body_family()}";
    }}
    QMainWindow, QStackedWidget, #RootSurface {{
        background: {C.surface};
    }}
    QLabel {{ background: transparent; }}
    QScrollArea {{ background: transparent; border: none; }}
    QScrollArea > QWidget > QWidget {{ background: transparent; }}
    QScrollBar:vertical {{
        background: transparent; width: 12px; margin: 4px;
    }}
    QScrollBar::handle:vertical {{
        background: {C.outline_variant}; border-radius: 6px; min-height: 40px;
    }}
    QScrollBar::add-line, QScrollBar::sub-line {{ height: 0; }}
    QScrollBar:horizontal {{ height: 0px; }}
    QToolTip {{
        background: {C.on_surface}; color: {C.surface};
        border-radius: 10px; padding: 6px 10px;
    }}
    QLineEdit, QSpinBox {{
        background: {C.white};
        border: 3px solid {C.outline_variant};
        border-radius: {R.lg}px;
        padding: 12px 18px;
        font-size: 18px;
        selection-background-color: {C.sky_soft};
        selection-color: {C.on_surface};
    }}
    QLineEdit:focus, QSpinBox:focus {{ border-color: {C.sky}; }}
    QCheckBox {{ spacing: 10px; font-size: 15px; }}
    QCheckBox::indicator {{
        width: 26px; height: 26px;
        border-radius: 13px;
        border: 3px solid {C.outline_variant};
        background: {C.white};
    }}
    QCheckBox::indicator:checked {{
        background: {C.mint}; border-color: {C.mint_bevel};
    }}
    QComboBox {{
        background: {C.white};
        border: 3px solid {C.outline_variant};
        border-radius: {R.lg}px;
        padding: 10px 16px; font-size: 16px;
    }}
    QComboBox::drop-down {{ border: none; width: 30px; }}
    QSlider::groove:horizontal {{
        height: 12px; border-radius: 6px; background: {C.surface_highest};
    }}
    QSlider::sub-page:horizontal {{
        height: 12px; border-radius: 6px; background: {C.sky};
    }}
    QSlider::handle:horizontal {{
        width: 26px; height: 26px; margin: -8px 0;
        border-radius: 13px; background: {C.white};
        border: 3px solid {C.sky_bevel};
    }}
    """
