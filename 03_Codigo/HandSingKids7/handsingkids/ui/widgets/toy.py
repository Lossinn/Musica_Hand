"""Componentes táctiles: botones con bisel, tarjetas, estrellas y píldoras.

El sistema de diseño no usa sombras difusas sino extrusiones: cada control tiene
un labio inferior más oscuro que se comprime al pulsarlo, como un botón de
juguete. Todo se dibuja a mano con QPainter porque las hojas de estilo de Qt no
permiten ese tipo de profundidad.
"""

from __future__ import annotations

from PySide6.QtCore import (Property, QEasingCurve, QPropertyAnimation, QRectF,
                            QSize, Qt, Signal)
from PySide6.QtGui import (QBrush, QColor, QFont, QFontMetrics, QPainter,
                           QPainterPath, QPen)
from PySide6.QtWidgets import (QAbstractButton, QFrame, QGraphicsDropShadowEffect,
                               QHBoxLayout, QLabel, QSizePolicy, QVBoxLayout,
                               QWidget)

from .. import theme as T

# Paletas de los botones: (cara, bisel, texto)
VARIANTS = {
    "primary":   (T.C.sun, T.C.sun_bevel, "#3A2E00"),
    "secondary": (T.C.sky, T.C.sky_bevel, "#FFFFFF"),
    "danger":    (T.C.bubblegum, T.C.bubblegum_bevel, "#FFFFFF"),
    "success":   (T.C.mint, T.C.mint_bevel, "#FFFFFF"),
    "magic":     (T.C.violet, T.C.violet_bevel, "#FFFFFF"),
    "warm":      (T.C.tangerine, T.C.tangerine_bevel, "#FFFFFF"),
    "ghost":     (T.C.surface_high, T.C.surface_dim, T.C.on_surface),
}


class ToyButton(QAbstractButton):
    """Botón con labio inferior que se hunde al pulsarlo."""

    def __init__(self, text: str = "", variant: str = "primary",
                 icon_text: str = "", *, height: int = 68, depth: int = 7,
                 font_size: int = 19, parent=None) -> None:
        super().__init__(parent)
        self.variant = variant if variant in VARIANTS else "primary"
        self.icon_text = icon_text
        self._depth = depth
        self._press = 0.0
        self.setText(text)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMinimumHeight(height + depth)
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        self._font = T.font(font_size, display=True)
        self._anim = QPropertyAnimation(self, b"press", self)
        self._anim.setDuration(90)
        self._anim.setEasingCurve(QEasingCurve.Type.OutQuad)

    # animación del hundido
    def get_press(self) -> float:
        return self._press

    def set_press(self, value: float) -> None:
        self._press = value
        self.update()

    press = Property(float, get_press, set_press)

    def _animate(self, to: float) -> None:
        self._anim.stop()
        self._anim.setStartValue(self._press)
        self._anim.setEndValue(to)
        self._anim.start()

    def mousePressEvent(self, e):
        super().mousePressEvent(e)
        self._animate(1.0)

    def mouseReleaseEvent(self, e):
        super().mouseReleaseEvent(e)
        self._animate(0.0)

    def leaveEvent(self, e):
        super().leaveEvent(e)
        self._animate(0.0)

    def sizeHint(self) -> QSize:
        fm = QFontMetrics(self._font)
        w = fm.horizontalAdvance(self.text()) + 64
        if self.icon_text:
            w += 44
        return QSize(max(140, w), self.minimumHeight())

    def paintEvent(self, _event) -> None:
        face_c, bevel_c, text_c = VARIANTS[self.variant]
        if not self.isEnabled():
            face_c, bevel_c, text_c = T.C.surface_highest, T.C.outline_variant, T.C.outline

        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        w, h = self.width(), self.height()
        depth = self._depth * (1.0 - self._press)
        radius = (h - self._depth) / 2.0

        # Labio inferior.
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(QColor(bevel_c))
        p.drawRoundedRect(QRectF(0, self._depth, w, h - self._depth),
                          radius, radius)

        # Cara.
        top = self._depth - depth
        face = QRectF(0, top, w, h - self._depth)
        p.setBrush(QColor(face_c))
        p.setPen(QPen(QColor(bevel_c), 2))
        p.drawRoundedRect(face.adjusted(1, 1, -1, -1), radius, radius)

        # Brillo superior, muy sutil.
        gloss = QRectF(face.left() + 10, face.top() + 5,
                       face.width() - 20, face.height() * 0.32)
        p.setPen(Qt.PenStyle.NoPen)
        c = QColor(255, 255, 255, 46)
        p.setBrush(c)
        p.drawRoundedRect(gloss, gloss.height() / 2, gloss.height() / 2)

        # Contenido.
        p.setFont(self._font)
        p.setPen(QColor(text_c))
        label = self.text()
        if self.icon_text:
            fm = QFontMetrics(self._font)
            icon_font = QFont(self._font)
            icon_font.setPixelSize(int(self._font.pixelSize() * 1.25))
            ifm = QFontMetrics(icon_font)
            gap = 12 if label else 0
            total = ifm.horizontalAdvance(self.icon_text) + gap + \
                fm.horizontalAdvance(label)
            x = face.center().x() - total / 2
            p.setFont(icon_font)
            p.drawText(QRectF(x, face.top(), ifm.horizontalAdvance(self.icon_text),
                              face.height()),
                       Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft,
                       self.icon_text)
            if label:
                p.setFont(self._font)
                p.drawText(QRectF(x + ifm.horizontalAdvance(self.icon_text) + gap,
                                  face.top(), fm.horizontalAdvance(label) + 4,
                                  face.height()),
                           Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft,
                           label)
        else:
            p.drawText(face, Qt.AlignmentFlag.AlignCenter, label)
        p.end()


class RoundIconButton(QAbstractButton):
    """Botón circular para acciones secundarias: atrás, ayuda, sonido."""

    def __init__(self, icon_text: str, variant: str = "ghost",
                 diameter: int = 58, parent=None) -> None:
        super().__init__(parent)
        self.icon_text = icon_text
        self.variant = variant if variant in VARIANTS else "ghost"
        self._d = diameter
        self._press = 0.0
        self.setFixedSize(diameter, diameter + 5)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def mousePressEvent(self, e):
        super().mousePressEvent(e); self._press = 1.0; self.update()

    def mouseReleaseEvent(self, e):
        super().mouseReleaseEvent(e); self._press = 0.0; self.update()

    def paintEvent(self, _e) -> None:
        face_c, bevel_c, text_c = VARIANTS[self.variant]
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        depth = 5 * (1 - self._press)
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(QColor(bevel_c))
        p.drawEllipse(QRectF(0, 5, self._d, self._d))
        face = QRectF(0, 5 - depth, self._d, self._d)
        p.setBrush(QColor(face_c))
        p.setPen(QPen(QColor(bevel_c), 2))
        p.drawEllipse(face.adjusted(1, 1, -1, -1))
        f = T.font(int(self._d * 0.44), display=True)
        p.setFont(f)
        p.setPen(QColor(text_c))
        p.drawText(face, Qt.AlignmentFlag.AlignCenter, self.icon_text)
        p.end()


class Card(QFrame):
    """Contenedor con borde grueso, esquinas muy redondeadas y sombra nítida."""

    def __init__(self, parent=None, *, bg: str = T.C.white,
                 border: str = T.C.outline_variant, radius: int = T.R.xl,
                 border_width: int = 3, shadow: bool = True,
                 padding: int = 22) -> None:
        super().__init__(parent)
        self.setObjectName("Card")
        self.setStyleSheet(
            f"#Card {{ background: {bg}; border: {border_width}px solid {border};"
            f" border-radius: {radius}px; }}")
        lay = QVBoxLayout(self)
        lay.setContentsMargins(padding, padding, padding, padding)
        lay.setSpacing(14)
        if shadow:
            fx = QGraphicsDropShadowEffect(self)
            fx.setBlurRadius(0)
            fx.setOffset(0, 7)
            fx.setColor(QColor(115, 100, 81, 40))
            self.setGraphicsEffect(fx)

    def body(self) -> QVBoxLayout:
        return self.layout()  # type: ignore[return-value]


class Chip(QLabel):
    """Etiqueta con forma de píldora."""

    def __init__(self, text: str, bg: str = T.C.sky_soft,
                 fg: str = T.C.on_surface, parent=None) -> None:
        super().__init__(text, parent)
        self.setFont(T.label_md())
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet(
            f"background: {bg}; color: {fg}; border-radius: 17px;"
            f" padding: 7px 16px;")
        self.setMinimumHeight(34)
        self.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)


class StarRow(QWidget):
    """Fila de estrellas; las conseguidas van en dorado."""

    def __init__(self, earned: int = 0, total: int = 3, size: int = 34,
                 parent=None) -> None:
        super().__init__(parent)
        self.earned = earned
        self.total = total
        self.size = size
        self.setFixedHeight(size + 6)
        self.setMinimumWidth(total * (size + 6))

    def set_earned(self, value: int) -> None:
        self.earned = value
        self.update()

    def paintEvent(self, _e) -> None:
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        for i in range(self.total):
            cx = self.size / 2 + i * (self.size + 6)
            cy = self.height() / 2
            filled = i < self.earned
            _draw_star(p, cx, cy, self.size / 2,
                       QColor(T.C.sun if filled else T.C.surface_highest),
                       QColor(T.C.sun_bevel if filled else T.C.outline_variant))
        p.end()


def _draw_star(p: QPainter, cx: float, cy: float, r: float,
               fill: QColor, stroke: QColor) -> None:
    import math
    path = QPainterPath()
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rad = r if i % 2 == 0 else r * 0.45
        x, y = cx + rad * math.cos(ang), cy + rad * math.sin(ang)
        if i == 0:
            path.moveTo(x, y)
        else:
            path.lineTo(x, y)
    path.closeSubpath()
    p.setBrush(QBrush(fill))
    p.setPen(QPen(stroke, 2.5))
    p.drawPath(path)


class ProgressPill(QWidget):
    """Barra de progreso gruesa con degradado, como en el prototipo."""

    def __init__(self, value: float = 0.0, height: int = 26,
                 colors: tuple[str, str] | None = None, parent=None) -> None:
        super().__init__(parent)
        self._value = max(0.0, min(1.0, value))
        self._h = height
        self.colors = colors or (T.C.sky, T.C.sun)
        self.setFixedHeight(height)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

    def set_value(self, v: float) -> None:
        self._value = max(0.0, min(1.0, v))
        self.update()

    def value(self) -> float:
        return self._value

    def paintEvent(self, _e) -> None:
        from PySide6.QtGui import QLinearGradient
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        r = self._h / 2
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(QColor(T.C.surface_highest))
        p.drawRoundedRect(QRectF(0, 0, self.width(), self._h), r, r)
        w = max(self._h, self.width() * self._value) if self._value > 0 else 0
        if w:
            g = QLinearGradient(0, 0, w, 0)
            g.setColorAt(0.0, QColor(self.colors[0]))
            g.setColorAt(1.0, QColor(self.colors[1]))
            p.setBrush(QBrush(g))
            p.drawRoundedRect(QRectF(0, 0, w, self._h), r, r)
        p.end()


class Title(QLabel):
    def __init__(self, text: str, size: int = 32, color: str = T.C.on_surface,
                 parent=None) -> None:
        super().__init__(text, parent)
        self.setFont(T.font(size, display=True))
        # El fondo transparente es necesario: en cuanto una QLabel recibe hoja
        # de estilo, Qt pinta su fondo con el color base de la paleta y aparece
        # un rectángulo blanco sobre la tarjeta.
        self.setStyleSheet(f"color: {color}; background: transparent;")
        self.setWordWrap(True)
        # Sin esto, una etiqueta con ajuste de línea se queda con todo el
        # espacio vertical sobrante de la columna y deja huecos enormes.
        self.setSizePolicy(QSizePolicy.Policy.Preferred,
                           QSizePolicy.Policy.Maximum)


class Body(QLabel):
    def __init__(self, text: str, size: int = 16,
                 color: str = T.C.on_surface_variant, parent=None) -> None:
        super().__init__(text, parent)
        self.setFont(T.font(size, bold=False))
        self.setStyleSheet(f"color: {color}; background: transparent;")
        self.setWordWrap(True)
        self.setSizePolicy(QSizePolicy.Policy.Preferred,
                           QSizePolicy.Policy.Maximum)


def row(*widgets, spacing: int = 12, margins: tuple = (0, 0, 0, 0)) -> QWidget:
    w = QWidget()
    lay = QHBoxLayout(w)
    lay.setContentsMargins(*margins)
    lay.setSpacing(spacing)
    for item in widgets:
        if item is None:
            lay.addStretch(1)
        elif isinstance(item, int):
            lay.addSpacing(item)
        else:
            lay.addWidget(item)
    return w


def column(*widgets, spacing: int = 12, margins: tuple = (0, 0, 0, 0)) -> QWidget:
    w = QWidget()
    lay = QVBoxLayout(w)
    lay.setContentsMargins(*margins)
    lay.setSpacing(spacing)
    for item in widgets:
        if item is None:
            lay.addStretch(1)
        elif isinstance(item, int):
            lay.addSpacing(item)
        else:
            lay.addWidget(item)
    return w
