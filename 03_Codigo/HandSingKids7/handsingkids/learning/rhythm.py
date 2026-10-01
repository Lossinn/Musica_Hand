"""Motor de la mecánica de nota viajera ("Canciones"): el mismo árbitro que
`evaluation.ActivityRunner`, pero dirigido por el reloj en vez de esperar a
que el niño reaccione.

En el ejercicio guiado de siempre, un paso espera indefinidamente a que el
niño haga la seña correcta antes de avanzar. Aquí no: como en la mecánica de
"Notas Rítmicas" de la primera versión de la aplicación (estilo Guitar Hero),
cada nota tiene un instante en el que su centro cruza la línea de impacto, y
una ventana de tiempo alrededor de ese instante en la que la seña confirmada
cuenta como acierto. Si la nota cruza la línea sin que se confirme la seña a
tiempo, se marca fallada y el juego sigue de inmediato, sin detenerse a
esperar ni a repetir — igual que en la v0.

La ventana no es un instante exacto porque, a diferencia de una tecla, una
seña necesita sostenerse un momento para que el estabilizador de la cámara la
confirme (ver `vision.stabilizer`); por eso la ventana se calcula ancha y
ligeramente adelantada, para absorber ese tiempo de confirmación sin que se
sienta injusta.

Expone la misma interfaz pública que `ActivityRunner` que consume
`learning.session_flow.apply_result()` (`activity`, `attempts`,
`build_result()`, `per_note_summary()`, `steps_correct`, `total_steps`), así
una canción del catálogo jugada aquí alimenta el dominio por nota y al
Agente Adaptativo exactamente igual que un ejercicio guiado. Una melodía
grabada en Modo Libre puede usar este mismo motor solo para puntuar en
pantalla, sin pasar nunca por `apply_result()` (así no cuenta para el
progreso, tal como se decidió para ese caso).
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from enum import Enum

from PySide6.QtCore import QObject, QTimer, Signal

from ..core.events import BUS, Event, EventBus
from ..domain.entities import Activity, ActivityResult, Attempt
from ..domain.notes import SILENCE

TICK_MS = 30                  # frecuencia del reloj interno de juicio
TRAVEL_MS = 2200.0            # cuánto tiempo es visible una nota antes de llegar
TRAILING_MS = 900.0           # margen tras la última nota antes de terminar
MIN_WINDOW_MS = 480.0         # ventana de acierto mínima, incluso a tempos muy rápidos
GAP_MIN_MS = 220.0            # límites al usar tiempos reales grabados en Modo Libre
GAP_MAX_MS = 4000.0

# Tramos de calidad según qué tan cerca del cruce exacto se confirmó la seña.
# (Ensanchados a partir de la queja de que Canciones se sentía "muy estricta":
# antes MIN_WINDOW_MS/TIER_GOOD_MS eran 380/380 ms; con el reconocimiento
# instantáneo actual, el niño tiene menos margen natural que con la vieja
# "barra de aceptación", así que la ventana y el tramo "bien" se ensanchan
# para compensarlo. Ver también TEMPO_FACTORS: un tempo más lento agranda
# esta ventana todavía más, porque queda acotada por el intervalo entre notas.)
TIER_PERFECT_MS = 200.0
TIER_GOOD_MS = 480.0
TIER_POINTS = {"perfecto": 100, "bien": 70, "vale": 50}

# Velocidad elegible para una canción del catálogo (petición explícita del
# usuario: "que pueda escogerse el tiempo porque están muy rápido"). Se aplica
# como un factor sobre el tempo propio de la canción, no lo reemplaza: así
# "lento" en una canción de 70 bpm y en una de 100 bpm siguen siendo,
# proporcionalmente, la misma rebaja de velocidad.
TEMPO_FACTORS = {"lento": 0.72, "normal": 1.0, "rapido": 1.15}
TEMPO_LABELS = {"lento": "🐢 Lento", "normal": "Normal", "rapido": "🐇 Rápido"}


class NoteJudgement(str, Enum):
    PENDING = "pendiente"
    HIT = "acierto"
    MISSED = "fallada"


@dataclass
class ScheduledNote:
    """Una nota (o un silencio) ya ubicada en la línea de tiempo de la
    partida: cuándo cruza la línea de impacto y qué tan ancha es la ventana
    de acierto a cada lado de ese instante."""
    index: int
    code: str
    arrival_ms: float
    window_before_ms: float
    window_after_ms: float
    judged: NoteJudgement = NoteJudgement.PENDING

    @property
    def is_silence(self) -> bool:
        return self.code == SILENCE


class RhythmRunner(QObject):
    """Árbitro de una partida de nota viajera."""

    noteJudged = Signal(int, str, str, int)  # (index, "acierto"|"fallada", tier, offset_ms)
    scoreChanged = Signal(int, int)         # (puntaje, combo)
    finished = Signal(object)               # ActivityResult

    def __init__(self, activity: Activity, profile_id: int, *,
                 gaps_ms: list[float] | None = None,
                 tempo_factor: float = 1.0,
                 bus: EventBus | None = None, parent=None) -> None:
        super().__init__(parent)
        self.activity = activity
        self.profile_id = profile_id
        self.bus = bus or BUS
        # Factor de velocidad elegido por la familia (ver TEMPO_FACTORS): no
        # toca `activity.tempo_bpm` (eso seguiría describiendo la canción tal
        # cual está en el catálogo), solo el tempo con el que se planifica y
        # se juzga esta partida en concreto.
        self.tempo_factor = max(0.4, min(1.6, tempo_factor))

        self.sequence = list(activity.sequence)
        self.notes: list[ScheduledNote] = self._schedule(gaps_ms)
        self.attempts: list[Attempt] = []
        self.confidences: list[float] = []
        self.intervals: list[float] = []
        self._last_hit_ms: float = 0.0

        self.score = 0
        self.combo = 0
        self.max_combo = 0
        self.steps_correct = 0

        self._elapsed_ms = 0.0
        self._running = False
        self._started_at = 0.0
        self._finished_at = 0.0

        self._timer = QTimer(self)
        self._timer.setInterval(TICK_MS)
        self._timer.timeout.connect(self._tick)

    # ------------------------------------------------------- planificación
    def _schedule(self, gaps_ms: list[float] | None) -> list[ScheduledNote]:
        """Calcula el instante de llegada de cada nota y su ventana de
        acierto. Con tempo constante (decisión tomada para este módulo), el
        intervalo entre notas es siempre `60000/tempo_bpm` salvo que se pasen
        `gaps_ms` explícitos: es lo que usa "a mi ritmo" para respetar el
        tiempo real que el niño dejó entre cada nota al grabarla en Modo
        Libre, con un mínimo y un máximo para que la partida siga siendo
        jugable aunque la grabación tuviera una pausa larguísima.

        `self.tempo_factor` (ver TEMPO_FACTORS) alarga o acorta ese intervalo
        de forma proporcional, tanto a tempo constante como con tiempos
        grabados: elegir "lento" no solo dilata el tiempo entre notas, sino
        que también ensancha la ventana de acierto de cada una (más abajo),
        porque esa ventana está acotada por lo ancho que sea el propio
        intervalo."""
        gap_tempo = 60_000.0 / max(30, self.activity.tempo_bpm)
        notas: list[ScheduledNote] = []
        arrival = TRAVEL_MS
        for i, code in enumerate(self.sequence):
            if i > 0:
                gap = (gaps_ms[i] if (gaps_ms and i < len(gaps_ms))
                       else gap_tempo)
                gap = gap / self.tempo_factor
                gap = max(GAP_MIN_MS, min(GAP_MAX_MS, float(gap)))
                arrival += gap
            else:
                gap = gap_tempo / self.tempo_factor
            half = max(MIN_WINDOW_MS,
                       min(self.activity.tolerance_ms, gap * 0.85)) / 2.0
            # Un poco más de margen antes de la línea que después: el niño
            # suele empezar a sostener la seña con anticipación, y así el
            # tiempo que tarda el estabilizador en confirmarla no lo penaliza.
            notas.append(ScheduledNote(
                index=i, code=code, arrival_ms=arrival,
                window_before_ms=half * 1.15, window_after_ms=half * 0.85))
        return notas

    # ------------------------------------------------------------- estado
    @property
    def total_steps(self) -> int:
        return sum(1 for n in self.notes if not n.is_silence)

    @property
    def running(self) -> bool:
        return self._running

    @property
    def elapsed_ms(self) -> float:
        return self._elapsed_ms

    @property
    def total_duration_ms(self) -> float:
        if not self.notes:
            return TRAVEL_MS + TRAILING_MS
        last = self.notes[-1]
        return last.arrival_ms + last.window_after_ms + TRAILING_MS

    def progress_fraction(self, n: ScheduledNote) -> float:
        """1.0 = la nota recién aparece por la derecha, 0.0 = está cruzando
        la línea de impacto, negativo = ya la pasó."""
        return (n.arrival_ms - self._elapsed_ms) / TRAVEL_MS

    def visible_notes(self) -> list[ScheduledNote]:
        """Notas que un widget debería estar dibujando ahora mismo."""
        return [n for n in self.notes if -0.35 <= self.progress_fraction(n) <= 1.05]

    # -------------------------------------------------------------- ciclo
    def start(self) -> None:
        self._started_at = time.time()
        self._running = True
        self._elapsed_ms = 0.0
        self.bus.publish(Event.EXERCISE_STARTED, activity=self.activity.code,
                         steps=self.total_steps)
        self._timer.start()

    def _tick(self) -> None:
        if not self._running:
            return
        self._elapsed_ms = (time.time() - self._started_at) * 1000.0
        for n in self.notes:
            if (n.judged == NoteJudgement.PENDING and not n.is_silence
                    and self._elapsed_ms > n.arrival_ms + n.window_after_ms):
                self._resolve_miss(n)
        if self._elapsed_ms >= self.total_duration_ms:
            self.finish()

    def _nota_activa(self) -> ScheduledNote | None:
        """La nota pendiente más próxima cuya ventana de acierto ya incluye
        el instante actual. Si ninguna nota está "en juego" ahora mismo, una
        seña confirmada de más simplemente no cuenta ni penaliza: es más
        justo que castigar una seña sostenida un poco de más."""
        candidatas = [n for n in self.notes
                      if n.judged == NoteJudgement.PENDING and not n.is_silence
                      and (n.arrival_ms - n.window_before_ms) <= self._elapsed_ms
                      <= (n.arrival_ms + n.window_after_ms)]
        return candidatas[0] if candidatas else None

    def submit(self, note: str, confidence: float = 1.0) -> bool:
        """Registra una seña confirmada. Devuelve si fue correcta.

        Calca la regla de "Notas Rítmicas" (la mecánica original, v0): una
        seña que no es la pedida no falla la nota ni rompe la racha, solo no
        cuenta. La nota sigue pendiente y el niño puede seguir intentando
        hasta acertarla o hasta que termine de cruzar su ventana de acierto
        (momento en que sí se falla, en `_tick`/`_resolve_miss`) — igual que
        en v0, donde una seña equivocada simplemente no coincidía con el
        sprite de la nota y esta seguía viajando sin más consecuencia."""
        if not self._running:
            return False
        n = self._nota_activa()
        if n is None:
            return False
        offset_ms = self._elapsed_ms - n.arrival_ms
        if note != n.code:
            # Se registra el intento (alimenta el dominio por nota), pero no
            # se resuelve la nota: queda pendiente para un próximo intento.
            self._register(n, detected=note, confidence=confidence,
                           correct=False, reaction_ms=int(abs(offset_ms)))
            return False

        n.judged = NoteJudgement.HIT
        self._register(n, detected=note, confidence=confidence,
                       correct=True, reaction_ms=int(abs(offset_ms)))
        self.steps_correct += 1
        self.confidences.append(confidence)
        if self._last_hit_ms:
            self.intervals.append((self._elapsed_ms - self._last_hit_ms) / 1000.0)
        self._last_hit_ms = self._elapsed_ms
        self.combo += 1
        self.max_combo = max(self.max_combo, self.combo)
        tier = self._tier(abs(offset_ms))
        self._award(tier)
        self.noteJudged.emit(n.index, "acierto", tier, int(offset_ms))
        return True

    def _resolve_miss(self, n: ScheduledNote) -> None:
        n.judged = NoteJudgement.MISSED
        self.combo = 0
        self._register(n, detected=None, confidence=0.0, correct=False,
                       reaction_ms=int(n.window_after_ms))
        self.scoreChanged.emit(self.score, self.combo)
        self.noteJudged.emit(n.index, "fallada", "", 0)

    def _register(self, n: ScheduledNote, *, detected: str | None,
                  confidence: float, correct: bool, reaction_ms: int) -> None:
        self.attempts.append(Attempt(
            profile_id=self.profile_id, activity_code=self.activity.code,
            step_index=n.index, expected=n.code, detected=detected,
            confidence=confidence, correct=correct, reaction_ms=reaction_ms))

    # ----------------------------------------------------------- puntaje
    @staticmethod
    def _tier(offset_ms: float) -> str:
        if offset_ms <= TIER_PERFECT_MS:
            return "perfecto"
        if offset_ms <= TIER_GOOD_MS:
            return "bien"
        return "vale"

    def _award(self, tier: str) -> None:
        # Fórmula calcada de "Notas Rítmicas" (v0, ScoreManager.hit()): cada
        # 10 de racha suma +0,5 al multiplicador, con techo en 4,0.
        multiplier = min(1.0 + (self.combo // 10) * 0.5, 4.0)
        self.score += int(TIER_POINTS[tier] * multiplier)
        self.scoreChanged.emit(self.score, self.combo)

    @property
    def live_accuracy(self) -> float:
        """Precisión sobre lo ya juzgado hasta ahora (no sobre la canción
        completa): el mismo `accuracy()` que mostraba el HUD de "Notas
        Rítmicas" en v0, que subía o bajaba nota a nota en vez de mostrarse
        solo al final."""
        juzgadas = [n for n in self.notes if not n.is_silence
                   and n.judged != NoteJudgement.PENDING]
        if not juzgadas:
            return 0.0
        aciertos = sum(1 for n in juzgadas if n.judged == NoteJudgement.HIT)
        return round(100.0 * aciertos / len(juzgadas), 1)

    # ------------------------------------------------------------- cierre
    def abandon(self) -> None:
        if not self._running:
            return
        self._running = False
        self._timer.stop()
        self.bus.publish(Event.EXERCISE_ABANDONED, activity=self.activity.code,
                         steps_done=self.steps_correct)

    def finish(self) -> ActivityResult:
        self._running = False
        self._timer.stop()
        self._finished_at = time.time()
        for n in self.notes:
            if n.judged == NoteJudgement.PENDING and not n.is_silence:
                self._resolve_miss(n)
        result = self.build_result()
        self.bus.publish(Event.EXERCISE_COMPLETED, activity=self.activity.code,
                         accuracy=result.accuracy, stars=result.stars)
        self.finished.emit(result)
        return result

    def rhythm_score(self) -> float:
        if self.activity.tempo_bpm <= 0 or len(self.intervals) < 2:
            return 100.0
        target = (60.0 / max(30, self.activity.tempo_bpm)) / self.tempo_factor
        tol = max(0.35, self.activity.tolerance_ms / 1000.0)
        vals = [max(0.0, 1.0 - abs(dt - target) / tol) for dt in self.intervals[1:]]
        return round(100.0 * sum(vals) / len(vals), 1)

    @staticmethod
    def stars(accuracy: float) -> int:
        if accuracy >= 90:
            return 3
        if accuracy >= 70:
            return 2
        return 1

    def build_result(self) -> ActivityResult:
        accuracy = round(100.0 * self.steps_correct / max(1, self.total_steps), 1)
        quality = round(100.0 * (sum(self.confidences) / len(self.confidences)), 1) \
            if self.confidences else 0.0
        return ActivityResult(
            profile_id=self.profile_id, activity_code=self.activity.code,
            accuracy=accuracy, rhythm=self.rhythm_score(),
            gesture_quality=quality, stars=self.stars(accuracy),
            score=self.score, max_combo=self.max_combo,
            duration_s=round((self._finished_at or time.time()) - self._started_at, 1),
            steps_total=self.total_steps, steps_correct=self.steps_correct)

    def per_note_summary(self) -> dict[str, tuple[int, int, float, list[bool]]]:
        out: dict[str, list] = {}
        for a in self.attempts:
            entry = out.setdefault(a.expected, [0, 0, [], []])
            entry[1] += 1
            if a.correct:
                entry[0] += 1
                entry[2].append(a.reaction_ms)
            entry[3].append(a.correct)
        return {note: (v[0], v[1],
                       (sum(v[2]) / len(v[2])) if v[2] else 0.0,
                       v[3])
                for note, v in out.items()}
