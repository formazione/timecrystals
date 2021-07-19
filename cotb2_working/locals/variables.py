import pygame


width = 15
height = 9

class Sprite:
    width = 32
    height = 32
tiles = pygame.image.load("assets\\tiles4.png")
NUM_OF_TILES = tiles.get_size()[0] // 32
menu = pygame.image.load("assets\\menu2.png")
diamond = pygame.image.load("assets\\diamond.png")
DOUBLE_SIZE = width*Sprite.width*2, height*Sprite.height*2 + 128