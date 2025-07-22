#barra que le pega a la pelota para romper los bloques
import pygame
import os
from config import BLUE, WIDTH

class Paddle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Ruta a la imagen de la copa
        script_dir = os.path.dirname(__file__)
        image_path = os.path.join(script_dir, "assets", "images", "paddle", "copa.png")

        try:
            loaded_image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(loaded_image, (100, 70))  # podés ajustar alto si querés
            print(f"Imagen del paddle 'copa' cargada correctamente: {image_path}")
        except pygame.error as e:
            print(f"Error al cargar la imagen del paddle: {e}")
            print("Se usará una barra azul por defecto.")
            self.image = pygame.Surface((100, 15))  # si falla, paddle azul
            self.image.fill(BLUE)

        self.rect = self.image.get_rect(midbottom=(WIDTH // 2, 570))  # posicion inicial
        self.speed = 7

    def update(self, keys): #con esto detectamos si nos movemos a la izquierda o a la derecha
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        self.rect.x = max(0, min(WIDTH - self.rect.width, self.rect.x))  # límites de la pantalla
