"""Clasificador de señas por vecino más cercano con confianza calibrada."""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from .features import PoseFeatures, weighted_distance
from .templates import TemplateStore

# Temperatura del reparto de probabilidad. Valores pequeños hacen la decisión
# más tajante; el valor por defecto se fijó observando las distancias reales
# entre señas calibradas (del orden de 0.2 a 0.7).
TEMPERATURE = 0.18
# Por encima de esta distancia se considera que la postura no corresponde a
# ninguna seña conocida (manos en reposo, gesto a medio hacer, ruido).
MAX_DISTANCE = 0.95


@dataclass
class Prediction:
    note: str | None
    confidence: float = 0.0
    margin: float = 0.0
    distance: float = float("inf")
    ranking: list[tuple[str, float]] = field(default_factory=list)

    @property
    def runner_up(self) -> str | None:
        return self.ranking[1][0] if len(self.ranking) > 1 else None


class GestureClassifier:
    def __init__(self, store: TemplateStore,
                 confidence_threshold: float = 0.55,
                 margin_threshold: float = 0.08,
                 temperature: float = TEMPERATURE,
                 max_distance: float = MAX_DISTANCE) -> None:
        self.store = store
        self.confidence_threshold = confidence_threshold
        self.margin_threshold = margin_threshold
        self.temperature = temperature
        self.max_distance = max_distance

    @property
    def ready(self) -> bool:
        return bool(self.store.samples)

    def calibrate_temperature(self) -> float:
        """Ajusta la temperatura a la separación real entre las señas del niño.

        Si sus señas quedaron muy parecidas entre sí, una temperatura alta
        repartiría la probabilidad entre varias notas y la aplicación nunca se
        decidiría. Se toma la mitad de la separación mínima observada, acotada
        para que el reparto no se vuelva ni plano ni degenerado:

            T = clip(0.5 * min_{a != b} d(a, b),  0.05,  0.20)
        """
        pairs = self.store.separation()
        if not pairs:
            return self.temperature
        self.temperature = float(min(0.20, max(0.05, 0.5 * pairs[0][2])))
        return self.temperature

    def distances(self, pose: PoseFeatures) -> dict[str, float]:
        """Distancia de la postura a cada nota: la menor entre sus muestras."""
        out: dict[str, float] = {}
        use_rel = self.store.relational and pose.relational_valid
        for code, samples in self.store.samples.items():
            best = min((weighted_distance(pose.vector, s, pose.hands, use_rel)
                        for s in samples), default=float("inf"))
            out[code] = best
        return out

    def classify(self, pose: PoseFeatures | None) -> Prediction:
        if pose is None or not self.ready:
            return Prediction(None)
        if pose.hands != self.store.hands:
            # La calibración se hizo con otro número de manos.
            return Prediction(None)

        dist = self.distances(pose)
        dist = {k: v for k, v in dist.items() if np.isfinite(v)}
        if not dist:
            return Prediction(None)

        codes = list(dist)
        values = np.array([dist[c] for c in codes])
        # Reparto de probabilidad tipo softmax sobre la distancia negativa,
        # anclado al mejor candidato para evitar desbordes numéricos.
        logits = -(values - values.min()) / max(self.temperature, 1e-6)
        exp = np.exp(logits)
        probs = exp / exp.sum()

        order = np.argsort(-probs)
        ranking = [(codes[i], float(probs[i])) for i in order]
        best_code, best_p = ranking[0]
        second_p = ranking[1][1] if len(ranking) > 1 else 0.0
        best_d = float(dist[best_code])

        pred = Prediction(note=None, confidence=float(best_p),
                          margin=float(best_p - second_p), distance=best_d,
                          ranking=ranking)
        if best_d > self.max_distance:
            return pred                       # ninguna seña se parece lo bastante
        if best_p < self.confidence_threshold:
            return pred
        if pred.margin < self.margin_threshold:
            return pred                       # dos señas empatadas: no se decide
        pred.note = best_code
        return pred
