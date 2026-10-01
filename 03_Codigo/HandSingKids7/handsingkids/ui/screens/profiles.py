"""Selección y creación de perfiles."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QGridLayout, QHBoxLayout, QLineEdit, QSpinBox,
                               QVBoxLayout, QWidget)

from ...domain.entities import Profile
from .. import theme as T
from ..widgets.mascot import MascotView, Mood
from ..widgets.toy import (Body, Card, Chip, RoundIconButton, Title,
                           ToyButton)
from .base import Screen, header, page, scrollable

AVATARES = [("iguana", "🦎"), ("gato", "🐱"), ("perro", "🐶"), ("zorro", "🦊"),
            ("panda", "🐼"), ("rana", "🐸"), ("buho", "🦉"), ("tortuga", "🐢")]
AVATAR_EMOJI = dict(AVATARES)


class ProfileCard(Card):
    """Tarjeta de un niño, pulsable."""

    def __init__(self, profile: Profile, on_click, on_delete, parent=None) -> None:
        super().__init__(parent, bg=T.C.white, border=T.C.outline_variant,
                         padding=18)
        self.profile = profile
        self._on_click = on_click
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFixedSize(256, 236)

        cabecera = QHBoxLayout()
        emoji = Title(AVATAR_EMOJI.get(profile.avatar, "🦎"), 54)
        cabecera.addWidget(emoji)
        cabecera.addStretch(1)
        borrar = RoundIconButton("🗑", "ghost", 42)
        borrar.setToolTip("Borrar este perfil")
        borrar.clicked.connect(lambda: on_delete(profile))
        cabecera.addWidget(borrar, 0, Qt.AlignmentFlag.AlignTop)
        self.body().addLayout(cabecera)

        self.body().addWidget(Title(profile.name, 26))
        self.body().addWidget(Body(f"{profile.age} años", 15))

        fila = QHBoxLayout()
        fila.setSpacing(8)
        fila.addWidget(Chip(f"⭐ {profile.stars}", T.C.sun_soft))
        if profile.streak_days > 1:
            fila.addWidget(Chip(f"🔥 {profile.streak_days}", T.C.bubblegum_soft))
        if not profile.calibrated:
            fila.addWidget(Chip("Falta calibrar", T.C.surface_high, T.C.cocoa))
        fila.addStretch(1)
        contenedor = QWidget()
        contenedor.setLayout(fila)
        self.body().addWidget(contenedor)
        self.body().addStretch(1)

    def mousePressEvent(self, event) -> None:
        super().mousePressEvent(event)
        self._on_click(self.profile)


class ProfilesScreen(Screen):
    def __init__(self, ctx, parent=None) -> None:
        super().__init__(ctx, parent)
        raiz = QVBoxLayout(self)
        raiz.setContentsMargins(0, 0, 0, 0)
        interior, self.lay = page()
        raiz.addWidget(scrollable(interior))

        self.lay.addWidget(header("¿Quién va a jugar?",
                                  on_back=lambda: self.go("splash"),
                                  subtitle="Elige tu personaje o crea uno nuevo"))
        self.grid_host = QWidget()
        self.grid = QGridLayout(self.grid_host)
        self.grid.setSpacing(18)
        self.grid.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.lay.addWidget(self.grid_host)
        self.lay.addStretch(1)

        self.vacio = QWidget()
        vacio_lay = QHBoxLayout(self.vacio)
        vacio_lay.addStretch(1)
        columna = QVBoxLayout()
        columna.setAlignment(Qt.AlignmentFlag.AlignCenter)
        columna.addWidget(MascotView(Mood.HAPPY, 190))
        t = Body("Todavía no hay nadie por aquí.\nCrea el primer perfil 👇", 19)
        t.setAlignment(Qt.AlignmentFlag.AlignCenter)
        columna.addWidget(t)
        host = QWidget()
        host.setLayout(columna)
        vacio_lay.addWidget(host)
        vacio_lay.addStretch(1)
        self.lay.addWidget(self.vacio)
        self.lay.addStretch(2)

    def on_enter(self, **kwargs) -> None:
        self._recargar()

    def _recargar(self) -> None:
        while self.grid.count():
            item = self.grid.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        perfiles = self.ctx.profiles.all()
        self.vacio.setVisible(not perfiles)
        columnas = 4
        for i, p in enumerate(perfiles):
            self.grid.addWidget(ProfileCard(p, self._elegir, self._borrar),
                                i // columnas, i % columnas)

        nuevo = Card(bg=T.C.surface_low, border=T.C.sky, padding=18)
        nuevo.setFixedSize(256, 236)
        nuevo.setCursor(Qt.CursorShape.PointingHandCursor)
        signo = Title("➕", 56)
        signo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        nuevo.body().addStretch(1)
        nuevo.body().addWidget(signo)
        etiqueta = Title("Soy nuevo", 22, T.C.sky_bevel)
        etiqueta.setAlignment(Qt.AlignmentFlag.AlignCenter)
        nuevo.body().addWidget(etiqueta)
        nuevo.body().addStretch(1)
        nuevo.mousePressEvent = lambda _e: self.go("create_profile")  # type: ignore
        idx = len(perfiles)
        self.grid.addWidget(nuevo, idx // columnas, idx % columnas)
        # Columna elástica al final para que las tarjetas queden a la izquierda
        # en lugar de estirarse a lo ancho de la ventana.
        self.grid.setColumnStretch(columnas, 1)

    def _elegir(self, profile: Profile) -> None:
        self.ctx.audio.button()
        self.ctx.select_profile(profile)
        destino = "home" if self.ctx.gestures.calibrated else "calibration"
        self.go(destino, primera_vez=not self.ctx.gestures.calibrated)

    def _borrar(self, profile: Profile) -> None:
        from PySide6.QtWidgets import QMessageBox
        r = QMessageBox.question(
            self, "Borrar perfil",
            f"¿Seguro que quieres borrar el perfil de {profile.name}?\n"
            "Se pierde su progreso y su calibración.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No)
        if r == QMessageBox.StandardButton.Yes and profile.id:
            self.ctx.profiles.delete(profile.id)
            self._recargar()


class CreateProfileScreen(Screen):
    def __init__(self, ctx, parent=None) -> None:
        super().__init__(ctx, parent)
        raiz = QVBoxLayout(self)
        raiz.setContentsMargins(0, 0, 0, 0)
        interior, lay = page()
        raiz.addWidget(scrollable(interior))

        lay.addWidget(header("Soy nuevo", on_back=lambda: self.go("profiles"),
                             subtitle="Cuéntanos quién eres"))

        tarjeta = Card(bg=T.C.white, padding=28)
        cuerpo = tarjeta.body()

        cuerpo.addWidget(Title("¿Cómo te llamas?", 24))
        self.nombre = QLineEdit()
        self.nombre.setPlaceholderText("Escribe tu nombre")
        self.nombre.setMaxLength(18)
        self.nombre.setMinimumHeight(64)
        cuerpo.addWidget(self.nombre)

        cuerpo.addSpacing(10)
        cuerpo.addWidget(Title("¿Cuántos años tienes?", 24))
        # Las flechitas del selector estándar son demasiado pequeñas para un
        # niño: se ocultan y se usan dos botones grandes.
        fila_edad = QHBoxLayout()
        fila_edad.setSpacing(12)
        menos = RoundIconButton("−", "danger", 62)
        menos.clicked.connect(lambda: self._cambiar_edad(-1))
        mas = RoundIconButton("+", "success", 62)
        mas.clicked.connect(lambda: self._cambiar_edad(+1))
        self.edad = QSpinBox()
        self.edad.setRange(3, 12)
        self.edad.setValue(6)
        self.edad.setButtonSymbols(QSpinBox.ButtonSymbols.NoButtons)
        self.edad.setReadOnly(True)
        self.edad.setFixedSize(132, 66)
        self.edad.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.edad.setFont(T.font(28, display=True))
        fila_edad.addWidget(menos)
        fila_edad.addWidget(self.edad)
        fila_edad.addWidget(mas)
        fila_edad.addWidget(Body("años", 18))
        fila_edad.addStretch(1)
        cuerpo.addLayout(fila_edad)

        cuerpo.addSpacing(10)
        cuerpo.addWidget(Title("Elige tu personaje", 24))
        self.avatar = "iguana"
        self.botones_avatar: list[ToyButton] = []
        rejilla = QGridLayout()
        rejilla.setSpacing(10)
        rejilla.setAlignment(Qt.AlignmentFlag.AlignLeft)
        for i, (code, emoji) in enumerate(AVATARES):
            b = ToyButton(emoji, "ghost", height=70, font_size=32)
            b.setFixedWidth(104)
            b.clicked.connect(lambda _=False, c=code: self._elegir_avatar(c))
            self.botones_avatar.append(b)
            rejilla.addWidget(b, i // 4, i % 4)
        cuerpo.addLayout(rejilla)

        lay.addWidget(tarjeta)

        self.aviso = Body("", 15, T.C.error)
        lay.addWidget(self.aviso)

        acciones = QHBoxLayout()
        acciones.addStretch(1)
        crear = ToyButton("¡Listo!", "success", "✓", height=76, font_size=23)
        crear.setMinimumWidth(240)
        crear.clicked.connect(self._crear)
        acciones.addWidget(crear)
        lay.addLayout(acciones)
        lay.addStretch(1)

    def on_enter(self, **kwargs) -> None:
        self.nombre.clear()
        self.edad.setValue(6)
        self.aviso.setText("")
        self._elegir_avatar("iguana")
        self.nombre.setFocus()

    def _cambiar_edad(self, delta: int) -> None:
        self.ctx.audio.button()
        self.edad.setValue(self.edad.value() + delta)

    def _elegir_avatar(self, code: str) -> None:
        self.avatar = code
        self.ctx.audio.button()
        for b, (c, _emoji) in zip(self.botones_avatar, AVATARES):
            b.variant = "secondary" if c == code else "ghost"
            b.update()

    def _crear(self) -> None:
        nombre = self.nombre.text().strip()
        if len(nombre) < 2:
            self.aviso.setText("Escribe un nombre de al menos dos letras 🙂")
            return
        perfil = self.ctx.profiles.create(nombre, self.edad.value(), self.avatar)
        self.ctx.audio.unlock()
        self.ctx.select_profile(perfil)
        self.go("calibration", primera_vez=True)
