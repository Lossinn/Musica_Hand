"""Coherencia de los contratos entre módulos (sin lógica implementada todavía).

Verifican que las interfaces encajan: nombres de pantallas, grafo de flujo,
campos de dataclasses y el store en memoria (única pieza ya funcional de
persistence)."""
from __future__ import annotations

import dataclasses

import pytest

from Prototipo import config
from Prototipo import screens
from Prototipo.persistence import MemoryStore
from Prototipo.adaptive.adapter import MargenAccion, ParametrosActividad


# ── flujo de pantallas ────────────────────────────────────────────────────
def test_pantallas_config_coincide_con_enum():
    assert set(config.PANTALLAS) == {p.value for p in screens.Pantalla}


def test_grafo_transiciones_cubre_todas_las_pantallas():
    assert set(screens.TRANSICIONES) == set(screens.Pantalla)
    for origen, destinos in screens.TRANSICIONES.items():
        for d in destinos:
            assert isinstance(d, screens.Pantalla), f"{origen} -> {d!r} no es Pantalla"


def test_grafo_no_tiene_pantallas_huerfanas():
    """Toda pantalla (salvo BIENVENIDA) es destino de alguna transición."""
    alcanzables = {d for destinos in screens.TRANSICIONES.values() for d in destinos}
    for p in screens.Pantalla:
        if p is not screens.Pantalla.BIENVENIDA:
            assert p in alcanzables, f"{p} es inalcanzable"


def test_requisitos_usan_claves_reales_del_contexto():
    campos = {f.name for f in dataclasses.fields(screens.ContextoApp)}
    for pantalla, claves in screens.REQUISITOS.items():
        for clave in claves:
            assert clave in campos, f"REQUISITOS[{pantalla}] pide '{clave}' inexistente"


# ── persistence: MemoryStore ya funciona ─────────────────────────────────
def test_memory_store_roundtrip():
    s = MemoryStore()
    assert s.leer("users/nino_01") is None
    s.escribir("users/nino_01", {"nombre": "Ana"})
    assert s.leer("users/nino_01") == {"nombre": "Ana"}
    assert s.existe("users/nino_01")
    s.escribir("users/nino_02", {"nombre": "Beto"})
    assert s.listar("users") == ["nino_01", "nino_02"]
    s.borrar("users/nino_01")
    assert not s.existe("users/nino_01")


def test_memory_store_listar_no_recursivo():
    s = MemoryStore()
    s.escribir("songs/nino_01/c1", {})
    s.escribir("songs/nino_01/c2", {})
    assert s.listar("songs/nino_01") == ["c1", "c2"]
    assert s.listar("songs") == []          # solo hijos directos


# ── adapter: el punto vive dentro del margen ─────────────────────────────
def test_parametros_actividad_tiene_todos_los_ejes_del_rango():
    from Prototipo import curriculum

    rango_campos = {f.name for f in dataclasses.fields(curriculum.RangoDificultad)}
    par_campos = {f.name for f in dataclasses.fields(ParametrosActividad)}
    # cada eje del RangoDificultad debe existir como parámetro concreto
    assert rango_campos <= par_campos, rango_campos - par_campos


def test_margen_accion_campos_minimos():
    campos = {f.name for f in dataclasses.fields(MargenAccion)}
    assert {"etapa_id", "rango", "notas", "figuras", "dinamicas", "compases"} <= campos
