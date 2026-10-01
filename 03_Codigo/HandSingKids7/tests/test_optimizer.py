"""Pruebas del optimizador de sesiones.

Lo importante aquí no es que devuelva una lista, sino que respete las
restricciones de la formulación y que la enumeración exhaustiva coincida con el
solucionador MILP, porque es el respaldo cuando CBC no está disponible.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from handsingkids.core import config  # noqa: E402

config.set_data_dir("/tmp/hsk_test_opt")

from handsingkids.data.database import Database, set_db  # noqa: E402

_db = Database("/tmp/hsk_test_opt/pruebas.sqlite3")
set_db(_db)

from handsingkids.data.repositories import ActivityRepository  # noqa: E402
from handsingkids.data.seed import build_skills, seed  # noqa: E402
from handsingkids.domain.entities import (ActivityKind, SkillState,  # noqa: E402
                                          SkillStatus)
from handsingkids.intelligence.optimizer import (DIFFICULTY_CAP,  # noqa: E402
                                                 SessionOptimizer)

seed(_db)


def _estados(dominio_por_defecto: float = 0.7, ajustes: dict | None = None):
    estados = {}
    for s in build_skills():
        estados[s.code] = SkillState(
            1, s.code, status=SkillStatus.PRACTICING,
            mastery=dominio_por_defecto, precision=dominio_por_defecto,
            consistency=dominio_por_defecto, speed=0.6, retention=1.0,
            attempts=12, hits=int(12 * dominio_por_defecto))
    for code, valor in (ajustes or {}).items():
        if code in estados:
            estados[code].mastery = valor
    return estados


def _candidatas(limite: int = 24):
    return [a for a in ActivityRepository(_db).all()
            if a.level <= 3 and a.sequence][:limite]


def test_respeta_el_tamano_y_el_tiempo() -> None:
    opt = SessionOptimizer(budget_minutes=8, session_size=4)
    sel = opt.solve(_candidatas(), _estados())
    assert len(sel.activities) == 4, sel.activities
    assert sel.total_minutes <= 8.0 + 1e-6, sel.total_minutes


def test_incluye_una_actividad_ludica() -> None:
    opt = SessionOptimizer(budget_minutes=10, session_size=4)
    sel = opt.solve(_candidatas(), _estados())
    assert any(a.kind == ActivityKind.GAME for a in sel.activities), \
        [a.code for a in sel.activities]


def test_no_insiste_mas_de_dos_veces_en_la_misma_habilidad() -> None:
    opt = SessionOptimizer(budget_minutes=10, session_size=4)
    sel = opt.solve(_candidatas(), _estados())
    conteo: dict[str, int] = {}
    for a in sel.activities:
        for c in a.skill_codes:
            conteo[c] = conteo.get(c, 0) + 1
    assert max(conteo.values(), default=0) <= 2, conteo


def test_acota_la_dificultad_media() -> None:
    opt = SessionOptimizer(budget_minutes=10, session_size=4)
    sel = opt.solve(_candidatas(), _estados())
    media = sum(a.difficulty for a in sel.activities) / len(sel.activities)
    assert media <= DIFFICULTY_CAP + 1e-6, media


def test_milp_y_enumeracion_coinciden() -> None:
    """La enumeración es el respaldo cuando CBC no está: debe dar el óptimo."""
    cand = _candidatas()
    estados = _estados(ajustes={"nota_MI3": 0.3, "nota_FA3": 0.45})

    con_milp = SessionOptimizer(budget_minutes=8, session_size=4,
                                prefer_milp=True).solve(cand, estados)
    sin_milp = SessionOptimizer(budget_minutes=8, session_size=4,
                                prefer_milp=False).solve(cand, estados)
    if con_milp.method != "milp":
        return                      # CBC no disponible en este equipo
    assert abs(con_milp.objective - sin_milp.objective) < 1e-4, \
        (con_milp.objective, sin_milp.objective)
    assert ({a.code for a in con_milp.activities}
            == {a.code for a in sin_milp.activities})


def test_la_seleccion_cambia_con_el_perfil() -> None:
    """Dos niños distintos no deben recibir la misma sesión."""
    cand = _candidatas()
    opt = SessionOptimizer(budget_minutes=8, session_size=4)
    novato = opt.solve(cand, _estados(0.15))
    avanzado = opt.solve(cand, _estados(0.9))
    assert ({a.code for a in novato.activities}
            != {a.code for a in avanzado.activities}), \
        "el optimizador ignoró el estado del niño"


def test_prefiere_lo_que_el_nino_tiene_flojo() -> None:
    cand = _candidatas()
    opt = SessionOptimizer(budget_minutes=10, session_size=4)
    estados = _estados(0.9, ajustes={"nota_MI3": 0.12})
    sel = opt.solve(cand, estados)
    toca_mi = any("nota_MI3" in a.skill_codes for a in sel.activities)
    assert toca_mi, [a.code for a in sel.activities]


def test_es_rapido() -> None:
    opt = SessionOptimizer(budget_minutes=8, session_size=4, prefer_milp=False)
    sel = opt.solve(_candidatas(), _estados())
    assert sel.seconds < 1.0, sel.seconds


if __name__ == "__main__":
    import traceback

    fallos = 0
    for nombre, fn in sorted(globals().items()):
        if nombre.startswith("test_") and callable(fn):
            try:
                fn()
                print(f"  ok   {nombre}")
            except AssertionError:
                fallos += 1
                print(f"  FALLA {nombre}")
                traceback.print_exc()

    opt = SessionOptimizer(budget_minutes=8, session_size=4)
    sel = opt.solve(_candidatas(), _estados(ajustes={"nota_MI3": 0.25}))
    print(f"\nSesión elegida ({sel.method}, {sel.seconds*1000:.0f} ms, "
          f"objetivo {sel.objective}):")
    for a in sel.activities:
        print(f"   {a.icon} {a.title:30} dif={a.difficulty:.2f}  {a.kind.value}")
    print("\nTodas las pruebas pasaron." if not fallos else f"\n{fallos} fallos.")
