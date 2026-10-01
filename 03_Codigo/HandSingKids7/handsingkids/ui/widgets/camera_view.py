"""Visor de cámara con superposiciones.

Muestra el vídeo recortado dentro de un marco redondeado y dibuja encima el
esqueleto de las manos detectadas, las insignias de detección y el anillo de
confirmación. Toda la información que el niño necesita está sobre la imagen, sin
menús ni cifras.
"""

from __future__ import annotations

import numpy as np
from PySide6.QtCore import QPointF, QRectF, Qt
from PySide6.QtGui import (QBrush, QColor, QImage, QPainter, QPainterPath, QPen,
                           QPixmap)
from PySide6.QtWidgets import QSizePolicy, QWidget

from ...vision.detector import CONNECTIONS
from .. import theme as T


class CameraView(QWidget):
    """Área principal de juego."""

    def __init__(self, parent=None, *, radius: int = 28,
                 border: str = T.C.violet, border_width: int = 5) -> None:
        super().__init__(parent)
        self.radius = radius
        self.border = border
        self.border_width = border_width
        self._pix: QPixmap | None = None
        self._hands: list[dict] = []
        self._mirrored = True
        self.show_skeleton = True
        self.placeholder = "Preparando la cámara…"
        self.badge_left = False
        self.badge_right = False
        self.ring_value = 0.0
        self.ring_label = ""
        self.ring_color = T.C.sky
        self.flash: tuple[str, float] | None = None   # (color, intensidad)
        self.setMinimumSize(420, 260)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    # ------------------------------------------------------------ entrada
    def set_frame(self, frame: np.ndarray | None, hands: list[dict] | None,
                  mirrored: bool = True) -> None:
        if frame is not None:
            h, w, _ = frame.shape
            img = QImage(frame.data, w, h, 3 * w, QImage.Format.Format_RGB888)
            self._pix = QPixmap.fromImage(img.copy())
        self._hands = hands or []
        self._mirrored = mirrored
        self.badge_left = any(h.get("hand_label") == "Left" for h in self._hands)
        self.badge_right = any(h.get("hand_label") == "Right" for h in self._hands)
        self.update()

    def set_ring(self, value: float, label: str = "",
                 color: str | None = None) -> None:
        self.ring_value = max(0.0, min(1.0, value))
        self.ring_label = label
        if color:
            self.ring_color = color
        self.update()

    def set_flash(self, color: str | None, intensity: float = 0.35) -> None:
        self.flash = (color, intensity) if color else None
        self.update()

    def clear(self) -> None:
        self._pix = None
        self._hands = []
        self.update()

    # ------------------------------------------------------------- dibujo
    def paintEvent(self, _e) -> None:
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        area = QRectF(self.border_width / 2, self.border_width / 2,
                      self.width() - self.border_width,
                      self.height() - self.border_width)
        recorte = QPainterPath()
        recorte.addRoundedRect(area, self.radius, self.radius)
        p.save()
        p.setClipPath(recorte)

        if self._pix is None:
            p.fillRect(area, QColor(T.C.surface_high))
            p.setPen(QColor(T.C.on_surface_variant))
            p.setFont(T.font(18, bold=False))
            p.drawText(area, Qt.AlignmentFlag.AlignCenter, self.placeholder)
        else:
            destino = self._fitted(area)
            p.drawPixmap(destino, self._pix,
                         QRectF(0, 0, self._pix.width(), self._pix.height()))
            self._draw_hands(p, destino)

        if self.flash:
            color, fuerza = self.flash
            c = QColor(color)
            c.setAlphaF(max(0.0, min(0.85, fuerza)))
            p.fillRect(area, c)
        p.restore()

        p.setPen(QPen(QColor(self.border), self.border_width))
        p.setBrush(Qt.BrushStyle.NoBrush)
        p.drawRoundedRect(area, self.radius, self.radius)

        self._draw_badges(p, area)
        if self.ring_value > 0 or self.ring_label:
            self._draw_ring(p, area)
        p.end()

    def _fitted(self, area: QRectF) -> QRectF:
        """Escala la imagen para llenar el marco sin deformarla."""
        assert self._pix is not None
        pw, ph = self._pix.width(), self._pix.height()
        if pw == 0 or ph == 0:
            return area
        escala = max(area.width() / pw, area.height() / ph)
        w, h = pw * escala, ph * escala
        return QRectF(area.center().x() - w / 2, area.center().y() - h / 2, w, h)

    def _draw_hands(self, p: QPainter, destino: QRectF) -> None:
        if not self.show_skeleton or not self._hands:
            return
        for mano in self._hands:
            pts = np.asarray(mano["landmarks"], dtype=float)
            es_izq = mano.get("hand_label") == "Left"
            color = QColor(T.C.mint if es_izq else T.C.sun)

            def mapear(i: int) -> QPointF:
                x, y = float(pts[i][0]), float(pts[i][1])
                if self._mirrored:
                    x = 1.0 - x
                return QPointF(destino.left() + x * destino.width(),
                               destino.top() + y * destino.height())

            p.setPen(QPen(QColor(0, 0, 0, 110), 8, Qt.PenStyle.SolidLine,
                          Qt.PenCapStyle.RoundCap))
            for a, b in CONNECTIONS:
                p.drawLine(mapear(a), mapear(b))
            p.setPen(QPen(color, 4.5, Qt.PenStyle.SolidLine,
                          Qt.PenCapStyle.RoundCap))
            for a, b in CONNECTIONS:
                p.drawLine(mapear(a), mapear(b))
            p.setPen(QPen(QColor(255, 255, 255, 220), 2))
            p.setBrush(QBrush(color))
            for i in (4, 8, 12, 16, 20):
                c = mapear(i)
                p.drawEllipse(QRectF(c.x() - 6, c.y() - 6, 12, 12))

    def _draw_badges(self, p: QPainter, area: QRectF) -> None:
        etiquetas = [("Manita izquierda", self.badge_left, T.C.mint),
                     ("Manita derecha", self.badge_right, T.C.sun)]
        x = area.left() + 16
        y = area.top() + 16
        p.setFont(T.label_md())
        for texto, activa, color in etiquetas:
            fm = p.fontMetrics()
            w = fm.horizontalAdvance(texto) + 54
            caja = QRectF(x, y, w, 40)
            p.setPen(Qt.PenStyle.NoPen)
            p.setBrush(QColor(255, 248, 244, 235) if activa
                       else QColor(255, 248, 244, 150))
            p.drawRoundedRect(caja, 20, 20)
            p.setBrush(QColor(color) if activa else QColor(T.C.outline_variant))
            p.drawEllipse(QRectF(caja.left() + 13, caja.center().y() - 7, 14, 14))
            p.setPen(QColor(T.C.on_surface if activa else T.C.outline))
            p.drawText(caja.adjusted(38, 0, -8, 0),
                       Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft,
                       texto)
            x += w + 10

    def _draw_ring(self, p: QPainter, area: QRectF) -> None:
        d = 118.0
        caja = QRectF(area.right() - d - 22, area.bottom() - d - 22, d, d)
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(QColor(255, 248, 244, 225))
        p.drawEllipse(caja)
        grosor = 11
        interior = caja.adjusted(grosor / 2 + 3, grosor / 2 + 3,
                                 -grosor / 2 - 3, -grosor / 2 - 3)
        p.setPen(QPen(QColor(T.C.surface_highest), grosor))
        p.setBrush(Qt.BrushStyle.NoBrush)
        p.drawEllipse(interior)
        if self.ring_value > 0:
            p.setPen(QPen(QColor(self.ring_color), grosor, Qt.PenStyle.SolidLine,
                          Qt.PenCapStyle.RoundCap))
            p.drawArc(interior, 90 * 16, int(-360 * 16 * self.ring_value))
        if self.ring_label:
            p.setPen(QColor(T.C.on_surface))
            p.setFont(T.font(30, display=True))
            p.drawText(caja, Qt.AlignmentFlag.AlignCenter, self.ring_label)
