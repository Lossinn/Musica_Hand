"""Pruebas de humo: la estructura importa y encaja. No prueban lógica todavía."""
from __future__ import annotations

import importlib

import pytest

MODULES = [
    "Prototipo.config",
    "Prototipo.curriculum",
    "Prototipo.persistence",
    "Prototipo.auth",
    "Prototipo.diagnostics",
    "Prototipo.levels",
    "Prototipo.composer",
    "Prototipo.screens",
    "Prototipo.vision",
    "Prototipo.calibration",
    "Prototipo.recognizer",
    "Prototipo.rhythm",
    "Prototipo.rhythm.engine",
    "Prototipo.rhythm.detector",
    "Prototipo.rhythm.evaluator",
    "Prototipo.game",
    "Prototipo.adaptive.profile",
    "Prototipo.adaptive.predictor",
    "Prototipo.adaptive.optimizer",
    "Prototipo.adaptive.environment",
    "Prototipo.adaptive.agent",
    "Prototipo.adaptive.adapter",
    "Prototipo.digital_twin.twin",
    "Prototipo.main",
]


@pytest.mark.parametrize("name", MODULES)
def test_module_importa(name):
    importlib.import_module(name)


def test_notas_y_dinamicas():
    from Prototipo import config

    # octava reducida DO3..DO4 (heredada de MusicaManos)
    assert config.NOTAS == ("DO3", "RE3", "MI3", "FA3", "SOL3", "LA3", "SI3", "DO4")
    assert config.NUM_LANDMARKS * config.LANDMARK_DIMS == 63          # por mano
    assert config.GESTURE_VECTOR_DIMS == 2 * 63                       # seña = 2 manos
    assert set(config.DINAMICAS) == {"tutorial", "libre", "ritmico", "reaccion"}


def test_cli_reporta_pendiente(capsys):
    from Prototipo import main

    # 'profile' y 'adaptive' siguen siendo esqueleto
    code = main.main(["--stage", "profile"])
    assert code == 1
    assert "pendiente" in capsys.readouterr().out.lower()


def test_cli_stages_incluye_vision_y_app():
    from Prototipo import main

    assert {"vision", "calibration", "app", "full"} <= set(main.STAGES)


def test_acciones_rl_completas():
    from Prototipo.adaptive.environment import ACTIONS

    assert len(ACTIONS) == 6
