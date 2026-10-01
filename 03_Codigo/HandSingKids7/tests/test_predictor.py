"""Pruebas de `intelligence.predictor.MasteryPredictor` y de
`learning.generator.generate_candidates`.

Esto no se probó por separado cuando se implementó `fit()` de verdad (sección
11.2 del documento técnico): quedó verificado solo por lectura de código e,
indirectamente, por `test_optimizer.py` y `test_integracion.py`. Esta prueba
cierra ese hueco con datos claramente sintéticos y señalados como tales —
nunca se usan para sembrar el perfil de un niño real, solo para comprobar que
el descenso de gradiente converge a algo sensato y que `probability()` se
comporta de forma monótona con sus propias variables.
"""

from __future__ import annotations

import os
import random
import sys
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

fallos: list[str] = []


def comprobar(condicion: bool, mensaje: str) -> None:
    if condicion:
        print(f"  ok   {mensaje}")
    else:
        fallos.append(mensaje)
        print(f"  FALLA {mensaje}")


def _filas_sinteticas_de_prueba(n: int, rng: random.Random) -> list[dict]:
    """Filas fabricadas solo para esta prueba numérica: una regla simple y
    conocida (más precisión y menos dificultad ⇒ más probable el acierto),
    con algo de ruido, para comprobar que `fit()` la recupera aproximadamente.
    Nunca se usan dentro de la aplicación ni sustituyen datos reales de un
    niño — `fit()` en producción solo se llama con `AttemptRepository.
    training_rows()`, que lee la tabla `attempts` real."""
    filas = []
    for _ in range(n):
        precision = rng.random()
        dificultad = rng.random()
        dias = rng.uniform(0, 10)
        z = 4.0 * precision - 3.0 * dificultad - 0.15 * dias - 0.3
        p = 1.0 / (1.0 + pow(2.718281828, -z))
        correcto = rng.random() < p
        filas.append({"correct": correcto, "precision_nota": precision,
                      "dificultad": dificultad, "dias_desde_ultima": dias})
    return filas


def test_arranque_en_frio() -> None:
    print("\n1. Sin entrenar: usa la fórmula fija")
    from handsingkids.domain.entities import Activity, ActivityKind, PlayMode, SkillState
    from handsingkids.intelligence.predictor import MasteryPredictor

    pred = MasteryPredictor()
    comprobar(not pred.trained, "el predictor nuevo empieza sin entrenar")
    estado = SkillState(profile_id=1, skill_code="nota_DO3", mastery=0.6)
    actividad = Activity(code="a", kind=ActivityKind.EXERCISE, title="t",
                         level=1, difficulty=0.4, skill_codes=["nota_DO3"],
                         sequence=["DO3"], mode=PlayMode.GUIDED)
    pred_baja = pred.probability(actividad, {"nota_DO3": estado})
    comprobar(pred_baja.method == "logistica_parametrica",
              "sin entrenar, el método reportado es la fórmula fija")
    comprobar(0.0 <= pred_baja.probability <= 1.0,
              f"la probabilidad está en rango ({pred_baja.probability:.3f})")

    actividad_dificil = Activity(code="b", kind=ActivityKind.EXERCISE, title="t",
                                 level=1, difficulty=0.95, skill_codes=["nota_DO3"],
                                 sequence=["DO3"], mode=PlayMode.GUIDED)
    pred_alta_dif = pred.probability(actividad_dificil, {"nota_DO3": estado})
    comprobar(pred_alta_dif.probability < pred_baja.probability,
              "una actividad más difícil que el dominio actual predice menos éxito")


def test_fit_pocos_datos_no_activa_el_modelo() -> None:
    print("\n2. Con menos de MIN_SAMPLES intentos, fit() no hace nada")
    from handsingkids.intelligence.predictor import MIN_SAMPLES, MasteryPredictor

    rng = random.Random(1)
    pred = MasteryPredictor()
    reporte = pred.fit(_filas_sinteticas_de_prueba(MIN_SAMPLES - 1, rng))
    comprobar(reporte is None, "fit() devuelve None si no alcanzan los intentos")
    comprobar(not pred.trained, "el predictor sigue sin entrenar")


def test_fit_converge_y_es_monotono() -> None:
    print("\n3. Con datos suficientes, fit() ajusta un modelo que responde a "
         "sus propias variables")
    from handsingkids.domain.entities import SkillState
    from handsingkids.intelligence.predictor import MasteryPredictor

    rng = random.Random(7)
    filas = _filas_sinteticas_de_prueba(400, rng)
    pred = MasteryPredictor()
    reporte = pred.fit(filas)
    comprobar(reporte is not None, "fit() entrena con suficientes intentos")
    if reporte is None:
        return
    comprobar(pred.trained, "el predictor queda marcado como entrenado")
    comprobar(reporte.samples == 400, f"reporta el número de muestras usadas ({reporte.samples})")
    comprobar(reporte.accuracy > 0.60,
              f"el ajuste hace mejor que el azar sobre sus propios datos "
              f"({reporte.accuracy*100:.0f}%)")

    ahora = 1_000_000.0
    baja = SkillState(profile_id=1, skill_code="nota_DO3", precision=0.1,
                      last_practice_at=ahora)
    alta = SkillState(profile_id=1, skill_code="nota_DO3", precision=0.9,
                      last_practice_at=ahora)
    p_baja = pred._note_probability(baja, 0.5, ahora)
    p_alta = pred._note_probability(alta, 0.5, ahora)
    comprobar(p_alta > p_baja,
              f"más precisión en la nota predice más éxito ({p_baja:.3f} → {p_alta:.3f})")

    facil = pred._note_probability(alta, 0.1, ahora)
    dificil = pred._note_probability(alta, 0.95, ahora)
    comprobar(facil > dificil,
              f"más dificultad predice menos éxito ({facil:.3f} → {dificil:.3f})")

    # Persistencia: guardar y recargar debe conservar el modelo entrenado.
    clon = MasteryPredictor.from_json(pred.to_json())
    comprobar(clon.trained and clon.weights == pred.weights,
              "to_json()/from_json() conserva el modelo entrenado")


def test_generador_procedural() -> None:
    print("\n4. El generador procedural produce actividades válidas")
    from handsingkids.domain.entities import SkillState, SkillStatus
    from handsingkids.intelligence.predictor import MasteryPredictor
    from handsingkids.learning.generator import generate_candidates

    pred = MasteryPredictor()
    estados = {
        f"nota_{c}": SkillState(profile_id=1, skill_code=f"nota_{c}",
                                status=SkillStatus.PRACTICING, mastery=m,
                                precision=m, attempts=12, hits=int(12 * m))
        for c, m in (("DO3", 0.85), ("RE3", 0.40), ("MI3", 0.55))
    }
    candidatas = generate_candidates(level=1, states=estados, predictor=pred,
                                     n=4, seed=3)
    comprobar(len(candidatas) > 0, f"se generaron actividades ({len(candidatas)})")
    for a in candidatas:
        comprobar(a.code.startswith("proc_"), f"código con el prefijo esperado ({a.code})")
        comprobar(bool(a.sequence), "la secuencia generada no está vacía")
        comprobar(all(c in estados for c in a.skill_codes),
                  "todas las habilidades de la actividad existen en los estados dados")

    vacias = generate_candidates(level=1, states={}, predictor=pred, n=4)
    comprobar(vacias == [],
              "sin al menos dos notas abiertas, no se genera nada")


def main() -> int:
    test_arranque_en_frio()
    test_fit_pocos_datos_no_activa_el_modelo()
    test_fit_converge_y_es_monotono()
    test_generador_procedural()
    print()
    if fallos:
        print(f"{len(fallos)} comprobaciones fallaron:")
        for f in fallos:
            print("  ·", f)
        return 1
    print("El predictor entrenable y el generador procedural funcionan como se esperaba.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
