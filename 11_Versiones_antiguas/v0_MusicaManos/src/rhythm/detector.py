import math
import time
from collections import deque


class ClapDetector:
    """
    Detecta aplausos mediante el movimiento de acercamiento
    de ambas manos.

    Utiliza una pequeña ventana temporal para evitar depender
    de que MediaPipe detecte las dos manos exactamente en el
    instante del contacto.
    """

    def __init__(
        self,
        clap_distance=0.16,
        release_distance=0.22,
        cooldown=0.30,
        history_size=12
    ):
        self.clap_distance = clap_distance
        self.release_distance = release_distance
        self.cooldown = cooldown

        self.state = "OPEN"
        self.last_clap_time = 0.0

        # Historial de observaciones:
        # (timestamp, distancia)
        self.history = deque(maxlen=history_size)

    def _get_wrist_position(self, hand):
        """
        Obtiene la posición normalizada de la muñeca.
        """

        landmarks = hand.get("landmarks")

        if not landmarks:
            return None

        wrist = landmarks[0]

        if len(wrist) < 2:
            return None

        return wrist[0], wrist[1]

    def _calculate_distance(self, hand_a, hand_b):
        """
        Calcula la distancia entre las muñecas de ambas manos.
        """

        pos_a = self._get_wrist_position(hand_a)
        pos_b = self._get_wrist_position(hand_b)

        if pos_a is None or pos_b is None:
            return None

        dx = pos_a[0] - pos_b[0]
        dy = pos_a[1] - pos_b[1]

        return math.sqrt(dx * dx + dy * dy)

    def _get_distance_from_hands(self, hands_data):
        """
        Obtiene exactamente una mano Left y una mano Right.

        Si MediaPipe entrega detecciones duplicadas o varias manos
        con la misma etiqueta, las ignora para evitar falsos
        positivos en el detector rítmico.
        """

        if not hands_data:
            return None

        left_hand = None
        right_hand = None

        for hand in hands_data:

            label = hand.get("hand_label")

            if label == "Left" and left_hand is None:
                left_hand = hand

            elif label == "Right" and right_hand is None:
                right_hand = hand

        # Para calcular el aplauso necesitamos
        # exactamente una mano de cada lado.
        if left_hand is None or right_hand is None:
            return None

        return self._calculate_distance(
            left_hand,
            right_hand
        )

    def update(self, hands_data, timestamp=None):
        """
        Actualiza el detector.

        Devuelve True cuando identifica un nuevo aplauso.
        """

        if timestamp is None:
            timestamp = time.time()

        distance = self._get_distance_from_hands(
            hands_data
        )

        # --------------------------------------------------
        # Tenemos dos manos visibles
        # --------------------------------------------------
        if distance is not None:

            self.history.append(
                (timestamp, distance)
            )

            # ----------------------------------------------
            # ESTADO OPEN
            # ----------------------------------------------
            if self.state == "OPEN":

                # Detectamos que las manos llegaron
                # a una distancia compatible con aplauso.
                if distance <= self.clap_distance:

                    if (
                        timestamp - self.last_clap_time
                        >= self.cooldown
                    ):
                        self.state = "CLAP"
                        self.last_clap_time = timestamp

                        return True

            # ----------------------------------------------
            # ESTADO CLAP
            # ----------------------------------------------
            elif self.state == "CLAP":

                if distance >= self.release_distance:
                    self.state = "OPEN"

        # --------------------------------------------------
        # Solo una mano visible
        # --------------------------------------------------
        else:

            # No borramos el historial.
            # La información anterior sigue siendo útil
            # para reconstruir el movimiento.
            pass

        return False

    def reset(self):
        """
        Reinicia completamente el detector.
        """

        self.state = "OPEN"
        self.last_clap_time = 0.0
        self.history.clear()