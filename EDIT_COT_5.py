# editor_mode
import pygame
import os
from levels2b import *


pygame.init()

columns = 15
rows = 9
spr_width = 32
spr_height = 32
tiles = pygame.image.load("assets\\tiles4.png")
NUM_OF_TILES = tiles.get_size()[0] // 32
menu = pygame.image.load("assets\\menu2.png")
diamond = pygame.image.load("assets\\diamond.png")
diamond2 = pygame.image.load("assets\\crystal2.png")
size = WD, HG = columns*spr_width, rows*spr_height
DOUBLE_SIZE = WD*2, HG*2 + 128


# The first room
_map = layout[1]
# _map[2][1] = "P"
print(_map)
# The size is given by the 
print(f"{size=}")
screen = pygame.display.set_mode(DOUBLE_SIZE)
screen0 = pygame.Surface((WD, HG + 64))

background = pygame.image.load("assets\\background.png")

def button(screen, position, text, size=50, color="yellow", bg="darkblue"):
    """ draws a rectangle and some lines and then blits the text on it """
    font = pygame.font.SysFont("Arial", size)
    text_render = font.render(text, 1, color)
    x, y, w , h = text_render.get_rect()
    x, y = position
    # line(surface, color, (startingpoint), (endingpoint), thickness)
    screen2 = pygame.Surface((w + 10, h + 10))
    pygame.draw.line(screen0, (150, 150, 150), (x, y), (x + w + 1, y), 5)
    pygame.draw.line(screen0, (150, 150, 150), (x, y - 2), (x, y + h), 5)
    pygame.draw.line(screen0, (50, 50, 50), (x, y + h), (x + w , y + h), 5)
    pygame.draw.line(screen0, (50, 50, 50), (x + w , y+h), [x + w , y], 5)
    # the rectangle that makes the background
    pygame.draw.rect(screen0, bg, (x, y, w + 2, h))
    return screen0.blit(text_render, (x, y))
    # return screen0

b1 = button(screen, (400, 300), "Quit", size=40, color="red", bg="white")

riga = 0
def blit_tiles(bg="") -> tuple:
    """ blit on a secundary surface first """
    if bg != "":
        screen0.blit(background, (0, 0))
    tup = []    
    for y, line in enumerate(_map): # y is the number of the line
        for x, str_num in enumerate(line): # x is the number of the column
            if str_num != " " and str_num != "P":
                if int(str_num) < 100 :
                    # takes a part of the tilesheet based on the number
                    level = 0
                    # CHOOSE THE SECOND SET OF 11 TILES
                    if int(str_num) > 10 and int(str_num) < 22:
                        str_num = str(int(str_num) - 11)
                        level = 32
                    # choose the 3rd set of tiles
                    elif int(str_num) > 20:
                        str_num = str(int(str_num) - 22)
                        level = 64
                    # Next set of tile:
                    # elif int(str_num) > 30:
                    #     str_num = str(int(str_num) - 33)
                    #     level = 96

                    screen0.blit(tiles, (x*32, y*32), (int(str_num) * 32, 0 + level, 32, 32))
                elif str_num == "100":
                    screen0.blit(diamond, (x*32, y*32))
                elif str_num == "101":
                    screen0.blit(diamond2, (x*32, y*32))

    screen0.blit(tiles, (0, 320), (0, riga, 32* NUM_OF_TILES, 32))

    return tup
# Load an image
pos = blit_tiles("bg")

font = pygame.font.SysFont("Arial", 14)
msg = font.render("Hello", 1, (0, 255, 0))
def message(text):
    global msg
    # screen0.fill(0, (0, 288, 480, 32))
    msg = font.render(text, 1, (0, 255, 0))
    # screen0.blit(msg, (0, 288))

    




# def print_map():
    # print("(")
    # for line in _map:
    #     print(f"\"{line}\",")
    # print("),")


def save_map(levels="levels.txt"):
    """ This changes all the maps with the new ones """
    global layout
    
    text = "layout = ["
    # This puts all the tuples of the maps into a list
    layout[0] = layout[1]
    for eachmap in layout:
        text += "["
        for line in eachmap:
            text += f"{list(line)},\n"
        text += "],"
    text += "]"
    print("You pressed s: this is saved into levels2.py")
    message("You pressed s: this is saved into levels2.py")
    # one map only
    with open(levels, "w") as file:
        file.write(text)
    # os.system(f"""start "" "C:\Program Files\Sublime Text 3\sublime_text.exe" {levels} """)

    return text


def get_pos() -> tuple:
    mpos = pygame.mouse.get_pos()
    # print(f"{mpos=}")
    # I multiply by 2 because I doubled the screen
    x = mpos[0]// 64
    y = mpos[1]// 64
    # print(x, y)
    return x, y

def update_screen():
    ''' Clear and show tiles '''

    screen0.fill(0)
    pygame.display.set_caption(f"Room n. {room}")
    blit_tiles("ciao")
    screen0.blit(msg, (0, 288))


def get_tile():
    rect_tile = (x * 32, 0, 32, 32)
    tile = tiles.subsurface(rect_tile)
    return tile

tiles_visible = 0
editor_mode = 0
help = """

pythonprogramming.altervista.org

                Commands
                ========
ARROW KEYS TO CHANGE room
MOUSE CLICK
    LEFT ADD TILE
    RIGHT DELETE Tiles
    MIDDLE ADD CRYSTAL
R REVERSE ROOM
M ADD COPY OF ROOM NEXT
N ADD COPY ROOM AT THE END
"""
room_len = len(layout)
room = 1
# print(f"{room_len=}")
menu_visible = 0

def goto_room(room_num, msg=""):
    global _map

    _map = layout[room]
    update_screen()
    if msg == "":
        message(f"you went int room {room}")


def position_tile(symbol):
    """ get the x and y and put in the map list the symbol for that tile """
    message("You positioned a tile in this room")
    x, y = get_pos()
    layout[room][y][x] = symbol
    update_screen()

message("You are in Room 1, choose a tile down here")
tile = pygame.Surface((0, 0))
clock = pygame.time.Clock()
tile_chosen_number = "0"
while True:
  
  for event in pygame.event.get():
    
      if event.type == pygame.QUIT:
          pygame.quit()
  

      # Iterate through the 3 lines of tiles
      if event.type == pygame.MOUSEBUTTONDOWN:
          if event.button == 4 or event.button == 5:
              if riga == 0:
                riga = 32
              elif riga == 32:
                riga = 64

              elif riga == 64:
                riga = 0
            # to add a 4th level ol tiles
                # riga = 96 # change this above

            # and add this
              # elif riga == 96:
              #   riga = 0
              print(riga)
              # then go in blit_tiles
          if b1.collidepoint(
            pygame.mouse.get_pos()[0]//2,
            pygame.mouse.get_pos()[1]//2,
            ):
              os.system("py GAME4c.py")
    
      if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                pygame.quit()

            if event.key == pygame.K_LEFT:
                if room > 1:
                    room -= 1
                goto_room(room)
            if event.key == pygame.K_RIGHT:
                if room < room_len - 1:
                    room += 1
                goto_room(room)

            if event.key in range(47, 58):
                riga = (event.key - 49) * 32 
                print(riga)

            if event.key == pygame.K_r:
                message("you pressed r: room is reversed")
                for n, line in enumerate(_map):
                    line = line[::-1]
                    _map[n] = line
                layout[room] = _map
                update_screen()


            if event.key == pygame.K_s:
                save_map(levels="levels2b.py")
                message("Map saved with changes")


            # n copy room at the end
            if event.key == pygame.K_n:
                new_map = []
                for n, line in enumerate(_map):
                    line = line[::-1]
                    new_map.append(line)
                layout.append(new_map)
                room_len = len(layout) # updates the lenght of the map
                message(f"you added a room at the end of the map like this one. N.map={room_len}")
                room = room_len - 1
                goto_room(room)

            if event.key == pygame.K_d:
                new_map = []
                for n, line in enumerate(_map):
                    for ni, i in enumerate(line):
                        line[ni] = "-1"
                    new_map.append(line)
                layout.append(new_map)
                room_len = len(layout) # updates the lenght of the map
                # message(f"You deleted all tiles in this map")
                goto_room(room, "You deleted all tiles in the map")

                  
            if event.key == pygame.K_m:
                new_map = []
                for n, line in enumerate(_map):
                    line = line[::-1]
                    new_map.append(line)
                layout.insert(room + 1, new_map)
                room_len = len(layout) # updates the lenght of the map
                message(f"you added a room at the end of the map like this one. N.map={room_len}")
                room += 1
                goto_room(room)
    
            if event.key == pygame.K_k:
                copied = _map
                # update_screen()

            if event.key == pygame.K_l:
                _map = copied
                layout[room] = _map
                # update_screen()

            if event.key == pygame.K_1:
                riga = 0

            if event.key == pygame.K_g:
                os.system("py GAME4b.py")

            # Go to last room
            if event.key == pygame.K_UP:
                room = room_len -1
                # update_screen()

            if event.key == pygame.K_DOWN:
                room = 0
                # update_screen(



            #################################

            #           This is where the map is changed
            #################################



      if get_pos()[1] == 10:
        if pygame.mouse.get_pressed()[0]:
          x = get_pos()[0]
          if x < NUM_OF_TILES:
              rect_tile = (x * 32, 0 + riga, 32, 32)
              tile = tiles.subsurface(rect_tile)
              # 11 is the number of tiles for each row 17.7.21 8:46
              tile_chosen_number = int(x + riga / 32 * 11)

      if get_pos()[1] < 9:
          if pygame.mouse.get_pressed()[0]:
              x, y = get_pos()
              layout[room][y][x] = f"{tile_chosen_number}"
              update_screen()
              print(tile_chosen_number)

          if pygame.mouse.get_pressed()[1]:
              x, y = get_pos()
              if layout[room][y][x] != "100":
                  layout[room][y][x] = "100"
              else:
                layout[room][y][x] = "101"
              update_screen()

          if pygame.mouse.get_pressed()[2]:
              x, y = get_pos()
              layout[room][y][x] = " "
              update_screen()


      update_screen()
      x, y = pygame.mouse.get_pos()
      screen0.blit(tile, (x//2 - 16, y//2 - 16))
  button(screen, (400, 300), "Game", size=20, color="red", bg="white")

  screen.blit(
    pygame.transform.scale(screen0, (DOUBLE_SIZE)),(0, 0))
  pygame.display.flip()
  clock.tick(60)
