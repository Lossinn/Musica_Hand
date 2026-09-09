# main.py

# pyrefly: ignore [missing-import]
import pygame 
from src.game import MusicHandApp

if __name__ == "__main__":
    pygame.init()
    try:
        pygame.mixer.init()
    except Exception as e:
        print(f"Advertencia: no se pudo inicializar el audio: {e}")
    app = MusicHandApp()
    app.run()