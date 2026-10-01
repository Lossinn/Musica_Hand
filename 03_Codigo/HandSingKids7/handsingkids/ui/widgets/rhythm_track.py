"""Pista de nota viajera: la mecánica de "Notas Rítmicas" de la primera
versión de la aplicación, con el estilo visual de las burbujas de nota que ya
existían (mismos colores, mismo nombre cantado), viajando de derecha a
izquierda hacia una línea de impacto fija — igual que en un juego de ritmo
clásico. La lógica de cuándo llega cada nota y si el acierto cuenta vive en
`learning.rhythm.RhythmRunner`; este widget solo dibuja lo que el árbitro le
cuenta que está pasando ahora mismo.
"""

from __future__ import annotations

from PySide6.QtCore import QRectF, Qt
from PySide6.QtGui import QColor, QPainter, QPainterPath, QPen
from PySide6.QtWidgets import QSizePolicy, QWidget

from ...domain.notes import solfa
from ...learning.rhythm import NoteJudgement, RhythmRunner, ScheduledNote
from .. import theme as T
from .gesture_images import gesture_pixmap

HIT_X_RATIO = 0.16   # posición de la línea de impacto, como fracción del ancho
BUBBLE_R = 40


class TravelingNoteTrack(QWidget):
    """Carril horizontal por el que viajan las notas hacia la línea de
    impacto. No sabe nada de tiempo ni de puntaje: solo pinta el estado que
    le entrega el `RhythmRunner` en cada refresco."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._runner: RhythmRunner | None = None
        self.setMinimumHeight(190)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

    def set_runner(self, runner: RhythmRunner | None) -> None:
        self._runner = runner
        self.update()

    def refresh(self) -> None:
        self.update()

    # -------------------------------------------------------------- dibujo
    def paintEvent(self, _e) -> None:
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        w, h = self.width(), self.height()
        centro_y = h / 2
        hit_x = w * HIT_X_RATIO

        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(QColor(T.C.surface_low))
        p.drawRoundedRect(QRectF(0, centro_y - 52, w, 104), 22, 22)

        p.setPen(QPen(QColor(T.C.outline), 4, Qt.PenStyle.DashLine))
        p.drawLine(int(hit_x), int(centro_y - 66), int(hit_x), int(centro_y + 66))
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(QColor(T.C.sun))
        p.drawEllipse(QRectF(hit_x - 7, centro_y - 7, 14, 14))

        if self._runner is None:
            p.end()
            return

        for n in self._runner.visible_notes():
            frac = self._runner.progress_fraction(n)
            x = hit_x + frac * (w - hit_x)
            if n.is_silence:
                self._draw_silence(p, x, centro_y)
            else:
                self._draw_bubble(p, x, centro_y, n)
        p.end()

    def _draw_silence(self, p: QPainter, x: float, y: float) -> None:
        p.setPen(QPen(QColor(T.C.outline).darker(115), 5, Qt.PenStyle.SolidLine,
                      Qt.PenCapStyle.RoundCap))
        p.drawLine(int(x - 14), int(y), int(x + 14), int(y))

    def _draw_bubble(self, p: QPainter, x: float, y: float,
                     n: ScheduledNote) -> None:
        r = BUBBLE_R
        base = QColor(T.NOTE_COLORS.get(n.code, T.C.sky))
        if n.judged == NoteJudgement.HIT:
            cara, borde, texto = QColor(T.C.mint), QColor(T.C.mint_bevel), QColor("#FFFFFF")
        elif n.judged == NoteJudgement.MISSED:
            cara, borde, texto = (QColor(T.C.surface_high), QColor(T.C.bubblegum),
                                  QColor(T.C.bubblegum_bevel))
        else:
            cara, borde, texto = base, base.darker(135), QColor("#FFFFFF")

        caja = QRectF(x - r, y - r, 2 * r, 2 * r)
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(borde)
        p.drawEllipse(caja.adjusted(0, 4, 0, 4))
        p.setBrush(cara)
        p.setPen(QPen(borde, 3))
        p.drawEllipse(caja.adjusted(1, 1, -1, -1))

        pix = gesture_pixmap(n.code)
        if pix is not None and n.judged == NoteJudgement.PENDING:
            p.save()
            recorte = QPainterPath()
            recorte.addEllipse(caja.adjusted(6, 6, -6, -6))
            p.setClipPath(recorte)
            p.drawPixmap(caja.adjusted(5, 5, -5, -5).toRect(), pix)
            p.restore()
        else:
            p.setPen(texto)
            p.setFont(T.font(int(r * 0.6), display=True))
            p.drawText(caja, Qt.AlignmentFlag.AlignCenter, solfa(n.code))
