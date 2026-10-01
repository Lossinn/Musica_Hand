"""Pruebas del cálculo de dominio y del repaso espaciado."""
from __future__ import annotations

import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from handsingkids.domain.entities import SkillState, SkillStatus  # noqa: E402
from handsingkids.learning import mastery as M  # noqa: E402

DIA = 86400.0


def test_precision_no_salta_a_uno() -> None:
    assert M.precision(2, 2) < 0.7, "dos aciertos no pueden valer dominio pleno"
    assert M.precision(30, 30) > 0.9
    assert M.precision(0, 0) == 0.25


def test_consistencia_penaliza_alternar() -> None:
    assert M.consistency([True] * 8) == 1.0
    assert M.consistency([False] * 8) == 0.0
    alterna = M.consistency([True, False] * 4)
    estable = M.consistency([False, False, True, True, True, True, True, True])
    assert alterna < 0.1, alterna
    assert estable > alterna


def test_velocidad_depende_de_la_edad() -> None:
    t = 3500.0
    assert M.speed(t, "pequeños") > M.speed(t, "grandes")
    assert M.speed(700.0, "medianos") == 1.0
    assert M.speed(9000.0, "medianos") == 0.0


def test_retencion_decae_con_el_tiempo() -> None:
    now = time.time()
    ayer = M.retention(now - DIA, 2.3, 0.8, now=now)
    semana = M.retention(now - 7 * DIA, 2.3, 0.8, now=now)
    assert 0.80 < ayer <= 1.0, ayer
    assert semana < 0.35, semana
    # A mayor dominio previo, olvido más lento.
    assert (M.retention(now - 3 * DIA, 2.3, 0.9, now=now)
            > M.retention(now - 3 * DIA, 2.3, 0.2, now=now))


def test_una_sesion_perfecta_no_basta_para_dominar() -> None:
    st = SkillState(profile_id=1, skill_code="nota_DO3",
                    status=SkillStatus.INTRODUCED)
    M.update_skill(st, recent=[True] * 4, new_hits=4, new_attempts=4,
                   reaction_ms=1800, age_band="medianos", quality=1.0)
    assert st.status == SkillStatus.PRACTICING, st.status
    assert st.mastery < M.MASTERED_AT, st.mastery


def test_la_practica_sostenida_lleva_al_dominio() -> None:
    st = SkillState(profile_id=1, skill_code="nota_DO3",
                    status=SkillStatus.INTRODUCED)
    now = time.time()
    for i in range(6):
        M.update_skill(st, recent=[True] * 8, new_hits=4, new_attempts=4,
                       reaction_ms=1500, age_band="medianos", quality=1.0,
                       now=now + i * 60)
    assert st.status in (SkillStatus.MASTERED, SkillStatus.CONSOLIDATED), st.status
    assert st.mastery >= M.MASTERED_AT, st.mastery


def test_el_intervalo_de_repaso_crece_y_se_reinicia() -> None:
    st = SkillState(profile_id=1, skill_code="nota_MI3")
    now = time.time()
    intervalos = []
    for i in range(4):
        M.schedule_review(st, 0.95, now=now + i * DIA)
        intervalos.append(st.interval_days)
    assert intervalos == sorted(intervalos), intervalos
    assert intervalos[-1] > intervalos[0]
    M.schedule_review(st, 0.3, now=now + 5 * DIA)
    assert st.interval_days == 1.0, "un mal repaso vuelve a empezar"


def test_el_olvido_puede_degradar_una_habilidad() -> None:
    st = SkillState(profile_id=1, skill_code="nota_FA3",
                    status=SkillStatus.MASTERED, precision=0.95,
                    consistency=0.95, speed=0.9, retention=1.0, mastery=0.94,
                    attempts=40, hits=38, ease=2.0)
    st.last_practice_at = time.time() - 30 * DIA
    M.decay(st)
    assert st.mastery < M.DEMOTE_AT, st.mastery
    assert M.next_status(st, SkillStatus.MASTERED) == SkillStatus.PRACTICING


if __name__ == "__main__":
    import traceback
    fallos = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn(); print(f"  ok   {name}")
            except AssertionError:
                fallos += 1; print(f"  FALLA {name}"); traceback.print_exc()
    print("\nTodas las pruebas pasaron." if not fallos else f"\n{fallos} fallos.")
