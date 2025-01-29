import pygame
import sys
import pygame.freetype
from Main import Main

# Inicializar Pygame
pygame.init()

# Configuración de pantalla
ANCHO, ALTO = 500, 700
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Knight Jump")

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
VERDE = (0, 255, 50)
TRANSLUCIDO = (0, 0, 0, 128)  # Color negro con transparencia (RGBA)

# Fuente
fuente_ruta = "assets/fonts/PressStart2P-Regular.ttf"
fuente = pygame.font.Font(fuente_ruta, 30)
fuente_grande = pygame.font.Font(fuente_ruta, 40)  # Fuente más grande para la selección

#Clase Menu
class Menu:
    def __init__(self):
        #Opciones
        self.opciones = ["Jugar", "Salir"]
        self.opcion_seleccionada = 0  # Índice de la opción seleccionada

        self.clock = pygame.time.Clock()

        #Fondo
        self.fondo = pygame.image.load("assets/images/castillo.png")
        self.x = 0
        self.velocidad_fondo = 1

        self.juego = Main()

        #Cargar y reproducir música de fondo
        pygame.mixer.music.load("assets/sounds/musica_fondo.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

    #Dibujar menu
    def draw(self):

        #Movimiento del fondo
        self.x += 0.5
        x_relativa = self.x % self.fondo.get_rect().width
        ventana.blit(self.fondo, (x_relativa - self.fondo.get_rect().width, 0))
        if x_relativa < ANCHO:
            ventana.blit(self.fondo, (x_relativa, 0))

        #Dibujar las opciones como si fueran botones
        for i, opcion in enumerate(self.opciones):
            # Calcular el tamaño de la fuente
            if i == self.opcion_seleccionada:
                texto = fuente_grande.render(opcion, True, BLANCO)
            else:
                texto = fuente.render(opcion, True, BLANCO)

            #Posición del texto
            posicion_texto = texto.get_rect(center=(ANCHO // 2, ALTO // 2 + i * 60))

            #Crear un rectángulo con el fondo translúcido
            rectangulo_fondo = pygame.Surface((texto.get_width() + 20, texto.get_height() + 10), pygame.SRCALPHA)
            rectangulo_fondo.fill(TRANSLUCIDO)  # Fondo translúcido
            ventana.blit(rectangulo_fondo, posicion_texto.move(-10, -5))  # Dibujar el rectángulo

            #Dibujar el texto encima del rectánguo
            ventana.blit(texto, posicion_texto)

        pygame.display.flip()

    #Ejecutar alguna de las opciones
    def ejecutar_opcion(self):
        if self.opcion_seleccionada == 0:  # Jugar
            pygame.mixer.music.stop()
            juego = Main()
            juego.run()
        elif self.opcion_seleccionada == 1:  # Salir
            pygame.quit()
            sys.exit()
    #Mover la selección de las opciones
    def mover_seleccion(self, direccion):
        self.opcion_seleccionada = (self.opcion_seleccionada + direccion) % len(self.opciones)
    #Manejo de eventos en el menu
    def ejecutar_menu(self):
        while True:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:  #Mover la selección si se pulsan las flechas
                    if event.key == pygame.K_UP:
                        self.mover_seleccion(-1)
                    elif event.key == pygame.K_DOWN:
                        self.mover_seleccion(1)
                    elif event.key == pygame.K_RETURN:  #Enter para seleccionar opción
                        self.ejecutar_opcion()
            self.draw()


if __name__ == "__main__":
    menu = Menu()
    menu.ejecutar_menu()
