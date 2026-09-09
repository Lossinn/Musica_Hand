"""Coherencia de la Ruta de Aprendizaje Musical (curriculum.py)."""
from __future__ import annotations

import pytest

from Prototipo import config, curriculum as cur


def test_importa_y_tiene_etapas():
    assert cur.N_ETAPAS == len(cur.CURRICULUM)
    assert cur.N_ETAPAS >= 2
    assert cur.CURRICULUM[0].id == 0 and not cur.CURRICULUM[0].puntua


def test_ids_consecutivos():
    assert [e.id for e in cur.CURRICULUM] == list(range(cur.N_ETAPAS))


def test_notas_activas_son_acumulativas_y_validas():
    validas = set(cur.NOTAS_EXTENDIDAS)
    prev: set[str] = set()
    for e in cur.CURRICULUM:
        activas = set(e.notas_activas)
        assert prev <= activas, f"Etapa {e.id} pierde notas ya desbloqueadas"
        assert activas <= validas, f"Etapa {e.id} usa una nota desconocida"
        prev = activas
    # al final se llega a la octava completa (7 + DO agudo)
    assert prev == validas


def test_figuras_activas_son_acumulativas():
    prev: list = []
    for e in cur.CURRICULUM:
        activas = list(e.figuras_activas)
        assert prev == activas[: len(prev)], f"Etapa {e.id} reordena/pierde figuras"
        prev = activas
    assert set(cur.CURRICULUM[-1].figuras_activas) == set(cur.TODAS_LAS_FIGURAS)


def test_una_dificultad_nueva_por_etapa():
    """§0 del doc: salvo la Etapa 1 (base), ninguna etapa introduce notas nuevas
    junto con una figura rítmica que subdivide el pulso (la dificultad fuerte)."""
    for e in cur.CURRICULUM:
        if e.id <= 1:
            continue
        subdivide_nueva = any(f.subdivide for f in e.figuras_nuevas)
        assert not (e.notas_nuevas and subdivide_nueva), (
            f"Etapa {e.id} introduce notas Y una figura que subdivide a la vez"
        )


def test_ruta_alterna_notas_y_ritmo():
    """Mientras entran notas (etapas 2..8) se alterna 'notas' / 'ritmo'.
    Después (9, 10) solo quedan etapas de ritmo, lo cual es esperado."""
    pilares = [e.pilar for e in cur.CURRICULUM if 2 <= e.id <= 8]
    for a, b in zip(pilares, pilares[1:]):
        assert a != b, f"Dos etapas de contenido seguidas con pilar '{a}'"


def test_dinamicas_validas():
    for e in cur.CURRICULUM:
        assert set(e.dinamicas) <= set(config.DINAMICAS)


def test_gesto_nota_cubre_todas_las_notas():
    assert set(cur.GESTO_NOTA) == set(config.NOTAS)
    assert len(config.NOTAS) == 8            # octava reducida DO3..DO4
    # identidad: el gesto ES el nombre de la nota
    assert all(g == n for g, n in cur.GESTO_NOTA.items())


def test_paleta_editor_nivel_vs_libre():
    nivel = cur.paleta_editor(3, modo="nivel")
    libre = cur.paleta_editor(3, modo="libre")
    assert set(nivel["notas"]) <= set(libre["notas"])
    assert len(libre["figuras"]) == len(cur.TODAS_LAS_FIGURAS)


def test_puede_avanzar():
    bien = {"precision": 0.9, "error_rate": 0.1, "timing_ok_rate": 0.85, "tendencia": "mejorando"}
    mal = {"precision": 0.6, "error_rate": 0.3, "timing_ok_rate": 0.5, "tendencia": "empeorando"}
    assert cur.puede_avanzar(bien)
    assert not cur.puede_avanzar(mal)


@pytest.mark.parametrize("etapa_id", range(13))
def test_interpolar_rango_monotono_dentro_de_limites(etapa_id):
    r0 = cur.interpolar_rango(etapa_id, 0.0)
    r1 = cur.interpolar_rango(etapa_id, 1.0)
    assert r0.bpm[0] <= r0.bpm[1]
    assert r1.tol_ms[0] <= r1.tol_ms[1]
