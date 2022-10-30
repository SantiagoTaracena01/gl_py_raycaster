"""
Universidad del Valle de Guatemala
(CC2018) Gráficos por Computadora
Proyecto 03: Raycaster
Santiago Taracena Puga (20017)
"""

# Librerías importantes para el desarrollo del raycaster.
import pygame
from OpenGL.GL import *

# Colores necesarios para el raycaster.
BG_COLOR = (1.0, 1.0, 1.0, 1.0)
PIXEL_COLOR = (0.25, 0.5, 1.0, 1.0)

# Inicialización de la librería pygame.
pygame.init()

# Creación de la pantalla del juego.
screen = pygame.display.set_mode((800, 600), pygame.OPENGL | pygame.DOUBLEBUF)

# Posición inicial de un pixel.
x, y = 0, 0

# Estado de ejecución del raycaster y velocidad de los pixeles.
running = True
speed = 1

# Función que dibuja un pixel con las tecnologías de OpenGL.
def pixel(x, y, color):
  glEnable(GL_SCISSOR_TEST)
  glScissor(x, y, 10, 10)
  glClearColor(*color)
  glClear(GL_COLOR_BUFFER_BIT)
  glDisable(GL_SCISSOR_TEST)

# Ciclo de "vida" del raycaster.
while (running):

  # Limpieza inicial de la pantalla
  glClearColor(*BG_COLOR)
  glClear(GL_COLOR_BUFFER_BIT)

  # Creación de un pixel en la pantalla y movimiento de la misma.
  pixel(x, 100, PIXEL_COLOR)
  x += speed

  # Cambio de la velocidad del raycaster.
  if (x == 800):
    speed = -1
  elif (x == 0):
    speed = 1

  # Flip del framebuffer de pygame.
  pygame.display.flip()

  # Posibilidad de cerrar la ventana creada por pygame. 
  for event in pygame.event.get():
    if (event.type == pygame.QUIT):
      running = False
