"""Mapa musical: niveles, actividades y la ruta que propone el optimizador."""

from __future__ import annotations

import math

from PySide6.QtCore import QPointF, QRectF, Qt, Signal
from PySide6.QtGui import QColor, QPainter, QPen
from PySide6.QtWidgets import (QHBoxLayout, QSizePolicy, QVBoxLayout, QWidget)

from ...domain.entities import Activity, ActivityKind, SkillStatus
from ...learning.generator import generate_candidates
from ...learning.progression import LevelState, current_level, level_states
from .. import theme as T
from ..widgets.toy import (Body, Card, Chip, StarRow, Title, ToyButton, _draw_star)
from .base import Screen, header, page, scrollable

COLOR_NIVEL = {"mint": T.C.mint, "tangerine": T.C.tangerine, "sky": T.C.sky,
               "violet": T.C.violet, "bubblegum": T.C.bubblegum, "sun": T.C.sun}

ICONO_TIPO = {ActivityKind.EXERCISE: "🎵", ActivityKind.GAME: "🎮",
              ActivityKind.SONG: "🎶", ActivityKind.ASSESSMENT: "🎯",
              ActivityKind.REVIEW: "🔄"}


class LevelMap(QWidget):
    """Camino de nodos: cada nivel es una isla del mundo musical."""

    levelClicked = Signal(int)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.estados: list[LevelState] = []
        self.seleccion = 1
        self._nodos: list[tuple[QPointF, LevelState]] = []
        self.setMinimumHeight(340)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    def set_states(self, estados: list[LevelState], seleccion: int) -> None:
        self.estados = estados
        self.seleccion = seleccion
        self.update()

    def _layout(self) -> None:
        self._nodos = []
        if not self.estados:
            return
        n = len(self.estados)
        margen_x, margen_y = 72, 60
        ancho = max(1, self.width() - 2 * margen_x)
        alto = max(1, self.height() - 2 * margen_y)
        for i, e in enumerate(self.estados):
            t = i / max(1, n - 1)
            x = margen_x + t * ancho
            # Serpenteo suave, para que el camino no sea una línea recta.
            y = margen_y + alto * (0.5 + 0.34 * math.sin(t * math.pi * 2.1))
            self._nodos.append((QPointF(x, y), e))

    def paintEvent(self, _e) -> None:
        self._layout()
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        if not self._nodos:
            p.end()
            return

        # Camino punteado.
        pen = QPen(QColor(T.C.outline_variant), 7, Qt.PenStyle.DotLine,
                   Qt.PenCapStyle.RoundCap)
        p.setPen(pen)
        for i in range(len(self._nodos) - 1):
            a, ea = self._nodos[i]
            b, _eb = self._nodos[i + 1]
            if ea.completed:
                p.setPen(QPen(QColor(T.C.mint), 7, Qt.PenStyle.DotLine,
                              Qt.PenCapStyle.RoundCap))
            else:
                p.setPen(pen)
            p.drawLine(a, b)

        for centro, e in self._nodos:
            r = 46.0 if e.level == self.seleccion else 39.0
            color = QColor(COLOR_NIVEL.get(e.color, T.C.sky))
            if not e.unlocked:
                color = QColor(T.C.surface_highest)
            p.setPen(Qt.PenStyle.NoPen)
            p.setBrush(color.darker(125) if e.unlocked
                       else QColor(T.C.outline_variant))
            p.drawEllipse(QRectF(centro.x() - r, centro.y() - r + 6, 2 * r, 2 * r))
            p.setBrush(color)
            p.setPen(QPen(color.darker(130) if e.unlocked
                          else QColor(T.C.outline_variant), 3))
            p.drawEllipse(QRectF(centro.x() - r, centro.y() - r, 2 * r, 2 * r))

            if e.level == self.seleccion:
                p.setPen(QPen(QColor(T.C.on_surface), 3, Qt.PenStyle.DashLine))
                p.setBrush(Qt.BrushStyle.NoBrush)
                p.drawEllipse(QRectF(centro.x() - r - 9, centro.y() - r - 9,
                                     2 * r + 18, 2 * r + 18))

            p.setPen(QColor("#FFFFFF" if e.unlocked else T.C.outline))
            p.setFont(T.font(int(r * 0.78), display=True))
            p.drawText(QRectF(centro.x() - r, centro.y() - r, 2 * r, 2 * r),
                       Qt.AlignmentFlag.AlignCenter,
                       e.icon if e.unlocked else "🔒")

            p.setPen(QColor(T.C.on_surface if e.unlocked else T.C.outline))
            p.setFont(T.font(14, display=True))
            p.drawText(QRectF(centro.x() - 95, centro.y() + r + 10, 190, 22),
                       Qt.AlignmentFlag.AlignCenter, f"Nivel {e.level}")
            p.setFont(T.font(12, bold=False))
            p.setPen(QColor(T.C.on_surface_variant))
            p.drawText(QRectF(centro.x() - 95, centro.y() + r + 30, 190, 20),
                       Qt.AlignmentFlag.AlignCenter, e.title)

            if e.unlocked and e.max_stars:
                ganadas = 3 if e.ratio >= 0.9 else 2 if e.ratio >= 0.55 \
                    else 1 if e.ratio > 0 else 0
                for k in range(3):
                    cx = centro.x() - 22 + k * 22
                    _draw_star(p, cx, centro.y() - r - 14, 9,
                               QColor(T.C.sun if k < ganadas else T.C.surface_highest),
                               QColor(T.C.sun_bevel if k < ganadas
                                      else T.C.outline_variant))
        p.end()

    def mousePressEvent(self, event) -> None:
        pos = event.position()
        for centro, e in self._nodos:
            if (pos - centro).manhattanLength() < 70 and e.unlocked:
                self.levelClicked.emit(e.level)
                return


class ActivityRow(Card):
    def __init__(self, activity: Activity, stars: int, on_click,
                 destacada: bool = False, parent=None) -> None:
        super().__init__(parent, bg=T.C.white,
                         border=T.C.sun if destacada else T.C.outline_variant,
                         padding=14, radius=T.R.lg)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._on_click = on_click
        self.activity = activity
        fila = QHBoxLayout()
        fila.setSpacing(12)
        fila.addWidget(Title(activity.icon, 30))
        caja = QVBoxLayout()
        caja.setSpacing(2)
        caja.addWidget(Title(activity.title, 19))
        if activity.code.startswith("proc_"):
            detalle = "🤖 generado para ti"
        else:
            detalle = f"{ICONO_TIPO.get(activity.kind,'🎵')} {activity.kind.value}"
        if activity.sequence:
            detalle += f" · {len(activity.sequence)} notas"
        detalle += f" · ⏱ {T.format_duration(activity.duration_s)}"
        caja.addWidget(Body(detalle, 13))
        host = QWidget()
        host.setLayout(caja)
        fila.addWidget(host, 1)
        fila.addWidget(StarRow(stars, 3, 22))
        self.body().addLayout(fila)

    def mousePressEvent(self, e) -> None:
        super().mousePressEvent(e)
        self._on_click(self.activity)


class AdventureScreen(Screen):
    def __init__(self, ctx, parent=None) -> None:
        super().__init__(ctx, parent)
        self.nivel = 1
        raiz = QVBoxLayout(self)
        raiz.setContentsMargins(0, 0, 0, 0)
        interior, self.lay = page()
        raiz.addWidget(scrollable(interior))

        self.lay.addWidget(header("Mi aventura musical",
                                  on_back=lambda: self.go("home"),
                                  subtitle="Toca una isla para ver sus retos"))

        self.mapa = LevelMap()
        self.mapa.levelClicked.connect(self._elegir_nivel)
        tarjeta_mapa = Card(bg=T.C.surface_low, border=T.C.outline_variant,
                            padding=8)
        tarjeta_mapa.body().addWidget(self.mapa)
        self.lay.addWidget(tarjeta_mapa, 3)

        cuerpo = QHBoxLayout()
        cuerpo.setSpacing(18)

        # --- ruta sugerida ---
        self.tarjeta_ruta = Card(bg=T.C.sun_soft, border=T.C.sun, padding=18)
        fila_r = QHBoxLayout()
        fila_r.addWidget(Title("✨ Tu ruta de hoy", 24), 1)
        self.chip_metodo = Chip("", T.C.white, T.C.cocoa)
        fila_r.addWidget(self.chip_metodo)
        self.tarjeta_ruta.body().addLayout(fila_r)
        self.tarjeta_ruta.body().addWidget(Body(
            "La aplicación eligió estas actividades según lo que ya dominas y "
            "lo que conviene repasar.", 14))
        self.contenedor_ruta = QVBoxLayout()
        self.contenedor_ruta.setSpacing(10)
        self.tarjeta_ruta.body().addLayout(self.contenedor_ruta)
        self.tarjeta_ruta.body().addStretch(1)
        self.boton_ruta = ToyButton("Empezar la ruta", "primary", "🚀",
                                    height=70, font_size=20)
        self.boton_ruta.clicked.connect(self._empezar_ruta)
        self.tarjeta_ruta.body().addWidget(self.boton_ruta)
        cuerpo.addWidget(self.tarjeta_ruta, 2)

        # --- actividades del nivel ---
        self.tarjeta_nivel = Card(bg=T.C.white, padding=18)
        self.titulo_nivel = Title("Nivel 1", 24)
        self.tarjeta_nivel.body().addWidget(self.titulo_nivel)
        self.contenedor_acts = QVBoxLayout()
        self.contenedor_acts.setSpacing(10)
        self.tarjeta_nivel.body().addLayout(self.contenedor_acts)
        self.tarjeta_nivel.body().addStretch(1)
        cuerpo.addWidget(self.tarjeta_nivel, 3)

        self.lay.addLayout(cuerpo, 4)
        self._ruta: list[Activity] = []

    # ------------------------------------------------------------- ciclo
    def on_enter(self, autoiniciar: bool = False, **kwargs) -> None:
        p = self.ctx.profile
        if p is None:
            self.go("profiles")
            return
        self.ctx.gestures.pause(True)
        estrellas = self.ctx.results.stars_by_activity(p.id)
        estados = level_states(self.ctx.activities.all(), estrellas)
        self.nivel = kwargs.get("nivel") or current_level(estados)
        self.mapa.set_states(estados, self.nivel)
        self._cargar_nivel(estrellas)
        self._calcular_ruta()
        if autoiniciar and self._ruta:
            self._empezar_ruta()

    def _elegir_nivel(self, nivel: int) -> None:
        self.ctx.audio.button()
        self.nivel = nivel
        p = self.ctx.profile
        estrellas = self.ctx.results.stars_by_activity(p.id) if p else {}
        self.mapa.set_states(self.mapa.estados, nivel)
        self._cargar_nivel(estrellas)

    def _cargar_nivel(self, estrellas: dict[str, int]) -> None:
        while self.contenedor_acts.count():
            item = self.contenedor_acts.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        estado = next((e for e in self.mapa.estados if e.level == self.nivel), None)
        if estado:
            self.titulo_nivel.setText(f"Nivel {estado.level}: {estado.title}")
        for a in self.ctx.activities.by_level(self.nivel):
            if a.kind.value == "repaso":
                continue
            self.contenedor_acts.addWidget(
                ActivityRow(a, estrellas.get(a.code, 0), self._jugar))

    # ----------------------------------------------------------- ruta
    def _calcular_ruta(self) -> None:
        while self.contenedor_ruta.count():
            item = self.contenedor_ruta.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        p = self.ctx.profile
        if p is None:
            return
        estados = self.ctx.skill_states.for_profile(p.id)
        niveles_abiertos = {e.level for e in self.mapa.estados if e.unlocked}

        def disponible(a) -> bool:
            """Restricción de prerrequisitos: no se propone una actividad que
            dependa de una seña que el niño todavía no tiene abierta."""
            if a.level not in niveles_abiertos or not a.sequence:
                return False
            for code in a.skill_codes:
                st = estados.get(code)
                if st is None or st.status == SkillStatus.LOCKED:
                    return False
            return True

        candidatas = [a for a in self.ctx.activities.all() if disponible(a)][:26]

        # Contenido generado sobre la marcha: se suma al catálogo fijo como
        # candidatas más, nunca lo reemplaza. El Agente Adaptativo (entrenado
        # o, si aún no hay datos propios, la fórmula fija) es quien elige
        # cuáles de estas valen la pena al puntuarlas junto con las demás.
        generadas = generate_candidates(self.nivel, estados, self.ctx.predictor)
        candidatas = candidatas + generadas

        vencidos = {a.code for a in candidatas
                    if any(estados.get(c) and estados[c].is_due
                           for c in a.skill_codes)}
        recientes = {r["activity_code"] for r in self.ctx.results.history(p.id, 8)}
        seleccion = self.ctx.optimizer.solve(candidatas, estados,
                                             recent_codes=recientes,
                                             overdue_codes=vencidos,
                                             predictor=self.ctx.predictor)
        self._ruta = seleccion.activities
        self.ctx.last_optimizer_method = seleccion.method

        # Solo lo que de verdad se propuso para hoy se guarda: así el
        # catálogo crece con lo que se llega a jugar, no con borradores que
        # nadie vio. Sin esto, una actividad generada que quedara en la cola
        # de "lo siguiente" no se podría recuperar por su código más tarde.
        elegidas_generadas = [a for a in self._ruta if a.code.startswith("proc_")]
        if elegidas_generadas:
            self.ctx.activities.upsert_many(elegidas_generadas)
        etiqueta = {"milp": "optimización exacta",
                    "exacto": "optimización exacta",
                    "voraz": "selección rápida"}.get(seleccion.method,
                                                     seleccion.method)
        self.chip_metodo.setText(f"{etiqueta} · {seleccion.seconds*1000:.0f} ms")
        estrellas = self.ctx.results.stars_by_activity(p.id)
        for a in self._ruta:
            self.contenedor_ruta.addWidget(
                ActivityRow(a, estrellas.get(a.code, 0), self._jugar,
                            destacada=True))
        self.boton_ruta.setEnabled(bool(self._ruta))

    def _empezar_ruta(self) -> None:
        if not self._ruta:
            return
        self.ctx.audio.button()
        self.go("exercise", activity=self._ruta[0],
                cola=[a.code for a in self._ruta[1:]])

    def _jugar(self, activity: Activity) -> None:
        self.ctx.audio.button()
        self.go("exercise", activity=activity, cola=[])
