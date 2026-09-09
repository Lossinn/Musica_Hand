"""Gestor de niveles y progreso (Fase 12 — integración).

Flujo 3 del diseño ("Niveles del juego"):
    Pantalla de niveles = etapas desbloqueadas + etapa actual + botón
    "Crea tus canciones". El progreso se guarda; las etapas se desbloquean
    dinámicamente según el desempeño.

`levels` es el puente entre el CURRÍCULO (contenido, `curriculum.py`), el
DIAGNÓSTICO (`diagnostics.py`) y la PERSISTENCIA. No genera actividades ni ajusta
dificultad fina (eso es `adaptive/`); decide **qué etapas puede tocar el niño y
en cuál está**.

Regla dura del flujo: *una etapa desbloqueada nunca se vuelve a bloquear.*
"""
from __future__ import annotations

from dataclasses import dataclass, field

from . import config, curriculum
from .diagnostics import Diagnosticador, Diagnostico
from .persistence import Store


@dataclass
class ProgresoEtapa:
    """Estado del niño en UNA etapa del currículo."""

    etapa_id: int
    desbloqueada: bool = False
    completada: bool = False               # cumplió `curriculum.puede_avanzar`
    actividades_hechas: int = 0
    mejor_precision: float = 0.0
    mejor_timing: float = 0.0
    estrellas: int = 0                     # 0..3 (como las tarjetas de canciones)
    ultima_dificultad: float = 0.0         # punto elegido dentro del RangoDificultad [0..1]
    ultima_vez: str = ""


@dataclass
class ProgresoJugador:
    """Todo el progreso de un niño. Se serializa a `progress/<user_id>.json`."""

    user_id: str
    etapa_actual: int = 0
    etapas: dict[int, ProgresoEtapa] = field(default_factory=dict)
    total_canciones_creadas: int = 0
    total_sesiones: int = 0
    actualizado_en: str = ""

    def desbloqueadas(self) -> list[int]:
        return sorted(i for i, e in self.etapas.items() if e.desbloqueada)

    def estrellas_totales(self) -> int:
        return sum(e.estrellas for e in self.etapas.values())


class GestorNiveles:
    """Carga, actualiza y persiste el `ProgresoJugador`."""

    def __init__(self, store: Store, diagnosticador: Diagnosticador) -> None:
        self.store = store
        self.diag = diagnosticador

    # ── ciclo de vida del progreso ─────────────────────────────────────
    def cargar(self, user_id: str) -> ProgresoJugador:
        """Carga el progreso o crea uno nuevo con la Etapa 0 desbloqueada.
        Si hay diagnóstico de colocación, desbloquea hasta `etapa_estimada`."""
        raise NotImplementedError("Fase 12: cargar/crear progreso + aplicar colocación")

    def guardar(self, progreso: ProgresoJugador) -> None:
        raise NotImplementedError("Fase 12")

    def nuevo(self, user_id: str, etapa_inicial: int = 0) -> ProgresoJugador:
        """Progreso inicial: etapas 0..etapa_inicial desbloqueadas."""
        raise NotImplementedError("Fase 12: sembrar ProgresoEtapa por cada etapa")

    # ── registro de resultados ─────────────────────────────────────────
    def registrar_resultado(
        self,
        progreso: ProgresoJugador,
        result,                            # game.ActivityResult
        diagnostico: Diagnostico,
    ) -> ProgresoJugador:
        """Actualiza `ProgresoEtapa` de la etapa actual (contadores, mejores
        marcas, estrellas) y, si procede, marca la etapa como completada y
        desbloquea la siguiente. Devuelve el progreso mutado (y lo guarda)."""
        raise NotImplementedError("Fase 12: actualizar etapa + evaluar avance")

    def evaluar_avance(self, progreso: ProgresoJugador, diagnostico: Diagnostico) -> bool:
        """True si la etapa actual cumple `curriculum.puede_avanzar` con las
        métricas del diagnóstico."""
        raise NotImplementedError("Fase 12: delegar en curriculum.puede_avanzar")

    def desbloquear_siguiente(self, progreso: ProgresoJugador) -> ProgresoJugador:
        """Desbloquea `etapa_actual + 1` (si existe) sin cambiar `etapa_actual`.
        Idempotente. No re-bloquea nada."""
        raise NotImplementedError("Fase 12")

    # ── navegación ─────────────────────────────────────────────────────
    def seleccionar_etapa(self, progreso: ProgresoJugador, etapa_id: int) -> ProgresoJugador:
        """El niño elige una etapa DESBLOQUEADA desde la pantalla de niveles.
        Lanza `ValueError` si está bloqueada."""
        raise NotImplementedError("Fase 12")

    def etapa_para_jugar(self, progreso: ProgresoJugador, diagnostico: Diagnostico) -> int:
        """Sugerencia por defecto al pulsar 'Aprender': normalmente la última
        desbloqueada, salvo que el diagnóstico recomiende repasar una previa."""
        raise NotImplementedError("Fase 12")

    # ── estrellas ──────────────────────────────────────────────────────
    @staticmethod
    def estrellas_por_desempeno(precision: float, timing: float) -> int:
        """0..3 según `config.ESTRELLAS_UMBRAL` (combina nota y ritmo)."""
        raise NotImplementedError("Fase 12: aplicar umbrales de estrellas")

    # ── vista para la UI ───────────────────────────────────────────────
    def resumen_ui(self, progreso: ProgresoJugador) -> list[dict]:
        """Una fila por etapa: {id, nombre, lema, desbloqueada, estrellas,
        es_actual} — lo que pinta la pantalla de niveles."""
        raise NotImplementedError("Fase 12: proyectar progreso + curriculum a la UI")
