import pygame
import sys
import random
pygame.init()

# Constantes
negro = (0, 0, 0)
salto = 50
ANCHO = 500
ALTO = 700
last_pos = True

# Ventana
size_ventana = (ANCHO, ALTO)
ventana = pygame.display.set_mode(size_ventana)

# Personaje
personaje_pos = [225, 500]
personaje_size = 50

# Plataforma

plataforma_size_ancho = 100
plataforma_size_alto = 25
plataforma_pos = [random.randint(0, ANCHO - plataforma_size_ancho), 500]

while True:
    # Para salir del juego
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    # Compruebo si se ha pulsado alguna tecla para mover de derecha a izquierda
    keys = pygame.key.get_pressed()
    x = personaje_pos[0]
    if keys[pygame.K_LEFT] and x > 0:
        x -= 0.2
    if keys[pygame.K_RIGHT] and x < size_ventana[0] - personaje_size:
        x += 0.2

    # Bucle para el salto automático del personaje
    y = personaje_pos[1]
    if y >= 250 and last_pos:
        y -= 0.3
        if y <= 250:
            last_pos = False
    else:
        y += 0.3
        if y >= 700 or (plataforma_pos[1] - 50 <= y <= plataforma_pos[1] - 40 and plataforma_pos[0] - 50 < x < plataforma_pos[0] + 100):
            if y >= 700:
                sys.exit()
            last_pos = True

    #Bucle para la plataforma
    #if plataforma_pos[1] < ALTO:
    #    plataforma_pos[1] += 0.2
    #else:
    #    plataforma_pos[0] = random.randint(0, ANCHO - plataforma_size_ancho)
    #    plataforma_pos[1] = 0

    #Ajustar posiciones y fondo
    personaje_pos[1] = y
    personaje_pos[0] = x
    ventana.fill(negro)

    # Dibujar jugador
    pygame.draw.rect(ventana, (255, 0, 0), (personaje_pos[0],
                                            personaje_pos[1],
                                            personaje_size,
                                            personaje_size))

    # Dibujar plataforma
    pygame.draw.rect(ventana, (255, 0, 0), (plataforma_pos[0],
                                            plataforma_pos[1],
                                            plataforma_size_ancho,
                                            plataforma_size_alto))
    pygame.display.update()
