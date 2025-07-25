#en este archivo va a estar la logica del juego, el bucle principal y la deteccion de eventos
# este controla todo 
import pygame
from config import WIDTH, HEIGHT, FPS, BLACK
from paddle import Paddle
from ball import Ball
from block import Block
import os
from datetime import datetime

pygame.init() #inicializamos el juego
pygame.mixer.init()

score = 0  # Guarda los puntos
lives = 3  # Guarda las vidas
font = pygame.font.SysFont(None, 36)   # Fuente para mostrar texto en pantalla

script_dir = os.path.dirname(__file__)

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
    pelota_ball_image = pygame.image.load(pelota_image_path).convert_alpha() 
    pelota_ball_image = pygame.transform.scale(pelota_ball_image, (35, 35))
    print(f"Imagen del mate cargada exitosamente para la pelota: {pelota_image_path}")
except pygame.error as e:
    print(f"ERROR: Pygame no pudo cargar la imagen del mate para la pelota. Mensaje: {e}")
    print(f"Asegúrate de que el archivo 'pelota.png' esté en la carpeta 'assets'.")
    print("La pelota se dibujará como un círculo blanco.")

#FUNCION PARA GUARDAR Y MOSTRAR PUNTAJES EN PANTALLA
def mostrar_game_over_en_pantalla(score):
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    linea = f"{ahora} - Puntaje: {score}\n"

    with open("scores.txt", "a") as f:
        f.write(linea)

    # Fondo negro o el mismo fondo si está cargado
    if background_image:
        screen.blit(background_image, (0, 0))
    else:
        screen.fill(BLACK)

    # Mostrar GAME OVER
    game_over_text = font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(game_over_text, (WIDTH // 2 - 100, 100))

    # Mostrar puntaje actual
    actual_text = font.render(f"Tu puntaje: {score}", True, (255, 255, 255))
    screen.blit(actual_text, (WIDTH // 2 - 120, 150))

    # Leer últimos 5 puntajes del archivo
    try:
        with open("scores.txt", "r") as f:
            lineas = f.readlines()
            ultimos = lineas[-5:] if len(lineas) >= 5 else lineas
            for i, l in enumerate(ultimos):
                t = font.render(l.strip(), True, (255, 255, 255))
                screen.blit(t, (WIDTH // 2 - 200, 220 + i * 30))
    except FileNotFoundError:
        t = font.render("No hay puntajes previos.", True, (255, 255, 255))
        screen.blit(t, (WIDTH // 2 - 150, 220))

    pygame.display.flip()
    pygame.time.wait(6000)  # Esperamos 6 segundos para que lo lea

#CREAMOS LOS GRUPOS (con esto podemos manejar muchos objetos a la vez)
all_sprites = pygame.sprite.Group()
blocks = pygame.sprite.Group()
balls = pygame.sprite.Group()

#creamos los objetos y lo agregamos a los grupos
paddle = Paddle()
all_sprites.add(paddle)

for row in range(5):
    for col in range(10):
        block = Block(60 + col * 70, 40 + row * 30) #creamos el bloque en una determinada posicion
        all_sprites.add(block)
        blocks.add(block)

ball = Ball(paddle, blocks, all_sprites, balls, ball_image=pelota_ball_image, hit_sound=hit_ball_in_block)
all_sprites.add(ball)
balls.add(ball)

#este bloque es el principal, es el que se ejecuta mientras el juego este constantemente activo

running = True
while running:
    clock.tick(FPS) #con esto hacemos que el bucle se ejecute 60 veces por segundo
    keys = pygame.key.get_pressed() #esto es para mover las flechas

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    paddle.update(keys)
    for ball in list(balls):
        result = ball.update()
        if result == 'block_destroyed':
            score += 10

    # cuando no hay pelotas se pierde una vida
    if len(balls) == 0:
        lives -= 1
        if lives > 0:
            new_ball = Ball(paddle, blocks, all_sprites, balls, hit_sound=hit_ball_in_block, ball_image=pelota_ball_image)
            all_sprites.add(new_ball)
            balls.add(new_ball)
        else:
            mostrar_game_over_en_pantalla(score)
            running = False

    #dibujamos
    if background_image:
        screen.blit(background_image, (0, 0))
    else:
        screen.fill(BLACK)

    all_sprites.draw(screen)
    lives_color = (255, 0, 0) if lives <= 1 else (255, 255, 255)
    score_text = font.render(f"Puntaje: {score}", True, (255, 255, 255))
    lives_text = font.render(f"Vidas: {lives}", True, lives_color)
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (WIDTH - 130, 10))
    pygame.display.flip()

pygame.quit()
print("Bye mundo")
