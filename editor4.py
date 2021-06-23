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
    "  72  222  26  ",
    "  72722222626  ",
    "  2   222   2  ",
    "               ",
    "000000000000000",
    "111111111111111",
    ]

size = width*Sprite.width, height*Sprite.height
screen = pygame.display.set_mode((size))
screen0 = pygame.Surface(size)

def blit_tiles(bg="") -> tuple:
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

pos = blit_tiles()

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

def get_pos() -> tuple:
    mpos = pygame.mouse.get_pos()
    print(mpos)
    x, y = [x//32 for x in mpos]
    print(x, y)
    return x, y

def update_screen():
    ''' Clear and show tiles '''
    global pos
    screen0.fill(0)
    pos = blit_tiles()


tiles_visible = 0
editor = 0
while True:

  for event in pygame.event.get():
    
      if event.type == pygame.QUIT:
          pygame.quit()
    
      if event.type == pygame.KEYDOWN:
    
            if event.key == pygame.K_s:
                save_map()
                os.startfile("map.txt")
    
            if event.key == pygame.K_p:
                tiles_visible = 1 if tiles_visible == 0 else 0
                if tiles_visible:
                    screen0.fill(0)
                    screen0.blit(tiles, (0, 0))
                else:
                    update_screen()
    
            if event.key == pygame.K_ESCAPE:
                editor = 0

      if event.type == pygame.MOUSEBUTTONDOWN:
        # if you click when the tiles_visible is on
        if tiles_visible:
            x, y = get_pos()
            print(x, y)
            if y == 0 and x < 8: # tiles are 8
                rect_tile = (x * 32, 0, 32, 32)
                # screen0.blit(tiles, (0, 100), rect_tile)
                menu = 0
                editor = 1
                update_screen()
        if menu == 0 and editor == 0:
            x, y = get_pos()
            line = list(_map[y])
            line[x] = " "
            _map[y] = "".join(line)
            print_map()
            update_screen()

        if menu == 0 and editor:
            x, y = get_pos()
            print(y)
            line = list(_map[y])
            line[x] = f"{x}"
            _map[y] = "".join(line)
            print_map()
            screen0.blit(tiles, (x * 32, y * 32), rect_tile)
            update_screen()
            print(rect_tile)
            
      screen.blit(screen0, (0, 0))
  pygame.display.flip()
