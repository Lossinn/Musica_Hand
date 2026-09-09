"""Hand Sing Music — punto de entrada.

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

# La consola de Windows no siempre usa UTF-8; evita mojibake en los acentos.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass

# Ejecutable tanto como módulo (-m Prototipo.main) como script suelto.
if __package__ in (None, ""):
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    __package__ = "Prototipo"

from . import __version__, config
from .auth import AuthService
from .calibration import Calibrator
from .composer import Editor
from .diagnostics import Diagnosticador
from .game import MusicGame
from .levels import GestorNiveles
from .persistence import JsonStore
from .screens import App
from .vision import HandVision, VisionUnavailable
from .adaptive.adapter import Adaptador
from .adaptive.profile import ChildProfile
from .adaptive.predictor import Predictor
from .adaptive.optimizer import ActivityOptimizer
from .adaptive.agent import AdaptiveAgent
from .digital_twin.twin import DigitalTwin


STAGES = ("vision", "calibration", "profile", "adaptive", "app", "full")


def build_components(user_id: str, edad: int):
    """Instancia todos los módulos (barato: los constructores no abren recursos)."""
    store = JsonStore()
    predictor = Predictor()
    optimizer = ActivityOptimizer()
    agent = AdaptiveAgent()
    twin = DigitalTwin()
    diagnosticador = Diagnosticador(store)
    return {
        "store": store,
        "auth": AuthService(store),
        "vision": HandVision(),
        "calibrator": Calibrator(user_id=user_id),
        "diagnosticador": diagnosticador,
        "gestor_niveles": GestorNiveles(store, diagnosticador),
        "game": MusicGame(),
        "profile": ChildProfile(user_id=user_id, edad=edad),
        "predictor": predictor,
        "optimizer": optimizer,
        "agent": agent,
        "twin": twin,
        "adaptador": Adaptador(predictor, optimizer, agent, twin),
        "editor_factory": lambda **kw: Editor(store, user_id=user_id, **kw),
    }


def run_app(c: dict) -> int:
    """Flujo completo de la app por pantallas (screens.App). §12."""
    return App(c).run()


def run_vision(c: dict) -> int:
    """Fases 2–3: abre la cámara real, reconoce señas y las imprime.
    Sirve para verificar visión + calibración sin la UED del juego."""
    vision, calibrator = c["vision"], c["calibrator"]
    calibrator.load()                     # usa la calibración del niño o la de referencia
    n_templates = len(calibrator.templates())
    print(f"Plantillas cargadas: {n_templates}/{len(config.NOTAS)} "
          f"({'calibración del niño' if calibrator.path().exists() else 'referencia'})")
    print("Haz señas frente a la cámara (las DOS manos). Ctrl+C para salir.")
    ultima = None
    with vision:
        while True:
            hands_data, _ = vision.read()
            nota = vision.recognize(hands_data, calibrator)
            if nota and nota != ultima:
                print(f"  ♪ {nota}")
            ultima = nota
    return 0


def run_calibration(c: dict) -> int:
    """Fase 4: calibración guiada por consola (captura con ENTER)."""
    vision, calibrator = c["vision"], c["calibrator"]
    calibrator.iniciar()
    print("Calibración: coloca la seña con AMBAS manos y pulsa ENTER para capturar.")
    with vision:
        while not calibrator.completa():
            nota = calibrator.siguiente_nota()
            input(f"  Seña para {nota} → ENTER...")
            hands_data, _ = vision.read()
            if calibrator.capturar(nota, hands_data):
                print(f"  ✓ {nota} capturada")
            else:
                print("  ✗ no se vieron dos manos, reintenta")
    calibrator.save()
    print(f"Calibración guardada en {calibrator.path()}")
    return 0


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
            hands_data, frame = vision.read()

            if hands_data:
                gesture = vision.recognize(hands_data, calibrator)
                result = game.evaluate(gesture)

                if result is not None:
                    profile.update(result)
                    prediction = predictor.predict(profile)
                    activity = optimizer.select(profile, prediction)
                    action = agent.choose(profile)
                    twin.simulate(profile, activity, action)
                    game.next_activity(activity)

            game.render(frame, hands_data)
            game.tick()
    game.stop()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="hand-sing-music", description=__doc__)
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("--stage", choices=STAGES, default="vision",
                        help="etapa a ejecutar (default: vision)")
    parser.add_argument("--user", default="default", help="id del niño")
    parser.add_argument("--edad", type=int, default=7,
                        help=f"edad ({config.EDAD_MIN}-{config.EDAD_MAX})")
    args = parser.parse_args(argv)

    for d in config.DATA_SUBDIRS:
        d.mkdir(parents=True, exist_ok=True)

    components = build_components(args.user, args.edad)

    print(f"Hand Sing Music {__version__}  ·  etapa = {args.stage}")
    try:
        if args.stage == "full":
            run_full(components)
        elif args.stage == "app":
            return run_app(components)
        elif args.stage == "vision":
            return run_vision(components)
        elif args.stage == "calibration":
            return run_calibration(components)
        else:
            # Cada etapa parcial se implementará en su propio runner.
            raise NotImplementedError(
                f"La etapa '{args.stage}' aún no está implementada. "
                f"Ver 03_Codigo/README.md y el plan de fases."
            )
    except NotImplementedError as e:
        print(f"[pendiente] {e}")
        return 1
    except VisionUnavailable as e:
        print(f"[cámara] {e}")
        return 2
    except KeyboardInterrupt:
        print("\nInterrumpido.")
        return 130
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
