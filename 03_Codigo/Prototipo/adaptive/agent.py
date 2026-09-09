"""Agente adaptativo (Fase 11) — DQN con Stable-Baselines3.

Aprende Q(s, a): qué tan conveniente es la acción `a` en el estado `s` (§21).

    Estado: precisión alta, errores bajos, nivel 3   -> aumentar dificultad
    Estado: precisión baja, muchos errores           -> reforzar contenido

En producción, `choose(profile)` mapea el perfil actual a una acción del
conjunto de `environment.ACTIONS`.
"""
from __future__ import annotations

from .. import config
from .environment import ACTIONS, HandSingKidsEnv


class AdaptiveAgent:
    """Envuelve un modelo DQN entrenado (models/ o ruta dada)."""

    def __init__(self, model_path=None) -> None:
        self.model_path = model_path or (config.MODELS_DIR / "dqn_hsk.zip")
        self._model = None            # stable_baselines3.DQN

    def train(self, env: HandSingKidsEnv, timesteps: int = 100_000):
        """Entrena el DQN en el entorno (típicamente con el gemelo digital)."""
        raise NotImplementedError("Fase 11: DQN.learn()")

    def load(self):
        raise NotImplementedError("Fase 11: DQN.load()")

    def save(self):
        raise NotImplementedError

    def choose(self, profile) -> int:
        """Devuelve la acción adaptativa (clave de environment.ACTIONS)."""
        raise NotImplementedError("Fase 11: predicción de acción")

    @staticmethod
    def action_name(action: int) -> str:
        return ACTIONS.get(action, "desconocida")
