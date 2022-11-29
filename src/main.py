"""
Universidad del Valle de Guatemala
(CC2018) Gráficos por Computadora
Proyecto 03: Raycaster
Santiago Taracena Puga (20017)
"""

# Librerías necesarias para el desarrollo del archivo main.py.
import math
import pygame
import colors
from raycaster import Raycaster

# Dimensiones de la ventana del juego.
WIDTH = 1000
HEIGHT = 500

# Muros cargados para el proyecto.
wall1 = pygame.image.load("./walls/hyrule_castle_wall.png")
wall2 = pygame.image.load("./walls/hyrule_castle_corner.png")
wall3 = pygame.image.load("./walls/hyrule_castle_flag.png")
wall4 = pygame.image.load("./walls/hyrule_castle_deco.png")
wall5 = pygame.image.load("./walls/hyrule_castle_curtain.png")

# Sprites cargados para el proyecto.
sprite1 = pygame.image.load("./sprites/sprite1.png")
sprite2 = pygame.image.load("./sprites/sprite2.png")

# Muros y enemigos del proyecto.
walls = { "1": wall1, "2": wall2, "3": wall3, "4": wall4, "5": wall5 }
enemies = [{ "x": 220, "y": 425, "sprite": sprite1 }, { "x": 320, "y": 420, "sprite": sprite2 }]

# Incialización de variables de pygame y el raycaster.
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.DOUBLEBUF | pygame.HWACCEL)
raycaster = Raycaster(screen, walls, enemies)
raycaster.load_map('./maps/map.txt')

# Música de fondo para el juego.
pygame.mixer.music.load("./music/overworld.wav")
pygame.mixer.music.play(-1)

# Variable que determina si el juego está corriendo o no.
running = True

# Ciclo infinito que hace que el juego corra.
while (running):

  # Suelo y techo del mapa del juego.
  screen.fill(colors.SKY, (raycaster.get_width() / 2, 0, raycaster.get_width(), raycaster.get_height() / 2))
  screen.fill(colors.GROUND, (raycaster.get_width() / 2, raycaster.get_height() / 2, raycaster.get_width(), raycaster.get_height() / 2))

  # Renderización de un frame del juego y flip de la pantalla.
  raycaster.render()
  pygame.display.flip()

  # Eventos del juego activados con el teclado.
  for event in pygame.event.get():
    if (event.type == pygame.QUIT):
      running = False
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_a:
        raycaster.rotate_player(((-1 * math.pi) / 20))
      elif event.key == pygame.K_d:
        raycaster.rotate_player((math.pi / 20))
      elif event.key == pygame.K_RIGHT:
        raycaster.move_player("x", 10)
      elif event.key == pygame.K_LEFT:
        raycaster.move_player("x", -10)
      elif event.key == pygame.K_UP:
        raycaster.move_player("y", 10)
      elif event.key == pygame.K_DOWN:
        raycaster.move_player("y", -10)
