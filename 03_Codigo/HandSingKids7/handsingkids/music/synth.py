"""Síntesis de los sonidos de la aplicación.

No se distribuye ningún archivo de audio: todo se genera con numpy la primera
vez que arranca la aplicación y se guarda como WAV en la carpeta de datos. Así
no hay dependencias de muestras ajenas y el timbre se puede ajustar cambiando
unos pocos números.

El timbre elegido imita un xilófono de juguete: ataque muy rápido, caída
exponencial y unos pocos parciales por encima del fundamental.
"""

from __future__ import annotations

import wave
from pathlib import Path

import numpy as np

SAMPLE_RATE = 44100

# Parciales del timbre: (razón respecto al fundamental, amplitud, factor de
# caída). Los parciales agudos se apagan antes, como en una lámina de madera.
PARTIALS: tuple[tuple[float, float, float], ...] = (
    (1.00, 1.00, 1.0),
    (2.00, 0.32, 1.6),
    (3.01, 0.14, 2.4),
    (4.02, 0.07, 3.2),
    (5.98, 0.04, 4.0),
)


def _envelope(n: int, attack_s: float, decay_s: float) -> np.ndarray:
    t = np.arange(n) / SAMPLE_RATE
    attack_n = max(1, int(attack_s * SAMPLE_RATE))
    env = np.exp(-t / decay_s)
    ramp = np.minimum(1.0, np.arange(n) / attack_n)
    # Pequeño apagado al final para que no quede un chasquido.
    tail = max(1, int(0.01 * SAMPLE_RATE))
    fade = np.ones(n)
    fade[-tail:] = np.linspace(1.0, 0.0, tail)
    return env * ramp * fade


def tone(freq: float, duration: float = 1.0, *, amplitude: float = 0.75,
         attack_s: float = 0.004, decay_s: float | None = None) -> np.ndarray:
    """Una nota con timbre de xilófono."""
    n = int(duration * SAMPLE_RATE)
    if n <= 0:
        return np.zeros(0, dtype=np.float64)
    decay = decay_s if decay_s is not None else duration * 0.45
    t = np.arange(n) / SAMPLE_RATE
    wave_sum = np.zeros(n)
    for ratio, amp, decay_factor in PARTIALS:
        partial_env = np.exp(-t / (decay / decay_factor))
        wave_sum += amp * partial_env * np.sin(2 * np.pi * freq * ratio * t)
    wave_sum *= _envelope(n, attack_s, decay)
    peak = float(np.max(np.abs(wave_sum))) or 1.0
    return amplitude * wave_sum / peak


def chime(freqs: list[float], step_s: float = 0.09, duration: float = 0.45,
          amplitude: float = 0.7) -> np.ndarray:
    """Varias notas encadenadas con un pequeño desfase: sirve para los
    efectos de acierto, estrella y desbloqueo."""
    total = int((step_s * (len(freqs) - 1) + duration) * SAMPLE_RATE) + 1
    out = np.zeros(total)
    for i, f in enumerate(freqs):
        start = int(i * step_s * SAMPLE_RATE)
        seg = tone(f, duration, amplitude=1.0)
        out[start:start + len(seg)] += seg
    peak = float(np.max(np.abs(out))) or 1.0
    return amplitude * out / peak


def click(freq: float = 1400.0, duration: float = 0.05,
          amplitude: float = 0.35) -> np.ndarray:
    """Golpe corto de madera para marcar el pulso."""
    n = int(duration * SAMPLE_RATE)
    t = np.arange(n) / SAMPLE_RATE
    body = np.sin(2 * np.pi * freq * t) * np.exp(-t / 0.012)
    noise = np.random.default_rng(3).normal(0, 0.35, n) * np.exp(-t / 0.004)
    out = body + noise
    peak = float(np.max(np.abs(out))) or 1.0
    return amplitude * out / peak


def pop(freq_from: float = 520.0, freq_to: float = 880.0,
        duration: float = 0.12, amplitude: float = 0.4) -> np.ndarray:
    """Burbuja suave para los botones."""
    n = int(duration * SAMPLE_RATE)
    t = np.arange(n) / SAMPLE_RATE
    freq = np.linspace(freq_from, freq_to, n)
    phase = 2 * np.pi * np.cumsum(freq) / SAMPLE_RATE
    out = np.sin(phase) * np.exp(-t / (duration * 0.35))
    peak = float(np.max(np.abs(out))) or 1.0
    return amplitude * out / peak


def intro_tune() -> np.ndarray:
    """Melodía corta de bienvenida, pensada para repetirse en bucle en la
    pantalla de inicio. Usa las propias notas de la aplicación (un arpegio que
    sube y baja la octava), así que ya "suena a Hand Sing Kids" sin depender
    de ningún archivo externo mientras la familia no ponga el suyo."""
    from ..domain.notes import frequency

    frase = ["DO3", "MI3", "SOL3", "DO4", "SOL3", "MI3", "DO3"]
    paso_s, dur = 0.30, 0.46
    total = int((paso_s * (len(frase) - 1) + dur) * SAMPLE_RATE) + 1
    out = np.zeros(total)
    for i, code in enumerate(frase):
        seg = tone(frequency(code), dur, amplitude=0.55)
        inicio = int(i * paso_s * SAMPLE_RATE)
        out[inicio:inicio + len(seg)] += seg
    peak = float(np.max(np.abs(out))) or 1.0
    out = 0.8 * out / peak
    # Respiro final antes de que el bucle vuelva a empezar.
    silencio = np.zeros(int(0.55 * SAMPLE_RATE))
    return np.concatenate([out, silencio])


def write_wav(path: Path, samples: np.ndarray) -> Path:
    """Guarda como WAV PCM de 16 bits, mono, que es lo que reproduce Qt."""
    data = np.clip(samples, -1.0, 1.0)
    pcm = (data * 32767.0).astype("<i2")
    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SAMPLE_RATE)
        w.writeframes(pcm.tobytes())
    return path


# --------------------------------------------------------------- catálogo

def build_all(folder: Path, force: bool = False) -> dict[str, Path]:
    """Genera todos los sonidos. Devuelve el mapa nombre -> archivo."""
    from ..domain.notes import NOTES

    folder.mkdir(parents=True, exist_ok=True)
    out: dict[str, Path] = {}

    def emit(name: str, samples_fn) -> None:
        path = folder / f"{name}.wav"
        if force or not path.exists():
            write_wav(path, samples_fn())
        out[name] = path

    for n in NOTES:
        emit(f"nota_{n.code}", lambda n=n: tone(n.frequency, 1.15, amplitude=0.8))

    do, mi, sol, do_alto = 261.63, 329.63, 392.00, 523.25
    emit("acierto", lambda: chime([mi, sol, do_alto], 0.075, 0.38, 0.65))
    emit("casi", lambda: chime([349.23, 293.66], 0.14, 0.42, 0.5))
    emit("estrella", lambda: chime([sol, do_alto, 659.26, 783.99], 0.065, 0.5, 0.7))
    emit("desbloqueo", lambda: chime([do, mi, sol, do_alto, sol, do_alto],
                                     0.085, 0.55, 0.75))
    emit("aplauso", lambda: chime([do, sol, mi, do_alto, 659.26], 0.07, 0.6, 0.72))
    emit("pulso", lambda: click(1500.0, 0.05, 0.30))
    emit("pulso_fuerte", lambda: click(1900.0, 0.06, 0.42))
    emit("boton", lambda: pop(520.0, 900.0, 0.11, 0.35))
    emit("atras", lambda: pop(760.0, 420.0, 0.12, 0.30))
    emit("musica_inicio", intro_tune)
    return out
