"""
Universidad del Valle de Guatemala
(CC2018) Gráficos por Computadora
Proyecto 03: Raycaster
Santiago Taracena Puga (20017)
"""

import pygame

from OpenGL.GL import *

pygame.init()

screen = pygame.display.set_mode((800, 600), pygame.OPENGL | pygame.DOUBLEBUF)

x, y = 0, 0

running = True

def pixel(x, y, color):
  glEnable(GL_SCISSOR_TEST)
  glScissor(x, y, 10, 10)
  glClearColor(*color)
  glClear(GL_COLOR_BUFFER_BIT)
  glDisable(GL_SCISSOR_TEST)

speed = 1

while (running):

  # Limpiar
  glClearColor(0.1, 0.8, 0.2, 1.0)
  glClear(GL_COLOR_BUFFER_BIT)
  
  # Pintar
  pixel(x, 100, (1.0, 0.0, 0.0, 1.0))
  x += speed
  
  if x == 800:
    speed = -1
  elif x == 0:
    speed = 1
  
  # Flip
  pygame.display.flip()
  

  for event in pygame.event.get():
    if (event.type == pygame.QUIT):
      running = False
