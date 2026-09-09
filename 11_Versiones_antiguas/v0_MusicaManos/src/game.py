# game.py — versión completa con ScoreManager, HUD y Resultados

# pyrefly: ignore [missing-import]
import pygame
import cv2
import sys
import os
import time
import numpy as np
import json
import random
import math

from .constants import *
from .vision import MediaPipeHandDetector, HandGestureRecognizer, StaffCalibrator
from src.core.performance import ScoreManager
from src.core.music import NoteSprite

# ==========================
#        MUSIC HANDS APP
# ==========================
class MusicHandApp:
    def __init__(self):
        pygame.init()
        try:
            pygame.mixer.init()
        except Exception as e:
            print(f"Advertencia: no se pudo inicializar pygame.mixer: {e}")

        self.clock = pygame.time.Clock()
        try:
            icon_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'images', 'mascot.png')
            icon_surface = pygame.image.load(icon_path)
            pygame.display.set_icon(icon_surface)
        except Exception as e:
            print(f"No se pudo cargar el ícono: {e}")

        self.running = True
        self.state = GameState.WELCOME
        self.RESULTS_STATE = GameState.RESULTS

        self.font_large = pygame.font.Font(None, 74)
        self.font_medium = pygame.font.Font(None, 50)
        self.font_small = pygame.font.Font(None, 36)
        self.camera_index = 0

        # Intentamos crear la ventana de vídeo; si falla (entornos sin GUI o sandbox),
        # entramos en modo headless creando una Surface en memoria para evitar excepciones.
        try:
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
            pygame.display.set_caption("Hand Sing Kids!")
            self.headless = False
        except Exception as e:
            print(f"Advertencia: no se pudo crear la ventana de vídeo: {e}. Intentando fallback dummy.")
            # Intentar forzar un driver dummy (headless) para poder usar la lógica sin GUI
            os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')
            try:
                pygame.display.init()
                try:
                    self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
                    pygame.display.set_caption("Hand Sing Kids!")
                    self.headless = False
                except Exception:
                    self.headless = True
                    self.screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            except Exception:
                print("No fue posible inicializar un driver de vídeo; ejecutando completamente en modo headless.")
                self.headless = True
                self.screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

        self.load_config()
        self.images = self.load_images()
        self.sounds = self.load_sounds()
        self.background_music = self.load_background_music()

        try:
            self.hand_detector = MediaPipeHandDetector()
            self.gesture_recognizer = HandGestureRecognizer()
            self.staff_calibrator = StaffCalibrator(NOTES)
        except Exception as e:
            print(f"Advertencia: módulo de visión no disponible: {e}")
            self.hand_detector = None
            self.gesture_recognizer = None
            self.staff_calibrator = None

        self.cap = None
        self.camera_active = False
        self.camera_error = False
        self.init_camera()
        self.hands_data = []
        self.processed_frame = None

        self.player_name = ""
        self.input_text = ""
        self.input_active = True

        self.buttons = {}
        self.create_main_menu_buttons()
        self.close_button_rect = pygame.Rect(SCREEN_WIDTH - 45, 10, 35, 35)

        self.note_sprites = pygame.sprite.Group()
        self.hit_zone = pygame.Rect(100, 0, 20, SCREEN_HEIGHT)

        self.minigame_start_time = 0

        # --- Canciones ---
        self.songs = self.load_songs()
        self.selected_song_id = "original"  
        self.song_sequence = self.songs[self.selected_song_id]["sequence"]
        self.next_note_index = 0


        self.tutorial_step = 0
        self.tutorial_sequence = ["DO3", "RE3", "MI3", "FA3", "SOL3", "LA3", "SI3", "DO4"]
        self.tutorial_feedback = ""
        self.tutorial_feedback_timer = 0
        self.tutorial_retry_button = pygame.Rect(SCREEN_WIDTH // 2 - 350, SCREEN_HEIGHT - 200, 300, 60)
        self.tutorial_menu_button = pygame.Rect(SCREEN_WIDTH // 2 + 50, SCREEN_HEIGHT - 200, 300, 60)

        self.last_note_detected = None
        self.note_cooldown = 0.3
        self.last_note_played_time = 0
        self.last_note_played = None

        self.volume = 0.5  # 0.0 a 1.0
        self.show_camera_feed = True
        self.show_hand_landmarks = True
        self.is_waiting_for_input = False

        # variables juego de reacción
        self.reaction_game_current_target_note = None
        self.reaction_game_start_time = 0
        self.reaction_game_countdown_active = False
        self.reaction_game_current_countdown = 0
        self.reaction_game_last_note_time = 0
        self.reaction_game_feedback_icon = None
        self.reaction_game_feedback_timer = 0
        self.reaction_game_note_display_duration = 2
        self.reaction_game_pause_between_notes = 1

        # ----- Sistema de puntuación -----
        self.score_manager = ScoreManager()
        self.last_judgement_text = ""
        self.last_judgement_until = 0  # timestamp para mostrar el feedback

        # ----- Resultados -----
        self.results_summary = None
        self.results_mode = None
        self.results_is_new_record = False
        self.results_retry_button = pygame.Rect(SCREEN_WIDTH//2 - 330, SCREEN_HEIGHT - 200, 300, 70)
        self.results_menu_button  = pygame.Rect(SCREEN_WIDTH//2 +  30, SCREEN_HEIGHT - 200, 300, 70)

        # Reacción: rondas
        self.reaction_game_rounds_target = 15
        self.reaction_game_rounds_done = 0
        # --- Selector de canciones ---
        self.song_cards = {}
        self.song_preview_buttons = {}

        self.song_back_button = pygame.Rect(SCREEN_WIDTH//2 - 320, SCREEN_HEIGHT - 120, 260, 60)
        self.song_play_button = pygame.Rect(SCREEN_WIDTH//2 +  60, SCREEN_HEIGHT - 120, 260, 60)

        # Canal de preview (si mixer no está inicializado, se ignora al reproducir)
        try:
            self.song_preview_channel = pygame.mixer.Channel(5)
        except Exception:
            self.song_preview_channel = None
        self.song_previews = self.load_song_previews()


    # --------------------------
    #        CARGAS
    # --------------------------
    def load_config(self):
        base_path = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.normpath(os.path.join(base_path, '..', 'config.json'))
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
                self.camera_index = config.get("camera_index", 0)
                print(f"Configuración cargada. Usando índice de cámara: {self.camera_index}")
        except FileNotFoundError:
            print("Advertencia: No se encontró config.json. Usando cámara por defecto (índice 0).")
        except json.JSONDecodeError:
            print("Advertencia: Error al leer config.json. Usando cámara por defecto (índice 0).")

    def load_images(self):
        images = {}
        base_path = os.path.dirname(__file__)
        path = os.path.join(base_path, '..', 'assets', 'images')
        note_size = (90, 90)

        try:
            # Fondos
            for name in ['welcome', 'menu', 'game']:
                bg_path = os.path.join(path, f"{name}_background.png")
                if os.path.exists(bg_path):
                    bg = pygame.image.load(bg_path).convert()
                    images[name] = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

            # Notas para el pentagrama
            notes_in_file = ['DO3', 'RE3', 'MI3', 'FA3', 'SOL3', 'LA3', 'SI3', 'DO4']
            for note in notes_in_file:
                note_path = os.path.join(path, f"{note}.png")
                if os.path.exists(note_path):
                    original_image = pygame.image.load(note_path).convert_alpha()
                    images[note] = pygame.transform.scale(original_image, note_size)
                else:
                    print(f"Advertencia: No se encontró la imagen de nota {note_path}")

            # Señas de manos
            hand_signs = ['do3', 're3', 'mi3', 'fa3', 'sol3', 'la3', 'si3', 'do4']
            for sign in hand_signs:
                sign_path = os.path.join(path, f"sign_{sign}.png")
                if os.path.exists(sign_path):
                    img = pygame.image.load(sign_path).convert_alpha()
                    images[f'sign_{sign}'] = pygame.transform.scale(img, (200, 200))
                else:
                    print(f"Advertencia: No se encontró la imagen de seña en {sign_path}")

            # Otros
            def _opt(imgname):
                p = os.path.join(path, imgname)
                return pygame.image.load(p).convert_alpha() if os.path.exists(p) else None

            images['mascot'] = _opt("mascot.png")
            images['hand_silhouette'] = _opt("hand_silhouette.png")
            images['UNO'] = _opt("UNO.png")
            images['DOS'] = _opt("DOS.png")
            images['TRES'] = _opt("TRES.png")
            images['LISTO'] = _opt("LISTO.png")
            # Miniaturas opcionales para las canciones
            images['song_original'] = _opt("song_original.png")
            images['song_estrellita'] = _opt("song_estrellita.png")


        except pygame.error as e:
            print(f"Error al cargar una imagen: {e}.")
        return images

    def load_sounds(self):
        sounds = {}
        base_path = os.path.dirname(__file__)
        sounds_path = os.path.join(base_path, '..', 'assets', 'sounds')

        for note in NOTES:
            file_path = os.path.join(sounds_path, f"{note}.mp3")
            if os.path.exists(file_path):
                try:
                    sounds[note] = pygame.mixer.Sound(file_path)
                    sounds[note].set_volume(0.8)
                except Exception as e:
                    print(f"Error cargando sonido {file_path}: {e}")
            else:
                print(f"Advertencia: No se encontró el archivo de sonido para {note} en {sounds_path}")
        return sounds

    def load_background_music(self):
        music = {}
        base_path = os.path.dirname(__file__)
        music_path = os.path.join(base_path, '..', 'assets', 'sounds')
        try:
            music['welcome_music'] = os.path.join(music_path, "sonido_fondo_1.mp3")
            music['menu_music'] = os.path.join(music_path, "sonido_fondo_2.mp3")
            for key, p in list(music.items()):
                if not os.path.exists(p):
                    print(f"Advertencia: No se encontró el archivo de música: {p}")
                    music[key] = None
        except Exception as e:
            print(f"Error al cargar la música: {e}")
        return music

    def load_songs(self):
        """
        Carga todas las canciones disponibles desde data/songs.json.

        Cada canción contiene:
          - title: nombre visible
          - difficulty: texto de dificultad
          - preview_file: archivo opcional de preview
          - sequence: lista de [nota, tiempo_spawn]
        """

        base_path = os.path.dirname(os.path.abspath(__file__))

        songs_path = os.path.normpath(
            os.path.join(
                base_path,
                '..',
                'data',
                'songs.json'
            )
        )

        try:
            with open(songs_path, "r", encoding="utf-8") as f:
                songs = json.load(f)

            print(f"Canciones cargadas correctamente: {len(songs)}")

            return songs

        except FileNotFoundError:
            print("Error: No se encontró data/songs.json")
            return {}

        except json.JSONDecodeError:
            print("Error: data/songs.json no contiene un JSON válido")
            return {}

    def load_song_previews(self):
        """
        Intenta cargar archivos de preview de cada canción.
        No son obligatorios: si no existen, sólo se muestra un print.
        """
        previews = {}
        base_path = os.path.dirname(__file__)
        sounds_path = os.path.join(base_path, '..', 'assets', 'sounds')

        for song_id, info in self.songs.items():
            filename = info.get("preview_file")
            if not filename:
                continue  # esta canción no tiene preview configurado

            full_path = os.path.join(sounds_path, filename)
            if not os.path.exists(full_path):
                print(f"(Info) Sin preview para canción '{song_id}': {full_path} no existe")
                continue

            try:
                snd = pygame.mixer.Sound(full_path)
                snd.set_volume(self.volume)
                previews[song_id] = snd
            except Exception as e:
                print(f"Error cargando preview de '{song_id}' ({full_path}): {e}")

        return previews


    # --------------------------
    #      CICLO PRINCIPAL
    # --------------------------
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.play_music_for_state()
            self.clock.tick(FPS)
        self.cleanup()

    def handle_events(self):
        # En modo headless evitamos usar `pygame.event.get()` (puede fallar si no hay driver)
        if getattr(self, 'headless', False):
            try:
                pygame.event.pump()
            except Exception:
                pass
            return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.close_button_rect.collidepoint(event.pos):
                    self.running = False

            if self.state == GameState.WELCOME:
                self.handle_welcome_events(event)
            elif self.state == GameState.MAIN_MENU:
                self.handle_menu_events(event)
            elif self.state == GameState.SONG_SELECT:           # <--- NUEVO
                self.handle_song_select_events(event)           # <--- NUEVO
            elif self.state == GameState.TUTORIAL:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.state = GameState.MAIN_MENU
            elif self.state == GameState.CALIBRATE_STAFF:
                self.handle_calibration_events(event)
            elif self.state == GameState.FREE_PLAY:
                self.handle_free_play_events(event)
            elif self.state == GameState.MINIGAME:
                self.handle_minigame_events(event)
            elif self.state == GameState.REACTION_GAME:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    # Terminar mostrando resultados
                    self.go_to_results("Juego de Reacción")
            elif self.state == self.RESULTS_STATE:
                self.handle_results_events(event)
    # --------------------------
    #   SELECTOR DE CANCIÓN
    # --------------------------
    def create_song_cards(self):
        """
        Calcula la posición de cada tarjeta de canción.
        """
        cards = {}
        total = len(self.songs)
        if total == 0:
            return cards

        card_w, card_h = 280, 360
        spacing = 40
        total_w = total * card_w + (total - 1) * spacing
        start_x = (SCREEN_WIDTH - total_w) // 2
        y = SCREEN_HEIGHT // 2 - card_h // 2

        for idx, song_id in enumerate(self.songs.keys()):
            x = start_x + idx * (card_w + spacing)
            cards[song_id] = pygame.Rect(x, y, card_w, card_h)

        return cards

    def play_song_preview(self, song_id):
        """
        Reproduce la vista previa de una canción, si existe.
        """
        snd = self.song_previews.get(song_id)
        if not snd:
            print(f"(Info) Sin preview de audio para canción '{song_id}'")
            return
        try:
            self.song_preview_channel.stop()
            self.song_preview_channel.play(snd)
        except Exception as e:
            print(f"Error reproduciendo preview de '{song_id}': {e}")

    def stop_song_preview(self):
        """
        Detiene cualquier preview que esté sonando.
        """
        try:
            self.song_preview_channel.stop()
        except Exception:
            pass

    def draw_song_select_screen(self):
        self.screen.fill(DARK_BLUE)

        self.draw_text("Selecciona una canción", self.font_large, ORO,
                       (SCREEN_WIDTH // 2, 100))

        mouse_pos = pygame.mouse.get_pos()
        self.song_preview_buttons = {}

        for song_id, card_rect in self.song_cards.items():
            info = self.songs.get(song_id, {})
            title = info.get("title", song_id)
            difficulty = info.get("difficulty", "N/A")

            # Color base de la tarjeta
            if song_id == self.selected_song_id:
                base_color = LIGHT_BLUE
            else:
                base_color = AZUL

            pygame.draw.rect(self.screen, base_color, card_rect, border_radius=16)
            pygame.draw.rect(self.screen, BLANCO, card_rect, 3, border_radius=16)

            # Miniatura (opcional)
            thumb_key = f"song_{song_id}"
            thumb = self.images.get(thumb_key)
            if thumb:
                thumb_h = 120
                aspect = thumb.get_width() / thumb.get_height()
                thumb_w = int(thumb_h * aspect)
                thumb_surf = pygame.transform.scale(thumb, (thumb_w, thumb_h))
                thumb_rect = thumb_surf.get_rect(midtop=(card_rect.centerx, card_rect.top + 20))
                self.screen.blit(thumb_surf, thumb_rect)
            else:
                # Placeholder si no hay imagen
                ph_rect = pygame.Rect(0, 0, 180, 120)
                ph_rect.midtop = (card_rect.centerx, card_rect.top + 20)
                pygame.draw.rect(self.screen, (30, 30, 80), ph_rect, border_radius=8)
                self.draw_text("Sin imagen", self.font_small, BLANCO, ph_rect.center)

            # Título
            self.draw_text(title, self.font_small, BLANCO,
                           (card_rect.centerx, card_rect.top + 170))

            # Dificultad
            self.draw_text(f"Dificultad: {difficulty}", self.font_small, LIGHT_GREEN,
                           (card_rect.centerx, card_rect.top + 210))

            # Botón de vista previa dentro de la tarjeta
            preview_rect = pygame.Rect(card_rect.centerx - 90, card_rect.bottom - 80, 180, 40)
            self.song_preview_buttons[song_id] = preview_rect
            self.draw_button("▶ Vista previa", preview_rect)

        # Botones inferiores
        self.draw_button("Volver", self.song_back_button)
        self.draw_button("Jugar", self.song_play_button)

        self.draw_text("Haz clic en una tarjeta para seleccionarla.",
                       self.font_small, BLANCO,
                       (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 160))

        self.draw_text("Luego pulsa 'Jugar' para empezar.",
                       self.font_small, BLANCO,
                       (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 130))

        self.draw_text("ESC para volver al menú",
                       self.font_small, BLANCO,
                       (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60))

    def handle_song_select_events(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.stop_song_preview()
            self.state = GameState.MAIN_MENU
            return

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos

            # Selección de tarjeta
            for song_id, rect in self.song_cards.items():
                if rect.collidepoint(pos):
                    self.selected_song_id = song_id

            # Preview
            for song_id, rect in self.song_preview_buttons.items():
                if rect.collidepoint(pos):
                    self.play_song_preview(song_id)

            # Botón Jugar
            if self.song_play_button.collidepoint(pos):
                self.start_minigame()

            # Botón Volver
            if self.song_back_button.collidepoint(pos):
                self.stop_song_preview()
                self.state = GameState.MAIN_MENU


    def update(self):
        # Procesa cámara siempre para mantener el flujo activo (evita congelamientos en Mac)
        if self.camera_active:
            self.process_camera_frame()

        # Lógica por estado
        if self.state == GameState.TUTORIAL:
            self.update_tutorial()
        elif self.state == GameState.MINIGAME:
            self.update_minigame()
        elif self.state == GameState.FREE_PLAY:
            self.update_free_play()
        elif self.state == GameState.REACTION_GAME:
            self.update_reaction_game()

    def draw(self):
        self.screen.fill(DARK_BLUE)

        if self.state == GameState.WELCOME:
            self.draw_welcome_screen()

        elif self.state == GameState.MAIN_MENU:
            self.draw_main_menu_screen()

        elif self.state == GameState.SONG_SELECT:          # <--- NUEVO
            self.draw_song_select_screen()                 # <--- NUEVO

        elif self.state == GameState.TUTORIAL:
            self.draw_tutorial_screen()

        elif self.state == GameState.CALIBRATE_STAFF:
            self.draw_calibrate_screen()

        elif self.state == GameState.FREE_PLAY:
            self.draw_free_play_screen()

        elif self.state == GameState.MINIGAME:
            self.draw_minigame_screen()

        elif self.state == GameState.REACTION_GAME:
            self.draw_reaction_game_screen()

        elif self.state == self.RESULTS_STATE:
            self.draw_results_screen()

        # Botón cerrar
        pygame.draw.rect(self.screen, ROJO, self.close_button_rect, border_radius=8)
        self.draw_text("X", self.font_small, BLANCO, self.close_button_rect.center, shadow=False)

        if not getattr(self, 'headless', False):
            pygame.display.flip()

    # --------------------------
    #   CÁMARA Y BIENVENIDA
    # --------------------------
    def init_camera(self):
        cap = cv2.VideoCapture(self.camera_index)
        if cap.isOpened():
            self.cap = cap
            self.camera_active = True
            self.camera_error = False
            print(f"Cámara abierta con éxito en el índice {self.camera_index}")
            return
        self.camera_error = True
        print(f"Error: No se pudo abrir la cámara en el índice {self.camera_index}.")

    def process_camera_frame(self):
        if not self.cap or not self.cap.isOpened():
            return
        if not self.hand_detector:
            return
        ret, frame = self.cap.read()
        if not ret:
            return
        frame = cv2.flip(frame, 1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.hands_data, self.processed_frame = self.hand_detector.detect_hands(frame_rgb, self.show_hand_landmarks)

    def handle_welcome_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            input_rect = pygame.Rect(SCREEN_WIDTH // 2 - 200, 450, 400, 50)
            if input_rect.collidepoint(event.pos):
                self.input_active = True
            else:
                self.input_active = False
        if self.input_active and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and self.input_text.strip():
                self.player_name = self.input_text.strip()
                self.state = GameState.MAIN_MENU
            elif event.key == pygame.K_BACKSPACE:
                self.input_text = self.input_text[:-1]
            else:
                self.input_text += event.unicode

    def draw_welcome_screen(self):
        if self.images.get('welcome'):
            self.screen.blit(self.images.get('welcome'), (0, 0))
        mascot_img = self.images.get('mascot')
        if mascot_img:
            mascot_size = (300, 300)
            scaled_mascot = pygame.transform.scale(mascot_img, mascot_size)
            mascot_rect = scaled_mascot.get_rect(center=(SCREEN_WIDTH // 2, 180))
            self.screen.blit(scaled_mascot, mascot_rect)
        self.draw_text("¡Bienvenido a Hand Sing Kids!", self.font_large, DARK_BLUE, (SCREEN_WIDTH // 2, 350))
        self.draw_text("Ingresa tu nombre:", self.font_medium, DARK_BLUE, (SCREEN_WIDTH // 2, 420))
        input_rect = pygame.Rect(SCREEN_WIDTH // 2 - 200, 450, 400, 50)
        pygame.draw.rect(self.screen, BLANCO, input_rect, border_radius=10)
        border_color = AZUL if self.input_active else NEGRO
        pygame.draw.rect(self.screen, border_color, input_rect, 3, border_radius=10)
        self.draw_text(self.input_text, self.font_small, NEGRO, input_rect.center, shadow=False)
        self.draw_text("Presiona ENTER para continuar", self.font_small, LIGHT_GREEN, (SCREEN_WIDTH // 2, 520))

    # --------------------------
    #         MENÚ
    # --------------------------
    def create_main_menu_buttons(self):
        button_center_x = SCREEN_WIDTH * 0.8
        button_width = 300
        start_x = button_center_x - (button_width / 2)
        self.buttons['calibrate']      = pygame.Rect(start_x, 120, button_width, 60)
        self.buttons['tutorial']       = pygame.Rect(start_x, 210, button_width, 60)
        self.buttons['minigame']       = pygame.Rect(start_x, 300, button_width, 60)
        self.buttons['reaction_game']  = pygame.Rect(start_x, 390, button_width, 60)
        self.buttons['free_play']      = pygame.Rect(start_x, 480, button_width, 60)
        self.buttons['settings']       = pygame.Rect(start_x, 570, button_width, 60)
        self.buttons['quit']           = pygame.Rect(start_x, 660, button_width, 60)

    def draw_main_menu_screen(self):
        if self.images.get('menu'):
            self.screen.blit(self.images.get('menu'), (0, 0))
        mascot_img = self.images.get('mascot')
        if mascot_img:
            mascot_rect = mascot_img.get_rect(center=(SCREEN_WIDTH // 4, 350))
            self.screen.blit(mascot_img, mascot_rect)
        saludo = f"¡Hola, {self.player_name}!" if self.player_name else "¡Hola!"
        self.draw_text(saludo, self.font_large, ORO, (SCREEN_WIDTH // 2, 80))
        self.draw_text("Ahora, selecciona una opción", self.font_medium, BLANCO, (SCREEN_WIDTH // 4, SCREEN_HEIGHT - 100))

        self.draw_button("Calibrar Manos", self.buttons['calibrate'])
        self.draw_button("Aprender Señas", self.buttons['tutorial'])
        self.draw_button("Notas Rítmicas", self.buttons['minigame'])
        self.draw_button("Juego de Reacción", self.buttons['reaction_game'])
        self.draw_button("Uso Libre", self.buttons['free_play'])
        self.draw_button("Configuración", self.buttons['settings'])
        self.draw_button("Salir", self.buttons['quit'])

    def handle_menu_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.buttons['calibrate'].collidepoint(event.pos):
                if self.staff_calibrator:
                    self.staff_calibrator.start()
                    self.state = GameState.CALIBRATE_STAFF
                else:
                    print("Advertencia: calibrador no disponible (mediapipe faltante).")
            if self.buttons['tutorial'].collidepoint(event.pos):
                self.start_tutorial()
            if self.buttons['minigame'].collidepoint(event.pos):
                # Abrir pantalla de selección de canción
                self.song_cards = self.create_song_cards()
                self.state = GameState.SONG_SELECT

            if self.buttons['reaction_game'].collidepoint(event.pos):
                self.start_reaction_game()
            if self.buttons['free_play'].collidepoint(event.pos):
                self.state = GameState.FREE_PLAY
            if self.buttons['settings'].collidepoint(event.pos):
                self.state = GameState.SETTINGS
            if self.buttons['quit'].collidepoint(event.pos):
                self.running = False
    # --------------------------
    #   SELECTOR DE CANCIÓN
    # --------------------------
    def create_song_cards(self):
        """
        Calcula la posición de cada tarjeta de canción.
        """
        cards = {}
        total = len(self.songs)
        if total == 0:
            return cards

        card_w, card_h = 280, 360
        spacing = 40
        total_w = total * card_w + (total - 1) * spacing
        start_x = (SCREEN_WIDTH - total_w) // 2
        y = SCREEN_HEIGHT // 2 - card_h // 2

        for idx, song_id in enumerate(self.songs.keys()):
            x = start_x + idx * (card_w + spacing)
            cards[song_id] = pygame.Rect(x, y, card_w, card_h)

        return cards

    def play_song_preview(self, song_id):
        """
        Reproduce la vista previa de una canción, si existe.
        """
        snd = self.song_previews.get(song_id)
        if not snd:
            print(f"(Info) Sin preview de audio para canción '{song_id}'")
            return
        try:
            self.song_preview_channel.stop()
            self.song_preview_channel.play(snd)
        except Exception as e:
            print(f"Error reproduciendo preview de '{song_id}': {e}")

    def stop_song_preview(self):
        """
        Detiene cualquier preview que esté sonando.
        """
        try:
            self.song_preview_channel.stop()
        except Exception:
            pass

    def draw_song_select_screen(self):
        self.screen.fill(DARK_BLUE)

        self.draw_text("Selecciona una canción", self.font_large, ORO,
                       (SCREEN_WIDTH // 2, 100))

        mouse_pos = pygame.mouse.get_pos()
        self.song_preview_buttons = {}

        for song_id, card_rect in self.song_cards.items():
            info = self.songs.get(song_id, {})
            title = info.get("title", song_id)
            difficulty = info.get("difficulty", "N/A")

            # Color base de la tarjeta
            if song_id == self.selected_song_id:
                base_color = LIGHT_BLUE
            else:
                base_color = AZUL

            pygame.draw.rect(self.screen, base_color, card_rect, border_radius=16)
            pygame.draw.rect(self.screen, BLANCO, card_rect, 3, border_radius=16)

            # Miniatura (opcional)
            thumb_key = f"song_{song_id}"
            thumb = self.images.get(thumb_key)
            if thumb:
                thumb_h = 120
                aspect = thumb.get_width() / thumb.get_height()
                thumb_w = int(thumb_h * aspect)
                thumb_surf = pygame.transform.scale(thumb, (thumb_w, thumb_h))
                thumb_rect = thumb_surf.get_rect(midtop=(card_rect.centerx, card_rect.top + 20))
                self.screen.blit(thumb_surf, thumb_rect)
            else:
                # Placeholder si no hay imagen
                ph_rect = pygame.Rect(0, 0, 180, 120)
                ph_rect.midtop = (card_rect.centerx, card_rect.top + 20)
                pygame.draw.rect(self.screen, (30, 30, 80), ph_rect, border_radius=8)
                self.draw_text("Sin imagen", self.font_small, BLANCO, ph_rect.center)

            # Título
            self.draw_text(title, self.font_small, BLANCO,
                           (card_rect.centerx, card_rect.top + 170))

            # Dificultad
            self.draw_text(f"Dificultad: {difficulty}", self.font_small, LIGHT_GREEN,
                           (card_rect.centerx, card_rect.top + 210))

            # Botón de vista previa dentro de la tarjeta
            preview_rect = pygame.Rect(card_rect.centerx - 90, card_rect.bottom - 80, 180, 40)
            self.song_preview_buttons[song_id] = preview_rect
            self.draw_button("▶ Vista previa", preview_rect)

        # Botones inferiores
        self.draw_button("Volver", self.song_back_button)
        self.draw_button("Jugar", self.song_play_button)

        self.draw_text("Haz clic en una tarjeta para seleccionarla.",
                       self.font_small, BLANCO,
                       (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 160))

        self.draw_text("Luego pulsa 'Jugar' para empezar.",
                       self.font_small, BLANCO,
                       (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 130))

        self.draw_text("ESC para volver al menú",
                       self.font_small, BLANCO,
                       (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60))

    def handle_song_select_events(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.stop_song_preview()
            self.state = GameState.MAIN_MENU
            return

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos

            # Selección de tarjeta
            for song_id, rect in self.song_cards.items():
                if rect.collidepoint(pos):
                    self.selected_song_id = song_id

            # Preview
            for song_id, rect in self.song_preview_buttons.items():
                if rect.collidepoint(pos):
                    self.play_song_preview(song_id)

            # Botón Jugar
            if self.song_play_button.collidepoint(pos):
                self.start_minigame()

            # Botón Volver
            if self.song_back_button.collidepoint(pos):
                self.stop_song_preview()
                self.state = GameState.MAIN_MENU


    # --------------------------
    #       CALIBRACIÓN
    # --------------------------
    def draw_calibrate_screen(self):
        if self.camera_error:
            self.draw_camera_error()
            return
        if self.processed_frame is not None:
            surf = pygame.surfarray.make_surface(self.processed_frame.swapaxes(0, 1))
            self.screen.blit(surf, (0, 0))
        if self.staff_calibrator:
            self.staff_calibrator.draw_feedback(self.screen, self.font_medium, (SCREEN_WIDTH//2, 50))
        else:
            self.draw_text("Calibrador no disponible (visión deshabilitada)", self.font_medium, ORO, (SCREEN_WIDTH//2, 50))
        self.draw_text("Presiona ESPACIO para capturar la posición de la nota", self.font_small, BLANCO, (SCREEN_WIDTH//2, SCREEN_HEIGHT - 50))
        if self.staff_calibrator.calibrated:
            self.state = GameState.MAIN_MENU

    def handle_calibration_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if self.staff_calibrator:
                    self.staff_calibrator.update(self.hands_data)
                else:
                    print("Advertencia: no se puede calibrar (mediapipe no disponible)")
            elif event.key == pygame.K_ESCAPE:
                if self.staff_calibrator:
                    self.staff_calibrator.is_calibrating = False
                self.state = GameState.MAIN_MENU

    # --------------------------
    #       FREE PLAY
    # --------------------------
    def draw_free_play_screen(self):
        if self.camera_error:
            self.draw_camera_error()
            return

        if self.show_camera_feed and self.processed_frame is not None:
            surf = pygame.surfarray.make_surface(self.processed_frame.swapaxes(0, 1))
            self.screen.blit(surf, (0, 0))

        if not self.hands_data:
            silhouette = self.images.get('hand_silhouette')
            if silhouette:
                s_rect = silhouette.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                self.screen.blit(silhouette, s_rect)

        detected_note = self.last_note_detected
        if detected_note:
            sign_image = self.images.get(f'sign_{detected_note}')
            if sign_image:
                img_scaled = pygame.transform.scale(sign_image, (120, 120))
                sign_rect = img_scaled.get_rect(topright=(SCREEN_WIDTH - 20, 20))
                self.screen.blit(img_scaled, sign_rect)

        self.draw_text("ESC para volver al menú", self.font_small, BLANCO, (SCREEN_WIDTH - 150, SCREEN_HEIGHT - 30))

        if detected_note:
            self.draw_text(f"Nota: {detected_note}", self.font_medium, LIGHT_GREEN, (SCREEN_WIDTH // 2, 50))

    def handle_free_play_events(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.state = GameState.MAIN_MENU

    def update_free_play(self):
        if not self.gesture_recognizer:
            return
        detected_note = self.gesture_recognizer.recognize_gesture(self.hands_data)
        if detected_note:
            if detected_note != self.last_note_played:
                if detected_note in self.sounds:
                    self.sounds[detected_note].play()
                self.last_note_played = detected_note
        else:
            self.last_note_played = None

    # --------------------------
    #       MINIJUEGO
    # --------------------------
    def start_minigame(self):
        if not self.staff_calibrator or not self.staff_calibrator.calibrated:
            print("Error: Debes calibrar las manos primero desde el menú principal.")
            return

        # Asegurar que haya al menos una canción
        if not self.songs:
            print("No hay canciones definidas en self.songs")
            return

        # Cancela cualquier preview
        self.stop_song_preview()

        # Obtener info de la canción seleccionada (o la primera por defecto)
        song_info = self.songs.get(self.selected_song_id)
        if not song_info:
            # fallback: primera canción del diccionario
            first_id = next(iter(self.songs.keys()))
            song_info = self.songs[first_id]
            self.selected_song_id = first_id

        # Secuencia que se usará en el minijuego
        self.song_sequence = song_info["sequence"]

        self.note_sprites.empty()
        self.next_note_index = 0
        self.minigame_start_time = time.time()
        self.state = GameState.MINIGAME

        # Score: nombre incluye canción
        mode_name = f"Notas Rítmicas - {song_info['title']}"
        self.score_manager.start(mode_name)
        self.last_judgement_text = ""
        self.last_judgement_until = 0

        print(f"Minijuego iniciado con canción: {song_info['title']}")


    def update_minigame(self):
        self.note_sprites.update()
        current_time = time.time() - self.minigame_start_time

        # Spawning de notas
        if self.next_note_index < len(self.song_sequence):
            note_name, spawn_time = self.song_sequence[self.next_note_index]
            if current_time >= spawn_time:
                y_pos = NOTE_POSITIONS.get(note_name, SCREEN_HEIGHT * 0.5)
                note_image = self.images.get(note_name)
                if note_image:
                    new_note = NoteSprite(note_name, note_image, y_pos)
                    self.note_sprites.add(new_note)
                self.next_note_index += 1

        # Detección
        detected_note = None
        if self.gesture_recognizer:
            detected_note = self.gesture_recognizer.recognize_gesture(self.hands_data)

        # Puntuación / Miss / Juicio
        for note in list(self.note_sprites):
            # Miss por pasar zona
            if note.rect.right < self.hit_zone.left:
                note.kill()
                self.score_manager.miss()
                self.last_judgement_text = "Miss"
                self.last_judgement_until = time.time() + 0.7
                continue

            # En zona de acierto
            if self.hit_zone.colliderect(note.rect):
                if detected_note == note.note_name:
                    zone_center_x = self.hit_zone.centerx
                    dist = abs(note.rect.centerx - zone_center_x)

                    # Ventanas de juicio
                    if dist <= 12:
                        tier = "Perfect"
                    elif dist <= 28:
                        tier = "Good"
                    else:
                        tier = "Ok"

                    self.score_manager.hit(tier)
                    if note.note_name in self.sounds:
                        self.sounds[note.note_name].play()

                    self.last_judgement_text = tier
                    self.last_judgement_until = time.time() + 0.5

                    note.kill()

        # Fin del minijuego: no quedan por spawnear y no hay sprites
        if self.next_note_index >= len(self.song_sequence) and len(self.note_sprites) == 0:
            self.go_to_results("Notas Rítmicas")
            return

    def draw_minigame_screen(self):
        if self.images.get('game'):
            self.screen.blit(self.images.get('game'), (0, 0))

        # Cámara a la izquierda
        if self.show_camera_feed and self.processed_frame is not None:
            camera_surf = pygame.surfarray.make_surface(self.processed_frame.swapaxes(0, 1))
            camera_rect_w = SCREEN_WIDTH // 2
            camera_rect_h = SCREEN_HEIGHT
            camera_scaled = pygame.transform.scale(camera_surf, (camera_rect_w, camera_rect_h))
            camera_scaled.set_alpha(200)
            self.screen.blit(camera_scaled, (0, 0))

        # Zona de acierto al centro
        hit_zone_width = 20
        self.hit_zone = pygame.Rect(SCREEN_WIDTH // 2, 0, hit_zone_width, SCREEN_HEIGHT)
        pygame.draw.rect(self.screen, LIGHT_GREEN, self.hit_zone, 5, border_radius=10)

        # Notas
        self.note_sprites.draw(self.screen)

        # HUD
        self.draw_hud(top_center=False)

        self.draw_text("ESC para salir", self.font_small, BLANCO, (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))

    def handle_minigame_events(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            # Termina mostrando resultados
            self.go_to_results("Notas Rítmicas")

    # --------------------------
    #     JUEGO DE REACCIÓN
    # --------------------------
    def start_reaction_game(self):
        self.state = GameState.REACTION_GAME

        # Score
        self.score_manager.start("Juego de Reacción")
        self.last_judgement_text = ""
        self.last_judgement_until = 0

        self.reaction_game_current_target_note = None
        self.is_waiting_for_input = False
        self.reaction_game_feedback_icon = None
        self.reaction_game_feedback_timer = 0
        self.reaction_game_start_time = time.time()
        self.reaction_game_countdown_active = True
        self.reaction_game_current_countdown = 3

        self.reaction_game_rounds_target = 15
        self.reaction_game_rounds_done = 0

    def update_reaction_game(self):
        # Cuenta regresiva
        if self.reaction_game_countdown_active:
            elapsed_time = time.time() - self.reaction_game_start_time
            if elapsed_time < 1:
                self.reaction_game_current_countdown = 3
            elif elapsed_time < 2:
                self.reaction_game_current_countdown = 2
            elif elapsed_time < 3:
                self.reaction_game_current_countdown = 1
            else:
                self.reaction_game_countdown_active = False
                self.generate_new_reaction_target_note()
            return

        # Fase activa
        if self.is_waiting_for_input:
            detected_note = None
            if self.gesture_recognizer:
                detected_note = self.gesture_recognizer.recognize_gesture(self.hands_data)

            if detected_note and detected_note == self.reaction_game_current_target_note:
                # Perfect si <= 0.6s, si no Good
                react_time = time.time() - self.reaction_game_last_note_time
                tier = "Perfect" if react_time <= 0.6 else "Good"
                self.score_manager.hit(tier)
                if detected_note in self.sounds:
                    self.sounds[detected_note].play()
                self.last_judgement_text = tier
                self.last_judgement_until = time.time() + 0.6

                self.is_waiting_for_input = False
                self.reaction_game_last_note_time = time.time()
                self.reaction_game_current_target_note = None

            elif time.time() - self.reaction_game_last_note_time > self.reaction_game_note_display_duration:
                self.score_manager.miss()
                self.last_judgement_text = "Miss"
                self.last_judgement_until = time.time() + 0.6

                self.is_waiting_for_input = False
                self.reaction_game_last_note_time = time.time()
                self.reaction_game_current_target_note = None

        # Pausa entre notas -> generar nueva
        elif (not self.is_waiting_for_input
              and self.reaction_game_current_target_note is None
              and time.time() - self.reaction_game_last_note_time > self.reaction_game_pause_between_notes):
            self.generate_new_reaction_target_note()

        # Fin por rondas completadas (y no estamos esperando input)
        if (not self.reaction_game_countdown_active
            and not self.is_waiting_for_input
            and self.reaction_game_rounds_done >= self.reaction_game_rounds_target):
            self.go_to_results("Juego de Reacción")
            return

    def draw_reaction_game_screen(self):
        self.screen.fill(DARK_BLUE)

        if self.show_camera_feed and self.processed_frame is not None:
            surf = pygame.surfarray.make_surface(self.processed_frame.swapaxes(0, 1))
            self.screen.blit(surf, (0, 0))

        # Cuenta regresiva
        if self.reaction_game_countdown_active:
            if self.reaction_game_current_countdown == 3:
                countdown_img = self.images.get('TRES')
            elif self.reaction_game_current_countdown == 2:
                countdown_img = self.images.get('DOS')
            elif self.reaction_game_current_countdown == 1:
                countdown_img = self.images.get('UNO')
            else:
                countdown_img = self.images.get('LISTO')
            if countdown_img:
                img_scaled = pygame.transform.scale(countdown_img, (180, 180))
                img_rect = img_scaled.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                self.screen.blit(img_scaled, img_rect)
        else:
            # Mostrar seña objetivo
            if self.is_waiting_for_input and self.reaction_game_current_target_note:
                target_sign_img = self.images.get(f'sign_{self.reaction_game_current_target_note.lower()}')
                if target_sign_img:
                    img_scaled = pygame.transform.scale(target_sign_img, (300, 300))
                    img_rect = img_scaled.get_rect(midright=(SCREEN_WIDTH - 50, SCREEN_HEIGHT // 2))
                    self.screen.blit(img_scaled, img_rect)

            # Feedback (si tuvieras íconos asignados)
            if self.reaction_game_feedback_icon and time.time() < self.reaction_game_feedback_timer:
                feedback_rect = self.reaction_game_feedback_icon.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                self.screen.blit(self.reaction_game_feedback_icon, feedback_rect)

            self.draw_text("¡Imita la seña!", self.font_large, ORO, (SCREEN_WIDTH // 2, 80))

            # HUD arriba centrado
            self.draw_hud(top_center=True)

        self.draw_text("ESC para volver al menú", self.font_small, BLANCO, (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))

    def generate_new_reaction_target_note(self):
        available_notes = ['DO3', 'RE3', 'MI3', 'FA3', 'SOL3', 'LA3', 'SI3', 'DO4']
        new_note = random.choice(available_notes)
        self.reaction_game_current_target_note = new_note
        self.reaction_game_last_note_time = time.time()
        self.is_waiting_for_input = True
        self.reaction_game_rounds_done += 1

    # --------------------------
    #          TUTORIAL
    # --------------------------
    def start_tutorial(self):
        base_path = os.path.dirname(os.path.abspath(__file__))

        pentagrama_path = os.path.normpath(
            os.path.join(
                base_path,
                '..',
                'data',
                'pentagrama_calibrado.json'
            )
        )

        if not os.path.exists(pentagrama_path):
            print("Error: Primero debes calibrar las manos desde el menú principal.")
            self.state = GameState.MAIN_MENU
            return

        self.tutorial_step = 0
        self.tutorial_state = 'learning'

        self.set_tutorial_feedback(
            "¡Vamos a aprender! Coloca tus manos en la silueta.",
            5
        )

        self.state = GameState.TUTORIAL

    def set_tutorial_feedback(self, message, duration=3):
        self.tutorial_feedback = message
        self.tutorial_feedback_timer = time.time() + duration

    def draw_tutorial_screen(self):
        self.screen.fill(DARK_BLUE)
        if self.processed_frame is not None:
            surf = pygame.surfarray.make_surface(self.processed_frame.swapaxes(0, 1))
            self.screen.blit(surf, (0, 0))
        if getattr(self, 'tutorial_state', 'learning') == 'learning':
            if not self.hands_data:
                silhouette = self.images.get('hand_silhouette')
                if silhouette:
                    s_rect = silhouette.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                    self.screen.blit(silhouette, s_rect)
            if self.tutorial_step < len(self.tutorial_sequence):
                current_note = self.tutorial_sequence[self.tutorial_step]
                sign_image = self.images.get(f'sign_{current_note.lower()}')
                if sign_image:
                    img_scaled = pygame.transform.scale(sign_image, (120, 120))
                    sign_rect = img_scaled.get_rect(topright=(SCREEN_WIDTH - 20, 20))
                    self.screen.blit(img_scaled, sign_rect)
        elif self.tutorial_state == 'finished':
            mascot_img = self.images.get('mascot')
            if mascot_img:
                scaled_mascot = pygame.transform.scale(mascot_img, (300, 300))
                mascot_rect = scaled_mascot.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
                self.screen.blit(scaled_mascot, mascot_rect)
            self.draw_button("Empezar de Nuevo", self.tutorial_retry_button)
            self.draw_button("Volver al Menú", self.tutorial_menu_button)
            self.draw_text("Usa tu dedo índice para seleccionar una opción", self.font_small, BLANCO, (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 250))
        if time.time() < self.tutorial_feedback_timer:
            self.draw_text(self.tutorial_feedback, self.font_medium, ORO, (SCREEN_WIDTH // 2, 80))

    def update_tutorial(self):
        if getattr(self, 'tutorial_state', 'learning') == 'finished':
            fingertip = self.get_fingertip_pos()
            if fingertip:
                if self.tutorial_retry_button.collidepoint(fingertip):
                    self.start_tutorial()
                elif self.tutorial_menu_button.collidepoint(fingertip):
                    self.state = GameState.MAIN_MENU
            return

        if self.tutorial_step >= len(self.tutorial_sequence):
            self.tutorial_state = 'finished'
            self.set_tutorial_feedback("¡Genial!", 10)
            return

        current_note_to_learn = self.tutorial_sequence[self.tutorial_step]
        detected_note = None
        if self.gesture_recognizer:
            detected_note = self.gesture_recognizer.recognize_gesture(self.hands_data)

        if detected_note == current_note_to_learn:
            if current_note_to_learn in self.sounds:
                self.sounds[current_note_to_learn].play()
            self.tutorial_step += 1
            if self.tutorial_step < len(self.tutorial_sequence):
                next_note = self.tutorial_sequence[self.tutorial_step]
                self.set_tutorial_feedback(f"¡Muy bien! Ahora la seña para {next_note}", 5)
            else:
                self.tutorial_state = 'finished'
                self.set_tutorial_feedback("¡Felicidades! ¡Has aprendido todas las señas!", 5)

    # --------------------------
    #       PANTALLA RESULTADOS
    # --------------------------
    def evaluate_rank(self, score: int, *_, **__):
        if score >= 97:
           return "S", 5
        if score >= 92:
           return "A", 4
        if score >= 85:
           return "B", 3
        if score >= 70:
           return "C", 2
        return "D", 1

    def go_to_results(self, mode_name: str):
        """
        Cierra el marcador, guarda highscore y prepara la pantalla de resultados.
        Usa siempre el mode interno del ScoreManager para ser consistente.
        """
        summary = self.score_manager.end()
        self.results_summary = summary

        # El modo real es el que usó ScoreManager.start(...)
        real_mode = summary.get("mode") or mode_name
        self.results_mode = real_mode

        # ¿Nuevo récord?
        hs = self.score_manager.load_highscores().get(real_mode)
        self.results_is_new_record = bool(hs and hs.get("score", 0) == summary["score"])

        self.state = self.RESULTS_STATE


    def draw_stars(self, center, count):
        """
        Dibuja 'count' estrellas llenas (1..5).
        """
        cx, cy = center
        spacing = 60
        for i in range(5):
            x = cx + (i - 2) * spacing
            r_outer, r_inner = 22, 10
            points = []
            for k in range(10):
                ang = -math.pi/2 + k * (math.pi/5)
                r = r_outer if k % 2 == 0 else r_inner
                px = x + int(r * math.cos(ang))
                py = cy + int(r * math.sin(ang))
                points.append((px, py))
            color = LIGHT_GREEN if i < count else (180, 180, 180)
            pygame.draw.polygon(self.screen, color, points)
            pygame.draw.polygon(self.screen, BLANCO, points, 2)

    def draw_results_screen(self):
        bg = self.images.get('menu') or self.images.get('welcome')
        if bg:
            self.screen.blit(bg, (0, 0))
        title = f"Resultados - {self.results_mode or ''}"
        self.draw_text(title, self.font_large, ORO, (SCREEN_WIDTH//2, 100))

        if not self.results_summary:
            self.draw_text("Sin datos", self.font_medium, BLANCO, (SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            return

        sc = self.results_summary["score"]
        acc = self.results_summary["accuracy"]
        mc = self.results_summary["max_combo"]
        dur = self.results_summary["time"]

        rank, stars = self.evaluate_rank(sc, acc, mc)
        self.draw_text(f"Rank: {rank}", self.font_large, LIGHT_GREEN, (SCREEN_WIDTH//2, 200))
        self.draw_stars((SCREEN_WIDTH//2, 260), stars)

        panel = pygame.Rect(SCREEN_WIDTH//2 - 380, 300, 760, 220)
        pygame.draw.rect(self.screen, (0, 0, 0, 140), panel, border_radius=16)
        pygame.draw.rect(self.screen, BLANCO, panel, 2, border_radius=16)

        self.draw_text(f"Puntuación: {sc}", self.font_medium, BLANCO, (SCREEN_WIDTH//2, 340))
        self.draw_text(f"Precisión: {acc}%", self.font_medium, BLANCO, (SCREEN_WIDTH//2, 380))
        self.draw_text(f"Max Combo: {mc}", self.font_medium, BLANCO, (SCREEN_WIDTH//2, 420))
        self.draw_text(f"Tiempo: {dur}s", self.font_medium, BLANCO, (SCREEN_WIDTH//2, 460))

        if self.results_is_new_record:
            self.draw_text("¡Nuevo récord!", self.font_medium, AZUL, (SCREEN_WIDTH//2, 520))

        self.draw_button("Reintentar", self.results_retry_button)
        self.draw_button("Volver al Menú", self.results_menu_button)

        self.draw_text("Usa tu dedo índice para seleccionar o haz clic", self.font_small, BLANCO, (SCREEN_WIDTH//2, SCREEN_HEIGHT - 240))

    def handle_results_events(self, event):
        click_pos = None
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            click_pos = event.pos
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.state = GameState.MAIN_MENU
            return
        else:
            fingertip = self.get_fingertip_pos()
            if fingertip:
                click_pos = fingertip

        if click_pos:
            if self.results_retry_button.collidepoint(click_pos):
                if self.results_mode == "Notas Rítmicas":
                    self.start_minigame()
                elif self.results_mode == "Juego de Reacción":
                    self.start_reaction_game()
            elif self.results_menu_button.collidepoint(click_pos):
                self.state = GameState.MAIN_MENU

    # --------------------------
    #      AJUSTES / HUD
    # --------------------------
    def draw_settings_screen(self):
        self.screen.fill(DARK_BLUE)
        self.draw_text("Configuración", self.font_large, ORO, (SCREEN_WIDTH // 2, 80))

        # Volumen
        self.draw_text("Volumen:", self.font_medium, BLANCO, (SCREEN_WIDTH // 2 - 200, 200))
        volume_down_rect = pygame.Rect(SCREEN_WIDTH // 2 - 50, 185, 40, 40)
        volume_up_rect = pygame.Rect(SCREEN_WIDTH // 2 + 50, 185, 40, 40)
        self.draw_button("-", volume_down_rect)
        self.draw_button("+", volume_up_rect)
        self.draw_text(f"{int(self.volume * 100)}%", self.font_medium, BLANCO, (SCREEN_WIDTH // 2, 205), shadow=False)

        # Cámara
        self.draw_text("Cámara:", self.font_medium, BLANCO, (SCREEN_WIDTH // 2 - 200, 400))
        cameras = self.find_available_cameras()
        camera_text = f"Cámara {self.camera_index}" if cameras else "No hay cámaras"
        self.draw_text(camera_text, self.font_small, BLANCO, (SCREEN_WIDTH // 2, 400))
        camera_rect = pygame.Rect(SCREEN_WIDTH // 2 - 50, 385, 100, 40)
        self.draw_button("Cambiar", camera_rect)

        # Alternar cámara
        self.draw_text("Mostrar cámara:", self.font_medium, BLANCO, (SCREEN_WIDTH // 2 - 200, 500))
        toggle_cam_rect = pygame.Rect(SCREEN_WIDTH // 2, 485, 100, 40)
        toggle_cam_text = "Sí" if self.show_camera_feed else "No"
        self.draw_button(toggle_cam_text, toggle_cam_rect)

        # Alternar landmarks
        self.draw_text("Puntos de referencia:", self.font_medium, BLANCO, (SCREEN_WIDTH // 2 - 200, 600))
        toggle_landmarks_rect = pygame.Rect(SCREEN_WIDTH // 2, 585, 100, 40)
        toggle_landmarks_text = "Sí" if self.show_hand_landmarks else "No"
        self.draw_button(toggle_landmarks_text, toggle_landmarks_rect)

        self.draw_text("ESC para volver al menú", self.font_small, BLANCO, (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))

    def handle_settings_events(self, event):
        mouse_pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos
            volume_down_rect = pygame.Rect(SCREEN_WIDTH // 2 - 50, 185, 40, 40)
            volume_up_rect = pygame.Rect(SCREEN_WIDTH // 2 + 50, 185, 40, 40)
            test_camera_rect = pygame.Rect(SCREEN_WIDTH // 2 - 150, 300, 300, 60)

            if volume_down_rect.collidepoint(mouse_pos):
                self.volume = max(0.0, self.volume - 0.1)
                pygame.mixer.music.set_volume(self.volume)
                for sound in self.sounds.values():
                    sound.set_volume(self.volume)
            elif volume_up_rect.collidepoint(mouse_pos):
                self.volume = min(1.0, self.volume + 0.1)
                pygame.mixer.music.set_volume(self.volume)
                for sound in self.sounds.values():
                    sound.set_volume(self.volume)
            elif test_camera_rect.collidepoint(mouse_pos):
                self.run_camera_test()

        camera_rect = pygame.Rect(SCREEN_WIDTH // 2 - 50, 385, 100, 40)
        if camera_rect.collidepoint(mouse_pos):
            cameras = self.find_available_cameras()
            if cameras:
                current_index_in_list = cameras.index(self.camera_index) if self.camera_index in cameras else -1
                new_index_in_list = (current_index_in_list + 1) % len(cameras)
                self.camera_index = cameras[new_index_in_list]
                self.init_camera()

        toggle_cam_rect = pygame.Rect(SCREEN_WIDTH // 2, 485, 100, 40)
        if toggle_cam_rect.collidepoint(mouse_pos):
            self.show_camera_feed = not self.show_camera_feed

        toggle_landmarks_rect = pygame.Rect(SCREEN_WIDTH // 2, 585, 100, 40)
        if toggle_landmarks_rect.collidepoint(mouse_pos):
            self.show_hand_landmarks = not self.show_hand_landmarks

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.state = GameState.MAIN_MENU

    def draw_hud(self, top_center=False):
        """
        Muestra: Score, Combo, Accuracy y último juicio (Perfect/Good/Ok/Miss).
        Si top_center=True lo centra arriba. Si no, lo muestra a la derecha.
        """
        x = SCREEN_WIDTH // 2 if top_center else SCREEN_WIDTH - 220
        base_y = 30 if top_center else 40

        panel_rect = pygame.Rect(x - 180, base_y - 20, 360, 120)
        pygame.draw.rect(self.screen, (0, 0, 0, 128), panel_rect, border_radius=12)
        pygame.draw.rect(self.screen, BLANCO, panel_rect, 2, border_radius=12)

        self.draw_text(f"Score: {self.score_manager.score}", self.font_small, ORO, (x, base_y))
        self.draw_text(f"Combo: {self.score_manager.combo} (Max {self.score_manager.max_combo})", self.font_small, BLANCO, (x, base_y + 30))
        self.draw_text(f"Accuracy: {self.score_manager.accuracy()}%", self.font_small, LIGHT_GREEN, (x, base_y + 60))

        if time.time() < self.last_judgement_until and self.last_judgement_text:
            color = {"Perfect": LIGHT_GREEN, "Good": AZUL, "Ok": BLANCO, "Miss": ROJO}.get(self.last_judgement_text, BLANCO)
            self.draw_text(self.last_judgement_text, self.font_medium, color, (x, base_y + 110))

    # --------------------------
    #   UTILIDADES / VARIOS
    # --------------------------
    def run_camera_test(self):
        print("Iniciando probador de cámaras...")
        if self.cap:
            self.cap.release()
        index = 0
        test_running = True
        while test_running and index < 10:
            cap = cv2.VideoCapture(index)
            if cap.isOpened():
                print(f"✅ ¡Cámara encontrada en el puerto {index}!")
                while True:
                    ret, frame = cap.read()
                    if not ret:
                        break
                    cv2.putText(frame, f"Puerto: {index}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    cv2.putText(frame, "Presiona 'N' para siguiente, 'Q' para salir", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                    cv2.imshow('Probador de Camaras', frame)
                    key = cv2.waitKey(1) & 0xFF
                    if key == ord('q'):
                        test_running = False
                        break
                    if key == ord('n'):
                        break
                cap.release()
            else:
                print(f"-- No se encontró cámara en el puerto {index}.")
            index += 1
        cv2.destroyAllWindows()
        self.init_camera()
        print("Probador de cámaras cerrado.")

    def draw_camera_error(self):
        self.screen.fill(NEGRO)
        self.draw_text("Error de Cámara", self.font_large, ROJO, (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
        self.draw_text("Revisa la conexión y permisos.", self.font_small, BLANCO, (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 20))

    def draw_text(self, text, font, color, pos, shadow=True):
        text_surf = font.render(text, True, color)
        text_rect = text_surf.get_rect(center=pos)
        if shadow:
            shadow_surf = font.render(text, True, NEGRO)
            self.screen.blit(shadow_surf, (text_rect.x + 2, text_rect.y + 2))
        self.screen.blit(text_surf, text_rect)

    def draw_button(self, text, rect, base_color=AZUL, hover_color=LIGHT_BLUE):
        mouse_pos = pygame.mouse.get_pos()
        is_hovered = rect.collidepoint(mouse_pos)
        color = hover_color if is_hovered else base_color
        pygame.draw.rect(self.screen, color, rect, border_radius=12)
        pygame.draw.rect(self.screen, BLANCO, rect, 3, border_radius=12)
        self.draw_text(text, self.font_medium, BLANCO, rect.center)

    def get_fingertip_pos(self):
        if not self.hands_data:
            return None
        hand_landmarks = self.hands_data[0]['raw_landmarks']
        index_fingertip = hand_landmarks.landmark[8]
        x = int(index_fingertip.x * SCREEN_WIDTH)
        y = int(index_fingertip.y * SCREEN_HEIGHT)
        return (x, y)

    def find_available_cameras(self):
        available_cameras = []
        for i in range(10):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                available_cameras.append(i)
                cap.release()
            else:
                cap.release()
                continue
        return available_cameras

    def play_music_for_state(self):
        if not pygame.mixer.get_init():
            return
        current_music = pygame.mixer.music.get_busy()
        if self.state == GameState.WELCOME and self.background_music.get('welcome_music'):
            if not current_music or pygame.mixer.music.get_volume() == 0:
                pygame.mixer.music.load(self.background_music['welcome_music'])
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(self.volume)
        elif self.state == GameState.MAIN_MENU and self.background_music.get('menu_music'):
            if not current_music or pygame.mixer.music.get_volume() == 0:
                pygame.mixer.music.load(self.background_music['menu_music'])
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(self.volume)
        elif self.state not in [GameState.WELCOME, GameState.MAIN_MENU]:
            if current_music:
                pygame.mixer.music.stop()

    def cleanup(self):
        if self.cap:
            self.cap.release()
        try:
            if pygame.mixer.get_init():
                pygame.mixer.music.stop()
        except Exception:
            pass
        pygame.quit()
        sys.exit()


# Nota: el arranque suele estar en main.py. Si deseas probar directo:
# if __name__ == "__main__":
#     app = MusicHandApp()
#     app.run()
