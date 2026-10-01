"""Pantalla de juego: la cámara y la secuencia de notas."""

from __future__ import annotations

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget

from ...core.events import Event
from ...domain.entities import Activity, PlayMode
from ...domain.notes import solfa
from ...learning.evaluation import ActivityRunner, StepState
from ...learning.session_flow import apply_result
from .. import theme as T
from ..widgets.camera_view import CameraView
from ..widgets.handsign import HandSignView
from ..widgets.notes import NoteState, NoteTrack
from ..widgets.toy import (Body, Card, Chip, ProgressPill, RoundIconButton,
                           Title, ToyButton)
from .base import Screen


class ExerciseScreen(Screen):
    def __init__(self, ctx, parent=None) -> None:
        super().__init__(ctx, parent)
        self.runner: ActivityRunner | None = None
        self.activity: Activity | None = None
        self.cola: list[str] = []
        self._memoria_oculta = False

        raiz = QVBoxLayout(self)
        raiz.setContentsMargins(T.S.margin, 20, T.S.margin, 20)
        raiz.setSpacing(14)

        # ---------- barra superior ----------
        barra = QHBoxLayout()
        barra.setSpacing(12)
        self.b_salir = RoundIconButton("←", "danger", 56)
        self.b_salir.clicked.connect(self._salir)
        barra.addWidget(self.b_salir)

        caja = QVBoxLayout()
        caja.setSpacing(0)
        self.titulo = Title("Actividad", 26)
        caja.addWidget(self.titulo)
        self.subtitulo = Body("", 14)
        caja.addWidget(self.subtitulo)
        host = QWidget()
        host.setLayout(caja)
        barra.addWidget(host)
        barra.addStretch(1)

        self.chip_puntaje = Chip("0 puntos", T.C.sun_soft)
        self.chip_combo = Chip("", T.C.bubblegum_soft)
        barra.addWidget(self.chip_puntaje)
        barra.addWidget(self.chip_combo)

        self.b_escuchar = RoundIconButton("🔊", "secondary", 56)
        self.b_escuchar.setToolTip("Escuchar la melodía")
        self.b_escuchar.clicked.connect(self._escuchar)
        self.b_espejo = RoundIconButton("⇄", "ghost", 56)
        self.b_espejo.setToolTip("Modo espejo")
        self.b_espejo.clicked.connect(self._alternar_espejo)
        self.b_repetir = RoundIconButton("↻", "warm", 56)
        self.b_repetir.setToolTip("Repetir desde el principio")
        self.b_repetir.clicked.connect(self._reiniciar)
        for b in (self.b_escuchar, self.b_espejo, self.b_repetir):
            barra.addWidget(b)
        raiz.addLayout(barra)

        self.barra_progreso = ProgressPill(0.0, 18, (T.C.sky, T.C.mint))
        raiz.addWidget(self.barra_progreso)

        # ---------- cuerpo ----------
        cuerpo = QHBoxLayout()
        cuerpo.setSpacing(18)
        self.camara = CameraView()
        cuerpo.addWidget(self.camara, 3)

        derecha = QVBoxLayout()
        derecha.setSpacing(14)

        self.tarjeta_objetivo = Card(bg=T.C.white, border=T.C.sun, padding=16)
        etiqueta = Body("AHORA TOCA", 12, T.C.bubblegum_bevel)
        etiqueta.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.tarjeta_objetivo.body().addWidget(etiqueta)
        self.nota_actual = Title("—", 54)
        self.nota_actual.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.tarjeta_objetivo.body().addWidget(self.nota_actual)
        self.seña = HandSignView(min_height=180)
        self.tarjeta_objetivo.body().addWidget(self.seña)
        derecha.addWidget(self.tarjeta_objetivo, 1)

        self.mensaje = Title("", 24, T.C.mint_bevel)
        self.mensaje.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mensaje.setMinimumHeight(44)
        derecha.addWidget(self.mensaje)

        self.b_pista = ToyButton("Ver la seña", "ghost", "💡", height=56,
                                 font_size=16)
        self.b_pista.clicked.connect(self._mostrar_pista)
        derecha.addWidget(self.b_pista)
        cuerpo.addLayout(derecha, 2)
        raiz.addLayout(cuerpo, 1)

        # ---------- pista de notas ----------
        self.pista = NoteTrack([], 72)
        raiz.addWidget(self.pista)

        self._flash_timer = QTimer(self)
        self._flash_timer.setSingleShot(True)
        self._flash_timer.timeout.connect(lambda: self.camara.set_flash(None))

    # =================================================== ciclo de pantalla
    def on_enter(self, activity: Activity | None = None,
                 cola: list[str] | None = None, **kwargs) -> None:
        if activity is None or self.ctx.profile is None:
            self.go("home")
            return
        self.activity = activity
        self.cola = list(cola or [])
        self.titulo.setText(activity.title)
        modo = {PlayMode.MEMORY: "Modo memoria", PlayMode.SPEED: "Modo velocidad",
                PlayMode.CHALLENGE: "Sin ayudas", PlayMode.MELODY: "Melodía",
                PlayMode.FREE: "Modo libre"}.get(activity.mode, "Practiquemos")
        self.subtitulo.setText(
            f"{modo} · {activity.tempo_bpm} pulsos por minuto · "
            f"{T.format_duration(activity.duration_s)}")
        self.b_escuchar.setVisible(activity.mode in (PlayMode.MELODY,
                                                     PlayMode.MEMORY))
        self.b_pista.setVisible(activity.hints)

        self.ctx.gestures.set_enabled(True)
        self.ctx.gestures.pause(False)
        self.ctx.gestures.frameReady.connect(self._on_frame)
        self._sub_conf = self.ctx.bus.subscribe(Event.GESTURE_CONFIRMED,
                                                self._on_confirmed)
        self._sub_hint = self.ctx.bus.subscribe(Event.HINT_SHOWN,
                                                lambda m: self._mostrar_pista())
        if not self.ctx.gestures.running:
            self.ctx.gestures.start()

        self._arrancar()

    def on_leave(self) -> None:
        try:
            self.ctx.gestures.frameReady.disconnect(self._on_frame)
        except (RuntimeError, TypeError):
            pass
        for desuscribir in (getattr(self, "_sub_conf", None),
                            getattr(self, "_sub_hint", None)):
            if desuscribir:
                desuscribir()
        self.ctx.music.stop_playback()
        self.ctx.music.stop_metronome()
        if self.runner and self.runner.running:
            self.runner.abandon()
        self.ctx.gestures.pause(True)

    # ========================================================= la partida
    def _arrancar(self) -> None:
        assert self.activity is not None
        self.runner = ActivityRunner(self.activity, self.ctx.profile.id,
                                     self.ctx.profile.age_band, self.ctx.bus,
                                     parent=self)
        self.runner.stepChanged.connect(self._on_step)
        self.runner.feedback.connect(self._on_feedback)
        self.runner.finished.connect(self._on_finished)
        self.runner.scoreChanged.connect(self._on_score)
        self.pista.set_sequence(self.runner.sequence, window=8)
        self.chip_puntaje.setText("0 puntos")
        self.chip_combo.setText("")
        self.mensaje.setText("")
        self.barra_progreso.set_value(0.0)

        if self.activity.mode == PlayMode.MEMORY:
            self._memoria_oculta = False
            self.mensaje.setText("Escucha y mira bien…")
            self.ctx.music.play_sequence(self.runner.sequence,
                                         self.activity.tempo_bpm)
            espera = int(len(self.runner.sequence) *
                         (60_000 / max(30, self.activity.tempo_bpm)) + 700)
            QTimer.singleShot(espera, self._ocultar_y_empezar)
        else:
            QTimer.singleShot(400, self.runner.start)

    def _ocultar_y_empezar(self) -> None:
        self._memoria_oculta = True
        self.seña.set_hands(None)
        self.mensaje.setText("¡Ahora tú!")
        self.runner.start()

    def _reiniciar(self) -> None:
        self.ctx.audio.button()
        if self.runner and self.runner.running:
            self.runner.abandon()
        self._arrancar()

    def _salir(self) -> None:
        self.ctx.audio.back()
        self.go("adventure", nivel=self.activity.level if self.activity else 1)

    # ------------------------------------------------------------ cámara
    def _on_frame(self, frame, hands) -> None:
        # Sin "barra de aceptación": la seña cuenta apenas se reconoce (ver
        # vision.stabilizer), así que no hay ningún progreso que dibujar aquí
        # — la confirmación en sí ya se ve en el flash de color y se oye en
        # la nota.
        self.camara.set_frame(frame, hands, self.ctx.settings.vision.mirror)

    def _on_confirmed(self, message) -> None:
        if not self.runner or not self.runner.running:
            return
        nota = message.get("note")
        confianza = float(message.get("confidence", 0.0))
        self.ctx.music.trigger(nota, confianza)
        self.runner.submit(nota, confianza)

    # ------------------------------------------------------------ juego
    def _on_step(self, step: StepState) -> None:
        self.nota_actual.setText(solfa(step.expected))
        self.nota_actual.setStyleSheet(
            f"color: {T.NOTE_COLORS.get(step.expected, T.C.on_surface)};")
        self.pista.set_current(step.index)
        self.barra_progreso.set_value(
            step.index / max(1, self.runner.total_steps))
        mostrar = (self.activity.hints
                   and self.activity.mode not in (PlayMode.CHALLENGE,)
                   and not self._memoria_oculta)
        store = self.ctx.gestures.store
        self.seña.set_hands(store.pose_for(step.expected)
                            if (mostrar and store) else None)


    def _on_feedback(self, tipo: str, mensaje: str) -> None:
        self.mensaje.setText(mensaje)
        if tipo == "acierto":
            # A propósito no suena nada aquí: el niño necesita encadenar notas
            # sin que un efecto lo interrumpa a cada acierto. El sonido de
            # celebración llega una sola vez, al terminar toda la actividad
            # (ver _on_finished), y aquí solo queda la respuesta visual.
            self.mensaje.setStyleSheet(f"color: {T.C.mint_bevel};")
            self.camara.set_flash(T.C.mint, 0.25)
            if self.runner:
                self.pista.mark(self.runner.step.index, NoteState.DONE)
        elif tipo == "casi":
            self.mensaje.setStyleSheet(f"color: {T.C.tangerine_bevel};")
            self.ctx.audio.almost()
            self.camara.set_flash(T.C.tangerine, 0.18)
        else:
            self.mensaje.setStyleSheet(f"color: {T.C.on_surface_variant};")
        self._flash_timer.start(260)

    def _on_score(self, puntaje: int, combo: int) -> None:
        self.chip_puntaje.setText(f"{puntaje} puntos")
        self.chip_combo.setText(f"⚡ {combo} seguidas" if combo >= 3 else "")

    def _mostrar_pista(self) -> None:
        if not self.runner or self.runner.step is None:
            return
        store = self.ctx.gestures.store
        if store:
            self.seña.set_hands(store.pose_for(self.runner.step.expected))
        self._memoria_oculta = False

    def _escuchar(self) -> None:
        if self.runner:
            self.ctx.music.play_sequence(self.runner.sequence,
                                         self.activity.tempo_bpm)

    def _alternar_espejo(self) -> None:
        v = self.ctx.settings.vision
        v.mirror = not v.mirror
        self.ctx.settings.save()

    # ------------------------------------------------------------ cierre
    def _on_finished(self, result) -> None:
        self.ctx.gestures.set_enabled(False)
        outcome = apply_result(self.ctx, self.runner)
        if outcome.stars_awarded or result.stars >= 3:
            self.ctx.audio.star()
        else:
            self.ctx.audio.applause()
        QTimer.singleShot(350, lambda: self.go(
            "results", outcome=outcome, activity=self.activity, cola=self.cola))
