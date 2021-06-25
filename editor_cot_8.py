# editor_mode
import pygame
import os


width = 15
height = 9

class Sprite:
    width = 32
    height = 32

tiles = pygame.image.load("assets\\tiles3.png")
menu = pygame.image.load("assets\\menu.png")

from levels2 import *

# Convert string to list to modify elements
for n, eachmap in enumerate(layout):
    layout[n] = list(layout[n])
_map = layout[0]
# _map = [
# "111111111111111",
# "1             1",
# "              1",
# "          11111",
# "      11       ",
# "               ",
# "  111    111111",
# " 11111   111111",
# "111111111111111",
#     ]



size = width*Sprite.width, height*Sprite.height
screen = pygame.display.set_mode((width*Sprite.width, height*Sprite.height))
screen0 = pygame.Surface(size)

def blit_tiles(bg="") -> tuple:
    """ blit on a secundary surface first """
    if bg != "":
        background(bg)
    tup = []    
    for y, line in enumerate(_map): # y is the number of the line
        for x, str_num in enumerate(line): # x is the number of the column
            if str_num not in "CP ":
                # the image, the position on the screen, the part of the image
                # tup.append([tiles, (x*32, y*32), (int(str_num) * 32, 0, 32, 32)])
                screen0.blit(tiles, (x*32, y*32), (int(str_num) * 32, 0, 32, 32))
    return tup
# Load an image
pos = blit_tiles()

def background(image):
    house1 = pygame.image.load(image)
    screen0.blit(house1, (0, 0))


def print_map():
    print("(")
    for line in _map:
        print(f"\"{line}\",")
    print("),")


def save_map(levels="levels.txt"):
    """ This changes all the maps with the new ones """
    global layout
    
    text = "layout = ["
    # This puts all the tuples of the maps into a list
    for eachmap in layout:
        text += "("
        for line in eachmap:
            text += f"\"{line}\",\n"
        text += "),"
    text += "]"
    print("This is saved into levels2.py")
    # one map only
    with open(levels, "w") as file:
        file.write(text)
    # os.system(f"""start "" "C:\Program Files\Sublime Text 3\sublime_text.exe" {levels} """)

    return text

# def save_map(levels="levels.txt", clear=0):
#     text = ""
#     text += "("
#     for line in _map:
#         text += f"\"{line}\",\n"
#     text += "),"
#     if clear==0:
#         # it appends the maps
#         with open(levels, "r") as file:
#             file = file.read()
#             file = file.replace("]", "")
#         with open(levels, "w") as file2:
#             stringa = f"{file}\n{text}\n]"
#             file2.write(stringa)
#     elif clear:
#         # one map only
#         with open(levels, "w") as file:
#             file.write(text)

#     return text

def get_pos() -> tuple:
    mpos = pygame.mouse.get_pos()
    print(f"{mpos=}")
    x = mpos[0]//32
    y = mpos[1]//32
    print(x, y)
    return x, y

def update_screen():
    ''' Clear and show tiles '''
    global pos
    screen0.fill(0)
    pygame.display.set_caption(f"Room n. {room}")
    pos = blit_tiles()


def get_tile():
    rect_tile = (x * 32, 0, 32, 32)
    tile = tiles.subsurface(rect_tile)
    return tile

tiles_visible = 0
editor_mode = 0
pygame.display.set_caption("Map Editor - Press t for tiles")
help = """

pythonprogramming.altervista.org

                Commands
                ========
t = show tiles
r = reverse tiles
s = append tiles to file
n = save only the last file

0,1,2.... = go into a room
arrows left and right = iterate
               the rooms
arrow Up => last room
arrow down => first room
h = help

"""
room_len = len(layout)
room = 0
print(f"{room_len=}")
menu_visible = 0
def goto_room(room_num):
    global _map

    _map = list(layout[room])
    update_screen()


while True:
  
  for event in pygame.event.get():
    
      if event.type == pygame.QUIT:
          pygame.quit()
    
      if event.type == pygame.KEYDOWN:

            # CHANGE ROOM when you press a key ====== ROOM NAVIGATOR ====
            if event.key == pygame.K_LEFT:
                if room > 0:
                    room -= 1
                    save_map(levels="levels2.py")
                    # pygame.display.set_caption(f"Room n. {room}")
                goto_room(room)
            if event.key == pygame.K_RIGHT:
                if room < room_len - 1:
                    room += 1
                    save_map(levels="levels2.py")
                goto_room(room)

            if event.key in range(47, 58):
                room = event.key - 48
                goto_room(room)

            # REVERSE THE SCREEN
            if event.key == pygame.K_r:
                print("you pressed r")
                for n, line in enumerate(_map):
                    line = line[::-1]
                    _map[n] = line
                print(_map)
                update_screen()
                print("done")

            print(event.key, f"{room=}")

            # This changes the actual levels
            if event.key == pygame.K_c or event.key == pygame.K_s:
                # I substitute the layout with this new
                save_map(levels="levels2.py")
                print("Map saved with changes")
                # os.startfile("levels2.py")


            if event.key == pygame.K_n:
                layout.append(_map)
                room_len = len(layout)
                # print(layout)
                # save_map(levels="levels1.txt", clear=1)
                # os.startfile("levels1.txt")
    
            if event.key == pygame.K_k:
                print("Room map has been copied, press p to paste it when in another room")
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
      if event.type == pygame.MOUSEMOTION:
        if editor_mode and not tiles_visible:
            update_screen()
            x, y = pygame.mouse.get_pos()
            screen0.blit(tile, (x-16, y-16))


            #################################

            #           This is where the map is changed
            #################################

      if event.type == pygame.MOUSEBUTTONDOWN:
        # if you click when the tiles_visible is on
        if pygame.mouse.get_pressed()[0]:
            if tiles_visible:
                x, y = get_pos()
                print(x, y)
                if y == 0 and x < 8: # tiles are 8
                    rect_tile = (x * 32, 0, 32, 32)
                    # screen0.blit(tiles, (0, 100), rect_tile)
                    tile = tiles.subsurface(rect_tile)
                    tile_chosen_number = x
                    menu = 0
                    update_screen()
                    tiles_visible = 0
                    editor_mode = 1
            
            if tiles_visible == 0:
                if editor_mode == 0:
                    x, y = get_pos()
                    line = list(_map[y])
                    line[x] = " "
                    _map[y] = "".join(line)
                    print_map()
                    update_screen()

                if editor_mode:
                    print("Editor mode")
                    x, y = get_pos()
                    print(f"{x=}{y=}")
                    line = list(_map[y])
                    # Changes the tile
                    line[x] = f"{tile_chosen_number}"
                    # Reconvert the list into a string
                    _map[y] = "".join(line)
                    # substitute di string into the layout string of that map
                    layout[room][y] = _map[y]
                    print_map()
                    # screen0.blit(tile, (x * 32, y * 32))
                    update_screen()
                    print(rect_tile)
        if pygame.mouse.get_pressed()[2]:
            x, y = get_pos()
            line = list(_map[y])
            line[x] = " "
            _map[y] = "".join(line)
            layout[room][y] = _map[y]
            print_map()
            update_screen()

  screen.blit(screen0, (0, 0))
  pygame.display.flip()
