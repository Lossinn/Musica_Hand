# pyrefly: ignore [missing-import]
import pygame

from src.constants import SCREEN_WIDTH


class NoteSprite(pygame.sprite.Sprite):
    def __init__(self, note_name, image, y_position):
        super().__init__()

        self.note_name = note_name
        self.image = image

        # Aparece del lado derecho y se desplaza hacia la zona de acierto
        self.rect = self.image.get_rect(
            center=(SCREEN_WIDTH, y_position)
        )

        self.speed = 4

    def update(self):
        self.rect.x -= self.speed

        if self.rect.right < 0:
            self.kill()