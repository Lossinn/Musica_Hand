"""Pantalla principal del niño."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGridLayout, QHBoxLayout, QVBoxLayout, QWidget

from ...learning.progression import current_level, level_states
from .. import theme as T
from ..widgets.mascot import MascotBubble, MascotView, Mood
from ..widgets.toy import (Body, Card, Chip, ProgressPill, RoundIconButton,
                           StarRow, Title, ToyButton)
from .base import Screen, page, scrollable

SALUDOS = [
    "¡Tus manitas mágicas están listas para el ritmo!",
    "Hoy vamos a tocar notas con las manos 🎵",
    "¿Seguimos donde lo dejamos?",
    "Las maracas ya están calentando 🪇",
]


class AccessCard(Card):
    def __init__(self, icon: str, title: str, text: str, chip: str,
                 chip_bg: str, on_click, parent=None) -> None:
        super().__init__(parent, bg=T.C.white, padding=18)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMinimumHeight(190)
        self._on_click = on_click
        fila = QHBoxLayout()
        emoji = Title(icon, 40)
        fila.addWidget(emoji)
        fila.addStretch(1)
        fila.addWidget(Chip(chip, chip_bg))
        self.body().addLayout(fila)
        self.body().addWidget(Title(title, 22))
        self.body().addWidget(Body(text, 15))
        self.body().addStretch(1)

    def mousePressEvent(self, e) -> None:
        super().mousePressEvent(e)
        self._on_click()


class HomeScreen(Screen):
    def __init__(self, ctx, parent=None) -> None:
        super().__init__(ctx, parent)
        raiz = QVBoxLayout(self)
        raiz.setContentsMargins(0, 0, 0, 0)
        interior, self.lay = page()
        raiz.addWidget(scrollable(interior))

        # --- barra superior ---
        barra = QHBoxLayout()
        barra.setSpacing(12)
        self.saludo = Title("¡Hola!", 40)
        caja = QVBoxLayout()
        caja.setSpacing(2)
        caja.addWidget(self.saludo)
        self.subtitulo = Body(SALUDOS[0], 18, T.C.cocoa)
        caja.addWidget(self.subtitulo)
        host = QWidget()
        host.setLayout(caja)
        barra.addWidget(host)
        barra.addStretch(1)

        self.chip_estrellas = Chip("⭐ 0", T.C.sun_soft)
        self.chip_racha = Chip("🔥 1", T.C.bubblegum_soft)
        barra.addWidget(self.chip_estrellas)
        barra.addWidget(self.chip_racha)

        b_padres = RoundIconButton("👨‍👩‍👧", "ghost", 56)
        b_padres.setToolTip("Zona de padres")
        b_padres.clicked.connect(lambda: self.go("parents"))
        b_ajustes = RoundIconButton("⚙", "ghost", 56)
        b_ajustes.setToolTip("Ajustes")
        b_ajustes.clicked.connect(lambda: self.go("settings"))
        b_salir = RoundIconButton("🚪", "danger", 56)
        b_salir.setToolTip("Cambiar de perfil")
        b_salir.clicked.connect(self._cambiar_perfil)
        for b in (b_padres, b_ajustes, b_salir):
            barra.addWidget(b)
        self.lay.addLayout(barra)

        # --- cuerpo en dos columnas ---
        cuerpo = QHBoxLayout()
        cuerpo.setSpacing(20)

        izquierda = Card(bg=T.C.surface_low, border=T.C.outline_variant,
                         padding=20)
        self.globo = MascotBubble(SALUDOS[0])
        izquierda.body().addWidget(self.globo)
        fila_mascota = QHBoxLayout()
        fila_mascota.addStretch(1)
        self.mascota = MascotView(Mood.HAPPY, 210)
        fila_mascota.addWidget(self.mascota)
        fila_mascota.addStretch(1)
        izquierda.body().addLayout(fila_mascota)
        nombre = Title("Kiki", 20)
        nombre.setAlignment(Qt.AlignmentFlag.AlignCenter)
        izquierda.body().addWidget(nombre)
        sub = Body("Tu compañera del ritmo", 14)
        sub.setAlignment(Qt.AlignmentFlag.AlignCenter)
        izquierda.body().addWidget(sub)
        izquierda.body().addStretch(1)
        cuerpo.addWidget(izquierda, 2)

        derecha = QVBoxLayout()
        derecha.setSpacing(16)

        self.tarjeta_nivel = Card(bg=T.C.surface_low, border=T.C.sun, padding=22)
        etiqueta = Body("MUNDO DEL RITMO · AVENTURA ACTIVA", 13, T.C.bubblegum_bevel)
        self.tarjeta_nivel.body().addWidget(etiqueta)
        fila_t = QHBoxLayout()
        self.titulo_nivel = Title("Nivel 1", 30)
        fila_t.addWidget(self.titulo_nivel, 1)
        self.estrellas_nivel = StarRow(0, 3, 32)
        fila_t.addWidget(self.estrellas_nivel, 0, Qt.AlignmentFlag.AlignTop)
        self.tarjeta_nivel.body().addLayout(fila_t)
        self.barra_nivel = ProgressPill(0.0, 26, (T.C.sky, T.C.sun))
        self.tarjeta_nivel.body().addWidget(self.barra_nivel)
        self.texto_nivel = Body("Progreso musical", 15)
        self.tarjeta_nivel.body().addWidget(self.texto_nivel)
        derecha.addWidget(self.tarjeta_nivel)

        self.continuar = ToyButton("¡Continuar aventura!", "primary", "🚀",
                                   height=86, font_size=25)
        self.continuar.clicked.connect(self._continuar)
        derecha.addWidget(self.continuar)

        rejilla = QGridLayout()
        rejilla.setSpacing(14)
        rejilla.addWidget(AccessCard(
            "🗺️", "Mi aventura", "Elige el nivel y la actividad que quieras.",
            "Mapa", T.C.sky_soft, lambda: self.go("adventure")), 0, 0)
        rejilla.addWidget(AccessCard(
            "🎼", "Canciones", "Toca melodías completas, nota a nota, al "
            "ritmo justo.", "Nuevo", T.C.mint_soft,
            lambda: self.go("songs")), 0, 1)
        rejilla.addWidget(AccessCard(
            "🎹", "Crear melodía", "Toca las notas libres y guarda tu canción.",
            "Modo libre", T.C.violet_soft, lambda: self.go("freeplay")), 1, 0)
        rejilla.addWidget(AccessCard(
            "🏆", "Mi progreso", "Mira tus estrellas, insignias y señas.",
            "Cofre", T.C.sun_soft, lambda: self.go("progress")), 1, 1)
        derecha.addLayout(rejilla)
        derecha.addStretch(1)
        cuerpo.addLayout(derecha, 3)
        self.lay.addLayout(cuerpo, 1)

        self.aviso_calibrar = Card(bg=T.C.bubblegum_soft, border=T.C.bubblegum,
                                   padding=16)
        fila_av = QHBoxLayout()
        fila_av.addWidget(Body("Todavía no has enseñado tus señas a la cámara.",
                               17, T.C.on_surface), 1)
        b_cal = ToyButton("Calibrar ahora", "danger", "📸", height=58,
                          font_size=17)
        b_cal.clicked.connect(lambda: self.go("calibration", primera_vez=False))
        fila_av.addWidget(b_cal)
        self.aviso_calibrar.body().addLayout(fila_av)
        self.lay.addWidget(self.aviso_calibrar)

        pie = Body("Espacio seguro: la cámara solo procesa gestos en este "
                   "equipo. Sin grabaciones, sin internet y sin anuncios.",
                   13, T.C.outline)
        self.lay.addWidget(pie)

    # ------------------------------------------------------------- ciclo
    def on_enter(self, **kwargs) -> None:
        import random
        p = self.ctx.profile
        if p is None:
            self.go("profiles")
            return
        self.ctx.gestures.pause(True)
        self.saludo.setText(f"¡Hola, {p.name}! ✨")
        mensaje = random.choice(SALUDOS)
        self.subtitulo.setText(mensaje)
        self.globo.set_text(mensaje)
        self.chip_estrellas.setText(f"⭐ {p.stars}")
        self.chip_racha.setText(f"🔥 {max(1, p.streak_days)}")
        self.chip_racha.setVisible(p.streak_days > 1)
        self.aviso_calibrar.setVisible(not self.ctx.gestures.calibrated)

        estados = level_states(self.ctx.activities.all(),
                               self.ctx.results.stars_by_activity(p.id))
        nivel = current_level(estados)
        actual = next((e for e in estados if e.level == nivel), estados[0])
        self.titulo_nivel.setText(f"Nivel {actual.level}: {actual.title}")
        self.barra_nivel.set_value(actual.ratio)
        self.estrellas_nivel.set_earned(
            3 if actual.ratio >= 0.9 else 2 if actual.ratio >= 0.55
            else 1 if actual.ratio > 0 else 0)
        self.texto_nivel.setText(
            f"{actual.subtitle} · {actual.stars} de {actual.max_stars} estrellas")

    def on_leave(self) -> None:
        pass

    def _continuar(self) -> None:
        self.ctx.audio.button()
        if not self.ctx.gestures.calibrated:
            self.go("calibration", primera_vez=False)
            return
        self.go("adventure", autoiniciar=True)

    def _cambiar_perfil(self) -> None:
        self.ctx.audio.back()
        self.ctx.end_session()
        self.ctx.gestures.stop()
        self.go("profiles")
