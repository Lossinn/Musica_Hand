"""Resultado de la actividad y decisión de qué sigue."""

from __future__ import annotations

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QGridLayout, QHBoxLayout, QVBoxLayout, QWidget

from ...domain.entities import ActivityKind
from ...domain.notes import solfa
from ...learning.adaptation import (Context, Decision, ease_activity,
                                    pick_anchor, shuffled_variant,
                                    targeted_activity)
from .. import theme as T
from ..widgets.mascot import MascotBubble, MascotView, Mood
from ..widgets.toy import (Body, Card, Chip, StarRow, Title, ToyButton)
from .base import Screen, page, scrollable


class Metric(Card):
    def __init__(self, icon: str, label: str, value: str, color: str,
                 parent=None) -> None:
        super().__init__(parent, bg=T.C.white, border=color, padding=14,
                         radius=T.R.lg)
        t = Title(icon, 28)
        t.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.body().addWidget(t)
        v = Title(value, 30, color)
        v.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.body().addWidget(v)
        l = Body(label, 14)
        l.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.body().addWidget(l)


class ResultsScreen(Screen):
    def __init__(self, ctx, parent=None) -> None:
        super().__init__(ctx, parent)
        self.siguiente = None
        self.cola: list[str] = []
        self.origen = "exercise"

        raiz = QVBoxLayout(self)
        raiz.setContentsMargins(0, 0, 0, 0)
        interior, self.lay = page()
        raiz.addWidget(scrollable(interior))

        self.titulo = Title("¡Terminaste!", 44)
        self.titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lay.addWidget(self.titulo)

        fila_estrellas = QHBoxLayout()
        fila_estrellas.addStretch(1)
        self.estrellas = StarRow(0, 3, 78)
        fila_estrellas.addWidget(self.estrellas)
        fila_estrellas.addStretch(1)
        self.lay.addLayout(fila_estrellas)

        cuerpo = QHBoxLayout()
        cuerpo.setSpacing(20)

        izq = QVBoxLayout()
        izq.setSpacing(12)
        fila_m = QHBoxLayout()
        fila_m.addStretch(1)
        self.mascota = MascotView(Mood.CHEER, 190)
        fila_m.addWidget(self.mascota)
        fila_m.addStretch(1)
        izq.addLayout(fila_m)
        self.globo = MascotBubble("")
        izq.addWidget(self.globo)
        cuerpo.addLayout(izq, 2)

        der = QVBoxLayout()
        der.setSpacing(14)
        self.rejilla = QGridLayout()
        self.rejilla.setSpacing(12)
        der.addLayout(self.rejilla)

        self.tarjeta_logros = Card(bg=T.C.sun_soft, border=T.C.sun, padding=16)
        self.titulo_logros = Title("🏆 ¡Nuevos logros!", 20)
        self.tarjeta_logros.body().addWidget(self.titulo_logros)
        self.lista_logros = QVBoxLayout()
        self.tarjeta_logros.body().addLayout(self.lista_logros)
        der.addWidget(self.tarjeta_logros)

        self.tarjeta_siguiente = Card(bg=T.C.surface_low,
                                      border=T.C.outline_variant, padding=16)
        fila_agente = QHBoxLayout()
        fila_agente.addWidget(Title("🤖 Decide el Agente Adaptativo", 20), 1)
        self.chip_decision = Chip("", T.C.violet_soft)
        fila_agente.addWidget(self.chip_decision)
        self.tarjeta_siguiente.body().addLayout(fila_agente)
        self.estado_modelo = Body("", 13, T.C.outline)
        self.tarjeta_siguiente.body().addWidget(self.estado_modelo)
        self.motivo = Body("", 16)
        self.tarjeta_siguiente.body().addWidget(self.motivo)
        der.addWidget(self.tarjeta_siguiente)
        der.addStretch(1)
        cuerpo.addLayout(der, 3)
        self.lay.addLayout(cuerpo, 1)

        acciones = QHBoxLayout()
        acciones.setSpacing(14)
        self.b_mapa = ToyButton("Al mapa", "ghost", "🗺️", height=72,
                                font_size=19)
        self.b_mapa.clicked.connect(lambda: self.go("adventure"))
        self.b_repetir = ToyButton("Otra vez", "secondary", "↻", height=72,
                                   font_size=19)
        self.b_repetir.clicked.connect(self._repetir)
        self.b_seguir = ToyButton("¡Seguir!", "primary", "🚀", height=80,
                                  font_size=24)
        self.b_seguir.setMinimumWidth(280)
        self.b_seguir.clicked.connect(self._seguir)
        acciones.addWidget(self.b_mapa)
        acciones.addWidget(self.b_repetir)
        acciones.addStretch(1)
        acciones.addWidget(self.b_seguir)
        self.lay.addLayout(acciones)

    # ------------------------------------------------------------- ciclo
    def on_enter(self, outcome=None, activity=None, cola=None,
                origen: str = "exercise", **kwargs) -> None:
        if outcome is None or activity is None:
            self.go("home")
            return
        self.ctx.gestures.pause(True)
        self.actividad = activity
        self.cola = list(cola or [])
        # De qué pantalla vino ("exercise" o "rhythm"): "Otra vez" vuelve ahí,
        # para no mandar a una canción del módulo Canciones de regreso al
        # ejercicio paso a paso de siempre.
        self.origen = origen
        r = outcome.result

        self.estrellas.set_earned(r.stars)
        triunfo = r.accuracy >= 60
        self.titulo.setText("¡Lo lograste! 🎉" if triunfo else "¡Casi, casi!")
        self.mascota.set_mood(Mood.CHEER if triunfo else Mood.HAPPY)
        self.globo.set_text(self._frase(outcome, triunfo))

        while self.rejilla.count():
            item = self.rejilla.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        metricas = [("🎯", "Precisión", f"{r.accuracy:.0f}%", T.C.mint),
                    ("✅", "Aciertos", f"{r.steps_correct}/{r.steps_total}",
                     T.C.sky),
                    ("⚡", "Racha", f"{r.max_combo}", T.C.tangerine),
                    ("🏅", "Puntos", f"{r.score}", T.C.violet)]
        if activity.mode.value in ("velocidad", "melodia"):
            metricas.append(("🥁", "Ritmo", f"{r.rhythm:.0f}%", T.C.bubblegum))
        for i, (icono, etiqueta, valor, color) in enumerate(metricas):
            self.rejilla.addWidget(Metric(icono, etiqueta, valor, color),
                                   i // 3, i % 3)

        # --- logros ---
        while self.lista_logros.count():
            item = self.lista_logros.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        catalogo = {a.code: a for a in self.ctx.achievements.all()}
        nuevos = [catalogo[c] for c in outcome.achievements if c in catalogo]
        for code in outcome.unlocked_skills:
            self.lista_logros.addWidget(
                Body(f"🔓 Se abrió una seña nueva: {self._nombre(code)}", 16))
        for a in nuevos:
            self.lista_logros.addWidget(Body(f"{a.icon} {a.title} — {a.description}", 16))
        self.tarjeta_logros.setVisible(bool(nuevos) or bool(outcome.unlocked_skills))

        self._decidir(outcome)

    def _estado_predictor(self, ctx) -> str:
        """Deja claro si el 'Decide' de arriba viene de la fórmula fija o de
        un modelo ya ajustado a los intentos de este niño — y, en ese caso,
        con cuántos. No es un detalle menor: es la diferencia entre 'reglas
        que siempre son iguales' y 'un agente que de verdad aprende con el
        progreso'."""
        from ...intelligence.predictor import MIN_SAMPLES
        total = ctx.attempts.total(ctx.profile.id)
        if ctx.predictor.trained:
            return (f"Entrenado con {ctx.predictor.n_samples} intentos propios "
                    f"· acierto interno {ctx.predictor.train_accuracy*100:.0f}%")
        return f"Aprendiendo con tus datos · {total}/{MIN_SAMPLES} intentos"

    def _nombre(self, code: str) -> str:
        if code.startswith("nota_"):
            return solfa(code.replace("nota_", ""))
        s = self.ctx.skills.get(code)
        return s.name if s else code

    def _frase(self, outcome, triunfo: bool) -> str:
        if outcome.mastered:
            nombres = ", ".join(self._nombre(c) for c in outcome.mastered)
            return f"¡Ya dominas {nombres}! Qué manitas tan hábiles 🎉"
        if triunfo:
            return "¡Excelente! Tus señas se entendieron muy bien."
        return "No pasa nada, cada intento cuenta. ¡Vamos otra vez!"

    # ------------------------------------------------------- qué sigue
    def _decidir(self, outcome) -> None:
        ctx = self.ctx
        estados = ctx.skill_states.for_profile(ctx.profile.id)
        catalogo = {s.code: s for s in ctx.skills.all()}
        contexto = Context(
            skill_states=estados, skills=catalogo,
            last_accuracy=outcome.result.accuracy,
            consecutive_failures=ctx.consecutive_failures,
            activities_in_session=len(ctx.session_results),
            minutes_in_session=ctx.minutes_in_session,
            session_budget_min=ctx.settings.learning.session_minutes,
            age_band=ctx.profile.age_band,
            last_kinds=[self.actividad.kind])
        plan = ctx.adaptation.decide(contexto)
        self.chip_decision.setText(plan.decision.value.capitalize())
        self.motivo.setText(plan.reason)
        self.estado_modelo.setText(self._estado_predictor(ctx))

        # 1. Si venía una cola de la ruta optimizada, se respeta.
        if self.cola:
            siguiente = ctx.activities.get(self.cola[0])
            if siguiente:
                self.siguiente = siguiente
                self.cola = self.cola[1:]
                self.b_seguir.setText("Siguiente")
                return

        if plan.decision == Decision.REST:
            self.siguiente = None
            self.b_seguir.setText("Terminar por hoy")
            self.b_seguir.variant = "success"
            return

        if plan.decision in (Decision.EASE_DOWN,):
            self.siguiente = ease_activity(self.actividad, plan)
        elif plan.decision in (Decision.TARGET, Decision.REVIEW) and plan.skill_code:
            nota = plan.skill_code.replace("nota_", "")
            ancla = pick_anchor(contexto, plan.skill_code)
            self.siguiente = targeted_activity(nota, ancla, self.actividad.level)
        elif plan.decision == Decision.PLAY:
            juegos = [a for a in ctx.activities.by_kind(ActivityKind.GAME)
                      if a.level <= self.actividad.level]
            self.siguiente = juegos[-1] if juegos else None
        elif plan.decision == Decision.STEP_UP:
            candidatas = [a for a in ctx.activities.all()
                          if a.difficulty > self.actividad.difficulty
                          and a.level <= self.actividad.level + 1 and a.sequence]
            self.siguiente = min(candidatas,
                                 key=lambda a: a.difficulty) if candidatas else None
        elif plan.decision == Decision.REPEAT:
            self.siguiente = shuffled_variant(self.actividad)
        else:
            mismas = [a for a in ctx.activities.by_level(self.actividad.level)
                      if a.code != self.actividad.code and a.sequence]
            self.siguiente = mismas[0] if mismas else None

        if self.siguiente is None:
            self.b_seguir.setText("Al mapa")

    def _repetir(self) -> None:
        self.ctx.audio.button()
        self.go(self.origen, activity=self.actividad, cola=self.cola)

    def _seguir(self) -> None:
        self.ctx.audio.button()
        if self.siguiente is None:
            self.go("home")
            return
        self.go("exercise", activity=self.siguiente, cola=self.cola)
