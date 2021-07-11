import pygame, time, random, math
from pygame.locals import *
import sys


pygame.init()
pygame.display.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((480, 270))


layout =  ("2222222222     ",
           "22 222         ",
           "222222         ",
           "2       22     ",
           "2      222     ",
           "2P    22 2     ",
           "2222222222   C ",
           "22 222 22200000",
           "222222222211111",
           )


spr_player = pygame.image.load("assets/lily.png").convert_alpha()
spr_tiles = pygame.image.load("assets/tiles.png").convert_alpha()
spr_crystal1 = pygame.image.load("assets/crystal.png").convert_alpha()
spr_crystal2 = pygame.image.load("assets/crystal2.png").convert_alpha()
spr_particle = pygame.image.load("assets/particles.png").convert_alpha()
spr_number = pygame.image.load("assets/number.png").convert_alpha()
background = pygame.image.load("assets/background.png").convert()
title = pygame.image.load("assets/title.png").convert()






for line in layout:
    for tile in line:
        print(tile)
try:
    while True:
        ### level generation
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
        load = []
        remove = []
        for line in layout:
            c = 0
            r = 0
            for tile in line:
                if tile == "2":
                    screen.blit(spr_crystal1, (c, r))
                c += 32
            r += 32


        pygame.display.flip()
        clock.tick(60)
except pygame.error as e:
    print()
    print("We have a problem:\n")
    print(e)
    print()
    pygame.quit()


