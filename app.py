#en este archivo va a estar la logica del juego, el bucle principal y la deteccion de eventos
# este controla todo 
import pygame
from config import WIDTH, HEIGHT, FPS, BLACK
from paddle import Paddle
from ball import Ball
from block import Block
import os
pygame.init() #inicializamos el juego

pygame.mixer.init()

script_dir = os.path.dirname(__file__)

import pygame
import sys
import random

pygame.init()

# Tamaño de pantalla
ancho, alto = 800, 600
pantalla = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption("Arkanoid")

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
    x = random.randint(0, ancho)
    y = random.randint(0, alto)
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
boton_play_rect, texto_play, rect_texto_play = crear_boton( "PLAY", ancho // 2, alto // 2 + 140, 200, 50, 40 )

# Botón REINICIAR (más chico y más abajo)
boton_reiniciar_rect, texto_reiniciar, rect_texto_reiniciar = crear_boton( "REINICIAR", ancho // 2 + 100, alto // 2 + 200, 180, 40, 30)

# Botón SALIR (más arriba y más angosto)
boton_salir_rect, texto_salir, rect_texto_salir = crear_boton( "SALIR", ancho // 2 - 100, alto // 2 + 200, 160, 40, 35)


# Texto título para menú y game over
texto_titulo_menu = fuente.render("☀️ Bienvenido Argenoid ☀️", True, negro)
rect_titulo_menu = texto_titulo_menu.get_rect(center=(ancho // 2, alto // 2 - 200))

texto_game_over = fuente.render("GAME OVER", True, negro)
rect_game_over = texto_game_over.get_rect(center=(ancho // 2, alto // 2 + 160))

# Función para dibujar soles
def dibujar_soles():
    for sol in soles:
        x, y, radio, brillo = sol
        dibujar_sol(pantalla, x, y, radio, brillo)
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

        pantalla.blit(texto_titulo_menu, rect_titulo_menu)
        pygame.draw.rect(pantalla, color_boton, boton_play_rect, border_radius=10)
        pantalla.blit(texto_play, rect_texto_play)

    elif estado == "jugando":
        # Aquí deberías poner la lógica real del juego.
        # Por ejemplo, para simular, aumentamos puntaje por tiempo:
        puntaje += 1

        # Mostrar puntaje en pantalla
        texto_puntaje = fuente_pequena.render(f"Puntaje: {puntaje}", True, negro)
        pantalla.blit(texto_puntaje, (10, 10))

        # Simulación de fin de juego: si puntaje llega a 1000 pasa a game over (solo como ejemplo)
        if puntaje >= 5:
            estado = "game_over"

    elif estado == "game_over":
        pantalla.blit(texto_game_over, rect_game_over)

        # Mostrar puntaje final
        texto_puntaje_final = fuente_pequena.render(f"Puntaje final: {puntaje}", True, negro)
        rect_puntaje_final = texto_puntaje_final.get_rect(center=(ancho // 2, alto // 2 - (-100)))
        pantalla.blit(texto_puntaje_final, rect_puntaje_final)

        # Botón REINICIAR
        color_boton_reiniciar = gold
        if boton_reiniciar_rect.collidepoint(mouse_pos):
            color_boton_reiniciar = gris_oscuro
            if click[0]:
                estado = "jugando"
                puntaje = 0

        pygame.draw.rect(pantalla, color_boton_reiniciar, boton_reiniciar_rect, border_radius=10)
        pantalla.blit(texto_reiniciar, rect_texto_reiniciar)

        # Botón SALIR
        color_boton_salir = gold
        if boton_salir_rect.collidepoint(mouse_pos):
            color_boton_salir = gris_oscuro
            if click[0]:
                pygame.quit()
                sys.exit()

        pygame.draw.rect(pantalla, color_boton_salir, boton_salir_rect, border_radius=10)
        pantalla.blit(texto_salir, rect_texto_salir)

    pygame.display.flip()
    clock.tick(60)



background_music_path = os.path.join(script_dir, "assets", "sounds", "himno-nacional-argentino.wav")
try:
    pygame.mixer.music.load(background_music_path)
    print(f"Música de fondo cargada: {background_music_path}")
except pygame.error as e:
    print(f"Error al cargar la música de fondo: {e}")
    print(f"Intentando cargar desde: {background_music_path}")
pygame.mixer.music.play(-1)

hit_sound_path = os.path.join(script_dir, "assets", "sounds", "arkanoid-sfx-1-101soundboards.mp3")
hit_ball_in_block = None # Inicializamos la variable a None
try:
    hit_ball_in_block = pygame.mixer.Sound(hit_sound_path)
    print(f"Sonido de golpe cargado: {hit_sound_path}")
except pygame.error as e:
    print(f"Error al cargar el sonido de golpe: {e}")
    print(f"Intentando cargar desde: {hit_sound_path}")

screen = pygame.display.set_mode((WIDTH, HEIGHT)) #configuramos la ventana donde se va a ejecutar el juego
pygame.display.set_caption("Arkanoid") #nombre del juego para que aparezca arriba
clock = pygame.time.Clock() # Objeto Clock para controlar el framerate

background_image_path = os.path.join(script_dir, "assets", "images", "messi.jpg") 
background_image = None

#Añadimos la imagen luego de inicializar el juego
#Asi se añade el fondo cuando se actualice la pantalla.

try:
    background_image = pygame.image.load(background_image_path).convert()
    # Escalamos la imagen para que se ajuste al tamaño de la pantalla
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
    print(f"Imagen de fondo cargada exitosamente: {background_image_path}")
except pygame.error as e:
    print(f"ERROR: Pygame no pudo cargar la imagen de fondo. Mensaje: {e}")
    print(f"Asegúrate de que el archivo no esté corrupto y sea un formato compatible (.jpg, .png).")
    print("Se usará un fondo negro en su lugar.")

pelota_image_path = os.path.join(script_dir, "assets","images", "pelota.png")
pelota_ball_image = None
try:
    # Carga la imagen y la convierte para optimización
    pelota_ball_image = pygame.image.load(pelota_image_path).convert_alpha() 
    # Escala la imagen al tamaño deseado para la pelota (ej. 15x15 píxeles)
    pelota_ball_image = pygame.transform.scale(pelota_ball_image, (35, 35))

    print(f"Imagen del mate cargada exitosamente para la pelota: {pelota_image_path}")
except pygame.error as e:
    print(f"ERROR: Pygame no pudo cargar la imagen del mate para la pelota. Mensaje: {e}")
    print(f"Asegúrate de que el archivo 'pelota.png' esté en la carpeta 'assets'.")
    print("La pelota se dibujará como un círculo blanco.")
    # Si la imagen no se carga, mate_ball_image seguirá siendo None.



#CREAMOS LOS GRUPOS (con esto podemos manejar muchos objetos a la vez)
all_sprites = pygame.sprite.Group()
blocks = pygame.sprite.Group()
balls = pygame.sprite.Group()

#creamos los objetos y lo agregamos a los grupos
paddle = Paddle()
all_sprites.add(paddle)


for row in range(5):
    for col in range(10):
        block = Block(60 + col * 70, 40 + row * 30) #creamos el bloque en una determinada posicion, que depende del indice de la fila y de la columna
        all_sprites.add(block)
        blocks.add(block)

ball = Ball(paddle, blocks, all_sprites, balls,ball_image= pelota_ball_image,hit_sound=hit_ball_in_block)
all_sprites.add(ball)
balls.add(ball)

#este bloque es el principal, es el que se ejecuta mientras el juego este constantemente activo

running = True
while running:
    clock.tick(FPS) #con esto hacemos que el bucle se ejecute 60 veces por segundo, para evitar que el programa vaya rapido o ande mal
    keys = pygame.key.get_pressed() #esto es para mover las flechas

    for event in pygame.event.get(): #aca verificamos si estamos haciendo
        if event.type == pygame.QUIT: #si el evento es QUIT se cierra el juego
            running = False

    paddle.update(keys) # con esto verificamos si se mueve la paleta
    for ball in list(balls):
        ball.update() #actualizamos el estado de la pelota

    #esto es para crear pelotas nuevas
    #esto despues se tiene que cambiar, cuando la pelota sea 0 se tiene que quitar una vida o hace un game over
    if len(balls) == 0: #si no hay pelotas se crea una nueva 
        new_ball = Ball(paddle, blocks, all_sprites, balls, hit_sound=hit_ball_in_block, ball_image=pelota_ball_image)
        all_sprites.add(new_ball)
        balls.add(new_ball)

    # --- Dibujamos los elementos de la pantalla ---
    if background_image: # Si la imagen de fondo se cargó correctamente
        screen.blit(background_image, (0, 0)) # Dibujamos la imagen de fondo en la posición (0,0)
    else:
        screen.fill(BLACK) # Si no hay imagen, el fondo sigue siendo negro

    all_sprites.draw(screen) # Dibujamos el escenario (paleta, pelotas, bloques)
    pygame.display.flip()  # Actualizamos la pantalla


pygame.quit() #cerramos el juego
