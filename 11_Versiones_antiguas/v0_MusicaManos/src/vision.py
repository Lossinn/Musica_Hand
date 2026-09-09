# src/vision.py

# pyrefly: ignore [missing-import]
import mediapipe as mp
import numpy as np
import os
import time
import json
from .constants import *

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CONFIG_PATH = os.path.normpath(
    os.path.join(
        BASE_DIR,
        '..',
        'data',
        'pentagrama_calibrado.json'
    )
)


# ============================================================
#   DETECTOR DE MANOS
# ============================================================

class MediaPipeHandDetector:
    def __init__(self, detection_conf=0.65, tracking_conf=0.5):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False, max_num_hands=2,
            min_detection_confidence=detection_conf,
            min_tracking_confidence=tracking_conf,
        )
        self.mp_drawing = mp.solutions.drawing_utils

    def detect_hands(self, frame_rgb, draw_landmarks=True):
        results = self.hands.process(frame_rgb)
        hands_data = []

        if results.multi_hand_landmarks:
            for hand_landmarks, handedness in zip(
                results.multi_hand_landmarks,
                results.multi_handedness
            ):
                label = handedness.classification[0].label
                wrist = hand_landmarks.landmark[self.mp_hands.HandLandmark.WRIST]

                # Normalización
                landmarks = [
                    [lm.x - wrist.x, lm.y - wrist.y, lm.z - wrist.z]
                    for lm in hand_landmarks.landmark
                ]

                hands_data.append({
                    'landmarks': landmarks,
                    'hand_label': label,
                    'raw_landmarks': hand_landmarks
                })

                if draw_landmarks:
                    self.mp_drawing.draw_landmarks(
                        frame_rgb, hand_landmarks, self.mp_hands.HAND_CONNECTIONS
                    )

        return hands_data, frame_rgb


# ============================================================
#   RECONOCEDOR DE GESTOS
# ============================================================

class HandGestureRecognizer:
    def __init__(self):
        self.templates = {}

        # --- SOLO UN UMBRAL GLOBAL ---
        self.global_threshold = 0.65   # AJÚSTALO SI QUIERES MÁS PRECISIÓN

        self.load_templates()

    def load_templates(self):
        try:
            with open(CONFIG_PATH, "r") as f:
                self.templates = json.load(f)
                print("✅ Reconocedor listo con plantillas personalizadas.")
        except:
            print("⚠️ El reconocedor necesita plantillas. Por favor, calibra primero.")

    def _prepare_vector(self, hands_data):
        vector = []
        for hand in sorted(hands_data, key=lambda h: h['hand_label']):
            for lm in hand['landmarks']:
                vector.extend(lm)
        return np.array(vector)

    def recognize_gesture(self, hands_data):
        if not hands_data or len(hands_data) < 2:
            return None
        if not self.templates:
            return None

        live_vector = self._prepare_vector(hands_data)
        if live_vector.size == 0:
            return None

        best_match = None
        highest_similarity = -1

        for note, template in self.templates.items():
            template_vector = self._prepare_vector(template["hands"])
            if template_vector.size == 0:
                continue

            if live_vector.shape != template_vector.shape:
                continue

            live_norm = np.linalg.norm(live_vector)
            temp_norm = np.linalg.norm(template_vector)
            if live_norm == 0 or temp_norm == 0:
                continue

            similarity = np.dot(live_vector, template_vector) / (live_norm * temp_norm)

            if similarity > highest_similarity:
                highest_similarity = similarity
                best_match = note

        # --- UMBRAL DE VALIDACIÓN ---
        if highest_similarity < self.global_threshold:
            return None

        return best_match

    def gesture_to_note(self, gesture):
        return gesture


# ============================================================
#   CALIBRADOR DEL PENTAGRAMA
# ============================================================

class StaffCalibrator:
    def __init__(self, notes_list):
        self.notes = notes_list
        self.points = {}
        self.current_note_index = 0
        self.is_calibrating = False
        self.feedback = ""
        self.feedback_timer = 0
        self.calibrated = False
        self.load_calibration()

    def load_calibration(self):
        try:
            with open(CONFIG_PATH, "r") as f:
                self.points = json.load(f)
                if self.points:
                    self.calibrated = True
                    print("✅ ¡Plantillas de gestos cargadas exitosamente!")
        except:
            print("ℹ️ No se encontraron plantillas de gestos. Se necesita calibrar.")

    def set_feedback(self, msg, duration=3):
        self.feedback = msg
        self.feedback_timer = time.time() + duration

    def start(self):
        self.is_calibrating = True
        self.calibrated = False
        self.current_note_index = 0
        self.points = {}
        self.set_feedback(
            f"Prepara la seña para: {self.notes[self.current_note_index]} y presiona ESPACIO"
        )

    def update(self, hands_data):
        if not self.is_calibrating:
            return

        if not hands_data or len(hands_data) < 2:
            self.set_feedback("Asegúrate de que ambas manos sean visibles", 2)
            return

        note = self.notes[self.current_note_index]

        gesture_data = {
            "hands": [
                {"landmarks": h["landmarks"], "hand_label": h["hand_label"]}
                for h in hands_data
            ],
        }

        self.points[note] = gesture_data
        self.current_note_index += 1

        if self.current_note_index >= len(self.notes):
            self.finish_calibration()
        else:
            next_note = self.notes[self.current_note_index]
            self.set_feedback(f"¡Bien! Ahora la seña para: {next_note}")

    def finish_calibration(self):
        self.is_calibrating = False
        self.calibrated = True
        self.set_feedback("¡Calibración completa y plantillas guardadas!")

        try:
            with open(CONFIG_PATH, "w") as f:
                json.dump(self.points, f, indent=4)
            print(f"💾 Plantillas guardadas en {CONFIG_PATH}")
        except Exception as e:
            print(f"❌ Error al guardar: {e}")

    def draw_feedback(self, screen, font, pos):
        if time.time() < self.feedback_timer:
            txt = font.render(self.feedback, True, ORO)
            rect = txt.get_rect(center=pos)
            screen.blit(txt, rect)