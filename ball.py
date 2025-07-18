#esta es la pelota del juego que destruye los bloques
import pygame
import random
from config import WHITE, WIDTH, HEIGHT

class Ball(pygame.sprite.Sprite):
    def __init__(self, paddle, blocks, all_sprites, balls):
        super().__init__()
        self.image = pygame.Surface((15, 15), pygame.SRCALPHA)
        pygame.draw.circle(self.image, WHITE, (7, 7), 7)
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.velocity = [random.choice([-4, 4]), -4]
        self.speed_multiplier = 1.0
        self.paddle = paddle
        self.blocks = blocks
        self.all_sprites = all_sprites
        self.balls = balls

    def update(self): #con esto le damos velocidad a la pelota 
        self.rect.x += int(self.velocity[0] * self.speed_multiplier)
        self.rect.y += int(self.velocity[1] * self.speed_multiplier)

        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.velocity[0] *= -1
        if self.rect.top <= 0:
            self.velocity[1] *= -1
        if self.rect.bottom >= HEIGHT:
            self.kill()
            return

        if self.rect.colliderect(self.paddle.rect):
            self.velocity[1] *= -1

        hit_block = pygame.sprite.spritecollideany(self, self.blocks)
        if hit_block:
            color = hit_block.color
            hit_block.kill() #si destruye un bloque, rebota y se acelera
            self.velocity[1] *= -1
            self.speed_multiplier += 0.1

            if color == 'yellow': #si pega en un bloque amarillo
                new_ball = Ball(self.paddle, self.blocks, self.all_sprites, self.balls)
                self.all_sprites.add(new_ball)
                self.balls.add(new_ball) #nueva pelota
