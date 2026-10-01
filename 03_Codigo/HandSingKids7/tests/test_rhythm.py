"""Pruebas del motor de nota viajera (`learning.rhythm.RhythmRunner`), el que
usa el nuevo módulo "Canciones".

Comprueba tres cosas que son justo las que cambiaron respecto al ejercicio
guiado de siempre: que hay una ventana de acierto alrededor de la línea de
impacto (no un instante exacto ni una espera indefinida), que una nota
fallada no detiene el juego, y que el resultado es compatible con
`session_flow.apply_result()` — es decir, que una canción del catálogo jugada
así alimenta el dominio por nota exactamente igual que un ejercicio guiado.
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

DATOS = Path("/tmp/hsk_test_rhythm")

fallos: list[str] = []


def comprobar(condicion: bool, mensaje: str) -> None:
    if condicion:
        print(f"  ok   {mensaje}")
    else:
        fallos.append(mensaje)
        print(f"  FALLA {mensaje}")


def test_ventana_y_planificacion() -> None:
    """Sin tocar la cámara ni la base de datos: solo la aritmética de cuándo
    llega cada nota y qué tan ancha es su ventana de acierto."""
    print("\n1. Planificación de tiempos (sin Qt real, solo el reloj interno)")
    from handsingkids.domain.entities import Activity, ActivityKind, PlayMode
    from handsingkids.learning.rhythm import (GAP_MAX_MS, GAP_MIN_MS,
                                              MIN_WINDOW_MS, TRAVEL_MS,
                                              RhythmRunner)

    actividad = Activity(
        code="prueba_ritmo", kind=ActivityKind.SONG, title="Prueba", level=1,
        difficulty=0.3, skill_codes=[], sequence=["DO3", "RE3", "MI3", "FA3"],
        mode=PlayMode.MELODY, tempo_bpm=90, tolerance_ms=2500)
    r = RhythmRunner(actividad, profile_id=1)
    gap_tempo = 60_000.0 / 90
    comprobar(r.notes[0].arrival_ms == TRAVEL_MS,
              "la primera nota llega justo tras el tiempo de vuelo inicial")
    for i in range(1, 4):
        delta = r.notes[i].arrival_ms - r.notes[i - 1].arrival_ms
        comprobar(abs(delta - gap_tempo) < 0.01,
                  f"nota {i}: el intervalo es el del tempo constante ({delta:.1f} ms)")
    comprobar(all(n.window_before_ms >= MIN_WINDOW_MS / 2 * 0.99 for n in r.notes),
              "ninguna ventana de acierto queda por debajo del mínimo")

    # "A mi ritmo": intervalos reales grabados, con recorte a los límites.
    actividad2 = Activity(
        code="prueba_grabada", kind=ActivityKind.GAME, title="Grabada", level=0,
        difficulty=0.3, skill_codes=[], sequence=["DO3", "RE3", "MI3"],
        mode=PlayMode.MELODY, tempo_bpm=84, tolerance_ms=2200)
    gaps = [0, 50, 9000]     # el primero se ignora, el segundo y tercero se recortan
    r2 = RhythmRunner(actividad2, profile_id=1, gaps_ms=gaps)
    d1 = r2.notes[1].arrival_ms - r2.notes[0].arrival_ms
    d2 = r2.notes[2].arrival_ms - r2.notes[1].arrival_ms
    comprobar(abs(d1 - GAP_MIN_MS) < 0.01,
              f"un intervalo grabado demasiado corto se recorta al mínimo ({d1:.0f} ms)")
    comprobar(abs(d2 - GAP_MAX_MS) < 0.01,
              f"un intervalo grabado demasiado largo se recorta al máximo ({d2:.0f} ms)")


def test_factor_de_tempo_afloja_la_velocidad_y_la_ventana() -> None:
    """Petición explícita del usuario: poder elegir el tiempo porque las
    canciones "están muy rápido". `tempo_factor` (elegido en la pantalla
    Canciones como 🐢/Normal/🐇) debe alargar proporcionalmente el intervalo
    entre notas y, con él, ensanchar su ventana de acierto — no basta con que
    la canción se vea más lenta si seguir siendo igual de exigente."""
    print("\n1b. El factor de tempo afloja velocidad y ventana")
    from handsingkids.domain.entities import Activity, ActivityKind, PlayMode
    from handsingkids.learning.rhythm import TEMPO_FACTORS, RhythmRunner

    actividad = Activity(
        code="prueba_tempo", kind=ActivityKind.SONG, title="Prueba", level=1,
        difficulty=0.3, skill_codes=[], sequence=["DO3", "RE3", "MI3"],
        mode=PlayMode.MELODY, tempo_bpm=100, tolerance_ms=2500)

    normal = RhythmRunner(actividad, profile_id=1, tempo_factor=TEMPO_FACTORS["normal"])
    lento = RhythmRunner(actividad, profile_id=1, tempo_factor=TEMPO_FACTORS["lento"])
    rapido = RhythmRunner(actividad, profile_id=1, tempo_factor=TEMPO_FACTORS["rapido"])

    gap_normal = normal.notes[1].arrival_ms - normal.notes[0].arrival_ms
    gap_lento = lento.notes[1].arrival_ms - lento.notes[0].arrival_ms
    gap_rapido = rapido.notes[1].arrival_ms - rapido.notes[0].arrival_ms
    comprobar(gap_lento > gap_normal > gap_rapido,
              f"«lento» separa más las notas y «rápido» las junta más "
              f"({gap_lento:.0f} > {gap_normal:.0f} > {gap_rapido:.0f} ms)")

    ventana_normal = normal.notes[1].window_before_ms + normal.notes[1].window_after_ms
    ventana_lento = lento.notes[1].window_before_ms + lento.notes[1].window_after_ms
    comprobar(ventana_lento > ventana_normal,
              f"«lento» también ensancha la ventana de acierto "
              f"({ventana_lento:.0f} > {ventana_normal:.0f} ms)")


def test_formula_de_combo_calca_notas_ritmicas() -> None:
    """La fórmula del multiplicador de combo se calca de "Notas Rítmicas"
    (`ScoreManager.hit()` en la v0, la primera versión en Pygame): cada 10 de
    racha suma +0,5 al multiplicador, con techo en 4,0 — no cada 5 con +0,25
    y techo 3,0, que era el valor provisional de esta reconstrucción."""
    print("\n1c. La fórmula de combo calca la de Notas Rítmicas")
    from handsingkids.domain.entities import Activity, ActivityKind, PlayMode
    from handsingkids.learning.rhythm import RhythmRunner, TIER_POINTS

    secuencia = ["DO3"] * 25
    actividad = Activity(
        code="prueba_combo", kind=ActivityKind.SONG, title="Prueba", level=1,
        difficulty=0.3, skill_codes=[], sequence=secuencia,
        mode=PlayMode.MELODY, tempo_bpm=90, tolerance_ms=2500)
    r = RhythmRunner(actividad, profile_id=1)
    r._running = True   # se maneja el reloj a mano, sin arrancar el QTimer

    esperado = 0
    for i, n in enumerate(r.notes):
        r._elapsed_ms = n.arrival_ms   # justo en el cruce: siempre "perfecto"
        acierto = r.submit(n.code, 0.95)
        combo_tras_acierto = i + 1
        multiplicador = min(1.0 + (combo_tras_acierto // 10) * 0.5, 4.0)
        esperado += int(TIER_POINTS["perfecto"] * multiplicador)
        if not acierto:
            break

    comprobar(r.score == esperado,
              f"el puntaje acumulado coincide con la fórmula de v0 "
              f"({r.score} == {esperado})")
    comprobar(r.combo == 25 and r.max_combo == 25,
              "25 aciertos seguidos mantienen la racha completa")


def test_ciclo_completo() -> None:
    """Con Qt real (QTimer con reloj de pared) y una canción del catálogo:
    aciertos dentro de la ventana, un fallo que no detiene el juego, y un
    resultado que `apply_result` puede consumir sin cambios."""
    print("\n2. Una canción completa, con aciertos y una nota fallada a propósito")
    from PySide6.QtWidgets import QApplication

    if DATOS.exists():
        shutil.rmtree(DATOS)
    app = QApplication.instance() or QApplication([])

    from handsingkids.core import config
    config.set_data_dir(DATOS)
    from handsingkids.data.database import Database, set_db
    set_db(Database(DATOS / "rhythm.sqlite3"))

    from handsingkids.app import AppContext
    ctx = AppContext()
    perfil = ctx.profiles.create("Prueba", 8, "iguana")
    ctx.select_profile(perfil)

    from handsingkids.learning.rhythm import RhythmRunner
    from handsingkids.learning.session_flow import apply_result

    actividad = ctx.activities.get("cancion_estrellita")
    comprobar(actividad is not None, "la canción de prueba existe en el catálogo")
    if actividad is None:
        return

    runner = RhythmRunner(actividad, perfil.id, bus=ctx.bus)
    terminado: list = []
    runner.finished.connect(lambda r: terminado.append(r))
    runner.start()

    secuencia = runner.sequence
    fallada_a_proposito = 1     # el segundo paso nunca se confirma, a propósito
    limite = time.time() + 40.0
    while not terminado and time.time() < limite:
        app.processEvents()
        for n in runner.notes:
            if n.judged.value != "pendiente" or n.index == fallada_a_proposito:
                continue
            # Confirma la seña un poco antes de que la nota cruce la línea,
            # como haría un niño que ya está sosteniendo la seña.
            offset = runner.elapsed_ms - n.arrival_ms
            if -n.window_before_ms * 0.6 <= offset <= 0:
                runner.submit(n.code, 0.9)
                break
        time.sleep(0.01)

    # Si el juego se hubiera quedado esperando la nota que nunca se tocó (como
    # haría el ejercicio guiado con su espera indefinida), esta comprobación
    # fallaría por tiempo agotado: es la prueba de que "sigue sin parar".
    comprobar(bool(terminado),
              "la canción terminó sola pese a la nota que nunca se confirmó, "
              "sin quedarse esperándola")
    if not terminado:
        runner.finish()
        terminado.append(runner.build_result())
    resultado = terminado[0]

    comprobar(resultado.steps_total == len(secuencia),
              f"se contaron todos los pasos, incluida la nota fallada "
              f"({resultado.steps_total})")
    comprobar(resultado.steps_correct == len(secuencia) - 1,
              f"se acertó todo menos la nota fallada a propósito "
              f"({resultado.steps_correct}/{resultado.steps_total})")
    comprobar(any(a.correct is False and a.step_index == fallada_a_proposito
                 for a in runner.attempts),
              "la nota que no se tocó quedó registrada como fallada, no ignorada")

    outcome = apply_result(ctx, runner)
    estados = ctx.skill_states.for_profile(perfil.id)
    notas_tocadas = {c for c in secuencia}
    comprobar(all(estados[f"nota_{n}"].attempts > 0 for n in notas_tocadas),
              "apply_result actualizó el dominio de cada nota de la canción, "
              "igual que con un ejercicio guiado")
    comprobar(ctx.attempts.total(perfil.id) == resultado.steps_total,
              "los intentos de la canción quedaron guardados en la base de datos")

    ctx.shutdown()


def test_solo_suena_la_nota_correcta() -> None:
    """Dos reglas de Canciones, calcadas de "Notas Rítmicas" (la mecánica
    original de la v0): una seña equivocada (o hecha fuera de la ventana de
    cualquier nota) no debe sonar — solo la nota que en ese momento se está
    pidiendo —, y esa seña equivocada tampoco falla la nota: el niño puede
    seguir intentando hasta acertarla o hasta que termine de cruzar su
    ventana. `RhythmScreen._on_confirmed` decide el sonido según lo que
    devuelve `RhythmRunner.submit()`, así que se prueba tal cual se conecta
    ahí, no solo el motor por separado."""
    print("\n3. Solo suena la nota correcta dentro de Canciones")
    from PySide6.QtWidgets import QApplication
    app = QApplication.instance() or QApplication([])

    datos = Path("/tmp/hsk_test_rhythm_sonido")
    if datos.exists():
        shutil.rmtree(datos)
    from handsingkids.core import config
    config.set_data_dir(datos)
    from handsingkids.data.database import Database, set_db
    set_db(Database(datos / "rhythm_sonido.sqlite3"))

    from handsingkids.app import AppContext
    from handsingkids.ui.screens.rhythm import RhythmScreen

    ctx = AppContext()
    perfil = ctx.profiles.create("Prueba2", 8, "iguana")
    ctx.select_profile(perfil)

    sonados: list[str] = []
    ctx.music.trigger = lambda nota, confianza=1.0: sonados.append(nota)

    pantalla = RhythmScreen(ctx)
    actividad = ctx.activities.get("cancion_estrellita")
    comprobar(actividad is not None, "la canción de prueba existe en el catálogo")
    if actividad is None:
        return
    pantalla.on_enter(activity=actividad)
    # `on_enter` arranca el motor con un QTimer.singleShot(500, ...), así que
    # hay que dejar correr el bucle de eventos hasta que de verdad empiece.
    limite = time.time() + 3.0
    while not (pantalla.runner and pantalla.runner.running) and time.time() < limite:
        app.processEvents()
        time.sleep(0.01)
    comprobar(bool(pantalla.runner and pantalla.runner.running),
              "la partida arrancó de verdad antes de seguir la prueba")

    primera, segunda = pantalla.runner.notes[0], pantalla.runner.notes[1]

    # La primera nota todavía no está "en juego" (arranca en TRAVEL_MS): una
    # seña hecha ahora mismo, aunque fuera a coincidir con ella, no debe
    # sonar — no hay ninguna nota activa a la que atribuírsela.
    pantalla._on_confirmed({"note": primera.code, "confidence": 0.9})
    comprobar(sonados == [],
              "una seña hecha antes de que cualquier nota entre a la ventana "
              "de acierto tampoco suena")

    def _esperar_ventana(nota) -> None:
        limite = time.time() + 5.0
        objetivo = nota.arrival_ms - nota.window_before_ms + 20
        while pantalla.runner.elapsed_ms < objetivo and time.time() < limite:
            app.processEvents()
            time.sleep(0.01)
        comprobar(pantalla.runner.elapsed_ms >= objetivo,
                  f"la nota {nota.index} llegó a su ventana de acierto")

    # Una seña equivocada dentro de la ventana de la primera nota no suena
    # nada — y, calcando la mecánica original de "Notas Rítmicas" (v0), no
    # la falla tampoco: la nota sigue pendiente y el niño puede reintentarla
    # mientras siga dentro de su ventana de acierto.
    _esperar_ventana(primera)
    from handsingkids.learning.rhythm import NoteJudgement
    otra_nota = next(c for c in ("DO3", "RE3", "MI3", "FA3", "SOL3", "LA3",
                                 "SI3", "DO4") if c != primera.code)
    pantalla._on_confirmed({"note": otra_nota, "confidence": 0.9})
    comprobar(sonados == [],
              f"una seña que no es la pedida no suena nada (pedía "
              f"{primera.code}, se hizo {otra_nota})")
    comprobar(primera.judged == NoteJudgement.PENDING,
              "la seña equivocada no falla la nota: sigue pendiente para "
              "un próximo intento, como en 'Notas Rítmicas'")

    # Un segundo intento, ya con la seña correcta y todavía dentro de la
    # misma ventana, sí debe contar y sonar.
    pantalla._on_confirmed({"note": primera.code, "confidence": 0.9})
    comprobar(sonados == [primera.code],
              f"un reintento con la seña correcta sí suena ({sonados})")
    comprobar(primera.judged == NoteJudgement.HIT,
              "el reintento correcto sí resuelve la nota como acierto")

    # La segunda nota, acertada al primer intento: también debe sonar.
    _esperar_ventana(segunda)
    pantalla._on_confirmed({"note": segunda.code, "confidence": 0.9})
    comprobar(sonados == [primera.code, segunda.code],
              f"la seña correcta sí suena ({sonados})")

    pantalla.on_leave()
    ctx.shutdown()


def main() -> int:
    test_ventana_y_planificacion()
    test_factor_de_tempo_afloja_la_velocidad_y_la_ventana()
    test_formula_de_combo_calca_notas_ritmicas()
    test_ciclo_completo()
    test_solo_suena_la_nota_correcta()
    print()
    if fallos:
        print(f"{len(fallos)} comprobaciones fallaron:")
        for f in fallos:
            print("  ·", f)
        return 1
    print("El motor de nota viajera funciona como se esperaba.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
