class RhythmEngine:
    """
    Motor encargado de convertir patrones TA/TITI
    en tiempos rítmicos esperados.
    """

    # TA = un golpe en un pulso
    # TITI = dos golpes dentro de un mismo pulso
    SUBDIVISIONS = {
        "TA": [0.0],
        "TITI": [0.0, 0.5],
    }

    def __init__(self, bpm=60):
        self.set_bpm(bpm)

    def set_bpm(self, bpm):
        """
        Define el tempo en pulsaciones por minuto.
        """
        if bpm <= 0:
            raise ValueError("El BPM debe ser mayor que 0.")

        self.bpm = bpm

        # Duración de un pulso en segundos.
        self.beat_duration = 60.0 / bpm

    def pattern_to_times(self, pattern, repetitions=1):
        """
        Convierte un patrón TA/TITI en una lista
        de tiempos esperados.

        Ejemplo:

        ["TA", "TA", "TITI", "TA"]

        produce:

        [0.0, 1.0, 2.0, 2.5, 3.0]

        usando 60 BPM.
        """

        expected_times = []

        current_beat = 0

        for _ in range(repetitions):

            for figure in pattern:

                if figure not in self.SUBDIVISIONS:
                    raise ValueError(
                        f"Figura rítmica desconocida: {figure}"
                    )

                offsets = self.SUBDIVISIONS[figure]

                for offset in offsets:
                    time_position = (
                        current_beat + offset
                    ) * self.beat_duration

                    expected_times.append(time_position)

                current_beat += 1

        return expected_times

    def get_pattern_duration(self, pattern, repetitions=1):
        """
        Devuelve la duración total esperada del patrón
        en segundos.
        """

        total_beats = len(pattern) * repetitions

        return total_beats * self.beat_duration