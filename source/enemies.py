
import pygame
import numpy as np
import time

# Defined twice!
height = 200

# Enemy class
class enemy(pygame.sprite.Sprite):
    def __init__(self, posx, posy, scene, ini_im, health):
        pygame.sprite.Sprite.__init__(self)

        # Initial sprite
        self.image = pygame.image.load(ini_im)

        # Position
        self.x = posx
        self.y = posy

        # Rectangle for collisions
        self.rect = self.image.get_rect()
        self.rect.top = self.y
        self.rect.left = self.x

        # Scene where the enemy appears
        self.scene = scene

        # Health
        self.health = health

    # Show enemy
    def draw(self, screen):
        screen.blit(self.image,(self.x, self.y))

    # Movement function, to be defined for each enemy
    def movement(self, playerposx, playerposy):
        pass

    # Death function, to be defined for each enemy
    def death(self):
        pass

# Metroid class
class metroid(enemy):
    def __init__(self, posx, posy, upward, scene, type="red"):
        super().__init__(posx, posy, scene, "sprites/enemies/metroid"+type+".png", 3)   # Type: red, blue

        self.upward = upward
        self.vel_metroid = 0.8
        self.danger_dist = 200

        # Make blue metroids stronger
        if type=="blue":
            self.health *= 2
            self.vel_metroid = 1

    # Enemy movement
    def movement(self, playerposx, playerposy):

        if np.sqrt((self.x-playerposx)**2. + (self.y-playerposy)**2.) < self.danger_dist:
            # Attack movement if player is near
            self.x -= np.sign(self.x-playerposx)*self.vel_metroid
            self.y -= np.sign(self.y-playerposy)*self.vel_metroid

        else:
            # Vertical rest movement otherwise
            if self.upward == True:
                if self.y < height-80:
                    self.y += self.vel_metroid
                else:
                    self.upward = False
            else:
                if self.y > height-120:
                    self.y -= self.vel_metroid
                else:
                    self.upward = True

        self.rect.top = self.y
        self.rect.left = self.x

# Mother brain class
class mother_brain(enemy):
    def __init__(self, posx, posy, scene):
        super().__init__(posx, posy, scene, "sprites/enemies/MotherBrain1.png", 8)

        self.im1 = pygame.image.load("sprites/enemies/MotherBrain1.png")
        self.im2 = pygame.image.load("sprites/enemies/MotherBrain2.png")
        self.im3 = pygame.image.load("sprites/enemies/MotherBrain3.png")
        self.im4 = pygame.image.load("sprites/enemies/MotherBrain4.png")
        mb_sup = pygame.image.load("sprites/misc/MotherBrain_support.png")
        self.mb_sup = pygame.transform.scale(mb_sup,(mb_sup.get_width()*2,mb_sup.get_height()*2))
        self.alive = True
        self.timecountdown = 0


    # Show enemy
    def draw(self, screen):
        if self.health<=2:
            self.image = self.im4
        elif self.health<=4:
            self.image = self.im3
        elif self.health<=6:
            self.image = self.im2
        elif self.health<=8:
            self.image = self.im1

        screen.blit(self.mb_sup, (self.x-15, self.y+50))
        screen.blit(pygame.transform.flip(self.image,True,False), (self.x, self.y))

    def death(self):

        # Start scape music
        pygame.mixer.music.load("music/Metroid Fusion Music - Escape.mp3")
        pygame.mixer.music.set_volume(0.6)
        pygame.mixer.music.play(-1, 0.0)

        self.alive = False
        self.timecountdown = time.time()
