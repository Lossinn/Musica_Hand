"""Reconocimiento + calibración + ritmo (lógica pura, sin cámara)."""
from __future__ import annotations

import json

import numpy as np
import pytest

from Prototipo import config
from Prototipo.calibration import Calibrator, CalibrationProfile
from Prototipo.recognizer import GestureRecognizer, hands_to_vector, cosine_similarity
from Prototipo.rhythm import RhythmEngine, RhythmEvaluator, ClapDetector


# ── utilidades de test ────────────────────────────────────────────────────
def _hand(seed: int, label: str) -> dict:
    rng = np.random.default_rng(seed)
    lm = rng.normal(0, 0.1, size=(config.NUM_LANDMARKS, 3))
    lm[0] = [0.0, 0.0, 0.0]                       # muñeca centrada
    return {"landmarks": lm.tolist(), "hand_label": label}


def _pose(seed: int) -> list[dict]:
    return [_hand(seed, "Left"), _hand(seed + 100, "Right")]


# ── recognizer ───────────────────────────────────────────────────────────
def test_hands_to_vector_dims_y_orden():
    v = hands_to_vector(_pose(1))
    assert v.shape == (config.GESTURE_VECTOR_DIMS,)
    # el orden no depende de cómo lleguen las manos
    p = _pose(1)
    assert np.allclose(hands_to_vector(p), hands_to_vector(list(reversed(p))))


def test_cosine_similarity_bordes():
    a = np.ones(6)
    assert cosine_similarity(a, a) == pytest.approx(1.0)
    assert cosine_similarity(a, np.zeros(6)) == -1.0
    assert cosine_similarity(a, np.ones(4)) == -1.0


def test_recognizer_identifica_la_plantilla_mas_cercana():
    cal = Calibrator(user_id="t", notas=("DO3", "SOL3", "LA3"))
    cal.iniciar()
    for i, nota in enumerate(("DO3", "SOL3", "LA3")):
        assert cal.capturar(nota, _pose(i))
    rec = GestureRecognizer(cal, threshold=0.0)
    # una pose casi idéntica a la de SOL3 -> SOL3
    assert rec.recognize(_pose(1)) == "SOL3"


def test_recognizer_none_sin_dos_manos_o_sin_plantillas():
    cal = Calibrator(user_id="t", notas=("DO3",))
    rec = GestureRecognizer(cal)
    assert rec.recognize([]) is None
    assert rec.recognize([_hand(1, "Left")]) is None          # una sola mano
    cal.iniciar()
    cal.capturar("DO3", _pose(0))
    assert rec.recognize(_pose(0)) == "DO3"                    # ahora sí


def test_recognizer_umbral_rechaza_lo_disímil():
    cal = Calibrator(user_id="t", notas=("DO3",))
    cal.iniciar()
    cal.capturar("DO3", _pose(0))
    rec = GestureRecognizer(cal, threshold=0.999)
    assert rec.recognize(_pose(42)) is None                   # pose distinta


def test_gesture_to_note_identidad():
    assert GestureRecognizer.gesture_to_note("MI3") == "MI3"
    assert GestureRecognizer.gesture_to_note("XX") is None


# ── calibration ──────────────────────────────────────────────────────────
def test_calibracion_guiada_avanza_y_completa():
    cal = Calibrator(user_id="t", notas=("DO3", "RE3"))
    cal.iniciar()
    assert cal.siguiente_nota() == "DO3"
    assert not cal.capturar("DO3", [_hand(1, "Left")])        # falta una mano: no avanza
    assert cal.siguiente_nota() == "DO3"
    assert cal.capturar("DO3", _pose(1))
    assert cal.siguiente_nota() == "RE3"
    assert cal.progreso() == pytest.approx(0.5)
    assert cal.capturar("RE3", _pose(2))
    assert cal.completa()
    assert cal.siguiente_nota() is None


def test_calibracion_roundtrip_disco(tmp_path, monkeypatch):
    monkeypatch.setattr(config, "CALIBRATION_DIR", tmp_path)
    cal = Calibrator(user_id="nino_01", notas=("DO3", "SOL3"))
    cal.iniciar()
    cal.capturar("DO3", _pose(3))
    cal.capturar("SOL3", _pose(4))
    cal.save()
    assert cal.path().exists()

    otro = Calibrator(user_id="nino_01", notas=("DO3", "SOL3"))
    otro.load(fallback_to_referencia=False)
    assert set(otro.notas_calibradas()) == {"DO3", "SOL3"}
    assert set(otro.templates()) == {"DO3", "SOL3"}
    assert otro.classify(_pose(3)) == "DO3"


def test_calibration_profile_lee_formato_referencia():
    """El JSON de MusicaManos es {nota: {"hands": [...]}} sin envoltura."""
    crudo = {"DO3": {"hands": [
        {"landmarks": [[0, 0, 0]] * 21, "hand_label": "Left"},
        {"landmarks": [[0, 0, 0]] * 21, "hand_label": "Right"},
    ]}}
    prof = CalibrationProfile.from_json(json.dumps(crudo))
    assert "DO3" in prof.references


def test_pentagrama_referencia_carga_las_8_notas():
    if not config.PENTAGRAMA_REFERENCIA.exists():
        pytest.skip("sin archivo de referencia")
    prof = CalibrationProfile.from_json(
        config.PENTAGRAMA_REFERENCIA.read_text(encoding="utf-8")
    )
    assert set(prof.references) == set(config.NOTAS)


# ── rhythm ───────────────────────────────────────────────────────────────
def test_rhythm_engine_ta_titi():
    eng = RhythmEngine(bpm=60)
    assert eng.pattern_to_times(["TA", "TA", "TITI", "TA"]) == [0.0, 1.0, 2.0, 2.5, 3.0]
    assert eng.get_pattern_duration(["TA", "TA-A"]) == 3.0     # 1 + 2 pulsos


def test_rhythm_engine_bpm_escala_tiempos():
    assert RhythmEngine(bpm=120).pattern_to_times(["TA", "TA"]) == [0.0, 0.5]
    with pytest.raises(ValueError):
        RhythmEngine(bpm=0)


def test_rhythm_evaluator_juicios():
    ev = RhythmEvaluator()
    assert ev.classify_error(0.05) == "Perfect"
    assert ev.classify_error(0.15) == "Good"
    assert ev.classify_error(0.5) == "Miss"
    res = ev.evaluate([0.0, 1.0, 2.0], [0.02, 1.05, 1.9])
    assert res["matched_hits"] == 3
    assert res["accuracy"] > 0


def test_clap_detector_detecta_acercamiento():
    det = ClapDetector(clap_distance=0.16, release_distance=0.22, cooldown=0.0)
    lejos = [
        {"landmarks": [[0.0, 0.0, 0.0]], "hand_label": "Left"},
        {"landmarks": [[0.5, 0.0, 0.0]], "hand_label": "Right"},
    ]
    cerca = [
        {"landmarks": [[0.0, 0.0, 0.0]], "hand_label": "Left"},
        {"landmarks": [[0.05, 0.0, 0.0]], "hand_label": "Right"},
    ]
    assert det.update(lejos, timestamp=0.0) is False
    assert det.update(cerca, timestamp=0.1) is True            # aplauso
    assert det.update(cerca, timestamp=0.2) is False           # sigue junto
