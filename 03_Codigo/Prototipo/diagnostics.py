"""Diagnóstico general del niño (Fases 6 y 8).

El usuario pidió "más diagnóstico general": no basta con la precisión de la última
nota. Este módulo produce una foto holística y explicable del estado musical del
niño, con dos usos:

  1. **Colocación** (`diagnostico_inicial`): una prueba corta al entrar por
     primera vez sitúa al niño en una etapa del currículo en vez de empezar
     siempre en la 0.
  2. **Seguimiento** (`actualizar` / `resumen_sesion`): tras cada actividad y al
     cerrar la sesión, se recalcula el diagnóstico y se guarda en
     `diagnostics/<user_id>.json`.

`diagnostics` NO decide qué actividad viene después (eso es `adaptive/`). Solo
responde: **¿qué domina el niño, qué le cuesta y dónde debería estar?**
"""
from __future__ import annotations

from dataclasses import dataclass, field

from . import config, curriculum
from .persistence import Store


# ─────────────────────────────────────────────────────────────────────────────
# 1. Dominio por elemento (nota / ritmo)
# ─────────────────────────────────────────────────────────────────────────────
@dataclass
class DominioNota:
    """Cuánto domina el niño UNA nota concreta."""

    nota: str
    intentos: int = 0
    aciertos: int = 0
    precision: float = 0.0                 # aciertos / intentos, suavizado
    latencia_media_s: float = 0.0
    racha: int = 0                         # aciertos seguidos (o negativa: fallos)
    estado: str = "nuevo"                  # config.ESTADOS_DOMINIO


@dataclass
class DominioRitmo:
    """Cuánto domina el niño UNA figura rítmica (por nombre de curriculum.Figura)."""

    figura: str
    intentos: int = 0
    aciertos_timing: int = 0
    precision_timing: float = 0.0
    desfase_medio_ms: float = 0.0          # + tarde / - pronto: revela sesgo
    estado: str = "nuevo"


# ─────────────────────────────────────────────────────────────────────────────
# 2. Diagnóstico agregado
# ─────────────────────────────────────────────────────────────────────────────
@dataclass
class Diagnostico:
    """Foto completa. Se persiste y se muestra (en versión resumida) a adultos."""

    user_id: str
    generado_en: str = ""
    n_actividades: int = 0                 # cuántos datos respaldan esto

    # Colocación / progreso
    etapa_estimada: int = 0               # dónde debería jugar ahora
    etapa_max_desbloqueada: int = 0

    # Detalle por elemento
    dominio_notas: dict[str, DominioNota] = field(default_factory=dict)
    dominio_ritmos: dict[str, DominioRitmo] = field(default_factory=dict)

    # Síntesis legible
    fortalezas: list[str] = field(default_factory=list)      # p. ej. ["SOL", "pulso estable"]
    dificultades: list[str] = field(default_factory=list)    # p. ej. ["FA", "corcheas"]
    tendencia: str = "estable"            # "mejorando" | "estable" | "empeorando"
    perfil_aprendizaje: str = "medio"    # config.PERFILES_APRENDIZAJE (liga con digital_twin)
    ritmo_vs_notas: float = 0.5           # 0 = flojo en ritmo, 1 = flojo en notas

    # Para el adulto / docente
    recomendacion: str = ""
    confianza: float = 0.0               # 0..1 según n_actividades

    def metricas_avance(self) -> dict:
        """Formato que espera `curriculum.puede_avanzar` para la etapa actual."""
        raise NotImplementedError("Fase 6: agregar métricas de la ventana reciente")


# ─────────────────────────────────────────────────────────────────────────────
# 3. Prueba de colocación
# ─────────────────────────────────────────────────────────────────────────────
@dataclass
class ItemDiagnostico:
    """Un reto de la prueba inicial: se sube o baja según acierte."""

    etapa_id: int
    notas: tuple[str, ...]
    figura: str
    bpm: int


def prueba_diagnostica() -> list[ItemDiagnostico]:
    """Secuencia adaptativa corta (`config.PRUEBA_DIAGNOSTICA_ITEMS` ítems) que
    recorre el currículo tipo búsqueda binaria para situar al niño."""
    raise NotImplementedError("Fase 6: generar ítems de colocación desde curriculum")


# ─────────────────────────────────────────────────────────────────────────────
# 4. Servicio
# ─────────────────────────────────────────────────────────────────────────────
class Diagnosticador:
    """Construye y mantiene el `Diagnostico`. Sin estado propio salvo el store."""

    def __init__(self, store: Store) -> None:
        self.store = store

    # ── colocación ─────────────────────────────────────────────────────
    def diagnostico_inicial(self, user_id: str, respuestas: list) -> Diagnostico:
        """A partir de las respuestas a `prueba_diagnostica()`, fija
        `etapa_estimada` y un primer mapa de dominio. Persiste y devuelve."""
        raise NotImplementedError("Fase 6: estimar etapa desde la prueba")

    # ── seguimiento ────────────────────────────────────────────────────
    def actualizar(self, diagnostico: Diagnostico, result) -> Diagnostico:
        """Incorpora UN `game.ActivityResult`: actualiza el `DominioNota` /
        `DominioRitmo` implicado, recalcula estados, tendencia y confianza."""
        raise NotImplementedError("Fase 6: actualización incremental del diagnóstico")

    def resumen_sesion(self, user_id: str, profile) -> Diagnostico:
        """Recalcula el diagnóstico completo desde el historial del `ChildProfile`
        al cerrar la sesión (pantalla 'resumen'). Persiste."""
        raise NotImplementedError("Fase 6/8: diagnóstico de cierre de sesión")

    # ── consultas derivadas ────────────────────────────────────────────
    def etapa_recomendada(self, diagnostico: Diagnostico) -> int:
        """Etapa donde el niño debería jugar ahora (0..curriculum.N_ETAPAS-1).
        Nunca supera `etapa_max_desbloqueada`."""
        raise NotImplementedError("Fase 6")

    def notas_fragiles(self, diagnostico: Diagnostico) -> list[str]:
        """Notas con estado 'fragil' — candidatas a repaso dirigido."""
        raise NotImplementedError("Fase 6")

    def clasificar_perfil(self, diagnostico: Diagnostico) -> str:
        """'rapido' | 'medio' | 'lento' según velocidad de dominio y retención.
        Alimenta `digital_twin.TwinParams` para la simulación."""
        raise NotImplementedError("Fase 9: mapear diagnóstico -> perfil de gemelo")

    # ── persistencia ───────────────────────────────────────────────────
    def cargar(self, user_id: str) -> Diagnostico:
        """Carga el diagnóstico guardado o crea uno vacío (confianza 0)."""
        raise NotImplementedError("Fase 6")

    def guardar(self, diagnostico: Diagnostico) -> None:
        raise NotImplementedError("Fase 6")

    # ── helpers de clasificación de estado ─────────────────────────────
    @staticmethod
    def estado_nota(d: DominioNota) -> str:
        """Regla explícita nuevo/en_progreso/fragil/dominado (config.ESTADOS_DOMINIO)."""
        raise NotImplementedError("Fase 6: umbrales de estado de dominio")
