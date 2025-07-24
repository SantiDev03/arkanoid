import pygame
import sys
import os
import random
from config import WIDTH, HEIGHT, FPS, BLACK
from paddle import Paddle
from ball import Ball
from block import Block

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Argenoid")
clock = pygame.time.Clock()

score = 0
lives = 3
font = pygame.font.SysFont(None, 36)

# Estados del juego
estado = "menu"

# Fuentes
fuente_grande = pygame.font.SysFont("Segoe UI Emoji", 60)
fuente_media = pygame.font.SysFont("Segoe UI Emoji", 40)

# Colores
negro = (0, 0, 0)
oro = (212, 175, 55)
gris_oscuro = (150, 150, 150)

# Soles animados
soles = [[random.randint(0, WIDTH), random.randint(0, HEIGHT), random.randint(3, 5), random.randint(180, 255)] for _ in range(100)]

def dibujar_sol(pantalla, x, y, radio, brillo):
    color = (brillo, max(brillo - 50, 0), 0)
    pygame.draw.circle(pantalla, color, (x, y), radio)
    for i in range(8):
        angulo = i * 45
        dx = int(radio * 1.8 * pygame.math.Vector2(1, 0).rotate(angulo).x)
        dy = int(radio * 1.8 * pygame.math.Vector2(1, 0).rotate(angulo).y)
        pygame.draw.line(pantalla, color, (x, y), (x + dx, y + dy), 1)

def dibujar_soles():
    for sol in soles:
        x, y, radio, brillo = sol
        dibujar_sol(screen, x, y, radio, brillo)
        sol[3] += random.randint(-15, 15)
        sol[3] = max(150, min(255, sol[3]))

def crear_boton(texto, x_center, y_pos, ancho_boton, alto_boton, tam_fuente):
    fuente_boton = pygame.font.SysFont(None, tam_fuente)
    boton_rect = pygame.Rect(0, y_pos, ancho_boton, alto_boton)
    boton_rect.centerx = x_center
    texto_render = fuente_boton.render(texto, True, negro)
    texto_rect = texto_render.get_rect(center=boton_rect.center)
    return boton_rect, texto_render, texto_rect

boton_play_rect, texto_play, rect_texto_play = crear_boton("PLAY", WIDTH // 2, HEIGHT // 2 + 140, 200, 50, 40)
boton_reiniciar_rect, texto_reiniciar, rect_texto_reiniciar = crear_boton("REINICIAR", WIDTH // 2 + 100, HEIGHT // 2 + 200, 180, 40, 30)
boton_salir_rect, texto_salir, rect_texto_salir = crear_boton("SALIR", WIDTH // 2 - 100, HEIGHT // 2 + 200, 160, 40, 35)

texto_titulo_menu = fuente_grande.render("\u2600\ufe0f Bienvenido Argenoid \u2600\ufe0f", True, negro)
rect_titulo_menu = texto_titulo_menu.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 200))
texto_game_over = fuente_grande.render("GAME OVER", True, negro)
rect_game_over = texto_game_over.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 160))

# Assets
script_dir = os.path.dirname(__file__)
background_image = None
try:
    background_image = pygame.image.load(os.path.join(script_dir, "assets", "images", "messi.jpg")).convert()
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
except:
    background_image = None

pelota_ball_image = None
try:
    pelota_ball_image = pygame.image.load(os.path.join(script_dir, "assets", "images", "pelota.png")).convert_alpha()
    pelota_ball_image = pygame.transform.scale(pelota_ball_image, (35, 35))
except:
    pelota_ball_image = None

hit_ball_in_block = None
try:
    hit_ball_in_block = pygame.mixer.Sound(os.path.join(script_dir, "assets", "sounds", "arkanoid-sfx-1-101soundboards.mp3"))
except:
    hit_ball_in_block = None

try:
    pygame.mixer.music.load(os.path.join(script_dir, "assets", "sounds", "himno-nacional-argentino.wav"))
    pygame.mixer.music.play(-1)
except:
    pass

# Grupos
all_sprites = pygame.sprite.Group()
blocks = pygame.sprite.Group()
balls = pygame.sprite.Group()

paddle = Paddle()
all_sprites.add(paddle)

for row in range(5):
    for col in range(10):
        block = Block(60 + col * 70, 40 + row * 30)
        all_sprites.add(block)
        blocks.add(block)

ball = Ball(paddle, blocks, all_sprites, balls, ball_image=pelota_ball_image, hit_sound=hit_ball_in_block)
all_sprites.add(ball)
balls.add(ball)

running = True
while running:
    clock.tick(FPS)
    keys = pygame.key.get_pressed()
    mouse_pos = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if estado == "menu":
        screen.blit(background_image, (0, 0)) if background_image else screen.fill(BLACK)
        dibujar_soles()
        screen.blit(texto_titulo_menu, rect_titulo_menu)
        color_play = gris_oscuro if boton_play_rect.collidepoint(mouse_pos) else oro
        pygame.draw.rect(screen, color_play, boton_play_rect, border_radius=10)
        screen.blit(texto_play, rect_texto_play)
        if boton_play_rect.collidepoint(mouse_pos) and click[0]:
            estado = "jugando"
            score = 0
            lives = 3

    elif estado == "jugando":
        paddle.update(keys)
        for ball in list(balls):
            result = ball.update()
            if result == 'block_destroyed':
                score += 10

        if len(balls) == 0:
            lives -= 1
            if lives > 0:
                new_ball = Ball(paddle, blocks, all_sprites, balls, ball_image=pelota_ball_image, hit_sound=hit_ball_in_block)
                all_sprites.add(new_ball)
                balls.add(new_ball)
            else:
                estado = "game_over"

        screen.blit(background_image, (0, 0)) if background_image else screen.fill(BLACK)
        all_sprites.draw(screen)
        lives_color = (255, 0, 0) if lives <= 1 else (255, 255, 255)
        score_text = font.render(f"Puntaje: {score}", True, (255, 255, 255))
        lives_text = font.render(f"Vidas: {lives}", True, lives_color)
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (WIDTH - 130, 10))

    elif estado == "game_over":
        screen.blit(background_image, (0, 0)) if background_image else screen.fill(BLACK)
        dibujar_soles()
        screen.blit(texto_game_over, rect_game_over)
        texto_puntaje_final = fuente_media.render(f"Puntaje final: {score}", True, negro)
        rect_puntaje_final = texto_puntaje_final.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))
        screen.blit(texto_puntaje_final, rect_puntaje_final)

        color_reiniciar = gris_oscuro if boton_reiniciar_rect.collidepoint(mouse_pos) else oro
        pygame.draw.rect(screen, color_reiniciar, boton_reiniciar_rect, border_radius=10)
        screen.blit(texto_reiniciar, rect_texto_reiniciar)
        if boton_reiniciar_rect.collidepoint(mouse_pos) and click[0]:
            estado = "jugando"
            score = 0
            lives = 3
            for block in blocks: block.kill()
            for row in range(5):
                for col in range(10):
                    block = Block(60 + col * 70, 40 + row * 30)
                    all_sprites.add(block)
                    blocks.add(block)
            for ball in balls: ball.kill()
            new_ball = Ball(paddle, blocks, all_sprites, balls, ball_image=pelota_ball_image, hit_sound=hit_ball_in_block)
            all_sprites.add(new_ball)
            balls.add(new_ball)

        color_salir = gris_oscuro if boton_salir_rect.collidepoint(mouse_pos) else oro
        pygame.draw.rect(screen, color_salir, boton_salir_rect, border_radius=10)
        screen.blit(texto_salir, rect_texto_salir)
        if boton_salir_rect.collidepoint(mouse_pos) and click[0]:
            running = False

    pygame.display.flip()

pygame.quit()
sys.exit()
