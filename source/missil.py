import pygame

# Missil class
class missil(pygame.sprite.Sprite):
    def __init__(self, posx, posy, to_right, to_up):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("sprites/misc/misil.png")
        self.rect = self.image.get_rect()

        self.x = posx
        self.y = posy

        self.vel_shot = 5

        self.to_right = to_right
        self.to_up = to_up

    # Function for drawing the misils
    def draw_shot(self, screen):

        if self.to_up==True:
            self.y -= self.vel_shot
        elif self.to_right==True:
            self.x += self.vel_shot
        else:
            self.x -= self.vel_shot

        if self.to_up==True:
            screen.blit(pygame.transform.rotate(self.image, 90.), (self.x, self.y-10))
        elif self.to_right==True:
            screen.blit(self.image, (self.x, self.y))
        else:
            screen.blit(pygame.transform.flip(self.image,True,False), (self.x-10, self.y))
