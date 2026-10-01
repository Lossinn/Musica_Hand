"""Las ocho notas de la octava de trabajo.

Se conservan los nombres de la versión 1 (DO3..DO4) para que las calibraciones
existentes sigan siendo válidas. La afinación corresponde a la cuarta octava
del piano: DO3 aquí es el do central, 261.63 Hz.
"""

from __future__ import annotations

from dataclasses import dataclass

A4 = 440.0


@dataclass(frozen=True)
class Note:
    code: str          # identificador interno y clave de calibración
    solfa: str         # nombre cantado
    scientific: str    # notación científica
    semitones: int     # distancia en semitonos respecto a La4
    degree: int        # grado de la escala, 1..8
    staff_step: int    # posición en el pentagrama, 0 = primera línea adicional

    @property
    def frequency(self) -> float:
        return A4 * (2.0 ** (self.semitones / 12.0))


NOTES: tuple[Note, ...] = (
    Note("DO3",  "Do",  "C4",  -9, 1, 0),
    Note("RE3",  "Re",  "D4",  -7, 2, 1),
    Note("MI3",  "Mi",  "E4",  -5, 3, 2),
    Note("FA3",  "Fa",  "F4",  -4, 4, 3),
    Note("SOL3", "Sol", "G4",  -2, 5, 4),
    Note("LA3",  "La",  "A4",   0, 6, 5),
    Note("SI3",  "Si",  "B4",   2, 7, 6),
    Note("DO4",  "Do↑", "C5",   3, 8, 7),
)

NOTE_CODES: tuple[str, ...] = tuple(n.code for n in NOTES)
BY_CODE: dict[str, Note] = {n.code: n for n in NOTES}

# Silencio: no es una nota ni una seña que la cámara reconozca, es una marca
# que el niño agrega a mano en el modo libre para dejar un espacio sin sonido
# dentro de su melodía. Se usa como cualquier otro código dentro de una
# secuencia, pero nunca aparece en NOTE_CODES ni requiere calibración.
SILENCE = "_"


def note(code: str) -> Note:
    return BY_CODE[code]


def is_silence(code: str) -> bool:
    return code == SILENCE


def solfa(code: str) -> str:
    if code == SILENCE:
        return "𝄽"
    n = BY_CODE.get(code)
    return n.solfa if n else code


def frequency(code: str) -> float:
    return BY_CODE[code].frequency


def index_of(code: str) -> int:
    return NOTE_CODES.index(code)


def interval(a: str, b: str) -> int:
    """Distancia en grados de la escala entre dos notas."""
    return abs(index_of(a) - index_of(b))


def sequence_span(seq: list[str]) -> int:
    """Amplitud de una secuencia: distancia entre la nota más grave y la más aguda."""
    if not seq:
        return 0
    idx = [index_of(c) for c in seq if c in BY_CODE]
    return (max(idx) - min(idx)) if idx else 0
