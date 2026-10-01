"""Pantalla base y utilidades comunes de navegación."""

from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (QHBoxLayout, QScrollArea, QVBoxLayout, QWidget)

from .. import theme as T
from ..widgets.toy import RoundIconButton, Title


class Screen(QWidget):
    """Toda pantalla recibe el contexto de la aplicación y responde a entrar y
    salir. El ciclo de vida explícito evita que la cámara siga encendida en una
    pantalla que ya no se ve."""

    navigate = Signal(str, dict)

    def __init__(self, ctx, parent=None) -> None:
        super().__init__(parent)
        self.ctx = ctx
        self.setObjectName("RootSurface")

    def on_enter(self, **kwargs) -> None:
        """Se llama cada vez que la pantalla pasa a primer plano."""

    def on_leave(self) -> None:
        """Se llama al abandonarla."""

    def go(self, name: str, **kwargs) -> None:
        self.navigate.emit(name, kwargs)


def scrollable(inner: QWidget) -> QScrollArea:
    area = QScrollArea()
    area.setWidgetResizable(True)
    area.setFrameShape(QScrollArea.Shape.NoFrame)
    area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    area.setWidget(inner)
    return area


def header(title: str, on_back=None, *, subtitle: str = "",
           extra: list[QWidget] | None = None) -> QWidget:
    """Cabecera con botón de volver, título y acciones a la derecha."""
    bar = QWidget()
    lay = QHBoxLayout(bar)
    lay.setContentsMargins(0, 0, 0, 0)
    lay.setSpacing(16)
    if on_back is not None:
        back = RoundIconButton("←", "danger", 58)
        back.clicked.connect(on_back)
        lay.addWidget(back)
    caja = QVBoxLayout()
    caja.setSpacing(2)
    t = Title(title, 30)
    caja.addWidget(t)
    if subtitle:
        from ..widgets.toy import Body
        caja.addWidget(Body(subtitle, 16))
    contenedor = QWidget()
    contenedor.setLayout(caja)
    lay.addWidget(contenedor)
    lay.addStretch(1)
    for w in (extra or []):
        lay.addWidget(w)
    return bar


def page(*, margins: tuple[int, int, int, int] = (T.S.margin, 26, T.S.margin, 26),
         spacing: int = 20) -> tuple[QWidget, QVBoxLayout]:
    w = QWidget()
    lay = QVBoxLayout(w)
    lay.setContentsMargins(*margins)
    lay.setSpacing(spacing)
    return w, lay
