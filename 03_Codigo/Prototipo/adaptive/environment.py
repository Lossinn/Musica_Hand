"""Entorno de aprendizaje por refuerzo (Fase 10) — Gymnasium.

Ciclo (§17):
    estado -> agente -> acción -> actividad -> niño -> resultado
           -> recompensa -> nuevo estado

Estado (§18):   S_t = (P, E, T, D, N, M)
Acciones (§19): 0 repetir · 1 cambiar nota · 2 subir dificultad
                3 bajar dificultad · 4 cambiar dinámica · 5 nueva nota
Recompensa (§20): R_t = w1·P_t − w2·E_t − w3·T_t + w4·L_t

El "niño" que responde puede ser el niño real (online) o el gemelo digital
(entrenamiento offline).
"""
from __future__ import annotations

import numpy as np

from .. import config

try:  # gymnasium es dependencia de fase avanzada
    import gymnasium as gym
    from gymnasium import spaces
    _Base = gym.Env
except ImportError:  # pragma: no cover
    gym = None
    spaces = None
    _Base = object


ACTIONS = {
    0: "repetir_actividad",
    1: "cambiar_nota",
    2: "aumentar_dificultad",
    3: "disminuir_dificultad",
    4: "cambiar_dinamica",
    5: "introducir_nueva_nota",
}


class HandSingMusicEnv(_Base):
    """Entorno RL. `student` responde actividades (niño real o DigitalTwin)."""

    metadata = {"render_modes": []}

    def __init__(self, student=None, reward_weights: dict | None = None) -> None:
        super().__init__()
        self.student = student
        self.reward_weights = reward_weights or dict(config.REWARD_WEIGHTS)
        # observación: vector de estado de 6 dimensiones
        if spaces is not None:
            self.observation_space = spaces.Box(
                low=0.0, high=1.0, shape=(6,), dtype=np.float32
            )
            self.action_space = spaces.Discrete(len(ACTIONS))

    def reset(self, *, seed=None, options=None):
        raise NotImplementedError("Fase 10: estado inicial del entorno")

    def step(self, action: int):
        """Aplica la acción, obtiene el resultado del estudiante y la recompensa.

        Devuelve (obs, reward, terminated, truncated, info).
        """
        raise NotImplementedError("Fase 10: transición del entorno")

    def _reward(self, result) -> float:
        """R_t = w1·P − w2·E − w3·T + w4·L."""
        raise NotImplementedError("Fase 10: cálculo de recompensa")
