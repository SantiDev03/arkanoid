import pygame
import random
import os

class Block(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        script_dir = os.path.dirname(__file__)
        image_dir = os.path.join(script_dir, "assets", "images", "blocks")

        # Elegimos un color aleatoriamente
        color_choice = random.choices(
            ['cyan', 'white', 'yellow'],
            weights=[5, 5, 1],
            k=1
        )[0]
        self.color = color_choice

        # Ruta de imagen según el color 
        image_filename = f"block_{color_choice}.jpg"
        image_path = os.path.join(image_dir, image_filename)

        try:
            loaded_image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(loaded_image, (60, 20))
        except pygame.error as e:
            print(f"Error al cargar imagen {image_filename}: {e}")
            # Si no se puede cargar la imagen, usamos un Surface de color
            fallback_color = {
                'cyan': (0, 255, 255),
                'white': (255, 255, 255),
                'yellow': (255, 255, 0)
            }.get(color_choice, (255, 0, 0))
            self.image = pygame.Surface((60, 20))
            self.image.fill(fallback_color)

        self.rect = self.image.get_rect(topleft=(x, y))
