import sys

import pygame

ANCHO = 500
ALTO = 700

class Knight:
    def __init__(self, x, y):
        self.image = pygame.image.load("knight_1.png")
        self.image = pygame.transform.scale(self.image, (20, 25))
        self.knightrect = self.image.get_rect(topleft=(x, y))
        self.velocidad_salto_original = -15
        self.velocidad_salto = self.velocidad_salto_original
        self.velocidad_caida = 10
        self.en_salto = False
        self.esta_girado = True
        self.plataforma_actual = None
        self.plataforma_nueva = None

    def update(self, keys, plataformas, jump_sound):
        # Movimiento horizontal
        if keys[pygame.K_LEFT]:
            if self.knightrect.left <= 0:
                self.knightrect.move_ip(ANCHO, 0)
            self.knightrect.move_ip(-7, 0)
            if self.esta_girado:
                self.image = pygame.transform.flip(self.image, 1, 0)
                self.esta_girado = False
        elif keys[pygame.K_RIGHT]:
            if self.knightrect.right >= ANCHO:
                self.knightrect.move_ip(-ANCHO, 0)
            self.knightrect.move_ip(7, 0)
            if not self.esta_girado:
                self.image = pygame.transform.flip(self.image, 1, 0)
                self.esta_girado = True

        # Salto controlado
        if keys[pygame.K_SPACE] and not self.en_salto and self.is_on_platform(plataformas):
            self.en_salto = True
            jump_sound.play()

        # Movimiento vertical
        if self.en_salto:
            self.knightrect.move_ip(0, self.velocidad_salto)
            self.velocidad_salto += 1
            if self.velocidad_salto > 4:
                self.en_salto = False
                self.velocidad_salto = self.velocidad_salto_original
        else:
            if not self.is_on_platform(plataformas):
                self.knightrect.move_ip(0, self.velocidad_caida)

            if self.knightrect.top > ALTO:
                pygame.quit()
                sys.exit()

    def is_on_platform(self, plataformas):
        for plataforma in plataformas:
            if (
                plataforma.rect.top <= self.knightrect.bottom <= plataforma.rect.top + 10 and
                plataforma.rect.left < self.knightrect.centerx < plataforma.rect.right
            ):
                self.knightrect.move_ip(0,plataforma.velocidad) #Si se encuentra en una plataforma cae a la vez que la plataforma
                self.plataforma_nueva = plataforma
                return True
        return False

    def draw(self, ventana):
        ventana.blit(self.image, self.knightrect)
