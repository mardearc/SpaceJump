import pygame
import random

ANCHO = 60
ALTO = 15
VELOCIDAD = 1

#Clase Platform
class Platform:
    def __init__(self, ancho, alto, offset_y):
        #Tamaño
        self.ancho = ANCHO
        self.alto = ALTO

        #Posicion
        self.x = random.randint(0, ancho - self.ancho)
        self.y = alto - offset_y

        #Cargar imagen
        self.image = pygame.image.load("assets/images/platformsGreen.png")
        self.image = pygame.transform.scale(self.image, (self.ancho, self.alto))
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

        #Establecer velocidad
        self.velocidad = VELOCIDAD

    #Actualizar movimiento
    def update(self, ancho, alto):
        self.rect.move_ip(0, self.velocidad)
        if self.rect.top >= alto:
            self.rect.left = random.randint(0, ancho - self.ancho)
            self.rect.top = -self.alto

    #Dibujar
    def draw(self, ventana):
        ventana.blit(self.image, self.rect)
