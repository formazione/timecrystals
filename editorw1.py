# editor_mode
import pygame
import os
import pickle
import time

# layout = [
# [
# [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
# [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
# [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
# [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
# [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
# [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
# [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
# [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
# [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
# ],

# [
# [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
# [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
# [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
# [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
# [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
# [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
# [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
# [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
# [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
# ],

# ]




# Gets the rooms of the map
def load_map():
    ''' levels are saved into this by save_map '''
    with open("levels\\levels2c.pkl", "rb") as file:
        layout = pickle.load(file)
    return layout
# starting map

def save_map(levels="levels\\levels2c.pkl"):
    with open("levels\\levels2c.pkl", "wb") as file:
        pickle.dump(layout, file)


def blit_tiles(bg="") -> tuple:
    """ blit on a secundary surface first """
    if bg != "":
        screen0.blit(background, (0, 0))
    tup = []    
    for row, line in enumerate(_map): # row is the number of the line
        for col, num_tl in enumerate(line): # col is the number of the column
            if num_tl < 100 and num_tl > -1:
                screen0.blit(tiles, (col*32, row*32), (num_tl * 32, 0, 32, 32))
            elif num_tl == 100:
                screen0.blit(diamond, (col*32, row*32))
    screen0.blit(tiles, (0, 320))

    return tup


def message(text):
    print(text)
    msg = font.render(text, 1, (0, 255, 0))
    screen0.blit(msg, (0, 288))


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
    global pos
    screen0.fill(0)
    pygame.display.set_caption(f"Room n. {room}")
    pos = blit_tiles("ciao")


def get_tile():
    rect_tile = (x * 32, 0, 32, 32)
    tile = tiles.subsurface(rect_tile)
    return tile


def goto_room(room_num):
    global _map

    _map = list(layout[room])
    update_screen()
    message(f"you went int room {room}")


def position_tile(symbol):
    """ get the x and y and put in the map list the symbol for that tile """
    message("You positioned a tile in this room")
    x, y = get_pos()
    layout[room][y][x] = symbol
    update_screen()


pygame.init()
width = 15
height = 9


class Sprite:
    ''' width and height of the tiles '''
    # you can change them for a different tile dimensions '''
    width = 32
    height = 32


tiles = pygame.image.load("images\\tiles4.png")
NUM_OF_TILES = tiles.get_size()[0] // 32
menu = pygame.image.load("images\\menu2.png")
diamond = pygame.image.load("images\\diamond.png")
DOUBLE_SIZE = width*Sprite.width*2, height*Sprite.height*2 + 128
# ===================
font = pygame.font.SysFont("Arial", 14)
# Gets the map and the starting room

layout = load_map()
# layout[0] = [
# [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
# [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
# [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
# [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
# [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
# [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
# [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
# [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
# [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
# ]
_map = layout[1]
print(layout[1])
room_len = len(layout) # how many rooms are there
room = 1 # the actual room
size = width*Sprite.width, height*Sprite.height
# the main and secundary screens
screen = pygame.display.set_mode(DOUBLE_SIZE)
screen0 = pygame.Surface((width*Sprite.width, height*Sprite.height + 64))
background = pygame.image.load("images\\background.png")
fx_tik = pygame.mixer.Sound("sounds/tik.ogg")
fx_whip = pygame.mixer.Sound("sounds/whip.ogg")
fx_save = pygame.mixer.Sound("sounds/save.ogg")
tile_chosen_number = 0
rect_tile = (0 * 32, 0, 32, 32)
tile = tiles.subsurface(rect_tile)
# tile = pygame.Surface((0, 0))
clock = pygame.time.Clock()
while True:

  # Event handler
  for event in pygame.event.get():
    
      if event.type == pygame.QUIT:
          pygame.quit()
    
      if event.type == pygame.KEYDOWN:

            # ======= NAVIGATE THE ROOMS ===== #
            if event.key == pygame.K_LEFT:
                if room > 1:
                    room -= 1
                goto_room(room)

            if event.key == pygame.K_RIGHT:
                if room < room_len - 1:
                    room += 1
                goto_room(room)

            # ==== type 0-9 to get to the rooms 0-9
            if event.key in range(47, 58):
                room = event.key - 48
                goto_room(room)

            # REVERSE THE SCREEN if you press r
            if event.key == pygame.K_r:
                message("you pressed r: room is reversed")
                for n, line in enumerate(_map):
                    line = line[::-1]
                    _map[n] = line
                layout[room] = _map
                update_screen()

            # Save the map with s
            if event.key == pygame.K_s:
                save_map()
                message("Map saved with changes")
                pygame.mixer.Sound.play(fx_save)

            # Take a screenshot
            if event.key == pygame.K_f:
                for n in range(room_len):
                    room = n
                    goto_room(n)
                    update_screen()
                    pygame.display.flip()
                    time.sleep(.5)
                    pygame.image.save(screen0, f"screenshots\\Room_{n}.png")
                    print(f"You saved screenshots\\Room_{n}.png")
                pygame.mixer.Sound.play(fx_save)

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

            # m copy room adding a room in the next space
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

            if event.key == pygame.K_x:
                room = room - 1
                goto_room(room)
                layout.pop(room + 1)
                room_len = len(layout)
    
            # copy actual room
            if event.key == pygame.K_c:
                copied = _map.copy()
                update_screen()

            # paste the room copied with c
            if event.key == pygame.K_p:
                layout[room] = copied
                update_screen()

            # Go to last room
            if event.key == pygame.K_UP:
                room = room_len -1
                update_screen()

            # go to the first room
            if event.key == pygame.K_DOWN:
                room = 0
                update_screen()
    
      update_screen()
      x, y = pygame.mouse.get_pos()
      screen0.blit(tile, (x//2 - 16, y//2 - 16))


            #################################
            # This is where the map is changed
            #################################


      if get_pos()[1] == 10:
          # if you are in the 10th row you can pick a tile
          x = get_pos()[0]
          # when you press a button
          if pygame.mouse.get_pressed()[0]:
            # prevent from clicking beyond tiles
              if x < NUM_OF_TILES:
                  rect_tile = (x * 32, 0, 32, 32)
                  tile = tiles.subsurface(rect_tile)
                  tile_chosen_number = x
                  pygame.mixer.Sound.play(fx_tik)


      if get_pos()[1] < 9:
          # Clicking the left mouse button you place a tile
          if pygame.mouse.get_pressed()[0]:
              x, y = get_pos()
              if layout[room][y][x] != tile_chosen_number:
                pygame.mixer.Sound.play(fx_tik)
              layout[room][y][x] = tile_chosen_number
              update_screen()

          if pygame.mouse.get_pressed()[1]:
              x, y = get_pos()
              if layout[room][y][x] != 100:
                pygame.mixer.Sound.play(fx_tik)
              layout[room][y][x] = 100
              update_screen()

          if pygame.mouse.get_pressed()[2]:
              x, y = get_pos()
              if layout[room][y][x] != -1:
                pygame.mixer.Sound.play(fx_whip)
              layout[room][y][x] = -1
              update_screen()

  # scaling the screen
  screen.blit(
    pygame.transform.scale(screen0, (DOUBLE_SIZE)),(0, 0))
  pygame.display.flip()
  clock.tick(60)


