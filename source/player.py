
import pygame



# Player class
class samus(pygame.sprite.Sprite):
    def __init__(self, posx, posy):
        pygame.sprite.Sprite.__init__(self)

        # Sprites
        self.im_front = pygame.image.load("sprites/samus/front.png")
        self.im_stop = pygame.image.load("sprites/samus/stop.png")
        self.im_up = pygame.image.load("sprites/samus/up.png")
        self.im_morf1 = pygame.image.load("sprites/samus/morf1.png")
        self.im_morf2 = pygame.image.load("sprites/samus/morf2.png")
        self.im_jump1 = pygame.image.load("sprites/samus/jump1.png")
        self.im_jump2 = pygame.image.load("sprites/samus/jump2.png")
        self.list_morf = [pygame.image.load("sprites/samus/morf"+str(i+1)+".png") for i in range(2)]
        self.list_run = [pygame.image.load("sprites/samus/run"+str(i+1)+".png") for i in range(8)]
        self.image = self.im_front

        # Position
        self.x = posx
        self.y = posy
        self.bottom = posy + self.image.get_height()

        # Rectangle for collisions
        self.rect = self.image.get_rect()
        self.rect.left = self.x
        self.rect.top = self.y

        # Health
        self.health = 194

        # Orientation
        self.to_right = True
        self.up = False

        # Running orientation and time
        self.move_left = False
        self.move_right = False
        self.timerun = 0
        self.timemorf = 0

        # Morphball state
        self.morf = False

        # Some physics quantities
        self.vel = 3
        self.vel_jump = self.vel*3
        self.t_anim = 8

        self.vely = 0
        self.accy = 0.5

        self.jumping = False

    # Function for selecting the image for Samus
    def imagesamus(self, screen):

        offset = 0

        # Morph Ball
        if self.morf==True:
            for i in range(0,len(self.list_morf)+1):
                if (self.timemorf >= i*self.t_anim) & (self.timemorf < ((i+1)*self.t_anim)):
                    imsamus = self.list_morf[i]

        # Up
        elif self.up == True:
            imsamus = self.im_up

        # Jump animation
        elif self.vely>0:
            imsamus = self.im_jump1
        elif self.vely<0:
            imsamus = self.im_jump2

        # Running animation
        elif (self.move_left | self.move_right)==True:
            for i in range(0,len(self.list_run)+1):
                if (self.timerun >= i*self.t_anim) & (self.timerun < ((i+1)*self.t_anim)):
                    imsamus = self.list_run[i]

        # Stopped
        else:
            imsamus = self.im_stop

        # Depict at the correct orientation
        self.y = self.bottom - imsamus.get_height()
        if self.to_right == True:
            screen.blit(imsamus, (self.x, self.y + offset))
        else:
            screen.blit(pygame.transform.flip(imsamus,True,False), (self.x, self.y + offset))

        self.image = imsamus

    # Move player
    def move_player(self, platforms):

        # Horizontal movement
        if self.move_left:
            self.to_right=False
            self.x-=self.vel
        elif self.move_right:
            self.to_right=True
            self.x+=self.vel

        # Vertical movement
        self.vely += self.accy
        #self.y += self.vely + 0.5*self.accy
        self.bottom += self.vely + 0.5*self.accy

        # Stop falling if player is above a platform or floor
        for plat in platforms:
            #if (self.rect.colliderect(plat.rect)) and (self.rect.bottom>=plat.rect.top) and (self.vely > 0):
            if (self.rect.colliderect(plat.rect)) and (self.rect.bottom>=plat.rect.top) and (self.vely > 0):
                self.vely = 0
                #if self.up==False:
                self.bottom = plat.rect.top
                #self.y = self.bottom - self.image.get_height()
                #self.y = plat.rect.top - self.image.get_height() #+ 7
                #if self.up==True: self.y+=7
                #if self.morf==True: self.y += 30
                self.jumping = False

        self.y = self.bottom - self.image.get_height()
        if self.up==True: self.y+=7

        # Update rect
        self.rect.left = self.x
        self.rect.top = self.y
        #if self.morf==True: self.rect.top+=30


    # Jump function
    def jump(self, platforms):
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits:
            self.vely = -self.vel_jump
            self.jumping = True
