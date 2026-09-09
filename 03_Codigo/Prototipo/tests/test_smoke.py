"""Pruebas de humo: la estructura importa y encaja. No prueban lógica todavía."""
from __future__ import annotations

import importlib

import pytest

MODULES = [
    "Prototipo.config",
    "Prototipo.vision",
    "Prototipo.calibration",
    "Prototipo.recognizer",
    "Prototipo.game",
    "Prototipo.adaptive.profile",
    "Prototipo.adaptive.predictor",
    "Prototipo.adaptive.optimizer",
    "Prototipo.adaptive.environment",
    "Prototipo.adaptive.agent",
    "Prototipo.digital_twin.twin",
    "Prototipo.main",
]


@pytest.mark.parametrize("name", MODULES)
def test_module_importa(name):
    importlib.import_module(name)


def test_notas_y_dinamicas():
    from Prototipo import config

    assert config.NOTAS == ("DO", "RE", "MI", "FA", "SOL", "LA", "SI")
    assert config.NUM_LANDMARKS * config.LANDMARK_DIMS == 63
    assert set(config.DINAMICAS) == {"tutorial", "libre", "ritmico", "reaccion"}


def test_cli_reporta_pendiente(capsys):
    from Prototipo import main

    code = main.main(["--stage", "vision"])
    assert code == 1
    assert "pendiente" in capsys.readouterr().out.lower()


def test_acciones_rl_completas():
    from Prototipo.adaptive.environment import ACTIONS

    assert len(ACTIONS) == 6
