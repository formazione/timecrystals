# editor_mode
import pygame
import os
from convert_level03 import *


layout = convert_level3_to_list()
''' v- 2.5
levels are in level3.py

Now the level3.py file contains rooms in this format

'01 __ 01 01 01 01 01 01 01 01 01 01 01 01 01', '01 __ __ __ __ __ __ __ __ 01 01 CC __ __ __', '01 __ __ __ __ __ __ __ __ 01 01 __ __ __ __', '01 __ __ __ __ __ __ __ __ 01 01 04 __ __ __', '06 06 06 07 __ __ __ __ __ __ __ __ __ __ __', '06 CC __ CC __ __ __ __ __ CC __ __ __ __ __', '02 __ __ __ __ __ __ __ __ __ __ __ __ __ __'

so that we can use up to 99 tiles (but to any
number indeed, the 2 digit are just for esthetic,
so that you can see the structure even in the
list mode)


they are converted in old format
['1', ' ', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1'], ['1', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '1', '1', 'CC', ' ', ' ', ' '],
by convert_level03 module and convert_level3_to_list

'''

# ========== working with level2.py ===== 
# from levels2 import *
# Convert string to list to modify elements
# for n, eachmap in enumerate(layout[1]):
#     layout[n] = list(layout[n])


_map = layout[1]

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
DOUBLE_SIZE = width*Sprite.width*2, height*Sprite.height*2 + 128



size = width*Sprite.width, height*Sprite.height
screen = pygame.display.set_mode(DOUBLE_SIZE)
screen0 = pygame.Surface((width*Sprite.width, height*Sprite.height + 64))
def blit_tiles(bg="") -> tuple:
    """ blit on a secundary surface first """
    if bg != "":
        background(bg)
    tup = []    
    for y, line in enumerate(_map): # y is the number of the line
        for x, str_num in enumerate(line): # x is the number of the column
            if str_num not in "CC PP":
                # the image, the position on the screen, the part of the image
                # tup.append([tiles, (x*32, y*32), (int(str_num) * 32, 0, 32, 32)])
                screen0.blit(tiles, (x*32, y*32), (int(str_num) * 32, 0, 32, 32))
            if str_num == "CC":
                screen0.blit(diamond, (x*32, y*32))
    screen0.blit(tiles, (0, 320))


blit_tiles()

font = pygame.font.SysFont("Arial", 14)
def message(text):
    # print(text)
    msg = font.render(text, 1, (0, 255, 0))
    screen0.blit(msg, (0, 288))



# def print_map():
#     print("(")
#     # for line in _map:
#         print(f"\"{line}\",")
#     print("),")


def save_map(levels="levels.txt"):
    """ This changes all the maps with the new ones """
    global layout
    
    text = "layout = ["
    # This puts all the tuples of the maps into a list
    layout[0] = layout[1]
    for eachmap in layout:
        text += "(\n"
        for line in eachmap:
            text += "'"
            for n, item in enumerate(line):
                if item == "C":
                    text += "CC"
                elif item == " ":
                    text += "__"
                elif item.isdigit():

                    if int(item) < 9:
                        text += f"0{item}"
                # avoid space after the last item
                # that causes a "" empty item error
                if n < 14:
                    text += " "
            text += "',\n"
            # text += f"\"{line}\",\n"
        text += "),\n\n"
    text += "]"
    # print("You pressed s: this is saved into levels3.py")
    message("You pressed s: this is saved into levels3.py")
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

    pygame.display.set_caption(f"Room n. {room}")
    screen0.fill(0)
    blit_tiles()


def get_tile():
    rect_tile = (x * 32, 0, 32, 32)
    tile = tiles.subsurface(rect_tile)
    return tile

tiles_visible = 0
editor_mode = 0
tile_chosen_number = 0
help = """

pythonprogramming.altervista.org

                Commands
                ========
t = show tiles
r = reverse tiles
s = append tiles to file
n = copied room at the end
m = copied room in new next level
0,1,2.... = go into a room
arrows left and right = iterate
               the rooms
arrow Up => last room
arrow down => first room
h = help

"""
room_len = len(layout)
room = 1
# print(f"{room_len=}")
menu_visible = 0

def goto_room(room_num):
    # global _map

    _map = layout[room_num]
    update_screen()
    message(f"you went int room {room_num}")

def position_tile(symbol):
    """ get the x and y and put in the map list the symbol for that tile """
    message("You positioned a tile in this room")
    x, y = get_pos()
    line = list(_map[y])
    line[x] = symbol
    # _map[y] = "".join(line)
    layout[room][y] = line
    # print(f"{layout[room][y]=}")
    # print(f"{layout[room]=}")
    # print(f"{room}")
    # print(f"{[y]=}")
    update_screen()


tile = pygame.Surface((0, 0))
clock = pygame.time.Clock()
while True:
  
  for event in pygame.event.get():
    
      if event.type == pygame.QUIT:
          pygame.quit()
    
      if event.type == pygame.KEYDOWN:

            # CHANGE ROOM when you press a key ====== ROOM NAVIGATOR ====
            if event.key == pygame.K_LEFT:
                if room > 1:
                    room -= 1
                    goto_room(room)
                    # message(f"you went int room {room}")
                    # save_map(levels="levels2.py")
                    # pygame.display.set_caption(f"Room n. {room}")
                # goto_room(room)
            if event.key == pygame.K_RIGHT:
                if room < room_len - 1:
                    room += 1
                    message(f"you went int room {room}")
                    goto_room(room)
                    # save_map(levels="levels2.py")
                # goto_room(room)

            if event.key in range(47, 58):
                if event.key - 48 < room_len:
                    room = event.key - 48
                    goto_room(room)

            # REVERSE THE SCREEN
            if event.key == pygame.K_r:
                message("you pressed r: room is reversed")
                for n, line in enumerate(_map):
                    line = line[::-1]
                    _map[n] = line
                # print(_map)
                layout[room] = _map
                update_screen()
                # print("Reversed room: done")

            # print(event.key, f"{room=}")

            # This changes the actual levels
            if event.key == pygame.K_c or event.key == pygame.K_s:
                # I substitute the layout with this new
                save_map(levels="levels3.py")
                # print("Map saved with changes")
                message("Map saved with changes")
                # os.startfile("levels2.py")


            if event.key == pygame.K_n:
                layout.append(_map)
                room_len = len(layout) # updates the lenght of the map
                message(f"you added a room at the end of the map like this one. N.map={room_len}")
                room = room_len - 1
                update_screen()

            if event.key == pygame.K_m:
                layout.insert(room + 1, _map)
                room_len = len(layout)
                message(f"you added copied a room in a new next level N.map={room_len}")
                room +=1 
                update_screen()
                # save_map(levels="levels1.txt", clear=1)
                # os.startfile("levels1.txt")
    
            if event.key == pygame.K_k:
                # print("Room map has been copied, press p to paste it when in another room")
                copied = _map
                update_screen()

            if event.key == pygame.K_l:
                _map = copied
                layout[room] = _map
                update_screen()

            # Go to last room
            if event.key == pygame.K_UP:
                room = room_len -1
                update_screen()

            if event.key == pygame.K_DOWN:
                room = 0
                update_screen()

            # This shows the tiles ================== TILES MENU ==== t ====
            if event.key == pygame.K_t:
                pygame.display.set_caption("Tiles avaiable - Click on one of them")
                tiles_visible = 1 if tiles_visible == 0 else 0
                if tiles_visible:
                    screen0.fill(0)
                    screen0.blit(tiles, (0, 0))
                else:
                    update_screen()

            if event.key == pygame.K_h:
                pygame.display.set_caption("Help")
                menu_visible = 1 if menu_visible == 0 else 0
                if menu_visible:
                    screen0.fill(0)
                    screen0.blit(menu, (0, 0))
                else:
                    update_screen()
    
            if event.key == pygame.K_ESCAPE:
                pygame.display.set_caption("Delete Mode")
                editor_mode = 0
        if event.type == pygame.KEYUP:
            update_screen()
      # if event.type == pygame.MOUSEMOTION:
      #   if editor_mode and not tiles_visible:
      # update_screen()
      x, y = pygame.mouse.get_pos()
      screen0.blit(tile, (x//2 - 16, y//2 - 16))


            #################################

            #           This is where the map is changed
            #################################

      # if event.type == pygame.MOUSEBUTTONDOWN:
        # When you press on the tiles menu...
      if get_pos()[1] != 9:
        if pygame.mouse.get_pressed()[0]:
            # if you click down in the menu
            if get_pos()[1] == 10:
                # print(f"{get_pos()[1]=} {tiles_visible=}")
                x = get_pos()[0]
                if x < NUM_OF_TILES:
                    rect_tile = (x * 32, 0, 32, 32)
                    tile = tiles.subsurface(rect_tile)
                    tile_chosen_number = x
                    # print(f"{tiles_visible=}")
                    editor_mode = 1
                    tiles_visible = 0
                    tiles_visible = 0
                    menu = 0
            # if you click anywhere else
            else:

                x, y = get_pos()
                # print(f"{x=}{y=}")
                line = list(_map[y])
                line[x] = f"{tile_chosen_number}"
                layout[room][y] = line

                update_screen()
        # v.1.9 - 25.06.2021 - adding the crystals with the middle mouse

        if pygame.mouse.get_pressed()[1]:
            position_tile("CC")

        if get_pos()[1] < 9:
            if pygame.mouse.get_pressed()[2]:
                x, y = get_pos()
                line = list(_map[y])
                line[x] = " "
                layout[room][y] = line
                # _map[y] = "".join(line)
                # layout[room][y] = _map[y]
                # print_map()
                update_screen()

  screen.blit(
    pygame.transform.scale(screen0, (DOUBLE_SIZE)),(0, 0))
  pygame.display.flip()
  clock.tick(60)
