# editor
import pygame



width = 15
height = 9

class Sprite:
    width = 32
    height = 32

tiles = pygame.image.load("assets\\tiles.png")

_map = (
    "               ", #1
    "               ", #2
    "               ", #3
    "  72  22 2 26 ",
    "    7222226    ",
    "      22       ",
    "      22       ",
    "000000000000000",
    "000000000000000",
    "111111111111111",
    )


screen = pygame.display.set_mode((width*Sprite.width, height*Sprite.height))



while True:
  for event in pygame.event.get():
      if event.type == pygame.QUIT:
          pygame.quit()
  for y, line in enumerate(_map): # y is the number of the line
      for x, str_num in enumerate(line): # x is the number of the column
          if str_num != " ":
              screen.blit(tiles, (x*32, y*32), (int(str_num) * 32, 0, 32, 32))
  pygame.display.flip()


