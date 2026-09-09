"""Motor rítmico: patrón de figuras -> tiempos esperados (en segundos).

Heredado de MusicaManos (TA/TITI) y ampliado a todo el vocabulario de
`curriculum.py`. Cada figura aporta:
  · `offsets`: en qué fracciones de su duración hay un golpe (silencio = []).
  · `beats`:   cuántos pulsos de negra ocupa.
"""
from __future__ import annotations

# figura -> (offsets de golpe dentro de la figura, duración en pulsos)
FIGURAS = {
    "TA":            ([0.0],                  1.0),   # negra
    "SH":            ([],                     1.0),   # silencio de negra
    "TITI":          ([0.0, 0.5],             1.0),   # dos corcheas
    "TA-A":          ([0.0],                  2.0),   # blanca
    "TA-A-A-A":      ([0.0],                  4.0),   # redonda
    "TA_I_TI":       ([0.0, 1.5],             2.0),   # negra con puntillo + corchea
    "TIRITIRI":      ([0.0, 0.25, 0.5, 0.75], 1.0),   # cuatro semicorcheas
}


class RhythmEngine:
    """Convierte un patrón de figuras en la lista de tiempos (s) en los que se
    espera un golpe del niño."""

    # compat: nombres cortos de la versión anterior
    SUBDIVISIONS = {k: v[0] for k, v in FIGURAS.items()}

    def __init__(self, bpm: float = 60) -> None:
        self.set_bpm(bpm)

    def set_bpm(self, bpm: float) -> None:
        if bpm <= 0:
            raise ValueError("El BPM debe ser mayor que 0.")
        self.bpm = bpm
        self.beat_duration = 60.0 / bpm

    def pattern_to_times(self, pattern: list[str], repetitions: int = 1) -> list[float]:
        """['TA','TA','TITI','TA'] @60 BPM -> [0.0, 1.0, 2.0, 2.5, 3.0]."""
        expected: list[float] = []
        current_beat = 0.0
        for _ in range(repetitions):
            for figure in pattern:
                if figure not in FIGURAS:
                    raise ValueError(f"Figura rítmica desconocida: {figure}")
                offsets, beats = FIGURAS[figure]
                for off in offsets:
                    expected.append((current_beat + off) * self.beat_duration)
                current_beat += beats
        return expected

    def get_pattern_duration(self, pattern: list[str], repetitions: int = 1) -> float:
        total_beats = sum(FIGURAS[f][1] for f in pattern) * repetitions
        return total_beats * self.beat_duration
