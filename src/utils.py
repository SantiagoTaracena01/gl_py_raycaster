"""
Universidad del Valle de Guatemala
(CC2018) Gráficos por Computadora
Proyecto 03: Raycaster
Santiago Taracena Puga (20017)
"""

# Librerías importantes para el archivo.
from OpenGL.GL import *
from initial_pattern import INITIAL_PATTERN

# Función que dibuja un pixel con las tecnologías de OpenGL.
def pixel(x, y, color):
  glEnable(GL_SCISSOR_TEST)
  glScissor(x, y, 10, 10)
  glClearColor(*color)
  glClear(GL_COLOR_BUFFER_BIT)
  glDisable(GL_SCISSOR_TEST)

# Función que genera el estado inicial del juego.
def generate_initial_state(width, height):

  # Lista inicial de casillas del juego.
  initial_positions = [[0 for x in range(width)] for y in range(height)]

  # Intercambio y colocación de células en las casillas determinadas.
  for i, row in enumerate(INITIAL_PATTERN):
    for j, number in enumerate(row):
      initial_positions[i][j] = number

  # Retorno del "tablero" inicial.
  return initial_positions

# Función para actualizar el estado del juego.
def update_game_state(current_state, cell_size, colors=((0.0, 0.0, 0.0, 1.0), (1.0, 1.0, 1.0, 1.0))):

  # Inicialización del próximo estado con casillas vacías.
  next_state = [[0 for x in range(len(current_state[0]))] for y in range(len(current_state))]

  # Iteración sobre el estado a construir.
  for i in range(len(next_state)):
    for j in range(len(next_state[0])):

      # Vecinos de la célula actual.
      actual_cell = current_state[i][j]
      neighbor_rows = current_state[(i - 1) : (i + 2)]
      neighbors = []

      # Construcción de la matriz 3x3 que representa la célula y sus vecions.
      for row in neighbor_rows:
        neighbors.append(row[(j - 1) : (j + 2)])

      # Recuento de las células vecinas a la actual
      neighbor_count = sum([sum(row) for row in neighbors]) - actual_cell

      # Casos a tratar en cada uno de los turnos.
      if ((current_state[i][j] == 1) and ((neighbor_count < 2) or (neighbor_count > 3))):
        color = colors[1]
      elif ((current_state[i][j] == 1) and (2 <= neighbor_count <= 3)) or ((current_state[i][j] == 0) and (neighbor_count == 3)):
        next_state[i][j] = 1
        color = colors[1]

      # Color seleccionado para pintar una casilla.
      color = color if (current_state[i][j] == 1) else colors[0]
      pixel((j * cell_size), (i * cell_size), color)

  # Retorno del nuevo estado creado.
  return next_state
