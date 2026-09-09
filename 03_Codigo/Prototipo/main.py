"""Hand Sing Kids — punto de entrada.

Este archivo ya refleja la ARQUITECTURA OBJETIVO (§41), pero cada componente es
todavía un esqueleto. La regla del proyecto (§42):

    Primero hacemos funcionar perfectamente cada componente; después los conectamos.

Ejecuta:  python 03_Codigo/Prototipo/main.py --help

Se puede correr por etapas con --stage:
    vision        Fases 1-3: cámara -> mano -> gesto -> nota -> juego
    calibration   Fase 4: calibración automática
    profile       Fases 5-6: registro + perfil
    adaptive      Fases 7-11: ML + MILP + DQN + gemelo digital
    full          bucle completo (§41)
"""
from __future__ import annotations

import argparse
import sys

# Ejecutable tanto como módulo (-m Prototipo.main) como script suelto.
if __package__ in (None, ""):
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    __package__ = "Prototipo"

from . import __version__, config
from .calibration import Calibrator
from .game import MusicGame
from .vision import HandVision
from .adaptive.profile import ChildProfile
from .adaptive.predictor import Predictor
from .adaptive.optimizer import ActivityOptimizer
from .adaptive.agent import AdaptiveAgent
from .digital_twin.twin import DigitalTwin


STAGES = ("vision", "calibration", "profile", "adaptive", "full")


def build_components(user_id: str, edad: int):
    """Instancia todos los módulos (barato: los constructores no abren recursos)."""
    return {
        "vision": HandVision(),
        "calibrator": Calibrator(user_id=user_id),
        "game": MusicGame(),
        "profile": ChildProfile(user_id=user_id, edad=edad),
        "predictor": Predictor(),
        "optimizer": ActivityOptimizer(),
        "agent": AdaptiveAgent(),
        "twin": DigitalTwin(),
    }


def run_full(c: dict) -> None:
    """Bucle objetivo (§41). Falla con NotImplementedError hasta implementar cada fase."""
    vision, calibrator, game = c["vision"], c["calibrator"], c["game"]
    profile, predictor = c["profile"], c["predictor"]
    optimizer, agent, twin = c["optimizer"], c["agent"], c["twin"]

    calibrator.load()
    game.start()
    with vision:
        while game.running:
            game.handle_events()
            frame = vision.capture()
            hand = vision.detect(frame)

            if hand:
                gesture = vision.recognize(hand, calibrator)
                result = game.evaluate(gesture)

                if result is not None:
                    profile.update(result)
                    prediction = predictor.predict(profile)
                    activity = optimizer.select(profile, prediction)
                    action = agent.choose(profile)
                    twin.simulate(profile, activity, action)
                    game.next_activity(activity)

            game.render(frame, hand)
            game.tick()
    game.stop()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="hand-sing-kids", description=__doc__)
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("--stage", choices=STAGES, default="vision",
                        help="etapa a ejecutar (default: vision)")
    parser.add_argument("--user", default="default", help="id del niño")
    parser.add_argument("--edad", type=int, default=7,
                        help=f"edad ({config.EDAD_MIN}-{config.EDAD_MAX})")
    args = parser.parse_args(argv)

    for d in (config.USERS_DIR, config.SESSIONS_DIR, config.CALIBRATION_DIR):
        d.mkdir(parents=True, exist_ok=True)

    components = build_components(args.user, args.edad)

    print(f"Hand Sing Kids {__version__}  ·  etapa = {args.stage}")
    try:
        if args.stage == "full":
            run_full(components)
        else:
            # Cada etapa parcial se implementará en su propio runner.
            raise NotImplementedError(
                f"La etapa '{args.stage}' aún no está implementada. "
                f"Ver 03_Codigo/README.md y el plan de fases."
            )
    except NotImplementedError as e:
        print(f"[pendiente] {e}")
        return 1
    except KeyboardInterrupt:
        print("\nInterrumpido.")
        return 130
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
