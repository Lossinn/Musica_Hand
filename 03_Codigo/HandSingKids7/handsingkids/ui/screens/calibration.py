"""Calibración de las señas.

El niño enseña cada seña a la cámara y la aplicación guarda varias muestras de
cada una. Al terminar se comprueba cuánto se parecen entre sí: si dos quedaron
demasiado juntas, se avisa, porque es exactamente ahí donde el reconocedor se
va a confundir después.
"""

from __future__ import annotations

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget

from ...core.events import Event
from ...domain.notes import NOTE_CODES, solfa
from ...vision.templates import SAMPLES_PER_NOTE
from .. import theme as T
from ..widgets.camera_view import CameraView
from ..widgets.handsign import HandSignView
from ..widgets.mascot import MascotBubble, MascotView, Mood
from ..widgets.notes import NoteBubble, NoteState
from ..widgets.toy import Body, Card, Chip, ProgressPill, Title, ToyButton
from .base import Screen, header

CUENTA_ATRAS = 3


class CalibrationScreen(Screen):
    def __init__(self, ctx, parent=None) -> None:
        super().__init__(ctx, parent)
        self.indice = 0
        self.muestra = 0
        self.primera_vez = True
        self._reiniciadas: set[str] = set()
        self._cuenta = 0
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._tic)

        raiz = QVBoxLayout(self)
        raiz.setContentsMargins(T.S.margin, 22, T.S.margin, 22)
        raiz.setSpacing(16)

        self.saltar = ToyButton("Saltar por ahora", "ghost", height=54,
                                font_size=16)
        self.saltar.clicked.connect(lambda: self.go("home"))
        raiz.addWidget(header("Enséñame tus señas", on_back=self._salir,
                              subtitle="Haz la seña y mantenla quieta",
                              extra=[self.saltar]))

        cuerpo = QHBoxLayout()
        cuerpo.setSpacing(18)

        # --- columna izquierda: cámara ---
        izquierda = QVBoxLayout()
        izquierda.setSpacing(12)
        self.camara = CameraView()
        self.camara.placeholder = "Encendiendo la cámara…"
        izquierda.addWidget(self.camara, 1)
        self.aviso = Body("", 16, T.C.error)
        izquierda.addWidget(self.aviso)
        cuerpo.addLayout(izquierda, 3)

        # --- columna derecha: instrucciones ---
        derecha = QVBoxLayout()
        derecha.setSpacing(14)

        self.tarjeta_nota = Card(bg=T.C.white, border=T.C.sun, padding=18)
        self.titulo_nota = Title("Do", 44)
        self.titulo_nota.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.tarjeta_nota.body().addWidget(self.titulo_nota)
        self.seña = HandSignView(min_height=170)
        self.tarjeta_nota.body().addWidget(self.seña)
        self.muestras_chip = Chip("Muestra 1 de 3", T.C.sky_soft)
        fila_chip = QHBoxLayout()
        fila_chip.addStretch(1)
        fila_chip.addWidget(self.muestras_chip)
        fila_chip.addStretch(1)
        self.tarjeta_nota.body().addLayout(fila_chip)
        derecha.addWidget(self.tarjeta_nota)

        self.progreso = ProgressPill(0.0, 24, (T.C.mint, T.C.sun))
        derecha.addWidget(self.progreso)

        fila_burbujas = QHBoxLayout()
        fila_burbujas.setSpacing(6)
        self.burbujas = []
        for code in NOTE_CODES:
            b = NoteBubble(code, NoteState.PENDING, 48)
            self.burbujas.append(b)
            fila_burbujas.addWidget(b)
        contenedor = QWidget()
        contenedor.setLayout(fila_burbujas)
        derecha.addWidget(contenedor)

        self.mascota = MascotView(Mood.THINKING, 130)
        self.globo = MascotBubble("Pon las dos manitas frente a la cámara")
        fila_mascota = QHBoxLayout()
        fila_mascota.addWidget(self.mascota)
        fila_mascota.addWidget(self.globo, 1)
        derecha.addLayout(fila_mascota)

        derecha.addStretch(1)
        self.boton = ToyButton("Capturar seña", "primary", "📸", height=74,
                               font_size=21)
        self.boton.clicked.connect(self._capturar)
        derecha.addWidget(self.boton)
        self.repetir = ToyButton("Repetir esta nota", "ghost", height=56,
                                 font_size=16)
        self.repetir.clicked.connect(self._repetir_nota)
        derecha.addWidget(self.repetir)

        cuerpo.addLayout(derecha, 2)
        raiz.addLayout(cuerpo, 1)

        self._suscripciones = []

    # ------------------------------------------------------------ ciclo
    def on_enter(self, primera_vez: bool = True, **kwargs) -> None:
        self.primera_vez = primera_vez
        self.saltar.setVisible(bool(self.ctx.gestures.calibrated))
        # Al recalibrar no se borra nada por adelantado: cada nota se reemplaza
        # en el momento en que el niño captura su primera muestra nueva. Así,
        # si abandona a mitad, conserva las señas que no llegó a rehacer.
        self._reiniciadas = set()
        self.indice = 0
        self.muestra = 0
        self.aviso.setText("")
        self._refrescar()
        self.ctx.gestures.set_enabled(False)   # durante la calibración no se juega
        self.ctx.gestures.frameReady.connect(self._on_frame)
        self.ctx.gestures.stateChanged.connect(self._on_state)
        if not self.ctx.gestures.running:
            self.ctx.gestures.start()

    def on_leave(self) -> None:
        self._timer.stop()
        try:
            self.ctx.gestures.frameReady.disconnect(self._on_frame)
            self.ctx.gestures.stateChanged.disconnect(self._on_state)
        except (RuntimeError, TypeError):
            pass
        self.ctx.gestures.set_enabled(True)

    def _salir(self) -> None:
        store = self.ctx.gestures.store
        if self._reiniciadas and store is not None and store.samples:
            store.save()
            if self.ctx.gestures.classifier:
                self.ctx.gestures.classifier.calibrate_temperature()
        self.ctx.gestures.stop()
        self.go("profiles" if self.primera_vez else "home")

    # ---------------------------------------------------------- cámara
    def _on_frame(self, frame, hands) -> None:
        self.camara.set_frame(frame, hands, self.ctx.settings.vision.mirror)
        listo = len(hands) >= (2 if self.ctx.settings.vision.require_two_hands else 1)
        self.boton.setEnabled(listo and not self._timer.isActive())
        if not listo and not self._timer.isActive():
            self.globo.set_text("Necesito ver tus dos manitas 🙌")

    def _on_state(self, estado: str) -> None:
        if estado == "error":
            self.aviso.setText(self.ctx.gestures.error or "No se pudo abrir la cámara")
            self.camara.placeholder = "Sin cámara"

    # ----------------------------------------------------------- captura
    def _capturar(self) -> None:
        if self._timer.isActive():
            return
        self._cuenta = CUENTA_ATRAS
        self.boton.setEnabled(False)
        self.camara.set_ring(1.0, str(self._cuenta), T.C.sun)
        self.globo.set_text("Mantén la seña quieta…")
        self._timer.start(700)

    def _tic(self) -> None:
        self._cuenta -= 1
        if self._cuenta > 0:
            self.ctx.audio.tick()
            self.camara.set_ring(self._cuenta / CUENTA_ATRAS, str(self._cuenta),
                                 T.C.sun)
            return
        self._timer.stop()
        self.camara.set_ring(0.0, "")
        self._guardar()

    def _guardar(self) -> None:
        code = NOTE_CODES[self.indice]
        store = self.ctx.gestures.store
        if (code not in self._reiniciadas and store is not None
                and not self.primera_vez):
            store.drop(code)          # se reemplaza esta nota, no se acumula
        self._reiniciadas.add(code)
        if not self.ctx.gestures.capture_sample(code):
            self.globo.set_text("No te vi bien. Inténtalo otra vez 🙂")
            self.ctx.audio.almost()
            self.boton.setEnabled(True)
            return
        self.ctx.audio.correct()
        self.camara.set_flash(T.C.mint, 0.3)
        QTimer.singleShot(200, lambda: self.camara.set_flash(None))
        self.muestra += 1
        if self.muestra >= SAMPLES_PER_NOTE:
            self.muestra = 0
            self.indice += 1
            self.mascota.celebrate(900)
            if self.indice >= len(NOTE_CODES):
                self._terminar()
                return
        self._refrescar()
        self.boton.setEnabled(True)

    def _repetir_nota(self) -> None:
        code = NOTE_CODES[self.indice] if self.indice < len(NOTE_CODES) else None
        if code and self.ctx.gestures.store is not None:
            self.ctx.gestures.store.drop(code)
            self._reiniciadas.add(code)
        self.muestra = 0
        self._refrescar()

    # --------------------------------------------------------- pantalla
    def _refrescar(self) -> None:
        if self.indice >= len(NOTE_CODES):
            return
        code = NOTE_CODES[self.indice]
        self.titulo_nota.setText(solfa(code))
        self.titulo_nota.setStyleSheet(
            f"color: {T.NOTE_COLORS.get(code, T.C.on_surface)};")
        self.muestras_chip.setText(
            f"Muestra {self.muestra + 1} de {SAMPLES_PER_NOTE}")
        store = self.ctx.gestures.store
        self.seña.set_hands(store.pose_for(code) if store else None)
        total = len(NOTE_CODES) * SAMPLES_PER_NOTE
        hechas = self.indice * SAMPLES_PER_NOTE + self.muestra
        self.progreso.set_value(hechas / total)
        for i, b in enumerate(self.burbujas):
            if i < self.indice:
                b.set_state(NoteState.DONE)
            elif i == self.indice:
                b.set_state(NoteState.CURRENT)
            else:
                b.set_state(NoteState.PENDING)
        if self.muestra == 0:
            self.globo.set_text(f"Ahora hazme la seña de {solfa(code)}")
        else:
            self.globo.set_text("¡Bien! Otra vez la misma, un poquito distinta")

    # ----------------------------------------------------------- cierre
    def _terminar(self) -> None:
        informe = self.ctx.gestures.finish_calibration()
        if self.ctx.profile:
            self.ctx.profile.calibrated = True
            self.ctx.profiles.save(self.ctx.profile)
        self.ctx.audio.unlock()
        self.progreso.set_value(1.0)
        for b in self.burbujas:
            b.set_state(NoteState.DONE)

        parecidas = informe.get("parecidas") or []
        conflicto = [p for p in parecidas if p[2] < 0.22]
        if conflicto:
            a, b, d = conflicto[0]
            self.globo.set_text(
                f"Las señas de {solfa(a)} y {solfa(b)} quedaron muy parecidas. "
                "Si luego se confunden, vuelve aquí y hazlas más distintas.")
            self.mascota.set_mood(Mood.THINKING)
            self.boton.setText("Entendido, ¡a jugar!")
        else:
            self.globo.set_text("¡Listo! Tus ocho señas quedaron bien guardadas 🎉")
            self.mascota.set_mood(Mood.CHEER)
            self.boton.setText("¡A jugar!")
        self.boton.variant = "success"
        self.boton.icon_text = "🎵"
        self.boton.setEnabled(True)
        self.repetir.setVisible(False)
        try:
            self.boton.clicked.disconnect()
        except RuntimeError:
            pass
        self.boton.clicked.connect(lambda: self.go("home"))
