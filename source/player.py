
import pygame



# Player class
class player(pygame.sprite.Sprite):
    def __init__(self, posx, posy):
        pygame.sprite.Sprite.__init__(self)

        # Sprites
        self.im_front = pygame.image.load("sprites/samus/front.png")
        self.im_stop = pygame.image.load("sprites/samus/stop.png")
        self.im_up = pygame.image.load("sprites/samus/up.png")
        self.im_morf1 = pygame.image.load("sprites/samus/morf1.png")
        self.im_morf2 = pygame.image.load("sprites/samus/morf2.png")
        self.im_run1 = pygame.image.load("sprites/samus/run1.png")
        self.im_run2 = pygame.image.load("sprites/samus/run2.png")
        self.im_run3 = pygame.image.load("sprites/samus/run3.png")
        self.im_run4 = pygame.image.load("sprites/samus/run4.png")
        self.im_jump1 = pygame.image.load("sprites/samus/jump1.png")
        self.im_jump2 = pygame.image.load("sprites/samus/jump2.png")
        self.list_run = [self.im_run1, self.im_run2, self.im_run3, self.im_run4]
        self.image = self.im_front

        # Rectangle for collisions
        self.rect = self.image.get_rect()

        # Position
        self.x = posx
        self.y = posy

        # Health
        self.health = 194

        # Orientation
        self.to_right = True
        self.up = False

        # Running orientation and time
        self.move_left = False
        self.move_right = False
        self.timerun = 0

        # Jump and time jumping
        self.jump = False
        self.jumptime = 0

        # Morphball state
        self.morf = False

        # Some physics quantities
        self.vel = 3
        self.t_jump = 25
        self.t_run = 10

    # Function for selecting the image for Samus
    def imagesamus(self, screen):

        offset = 0

        # Morph Ball
        if self.morf==True:
            imsamus = self.im_morf1
            offset = 30

        # Jump animation
        elif self.jump == True:

            if self.jumptime <= self.t_jump:
                imsamus = self.im_jump1
            elif self.jumptime <= 2*self.t_jump:
                imsamus = self.im_jump2
            else:
                imsamus = self.im_jump2

        # Running animation
        elif (self.move_left | self.move_right)==True:
            for i in range(0,len(self.list_run)+1):
                if (self.timerun >= i*self.t_run) & (self.timerun < ((i+1)*self.t_run)):
                    imsamus = self.list_run[i]

        # Up
        elif self.up == True:
            imsamus = self.im_up
            offset = -10

        # Stopped
        else:
            imsamus = self.im_stop

        # Depict at the correct orientation
        if self.to_right == True:
            screen.blit(imsamus, (self.x, self.y + offset))
        else:
            screen.blit(pygame.transform.flip(imsamus,True,False), (self.x, self.y + offset))

        self.image = imsamus

    # Move player
    def move_player(self):

        if self.move_left:
            self.to_right=False
            self.x-=self.vel
        elif self.move_right:
            self.to_right=True
            self.x+=self.vel
        if self.jump==True:
            if self.jumptime < self.t_jump:
                self.y-=self.vel
            elif self.jumptime < 2*self.t_jump:
                self.y+=self.vel
            else:
                self.jump=False

    time_change = 1
