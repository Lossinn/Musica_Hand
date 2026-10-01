"""Mi progreso: la vista del niño, visual y sin cifras técnicas."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGridLayout, QHBoxLayout, QVBoxLayout, QWidget

from ...domain.entities import SkillStatus
from ...domain.notes import NOTE_CODES, solfa
from ...intelligence import digital_twin
from .. import theme as T
from ..widgets.handsign import HandSignView
from ..widgets.mascot import MascotView, Mood
from ..widgets.toy import (Body, Card, Chip, ProgressPill, StarRow, Title)
from .base import Screen, header, page, scrollable

ESTADO_ICONO = {
    SkillStatus.LOCKED: ("🔒", T.C.surface_highest, "Todavía no"),
    SkillStatus.INTRODUCED: ("👀", T.C.sky_soft, "La conociste"),
    SkillStatus.PRACTICING: ("🟡", T.C.sun_soft, "Practicando"),
    SkillStatus.MASTERED: ("🟢", T.C.mint_soft, "¡La dominas!"),
    SkillStatus.CONSOLIDATED: ("⭐", T.C.sun, "¡De memoria!"),
}


class NoteCard(Card):
    def __init__(self, code: str, snapshot, pose, parent=None) -> None:
        icono, fondo, etiqueta = ESTADO_ICONO.get(
            snapshot.status if snapshot else SkillStatus.LOCKED,
            ESTADO_ICONO[SkillStatus.LOCKED])
        super().__init__(parent, bg=fondo, border=T.C.outline_variant,
                         padding=12, radius=T.R.lg)
        self.setMinimumHeight(216)
        fila = QHBoxLayout()
        t = Title(solfa(code), 26, T.NOTE_COLORS.get(code, T.C.on_surface))
        fila.addWidget(t)
        fila.addStretch(1)
        fila.addWidget(Title(icono, 22))
        self.body().addLayout(fila)
        vista = HandSignView(pose, min_height=110)
        self.body().addWidget(vista)
        barra = ProgressPill(snapshot.mastery if snapshot else 0.0, 14,
                             (T.C.mint, T.C.sun))
        self.body().addWidget(barra)
        e = Body(etiqueta, 13)
        e.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.body().addWidget(e)


class ProgressScreen(Screen):
    def __init__(self, ctx, parent=None) -> None:
        super().__init__(ctx, parent)
        raiz = QVBoxLayout(self)
        raiz.setContentsMargins(0, 0, 0, 0)
        interior, self.lay = page()
        raiz.addWidget(scrollable(interior))

        self.lay.addWidget(header("Mi progreso", on_back=lambda: self.go("home"),
                                  subtitle="Todo lo que has conseguido"))

        self.resumen = QHBoxLayout()
        self.resumen.setSpacing(14)
        self.lay.addLayout(self.resumen)

        self.lay.addWidget(Title("Mis señas", 26))
        self.rejilla_host = QWidget()
        self.rejilla = QGridLayout(self.rejilla_host)
        self.rejilla.setSpacing(12)
        self.lay.addWidget(self.rejilla_host)

        self.lay.addWidget(Title("Mis insignias", 26))
        self.insignias_host = QWidget()
        self.insignias = QGridLayout(self.insignias_host)
        self.insignias.setSpacing(12)
        self.lay.addWidget(self.insignias_host)
        self.lay.addStretch(1)

    def on_enter(self, **kwargs) -> None:
        p = self.ctx.profile
        if p is None:
            self.go("profiles")
            return
        self.ctx.gestures.pause(True)
        estados = self.ctx.skill_states.for_profile(p.id)
        catalogo = {s.code: s for s in self.ctx.skills.all()}
        gemelo = digital_twin.build(
            p, catalogo, estados,
            weekly_minutes=self.ctx.results.weekly_minutes(p.id),
            total_attempts=self.ctx.attempts.total(p.id))
        por_codigo = {s.code: s for s in gemelo.skills}

        self._limpiar(self.resumen)
        tarjetas = [
            ("⭐", f"{p.stars}", "estrellas", T.C.sun),
            ("🔥", f"{max(1, p.streak_days)}", "días seguidos", T.C.bubblegum),
            ("🎵", f"{len(gemelo.notes_mastered)}/8", "señas dominadas", T.C.mint),
            ("⏱", f"{gemelo.weekly_minutes:.0f}", "minutos esta semana", T.C.sky),
        ]
        for icono, valor, etiqueta, color in tarjetas:
            c = Card(bg=T.C.white, border=color, padding=16, radius=T.R.lg)
            t = Title(icono, 30); t.setAlignment(Qt.AlignmentFlag.AlignCenter)
            v = Title(valor, 34, color); v.setAlignment(Qt.AlignmentFlag.AlignCenter)
            l = Body(etiqueta, 14); l.setAlignment(Qt.AlignmentFlag.AlignCenter)
            for w in (t, v, l):
                c.body().addWidget(w)
            self.resumen.addWidget(c)

        self._limpiar_grid(self.rejilla)
        store = self.ctx.gestures.store
        for i, code in enumerate(NOTE_CODES):
            snap = por_codigo.get(f"nota_{code}")
            pose = store.pose_for(code) if store else None
            self.rejilla.addWidget(NoteCard(code, snap, pose), i // 4, i % 4)

        self._limpiar_grid(self.insignias)
        desbloqueados = self.ctx.achievements.unlocked(p.id)
        todos = self.ctx.achievements.all()
        for i, a in enumerate(todos):
            tiene = a.code in desbloqueados
            c = Card(bg=T.C.white if tiene else T.C.surface_high,
                     border=T.C.sun if tiene else T.C.outline_variant,
                     padding=12, radius=T.R.lg)
            c.setMinimumHeight(128)
            t = Title(a.icon if tiene else "🔒", 26)
            t.setAlignment(Qt.AlignmentFlag.AlignCenter)
            c.body().addWidget(t)
            n = Body(a.title if tiene else "Por descubrir", 14,
                     T.C.on_surface if tiene else T.C.outline)
            n.setAlignment(Qt.AlignmentFlag.AlignCenter)
            c.body().addWidget(n)
            self.insignias.addWidget(c, i // 6, i % 6)

    @staticmethod
    def _limpiar(layout) -> None:
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    @staticmethod
    def _limpiar_grid(grid) -> None:
        while grid.count():
            item = grid.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
