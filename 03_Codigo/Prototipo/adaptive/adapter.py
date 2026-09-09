"""Orquestador adaptativo — el "margen de acción" (Fases 7–11).

Este módulo es la respuesta al encargo de *pensar de forma parametrizada*:
convierte el estado del niño en **parámetros concretos de la siguiente
actividad**, siempre DENTRO de los límites que fijan el currículo y el progreso.

Cadena de decisión (§41 de main.py, en detalle):

    curriculum + progreso + diagnóstico
        └─> MargenAccion            (¿entre qué límites puedo moverme ahora?)
    perfil + predicción
        └─> Adaptador.proponer      (¿qué punto exacto elijo dentro del margen?)
              ├─ predictor.predict   desempeño esperado P_(t+1)
              ├─ optimizer.select    plan de sesión (MILP) -> Activity
              └─ agent.choose        acción a largo plazo (DQN) -> ajuste del punto
    resultado observado
        └─> Adaptador.ajustar_tras_resultado   (bucle rápido, sin re-resolver MILP)

Separación (§40): `adapter` NO evalúa gestos ni desbloquea etapas; solo decide
parámetros. `game` los ejecuta; `levels` gestiona el desbloqueo.
"""
from __future__ import annotations

from dataclasses import dataclass

from .. import config, curriculum


# ─────────────────────────────────────────────────────────────────────────────
# 1. Margen de acción — los límites del instante
# ─────────────────────────────────────────────────────────────────────────────
@dataclass
class MargenAccion:
    """Caja dentro de la que la IA puede moverse en este momento.

    Todo lo de aquí sale del CURRÍCULO y el PROGRESO (contenido desbloqueado),
    nunca del capricho del optimizador. El optimizador elige un punto; nunca
    sale de esta caja.
    """

    etapa_id: int
    rango: curriculum.RangoDificultad          # min/max de cada parámetro continuo
    notas: tuple[str, ...]                      # notas que se pueden pedir
    figuras: tuple[str, ...]                    # figuras rítmicas (por nombre)
    dinamicas: tuple[str, ...]                  # subconjunto de config.DINAMICAS
    compases: tuple[str, ...]
    dificultad_min: int = config.DIFICULTAD_MIN
    dificultad_max: int = config.DIFICULTAD_MAX
    # cuántas notas "frágiles" del diagnóstico conviene reforzar en esta sesión
    notas_a_reforzar: tuple[str, ...] = ()
    # tope de notas nuevas por sesión (evita saturar): normalmente 1
    max_notas_nuevas: int = 1


# ─────────────────────────────────────────────────────────────────────────────
# 2. Parámetros concretos de una actividad — el punto elegido
# ─────────────────────────────────────────────────────────────────────────────
@dataclass
class ParametrosActividad:
    """Punto concreto dentro del `MargenAccion`. Es lo que consume
    `game.MusicGame.next_activity` para construir la actividad real."""

    etapa_id: int
    dinamica: str
    compas: str
    bpm: int
    n_eventos: int
    densidad: float                # eventos por pulso (media objetivo)
    p_lectura: float               # proporción de eventos en pentagrama (vs. color)
    p_salto: float                 # proporción de saltos melódicos (vs. grados conjuntos)
    tol_ms: int                    # ventana de acierto de tiempo
    ayudas: int                    # nº de apoyos visuales activos
    notas: tuple[str, ...]         # notas efectivamente en juego en esta actividad
    figuras: tuple[str, ...]       # figuras efectivamente en juego
    dificultad: int                # knob grueso 1..5 (compatibilidad)
    objetivo: str = "practica"     # "practica" | "repaso" | "reto" | "evaluacion"

    def dentro_de(self, margen: MargenAccion) -> bool:
        """Chequeo de seguridad: ningún parámetro se sale de la caja."""
        raise NotImplementedError("Fase 7: validar cada campo contra margen.rango y listas")


# ─────────────────────────────────────────────────────────────────────────────
# 3. Adaptador
# ─────────────────────────────────────────────────────────────────────────────
class Adaptador:
    """Une predictor + optimizer + agent + gemelo digital en una sola decisión."""

    def __init__(self, predictor, optimizer, agent, twin=None) -> None:
        self.predictor = predictor
        self.optimizer = optimizer
        self.agent = agent
        self.twin = twin

    # ── 1. definir el margen ──────────────────────────────────────────
    def margen(self, progreso, diagnostico) -> MargenAccion:
        """Construye el `MargenAccion` de la etapa actual del niño:
        interpola `curriculum.interpolar_rango` con el progreso dentro de la
        etapa y añade las notas frágiles del diagnóstico."""
        raise NotImplementedError("Fase 7: currículo + progreso + diagnóstico -> MargenAccion")

    # ── 2. elegir el punto ────────────────────────────────────────────
    def proponer(self, profile, diagnostico, margen: MargenAccion) -> ParametrosActividad:
        """Decisión principal:
          1. `predictor.predict(profile)` -> desempeño esperado.
          2. Si el esperado es alto -> empujar hacia el máximo del rango
             (`agent.choose` puede pedir `aumentar_dificultad` /
             `introducir_nueva_nota`); si es bajo -> hacia el mínimo o `repaso`.
          3. `optimizer.select(...)` afina la mezcla de notas/figuras/dinámica
             respetando restricciones de sesión.
        Garantiza `resultado.dentro_de(margen)`.
        """
        raise NotImplementedError("Fase 7-11: resolver ParametrosActividad")

    # ── 3. bucle rápido tras cada actividad ───────────────────────────
    def ajustar_tras_resultado(self, params: ParametrosActividad, result) -> ParametrosActividad:
        """Micro-ajuste barato (sin re-resolver el MILP) para la siguiente
        actividad de la MISMA sesión: subir/bajar bpm, tol_ms, n_eventos o
        ayudas un paso según acierto/tiempo/errores. Sigue dentro del margen."""
        raise NotImplementedError("Fase 7: ajuste incremental de parámetros")

    # ── acción de largo plazo (RL) ────────────────────────────────────
    def accion_rl(self, profile) -> int:
        """Clave de `environment.ACTIONS` que el DQN recomienda para el estado
        actual. `proponer` la usa como sesgo, no como orden."""
        raise NotImplementedError("Fase 11: agent.choose(profile)")

    # ── simulación (gemelo digital) ───────────────────────────────────
    def simular_estrategia(self, profile, params: ParametrosActividad, accion: int) -> dict:
        """'¿Qué pasaría si aplico esta acción?' — rollout con el gemelo digital
        antes de comprometer la decisión. Devuelve métricas agregadas."""
        raise NotImplementedError("Fase 9: twin.simulate(...)")

    # ── helpers de mapeo rango <-> punto ──────────────────────────────
    @staticmethod
    def punto_en_rango(rango: curriculum.RangoDificultad, t: float) -> ParametrosActividad:
        """Mapea un escalar de intensidad `t` in [0, 1] a un punto del rango
        (t=0 -> todos los parámetros en su mínimo; t=1 -> en su máximo).
        Base para razonar la dificultad con UN número antes de afinar."""
        raise NotImplementedError("Fase 7: interpolación rango -> ParametrosActividad")

    @staticmethod
    def intensidad_desde_desempeno(esperado: float, objetivo: float = 0.8) -> float:
        """Traduce 'desempeño esperado' a 'intensidad deseada' in [0,1]:
        si el niño va a acertar de sobra, subir; si va justo, mantener; si va a
        fallar, bajar. Curva suave centrada en `objetivo`."""
        raise NotImplementedError("Fase 7-8: política de dificultad objetivo")
