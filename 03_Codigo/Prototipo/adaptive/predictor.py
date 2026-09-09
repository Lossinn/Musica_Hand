"""Modelo predictivo (Fase 8) — TensorFlow / Keras.

Estima el desempeño esperado del niño (§16):
    P_(t+1) = f(S_t, A_t)

Entradas: edad, precisión, errores, tiempo_respuesta, nivel, nota,
          repeticiones, progreso.
Salida:   desempeño esperado en [0, 1].
"""
from __future__ import annotations

from dataclasses import dataclass

from .. import config


FEATURES: tuple[str, ...] = (
    "edad",
    "precision",
    "errores",
    "tiempo_respuesta",
    "nivel",
    "nota_idx",
    "repeticiones",
    "progreso",
)


class Predictor:
    """Envuelve un modelo Keras guardado en models/predictive/."""

    def __init__(self, model_path=None) -> None:
        self.model_path = model_path or (config.MODELS_DIR / "predictive")
        self._model = None            # keras.Model

    def build(self):
        """Define la arquitectura (MLP de regresión)."""
        raise NotImplementedError("Fase 8: construir MLP Keras")

    def train(self, X, y, epochs: int = 50):
        """Entrena con el histórico de sesiones (data/sessions/)."""
        raise NotImplementedError("Fase 8: entrenamiento")

    def load(self):
        raise NotImplementedError("Fase 8: cargar modelo entrenado")

    def save(self):
        raise NotImplementedError

    def predict(self, profile, activity=None) -> float:
        """Desempeño esperado P_(t+1) para el perfil (y actividad opcional)."""
        raise NotImplementedError("Fase 8: inferencia")
