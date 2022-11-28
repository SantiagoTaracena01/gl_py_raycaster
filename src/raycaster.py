"""
Universidad del Valle de Guatemala
(CC2018) Gráficos por Computadora
Proyecto 03: Raycaster
Santiago Taracena Puga (20017)
"""

# Librerías necesarias para el desarrollo de la clase Raycaster.
import pygame
import math
import colors

wall1 = pygame.image.load("./textures/wall1.png")
wall2 = pygame.image.load("./textures/wall2.png")
wall3 = pygame.image.load("./textures/wall3.png")
wall4 = pygame.image.load("./textures/wall4.png")
wall5 = pygame.image.load("./textures/wall5.png")

# Cambiar a object
walls = [wall1, wall2, wall3, wall4, wall5]

sprite1 = pygame.image.load("./sprites/sprite1.png")
sprite2 = pygame.image.load("./sprites/sprite2.png")

enemies = [{ "x": 80, "y": 80, "sprite": sprite1 }, { "x": 300, "y": 300, "sprite": sprite2 }]

# Definición de la clase Raycaster.
class Raycaster(object):

  # Método constructor de la clase Raycaster.
  def __init__(self, screen):
    self.__screen = screen
    _, _, self.__width, self.__height = self.__screen.get_rect()
    self.__blocksize = 50
    self.__map = []
    self.player = {
      "x": int(((1.5) * self.__blocksize)),
      "y": int(((1.5) * self.__blocksize)),
      "field_of_view": int((math.pi / 3)),
      "direction": int((math.pi / 3)),
    }
    self.clear_z_buffer()

  # Funciones para obtener el ancho y alto del raycaster.
  get_width = lambda self: self.__width
  get_height = lambda self: self.__height

  # Función para limpiar el z_buffer del raycaster.
  def clear_z_buffer(self):
    self.__z_buffer = [999_999 for _ in range(0, int(self.__width / 2))]

  # Función para colocar un punto en la pantalla.
  def point(self, x, y, color=colors.WHITE):
    self.__screen.set_at((int(x), int(y)), color)

  # Función que dibuja un bloque en la pantalla.
  def block(self, x, y, wall):
    for i in range(x, (x + self.__blocksize)):
      for j in range(y, (y + self.__blocksize)):
        x_texture = int((((i - x) * 128) / self.__blocksize))
        y_texture = int((((j - y) * 128) / self.__blocksize))
        color = wall.get_at((x_texture, y_texture))
        self.point(i, j, color)

  # Función que carga un mapa en formato .txt.
  def load_map(self, filename):
    with open(filename) as file:
      for line in file.readlines():
        self.__map.append(list(line))

  # Función que dibuja una línea vertical en la pantalla.
  def draw_stake(self, x, h, color, x_texture):

    # Cálculo de los puntos inicial y final de la línea.
    start_y = int(((self.__height / 2) - (h / 2)))
    end_y = int(((self.__height / 2) + (h / 2)))
    height = (end_y - start_y)

    # Puntos a lo largo de toda la altura calculada.
    for y in range(start_y, end_y):
      y_texture = int((((y - start_y) * 128) / height))
      texture_color = walls[(int(color) - 1)].get_at((x_texture, y_texture))
      self.point(x, y, texture_color)

  # Función para lanzar un rayo en dirección del jugador.
  def cast_ray(self, a):

    # Constantes importantes para el lanzamiento del rayo.
    distance = 0
    x_origin = self.player["x"]
    y_origin = self.player["y"]

    # Ciclo que simula el lanzamiento del rayo.
    while (True):

      # Coordenadas de visión x e y.
      x = int((x_origin + (distance * math.cos(a))))
      y = int((y_origin + (distance * math.sin(a))))

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

      # Dibujo de un nuevo punto y aumento de la distancia.
      #self.point(x, y)
      distance += 1

  # Función que dibuja el mapa en la parte izquierda de la pantalla.
  def draw_map(self):
    for x in range(0, 500, self.__blocksize):
      for y in range(0, 500, self.__blocksize):
        i, j = int((x / self.__blocksize)), int((y / self.__blocksize))
        if (self.__map[j][i] != " "):
          self.block(x, y, walls[(int(self.__map[j][i]) - 1)])

  # Función que dibuja un punto en la posición del jugador en el mapa.
  def draw_player(self):
    self.point(self.player["x"], self.player["y"])

  # Función para dibujar
  def draw_sprite(self, enemy):

    # Dirección, distancia y tamaño del sprite.
    sprite_direction = math.atan2((enemy["y"] - self.player["y"]), (enemy["x"] - self.player["x"]))
    distance = ((((self.player["x"] - enemy["x"]) ** 2) + ((self.player["y"] - enemy["y"]) ** 2)) ** 0.5)
    sprite_size = int(((500 / distance) * (self.__height / 10)))

    # Coordenadas x e y del sprite.
    sprite_x = int(500 + (sprite_direction - self.player["direction"]) * 500 / self.player["field_of_view"] + sprite_size / 2)
    sprite_y = int(((500 / 2) - (sprite_size / 2)))

    # Iteración para dibujar los sprites en la pantalla.
    for x in range(sprite_x, sprite_x + sprite_size):
      for y in range(sprite_y, sprite_y + sprite_size):

        # Texturas en x, y, y color del sprite.
        x_texture = int((x - sprite_x) * 128 / sprite_size)
        y_texture = int((y - sprite_y) * 128 / sprite_size)
        color = enemy["sprite"].get_at((x_texture, y_texture))
        index = (x - 500)

        # Condiciones para dibujar un punto del sprite.
        if (color != colors.TRANSPARENT) and (x > 500) and (index < len(self.__z_buffer)) and (self.__z_buffer[index] >= distance):
          self.point(x, y, color)
          self.__z_buffer[index] = distance

  # Función para renderizar un frame del juego.
  def render(self):

    # Funciones para renderizar los componentes de la ventana.
    self.draw_map()
    self.draw_player()
    self.clear_z_buffer()
    density = 100

    # Dibujo del minimapa del juego.
    for i in range(0, density):
      direction = self.player["direction"] - self.player["field_of_view"] / 2 + self.player["field_of_view"] * i / density
      distance, color, _ = self.cast_ray(direction)

    # Línea divisoria entre el minimapa y el juego.
    for y in range(500):
      for x in (499, 500, 501):
        self.point(x, y, color=colors.BLACK)

    # Dibujo del mapa en 3D del juego.
    for i in range(0, int(self.__width / 2)):

      # Ángulo de disparo del rayo, materiales y puntos para el dibujo de una línea.
      direction = self.player["direction"] - (self.player["field_of_view"] / 2) + self.player["field_of_view"] * i / int(self.__width / 2)
      distance, color, x_texture = self.cast_ray(direction)
      x = int((self.__width / 2)) + i
      h = (self.__height / ((distance * math.cos(direction - self.player["direction"])) * (self.__height / 10)))

      # Dibujo de una línea si la distancia es menor al valor del z-buffer.
      if (self.__z_buffer[i] >= distance):
        self.draw_stake(x, h, color, x_texture)
        self.__z_buffer[i] = distance

    # Dibujo de los enemigos en el minimapa.
    for enemy in enemies:
      self.point(enemy["x"], enemy["y"], (255, 0, 0))

    # Dibujo de los enemigos en el juego.
    for enemy in enemies:
      self.draw_sprite(enemy)

pygame.init()
screen = pygame.display.set_mode((1000, 500))
raycaster = Raycaster(screen)
raycaster.load_map("./maps/map.txt")

running = True

while (running):

  screen.fill(colors.BLACK, (0, 0, raycaster.get_width() / 2, raycaster.get_height()))
  screen.fill(colors.SKY, (raycaster.get_width() / 2, 0, raycaster.get_width(), raycaster.get_height() / 2))
  screen.fill(colors.GROUND, (raycaster.get_width() / 2, raycaster.get_height() / 2, raycaster.get_width(), raycaster.get_height() / 2))

  raycaster.render()
  raycaster.clear_z_buffer()
  pygame.display.flip()
  
  for event in pygame.event.get():
    if (event.type == pygame.QUIT):
      running = False
    elif (event.type == pygame.KEYDOWN):
      if (event.key == pygame.K_d):
        raycaster.player["direction"] += math.pi / 25
      if (event.key == pygame.K_a):
        raycaster.player["direction"] -= math.pi / 25
      if (event.key == pygame.K_RIGHT):
        raycaster.player["x"] += 10
      if (event.key == pygame.K_LEFT):
        raycaster.player["x"] -= 10
      if (event.key == pygame.K_DOWN):
        raycaster.player["y"] += 10
      if (event.key == pygame.K_UP):
        raycaster.player["y"] -= 10
