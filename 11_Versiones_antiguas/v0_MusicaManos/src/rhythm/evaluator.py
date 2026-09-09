class RhythmEvaluator:
    """
    Evalúa qué tan cerca estuvo el niño de los tiempos
    esperados de un patrón rítmico.
    """

    # Tolerancias en segundos
    PERFECT_TOLERANCE = 0.10
    GOOD_TOLERANCE = 0.20
    OK_TOLERANCE = 0.35

    def __init__(self):
        pass

    def classify_error(self, error):
        """
        Clasifica un golpe según su diferencia temporal
        respecto al tiempo esperado.
        """

        error = abs(error)

        if error <= self.PERFECT_TOLERANCE:
            return "Perfect"

        if error <= self.GOOD_TOLERANCE:
            return "Good"

        if error <= self.OK_TOLERANCE:
            return "Ok"

        return "Miss"

    def evaluate(self, expected_times, actual_times):
        """
        Compara los tiempos esperados con los tiempos
        realizados por el niño.

        Devuelve un resumen del desempeño.
        """

        expected_times = list(expected_times)
        actual_times = list(actual_times)

        matched = []
        used_actual = set()

        # Buscar para cada golpe esperado el golpe real
        # más cercano que todavía no haya sido utilizado.
        for expected_index, expected in enumerate(expected_times):

            best_index = None
            best_error = None

            for actual_index, actual in enumerate(actual_times):

                if actual_index in used_actual:
                    continue

                error = abs(actual - expected)

                if best_error is None or error < best_error:
                    best_error = error
                    best_index = actual_index

            if best_index is not None:
                used_actual.add(best_index)

                judgement = self.classify_error(best_error)

                matched.append({
                    "expected": expected,
                    "actual": actual_times[best_index],
                    "error": round(best_error, 4),
                    "judgement": judgement
                })

        perfect = sum(
            1 for item in matched
            if item["judgement"] == "Perfect"
        )

        good = sum(
            1 for item in matched
            if item["judgement"] == "Good"
        )

        ok = sum(
            1 for item in matched
            if item["judgement"] == "Ok"
        )

        miss = sum(
            1 for item in matched
            if item["judgement"] == "Miss"
        )

        expected_count = len(expected_times)
        actual_count = len(actual_times)

        missed_hits = max(
            expected_count - len(matched),
            0
        )

        extra_hits = max(
            actual_count - len(matched),
            0
        )

        errors = [
            item["error"]
            for item in matched
        ]

        average_error = (
            sum(errors) / len(errors)
            if errors else 0.0
        )

        # La precisión se basa en la cercanía temporal.
        if expected_count == 0:
            accuracy = 0.0
        else:
            weighted_score = (
                perfect * 1.0
                + good * 0.8
                + ok * 0.5
            )

            accuracy = (
                weighted_score / expected_count
            ) * 100

        return {
            "expected_hits": expected_count,
            "actual_hits": actual_count,
            "matched_hits": len(matched),
            "perfect": perfect,
            "good": good,
            "ok": ok,
            "miss": miss,
            "missed_hits": missed_hits,
            "extra_hits": extra_hits,
            "average_error": round(average_error, 4),
            "accuracy": round(accuracy, 1),
            "details": matched
        }