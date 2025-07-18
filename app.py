#en este archivo va a estar la logica del juego, el bucle principal y la deteccion de eventos
# este controla todo 
import pygame
from config import WIDTH, HEIGHT, FPS, BLACK
from paddle import Paddle
from ball import Ball
from block import Block

pygame.init() #inicializamos el juego
screen = pygame.display.set_mode((WIDTH, HEIGHT)) #configuramos la ventana donde se va a ejecutar el juego
pygame.display.set_caption("Arkanoid") #nombre del juego para que aparezca arriba
clock = pygame.time.Clock() #?

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

ball = Ball(paddle, blocks, all_sprites, balls)
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
        new_ball = Ball(paddle, blocks, all_sprites, balls)
        all_sprites.add(new_ball)
        balls.add(new_ball)

    #dibujamos los elementos de la pantalla
    screen.fill(BLACK) #fondo negro
    all_sprites.draw(screen) #dibujamos el escenario 
    pygame.display.flip()  #actualizamos la pantalla

pygame.quit() #cerramos el juego
