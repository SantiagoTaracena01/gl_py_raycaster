"""
Universidad del Valle de Guatemala
(CC2018) Gráficos por Computadora
Proyecto 03: Raycaster
Santiago Taracena Puga (20017)
"""

# Librerías importantes para el desarrollo del raycaster.
from OpenGL.GL import *
import pygame
import utils
import colors

# Medidas de la ventana del raycaster.
WIDTH = 400
HEIGHT = 300

# Inicialización de la librería pygame.
pygame.init()

# Creación de la pantalla del juego.
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.OPENGL | pygame.DOUBLEBUF)
pygame.display.set_caption("Lab 3: Conway's Game Of Life")

# Estado inicial del juego.
state = utils.generate_initial_state(WIDTH, HEIGHT)

# Estado de ejecución del raycaster y velocidad de los pixeles.
running = True
speed = 1
x = 0

# Ciclo de "vida" del raycaster.
while (running):

  # Limpieza inicial de la pantalla.
  glClearColor(*colors.BG_COLOR)
  glClear(GL_COLOR_BUFFER_BIT)

  # Cambio de estado hacia un nuevo estado del juego.
  state = utils.update_game_state(state, 10, (colors.BG_COLOR, colors.PIXEL_COLOR))

  # Flip del framebuffer de pygame.
  pygame.display.flip()

  # Posibilidad de cerrar la ventana creada por pygame. 
  for event in pygame.event.get():
    if (event.type == pygame.QUIT):
      running = False
