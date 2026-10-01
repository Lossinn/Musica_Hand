"""Estimación de la probabilidad de éxito en una actividad.

Hay dos regímenes, según cuántos intentos reales tenga ya el perfil.

**Arranque en frío** (menos de `MIN_SAMPLES` intentos): una función logística
con coeficientes fijados a mano sobre la holgura entre el dominio del niño y
la dificultad de la actividad.

    p = sigma( k * (mubar - dif) + b )

**Entrenado**: en cuanto el perfil acumula suficientes intentos reales, se
ajusta por descenso de gradiente una regresión logística de tres variables
sobre los intentos de ese niño — nunca sobre datos inventados; entrenar con
datos sintéticos no mediría nada real, así que si no hay suficientes intentos
propios el modelo simplemente no se activa:

    p = sigma( w1*precision_nota + w2*dificultad + w3*dias_desde_ultima + b )

Las tres variables son exactamente las que `learning.mastery` ya calcula en
producción (`SkillState.precision`, la dificultad de la actividad y los días
desde la última práctica), así que el modelo entrenado predice sobre lo mismo
que ve cuando se usa. El ajuste se repite cada vez que se acumulan
`RETRAIN_EVERY` intentos nuevos (ver `learning.session_flow`): el agente no
se entrena una sola vez y se queda quieto, sigue cambiando con el progreso.

`SessionOptimizer` y `AdaptationEngine` solo consumen `probability()`: no les
importa si por dentro hay una fórmula fija o un modelo ajustado.
"""

from __future__ import annotations

import json
import math
import time
from dataclasses import dataclass

import numpy as np

from ..domain.entities import Activity, SkillState

LOGISTIC_K = 6.0
BIAS = 0.0

MIN_SAMPLES = 40           # intentos mínimos del perfil para confiar en un modelo propio
RETRAIN_EVERY = 20         # intentos nuevos entre un reajuste y el siguiente
LEARNING_RATE = 0.35
EPOCHS = 300
FEATURE_NAMES = ("precision_nota", "dificultad", "dias_desde_ultima")


def sigmoid(z: float) -> float:
    if z < -40:
        return 0.0
    if z > 40:
        return 1.0
    return 1.0 / (1.0 + math.exp(-z))


@dataclass
class Prediction:
    probability: float
    method: str
    features: dict[str, float]


@dataclass
class TrainingReport:
    samples: int
    accuracy: float
    trained_at: float


class MasteryPredictor:
    """Estimador de la probabilidad de superar una actividad."""

    def __init__(self, k: float = LOGISTIC_K, bias: float = BIAS) -> None:
        self.k = k
        self.bias = bias
        self.trained = False
        self.weights: list[float] | None = None
        self.trained_bias = 0.0
        self.n_samples = 0
        self.trained_at: float = 0.0
        self.train_accuracy: float = 0.0

    # ------------------------------------------------------- persistencia
    def to_json(self) -> str:
        """Serializa el modelo para guardarlo en `meta` (una fila por perfil):
        así el agente no "olvida" lo aprendido al cerrar la aplicación."""
        return json.dumps({
            "weights": self.weights, "bias": self.trained_bias,
            "n_samples": self.n_samples, "trained_at": self.trained_at,
            "train_accuracy": self.train_accuracy,
        })

    @classmethod
    def from_json(cls, data: str | None, *, k: float = LOGISTIC_K,
                  bias: float = BIAS) -> "MasteryPredictor":
        obj = cls(k=k, bias=bias)
        if not data:
            return obj
        try:
            payload = json.loads(data)
            pesos = payload.get("weights")
            if pesos:
                obj.weights = [float(w) for w in pesos]
                obj.trained_bias = float(payload.get("bias", 0.0))
                obj.n_samples = int(payload.get("n_samples", 0))
                obj.trained_at = float(payload.get("trained_at", 0.0))
                obj.train_accuracy = float(payload.get("train_accuracy", 0.0))
                obj.trained = True
        except Exception:
            pass
        return obj

    # ------------------------------------------------------- predicción
    def _note_probability(self, state: SkillState | None, difficulty: float,
                          now: float) -> float:
        if not self.trained or not self.weights:
            mu = state.mastery if state else 0.0
            return sigmoid(self.k * (mu - difficulty) + self.bias)
        precision = state.precision if state else 0.25
        dias = ((now - state.last_practice_at) / 86400.0
                if state and state.last_practice_at else 0.0)
        x = (precision, difficulty, max(0.0, min(14.0, dias)))
        z = sum(w * v for w, v in zip(self.weights, x)) + self.trained_bias
        return sigmoid(z)

    def probability(self, activity: Activity,
                    states: dict[str, SkillState], *,
                    now: float | None = None) -> Prediction:
        now = now if now is not None else time.time()
        codes = [c for c in activity.skill_codes if c in states] or list(activity.skill_codes)
        mus = [states[c].mastery for c in codes if c in states]
        mubar = sum(mus) / len(mus) if mus else 0.0

        if not self.trained or not self.weights:
            z = self.k * (mubar - activity.difficulty) + self.bias
            return Prediction(
                probability=sigmoid(z), method="logistica_parametrica",
                features={"dominio_medio": round(mubar, 4),
                          "dificultad": activity.difficulty,
                          "holgura": round(mubar - activity.difficulty, 4)})

        probs = [self._note_probability(states.get(c), activity.difficulty, now)
                 for c in codes] or [0.5]
        p = sum(probs) / len(probs)
        return Prediction(
            probability=p, method="entrenado",
            features={"dominio_medio": round(mubar, 4),
                      "dificultad": activity.difficulty,
                      "muestras_entrenamiento": float(self.n_samples)})

    # ---------------------------------------------------------- entrenamiento
    def fit(self, rows: list[dict]) -> TrainingReport | None:
        """Ajusta la regresión logística sobre intentos reales de un niño.

        `rows`: diccionarios con 'correct', 'precision_nota', 'dificultad' y
        'dias_desde_ultima' (ver `AttemptRepository.training_rows`). Si no
        hay al menos `MIN_SAMPLES`, no hace nada y devuelve `None`: un modelo
        ajustado con pocos datos generaliza peor que la fórmula fija, y con
        datos inventados no mediría nada real.
        """
        if len(rows) < MIN_SAMPLES:
            return None

        X = np.array([[r["precision_nota"], r["dificultad"],
                       r["dias_desde_ultima"]] for r in rows], dtype=float)
        y = np.array([1.0 if r["correct"] else 0.0 for r in rows], dtype=float)

        # Estandarizar para que el descenso por gradiente converja parejo:
        # las tres variables tienen escalas distintas (0-1, 0-1, 0-14).
        mu, sigma = X.mean(axis=0), X.std(axis=0)
        sigma = np.where(sigma < 1e-6, 1.0, sigma)
        Xs = (X - mu) / sigma

        w = np.zeros(Xs.shape[1])
        b = 0.0
        n = len(y)
        for _ in range(EPOCHS):
            z = Xs @ w + b
            p = 1.0 / (1.0 + np.exp(-np.clip(z, -40, 40)))
            grad_w = Xs.T @ (p - y) / n
            grad_b = float(np.mean(p - y))
            w -= LEARNING_RATE * grad_w
            b -= LEARNING_RATE * grad_b

        # Deshacer la estandarización para guardar pesos sobre las variables
        # originales: así predecir no exige repetir la normalización.
        w_orig = w / sigma
        b_orig = b - float(np.sum(w * mu / sigma))

        z_final = Xs @ w + b
        p_final = 1.0 / (1.0 + np.exp(-np.clip(z_final, -40, 40)))
        accuracy = float(np.mean((p_final >= 0.5) == (y >= 0.5)))

        self.weights = [float(v) for v in w_orig]
        self.trained_bias = float(b_orig)
        self.n_samples = n
        self.trained_at = time.time()
        self.train_accuracy = accuracy
        self.trained = True
        return TrainingReport(samples=n, accuracy=accuracy, trained_at=self.trained_at)
