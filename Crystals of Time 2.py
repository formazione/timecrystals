import pygame, time, random, math
from pygame.locals import *
pygame.display.init()
pygame.mixer.init()

display = pygame.display.set_mode((480*2, 288*2))
screen = pygame.Surface((480, 288))
pygame.display.set_caption("Crystals of Time by SmellyFrog")

spr_player = pygame.image.load("assets/lily.png").convert_alpha()
spr_tiles = pygame.image.load("assets/tiles2.png").convert_alpha()
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

# class Player(pygame.sprite.Sprite):
class Player():
    def __init__(self, x, y):
        # super(Player, self).__init__()
        self.x = x
        self.y = y
        self.xSpeed = 0
        self.ySpeed = 0
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
        if self.bottomCol:
            self.ySpeed = 0
            if self.xSpeed > 0:
                self.xSpeed -= 0.3
            elif self.xSpeed < 0:
                self.xSpeed += 0.3
            if abs(self.xSpeed) < 0.3:
                self.xSpeed = 0

        if self.timer <= 0:
            if keys[pygame.K_UP] and self.bottomCol:
                self.ySpeed = -8
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
        screen.blit(spr_player, (int(self.x), int(self.y) - 16), (self.frame * 32, (not self.faceRight) * 48, 32, 48))
        #pygame.draw.rect(display, (0, 255, 0), (int(self.x), int(self.y), 32, 32))

class Terrain():
    def __init__(self, x, y, Type):
        self.x = x
        self.y = y
        self.col = False
        self.type = Type
    def update(self):

        if player.x + 32 > self.x and player.x < self.x + 32 and not self.col:
            if player.y + 32 > self.y and player.y + 32 < self.y + 16:
                player.y = self.y - 32
                player.ySpeed = 0
                player.bottomCol = True
                self.col = True

        # Tipes of tiles

                # Fire, makes you die
                if self.type == 3:
                    player.x -= 96
                    pygame.mixer.Sound.play(sfx_crystal)
                
                elif self.type == 4:
                    player.ySpeed = -10
                    player.bottomCol = False
                    pygame.mixer.Sound.play(sfx_crystal)
                # The tile jump
                
                elif self.type == 5:
                    player.y += 64
                    pygame.mixer.Sound.play(sfx_crystal)
                    
            elif player.y > self.y + 16 and player.y < self.y + 32:
                player.y = self.y + 32
                player.ySpeed = 0
                player.topCol = True
                self.col = True
        if player.y + 32 > self.y and player.y < self.y + 32 and not self.col:
            if player.x + 32 > self.x and player.x + 32 < self.x + 16:
                player.x = self.x - 32
                player.xSpeed = -0.4
                player.rightCol = True
                self.col = True
            elif player.x > self.x + 16 and player.x < self.x + 32:
                player.x = self.x + 32
                player.xSpeed = 0.4
                player.leftCol = True
                self.col = True
        self.col = False
        
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
            player.timer = 15
            player.xSpeed = 0
            pygame.mixer.Sound.play(sfx_collect)
        if (self.x, self.y, self.num) in collected:
            remove.append(self)

            
    def draw(self):
        if not self in remove:
            screen.blit(spr_crystal1, (int(self.x), int(self.y) + math.sin(timer / 16) * 16), ((timer % 16 < 8) * 32, 0, 32, 32))


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
        if ((player.x - self.x)**2 + (player.y - self.y)**2)**0.5 < 96 and self.alive and countdown > 0:
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
                countdown = 1200
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
layout = [
          ("222222222222222", # cover
           "22 226        2",
           "2226          2",
           "2       76    2",
           "2      7226   2",
           "2P    72 226   ",
           "222222222226 C ",
           "22 222 2 22 222",
           "222222222222222",
           ),


          
          # stage 1 like the cover
          ("222222222222222", # cover
           "22 226        2",
           "2226          2",
           "2       76    2",
           "2      7226   2",
           "2P    72 226   ",
           "222222222226 C ",
           "22 222 2 22 222",
           "222222222222222",
           ),
("               ",
"            C  ",
"               ",
"            111",
"   1  4  4  1 1",
"P 11  0  0  111",
"1111  1  1  111",
"111133133133111",
"               ",
),

(
"               ",
"               ",
"               ",
"          C    ",
"    111        ",
"   11111  11   ",
"  111111  1111 ",
"11111111  11111",
"111111111111111",
),
("      676      ",
"    22 2 22    ",
"      2 2      ",
"       2   26  ",
"  777       6  ",
"  2         2  ",
"      666 C    ",
"000000000000000",
"000000000000000",
),("               ",
"               ",
"      111      ",
"       1       ",
"   111111111   ",
"  1   111   1  ",
"  1    1    1 C",
"111111111111111",
"111111111111111",
),("               ",
"   722222226   ",
"  72222222226  ",
"  72  222  26  ",
"  72722222626  ",
"  2   222   2  ",
"               ",
"000000000000000",
"111111111111111",
),("               ",
"   222222226   ",
"   22     22   ",
"   2       2   ",
"227272222262622",
"               ",
"            C  ",
"11  11 11  11  ",
"112211211221122",
),("1              ",
"1              ",
"1  111  1111   ",
"1C 1111111111  ",
"111111111111   ",
"              1",
"             11",
"111111111111111",
"111111111111111",
),("               ",
"               ",
"     1  C 1    ",
"     111111    ",
"    11111111   ",
"1             1",
"11           11",
"111111111111111",
"111111111111111",
),
            # new map
            ("               ",
            "               ",
            "   222   222   ",
            "  7   2 2   6  ",
            "  72722 22626  ",
            "  2   2 2   2  ",
            "            C  ",
            "0000      00000",
            "111111  1111111",
            ),

("               ",
"               ",
"      111      ",
"       1       ",
"   111111111   ",
"  1   111   1  ",
"  1    1    1  ",
"111111111111111",
"111111111111111",
),
            (
            "               ",
            "   7222 2226   ",
            "  72  222  26  ",
            "   2  2 2  2   ",
            "  72722222626  ",
            "  2   2 2   2  ",
            "             C ",
            "00 00 00 00 000",
            "111111111111111"),

          # ("22222222226    ", # 1st as cover
          #  "22 226         ",
          #  "22226          ",
          #  "2       76     ",
          #  "2      726     ",
          #  "2P    72 6     ",
          #  "2222222226   C ",
          #  "22 222 22200000",
          #  "222222222211111",
          #  ),

          ("222222222222222", # 2 - the stairs
           "2  2         C2",
           "2222           ",
           "2        722222",
           "2       72 22 2",
           "2     722222222",
           "    72222 22 22",
           "222222222222222",
           "222 2222 222 22",
           ),

          ("222222222222222", # 3 - under palace
           "2             2",
           "2              ",
           "      2  2    2",
           "      2C 2   22",
           "     222222   2",
           "22  22222222  2",
           "2    C   C    2",
           "222222222222222"
           ),


          ("               ", # 4 jumping
           "             C ",
           "               ",
           "222        2222",
           "2 2        22 2",
           "222     4442222",
           "2 2     22222 2",
           "222 444 2222222",
           "222333332222222",
           ),
          ("               ", # 5 - triple jumping
           "               ",
           "             72",
           "26        4  2 ",
           " 2     4     22",
           "22  4        2 ",
           "22  C  C  C  22",
           "222222333222222",
           "222222222222222",
           ),
          ("               ", # beware the fire
           "               ",
           "2              ",
           "22         C ",
           "2      2       ",
           "22         2   ",
           "2C  2      2   ",
           "222223333332222",
           "222222222222222",
           ),
           ("222222222222222",
           "2222222222226  ",
           "2              ",
           "              2",
           "       76     2",
           "           2 C2",
           "   22      2222",
           "222223333332222",
           "222222222222222",
           ),
           # arrived here
                    ("               ",
           "             C ",
           "           2222",
           "222          22",
           "2          22 2",
           "222     4  2222",
           "2C      1   C 2",
           "222  4  1111222",
           "222333331111111",
           ),

          ("222222222222222",
           "            C  ",
           "               ",
           "               ",
           "           2   ",
           "  2  2  2     2",
           "  2         C22",
           "222333333332222",
           "111111111111111",
           ),
          ("     7222222222",
           "     7        2",
           "     7  7226  2",
           "     7     2  2",
           "    7226  32  2",
           "     7    22 C2",
           "         222   ",
           "000000000000000",
           "111111111111111",
           ),
          ("             7 ",
           "           C 7 ",
           "             7 ",
           "    7222222522 ",
           "               ",
           "   2       C   ",
           "               ",
           "000000000000000",
           "111111111111111",
           ),
          ("               ",
           "             72",
           "             72",
           "               ",
           "            C  ",
           "             72",
           "   738  736   2",
           "000000000022222",
           "111111111111111",
           ),
          ("               ",
           "               ",
           "               ",
           "    C    252  2",
           "               ",
           "    22         ",
           "222222         ",
           "000000000000000",
           "111111111111111",
           ),
          ("               ",
           "         C     ",
           "               ",
           "222     2222222",
           "     4         ",
           "               ",
           "               ",
           "000000000000000",
           "111111111111111",
           ),
          ("               ",
           "    C          ",
           "               ",
           "2222225222     ",
           "               ",
           "      C      00",
           "            011",
           "000000000000111",
           "111111111111111",
           ),
          ("               ",
           "               ",
           "               ",
           "             22",
           "         L   22",
           "000          22",
           "111022       22",
           "111100000000000",
           "111111111111111",
           ),
          ("               ",
           "               ",
           "               ",
           "               ",
           "               ",
           "               ",
           "               ",
           "               ",
           ),
          ("               ",
           "               ",
           "               ",
           "               ",
           "               ",
           "               ",
           "               ",
           "               ",
           ),
          ]
player_y = 42069
player_x = 42069
collected = []
room_num = 0
timer = 0
countdown = 1200
run = True
while run:
    ### level generation

    load = []
    remove = []
    player = Player(0, 0)

    for i in range(len(layout[room_num])):
        for j in range(len(layout[room_num][i])):
            if layout[room_num][i][j] == "P":
                player = Player(j*32, i*32)
                load.append(player)
            if layout[room_num][i][j] == "0":
                load.append(Terrain(j*32, i*32, 0))
            if layout[room_num][i][j] == "1":
                load.append(Terrain(j*32, i*32, 1))
            if layout[room_num][i][j] == "2":
                load.append(Terrain(j*32, i*32, 2))
            if layout[room_num][i][j] == "3":
                load.append(Terrain(j*32, i*32, 3))
            if layout[room_num][i][j] == "4":
                load.append(Terrain(j*32, i*32, 4))
            if layout[room_num][i][j] == "5":
                load.append(Terrain(j*32, i*32, 5))
            # bricks
            if layout[room_num][i][j] == "6":
                load.append(Terrain(j*32, i*32, 6))
            if layout[room_num][i][j] == "7":
                load.append(Terrain(j*32, i*32, 7))
            if layout[room_num][i][j] == "C":
                load.append(Crystal(j*32, i*32, room_num))
            if layout[room_num][i][j] == "L":
                load.append(LargeCrystal(j*32, i*32))

    if player not in load and room_num not in (0, 14, 15):
        load.append(player)

    if player_y != 42069:
        player.y = player_y
        player.x = player_x
    
    clock = pygame.time.Clock()
    alive = True
    while run and alive:

        timer += 1
        if countdown <= 3000 and room_num >= 1:
            countdown -= 1

        clock.tick(60)

        screen.fill((0, 0, 0))
        if room_num == 0:
            screen.blit(title, (0, 0))
        else:
            screen.blit(background, (0, 0))

        # meteor


        if countdown == 0:
            pygame.mixer.Sound.play(sfx_crash)
            pygame.mixer.music.stop()
        if countdown < 0:
            pygame.draw.circle(screen, (255, 255, 255), (240, 204), -10 * countdown)
        if countdown < -100:
            alive = False
            room_num = 0
            countdown = 1200
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

        for obj in load:
            obj.update()
            obj.draw()
        for obj in remove:
            load.remove(obj)
        remove = []

        if player.x + 16 > 480 or player.x + 16 < 0:
            alive = False

        # counter

        if countdown > 0 and countdown < 3000 and room_num >= 1:
            for i in range(len(str(countdown))):
                screen.blit(spr_number, (16 + i *16, 16), (int(str(countdown)[i]) * 16, 0, 16, 32))

        if room_num == 0 and (keys[pygame.K_SPACE] or keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP] or keys[pygame.K_DOWN]):
            room_num += 1
            alive = False
            music = pygame.mixer.music.load("assets/swinging in the night sky.wav")
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play(-1)
            player_y = 42069
            countdown = 1200
            player_x = 42069
            collected = []
                        
        pygame.draw.line(screen, (200, 255, 255), (239, 160 - (countdown // 6)), (239, -4), 6)
        pygame.draw.circle(screen, (200, 255, 255), (240, 160 - (countdown // 6)), 8)
        pygame.draw.circle(screen, (255, 255, 255), (240, 164 - (countdown // 6)), 4)
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
