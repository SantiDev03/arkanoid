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
