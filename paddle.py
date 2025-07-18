#barra que le pega a la pelota para romper los bloques
import pygame
from config import BLUE, WIDTH

class Paddle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((100, 15))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect(midbottom=(WIDTH // 2, 570))
        self.speed = 7

    def update(self, keys): #con esto detectamos si nos movemos a la izquierda oa la derecha
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        self.rect.x = max(0, min(WIDTH - self.rect.width, self.rect.x))
