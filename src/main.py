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
zelda = pygame.image.load("./sprites/zelda.png")
elder = pygame.image.load("./sprites/elder.png")
lady = pygame.image.load("./sprites/lady.png")
trader = pygame.image.load("./sprites/trader.png")
kid = pygame.image.load("./sprites/kid.png")
woman = pygame.image.load("./sprites/woman.png")

# Muros y enemigos del proyecto.
walls = { "1": wall1, "2": wall2, "3": wall3, "4": wall4, "5": wall5 }
sprites = [
  { "x": 220, "y": 425, "sprite": zelda },
  { "x": 320, "y": 420, "sprite": elder },
  { "x": 100, "y": 300, "sprite": lady },
  { "x": 450, "y": 225, "sprite": trader },
  { "x": 200, "y": 100, "sprite": kid },
  { "x": 400, "y": 100, "sprite": woman },
]

# Incialización de variables de pygame y el raycaster.
pygame.init()
pygame_clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.DOUBLEBUF | pygame.HWACCEL)
raycaster = Raycaster(screen, walls, sprites)
raycaster.load_map("./maps/map.txt")

# Música de fondo para el juego.
pygame.mixer.music.load("./music/overworld.wav")
pygame.mixer.music.play(-1)

# Efecto de sonido para los pasos en el juego.
step = pygame.mixer.Sound("./music/step.wav")

# Carga de la pantalla inicial del juego.
player_has_started = False
start_screen = pygame.image.load("./screens/start_screen.png").convert()
screen.blit(start_screen, (0, 0))
pygame.display.flip()

# Ciclo que mantiene la carga de la pantalla inicial del juego.
while (not player_has_started):
  for event in pygame.event.get():
    if (event.type == pygame.QUIT):
      exit(0)
    if (event.type == pygame.KEYDOWN):
      if (event.key == pygame.K_SPACE):
        player_has_started = True

# Variable que determina si el juego está corriendo o no.
running = True

# Ciclo infinito que hace que el juego corra.
while (running):

  # Suelo y techo del mapa del juego.
  screen.fill(colors.SKY, (raycaster.get_width() / 2, 0, raycaster.get_width(), raycaster.get_height() / 2))
  screen.fill(colors.GROUND, (raycaster.get_width() / 2, raycaster.get_height() / 2, raycaster.get_width(), raycaster.get_height() / 2))

  # Contador de FPS del juego.
  fps_font = pygame.font.Font("./fonts/mononoki.ttf", 16)
  fps_span = fps_font.render(f"{round(pygame_clock.get_fps(), 2)} FPS", True, colors.WHITE, colors.BLACK)
  fps_span_rect = fps_span.get_rect()
  fps_span_rect.center = (950, 25)
  screen.blit(fps_span, fps_span_rect)
  pygame_clock.tick()

  # Renderización de un frame del juego y flip de la pantalla.
  raycaster.render()
  pygame.display.flip()

  # Eventos del juego activados con el teclado.
  for event in pygame.event.get():
    if (event.type == pygame.QUIT):
      running = False
    if event.type == pygame.KEYDOWN:
      pygame.mixer.Sound.play(step)
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
