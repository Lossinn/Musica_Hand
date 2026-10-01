"""Zona de padres: la misma información, en registro adulto y con cifras."""

from __future__ import annotations

from PySide6.QtCore import QRectF, Qt
from PySide6.QtGui import QColor, QPainter, QPen
from PySide6.QtWidgets import (QHBoxLayout, QSizePolicy, QVBoxLayout, QWidget)

from ...domain.notes import solfa
from ...intelligence import digital_twin
from ...learning import mastery as M
from .. import theme as T
from ..widgets.toy import Body, Card, Chip, Title, ToyButton
from .base import Screen, header, page, scrollable


class MasteryBars(QWidget):
    """Barras horizontales de dominio por habilidad."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.filas: list[tuple[str, float, str]] = []
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

    def set_rows(self, filas: list[tuple[str, float, str]]) -> None:
        self.filas = filas
        self.setMinimumHeight(max(60, 34 * len(filas) + 10))
        self.setMaximumHeight(34 * len(filas) + 16)
        self.update()

    def paintEvent(self, _e) -> None:
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        etiqueta_w = 190
        alto = 22
        for i, (nombre, valor, color) in enumerate(self.filas):
            y = 6 + i * 34
            p.setPen(QColor(T.C.on_surface))
            p.setFont(T.font(15, bold=False))
            p.drawText(QRectF(0, y, etiqueta_w - 10, alto),
                       Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft,
                       nombre)
            pista = QRectF(etiqueta_w, y, self.width() - etiqueta_w - 70, alto)
            p.setPen(Qt.PenStyle.NoPen)
            p.setBrush(QColor(T.C.surface_highest))
            p.drawRoundedRect(pista, alto / 2, alto / 2)
            if valor > 0:
                relleno = QRectF(pista.left(), pista.top(),
                                 max(alto, pista.width() * valor), alto)
                p.setBrush(QColor(color))
                p.drawRoundedRect(relleno, alto / 2, alto / 2)
            # Línea del umbral de dominio.
            x_umbral = pista.left() + pista.width() * M.MASTERED_AT
            p.setPen(QPen(QColor(T.C.outline), 2, Qt.PenStyle.DashLine))
            p.drawLine(x_umbral, pista.top() - 3, x_umbral, pista.bottom() + 3)
            p.setPen(QColor(T.C.on_surface_variant))
            p.setFont(T.font(14, display=True))
            p.drawText(QRectF(pista.right() + 8, y, 62, alto),
                       Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft,
                       f"{valor*100:.0f}%")
        p.end()


class ParentsScreen(Screen):
    def __init__(self, ctx, parent=None) -> None:
        super().__init__(ctx, parent)
        raiz = QVBoxLayout(self)
        raiz.setContentsMargins(0, 0, 0, 0)
        interior, self.lay = page()
        raiz.addWidget(scrollable(interior))

        ajustes = ToyButton("Ajustes", "ghost", "⚙", height=54, font_size=16)
        ajustes.clicked.connect(lambda: self.go("settings"))
        self.lay.addWidget(header("Zona de padres", on_back=lambda: self.go("home"),
                                  subtitle="Seguimiento del aprendizaje",
                                  extra=[ajustes]))

        self.resumen = QHBoxLayout()
        self.resumen.setSpacing(14)
        self.lay.addLayout(self.resumen)

        cuerpo = QHBoxLayout()
        cuerpo.setSpacing(18)

        self.tarjeta_dominio = Card(bg=T.C.white, padding=18)
        self.tarjeta_dominio.body().addWidget(Title("Dominio por habilidad", 22))
        self.tarjeta_dominio.body().addWidget(Body(
            "La línea punteada marca el umbral a partir del cual la aplicación "
            "considera la habilidad dominada.", 13))
        self.barras = MasteryBars()
        self.tarjeta_dominio.body().addWidget(self.barras)
        cuerpo.addWidget(self.tarjeta_dominio, 3)

        der = QVBoxLayout()
        der.setSpacing(14)

        self.tarjeta_reco = Card(bg=T.C.sun_soft, border=T.C.sun, padding=18)
        self.tarjeta_reco.body().addWidget(Title("Recomendación", 20))
        self.texto_reco = Body("", 16)
        self.tarjeta_reco.body().addWidget(self.texto_reco)
        der.addWidget(self.tarjeta_reco)

        self.tarjeta_conf = Card(bg=T.C.white, padding=18)
        self.tarjeta_conf.body().addWidget(Title("Confusiones frecuentes", 20))
        self.lista_conf = QVBoxLayout()
        self.tarjeta_conf.body().addLayout(self.lista_conf)
        der.addWidget(self.tarjeta_conf)

        self.tarjeta_tecnica = Card(bg=T.C.surface_low, padding=18)
        self.tarjeta_tecnica.body().addWidget(Title("Detalle técnico", 20))
        self.lista_tecnica = QVBoxLayout()
        self.tarjeta_tecnica.body().addLayout(self.lista_tecnica)
        der.addWidget(self.tarjeta_tecnica)
        der.addStretch(1)
        cuerpo.addLayout(der, 2)
        self.lay.addLayout(cuerpo, 1)
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
            confusions=self.ctx.attempts.confusion_pairs(p.id),
            weekly_minutes=self.ctx.results.weekly_minutes(p.id),
            weekly_activities=self.ctx.results.count_since(
                p.id, __import__("time").time() - 7 * 86400),
            total_attempts=self.ctx.attempts.total(p.id))

        self._limpiar(self.resumen)
        tarjetas = [
            ("Dominio global", f"{gemelo.overall_mastery*100:.0f}%", T.C.mint),
            ("Señas dominadas", f"{len(gemelo.notes_mastered)} de 8", T.C.sky),
            ("Minutos esta semana", f"{gemelo.weekly_minutes:.0f}", T.C.violet),
            ("Actividades", f"{gemelo.weekly_activities}", T.C.tangerine),
            ("Intentos totales", f"{gemelo.total_attempts}", T.C.bubblegum),
        ]
        for etiqueta, valor, color in tarjetas:
            c = Card(bg=T.C.white, border=color, padding=16, radius=T.R.lg)
            v = Title(valor, 30, color)
            v.setAlignment(Qt.AlignmentFlag.AlignCenter)
            l = Body(etiqueta, 13)
            l.setAlignment(Qt.AlignmentFlag.AlignCenter)
            c.body().addWidget(v)
            c.body().addWidget(l)
            self.resumen.addWidget(c)

        filas = []
        for s in gemelo.skills:
            color = (T.C.mint if s.mastery >= M.MASTERED_AT
                     else T.C.sun if s.mastery >= 0.5 else T.C.bubblegum)
            filas.append((s.label, s.mastery, color))
        self.barras.set_rows(filas)

        self.texto_reco.setText(gemelo.recommendation())

        self._limpiar(self.lista_conf)
        if not gemelo.confusions:
            self.lista_conf.addWidget(Body("Todavía no hay confusiones "
                                           "repetidas registradas.", 15))
        for esperada, detectada, n in gemelo.confusions[:5]:
            self.lista_conf.addWidget(Body(
                f"{solfa(esperada)} se confundió con {solfa(detectada)} "
                f"· {n} veces", 15))

        self._limpiar(self.lista_tecnica)
        store = self.ctx.gestures.store
        separacion = store.separation()[0] if (store and store.notes) else None
        detalles = [
            f"Umbral de dominio: {M.MASTERED_AT:.2f}",
            f"Confianza mínima del reconocedor: "
            f"{self.ctx.settings.vision.confidence_threshold:.2f}",
            f"Ventana de estabilización: "
            f"{self.ctx.settings.vision.window_frames} fotogramas",
            f"Selección de actividades: "
            f"{self.ctx.last_optimizer_method or 'sin calcular'}",
            self._detalle_agente(),
        ]
        if separacion:
            a, b, d = separacion
            detalles.append(f"Señas más parecidas: {solfa(a)} y {solfa(b)} "
                            f"(distancia {d:.3f})")
        for texto in detalles:
            self.lista_tecnica.addWidget(Body(texto, 14))

    def _detalle_agente(self) -> str:
        from ...intelligence.predictor import MIN_SAMPLES
        pred = self.ctx.predictor
        if pred.trained:
            return (f"Agente Adaptativo: modelo propio de {self.ctx.profile.name} "
                    f"entrenado con {pred.n_samples} intentos suyos (acierto "
                    f"interno {pred.train_accuracy*100:.0f}%); se reajusta cada "
                    f"vez que juega más. Nunca se entrena con datos de otro perfil.")
        total = self.ctx.attempts.total(self.ctx.profile.id)
        return (f"Agente Adaptativo: por ahora usa reglas fijas — le faltan "
                f"{max(0, MIN_SAMPLES - total)} intentos para empezar a "
                f"entrenarse con los datos propios de {self.ctx.profile.name}.")

    @staticmethod
    def _limpiar(layout) -> None:
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
