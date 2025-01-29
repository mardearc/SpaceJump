import pygame

#Dimensiones pantalla
ANCHO = 500
ALTO = 700

#Velocidades
V_SALTO = -15
VELOCIDAD_CAIDA = 10

#Clase Knight
class Knight:
    def __init__(self, x, y):
        #Cargar imagen
        self.image = pygame.image.load("assets/images/knight_1.png")
        self.image = pygame.transform.scale(self.image, (20, 25))
        self.knightrect = self.image.get_rect(topleft=(x, y))

        #Establecer velocidades
        self.velocidad_salto_original = V_SALTO
        self.velocidad_salto = self.velocidad_salto_original
        self.velocidad_caida = VELOCIDAD_CAIDA

        #Inicializar variables
        self.en_salto = False
        self.esta_girado = True
        self.plataforma_actual = None
        self.plataforma_nueva = None

    #Actualizar
    def update(self, keys, plataformas, jump_sound):
        # Movimiento horizontal
        if keys[pygame.K_LEFT]:  #Mover para la izquierda
            if self.knightrect.left <= 0:
                self.knightrect.move_ip(ANCHO, 0)    #Si se sale de la pantalla aparece por el lado contrario
            self.knightrect.move_ip(-7, 0)
            if self.esta_girado:        #Girar horizontalmente la imagen
                self.image = pygame.transform.flip(self.image, 1, 0)
                self.esta_girado = False
        elif keys[pygame.K_RIGHT]:  #Mover para la derecha
            if self.knightrect.right >= ANCHO:
                self.knightrect.move_ip(-ANCHO, 0)  #Si se sale de la pantalla aparece por el lado contrario
            self.knightrect.move_ip(7, 0)
            if not self.esta_girado:        #Girar horizontalmente la imagen
                self.image = pygame.transform.flip(self.image, 1, 0)
                self.esta_girado = True

        #Control del salto
        if keys[pygame.K_SPACE] and not self.en_salto and self.is_on_platform(plataformas):
            self.en_salto = True
            jump_sound.play()

        #Movimiento vertical
        if self.en_salto:  #Si está en salto, se produce el salto
            self.knightrect.move_ip(0, self.velocidad_salto)
            self.velocidad_salto += 1  #Disminuir la velocidad para simular gravedad
            if self.velocidad_salto > 4:
                self.en_salto = False
                self.velocidad_salto = self.velocidad_salto_original
        else:   #Si no está en salto ni sobre una plataforma el caballero cae
            if not self.is_on_platform(plataformas):
                self.knightrect.move_ip(0, self.velocidad_caida)


    #Metodo para saber si está sobre una plataforma
    def is_on_platform(self, plataformas):
        for plataforma in plataformas:
            if (
                plataforma.rect.top <= self.knightrect.bottom <= plataforma.rect.top + 10 and
                plataforma.rect.left < self.knightrect.centerx < plataforma.rect.right
            ):
                self.knightrect.move_ip(0,plataforma.velocidad) #Si se encuentra en una plataforma, el caballero cae a la vez que la plataforma
                self.plataforma_nueva = plataforma
                return True
        return False
    #Dibujar
    def draw(self, ventana):
        ventana.blit(self.image, self.knightrect)
