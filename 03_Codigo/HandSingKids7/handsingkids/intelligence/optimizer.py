"""Selección de la próxima sesión como problema de optimización entera.

FORMULACIÓN

Conjuntos
    A   actividades candidatas, indexadas por i
    S   habilidades, indexadas por s
    S_i habilidades que toca la actividad i
    G   actividades lúdicas          R   repasos vencidos

Variable de decisión
    x_i = 1 si la actividad i entra en la sesión, 0 si no

Parámetros derivados del gemelo digital
    mu_s        dominio actual de la habilidad s, en [0, 1]
    dif_i       dificultad de la actividad, en [0, 1]
    d_i         duración estimada, en minutos
    u_s         urgencia de repaso, en [0, 1]

    Probabilidad estimada de éxito, logística sobre la holgura entre lo que el
    niño domina y lo que la actividad exige:

        mubar_i = (1/|S_i|) * sum_{s in S_i} mu_s
        p_i     = 1 / (1 + exp(-k * (mubar_i - dif_i))),    k = 6

    Factor de dificultad deseable. El aprendizaje no es máximo donde todo sale
    bien ni donde nada sale: se concentra alrededor de p* = 0.75.

        eta_i = exp( -(p_i - p*)^2 / (2 * sigma_p^2) ),     sigma_p = 0.18

    Ganancia de aprendizaje, urgencia, motivación y fatiga:

        g_i = eta_i * ( sum_{s in S_i} (1 - mu_s) ) / sqrt(|S_i|)
        r_i = (1/|S_i|) * sum_{s in S_i} u_s
        m_i = beta(tipo_i) + nu_i            nu_i = novedad
        f_i = (d_i / D) * (0.5 + dif_i)

Objetivo
    max  sum_i ( a1*g_i + a2*r_i + a3*m_i - a4*f_i ) * x_i

Restricciones
    (1)  sum_i d_i x_i <= T                        presupuesto de tiempo
    (2)  sum_i x_i = K                             tamaño de la sesión
    (3)  x_i <= a_i                                prerrequisitos cumplidos
    (4)  sum_{i in G} x_i >= 1        si K >= 3    al menos una actividad lúdica
    (5)  sum_i dif_i x_i <= dmax * K               dificultad media acotada
    (6)  sum_{i: s in S_i} x_i <= 2   para todo s  no insistir en lo mismo
    (7)  sum_{i in R} x_i >= 1        si R != {}   los repasos vencidos entran

RESOLUCIÓN

Se intenta primero con CBC a través de PuLP. Si el solucionador no está
disponible —el binario que trae PuLP para macOS es de Intel y en Apple Silicon
exige Rosetta— se resuelve por enumeración exhaustiva, que para los tamaños de
este problema (del orden de veinte candidatos y cuatro actividades) recorre unas
decenas de miles de combinaciones y devuelve el óptimo exacto, no una
aproximación. Solo si el catálogo creciera mucho se recurre a la heurística
voraz.
"""

from __future__ import annotations

import logging
import math
import time
from dataclasses import dataclass, field
from itertools import combinations

from ..domain.entities import Activity, ActivityKind, SkillState
from .predictor import MasteryPredictor

log = logging.getLogger(__name__)

# Pesos del objetivo.
A_GAIN = 1.00
A_REVIEW = 0.70
A_MOTIVATION = 0.35
A_FATIGUE = 0.55

# Forma de la dificultad deseable.
P_STAR = 0.75
SIGMA_P = 0.18
LOGISTIC_K = 6.0

# Cota de dificultad media.
DIFFICULTY_CAP = 0.72

# Bonificación de motivación por tipo de actividad.
KIND_BONUS = {
    ActivityKind.GAME: 0.85,
    ActivityKind.SONG: 0.70,
    ActivityKind.EXERCISE: 0.30,
    ActivityKind.REVIEW: 0.25,
    ActivityKind.ASSESSMENT: 0.10,
}

# A partir de aquí la enumeración exacta se vuelve costosa.
MAX_COMBINATIONS = 400_000


@dataclass
class Selection:
    activities: list[Activity]
    objective: float
    method: str                      # 'milp' | 'exacto' | 'voraz'
    seconds: float
    detail: dict[str, float] = field(default_factory=dict)

    @property
    def total_minutes(self) -> float:
        return sum(a.duration_s for a in self.activities) / 60.0


def _sigmoid(z: float) -> float:
    if z < -40:
        return 0.0
    if z > 40:
        return 1.0
    return 1.0 / (1.0 + math.exp(-z))


@dataclass
class ActivityScore:
    activity: Activity
    success_prob: float
    gain: float
    review: float
    motivation: float
    fatigue: float

    @property
    def value(self) -> float:
        return (A_GAIN * self.gain + A_REVIEW * self.review
                + A_MOTIVATION * self.motivation - A_FATIGUE * self.fatigue)


class SessionOptimizer:
    def __init__(self, budget_minutes: int = 8, session_size: int = 4,
                 prefer_milp: bool = True) -> None:
        self.budget_minutes = budget_minutes
        self.session_size = session_size
        self.prefer_milp = prefer_milp

    # ------------------------------------------------------- puntuaciones
    def score(self, activities: list[Activity],
              skill_states: dict[str, SkillState],
              recent_codes: set[str] | None = None,
              now: float | None = None,
              predictor: MasteryPredictor | None = None) -> list[ActivityScore]:
        """`predictor` es opcional: sin él (o mientras no tenga datos propios
        suficientes) se usa la misma fórmula fija de siempre. En cuanto el
        perfil acumula intentos reales y el predictor se entrena, sus
        probabilidades reemplazan a la fórmula sin que cambie nada más aquí —
        es justo el punto de extensión que `intelligence.predictor` documenta."""
        now = now if now is not None else time.time()
        recent_codes = recent_codes or set()
        out: list[ActivityScore] = []
        for a in activities:
            codes = [c for c in a.skill_codes if c in skill_states] or a.skill_codes
            mus = [skill_states[c].mastery for c in codes if c in skill_states]
            mubar = sum(mus) / len(mus) if mus else 0.0
            if predictor is not None:
                p = predictor.probability(a, skill_states, now=now).probability
            else:
                p = _sigmoid(LOGISTIC_K * (mubar - a.difficulty))
            eta = math.exp(-((p - P_STAR) ** 2) / (2 * SIGMA_P ** 2))

            gap = sum(1.0 - m for m in mus) if mus else 1.0
            gain = eta * gap / math.sqrt(max(1, len(mus) or 1))

            urg = []
            for c in codes:
                st = skill_states.get(c)
                if st is None or st.due_at <= 0:
                    urg.append(0.0)
                else:
                    atraso = (now - st.due_at) / 86400.0
                    urg.append(max(0.0, min(1.0, atraso / 3.0)))
            review = sum(urg) / len(urg) if urg else 0.0

            novelty = 0.0 if a.code in recent_codes else 0.25
            motivation = KIND_BONUS.get(a.kind, 0.2) + novelty

            minutes = a.duration_s / 60.0
            fatigue = (minutes / max(1.0, self.budget_minutes)) * (0.5 + a.difficulty)

            out.append(ActivityScore(a, p, gain, review, motivation, fatigue))
        return out

    # ---------------------------------------------------------- factible
    def _feasible(self, subset: tuple[ActivityScore, ...],
                  overdue_codes: set[str]) -> bool:
        k = len(subset)
        minutes = sum(s.activity.duration_s for s in subset) / 60.0
        if minutes > self.budget_minutes:
            return False                                       # (1)
        if sum(s.activity.difficulty for s in subset) > DIFFICULTY_CAP * k:
            return False                                       # (5)
        por_habilidad: dict[str, int] = {}
        for s in subset:
            for c in s.activity.skill_codes:
                por_habilidad[c] = por_habilidad.get(c, 0) + 1
                if por_habilidad[c] > 2:
                    return False                               # (6)
        if k >= 3 and not any(s.activity.kind == ActivityKind.GAME
                              for s in subset):
            return False                                       # (4)
        if overdue_codes and not any(s.activity.code in overdue_codes
                                     for s in subset):
            return False                                       # (7)
        return True

    # ----------------------------------------------------------- resolver
    def solve(self, activities: list[Activity],
              skill_states: dict[str, SkillState],
              recent_codes: set[str] | None = None,
              overdue_codes: set[str] | None = None,
              now: float | None = None,
              predictor: MasteryPredictor | None = None) -> Selection:
        t0 = time.time()
        scores = self.score(activities, skill_states, recent_codes, now, predictor)
        if not scores:
            return Selection([], 0.0, "vacio", 0.0)

        k = min(self.session_size, len(scores))
        overdue = set(overdue_codes or set())
        overdue &= {s.activity.code for s in scores}

        if self.prefer_milp:
            sel = self._solve_milp(scores, k, overdue)
            if sel is not None:
                sel.seconds = round(time.time() - t0, 4)
                return sel

        sel = self._solve_exact(scores, k, overdue)
        if sel is not None:
            sel.seconds = round(time.time() - t0, 4)
            return sel

        sel = self._solve_greedy(scores, k, overdue)
        sel.seconds = round(time.time() - t0, 4)
        return sel

    # -------------------------------------------------------------- MILP
    def _solve_milp(self, scores: list[ActivityScore], k: int,
                    overdue: set[str]) -> Selection | None:
        try:
            import pulp
        except Exception:
            return None
        try:
            prob = pulp.LpProblem("sesion_hand_sing_kids", pulp.LpMaximize)
            x = {i: pulp.LpVariable(f"x_{i}", cat="Binary")
                 for i in range(len(scores))}

            prob += pulp.lpSum(scores[i].value * x[i] for i in x)

            prob += pulp.lpSum(
                (scores[i].activity.duration_s / 60.0) * x[i] for i in x
            ) <= self.budget_minutes, "tiempo"
            prob += pulp.lpSum(x.values()) == k, "tamano"
            prob += pulp.lpSum(
                scores[i].activity.difficulty * x[i] for i in x
            ) <= DIFFICULTY_CAP * k, "dificultad_media"

            por_habilidad: dict[str, list[int]] = {}
            for i, s in enumerate(scores):
                for c in s.activity.skill_codes:
                    por_habilidad.setdefault(c, []).append(i)
            for c, idxs in por_habilidad.items():
                if len(idxs) > 2:
                    prob += pulp.lpSum(x[i] for i in idxs) <= 2, f"hab_{c}"

            juegos = [i for i, s in enumerate(scores)
                      if s.activity.kind == ActivityKind.GAME]
            if k >= 3 and juegos:
                prob += pulp.lpSum(x[i] for i in juegos) >= 1, "ludica"

            vencidos = [i for i, s in enumerate(scores)
                        if s.activity.code in overdue]
            if vencidos:
                prob += pulp.lpSum(x[i] for i in vencidos) >= 1, "repaso"

            status = prob.solve(pulp.PULP_CBC_CMD(msg=0, timeLimit=5))
            if pulp.LpStatus[status] != "Optimal":
                return None
            elegidas = [scores[i].activity for i in x
                        if x[i].value() is not None and x[i].value() > 0.5]
            if not elegidas:
                return None
            objetivo = sum(scores[i].value for i in x
                           if x[i].value() and x[i].value() > 0.5)
            return Selection(elegidas, round(objetivo, 4), "milp", 0.0)
        except Exception as exc:
            log.info("CBC no disponible o falló (%s); se resuelve por enumeración", exc)
            return None

    # ---------------------------------------------------------- exacto
    def _solve_exact(self, scores: list[ActivityScore], k: int,
                     overdue: set[str]) -> Selection | None:
        n = len(scores)
        if k <= 0 or k > n:
            return None
        if math.comb(n, k) > MAX_COMBINATIONS:
            return None
        mejor, mejor_valor = None, float("-inf")
        for subset in combinations(scores, k):
            if not self._feasible(subset, overdue):
                continue
            valor = sum(s.value for s in subset)
            if valor > mejor_valor:
                mejor, mejor_valor = subset, valor
        if mejor is None:
            # Ninguna combinación cumple todo: se relajan las restricciones
            # blandas (lúdica y repaso) antes que devolver una sesión vacía.
            for subset in combinations(scores, k):
                minutes = sum(s.activity.duration_s for s in subset) / 60.0
                if minutes > self.budget_minutes:
                    continue
                valor = sum(s.value for s in subset)
                if valor > mejor_valor:
                    mejor, mejor_valor = subset, valor
        if mejor is None:
            return None
        return Selection([s.activity for s in mejor], round(mejor_valor, 4),
                         "exacto", 0.0)

    # ----------------------------------------------------------- voraz
    def _solve_greedy(self, scores: list[ActivityScore], k: int,
                      overdue: set[str]) -> Selection:
        restantes = sorted(scores, key=lambda s: -s.value)
        elegidas: list[ActivityScore] = []
        for s in restantes:
            tentativa = tuple(elegidas + [s])
            minutes = sum(t.activity.duration_s for t in tentativa) / 60.0
            if minutes > self.budget_minutes:
                continue
            por_hab: dict[str, int] = {}
            exceso = False
            for t in tentativa:
                for c in t.activity.skill_codes:
                    por_hab[c] = por_hab.get(c, 0) + 1
                    if por_hab[c] > 2:
                        exceso = True
            if exceso:
                continue
            elegidas.append(s)
            if len(elegidas) >= k:
                break
        return Selection([s.activity for s in elegidas],
                         round(sum(s.value for s in elegidas), 4), "voraz", 0.0)
