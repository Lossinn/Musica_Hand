# src/constants.py

import pygame 

# --- Colores ---
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
AZUL = (70, 130, 180)
VERDE = (34, 139, 34)
LIGHT_GREEN = (144, 238, 144)
ROJO = (220, 20, 60)
ORO = (255, 215, 0)
LIGHT_BLUE = (173, 216, 230)
DARK_BLUE = (25, 25, 112)
NARANJA = (255, 165, 0)
PURPURA = (147, 112, 219)

# --- Configuración de Pantalla ---
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
FPS = 60

# --- Estados del Juego ---
class GameState:
    WELCOME = 'welcome'
    MAIN_MENU = 'main_menu'
    TUTORIAL = 'tutorial'
    CALIBRATE_STAFF = 'calibrate_staff'
    FREE_PLAY = 'free_play'
    MINIGAME = 'minigame'
    REACTION_GAME = 'reaction_game'
    SETTINGS = 'settings'
    SONG_SELECT = 'song_select'   # <--- NUEVO
    RESULTS = 'results'


# --- Notas Musicales (Octava Reducida) ---
# Nos quedamos solo con la octava de DO3 a DO4
NOTES = ["DO3", "RE3", "MI3", "FA3", "SOL3", "LA3", "SI3", "DO4"]

NOTE_POSITIONS = {
    "DO3": SCREEN_HEIGHT * 0.73,  # Línea imaginaria debajo
    "RE3": SCREEN_HEIGHT * 0.69,  # Espacio
    "MI3": SCREEN_HEIGHT * 0.65,  # Línea 1
    "FA3": SCREEN_HEIGHT * 0.61,  # Espacio
    "SOL3": SCREEN_HEIGHT * 0.57, # Línea 2
    "LA3": SCREEN_HEIGHT * 0.53,  # Espacio
    "SI3": SCREEN_HEIGHT * 0.49,  # Línea 3
    "DO4": SCREEN_HEIGHT * 0.45,  # Espacio
}