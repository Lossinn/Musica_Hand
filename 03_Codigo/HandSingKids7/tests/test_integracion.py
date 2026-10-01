"""Prueba de extremo a extremo del ciclo completo, sin cámara y sin ventana.

Se alimenta el reconocedor con las posturas reales del archivo de calibración,
como si el niño estuviera haciendo las señas, y se comprueba que el recorrido
entero funciona: gesto reconocido, nota emitida, intento evaluado, dominio
actualizado, estrellas repartidas y siguiente actividad decidida.

Es la prueba que responde a la pregunta «¿esto de verdad funciona junto?».
"""

from __future__ import annotations

import json
import os
import shutil
import sys
import time
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

DATOS = Path("/tmp/hsk_integracion")
FIXTURE = ROOT / "tests" / "fixtures" / "calibracion_v1.json"


def _montar():
    from PySide6.QtWidgets import QApplication

    if DATOS.exists():
        shutil.rmtree(DATOS)
    app = QApplication.instance() or QApplication([])

    from handsingkids.core import config
    config.set_data_dir(DATOS)
    from handsingkids.data.database import Database, set_db
    set_db(Database(DATOS / "integracion.sqlite3"))

    from handsingkids.app import AppContext
    ctx = AppContext()
    perfil = ctx.profiles.create("Prueba", 7, "iguana")
    ctx.select_profile(perfil)

    # Calibración: se importa la del proyecto como si el niño la acabara de hacer.
    from handsingkids.vision.templates import TemplateStore
    store = TemplateStore(perfil.id)
    assert store.import_legacy(FIXTURE) == 8, "no se importaron las ocho señas"
    store.save()
    ctx.gestures.set_profile(perfil.id)
    assert ctx.gestures.calibrated
    return app, ctx, perfil


def _posturas() -> dict:
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def _hacer_sena(ctx, hands, veces: int = 10, fps: float = 24.0) -> None:
    """Simula que el niño sostiene una seña frente a la cámara."""
    for _ in range(veces):
        ctx.gestures._on_frame(None, hands)
        time.sleep(1.0 / fps)


def _soltar(ctx, veces: int = 6, fps: float = 24.0) -> None:
    for _ in range(veces):
        ctx.gestures._on_frame(None, [])
        time.sleep(1.0 / fps)


def main() -> int:
    from PySide6.QtCore import QTimer

    app, ctx, perfil = _montar()
    posturas = _posturas()
    fallos: list[str] = []

    def comprobar(condicion: bool, mensaje: str) -> None:
        if condicion:
            print(f"  ok   {mensaje}")
        else:
            fallos.append(mensaje)
            print(f"  FALLA {mensaje}")

    # ---------------------------------------------------------------- 1
    print("\n1. Reconocimiento a partir de posturas reales")
    from handsingkids.core.events import Event
    confirmadas: list[str] = []
    ctx.bus.subscribe(Event.GESTURE_CONFIRMED,
                      lambda m: confirmadas.append(m.get("note")))
    for nota in ("DO3", "RE3", "MI3"):
        _hacer_sena(ctx, posturas[nota]["hands"])
        _soltar(ctx)
    comprobar(confirmadas == ["DO3", "RE3", "MI3"],
              f"las tres señas se reconocieron en orden ({confirmadas})")

    # ---------------------------------------------------------------- 2
    print("\n2. Una actividad completa")
    from handsingkids.learning.evaluation import ActivityRunner
    from handsingkids.learning.session_flow import apply_result

    actividad = ctx.activities.get("n1_trio")      # DO RE MI RE
    runner = ActivityRunner(actividad, perfil.id, perfil.age_band, ctx.bus)
    terminado: list = []
    runner.finished.connect(lambda r: terminado.append(r))

    desuscribir = ctx.bus.subscribe(
        Event.GESTURE_CONFIRMED,
        lambda m: (ctx.music.trigger(m.get("note"), m.get("confidence", 1.0)),
                   runner.submit(m.get("note"), m.get("confidence", 1.0))))
    runner.start()

    for esperada in actividad.sequence:
        limite = time.time() + 4.0
        while runner.running and runner.step and \
                runner.step.expected == esperada and time.time() < limite:
            _hacer_sena(ctx, posturas[esperada]["hands"], veces=4)
            app.processEvents()
            _soltar(ctx, veces=3)
            app.processEvents()
            time.sleep(0.05)
    limite = time.time() + 3.0
    while not terminado and time.time() < limite:
        app.processEvents()
        time.sleep(0.05)
    desuscribir()

    comprobar(bool(terminado), "la actividad terminó sola al completar la secuencia")
    if not terminado:
        runner.finish()
        terminado.append(runner.build_result())
    resultado = terminado[0]
    comprobar(resultado.steps_correct == resultado.steps_total,
              f"se acertaron todos los pasos ({resultado.summary_line})")
    comprobar(resultado.stars == 3, f"se otorgaron tres estrellas ({resultado.stars})")

    # ---------------------------------------------------------------- 3
    print("\n3. Persistencia y dominio")
    outcome = apply_result(ctx, runner)
    estados = ctx.skill_states.for_profile(perfil.id)

    comprobar(ctx.attempts.total(perfil.id) >= resultado.steps_total,
              f"los intentos quedaron guardados ({ctx.attempts.total(perfil.id)})")
    comprobar(all(estados[f"nota_{n}"].attempts > 0 for n in ("DO3", "RE3", "MI3")),
              "el dominio se actualizó para las tres notas")
    comprobar(all(0 < estados[f"nota_{n}"].mastery < 1 for n in ("DO3", "RE3", "MI3")),
              "los valores de dominio están en rango")
    comprobar(all(estados[f"nota_{n}"].due_at > time.time()
                  for n in ("DO3", "RE3", "MI3")),
              "se programó el próximo repaso de cada nota")
    perfil_actualizado = ctx.profiles.get(perfil.id)
    comprobar(perfil_actualizado.stars > 0,
              f"el perfil ganó estrellas ({perfil_actualizado.stars})")
    comprobar("primer_gesto" in outcome.achievements,
              f"se desbloqueó algún logro ({outcome.achievements})")

    # ---------------------------------------------------------------- 4
    print("\n4. Decisión de la siguiente actividad")
    from handsingkids.learning.adaptation import AdaptationEngine, Context
    catalogo = {s.code: s for s in ctx.skills.all()}
    contexto = Context(skill_states=estados, skills=catalogo,
                       last_accuracy=resultado.accuracy,
                       consecutive_failures=ctx.consecutive_failures,
                       activities_in_session=len(ctx.session_results),
                       minutes_in_session=ctx.minutes_in_session,
                       age_band=perfil.age_band)
    plan = AdaptationEngine().decide(contexto)
    comprobar(plan.decision is not None,
              f"el motor adaptativo decidió: {plan.decision.value} — {plan.reason}")

    seleccion = ctx.optimizer.solve(
        [a for a in ctx.activities.all() if a.level == 1 and a.sequence][:20],
        estados)
    comprobar(len(seleccion.activities) > 0,
              f"el optimizador armó una ruta ({seleccion.method}, "
              f"{len(seleccion.activities)} actividades)")

    # ---------------------------------------------------------------- 5
    print("\n5. Aislamiento de los datos")
    comprobar((DATOS / "integracion.sqlite3").exists(),
              "la base de datos se creó en la carpeta de datos")
    comprobar((DATOS / "gestos" / f"perfil_{perfil.id}.json").exists(),
              "las plantillas se guardaron por perfil")
    comprobar(len(list((DATOS / "audio").glob("*.wav"))) >= 15,
              "los sonidos se generaron en el primer arranque")

    ctx.shutdown()
    print()
    if fallos:
        print(f"{len(fallos)} comprobaciones fallaron:")
        for f in fallos:
            print("  ·", f)
        return 1
    print("El ciclo completo funciona de extremo a extremo.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
