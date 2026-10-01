"""Renderiza cada pantalla sin abrir una ventana y guarda una imagen.

Sirve para revisar la interfaz en un entorno sin pantalla y para detectar
errores de construcción antes de entregar. No sustituye a la prueba real con
cámara, que solo puede hacerse en el equipo del usuario.
"""

from __future__ import annotations

import os
import shutil
import sys
import time
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

SALIDA = Path(os.environ.get("HSK_SHOTS", "/tmp/hsk_capturas"))
DATOS = Path("/tmp/hsk_demo_data")


def preparar_datos(ctx):
    """Crea un perfil con historial para que las pantallas no salgan vacías."""
    import json
    import random
    from handsingkids.domain.entities import (ActivityResult, Attempt,
                                              SkillState, SkillStatus)
    from handsingkids.learning import mastery as M
    from handsingkids.vision.templates import TemplateStore

    perfil = ctx.profiles.create("Mateo", 7, "iguana")
    ctx.select_profile(perfil)

    store = TemplateStore(perfil.id)
    store.import_legacy(ROOT / "tests" / "fixtures" / "calibracion_v1.json")
    store.save()
    ctx.gestures.set_profile(perfil.id)
    perfil.calibrated = True
    perfil.stars = 18
    perfil.streak_days = 3
    ctx.profiles.save(perfil)

    rng = random.Random(4)
    ahora = time.time()
    dominio = {"DO3": 0.95, "RE3": 0.88, "MI3": 0.42, "FA3": 0.55,
               "SOL3": 0.81, "LA3": 0.30, "SI3": 0.0, "DO4": 0.0}
    for nota, objetivo in dominio.items():
        if objetivo <= 0:
            continue
        st = SkillState(perfil.id, f"nota_{nota}", status=SkillStatus.PRACTICING)
        intentos = 18
        aciertos = int(intentos * min(1.0, objetivo + 0.05))
        recientes = [True] * aciertos + [False] * (intentos - aciertos)
        rng.shuffle(recientes)
        M.update_skill(st, recent=recientes[-8:], new_hits=aciertos,
                       new_attempts=intentos,
                       reaction_ms=1200 + (1 - objetivo) * 2600,
                       age_band="medianos", quality=objetivo,
                       now=ahora - rng.random() * 3 * 86400)
        ctx.skill_states.save(st)
        for i in range(10):
            correcto = rng.random() < objetivo
            detectada = nota if correcto else rng.choice(list(dominio))
            ctx.attempts.add(Attempt(
                profile_id=perfil.id, activity_code="n1_trio", step_index=i,
                expected=nota, detected=detectada, confidence=0.7 + 0.25 * rng.random(),
                correct=correcto, reaction_ms=int(900 + rng.random() * 2500),
                at=ahora - rng.random() * 5 * 86400))

    for codigo, precision in (("n1_DO3_intro", 96), ("n1_RE3_intro", 92),
                              ("n1_do_re", 88), ("n1_trio", 74),
                              ("n1_juego_burbujas", 81), ("n2_FA3_intro", 62),
                              ("cancion_estrellita", 70)):
        r = ActivityResult(
            profile_id=perfil.id, activity_code=codigo, accuracy=precision,
            rhythm=precision - 6, gesture_quality=84,
            stars=3 if precision >= 90 else 2 if precision >= 70 else 1,
            score=int(precision * 9), max_combo=int(precision / 8),
            duration_s=52, steps_total=8,
            steps_correct=int(8 * precision / 100),
            at=ahora - rng.random() * 6 * 86400)
        ctx.results.add(r)
    for code in ("primer_gesto", "tres_estrellas", "racha_3", "primera_cancion"):
        ctx.achievements.unlock(perfil.id, code)

    # Una melodía grabada de muestra, para que "Canciones" no salga vacío.
    from handsingkids.data import melodies
    melodies.save(perfil.name,
                  ["DO3", "MI3", "SOL3", "MI3", "DO3", "_", "RE3", "FA3"],
                  6.4, gaps_ms=[0, 520, 480, 610, 700, 900, 540, 560])
    return perfil


def main() -> int:
    from PySide6.QtWidgets import QApplication
    from PySide6.QtCore import QTimer

    if DATOS.exists():
        shutil.rmtree(DATOS)
    SALIDA.mkdir(parents=True, exist_ok=True)
    os.environ["HSK_DATA_DIR"] = str(DATOS)

    from handsingkids.core import config
    config.set_data_dir(DATOS)
    from handsingkids.data.database import Database, set_db
    set_db(Database(DATOS / "demo.sqlite3"))

    app = QApplication(sys.argv)
    from handsingkids.ui import theme as T
    app.setStyleSheet(T.global_stylesheet())

    from handsingkids.app import AppContext, MainWindow
    ctx = AppContext()
    perfil = preparar_datos(ctx)

    ventana = MainWindow(ctx)
    ventana.resize(1440, 900)
    ventana.show()
    app.processEvents()

    from handsingkids.domain.entities import ActivityResult
    from handsingkids.learning.session_flow import Outcome

    guion = [
        ("01_splash", "splash", {}),
        ("02_perfiles", "profiles", {}),
        ("03_crear_perfil", "create_profile", {}),
        ("04_inicio", "home", {}),
        ("05_aventura", "adventure", {}),
        ("06_calibracion", "calibration", {"primera_vez": False}),
        ("07_progreso", "progress", {}),
        ("08_padres", "parents", {}),
        ("09_ajustes", "settings", {}),
        ("10_modo_libre", "freeplay", {}),
        ("13_canciones", "songs", {}),
    ]

    fallos = []
    for nombre, pantalla, kwargs in guion:
        try:
            ventana.navigate(pantalla, kwargs)
            for _ in range(6):
                app.processEvents()
                time.sleep(0.02)
            ventana.grab().save(str(SALIDA / f"{nombre}.png"))
            print(f"  ok   {nombre}")
        except Exception as exc:
            fallos.append((nombre, exc))
            print(f"  FALLA {nombre}: {exc}")
            import traceback
            traceback.print_exc()

    # Ejercicio y resultados necesitan datos simulados.
    try:
        actividad = ctx.activities.get("n1_trio")
        ventana.navigate("exercise", {"activity": actividad, "cola": []})
        for _ in range(30):      # el ejercicio arranca con medio segundo de espera
            app.processEvents()
            time.sleep(0.03)
        pantalla = ventana._screens["exercise"]
        _simular_ejercicio(app, pantalla)
        ventana.grab().save(str(SALIDA / "11_ejercicio.png"))
        print("  ok   11_ejercicio")
    except Exception as exc:
        fallos.append(("11_ejercicio", exc))
        print(f"  FALLA 11_ejercicio: {exc}")
        import traceback
        traceback.print_exc()

    try:
        runner = ventana._screens["exercise"].runner
        if runner:
            outcome = _resultado_simulado(ctx, runner)
            ventana.navigate("results", {"outcome": outcome,
                                         "activity": actividad, "cola": []})
            for _ in range(6):
                app.processEvents()
                time.sleep(0.02)
            ventana.grab().save(str(SALIDA / "12_resultados.png"))
            print("  ok   12_resultados")
    except Exception as exc:
        fallos.append(("12_resultados", exc))
        print(f"  FALLA 12_resultados: {exc}")
        import traceback
        traceback.print_exc()

    try:
        cancion = ctx.activities.get("cancion_pollitos")
        ventana.navigate("rhythm", {"activity": cancion})
        for _ in range(20):
            app.processEvents()
            time.sleep(0.03)
        pantalla_ritmo = ventana._screens["rhythm"]
        _simular_ritmo(app, pantalla_ritmo)
        ventana.grab().save(str(SALIDA / "14_ritmo.png"))
        print("  ok   14_ritmo")
    except Exception as exc:
        fallos.append(("14_ritmo", exc))
        print(f"  FALLA 14_ritmo: {exc}")
        import traceback
        traceback.print_exc()

    ctx.shutdown()
    print(f"\nCapturas en {SALIDA}")
    if fallos:
        print(f"{len(fallos)} pantallas con error")
        return 1
    print("Todas las pantallas se construyeron sin errores.")
    return 0


def _simular_ejercicio(app, pantalla) -> None:
    """Pone la pantalla de ejercicio en un estado intermedio realista."""
    import json
    import numpy as np
    import time as _t

    raw = json.loads((ROOT / "tests" / "fixtures" /
                      "calibracion_v1.json").read_text())
    h, w = 360, 640
    yy, xx = np.mgrid[0:h, 0:w]
    frame = np.dstack([
        (206 + 26 * np.sin(xx / 70)).clip(0, 255),
        (194 + 20 * np.cos(yy / 60)).clip(0, 255),
        (176 + 16 * np.sin((xx + yy) / 90)).clip(0, 255)]).astype(np.uint8)
    manos = []
    for i, hd in enumerate(raw["MI3"]["hands"]):
        pts = np.asarray(hd["landmarks"], float).copy()
        pts[:, :2] = pts[:, :2] * 2.6 + np.array([0.33 + 0.32 * i, 0.55])
        manos.append({"landmarks": pts.tolist(), "hand_label": hd["hand_label"]})
    runner = pantalla.runner
    if runner and runner.running:
        runner.submit("DO3", 0.94)
        for _ in range(8):
            app.processEvents()
            _t.sleep(0.06)
    pantalla.camara.set_frame(np.ascontiguousarray(frame), manos, False)
    pantalla.mensaje.setText("¡Excelente!")
    pantalla._on_score(170, 4)
    for _ in range(4):
        app.processEvents()
        _t.sleep(0.02)


def _simular_ritmo(app, pantalla) -> None:
    """Deja que la pista de nota viajera avance un poco y confirma la primera
    nota, para que la captura muestre burbujas en movimiento y una acertada."""
    import time as _t

    runner = pantalla.runner
    if runner and runner.running:
        limite = _t.time() + 3.0
        while runner.running and runner.elapsed_ms < 1200 and _t.time() < limite:
            app.processEvents()
            _t.sleep(0.03)
        if runner.running and runner.sequence:
            runner.submit(runner.sequence[0], 0.92)
        for _ in range(6):
            app.processEvents()
            _t.sleep(0.02)


def _resultado_simulado(ctx, runner):
    from handsingkids.learning.session_flow import Outcome
    resultado = runner.build_result()
    resultado.accuracy = 83.0
    resultado.stars = 2
    resultado.score = 640
    resultado.max_combo = 7
    resultado.steps_total = 4
    resultado.steps_correct = 3
    resultado.rhythm = 78.0
    return Outcome(result=resultado, mastered=["nota_RE3"],
                   unlocked_skills=[], achievements=["tres_estrellas"],
                   stars_awarded=2, coins_awarded=20)


if __name__ == "__main__":
    raise SystemExit(main())
