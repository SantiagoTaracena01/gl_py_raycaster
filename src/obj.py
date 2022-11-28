"""
Universidad del Valle de Guatemala
(CC2018) Gráficos por Computadora
Proyecto 03: Raycaster
Santiago Taracena Puga (20017)
"""

# Definición de la clase Obj para leer archivos .obj.
class Obj(object):

  # Método constructor de la clase Obj.
  def __init__(self, filename):

    # Lectura de todas las líneas del archivo .obj.
    with open(filename) as file:
      self.lines = file.read().splitlines()

    # Definición de las caras y los vértices del archivo.
    self.faces = []
    self.vertices = []
    self.texture_vertices = []
    self.normal_vertices = []
    self.__read_obj_lines()

  # Método que obtiene las caras y los vértices del archivo .obj.
  def __read_obj_lines(self):

    # Iteración sobre cada línea del archivo.
    for line in self.lines:

      # Si la longitud de la línea es menor a tres, no es una línea útil.
      if (len(line.split(" ")) < 3):
        continue

      # Prefijo y valor de cada línea útil del archivo.
      prefix, value = line.split(" ", 1)
      value = value.strip()

      # Obtención de los vértices del archivo.
      if (prefix == "v"):
        values = list(map(float, value.split(" ")))
        for value in values:
          self.vertices.append(value)
