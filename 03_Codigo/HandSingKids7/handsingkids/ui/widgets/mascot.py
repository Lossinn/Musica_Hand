"""Kiki, la iguana compañera de ritmo.

Dibujo vectorial propio hecho con QPainter: no hay imágenes externas, así que
la aplicación funciona sin conexión y el personaje escala a cualquier tamaño sin
perder nitidez. Cambia de gesto según el momento del juego.
"""

from __future__ import annotations

import math
from enum import Enum

from PySide6.QtCore import QPointF, QRectF, Qt, QTimer
from PySide6.QtGui import QBrush, QColor, QPainter, QPainterPath, QPen
from PySide6.QtWidgets import QSizePolicy, QWidget

from .. import theme as T

VERDE = "#5FBF6A"
VERDE_OSCURO = "#3D9450"
VERDE_CLARO = "#8FDC94"
PANZA = "#DFF5D8"
CRESTA = "#F2A33C"


class Mood(str, Enum):
    IDLE = "tranquila"
    HAPPY = "contenta"
    CHEER = "celebrando"
    THINKING = "pensando"
    SLEEPY = "dormida"


class MascotView(QWidget):
    """La mascota, con una animación de respiración muy suave."""

    def __init__(self, mood: Mood = Mood.IDLE, size: int = 180,
                 animated: bool = True, parent=None) -> None:
        super().__init__(parent)
        self.mood = mood
        self._phase = 0.0
        self.setFixedSize(size, size)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._tick)
        if animated:
            self._timer.start(60)

    def set_mood(self, mood: Mood) -> None:
        self.mood = mood
        self.update()

    def celebrate(self, ms: int = 2200) -> None:
        previous = self.mood
        self.set_mood(Mood.CHEER)
        QTimer.singleShot(ms, lambda: self.set_mood(previous))

    def _tick(self) -> None:
        self._phase += 0.09
        self.update()

    # ------------------------------------------------------------- dibujo
    def paintEvent(self, _e) -> None:
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        s = min(self.width(), self.height())
        p.translate(self.width() / 2, self.height() / 2)
        p.scale(s / 200.0, s / 200.0)

        bob = math.sin(self._phase) * 3.0
        shake = math.sin(self._phase * 2.6) * (9.0 if self.mood == Mood.CHEER else 2.0)
        p.translate(0, bob)

        # El orden importa: cola y cuerpo al fondo, luego los brazos con las
        # maracas, y la cabeza con su cresta encima de todo.
        self._shadow(p)
        self._tail(p)
        self._body(p)
        self._arms(p, shake)
        self._head(p)
        self._crest(p)
        p.end()

    def _shadow(self, p: QPainter) -> None:
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(QColor(115, 100, 81, 34))
        p.drawEllipse(QRectF(-52, 74, 104, 16))

    def _body(self, p: QPainter) -> None:
        p.setPen(QPen(QColor(VERDE_OSCURO), 4))
        p.setBrush(QColor(VERDE))
        p.drawRoundedRect(QRectF(-44, -6, 88, 84), 40, 40)
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(QColor(PANZA))
        p.drawRoundedRect(QRectF(-26, 14, 52, 54), 26, 26)
        # Chaleco de rayas, guiño a la vestimenta festiva.
        p.setBrush(QColor(CRESTA))
        for i, x in enumerate((-40, -30)):
            p.drawRoundedRect(QRectF(x, 6, 6, 44), 3, 3)
        p.setBrush(QColor(T.C.bubblegum))
        p.drawRoundedRect(QRectF(32, 6, 6, 44), 3, 3)

    def _crest(self, p: QPainter) -> None:
        """Púas naranjas a lo largo de la coronilla."""
        p.setPen(QPen(QColor("#D98A22"), 3))
        p.setBrush(QColor(CRESTA))
        path = QPainterPath()
        for i in range(5):
            x = -30 + i * 15
            alto = 16 - abs(i - 2) * 3
            path.moveTo(x - 7, -68)
            path.lineTo(x, -68 - alto)
            path.lineTo(x + 7, -68)
            path.closeSubpath()
        p.drawPath(path)

    def _tail(self, p: QPainter) -> None:
        p.setPen(QPen(QColor(VERDE_OSCURO), 4))
        p.setBrush(QColor(VERDE_CLARO))
        path = QPainterPath()
        path.moveTo(30, 48)
        path.cubicTo(84, 56, 96, 20, 70, 2)
        path.cubicTo(88, 26, 76, 52, 30, 70)
        path.closeSubpath()
        p.drawPath(path)

    def _arms(self, p: QPainter, shake: float) -> None:
        for side, extra in ((-1, shake), (1, -shake)):
            p.save()
            p.translate(side * 50, 14)
            p.rotate(side * (26 + extra))
            p.setPen(QPen(QColor(VERDE_OSCURO), 4))
            p.setBrush(QColor(VERDE))
            p.drawRoundedRect(QRectF(-7, -6, 14, 34), 7, 7)
            # Maraca
            p.setBrush(QColor(T.C.tangerine))
            p.drawEllipse(QRectF(-14, 24, 28, 28))
            p.setPen(Qt.PenStyle.NoPen)
            p.setBrush(QColor("#FFE7B8"))
            p.drawEllipse(QRectF(-7, 29, 9, 8))
            p.setBrush(QColor(T.C.bubblegum))
            for k in range(3):
                p.drawEllipse(QRectF(-10 + k * 8, 40, 5, 5))
            p.restore()

    def _head(self, p: QPainter) -> None:
        p.setPen(QPen(QColor(VERDE_OSCURO), 4))
        p.setBrush(QColor(VERDE_CLARO))
        p.drawRoundedRect(QRectF(-42, -74, 84, 72), 34, 34)
        # Hocico
        p.setBrush(QColor(VERDE))
        p.drawRoundedRect(QRectF(-24, -30, 48, 26), 13, 13)

        durmiendo = self.mood == Mood.SLEEPY
        cerrados = self.mood == Mood.CHEER
        for cx in (-18.0, 18.0):
            p.setPen(Qt.PenStyle.NoPen)
            if durmiendo or cerrados:
                p.setPen(QPen(QColor("#2E5B36"), 4, Qt.PenStyle.SolidLine,
                              Qt.PenCapStyle.RoundCap))
                p.drawArc(QRectF(cx - 11, -56, 22, 16), 0, 180 * 16)
                p.setPen(Qt.PenStyle.NoPen)
                continue
            p.setBrush(QColor("#FFFFFF"))
            p.drawEllipse(QRectF(cx - 12, -60, 24, 26))
            mira = 3.0 if self.mood == Mood.THINKING else 0.0
            p.setBrush(QColor("#2E3A2F"))
            p.drawEllipse(QRectF(cx - 5 + mira, -52, 11, 13))
            p.setBrush(QColor("#FFFFFF"))
            p.drawEllipse(QRectF(cx - 2 + mira, -50, 4, 4))

        # Mejillas
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(QColor(255, 140, 160, 120))
        p.drawEllipse(QRectF(-38, -34, 18, 12))
        p.drawEllipse(QRectF(20, -34, 18, 12))

        # Fosas nasales
        p.setBrush(QColor("#2E5B36"))
        p.drawEllipse(QRectF(-9, -24, 5, 4))
        p.drawEllipse(QRectF(4, -24, 5, 4))

        # Boca
        p.setPen(QPen(QColor("#2E5B36"), 4, Qt.PenStyle.SolidLine,
                      Qt.PenCapStyle.RoundCap))
        p.setBrush(Qt.BrushStyle.NoBrush)
        if self.mood in (Mood.HAPPY, Mood.CHEER):
            p.drawArc(QRectF(-16, -22, 32, 20), 200 * 16, 140 * 16)
        elif self.mood == Mood.THINKING:
            p.drawLine(QPointF(-8, -12), QPointF(8, -14))
        elif self.mood == Mood.SLEEPY:
            p.drawArc(QRectF(-10, -18, 20, 14), 200 * 16, 140 * 16)
        else:
            p.drawArc(QRectF(-14, -20, 28, 16), 210 * 16, 120 * 16)

        if self.mood == Mood.CHEER:
            p.setPen(QPen(QColor(T.C.sun), 5, Qt.PenStyle.SolidLine,
                          Qt.PenCapStyle.RoundCap))
            for ang in (-60, -20, 20, 60):
                r = math.radians(ang - 90)
                p.drawLine(QPointF(58 * math.cos(r), -60 + 18 * math.sin(r)),
                           QPointF(70 * math.cos(r), -66 + 22 * math.sin(r)))


class MascotBubble(QWidget):
    """Globo de diálogo con la punta hacia la mascota."""

    def __init__(self, text: str = "", parent=None) -> None:
        super().__init__(parent)
        self._text = text
        self.setMinimumHeight(96)
        self.setMaximumHeight(160)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)

    def set_text(self, text: str) -> None:
        self._text = text
        self.update()

    def text(self) -> str:
        return self._text

    def paintEvent(self, _e) -> None:
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        w, h = self.width(), self.height()
        cuerpo = QRectF(2, 2, w - 4, h - 18)
        p.setPen(QPen(QColor(T.C.outline_variant), 3))
        p.setBrush(QColor(T.C.white))
        p.drawRoundedRect(cuerpo, 22, 22)
        punta = QPainterPath()
        punta.moveTo(44, cuerpo.bottom() - 2)
        punta.lineTo(30, h - 2)
        punta.lineTo(70, cuerpo.bottom() - 2)
        punta.closeSubpath()
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(QColor(T.C.white))
        p.drawPath(punta)
        p.setPen(QPen(QColor(T.C.outline_variant), 3))
        p.drawLine(QPointF(44, cuerpo.bottom()), QPointF(30, h - 3))
        p.drawLine(QPointF(30, h - 3), QPointF(70, cuerpo.bottom()))
        p.setPen(QColor(T.C.on_surface))
        p.setFont(T.font(17, bold=False))
        p.drawText(cuerpo.adjusted(20, 10, -20, -10),
                   Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft |
                   Qt.TextFlag.TextWordWrap, self._text)
        p.end()
