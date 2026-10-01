"""Dibujo animado de una seña a partir de sus puntos de referencia.

No hacen falta ilustraciones fijas: la seña que se muestra al niño es
exactamente la que él mismo calibró, redibujada con una respiración suave, un
brillo que recorre las puntas de los dedos y un halo de color de fondo. Así la
ayuda se siente viva ("chévere") sin dejar de coincidir con lo que el
reconocedor espera ver — que es la propiedad que de verdad importa para que la
pista no confunda al niño.
"""

from __future__ import annotations

import math

import numpy as np
from PySide6.QtCore import QPointF, QRectF, Qt, QTimer
from PySide6.QtGui import QColor, QPainter, QPen
from PySide6.QtWidgets import QSizePolicy, QWidget

from ...vision.detector import CONNECTIONS
from .. import theme as T

DEDOS = {
    "pulgar": ((0, 1, 2, 3, 4), "#FF9F1C"),
    "indice": ((0, 5, 6, 7, 8), "#38B6FF"),
    "medio": ((5, 9, 10, 11, 12), "#7A5CFA"),
    "anular": ((9, 13, 14, 15, 16), "#2EC4B6"),
    "menique": ((13, 17, 18, 19, 20), "#FF6B8B"),
}


def _layout_hands(hands: list[dict]) -> list[np.ndarray]:
    """Devuelve los puntos de cada mano en un plano común.

    Las calibraciones de la versión 1 traen ambas manos centradas en su propia
    muñeca, de modo que se superpondrían; en ese caso se separan a izquierda y
    derecha según su etiqueta.
    """
    puntos = [np.asarray(h["landmarks"], dtype=float)[:, :2] for h in hands]
    if len(puntos) < 2:
        return puntos
    muñecas = [p[0] for p in puntos]
    if float(np.linalg.norm(muñecas[0] - muñecas[1])) < 1e-6:
        escala = max(float(np.abs(p - p[0]).max()) for p in puntos) or 1.0
        for i, h in enumerate(hands):
            lado = -1.0 if str(h.get("hand_label", "")).startswith("L") else 1.0
            puntos[i] = puntos[i] + np.array([lado * escala * 1.25, 0.0])
    return puntos


class HandSignView(QWidget):
    """Esquema de una o dos manos."""

    def __init__(self, hands: list[dict] | None = None, parent=None, *,
                 min_height: int = 150, line_width: float = 7.0,
                 show_dots: bool = True, tint: str | None = None,
                 animated: bool = True) -> None:
        super().__init__(parent)
        self._hands = hands or []
        self.line_width = line_width
        self.show_dots = show_dots
        self.tint = tint
        self._phase = 0.0
        self.setMinimumHeight(min_height)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._tick)
        if animated:
            self._timer.start(45)

    def set_hands(self, hands: list[dict] | None) -> None:
        self._hands = hands or []
        self.update()

    def _tick(self) -> None:
        if self._hands:
            self._phase += 0.09
            self.update()

    @property
    def has_pose(self) -> bool:
        return bool(self._hands)

    def paintEvent(self, _e) -> None:
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        if not self._hands:
            p.setPen(QColor(T.C.outline_variant))
            p.setFont(T.font(15, bold=False))
            p.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter,
                       "Sin seña calibrada")
            p.end()
            return

        puntos = _layout_hands(self._hands)
        todos = np.vstack(puntos)
        minimo, maximo = todos.min(axis=0), todos.max(axis=0)
        extent = np.maximum(maximo - minimo, 1e-6)
        margen = 16
        disponible = np.array([self.width() - 2 * margen,
                               self.height() - 2 * margen], dtype=float)
        escala = float(min(disponible / extent))
        centro = (minimo + maximo) / 2.0
        centro_widget = np.array([self.width() / 2.0, self.height() / 2.0])

        # Respiración suave: toda la seña crece y encoge un poquito, como si
        # estuviera viva en vez de ser un diagrama estático.
        respiracion = 1.0 + 0.025 * math.sin(self._phase)

        def mapear(v: np.ndarray) -> QPointF:
            xy = centro_widget + ((v - centro) * escala * respiracion)
            return QPointF(float(xy[0]), float(xy[1]))

        # Halo de color detrás de la mano, que pulsa despacio: da la sensación
        # de "imagen animada" sin depender de ilustraciones externas.
        halo = QColor(self.tint or T.C.sun)
        halo.setAlpha(int(26 + 14 * (0.5 + 0.5 * math.sin(self._phase * 0.8))))
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(halo)
        radio_halo = min(self.width(), self.height()) / 2.0 - 4
        p.drawEllipse(QRectF(centro_widget[0] - radio_halo,
                             centro_widget[1] - radio_halo,
                             2 * radio_halo, 2 * radio_halo))

        for pts in puntos:
            # Contorno oscuro para que el esquema se lea sobre cualquier fondo.
            p.setPen(QPen(QColor(T.C.on_surface), self.line_width + 5,
                          Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap,
                          Qt.PenJoinStyle.RoundJoin))
            for a, b in CONNECTIONS:
                p.drawLine(mapear(pts[a]), mapear(pts[b]))

            for nombre, (cadena, color) in DEDOS.items():
                p.setPen(QPen(QColor(self.tint or color), self.line_width,
                              Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap,
                              Qt.PenJoinStyle.RoundJoin))
                for i in range(len(cadena) - 1):
                    p.drawLine(mapear(pts[cadena[i]]), mapear(pts[cadena[i + 1]]))

            if self.show_dots:
                r = max(3.0, self.line_width * 0.55)
                puntas = (4, 8, 12, 16, 20)
                for i, idx in enumerate(puntas):
                    # Un brillo recorre las puntas de los dedos una a una,
                    # como una animación de "encendido" en bucle.
                    encendida = (int(self._phase / 0.55) % len(puntas)) == i
                    c = mapear(pts[idx])
                    if encendida:
                        p.setPen(Qt.PenStyle.NoPen)
                        p.setBrush(QColor(T.C.sun))
                        p.drawEllipse(QRectF(c.x() - r - 3, c.y() - r - 3,
                                             2 * r + 6, 2 * r + 6))
                    p.setPen(QPen(QColor(T.C.on_surface), 2))
                    p.setBrush(QColor(T.C.white))
                    p.drawEllipse(QRectF(c.x() - r, c.y() - r, 2 * r, 2 * r))
                muñeca = mapear(pts[0])
                p.setPen(QPen(QColor(T.C.on_surface), 2))
                p.setBrush(QColor(T.C.sun))
                p.drawEllipse(QRectF(muñeca.x() - r - 2, muñeca.y() - r - 2,
                                     2 * r + 4, 2 * r + 4))
        p.end()
