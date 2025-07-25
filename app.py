import pygame
import sys
import os
import random
from config import WIDTH, HEIGHT, FPS, BLACK
from paddle import Paddle
from ball import Ball
from block import Block
from datetime import datetime

pygame.init()
pygame.mixer.init()

# Ventana
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Argenoid")
clock = pygame.time.Clock()

# Puntaje y vidas
score = 0
lives = 3

# Fuentes
font = pygame.font.SysFont(None, 36)
fuente_grande = pygame.font.SysFont("Segoe UI Emoji", 60)
fuente_media = pygame.font.SysFont("Segoe UI Emoji", 40)

# Colores
negro = (0, 0, 0)
oro = (212, 175, 55)
gris_oscuro = (150, 150, 150)
amarillo = (255, 255, 0)
rojo = (255, 0, 0 )

# Estados
estado = "menu"

# Cargar imágenes
script_dir = os.path.dirname(__file__)
background_image = None
bandera_image = None

try:
    background_image = pygame.image.load(os.path.join(script_dir, "assets", "images", "messi.jpg")).convert()
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
except:
    pass

try:
    bandera_image = pygame.image.load(os.path.join(script_dir, "assets", "images", "bandera_argentina.jpg")).convert()
    bandera_image = pygame.transform.scale(bandera_image, (WIDTH, HEIGHT))
except:
    pass

# Cargar sonidos
hit_sound = None
try:
    path_hit = os.path.join(script_dir, "assets", "sounds", "arkanoid-sfx-1-101soundboards.mp3")
    hit_sound = pygame.mixer.Sound(path_hit)
except:
    print("Error cargando sonido de golpe")

try:
    bg_music_path = os.path.join(script_dir, "assets", "sounds", "himno-nacional-argentino.wav")
    pygame.mixer.music.load(bg_music_path)
    pygame.mixer.music.play(-1)
except:
    pass

# Cargar imagen pelota
pelota_ball_image = None
try:
    pelota_path = os.path.join(script_dir, "assets", "images", "pelota.png")
    pelota_ball_image = pygame.image.load(pelota_path).convert_alpha()
    pelota_ball_image = pygame.transform.scale(pelota_ball_image, (35, 35))
except:
    pass

# Crear botones
def crear_boton(texto, x_center, y_pos, ancho, alto, tam_fuente):
    fuente = pygame.font.SysFont(None, tam_fuente)
    rect = pygame.Rect(0, y_pos, ancho, alto)
    rect.centerx = x_center
    render = fuente.render(texto, True, negro)
    rect_texto = render.get_rect(center=rect.center)
    return rect, render, rect_texto

# Botones
boton_play_rect, texto_play, rect_play = crear_boton("PLAY", WIDTH // 2, HEIGHT // 2 + 140, 200, 50, 40)
boton_ver_puntaje_rect, texto_ver_puntaje, rect_ver_puntaje = crear_boton("VER PUNTUACIÓN", WIDTH // 2, HEIGHT // 2 + 200, 260, 50, 35)
boton_salir_menu_rect, texto_salir_menu, rect_salir_menu = crear_boton("SALIR", WIDTH // 2, HEIGHT // 2 + 260, 160, 50, 35)

boton_reiniciar_rect, texto_reiniciar, rect_reiniciar = crear_boton("REINICIAR", WIDTH // 2 + 100, HEIGHT // 2 + 200, 180, 40, 30)
boton_salir_rect, texto_salir, rect_salir = crear_boton("SALIR", WIDTH // 2 - 100, HEIGHT // 2 + 200, 160, 40, 35)
boton_volver_rect, texto_volver, rect_volver = crear_boton("VOLVER", WIDTH // 2, HEIGHT - 100, 160, 40, 35)

texto_titulo = fuente_grande.render("🧉Bienvenido Argenoid🧉", True, negro)
rect_titulo = texto_titulo.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 200))

texto_game_over = fuente_grande.render("GAME OVER", True, negro)
rect_game_over = texto_game_over.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))

texto_winner = fuente_grande.render("WINNER", True, negro)
rect_winner = texto_winner.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))

# Guardar puntaje
def guardar_puntaje(score):
    fecha = datetime.now().strftime("%Y-%m-%d") 
    linea = f"{fecha} - Puntaje: {score}\n"
    with open("scores.txt", "a") as f:
        f.write(linea)

# Mostrar puntajes
def mostrar_puntajes():
    try:
        with open("scores.txt", "r") as f:
            lineas = f.readlines()
            ultimos = lineas[-5:] if len(lineas) >= 5 else lineas
        for i, l in enumerate(ultimos):
            t = font.render(l.strip(), True, negro)
            screen.blit(t, (WIDTH // 2 - 200, 250 + i * 40))
    except:
        t = font.render("No hay puntajes previos.", True, negro)
        screen.blit(t, (WIDTH // 2 - 150, 250))

# Crear juego
def iniciar_juego():
    global all_sprites, blocks, balls, paddle
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
    ball = Ball(paddle, blocks, all_sprites, balls, hit_sound=hit_sound, ball_image=pelota_ball_image)
    all_sprites.add(ball)
    balls.add(ball)

# Inicial
iniciar_juego()

# Loop principal
running = True
while running:
    clock.tick(FPS)
    keys = pygame.key.get_pressed()
    mouse_pos = pygame.mouse.get_pos()
    click_event = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            click_event = True

    if estado == "menu":
        screen.blit(bandera_image, (0, 0)) if bandera_image else screen.fill(BLACK)
        screen.blit(texto_titulo, rect_titulo)

        pygame.draw.rect(screen, oro if boton_play_rect.collidepoint(mouse_pos) else gris_oscuro, boton_play_rect, border_radius=10)
        screen.blit(texto_play, rect_play)

        pygame.draw.rect(screen, oro if boton_ver_puntaje_rect.collidepoint(mouse_pos) else gris_oscuro, boton_ver_puntaje_rect, border_radius=10)
        screen.blit(texto_ver_puntaje, rect_ver_puntaje)

        pygame.draw.rect(screen, oro if boton_salir_menu_rect.collidepoint(mouse_pos) else gris_oscuro, boton_salir_menu_rect, border_radius=10)
        screen.blit(texto_salir_menu, rect_salir_menu)

        if boton_play_rect.collidepoint(mouse_pos) and click_event:
            estado = "jugando"
            score = 0
            lives = 3
            iniciar_juego()

        if boton_ver_puntaje_rect.collidepoint(mouse_pos) and click_event:
            estado = "ver_puntajes"

        if boton_salir_menu_rect.collidepoint(mouse_pos) and click_event:
            running = False

    elif estado == "ver_puntajes":
        screen.blit(bandera_image, (0, 0)) if bandera_image else screen.fill(BLACK)
        texto_titulo_puntajes = fuente_media.render("Últimos Puntajes", True, negro)
        screen.blit(texto_titulo_puntajes, (WIDTH // 2 - 170, 100))
        mostrar_puntajes()

        pygame.draw.rect(screen, oro if boton_volver_rect.collidepoint(mouse_pos) else gris_oscuro, boton_volver_rect, border_radius=10)
        screen.blit(texto_volver, rect_volver)

        if boton_volver_rect.collidepoint(mouse_pos) and click_event:
            estado = "menu"

    elif estado == "jugando":
        screen.blit(background_image, (0, 0)) if background_image else screen.fill(BLACK)

        # ACTUALIZAMOS SPRITES CORRECTAMENTE
        paddle.update(keys)   # Paddle recibe las teclas
        for ball in balls:
            resultado = ball.update()
            if resultado == 'block_destroyed':
                score += 10        # Ball no recibe teclas
        blocks.update()       # Blocks tampoco

        all_sprites.draw(screen)

        # Mostrar score y vidas
        texto_score = font.render(f"Puntaje: {score}", True, amarillo)
        screen.blit(texto_score, (20, 10))
        texto_vidas = font.render(f"Vidas: {lives}", True, rojo)
        screen.blit(texto_vidas, (WIDTH - 150, 10))

        # Verificar si no hay bloques (ganó)
        if len(blocks) == 0:
            estado = "ganador"
            guardar_puntaje(score)

        # Verificar si todas las pelotas se perdieron
        elif len(balls) == 0:
            lives -= 1
            if lives > 0:
                ball = Ball(paddle, blocks, all_sprites, balls, hit_sound=hit_sound, ball_image=pelota_ball_image)
                all_sprites.add(ball)
                balls.add(ball)
            else:
                estado = "game_over"
                guardar_puntaje(score)

    elif estado == "game_over":
        screen.blit(bandera_image, (0, 0)) if bandera_image else screen.fill(BLACK)
        screen.blit(texto_game_over, rect_game_over)

        pygame.draw.rect(screen, oro if boton_reiniciar_rect.collidepoint(mouse_pos) else gris_oscuro, boton_reiniciar_rect, border_radius=10)
        screen.blit(texto_reiniciar, rect_reiniciar)

        pygame.draw.rect(screen, oro if boton_salir_rect.collidepoint(mouse_pos) else gris_oscuro, boton_salir_rect, border_radius=10)
        screen.blit(texto_salir, rect_salir)

        if boton_reiniciar_rect.collidepoint(mouse_pos) and click_event:
            score = 0
            lives = 3
            iniciar_juego()
            estado = "jugando"

        if boton_salir_rect.collidepoint(mouse_pos) and click_event:
            estado = "menu"

    elif estado == "ganador":
        screen.blit(bandera_image, (0, 0)) if bandera_image else screen.fill(BLACK)
        screen.blit(texto_winner, rect_winner)

        pygame.draw.rect(screen, oro if boton_reiniciar_rect.collidepoint(mouse_pos) else gris_oscuro, boton_reiniciar_rect, border_radius=10)
        screen.blit(texto_reiniciar, rect_reiniciar)

        pygame.draw.rect(screen, oro if boton_salir_rect.collidepoint(mouse_pos) else gris_oscuro, boton_salir_rect, border_radius=10)
        screen.blit(texto_salir, rect_salir)

        if boton_reiniciar_rect.collidepoint(mouse_pos) and click_event:
            score = 0
            lives = 3
            iniciar_juego()
            estado = "jugando"

        if boton_salir_rect.collidepoint(mouse_pos) and click_event:
            estado = "menu"

    pygame.display.flip()

pygame.quit()
sys.exit()
