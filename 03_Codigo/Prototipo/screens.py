"""Máquina de estados del flujo de la app (Fase 12 — integración).

Mapea los 5 pasos del diseño a pantallas y define qué transiciones son legales
(el "margen de acción" del flujo). La lógica de cada pantalla vive en su handler;
`screens` solo garantiza que no se pueda, p. ej., entrar a 'niveles' sin haber
calibrado.

    Paso 1 (ingreso)      -> BIENVENIDA -> LOGIN | CREAR_PERFIL
    Paso 2 (calibración)  -> CALIBRACION -> DIAGNOSTICO
    Paso 3 (niveles)      -> NIVELES
    Paso 4 (creación)     -> COMPOSITOR
    Paso 5 (progreso)     -> JUEGO -> RESUMEN -> NIVELES

Render y eventos concretos (pygame) los pone `game.py` / la capa de UI; aquí solo
está el grafo y el contexto compartido.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class Pantalla(str, Enum):
    BIENVENIDA = "bienvenida"
    LOGIN = "login"
    CREAR_PERFIL = "crear_perfil"
    CALIBRACION = "calibracion"
    DIAGNOSTICO = "diagnostico"
    NIVELES = "niveles"
    JUEGO = "juego"
    COMPOSITOR = "compositor"
    RESUMEN = "resumen"
    AJUSTES = "ajustes"


# Grafo de transiciones legales. `screens.puede_ir_a` lo consulta.
TRANSICIONES: dict[Pantalla, tuple[Pantalla, ...]] = {
    Pantalla.BIENVENIDA:   (Pantalla.LOGIN, Pantalla.CREAR_PERFIL, Pantalla.AJUSTES),
    Pantalla.LOGIN:        (Pantalla.BIENVENIDA, Pantalla.CALIBRACION, Pantalla.NIVELES),
    Pantalla.CREAR_PERFIL: (Pantalla.BIENVENIDA, Pantalla.CALIBRACION),
    Pantalla.CALIBRACION:  (Pantalla.DIAGNOSTICO, Pantalla.NIVELES),
    Pantalla.DIAGNOSTICO:  (Pantalla.NIVELES,),
    Pantalla.NIVELES:      (Pantalla.JUEGO, Pantalla.COMPOSITOR, Pantalla.CALIBRACION,
                            Pantalla.AJUSTES, Pantalla.BIENVENIDA),
    Pantalla.JUEGO:        (Pantalla.RESUMEN, Pantalla.NIVELES),
    Pantalla.COMPOSITOR:   (Pantalla.NIVELES,),
    Pantalla.RESUMEN:      (Pantalla.NIVELES, Pantalla.JUEGO),
    Pantalla.AJUSTES:      (Pantalla.BIENVENIDA, Pantalla.NIVELES),
}

# Precondiciones de datos para entrar a cada pantalla (además del grafo).
#   clave de ContextoApp que debe estar presente (no None).
REQUISITOS: dict[Pantalla, tuple[str, ...]] = {
    Pantalla.CALIBRACION: ("perfil",),
    Pantalla.DIAGNOSTICO: ("perfil", "calibracion"),
    Pantalla.NIVELES:     ("perfil", "calibracion", "progreso"),
    Pantalla.JUEGO:       ("perfil", "calibracion", "progreso", "etapa_seleccionada"),
    Pantalla.COMPOSITOR:  ("perfil", "calibracion", "progreso"),
    Pantalla.RESUMEN:     ("perfil", "diagnostico"),
}


@dataclass
class ContextoApp:
    """Estado compartido entre pantallas durante una ejecución."""

    pantalla: Pantalla = Pantalla.BIENVENIDA
    perfil: object | None = None            # auth.Perfil
    calibracion: object | None = None       # calibration.CalibrationProfile
    diagnostico: object | None = None       # diagnostics.Diagnostico
    progreso: object | None = None          # levels.ProgresoJugador
    etapa_seleccionada: int | None = None
    modo_compositor: str = "libre"          # "nivel" | "libre"
    historial_pantallas: list[Pantalla] = field(default_factory=list)

    def tiene(self, clave: str) -> bool:
        return getattr(self, clave, None) is not None


class TransicionInvalida(Exception):
    """Se intentó ir a una pantalla no alcanzable o sin los datos requeridos."""


class App:
    """Bucle de alto nivel. Instancia y cablea todos los servicios; delega el
    render/eventos de cada pantalla en su handler."""

    def __init__(self, componentes: dict) -> None:
        # componentes: auth, calibrator, diagnosticador, gestor_niveles,
        #   adaptador, game, vision, editor_factory
        self.c = componentes
        self.ctx = ContextoApp()

    # ── navegación ─────────────────────────────────────────────────────
    def puede_ir_a(self, destino: Pantalla) -> bool:
        """Legal si (a) está en TRANSICIONES[actual] y (b) el contexto cumple
        REQUISITOS[destino]."""
        raise NotImplementedError("Fase 12: validar grafo + requisitos de datos")

    def ir_a(self, destino: Pantalla) -> None:
        """Cambia de pantalla o lanza `TransicionInvalida`."""
        raise NotImplementedError("Fase 12: push historial + set pantalla")

    def atras(self) -> None:
        raise NotImplementedError("Fase 12: pop historial")

    # ── bucle ──────────────────────────────────────────────────────────
    def run(self) -> int:
        """Bucle principal: despacha al handler de `self.ctx.pantalla` hasta
        que el niño sale. Devuelve un código de salida."""
        raise NotImplementedError("Fase 12: dispatch de pantallas")

    # ── handlers (uno por pantalla) ────────────────────────────────────
    # Cada handler consume/rellena `self.ctx` y llama a `ir_a(...)`.
    def _bienvenida(self) -> None: raise NotImplementedError("Fase 1: 'Comenzar/Aprender/Ajustes'")
    def _login(self) -> None: raise NotImplementedError("Fase 6: auth.login -> ctx.perfil")
    def _crear_perfil(self) -> None: raise NotImplementedError("Fase 6: auth.crear_perfil")
    def _calibracion(self) -> None: raise NotImplementedError("Fase 4: calibrator.run_auto -> ctx.calibracion")
    def _diagnostico(self) -> None: raise NotImplementedError("Fase 6: prueba de colocación -> ctx.diagnostico + progreso")
    def _niveles(self) -> None: raise NotImplementedError("Fase 12: gestor_niveles.resumen_ui; elegir etapa o compositor")
    def _juego(self) -> None: raise NotImplementedError("Fase 1-11: bucle de actividad adaptativa")
    def _compositor(self) -> None: raise NotImplementedError("Fase 1: Editor (modo nivel/libre)")
    def _resumen(self) -> None: raise NotImplementedError("Fase 6: diagnosticador.resumen_sesion + estrellas")
    def _ajustes(self) -> None: raise NotImplementedError("Fase 12: volumen, cámara, cambiar contraseña")
