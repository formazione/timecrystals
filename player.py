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

        # this moves the player: the xSpeed is 0, but if you
        self.x += self.xSpeed
        self.y += self.ySpeed
        

        if self.ySpeed < 8:
            self.ySpeed += 0.5


        # COLLISION WITH A TILE TO THE BOTTO
        if self.bottomCol: # quando c'è un tile sotto non cade
            self.ySpeed = 0
            if self.xSpeed > 0: # decelera quando cade su un tile andando verso destra
                self.xSpeed -= 0.2 # [[[[[[[[ 0.3 valore originale ]]]]]]]]
            elif self.xSpeed < 0: # se va verso sinistra decelera con un + perchè...
                self.xSpeed += 0.2 # CAMBIO!!!! #######>>>> 0.3 valore originale
            if abs(self.xSpeed) < 0.3: # quando la velocità è inferiore a 0.3 si ferma
                self.xSpeed = 0



        # timer is used to stop the player when collects a crystal (I do not want it)
        # if self.timer <= 0:
        #     #                        JUMP
        if keys[pygame.K_UP] and self.bottomCol:
        # if keys[pygame.K_UP] and self.bottomCol:
            self.ySpeed = -8
            self.bottomCol = 0

                                 #############
        #                         LEFT - RIGHT                           #
                                 #############

        if keys[pygame.K_LEFT] and self.xSpeed > -3:
            self.xSpeed -= 0.2
            self.faceRight = False
            self.frame = (timer % 16 < 8) # is 1 or 0
    
        if keys[pygame.K_RIGHT] and self.xSpeed < 3:
            self.xSpeed += 0.2
            self.faceRight = True
            self.frame = (timer % 16 < 8) # is 1 or 0

            
        # else:
        #     self.frame = 0 # Idle frame
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
            (int(self.x), int(self.y)),
            # Here is where he gets the sprite from the spritesheet
            (self.frame * 32, (not self.faceRight) * 32, 32, 32))
        # pygame.draw.rect(display, (0, 255, 0), (int(self.x), int(self.y), 32, 32))