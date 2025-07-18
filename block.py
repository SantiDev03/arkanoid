#aca estan los bloques que van a ser destuidos
import pygame
from config import CYAN, WHITE, YELLOW
import random

class Block(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((60, 20))
        color_choice = random.choices( #creamos los bloques con colores
            ['cyan', 'white', 'yellow'],
            weights=[5, 5, 1],
            k=1
        )[0]
        self.color = color_choice

        if color_choice == 'cyan':
            self.image.fill(CYAN)
        elif color_choice == 'white':
            self.image.fill(WHITE)
        else:
            self.image.fill(YELLOW)

        self.rect = self.image.get_rect(topleft=(x, y))
