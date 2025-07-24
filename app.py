#en este archivo va a estar la logica del juego, el bucle principal y la deteccion de eventos
# este controla todo 
import pygame
from config import WIDTH, HEIGHT, FPS, BLACK
from paddle import Paddle
from ball import Ball
from block import Block

import sys
import random
import os
pygame.init() #inicializamos el juego

pygame.mixer.init()

script_dir = os.path.dirname(__file__)
# Tamaño de pantalla

# Fondo
screen = pygame.display.set_mode((WIDTH, HEIGHT)) #configuramos la ventana donde se va a ejecutar el juego
pygame.display.set_caption("Arkanoid") #nombre del juego para que aparezca arriba
clock = pygame.time.Clock()

menu_background_path = os.path.join(script_dir, "assets", "images", "fondo.juego.jpg")
menu_background_image = None
try:
    menu_background_image = pygame.image.load(menu_background_path).convert()
    menu_background_image = pygame.transform.scale(menu_background_image, (WIDTH, HEIGHT))
    print(f"Imagen de fondo de menú cargada: {menu_background_path}")
except pygame.error as e:
    print(f"ERROR cargando fondo menú: {e}")
    print("Se usará fondo negro para menú.")

# Fuente con emoji
fuente = pygame.font.SysFont("Segoe UI Emoji", 60)
fuente_pequena = pygame.font.SysFont("Segoe UI Emoji", 40)


# Colores
negro = (0, 0, 0)
gold = (212, 175, 55)
gris_oscuro = (150, 150, 150)

# Soles animados
soles = []
for _ in range(100):
    x = random.randint(0, WIDTH)
    y = random.randint(0, HEIGHT)
    radio = random.randint(3, 5)
    brillo = random.randint(180, 255)
    soles.append([x, y, radio, brillo])

def dibujar_sol(pantalla, x, y, radio, brillo):
    color = (brillo, max(brillo - 50,0), 0)
    pygame.draw.circle(pantalla, color, (x, y), radio)
    for i in range(8):
        angulo = i * 45
        dx = int(radio * 1.8 * pygame.math.Vector2(1, 0).rotate(angulo).x)
        dy = int(radio * 1.8 * pygame.math.Vector2(1, 0).rotate(angulo).y)
        pygame.draw.line(pantalla, color, (x, y), (x + dx, y + dy), 1)

# Variables de estado
estado = "menu"
puntaje = 0
clock = pygame.time.Clock()

# Botón de menú y game over (usaremos mismos tamaños)
boton_width, boton_height = 200, 60

def crear_boton(texto, x_center, y_pos, ancho_boton, alto_boton, tam_fuente):
    fuente_boton = pygame.font.SysFont(None, tam_fuente)
    boton_rect = pygame.Rect(0, y_pos, ancho_boton, alto_boton)
    boton_rect.centerx = x_center  
    texto_render = fuente_boton.render(texto, True, negro)
    texto_rect = texto_render.get_rect(center=boton_rect.center)
    return boton_rect, texto_render, texto_rect


# Botón PLAY
boton_play_rect, texto_play, rect_texto_play = crear_boton( "PLAY", WIDTH // 2, HEIGHT // 2 + 140, 200, 50, 40 )

# Botón REINICIAR (más chico y más abajo)
boton_reiniciar_rect, texto_reiniciar, rect_texto_reiniciar = crear_boton( "REINICIAR", WIDTH // 2 + 100, HEIGHT // 2 + 200, 180, 40, 30)

# Botón SALIR (más arriba y más angosto)
boton_salir_rect, texto_salir, rect_texto_salir = crear_boton( "SALIR", WIDTH // 2 - 100, HEIGHT // 2 + 200, 160, 40, 35)


# Texto título para menú y game over
texto_titulo_menu = fuente.render("☀️ Bienvenido Argenoid ☀️", True, negro)
rect_titulo_menu = texto_titulo_menu.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 200))

texto_game_over = fuente.render("GAME OVER", True, negro)
rect_game_over = texto_game_over.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 160))

# Función para dibujar soles
def dibujar_soles():
    for sol in soles:
        x, y, radio, brillo = sol
        dibujar_sol(screen, x, y, radio, brillo)
        sol[3] += random.randint(-15, 15)
        sol[3] = max(150, min(255, sol[3]))

# Bucle principal
corriendo = True
while corriendo:
    mouse_pos = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
if estado == "menu":
    if menu_background_image:
        screen.blit(menu_background_image, (0, 0))
    else:
        screen.fill(BLACK)
    dibujar_soles()

    if estado == "menu":
        # Botón PLAY
        color_boton = gold
        if boton_play_rect.collidepoint(mouse_pos):
            color_boton = gris_oscuro
            if click[0]:
                estado = "jugando"
                puntaje = 0

        screen.blit(texto_titulo_menu, rect_titulo_menu)
        pygame.draw.rect(screen, color_boton, boton_play_rect, border_radius=10)
        screen.blit(texto_play, rect_texto_play)

    elif estado == "jugando":
        # Aquí deberías poner la lógica real del juego.
        # Por ejemplo, para simular, aumentamos puntaje por tiempo:
        puntaje += 1

        # Mostrar puntaje en pantalla
        texto_puntaje = fuente_pequena.render(f"Puntaje: {puntaje}", True, negro)
        screen.blit(texto_puntaje, (10, 10))

        # Simulación de fin de juego: si puntaje llega a 1000 pasa a game over (solo como ejemplo)
        if puntaje >= 5:
            estado = "game_over"

    elif estado == "game_over":
        screen.blit(texto_game_over, rect_game_over)

        # Mostrar puntaje final
        texto_puntaje_final = fuente_pequena.render(f"Puntaje final: {puntaje}", True, negro)
        rect_puntaje_final = texto_puntaje_final.get_rect(center=(WIDTH // 2, HEIGHT// 2 - (-100)))
        screen.blit(texto_puntaje_final, rect_puntaje_final)

        # Botón REINICIAR
        color_boton_reiniciar = gold
        if boton_reiniciar_rect.collidepoint(mouse_pos):
            color_boton_reiniciar = gris_oscuro
            if click[0]:
                estado = "jugando"
                puntaje = 0

        pygame.draw.rect(screen, color_boton_reiniciar, boton_reiniciar_rect, border_radius=10)
        screen.blit(texto_reiniciar, rect_texto_reiniciar)

        # Botón SALIR
        color_boton_salir = gold
        if boton_salir_rect.collidepoint(mouse_pos):
            color_boton_salir = gris_oscuro
            if click[0]:
                pygame.quit()
                sys.exit()

        pygame.draw.rect(screen, color_boton_salir, boton_salir_rect, border_radius=10)
        screen.blit(texto_salir, rect_texto_salir)

    pygame.display.flip()
    clock.tick(60)



