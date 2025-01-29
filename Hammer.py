import pygame
import random

ANCHO = 22
ALTO = 30
ANGULO = 1

#Clase Hammer
class Hammer:
    def __init__(self, ancho, velocidad):
        #Dimensiones del martillo
        self.ancho = ANCHO
        self.alto = ALTO
        #Posición y ángulo inicial
        self.x = random.randint(0, ancho - self.ancho)
        self.y = 0
        self.angle = ANGULO

        #Imagen
        self.image = pygame.image.load("assets/images/hammer.png")
        self.image = pygame.transform.scale(self.image,(self.ancho,self.alto))
        self.image = pygame.transform.rotate(self.image, self.angle)
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.rotated_image = self.image
        self.rotated_rect = self.rect

        #Velocidad
        self.velocidad = velocidad

    def update(self):
        #Incrementar el ángulo para rotar el martillo
        self.angle += (self.velocidad +3)

        #Rotar la imagen
        self.rotated_image = pygame.transform.rotate(self.image, self.angle)

        #Calcula la posición para mantener el centro
        self.rotated_rect = self.rotated_image.get_rect(center=(self.x, self.y))

        #Movimiento
        self.y += self.velocidad

    #Dibujar martillo
    def draw(self, ventana):
        ventana.blit(self.rotated_image, self.rotated_rect)

    #Hacer visible los martillos
    def is_visible(self, ancho, alto):
        visible = False
        if (0 < self.rotated_rect.x < ancho) and (alto > self.rotated_rect.y > 0):
            visible = True
        return visible