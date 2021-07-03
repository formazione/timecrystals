# editor_mode
import pygame
import os


pygame.init()
width = 15
height = 9

class Sprite:
    width = 32
    height = 32

tiles = pygame.image.load("assets\\tiles3.png")
NUM_OF_TILES = tiles.get_size()[0] // 32
menu = pygame.image.load("assets\\menu2.png")
diamond = pygame.image.load("assets\\diamond.png")

from levels3 import *

_map = layout[0]
print(_map)
for y, line in enumerate(_map): # y is the number of the line
    print(line)

from levels2 import *

# Convert string to list to modify elements
for n, eachmap in enumerate(layout):
    layout[n] = list(layout[n])
_map = layout[0]
print(_map)