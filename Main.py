import pygame
import sys
from Knight import Knight
from Platform import Platform
from Hammer import Hammer
import itertools
#Inicializar Pygame
pygame.init()

#Constantes
azul = (128, 191, 255)
white = (255, 255, 255)
ANCHO = 500
ALTO = 700

#Cargar sonido
level_up_sound = pygame.mixer.Sound("assets/sounds/level_up.mp3")
level_up_sound.set_volume(0.7)

lose_sound = pygame.mixer.Sound("assets/sounds/lose.mp3")
lose_sound.set_volume(0.7)

pygame.display.set_caption("Knight Jump")

#Clase Main
class Main:
    def __init__(self):
        self.velocidad_martillo = 2

        #Inicializar ventana
        self.size_ventana = (ANCHO, ALTO)
        self.ventana = pygame.display.set_mode(self.size_ventana)

        #Inicializar caballero
        self.knight = Knight(225, 0)
        self.knightrect = self.knight.knightrect

        #Inicializar plataformas usando el generador
        self.plataformas = list(itertools.islice(self.generador_plataformas(ANCHO, ALTO), 14))

        #Martillos
        self.martillos = list()
        self.ultimo_martillo = 0
        self.tiempo_entre_martillos = 1600

        #Control de FPS
        self.clock = pygame.time.Clock()

        #Crear una fuente para la puntuación
        self.font = pygame.font.Font(None, 36)
        self.score = 0

        #Fondo
        self.fondo1 = pygame.image.load("assets/images/fondo1.png")
        self.fondo2 = pygame.image.load("assets/images/fondoNubes.png")
        self.y = 0
        self.velocidad_fondo = 1
        self.usar_primer_fondo = True

        # Cargar sonidos
        self.jump_sound = pygame.mixer.Sound("assets/sounds/jump.wav")
        self.jump_sound.set_volume(0.5)

        self.enJuego = True

        # Cargar y reproducir música de fondo
        pygame.mixer.music.load("assets/sounds/musica_fondo.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

    #Metodo para poner en funcionamiento el juego
    def run(self):
        while self.enJuego:
            self.clock.tick(60)
            self.handle_events()
            self.update()
            self.draw()

    #Generador de plataformas
    def generador_plataformas(self, ancho, alto):
        offset_y = 50
        while True:
            yield Platform(ancho, alto, offset_y)
            offset_y += 50  # Ajuste de la posición y de cada nueva plataforma

    #Generador de martillos
    def generador_martillos(self, ancho):
        while True:
            yield Hammer(ancho,self.velocidad_martillo)

    #Manejo de eventos (salir del juego)
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    #Actualizar los componentes
    def update(self):
        keys = pygame.key.get_pressed()
        self.knight.update(keys, self.plataformas, self.jump_sound)

        #Actualizar fondo
        self.y += self.velocidad_fondo

        #Cambiar a segundo fondo cuando el primer fondo desaparezca
        if self.usar_primer_fondo and self.y + ALTO >= self.fondo1.get_rect().height: #Se suma el ALTO a self.y porque la primera imagen de fondo mide ALTO*2
            self.usar_primer_fondo = False
            self.y = 0  # Reiniciar la posición del fondo

        #Volver al menu si pierde, parar la música
        if self.knightrect.top > ALTO:      #Si el knight cae al fondo se termina la partida
            pygame.mixer_music.stop()
            lose_sound.play()
            pygame.time.wait(1000)
            self.enJuego = False

        for martillo in self.martillos:  #Manejar si colisiona con un martillo
            if self.knightrect.colliderect(martillo.rotated_rect):  #Si el knight toca el martillo se termina la partida
                pygame.mixer_music.stop()
                lose_sound.play()
                pygame.time.wait(1000)
                self.enJuego = False

        #Actualizar plataformas
        for plataforma in self.plataformas:
            plataforma.update(ANCHO, ALTO)

        # Comprobar si aterriza en una nueva plataforma
        if self.knight.plataforma_nueva and self.knight.plataforma_nueva != self.knight.plataforma_actual:
            if self.knight.plataforma_actual:
                if self.knight.plataforma_nueva.rect.top < self.knight.plataforma_actual.rect.top:
                    self.score += 1

                    # Aumentar velocidad cada 10 puntos en el rango 10-99
                    if 10 <= self.score < 100 and self.score % 20 == 0:
                        self.aumentar_velocidad()
                        level_up_sound.play()

            # Actualizar plataforma actual
            self.knight.plataforma_actual = self.knight.plataforma_nueva

        # Generar nuevas plataformas si alguna ha salido de la pantalla
        if self.plataformas[-1].rect.top >= ALTO:
            self.plataformas.pop(0)  # Elimina la plataforma más antigua
            nueva_plataforma = next(self.generador_plataformas(ANCHO, ALTO))
            self.plataformas.append(nueva_plataforma)  # Añade una nueva plataforma

        #A partir de la puntuación 20 empiezan a caer martillos
        if self.score >= 20:
            # Obtener el tiempo actual
            tiempo_actual = pygame.time.get_ticks()

            # Generar martillos cada x segundos
            if tiempo_actual - self.ultimo_martillo >= self.tiempo_entre_martillos:
                # Generar un nuevo martillo
                self.martillos.append(next(self.generador_martillos(ANCHO)))
                # Actualizar el último tiempo de generación
                self.ultimo_martillo = tiempo_actual

        
        #Actualizar todos los martillos
        for martillo in self.martillos:
            martillo.update()

    #Metodo para aumentar la velocidad progresivamente
    def aumentar_velocidad(self):
        for plataforma in self.plataformas:  #Cuando aumente la velocidad de plataformas tambien lo hace la del caballero
            plataforma.velocidad += 1
        self.velocidad_fondo += 1
        self.knight.velocidad_caida += 1
        if 20 <= self.score <= 200:    #Si la puntuacion supera a 20 la velocidad de las plataformas y martillos aumenta
            self.tiempo_entre_martillos -= 200
            self.velocidad_martillo += 1
            for martillo in self.martillos:
                martillo.velocidad = self.velocidad_martillo

    #Dibujar
    def draw(self):
        #Movimiento del fondo
        if self.usar_primer_fondo:
            # Dibujar el primer fondo
            y_relativa = self.y + ALTO % self.fondo1.get_rect().height #Se suma el ALTO porque la primera imagen de fondo mide ALTO*2
            self.ventana.blit(self.fondo1, (0, y_relativa - self.fondo1.get_rect().height))
            if y_relativa < ALTO:
                self.ventana.blit(self.fondo1, (0, y_relativa))
        else:
            #Dibujar el segundo fondo
            y_relativa = self.y % self.fondo2.get_rect().height
            self.ventana.blit(self.fondo2, (0, y_relativa - self.fondo2.get_rect().height))
            if y_relativa < ALTO:
                self.ventana.blit(self.fondo2, (0, y_relativa))

        #Dibujar plataformas
        for plataforma in self.plataformas:
            plataforma.draw(self.ventana)

        #Dibujar caballero y puntuación
        self.knight.draw(self.ventana)
        score_text = self.font.render(f"Puntuación: {self.score}", True, white)
        self.ventana.blit(score_text, (10, 10))

        #Dibujar martillo
        for martillo in self.martillos:
            martillo.draw(self.ventana)

        pygame.display.update()


if __name__ == "__main__":
    Main().run()
