"""Pruebas del estabilizador temporal."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from handsingkids.vision.stabilizer import GestureStabilizer  # noqa: E402


def _feed(st: GestureStabilizer, lecturas, t0: float = 0.0, dt: float = 0.04):
    out = []
    for i, (note, conf) in enumerate(lecturas):
        c = st.push(note, conf, now=t0 + i * dt)
        if c:
            out.append((round(c.at - t0, 3), c.note))
    return out


def test_no_confirma_lecturas_sueltas() -> None:
    st = GestureStabilizer(window=8, agreement=0.62)
    lecturas = [("DO3", 0.9), (None, 0.0), ("SOL3", 0.8), (None, 0.0),
                ("MI3", 0.7), (None, 0.0), ("RE3", 0.9), (None, 0.0)]
    assert _feed(st, lecturas) == []


def test_confirma_una_sena_sostenida() -> None:
    st = GestureStabilizer(window=8, agreement=0.62)
    conf = _feed(st, [("DO3", 0.9)] * 8)
    assert len(conf) == 1 and conf[0][1] == "DO3"


def test_transicion_no_dispara_las_notas_del_camino() -> None:
    """Al pasar de Do a Sol el clasificador puede leer notas intermedias
    sueltas; ninguna debe confirmarse."""
    st = GestureStabilizer(window=8, agreement=0.62)
    stream = ([("DO3", 0.92)] * 8
              + [("RE3", 0.6), (None, 0.0), ("MI3", 0.58), ("FA3", 0.61),
                 (None, 0.0), ("FA3", 0.55)]
              + [("SOL3", 0.9)] * 8)
    notas = [n for _, n in _feed(st, stream)]
    assert notas == ["DO3", "SOL3"], notas


def test_permite_repetir_la_misma_nota_tras_soltar() -> None:
    st = GestureStabilizer(window=6, agreement=0.6, refractory_s=0.2,
                           release_frames=2)
    stream = ([("DO3", 0.9)] * 6 + [(None, 0.0)] * 4
              + [("DO3", 0.9)] * 6 + [(None, 0.0)] * 4
              + [("DO3", 0.9)] * 6)
    notas = [n for _, n in _feed(st, stream, dt=0.05)]
    assert notas == ["DO3", "DO3", "DO3"], notas


def test_mano_quieta_no_dispara_rafaga() -> None:
    st = GestureStabilizer(window=6, agreement=0.6, refractory_s=0.3,
                           release_frames=3)
    notas = [n for _, n in _feed(st, [("MI3", 0.95)] * 60, dt=0.04)]
    assert len(notas) == 1, f"se dispararon {len(notas)} notas con la mano quieta"


def test_confirma_de_inmediato_con_ventana_de_un_fotograma() -> None:
    """Configuración por defecto desde que se quitó la 'barra de aceptación':
    la nota debe contar en el mismo fotograma en que se reconoce, sin ninguna
    espera, y sin dejar de filtrar una lectura suelta entre fotogramas sin
    seña."""
    st = GestureStabilizer(window=1, agreement=0.62, refractory_s=0.2,
                           release_frames=1)
    conf = _feed(st, [("DO3", 0.9)])
    assert len(conf) == 1 and conf[0] == (0.0, "DO3"), conf

    st2 = GestureStabilizer(window=1, agreement=0.62)
    assert _feed(st2, [(None, 0.0)]) == []

    # Con ventana de un solo fotograma, una nota distinta en el fotograma
    # siguiente no arrastra la anterior: cada lectura se juzga por sí sola.
    st3 = GestureStabilizer(window=1, agreement=0.62, refractory_s=0.0,
                            release_frames=1)
    notas = [n for _, n in _feed(st3, [("DO3", 0.9), ("SOL3", 0.9)], dt=0.1)]
    assert notas == ["DO3", "SOL3"], notas


def test_parpadeo_breve_no_duplica_la_nota_sostenida() -> None:
    """Petición explícita del usuario: "el sonido se sigue duplicando". Con
    ventana de un fotograma, un parpadeo de 1-2 fotogramas del rastreo de la
    mano (MediaPipe pierde el contorno un instante incluso con la mano
    perfectamente quieta) no debe interpretarse como que el niño soltó la
    seña: si lo fuera, la misma nota volvería a sonar sola apenas se
    recupera el rastreo, sin que el niño haya hecho nada. Por eso
    `release_frames` viene en 6 (no en 2) para esta configuración: dos
    fotogramas de ruido no alcanzan para soltar, pero seis sí — que es lo
    que de verdad ocurre cuando el niño baja la mano o cambia de seña."""
    st = GestureStabilizer(window=1, agreement=0.62, refractory_s=0.05)
    stream = ([("DO3", 0.9)]           # se confirma de inmediato
              + [(None, 0.0)] * 2      # parpadeo breve del rastreo (~80 ms)
              + [("DO3", 0.9)] * 10)   # la mano nunca se movió de verdad
    notas = [n for _, n in _feed(st, stream, dt=0.04)]
    assert notas == ["DO3"], (
        f"un parpadeo de 2 fotogramas no debe hacer sonar la nota otra vez: {notas}")

    # En cambio, un parpadeo largo de verdad (la mano se retira o cambia de
    # postura varios fotogramas seguidos) sí debe permitir repetir la misma
    # nota: no se trata de bloquear el repetir, solo el ruido.
    st2 = GestureStabilizer(window=1, agreement=0.62, refractory_s=0.05)
    stream2 = ([("DO3", 0.9)]
              + [(None, 0.0)] * 6       # soltar de verdad
              + [("DO3", 0.9)] * 3)
    notas2 = [n for _, n in _feed(st2, stream2, dt=0.04)]
    assert notas2 == ["DO3", "DO3"], (
        f"soltar la seña de verdad sí debe permitir repetir la nota: {notas2}")


def test_el_voto_recupera_lecturas_perdidas() -> None:
    """Con ruido, algunos fotogramas se pierden; la mayoría debe imponerse."""
    st = GestureStabilizer(window=8, agreement=0.62)
    stream = [("LA3", 0.8), (None, 0.0), ("LA3", 0.85), ("LA3", 0.7),
              (None, 0.0), ("LA3", 0.9), ("LA3", 0.75), ("LA3", 0.8)]
    notas = [n for _, n in _feed(st, stream)]
    assert notas == ["LA3"], notas


if __name__ == "__main__":
    import traceback
    fallos = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn()
                print(f"  ok   {name}")
            except AssertionError:
                fallos += 1
                print(f"  FALLA {name}")
                traceback.print_exc()
    print("\nTodas las pruebas pasaron." if not fallos else f"\n{fallos} fallos.")
