"""
Universidad del Valle de Guatemala
(CC2018) Gráficos por Computadora
Proyecto 03: Raycaster
Santiago Taracena Puga (20017)
"""

# Librerías necesarias para el archivo.
import glm
import random
import pygame
import numpy
import ctypes
from OpenGL.GL import *
from OpenGL.GL.shaders import *

# Ancho y alto de la ventana creada por pygame.
WIDTH = 800
HEIGHT = 600

# Constantes importantes del visor.
SLOTS = 3
BYTES = 4

# Inicialización de pygame.
pygame.init()

# Pantalla de pygame.
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.OPENGL | pygame.DOUBLEBUF)

# Código del vertex shader del visor.
vertex_shader = """
#version 460
layout (location = 0) in vec3 position;
layout (location = 1) in vec3 vertexColor;
uniform mat4 myMatrix;
out vec3 ourColor;
void main() {
  gl_Position = myMatrix * vec4(position, 1.0f);
  ourColor = vertexColor;
}
"""

# Código del fragment shader del visor.
fragment_shader = """
#version 460
layout (location = 0) out vec4 fragColor;
uniform vec3 color;
in vec3 ourColor;
void main() {
  fragColor = vec4(color, 1.0f);
}
"""

# Proceso de compilación y uso de los shaders.
compiled_vertex_shader = compileShader(vertex_shader, GL_VERTEX_SHADER)
compiled_fragment_shader = compileShader(fragment_shader, GL_FRAGMENT_SHADER)
shader = compileProgram(compiled_vertex_shader, compiled_fragment_shader)
glUseProgram(shader)

# Array de vértices a dibujar por el visor.
vertex_data = numpy.array([
  -0.5, -0.5, 0.0,
  0.5, -0.5, 0.0,
  0.0, 0.5, 0.0,
], dtype=numpy.float32)

# Creación del vertex buffer object.
vertex_buffer_object = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer_object)
glBufferData(GL_ARRAY_BUFFER, vertex_data.nbytes, vertex_data, GL_STATIC_DRAW)

# Creación del vertex array object.
vertex_array_object = glGenVertexArrays(1)
glBindVertexArray(vertex_array_object)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, (SLOTS * BYTES), ctypes.c_void_p(0))
glEnableVertexAttribArray(0)

# Función para recalcular la matrix de transformación del visor.
def recalculate_transformation_matrix(angle):

  # Cálculos entre matrices para la obtención de la matriz de modelo del visor.
  identity = glm.mat4(1)
  translate = glm.translate(identity, glm.vec3(0.0, 0.0, 0.0))
  rotate = glm.rotate(identity, glm.radians(angle), glm.vec3(0.0, 1.0, 0.0))
  scale = glm.scale(identity, glm.vec3(1.0, 1.0, 1.0))
  model = (translate * rotate * scale)

  # Matrices de vista, proyección y viewport del visor.
  view = glm.lookAt(glm.vec3(0, 0, 5), glm.vec3(0, 0, 0), glm.vec3(0, 1, 0))
  projection = glm.perspective(glm.radians(45), (4 / 3), 0.1, 1000.0)
  glViewport(0, 0, WIDTH, HEIGHT)

  # Matriz de transformación final y almacenamiento de la misma.
  my_matrix = (projection * view * model)
  my_matrix_location = glGetUniformLocation(shader, "myMatrix")
  glUniformMatrix4fv(my_matrix_location, 1, GL_FALSE, glm.value_ptr(my_matrix))

# Color del fondo de pantalla.
glClearColor(0.0, 0.0, 0.0, 1.0)

# Estado de ejecución del visor.
running = True
degrees = 0

# Ciclo de ejecución del visor.
while (running):

  # Limpieza del color buffer bit.
  glClear(GL_COLOR_BUFFER_BIT)

  # Colores aleatorios del modelo a visualizar.
  first_color = random.random()
  second_color = random.random()
  third_color = random.random()

  # Color pasado al shader vertex.
  full_color = glm.vec3(first_color, second_color, third_color)
  first_color_location = glGetUniformLocation(shader, "color")
  glUniform3fv(first_color_location, 1, glm.value_ptr(full_color))

  # Cambio del ángulo en el que se encuentra el modelo.
  recalculate_transformation_matrix(degrees)

  # Espera para que el modelo no vaya tan rápido.
  pygame.time.wait(100)

  # Dibujo de los triángulos del vertex buffer object.
  glDrawArrays(GL_TRIANGLES, 0, 3)

  # Flip de pygame para actualizar la pantalla.
  pygame.display.flip()

  # Eventos a realizar con el teclado o los botones de la ventana.
  for event in pygame.event.get():
    if (event.type == pygame.QUIT):
      running = False
    if (event.type == pygame.KEYDOWN):
      if (event.key == pygame.K_a):
        degrees -= 10
      if (event.key == pygame.K_d):
        degrees += 10
