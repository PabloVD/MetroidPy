
import pygame


# Background class
class background():
    def __init__(self):

        # Background images
        back1 = pygame.image.load("sprites/backgrounds/back1.png")
        back2 = pygame.image.load("sprites/backgrounds/back2.png")
        back3 = pygame.image.load("sprites/backgrounds/back3.png")
        back4 = pygame.image.load("sprites/backgrounds/back4.png")
        back5 = pygame.image.load("sprites/backgrounds/ceres_lab.bmp")
        back5 = pygame.transform.scale(back5,(back4.get_width(),back4.get_height()))
        backchozo = pygame.image.load("sprites/backgrounds/backchozo2.png")

        # Floor images
        im_floor1 = pygame.image.load("sprites/floors/floor1.png")
        im_floor2 = pygame.image.load("sprites/floors/floor2.png")
        im_floor3 = pygame.image.load("sprites/floors/floor3.png")
        im_floor4 = pygame.image.load("sprites/floors/floor4.png")

        # Samus spaceship
        self.im_spaceship = pygame.image.load("sprites/misc/spaceship.png")

        self.backs = [back1, back2, back3, back4, back5]
        self.floors = [im_floor1, im_floor1, im_floor3, im_floor4, im_floor2]
        self.numscenes = len(self.backs)

    # Function for drawing the scenario
    def draw_background(self, screen, scene):

        width, height = screen.get_width(), screen.get_height()

        screen.fill(0)

        # Flip vertically some backgrounds
        flip = False
        if scene == 5:
            flip = True

        # Background
        for x in range(width//self.backs[scene-1].get_width()+1):
            screen.blit(pygame.transform.flip(self.backs[scene-1],False,flip),(x*self.backs[scene-1].get_width(),height//2))
            screen.blit(self.backs[scene-1],(x*self.backs[scene-1].get_width(),0))

        # Floors
        #for x in range(width//self.floors[scene-1].get_width()+2):
        #    screen.blit(self.floors[scene-1],(x*self.floors[scene-1].get_width(),height-40))

        # Other objects in scene
        if scene==1:
            screen.blit(self.im_spaceship,(width/2 - self.im_spaceship.get_width()/2, height//2-20))


# Background class
class platform(pygame.sprite.Sprite):
    def __init__(self, posx, posy, scene, scale=1):
        pygame.sprite.Sprite.__init__(self)

        # Floor images
        im_floor1 = pygame.image.load("sprites/floors/floor1.png")
        im_floor2 = pygame.image.load("sprites/floors/floor2.png")
        im_floor3 = pygame.image.load("sprites/floors/floor3.png")
        im_floor4 = pygame.image.load("sprites/floors/floor4.png")

        self.floors = [im_floor1, im_floor1, im_floor3, im_floor4, im_floor2]
        for i, floor in enumerate(self.floors):
            if scale>1:
                floorpos = int(floor.get_width()*scale)
            else:
                floorpos = floor.get_width()//int(1/scale)
            self.floors[i] = pygame.transform.scale(floor, (floorpos, floor.get_height()))
        self.image = self.floors[0]

        # Position
        self.x = posx
        self.y = posy

        # Scene
        self.scene = scene

        # Rectangle for collisions
        self.rect = self.image.get_rect()
        self.rect.top = self.y
        self.rect.left = self.x

    # Function for drawing the scenario
    def draw(self, screen, scene):

        if self.scene==scene:

            self.image = self.floors[scene-1]
            self.rect = self.image.get_rect()
            self.rect.top = self.y
            self.rect.left = self.x
            screen.blit(self.image,(self.x, self.y))
