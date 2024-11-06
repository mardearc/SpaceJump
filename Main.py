import pygame
import sys
from Knight import Knight
from Platform import Platform

# Inicializar Pygame
pygame.init()

# Constantes
azul = (128, 191, 255)
white = (255, 255, 255)
ANCHO = 500
ALTO = 700

class Main:
    def __init__(self):
        self.size_ventana = (ANCHO, ALTO)
        self.ventana = pygame.display.set_mode(self.size_ventana)

        self.knight = Knight(225, 0)
        self.knightrect = self.knight.image.get_rect(topleft=(225, 0))
        self.plataformas = [Platform(ANCHO, ALTO, i * 50) for i in range(14)]

        # Control de FPS
        self.clock = pygame.time.Clock()

        # Crear una fuente para la puntuación
        self.font = pygame.font.Font(None, 36)
        self.score = 0

        # Cargar sonidos
        self.jump_sound = pygame.mixer.Sound("jump.wav")
        self.jump_sound.set_volume(0.5)

        # Cargar y reproducir música de fondo
        pygame.mixer.music.load("musica_fondo.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

    def run(self):
        while True:
            self.clock.tick(60)
            self.handle_events()
            self.update()
            self.draw()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def update(self):
        keys = pygame.key.get_pressed()
        self.knight.update(keys, self.plataformas, self.jump_sound)

        # Actualizar plataformas
        for plataforma in self.plataformas:
            plataforma.update(ANCHO, ALTO, self.knightrect)
            # Si aterriza en una nueva plataforma, incrementa la puntuación
            if self.knight.plataforma_nueva is not None and self.knight.plataforma_nueva != self.knight.plataforma_actual:
                if self.knight.plataforma_actual is not None:
                    if self.knight.plataforma_nueva.rect.top < self.knight.plataforma_actual.rect.top:
                        self.score += 1
                    if self.score % 10 == 0 and 1 < self.score < 100:  # Incrementa la velocidad de caída del personaje y de las plataformas
                        for plataforma in self.plataformas:
                            plataforma.velocidad += 0.25
                        self.knight.velocidad_caida += 0.25

                self.knight.plataforma_actual = self.knight.plataforma_nueva  # Actualiza la plataforma actual

    def draw(self):
        self.ventana.fill(azul)

        # Dibujar plataformas
        for plataforma in self.plataformas:
            plataforma.draw(self.ventana)

        # Dibujar caballero y puntuación
        self.knight.draw(self.ventana)
        score_text = self.font.render(f"Puntuación: {self.score}", True, white)
        self.ventana.blit(score_text, (10, 10))

        pygame.display.update()

if __name__ == "__main__":
    Main().run()
