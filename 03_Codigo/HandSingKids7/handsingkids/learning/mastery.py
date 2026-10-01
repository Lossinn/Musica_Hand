"""Cálculo del dominio de una habilidad y programación del repaso.

Una habilidad no se considera dominada por acertar una vez. El dominio se
define como el desempeño demostrado, moderado por cuánto se recuerda:

    M_s = ( lambda + (1 - lambda) * R_s^gamma ) * ( w_p P_s + w_c C_s + w_v V_s )

con w_p + w_c + w_v = 1 y lambda = 0.65. La retención entra multiplicando y no
sumando: si entrara como un cuarto sumando con peso 0.20, un mes sin practicar
haría bajar el dominio como mucho 0.20 y una habilidad olvidada seguiría
figurando como dominada. Multiplicando, el desuso prolongado sí la degrada,
mientras que el término lambda impide que el dominio se desplome a cero y borre
todo lo aprendido por faltar unos días.

Precisión, con suavizado bayesiano para que dos aciertos seguidos no den 100 %:

    P_s = (h_s + alpha) / (n_s + alpha + beta),    alpha = 1,  beta = 3

Sin práctica alguna, P_s = 0.25: el sistema parte de la duda, no del optimismo.

Consistencia sobre los últimos k intentos y_1..y_k en {0, 1}. Penaliza alternar
entre acierto y fallo, que es la firma de quien todavía no sabe, y se reduce
proporcionalmente cuando hay menos de k intentos, porque cuatro aciertos
seguidos no son evidencia de la misma fuerza que ocho:

    C_s = ybar_k * ( 1 - cambios / (k - 1) ) * min(1, k / K)

Velocidad, respecto a un tiempo de referencia propio de la edad:

    V_s = clip( (t_ref - tbar_s) / (t_ref - t_min),  0,  1 )

Retención, con olvido exponencial desde la última práctica:

    R_s = exp( -delta_t / tau_s ),    tau_s = tau_0 * eps_s * (0.6 + M_s^-)

donde delta_t va en días, eps_s es el factor de facilidad del repaso espaciado y
M_s^- es el dominio calculado en la actualización anterior. Usar el dominio
previo, y no el actual, es lo que evita una definición circular.
"""

from __future__ import annotations

import time
from dataclasses import dataclass

from ..domain.entities import SkillState, SkillStatus

# Pesos del desempeño demostrado. Suman 1.
W_PRECISION = 0.55
W_CONSISTENCY = 0.25
W_SPEED = 0.20

# Modulación por retención.
LAMBDA_FLOOR = 0.65     # cuánto del dominio resiste al olvido
GAMMA = 0.40            # suaviza la caída de la retención

# Suavizado bayesiano de la precisión.
ALPHA = 1.0
BETA = 3.0

# Ventana de consistencia.
K_RECENT = 8

# Tiempos de reacción de referencia, en milisegundos, por franja de edad.
REACTION_MIN_MS = 700.0
REACTION_REF_MS = {"pequeños": 5200.0, "medianos": 4000.0, "grandes": 3200.0}

# Olvido y repaso espaciado.
TAU_0_DAYS = 1.8
EASE_MIN, EASE_MAX = 1.3, 2.8

# Umbrales de estado.
MASTERED_AT = 0.80
CONSOLIDATED_AT = 0.92
DEMOTE_AT = 0.70
MIN_ATTEMPTS_TO_MASTER = 6


def _clip(v: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, v))


def precision(hits: int, attempts: int) -> float:
    return (hits + ALPHA) / (attempts + ALPHA + BETA) if attempts >= 0 else 0.0


def consistency(recent: list[bool]) -> float:
    """`recent` va del intento más antiguo al más nuevo."""
    y = [1.0 if r else 0.0 for r in recent][-K_RECENT:]
    if not y:
        return 0.0
    evidencia = min(1.0, len(y) / K_RECENT)
    if len(y) < 2:
        return _clip(y[0] * evidencia)
    mean = sum(y) / len(y)
    cambios = sum(1 for i in range(1, len(y)) if y[i] != y[i - 1])
    return _clip(mean * (1.0 - cambios / (len(y) - 1)) * evidencia)


def speed(mean_reaction_ms: float, age_band: str = "medianos") -> float:
    if mean_reaction_ms <= 0:
        return 0.0
    ref = REACTION_REF_MS.get(age_band, 4000.0)
    return _clip((ref - mean_reaction_ms) / (ref - REACTION_MIN_MS))


def retention(last_practice_at: float, ease: float, previous_mastery: float,
              now: float | None = None) -> float:
    if last_practice_at <= 0:
        return 1.0
    now = now if now is not None else time.time()
    delta_days = max(0.0, (now - last_practice_at) / 86400.0)
    tau = TAU_0_DAYS * max(ease, EASE_MIN) * (0.6 + _clip(previous_mastery))
    return _clip(pow(2.718281828459045, -delta_days / max(tau, 1e-6)))


def performance(p: float, c: float, v: float) -> float:
    """Desempeño demostrado, sin considerar el paso del tiempo."""
    return _clip(W_PRECISION * p + W_CONSISTENCY * c + W_SPEED * v)


def mastery(p: float, c: float, v: float, r: float) -> float:
    factor = LAMBDA_FLOOR + (1.0 - LAMBDA_FLOOR) * pow(_clip(r), GAMMA)
    return _clip(factor * performance(p, c, v))


# --------------------------------------------------------- repaso espaciado

def schedule_review(state: SkillState, quality: float,
                    now: float | None = None) -> None:
    """Actualiza el factor de facilidad y la fecha del próximo repaso.

    Adaptación del esquema SM-2 a una escala de calidad continua en [0, 1]:

        eps  <- clip( eps + 0.1 - (1 - q) * (0.8 + (1 - q)),  1.3,  2.8 )
        I    <- 1                 si q < 0.6
                max(1, I * eps)   en caso contrario

    El primer repaso cae al día siguiente; a partir de ahí el intervalo crece
    en proporción a lo bien que va la habilidad.
    """
    now = now if now is not None else time.time()
    q = _clip(quality)
    state.ease = max(EASE_MIN, min(EASE_MAX,
                                   state.ease + 0.1 - (1 - q) * (0.8 + (1 - q))))
    if q < 0.6:
        state.interval_days = 1.0
    elif state.interval_days <= 0:
        state.interval_days = 1.0
    else:
        state.interval_days = max(1.0, state.interval_days * state.ease)
    state.last_practice_at = now
    state.due_at = now + state.interval_days * 86400.0


# ------------------------------------------------------------- transiciones

def next_status(state: SkillState, current: SkillStatus) -> SkillStatus:
    """Avance —o retroceso— del estado de una habilidad."""
    if current == SkillStatus.LOCKED:
        return current
    if state.attempts == 0:
        return SkillStatus.INTRODUCED
    if state.mastery >= CONSOLIDATED_AT and state.attempts >= MIN_ATTEMPTS_TO_MASTER * 2:
        return SkillStatus.CONSOLIDATED
    if state.mastery >= MASTERED_AT and state.attempts >= MIN_ATTEMPTS_TO_MASTER:
        return SkillStatus.MASTERED
    if current in (SkillStatus.MASTERED, SkillStatus.CONSOLIDATED) \
            and state.mastery < DEMOTE_AT:
        return SkillStatus.PRACTICING
    if current in (SkillStatus.MASTERED, SkillStatus.CONSOLIDATED):
        return current
    return SkillStatus.PRACTICING


@dataclass
class MasteryUpdate:
    state: SkillState
    previous_mastery: float
    previous_status: SkillStatus
    promoted: bool

    @property
    def delta(self) -> float:
        return self.state.mastery - self.previous_mastery


def update_skill(state: SkillState, *, recent: list[bool], new_hits: int,
                 new_attempts: int, reaction_ms: float, age_band: str,
                 quality: float, now: float | None = None) -> MasteryUpdate:
    """Aplica el resultado de una práctica sobre el estado de la habilidad."""
    now = now if now is not None else time.time()
    previous_mastery = state.mastery
    previous_status = state.status

    total_attempts = state.attempts + new_attempts
    if new_attempts > 0 and reaction_ms > 0:
        # Media móvil del tiempo de reacción, ponderada por el número de intentos.
        w = new_attempts / max(1, total_attempts)
        state.mean_reaction_ms = ((1 - w) * state.mean_reaction_ms + w * reaction_ms
                                  if state.mean_reaction_ms > 0 else reaction_ms)
    state.attempts = total_attempts
    state.hits += new_hits

    state.precision = precision(state.hits, state.attempts)
    state.consistency = consistency(recent)
    state.speed = speed(state.mean_reaction_ms, age_band)

    schedule_review(state, quality, now=now)
    state.retention = retention(state.last_practice_at, state.ease,
                                previous_mastery, now=now)
    state.mastery = mastery(state.precision, state.consistency,
                            state.speed, state.retention)
    state.status = next_status(state, previous_status)

    return MasteryUpdate(state=state, previous_mastery=previous_mastery,
                         previous_status=previous_status,
                         promoted=state.status.order > previous_status.order)


def decay(state: SkillState, now: float | None = None) -> float:
    """Recalcula el dominio por el simple paso del tiempo, sin practicar."""
    state.retention = retention(state.last_practice_at, state.ease,
                                state.mastery, now=now)
    state.mastery = mastery(state.precision, state.consistency,
                            state.speed, state.retention)
    return state.mastery
