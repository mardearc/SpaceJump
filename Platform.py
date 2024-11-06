import pygame
import random


class Platform:
    def __init__(self, ancho, alto, offset_y):
        self.ancho = 60
        self.alto = 15
        self.x = random.randint(0, ancho - self.ancho)
        self.y = alto - offset_y
        self.image = pygame.image.load("platformsGreen.png")
        self.image = pygame.transform.scale(self.image, (self.ancho, self.alto))
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.velocidad = 1

    def update(self, ancho, alto, knightrect):

        self.rect.move_ip(0, self.velocidad)
        if self.rect.top >= alto:
            self.rect.left = random.randint(0, ancho - self.ancho)
            self.rect.top = -self.alto

    def draw(self, ventana):
        ventana.blit(self.image, self.rect)
