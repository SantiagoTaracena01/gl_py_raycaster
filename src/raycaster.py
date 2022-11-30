"""
Universidad del Valle de Guatemala
(CC2018) Gráficos por Computadora
Proyecto 03: Raycaster
Santiago Taracena Puga (20017)
"""

# Librerías necesarias para el desarrollo de la clase Raycaster.
import math
import colors

# Definición de la clase Raycaster.
class Raycaster(object):

  # Método constructor de la clase Raycaster.
  def __init__(self, screen, walls, enemies):
    self.__screen = screen
    _, _, self.__width, self.__height = self.__screen.get_rect()
    self.__blocksize = 50
    self.__map = []
    self.__walls = walls
    self.__sprites = enemies
    self.clear_z_buffer()
    self.__player = {
      "x": int((1.5 * self.__blocksize)),
      "y": int((1.5 * self.__blocksize)),
      "direction": int((math.pi / 2)),
      "field_of_view": int((math.pi / 3)),
    }

  # Funciones para obtener el ancho y alto del raycaster.
  get_width = lambda self: self.__width
  get_height = lambda self: self.__height

  # Función para rotar la vista del jugador.
  def rotate_player(self, degrees):
    self.__player["direction"] += degrees

  # Función para mover al jugador.
  def move_player(self, axis, steps):
    if ((axis == "x") or (axis == "y")):
      self.__player[axis] += steps

  # Función para limpiar el z_buffer del raycaster.
  def clear_z_buffer(self):
    self.__z_buffer = [999_999 for _ in range(0, int(self.__width / 2))]

  # Función para colocar un punto en la pantalla.
  def point(self, x, y, color=colors.WHITE):
    self.__screen.set_at((x, y), color)

  # Función que dibuja un bloque en la pantalla.
  def block(self, x, y, wall):
    for i in range(x, (x + self.__blocksize)):
      for j in range(y, (y + self.__blocksize)):
        x_texture = int((((i - x) * 128) / self.__blocksize))
        y_texture = int((((j - y) * 128) / self.__blocksize))
        color = wall.get_at((x_texture, y_texture))
        self.point(i, j, color)

  # Función que dibuja un bloque de suelo en el minimapa.
  def ground(self, x, y):
    for i in range(x, (x + self.__blocksize)):
      for j in range(y, (y + self.__blocksize)):
        self.point(i, j, colors.GROUND)

  # Función que carga un mapa en formato .txt.
  def load_map(self, filename):
    with open(filename) as file:
      for line in file.readlines():
        self.__map.append(list(line))

  # Función que dibuja una línea vertical en la pantalla.
  def draw_stake(self, x, h, wall, x_texture):

    # Cálculo de los puntos inicial y final de la línea.
    start_y = int(((self.__height / 2) - (h / 2)))
    end_y = int(((self.__height / 2) + (h / 2)))
    height = (end_y - start_y)

    # Puntos a lo largo de toda la altura calculada.
    for y in range(start_y, end_y):
      y_texture = int((((y - start_y) * 128) / height))
      color = wall.get_at((x_texture, y_texture))
      self.point(x, y, color)

  # Función para lanzar un rayo en dirección del jugador.
  def cast_ray(self, a):

    # Distancia para el lanzamiento del rayo.
    distance = 0

    # Ciclo que simula el lanzamiento del rayo.
    while (True):

      # Coordenadas de visión x e y.
      x = int((self.__player["x"] + (distance * math.cos(a))))
      y = int((self.__player["y"] + (distance * math.sin(a))))

      # Factores i y j del hit.
      i, j = int((x / self.__blocksize)), int((y / self.__blocksize))

      # Si el caracter no es vacío se dibuja una pared.
      if (self.__map[j][i] != " "):

        # Hits en los ejes x e y.
        hitx = (x - (i * self.__blocksize))
        hity = (y - (j * self.__blocksize))

        # Definición de la distancia máxima del hit.
        maxhit = hitx if (1 < hitx < (self.__blocksize - 1)) else hity

        # Textura del bloque.
        x_texture = int(((maxhit * 128) / self.__blocksize))

        # Retorno de la distancia, la pared y su textura.
        return distance, self.__map[j][i], x_texture

      # Dibujo de un nuevo punto en el minimapa y aumento de la distancia.
      self.point(x, y)
      distance += 2

  # Función que dibuja el mapa en la parte izquierda de la pantalla.
  def draw_map(self):
    for x in range(0, 500, self.__blocksize):
      for y in range(0, 500, self.__blocksize):
        i, j = int((x / self.__blocksize)), int((y / self.__blocksize))
        if (self.__map[j][i] != " "):
          self.block(x, y, self.__walls[self.__map[j][i]])
        else:
          self.ground(x, y)

  # Función para dibujar un sprite en la pantalla.
  def draw_sprite(self, sprite):

    # Dirección, distancia y tamaño del sprite.
    sprite_a = math.atan2((sprite["y"] - self.__player["y"]), (sprite["x"] - self.__player["x"]))
    sprite_distance = ((((self.__player["x"] - sprite["x"]) ** 2) + ((self.__player["y"] - sprite["y"]) ** 2)) ** 0.5)
    sprite_size = int(((500 / sprite_distance) * 75))

    # Coordenadas x e y del sprite.
    sprite_x = int(((self.__width / 2) + (sprite_a - self.__player["direction"]) * self.__height / self.__player["field_of_view"] + 250 - sprite_size / 2))
    sprite_y = int(((self.__height / 2) - (sprite_size / 2)))

    # Iteración para dibujar los sprites en la pantalla.
    for x in range(sprite_x, (sprite_x + sprite_size)):
      for y in range(sprite_y, (sprite_y + sprite_size)):

        # Índice sobre el cual iterar el z-buffer.
        index = (x - 500)

        # Verificación de puntos en el z-buffer.
        if ((500 < x < 1000) and (self.__z_buffer[index] >= sprite_distance)):

          # Texturas en x, y, y color del sprite.
          x_texture = int((((x - sprite_x) * 128) / sprite_size))
          y_texture = int((((y - sprite_y) * 128) / sprite_size))
          color = sprite["sprite"].get_at((x_texture, y_texture))

          # Condiciones para dibujar un punto del sprite.
          if (color != colors.TRANSPARENT):
            self.point(x, y, color)
            self.__z_buffer[index] = sprite_distance

  # Función que dibuja los sprites en el mapa del juego.
  def draw_sprite_in_map(self, x, y):
    for i in (x, (x + 5)):
      for j in (y, (y + 5)):
        color = colors.SPRITE_BLUE
        self.point(i, j, color)

  # Función para renderizar un frame del juego.
  def render(self):

    # Funciones para renderizar los componentes de la ventana.
    self.draw_map()
    self.point(self.__player["x"], self.__player["y"], (255, 255, 255))

    # Línea divisoria entre el minimapa y el juego.
    for y in range(0, self.__height):
      for x in (499, 500, 501):
        self.point(x, y, color=colors.BLACK)

    # Dibujo del mapa en 3D del juego.
    for i in range(0, int((self.__width / 2))):

      # Ángulo de disparo del rayo, materiales y puntos para el dibujo de una línea.
      direction = self.__player["direction"] - self.__player["field_of_view"] / 2 + self.__player["field_of_view"] * i / int((self.__width / 2))
      distance, color, x_texture = self.cast_ray(direction)
      x = (int((self.__width / 2)) + i)
      h = (self.__height / (distance * math.cos(direction - self.__player["direction"])) * 70)

      # Dibujo de una línea perteneciente al mapa.
      self.draw_stake(x, h, self.__walls[color], x_texture)
      self.__z_buffer[i] = distance

    # Dibujo de los enemigos en el juego.
    for sprite in self.__sprites:
      self.draw_sprite_in_map(sprite["x"], sprite["y"])
      self.draw_sprite(sprite)

  # Función que comprueba si el jugador ha ganado.
  def player_has_won(self):
    return ((300 < self.__player["x"] < 400) and (400 < self.__player["y"] < 450))
