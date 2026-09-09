"""Gemelo digital del niño (Fase 9).

Representación computacional del *comportamiento de aprendizaje* del niño
(no una copia física). Sirve para (§23):

  · simular distintos perfiles de estudiante (rápido / medio / lento);
  · entrenar el agente RL offline sin depender del niño real;
  · evaluar "¿qué pasaría si aplicamos esta estrategia?" antes de aplicarla.
"""
from __future__ import annotations

from dataclasses import dataclass

from .. import config


@dataclass
class TwinParams:
    """Rasgos latentes que gobiernan cómo responde el gemelo."""

    velocidad_aprendizaje: float = 0.5     # 0 lento .. 1 rápido
    propension_error: float = 0.3
    tiempo_base_s: float = 2.5
    retencion: float = 0.7                 # cuánto conserva entre sesiones


# Perfiles de referencia (§23)
PERFILES = {
    "rapido": TwinParams(0.85, 0.1, 1.6, 0.9),
    "medio": TwinParams(0.55, 0.3, 2.4, 0.7),
    "lento": TwinParams(0.25, 0.6, 3.4, 0.5),
}


class DigitalTwin:
    """Simulador del estudiante.

    Implementa la misma interfaz que espera el entorno RL: dada una actividad,
    produce un `ActivityResult` verosímil según los parámetros del gemelo y su
    estado interno actual.
    """

    def __init__(self, params: TwinParams | None = None, seed: int | None = None) -> None:
        self.params = params or PERFILES["medio"]
        self.seed = seed
        self.state = None                 # profile.StateVector interno

    @classmethod
    def from_profile(cls, profile) -> "DigitalTwin":
        """Calibra el gemelo a partir del historial de un niño real."""
        raise NotImplementedError("Fase 9: ajustar TwinParams desde el perfil")

    def respond(self, activity):
        """Simula la respuesta del niño a una actividad -> ActivityResult."""
        raise NotImplementedError("Fase 9: modelo generativo de respuesta")

    def simulate(self, profile, activity, action, horizon: int = 10):
        """Proyecta la trayectoria de aprendizaje si se aplica `action`.

        Devuelve métricas agregadas para comparar estrategias.
        """
        raise NotImplementedError("Fase 9: rollout de simulación")

    def step(self, activity):
        """Un paso: actualiza el estado interno y devuelve el resultado."""
        raise NotImplementedError("Fase 9: transición interna del gemelo")
