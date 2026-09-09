import os
import json
import time
# ==========================
#       SCORE MANAGER
# ==========================
class ScoreManager:
    """
    Maneja la puntuación, combo, precisión y high scores por modo de juego.
    """
    def __init__(self, highscores_file="highscores.json"):
        base_path = os.path.dirname(os.path.abspath(__file__))

        if not os.path.isabs(highscores_file):
            highscores_file = os.path.normpath(
                os.path.join(
                    base_path,
                    '..',
                    '..',
                    'data',
                    highscores_file
                )
            )

        self.highscores_file = highscores_file
        self.reset()

    def reset(self):
        self.mode = None
        self.score = 0
        self.combo = 0
        self.max_combo = 0
        self.hits = 0
        self.misses = 0
        self.start_time = None
        self.judgement = None  # ("Perfect"/"Good"/"Ok"/"Miss", timestamp)

    # ----- Ciclo de partida -----
    def start(self, mode_name: str):
        self.reset()
        self.mode = mode_name
        self.start_time = time.time()

    def end(self):
        summary = {
            "mode": self.mode,
            "score": int(round(self.accuracy())),
            "max_combo": self.max_combo,
            "accuracy": self.accuracy(),
            "time": round(time.time() - self.start_time, 2) if self.start_time else 0,
        }
        self._save_highscore_if_needed(summary)
        return summary

    # ----- Acciones de juego -----
    def hit(self, tier: str):
        """
        tier ∈ {"Perfect","Good","Ok"}.
        Puntajes y combo por tier.
        """
        points = {"Perfect": 100, "Good": 70, "Ok": 50}.get(tier, 50)
        self.combo += 1
        self.max_combo = max(self.max_combo, self.combo)

        # Multiplicador por combo (cada 10 aumenta +0.5, cap 4.0)
        multiplier = min(1.0 + (self.combo // 10) * 0.5, 4.0)
        gained = int(points * multiplier)

        self.score += gained
        self.hits += 1
        self.judgement = (tier, time.time())

        return gained, multiplier

    def miss(self):
        self.combo = 0
        self.misses += 1
        self.judgement = ("Miss", time.time())

    # ----- Métricas -----
    def accuracy(self):
        total = self.hits + self.misses
        return round((self.hits / total) * 100, 1) if total else 0.0

    # ----- High scores -----
    def load_highscores(self):
        try:
            with open(self.highscores_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}

    def _save_highscore_if_needed(self, summary):
        data = self.load_highscores()
        mode = summary["mode"] or "Unknown"
        prev = data.get(mode)
        if (not prev) or summary["score"] > prev.get("score", 0):
            data[mode] = summary
            try:
                with open(self.highscores_file, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
            except Exception:
                pass  # no bloqueamos el juego si no se puede guardar
