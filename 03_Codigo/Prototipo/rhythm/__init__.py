"""Pilar rítmico (heredado de MusicaManos, Fase 1). IMPLEMENTADO.

    engine.RhythmEngine       patrón TA/TITI  -> tiempos esperados (según BPM)
    detector.ClapDetector     dos manos que se juntan -> un golpe (aplauso)
    evaluator.RhythmEvaluator tiempos reales vs. esperados -> juicio + precisión

El vocabulario TA/TITI mapea a `curriculum.Figura`:
    TA   -> NEGRA           TITI -> DOS_CORCHEAS
Las figuras de etapas superiores (blanca, puntillo, semicorcheas) amplían
`RhythmEngine.SUBDIVISIONS` cuando se implementen (ver curriculum.py §2).
"""
from .engine import RhythmEngine
from .detector import ClapDetector
from .evaluator import RhythmEvaluator

__all__ = ["RhythmEngine", "ClapDetector", "RhythmEvaluator"]
