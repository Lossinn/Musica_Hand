"""Representación visual de las notas y de la secuencia del ejercicio."""

from __future__ import annotations

import math
from enum import Enum

from PySide6.QtCore import QPointF, QRectF, Qt, QTimer
from PySide6.QtGui import QColor, QPainter, QPainterPath, QPen
from PySide6.QtWidgets import QHBoxLayout, QSizePolicy, QWidget

from ...domain.notes import BY_CODE, SILENCE, solfa
from .. import theme as T
from .gesture_images import gesture_pixmap


class NoteState(str, Enum):
    PENDING = "pendiente"
    CURRENT = "actual"
    DONE = "hecha"
    MISSED = "fallada"


class NoteBubble(QWidget):
    """Burbuja con el nombre cantado de la nota.

    Se usa en toda la aplicación donde una nota se representa como un
    círculo suelto: la pista del ejercicio guiado, la fila de referencia de
    Modo libre y la fila de notas de la Calibración. Si existe la
    ilustración genérica de la seña (ver `.gesture_images`), se dibuja
    dentro del círculo en vez del nombre cantado — igual que ya hacían las
    burbujas viajeras de Canciones — mientras la nota esté pendiente o sea
    la actual; una vez juzgada (acertada o fallada), vuelve a mostrarse el
    color y el nombre para que ese resultado se lea sin ambigüedad."""

    def __init__(self, code: str, state: NoteState = NoteState.PENDING,
                 size: int = 74, parent=None) -> None:
        super().__init__(parent)
        self.code = code
        self.state = state
        self._size = size
        self._pulse = 0.0
        self.setFixedSize(size, size + 8)
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._tick)

    def set_state(self, state: NoteState) -> None:
        self.state = state
        if state == NoteState.CURRENT:
            self._timer.start(55)
        else:
            self._timer.stop()
            self._pulse = 0.0
        self.update()

    def _tick(self) -> None:
        self._pulse += 0.14
        self.update()

    def paintEvent(self, _e) -> None:
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        base = QColor(T.NOTE_COLORS.get(self.code, T.C.sky))
        borde = base.darker(135)

        if self.state == NoteState.PENDING:
            cara, linea, texto = QColor(T.C.surface_highest), QColor(T.C.outline_variant), QColor(T.C.outline)
        elif self.state == NoteState.DONE:
            cara, linea, texto = QColor(T.C.mint), QColor(T.C.mint_bevel), QColor("#FFFFFF")
        elif self.state == NoteState.MISSED:
            cara, linea, texto = QColor(T.C.surface_high), QColor(T.C.bubblegum), QColor(T.C.bubblegum_bevel)
        else:
            cara, linea, texto = base, borde, QColor("#FFFFFF")

        escala = 1.0 + (0.06 * math.sin(self._pulse)
                        if self.state == NoteState.CURRENT else 0.0)
        d = self._size * escala
        x = (self.width() - d) / 2
        y = (self.height() - 8 - d) / 2

        if self.state == NoteState.CURRENT:
            halo = QColor(base)
            halo.setAlpha(70)
            p.setPen(Qt.PenStyle.NoPen)
            p.setBrush(halo)
            p.drawEllipse(QRectF(x - 8, y - 8 + 4, d + 16, d + 16))

        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(linea)
        p.drawEllipse(QRectF(x, y + 6, d, d))
        p.setBrush(cara)
        p.setPen(QPen(linea, 3))
        p.drawEllipse(QRectF(x, y, d, d))

        pix = (gesture_pixmap(self.code)
              if self.state in (NoteState.PENDING, NoteState.CURRENT) else None)
        if pix is not None:
            p.save()
            recorte = QPainterPath()
            recorte.addEllipse(QRectF(x, y, d, d).adjusted(3, 3, -3, -3))
            p.setClipPath(recorte)
            p.drawPixmap(QRectF(x, y, d, d).adjusted(2, 2, -2, -2).toRect(), pix)
            p.restore()
        else:
            p.setPen(texto)
            p.setFont(T.font(int(d * 0.33), display=True))
            p.drawText(QRectF(x, y, d, d), Qt.AlignmentFlag.AlignCenter,
                       solfa(self.code))
        if self.state == NoteState.DONE:
            # Insignia en la esquina, para no tapar el nombre de la nota.
            br = d * 0.30
            bx, by = x + d - br * 0.95, y + d - br * 0.95
            p.setPen(QPen(QColor("#FFFFFF"), 2.5))
            p.setBrush(QColor(T.C.mint_bevel))
            p.drawEllipse(QRectF(bx - br / 2, by - br / 2, br, br))
            p.setPen(QPen(QColor("#FFFFFF"), 3, Qt.PenStyle.SolidLine,
                          Qt.PenCapStyle.RoundCap))
            p.drawLine(QPointF(bx - br * 0.22, by),
                       QPointF(bx - br * 0.05, by + br * 0.18))
            p.drawLine(QPointF(bx - br * 0.05, by + br * 0.18),
                       QPointF(bx + br * 0.24, by - br * 0.20))
        p.end()


class NoteTrack(QWidget):
    """Secuencia de notas del ejercicio, con la actual destacada."""

    def __init__(self, sequence: list[str] | None = None, bubble: int = 74,
                 parent=None) -> None:
        super().__init__(parent)
        self._bubble = bubble
        self._bubbles: list[NoteBubble] = []
        self._lay = QHBoxLayout(self)
        self._lay.setContentsMargins(0, 0, 0, 0)
        self._lay.setSpacing(12)
        self._lay.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setFixedHeight(bubble + 20)
        if sequence:
            self.set_sequence(sequence)

    def set_sequence(self, sequence: list[str], window: int = 7) -> None:
        while self._lay.count():
            item = self._lay.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self._bubbles = []
        for code in sequence[:window]:
            b = NoteBubble(code, NoteState.PENDING, self._bubble)
            self._bubbles.append(b)
            self._lay.addWidget(b)

    def set_current(self, index: int) -> None:
        for i, b in enumerate(self._bubbles):
            if i < index:
                b.set_state(NoteState.DONE)
            elif i == index:
                b.set_state(NoteState.CURRENT)
            else:
                b.set_state(NoteState.PENDING)

    def mark(self, index: int, state: NoteState) -> None:
        if 0 <= index < len(self._bubbles):
            self._bubbles[index].set_state(state)


class ConfirmRing(QWidget):
    """Anillo que se llena mientras el niño sostiene la seña.

    Es la traducción visual del filtro temporal: lo que el estabilizador
    necesita para confirmar, el niño lo ve como un círculo que se completa.
    """

    def __init__(self, diameter: int = 92, parent=None) -> None:
        super().__init__(parent)
        self._d = diameter
        self._value = 0.0
        self._label = ""
        self._color = T.C.sky
        self.setFixedSize(diameter, diameter)

    def set_progress(self, value: float, label: str = "",
                     color: str | None = None) -> None:
        self._value = max(0.0, min(1.0, value))
        self._label = label
        if color:
            self._color = color
        self.update()

    def paintEvent(self, _e) -> None:
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        grosor = 9
        caja = QRectF(grosor / 2 + 1, grosor / 2 + 1,
                      self._d - grosor - 2, self._d - grosor - 2)
        p.setPen(QPen(QColor(T.C.surface_highest), grosor))
        p.drawEllipse(caja)
        if self._value > 0:
            p.setPen(QPen(QColor(self._color), grosor, Qt.PenStyle.SolidLine,
                          Qt.PenCapStyle.RoundCap))
            p.drawArc(caja, 90 * 16, int(-360 * 16 * self._value))
        if self._label:
            p.setPen(QColor(T.C.on_surface))
            p.setFont(T.font(int(self._d * 0.26), display=True))
            p.drawText(caja, Qt.AlignmentFlag.AlignCenter, self._label)
        p.end()


class Staff(QWidget):
    """Pentagrama sencillo: sitúa las notas en su altura real.

    No se usa con los más pequeños, pero a partir de los ocho años ayuda a
    ligar el gesto con la escritura musical.
    """

    def __init__(self, sequence: list[str] | None = None, parent=None) -> None:
        super().__init__(parent)
        self.sequence = sequence or []
        self.current = -1
        self.setMinimumHeight(170)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

    def set_sequence(self, seq: list[str]) -> None:
        self.sequence = list(seq)
        self.update()

    def set_current(self, index: int) -> None:
        self.current = index
        self.update()

    def paintEvent(self, _e) -> None:
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        w, h = self.width(), self.height()
        margen = 30
        sep = 16
        centro = h / 2 - 10
        # Cinco líneas del pentagrama.
        p.setPen(QPen(QColor(T.C.outline_variant), 2.5))
        for i in range(5):
            y = centro - 2 * sep + i * sep
            p.drawLine(QPointF(margen, y), QPointF(w - margen, y))

        if not self.sequence:
            p.end()
            return

        # staff_step 0 corresponde a la primera línea adicional inferior.
        base_y = centro + 3 * sep
        n = len(self.sequence)
        paso = (w - 2 * margen - 40) / max(1, n)
        for i, code in enumerate(self.sequence):
            x = margen + 30 + i * paso
            if code == SILENCE:
                # Un silencio se dibuja como una pausa sobre la línea central,
                # no como una nota: así se distingue de un DO sin confundirse.
                actual = (i == self.current)
                color = QColor(T.C.mint if i < self.current
                               else (T.C.outline if actual else T.C.outline_variant))
                p.setPen(QPen(color.darker(120), 3, Qt.PenStyle.SolidLine,
                              Qt.PenCapStyle.RoundCap))
                p.drawLine(QPointF(x - 9, centro), QPointF(x + 9, centro))
                p.setPen(QColor(T.C.on_surface_variant))
                p.setFont(T.font(12, display=True))
                p.drawText(QRectF(x - 24, centro + 14, 48, 18),
                           Qt.AlignmentFlag.AlignCenter, "silencio")
                continue
            nota = BY_CODE.get(code)
            if nota is None:
                continue
            y = base_y - nota.staff_step * (sep / 2)
            actual = (i == self.current)
            color = QColor(T.NOTE_COLORS.get(code, T.C.sky))
            if i < self.current:
                color = QColor(T.C.mint)
            elif not actual:
                color = QColor(T.C.outline_variant)
            # Línea adicional para el do grave.
            if nota.staff_step == 0:
                p.setPen(QPen(QColor(T.C.outline_variant), 2.5))
                p.drawLine(QPointF(x - 17, y), QPointF(x + 17, y))
            p.setPen(QPen(color.darker(130), 2.5))
            p.setBrush(color)
            r = 12 if actual else 10
            p.drawEllipse(QRectF(x - r, y - r * 0.8, 2 * r, 1.6 * r))
            p.setPen(QColor(T.C.on_surface_variant))
            p.setFont(T.font(12, display=True))
            p.drawText(QRectF(x - 24, y + 14, 48, 18),
                       Qt.AlignmentFlag.AlignCenter, solfa(code))
        p.end()
