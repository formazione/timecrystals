import pygame, time, random, math
from pygame.locals import *

pygame.init()
pygame.display.init()
pygame.mixer.init()

display = pygame.display.set_mode((480*2, 288*2))
screen = pygame.Surface((480, 288))
pygame.display.set_caption("Crystals of Time by SmellyFrog")

spr_player = pygame.image.load("assets/lily2.png").convert_alpha()
# spr_player = pygame.transform.scale(spr_player, (160, 160))
player_rect = spr_player.get_rect()
spr_tiles = pygame.image.load("assets/tiles3.png").convert_alpha()
NUM_OF_TILES = spr_tiles.get_size()[0] // 32
spr_crystal1 = pygame.image.load("assets/crystal.png").convert_alpha()
spr_crystal2 = pygame.image.load("assets/crystal2.png").convert_alpha()
spr_particle = pygame.image.load("assets/particles.png").convert_alpha()
spr_number = pygame.image.load("assets/number.png").convert_alpha()
background = pygame.image.load("assets/background.png").convert()
title = pygame.image.load("assets/title.png").convert()


sfx_crash = pygame.mixer.Sound("assets/crash.wav")
sfx_crash.set_volume(0.2)
sfx_collect = pygame.mixer.Sound("assets/collect.wav")
sfx_crystal = pygame.mixer.Sound("assets/crystal.wav")


def play(song):
    pygame.mixer.music.load(song)
    pygame.mixer.music.play()

# class Player(pygame.sprite.Sprite):
class Player():
    def __init__(self, x, y):
        # super(Player, self).__init__()
        self.x = x
        self.y = y
        self.xSpeed = 0
        self.ySpeed = 0
        # credo che siano 1 quanto c'è un tile sotto, sopra...
        self.bottomCol = False
        self.topCol = False
        self.leftCol = False
        self.rightCol = False
        self.frame = 0
        self.faceRight = True
        self.timer = 0

    def update(self):

        self.x += self.xSpeed
        self.y += self.ySpeed


        if self.ySpeed < 8:
            self.ySpeed += 0.5
        if self.bottomCol: # quando c'è un tile sotto non cade
            self.ySpeed = 0
            if self.xSpeed > 0: # decelera quando cade su un tile andando verso destra
                self.xSpeed -= 0.2 # [[[[[[[[ 0.3 valore originale ]]]]]]]]
            elif self.xSpeed < 0: # se va verso sinistra decelera con un + perchè...
                self.xSpeed += 0.2 # CAMBIO!!!! #######>>>> 0.3 valore originale
            if abs(self.xSpeed) < 0.3: # quando la velocità è inferiore a 0.3 si ferma
                self.xSpeed = 0

        if self.timer <= 0:
            # salta solo ce è sopra un tile
            if keys[pygame.K_UP] and self.bottomCol:
                self.ySpeed = -8 # [[[[[[[[[[[[[[[[[[[-8 valore originale]]]]]]]]]]]]]]]]]]]
            if keys[pygame.K_LEFT] and self.xSpeed > -3:
                self.xSpeed -= 0.2
                self.faceRight = False
            if keys[pygame.K_RIGHT] and self.xSpeed < 3:
                self.xSpeed += 0.2
                self.faceRight = True

        if keys[pygame.K_RIGHT] or keys[pygame.K_LEFT]:
            self.frame = timer % 16 < 8
        else:
            self.frame = 0
        if not self.bottomCol and abs(self.ySpeed) > 1:
            self.frame = 2

        if self.timer > 0:
            self.frame = (timer % 16 < 8) + 3
            
        self.bottomCol = False
        self.topCol = False
        self.leftCol = False
        self.rightCol = False
            
    def draw(self):

        screen.blit(
            spr_player, 
            (int(self.x), int(self.y) - 8),
            # Here is where he gets the sprite from the spritesheet
            (self.frame * 16, (not self.faceRight) * 24, 16, 24))
        # pygame.draw.rect(display, (0, 255, 0), (int(self.x), int(self.y), 32, 32))

class Terrain():
    def __init__(self, x, y, Type):
        self.x = x
        self.y = y
        self.col = False
        self.type = Type

    def bottom_collision(self):
        if player.y + 16 > self.y and player.y + 16 < self.y + 16:
            player.y = self.y - 16
            player.ySpeed = 0
            player.bottomCol = True
            # self.col = True
            self.what_tile_youre_on()


    def what_tile_youre_on(self):
            if self.type == 3:
                player.x -= 96
                pygame.mixer.Sound.play(sfx_crystal)

            
            elif self.type == 4: 
                player.ySpeed = -10
                player.bottomCol = False
                pygame.mixer.Sound.play(sfx_crystal)
        
            
            elif self.type == 5:
                player.y += 64
                pygame.mixer.Sound.play(sfx_crystal)

    def update(self):
        # Se il giocatore si trova sopra ad un tile... cos'è self.col
        # quand'è che self.col = 1???
        player_on_tile = player.x + 16 > self.x and player.x < self.x + 32 ######
        if player_on_tile and not self.col:
            self.bottom_collision()
            self.top_collision()
            self.right_collision()
            self.left_collision()
        self.col = False
            


    def top_collision(self):
            if player.y > self.y + 16 and player.y < self.y + 32:
                player.y = self.y + 32
                player.ySpeed = 0
                player.topCol = True
                # self.col = True

    def right_collision(self):
        if player.y + 16 > self.y and player.y < self.y + 32:# and not self.col:
            if player.x + 16 > self.x and player.x + 16 < self.x + 16:
                player.x = self.x - 32
                player.xSpeed = -0.4
                player.rightCol = True
                # self.col = True

    def left_collision(self):
        if player.y + 16 > self.y and player.y < self.y + 32:# and not self.col:
            if player.x > self.x + 16 and player.x < self.x + 16:
                player.x = self.x + 16
                player.xSpeed = 0.4
                player.leftCol = True
                # self.col = True
        
    def draw(self):
        # this blits the tiles at the position, but starting with 6*32 end ending 32 further
        screen.blit(spr_tiles, (int(self.x), int(self.y)), (self.type * 32, 0, 32, 32))

class Crystal():
    def __init__(self, x, y, num):
        self.x = x
        self.y = y
        self.num = num
    def update(self):
        global countdown
        if ((player.x - self.x)**2 + (player.y - self.y)**2)**0.5 < 32 and countdown > 0:
            collected.append((self.x, self.y, room_num))
            # player.timer = 15
            # player.xSpeed = 0
            
            pygame.mixer.Sound.play(sfx_collect)
        if (self.x, self.y, self.num) in collected:
            remove.append(self)

            
    def draw(self):
        if not self in remove:
            screen.blit(spr_crystal1,
                (int(self.x), int(self.y) + math.sin(timer*3 / 32) * 16), ((timer % 16 < 8) * 32, 0, 32, 32))


class LargeCrystal():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.timer = 0
        self.alive = True
        self.winCountdown = 500
    def update(self):
        global alive
        global room_num
        global player_y
        global player_x
        global countdown
        if ((player.x - self.x)**2 + (

            player.y - self.y)**2)**0.5 < 96 and self.alive and countdown > 0:
            self.timer += 1
            if self.timer > 80 and self.alive:
                player.timer = 3000
                self.alive = False
                pygame.mixer.Sound.play(sfx_crash)
                pygame.mixer.music.stop()
        if not self.alive:
            self.winCountdown -= 1
            if self.winCountdown <= 0 and countdown > 0:
                alive = False
                room_num = 0
                player_y = 42069
                countdown = 2400
                player_x = 42069
                collected.clear()

            
    def draw(self):
        if not self in remove:
            screen.blit(spr_crystal2, (int(self.x), int(self.y)), (self.timer // 32 * 64, 0, 64, 96))

        
'''
P is the player
0 is the grass
2 is the wall
1 is the dirt
C diamond
4 jumper
3 danger stone
'''

# THE LEVELS ARE HERE, they
# are created by this program with 's'
from levels2 import *




player_y = 42069
player_x = 42069
collected = []
room_num = 0
timer = 0
countdown = 2400
run = True

room_r = len(layout[room_num])
room_c = len(layout[room_num][0])

def music_on():
    music = pygame.mixer.music.load("assets/swinging in the night sky.wav")
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)

str_num_tiles = [str(x) for x in range(NUM_OF_TILES)]
str_num_tiles = "".join(str_num_tiles)


while run:
    ### level generation

    load = []
    remove = []
    player = Player(0, 0)

    for i in range(room_r):
        for j in range(room_c):
            if layout[room_num][i][j] == "P":
                player = Player(j*32, i*32)
                load.append(player)
            if layout[room_num][i][j] in str_num_tiles:
                val = int(layout[room_num][i][j])
                load.append(Terrain(j*32, i*32, val))
            elif layout[room_num][i][j] == "C":
                load.append(Crystal(j*32, i*32, room_num))
            # elif layout[room_num][i][j] == "L":
            #     load.append(LargeCrystal(j*32, i*32))

    if player not in load and room_num not in (0, 14, 15):
        load.append(player)

    if player_y != 42069:
        player.y = player_y
        player.x = player_x


    
    clock = pygame.time.Clock()
    alive = True
    while run and alive:

        timer += 1
        # Countdown starts from second room
        if countdown <= 3000 and room_num >= 1:
            countdown -= 1

        clock.tick(60)

        screen.fill((0, 0, 0))
        if room_num == 0:
            screen.blit(title, (0, 0))
        else:
            screen.blit(background, (0, 0))

        # meteor

        # WHEN TIME'S OVER
        if countdown == 0:
            pygame.mixer.Sound.play(sfx_crash)
            pygame.mixer.music.stop()
        # This draws the the circle
        if countdown < 0:
            pygame.draw.circle(screen, (255, 255, 255), (240, 204), -10 * countdown)
        if countdown < -100:
            alive = False
            room_num = 0
            countdown = 1500
            player_y = 42069
            player_x = 42069
            collected = []

        if player.timer > 0:
            player.timer -= 1
            countdown += 11
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()

        # 
        for obj in load:
            obj.update()
            obj.draw()
        for obj in remove:
            load.remove(obj)
        remove = []

        if player.x + 16 > 480 or player.x + 16 < 0:
            alive = False

        # counter

        if countdown > 0 and countdown < 1500 and room_num >= 1:
            for i in range(len(str(countdown))):
                screen.blit(spr_number, (16 + i *16, 16), (int(str(countdown)[i]) * 16, 0, 16, 32))

        if room_num == 0 and (keys[pygame.K_SPACE] or keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP] or keys[pygame.K_DOWN]):
            room_num += 1
            alive = False

            player_y = 42069
            countdown = 1200
            player_x = 42069
            collected = []
                        
        pygame.draw.line(screen, (200, 255, 255), (239, 160 - (countdown // 5)), (239, -4), 6)
        pygame.draw.circle(screen, (200, 255, 255), (240, 160 - (countdown // 5)), 8)
        pygame.draw.circle(screen, (255, 255, 255), (240, 164 - (countdown // 5)), 4)
        display.blit(pygame.transform.scale(screen, (480*2, 288*2)),(0, 0))
        pygame.display.flip()

    if player.x + 16 < 0:
        player_y = player.y
        player_x = 480 - 24
        room_num -= 1
    elif player.x + 16 > 480:
        player_y = player.y
        player_x = -8
        room_num += 1
            
pygame.quit()