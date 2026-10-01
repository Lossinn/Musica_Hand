"""Lo que ocurre cuando termina una actividad.

Guardar intentos, recalcular el dominio, repartir estrellas, abrir habilidades y
comprobar logros son cosas del dominio, no de la pantalla. Se agrupan aquí para
poder probarlas sin abrir una ventana.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field

from ..domain.entities import (ActivityResult, SkillState, SkillStatus)
from ..learning import mastery as M
from ..learning.evaluation import ActivityRunner
from ..learning.progression import unlock_skills


@dataclass
class Outcome:
    result: ActivityResult
    mastered: list[str] = field(default_factory=list)
    unlocked_skills: list[str] = field(default_factory=list)
    achievements: list[str] = field(default_factory=list)
    stars_awarded: int = 0
    coins_awarded: int = 0
    mastery_changes: dict[str, float] = field(default_factory=dict)


def apply_result(ctx, runner: ActivityRunner, *, now: float | None = None) -> Outcome:
    """Registra el resultado de una actividad y actualiza todo lo que dependa
    de él. `ctx` es el contexto de la aplicación."""
    now = now if now is not None else time.time()
    profile = ctx.profile
    result = runner.build_result()
    result.session_id = ctx.session.id if ctx.session else None
    result.profile_id = profile.id

    # El récord anterior se consulta antes de insertar este resultado; si no,
    # el propio resultado cuenta como récord previo y nunca se otorgan estrellas.
    mejor_previo = ctx.results.best_stars(profile.id, runner.activity.code)

    # 1. Intentos y resultado.
    for a in runner.attempts:
        a.profile_id = profile.id
        a.session_id = result.session_id
        ctx.attempts.add(a)
    ctx.results.add(result)

    outcome = Outcome(result=result)

    # 2. Dominio, nota por nota.
    estados = ctx.skill_states.for_profile(profile.id)
    resumen = runner.per_note_summary()
    calidad = result.accuracy / 100.0
    for note, (aciertos, intentos, reaccion, secuencia) in resumen.items():
        code = f"nota_{note}"
        st = estados.get(code) or SkillState(profile.id, code)
        if st.status == SkillStatus.LOCKED:
            st.status = SkillStatus.INTRODUCED
        antes = st.mastery
        recientes = _recent_outcomes(ctx, profile.id, note, secuencia)
        M.update_skill(st, recent=recientes, new_hits=aciertos,
                       new_attempts=intentos, reaction_ms=reaccion,
                       age_band=profile.age_band, quality=calidad, now=now)
        ctx.skill_states.save(st)
        estados[code] = st
        outcome.mastery_changes[code] = round(st.mastery - antes, 4)
        if st.status in (SkillStatus.MASTERED, SkillStatus.CONSOLIDATED) \
                and antes < M.MASTERED_AT <= st.mastery:
            outcome.mastered.append(code)

    # 3. Habilidades compuestas de la actividad (secuencias, ritmo, melodía).
    for code in runner.activity.skill_codes:
        if code.startswith("nota_"):
            continue
        st = estados.get(code) or SkillState(profile.id, code)
        if st.status == SkillStatus.LOCKED:
            st.status = SkillStatus.INTRODUCED
        antes = st.mastery
        M.update_skill(st, recent=[a.correct for a in runner.attempts][-8:],
                       new_hits=runner.steps_correct,
                       new_attempts=runner.total_steps,
                       reaction_ms=_mean_reaction(runner),
                       age_band=profile.age_band, quality=calidad, now=now)
        ctx.skill_states.save(st)
        estados[code] = st
        outcome.mastery_changes[code] = round(st.mastery - antes, 4)

    # 4. Apertura de habilidades nuevas.
    catalogo = {s.code: s for s in ctx.skills.all()}
    abiertas = unlock_skills(catalogo, estados)
    for code in abiertas:
        ctx.skill_states.save(estados[code])
    outcome.unlocked_skills = abiertas

    # 5. Estrellas y monedas. Solo se suman las que mejoran el récord de esa
    # actividad, para que repetirla no infle el contador sin límite.
    nuevas = max(0, result.stars - mejor_previo)
    monedas = result.stars * 5 + (10 if result.accuracy >= 90 else 0)
    ctx.profiles.add_stars(profile, nuevas, monedas)
    outcome.stars_awarded = nuevas
    outcome.coins_awarded = monedas

    # 6. Logros.
    outcome.achievements = _check_achievements(ctx, runner, result, outcome)

    # 7. Memoria de la sesión, que alimenta al motor adaptativo.
    ctx.session_results.append(result)
    if result.accuracy < 55:
        ctx.consecutive_failures += 1
    else:
        ctx.consecutive_failures = 0

    # 8. Reentrenar el Agente Adaptativo cuando ya se acumularon intentos
    # nuevos suficientes. Se repite cada RETRAIN_EVERY intentos, no solo una
    # vez: así el agente sigue cambiando con el progreso del niño en lugar de
    # quedarse fijo tras el primer ajuste.
    _maybe_retrain(ctx, profile.id)

    return outcome


def _maybe_retrain(ctx, profile_id: int) -> None:
    from ..intelligence.predictor import MIN_SAMPLES, RETRAIN_EVERY

    total = ctx.attempts.total(profile_id)
    if total < MIN_SAMPLES or (total - ctx.predictor.n_samples) < RETRAIN_EVERY:
        return
    filas = ctx.attempts.training_rows(profile_id)
    if ctx.predictor.fit(filas) is not None:
        ctx.save_predictor()


def _mean_reaction(runner: ActivityRunner) -> float:
    tiempos = [a.reaction_ms for a in runner.attempts if a.correct]
    return sum(tiempos) / len(tiempos) if tiempos else 0.0


def _recent_outcomes(ctx, profile_id: int, note: str,
                     nuevos: list[bool]) -> list[bool]:
    """Últimos resultados de esa nota: los guardados más los de ahora."""
    filas = ctx.attempts.recent_for_note(profile_id, note, limit=8)
    previos = [bool(r["correct"]) for r in reversed(filas)]
    return (previos + nuevos)[-8:]


def _check_achievements(ctx, runner, result, outcome) -> list[str]:
    """Comprueba los logros que dependen de esta actividad."""
    from ..domain.entities import ActivityKind
    from ..domain.notes import NOTE_CODES

    profile = ctx.profile
    ganados: list[str] = []

    def otorgar(code: str) -> None:
        if ctx.achievements.unlock(profile.id, code):
            ganados.append(code)

    if ctx.attempts.total(profile.id) >= 1:
        otorgar("primer_gesto")
    if ctx.attempts.total(profile.id) >= 100:
        otorgar("cien_intentos")
    if runner.activity.kind == ActivityKind.SONG and result.accuracy >= 60:
        otorgar("primera_cancion")
    if result.stars >= 3:
        otorgar("tres_estrellas")
    if result.max_combo >= 10:
        otorgar("combo_10")
    if profile.streak_days >= 3:
        otorgar("racha_3")
    if profile.streak_days >= 7:
        otorgar("racha_7")
    if (len(runner.activity.sequence) == len(NOTE_CODES)
            and list(runner.activity.sequence) == list(NOTE_CODES)
            and result.accuracy >= 90):
        otorgar("octava_completa")
    for code in outcome.mastered:
        nota = code.replace("nota_", "")
        if nota in NOTE_CODES:
            otorgar(f"domina_{nota}")
    return ganados
