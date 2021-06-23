# editor
import pygame
import os


width = 15
height = 9

class Sprite:
    width = 32
    height = 32

tiles = pygame.image.load("assets\\tiles.png")


_map = [
    "               ", #1
    "   722222226   ", #2
    "  72222222226  ", #3
    "  72  222  26 ",
    "  72722222626  ",
    "  2   222   2  ",
    "               ",
    "000000000000000",
    "111111111111111",
    ]

size = width*Sprite.width, height*Sprite.height
screen = pygame.display.set_mode((size))
screen0 = pygame.Surface(size)

def tiles_pos(bg="") -> tuple:
    """ blit on a secundary surface first """
    if bg != "":
        background(bg)
    tup = []    
    for y, line in enumerate(_map): # y is the number of the line
        for x, str_num in enumerate(line): # x is the number of the column
            if str_num != " ":
                # the image, the position on the screen, the part of the image
                # tup.append([tiles, (x*32, y*32), (int(str_num) * 32, 0, 32, 32)])
                screen0.blit(tiles, (x*32, y*32), (int(str_num) * 32, 0, 32, 32))
    return tup
# Load an image

def background(image):
    house1 = pygame.image.load(image)
    screen0.blit(house1, (0, 0))

pos = tiles_pos()

def print_map():
    print("(")
    for line in _map:
        print(f"\"{line}\",")
    print("),")

def save_map():
    text = ""
    text += "("
    for line in _map:
        text += f"\"{line}\",\n"
    text += "),"
    with open("map.txt", "w") as file:
        file.write(text)
    return text


while True:
  for event in pygame.event.get():
      if event.type == pygame.QUIT:
          pygame.quit()
      if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                save_map()
                os.startfile("map.txt")
      if event.type == pygame.MOUSEBUTTONDOWN:
        mpos = pygame.mouse.get_pos()
        print(mpos)
        x, y = [x//32 for x in mpos]
        print(x, y)
        line = list(_map[y])
        line[x] = " "
        _map[y] = "".join(line)
        print_map()
        screen0.fill(0)
        pos = tiles_pos()
      screen.blit(screen0, (0, 0))
  pygame.display.flip()
