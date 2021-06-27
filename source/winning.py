
import pygame

# Winning animation
class win_anim():
    def __init__(self):

        win1 = pygame.image.load("sprites/samus/win1.png")
        win2 = pygame.image.load("sprites/samus/win2.png")
        win3 = pygame.image.load("sprites/samus/win3.png")
        self.winims = [win1, win2, win3]

        self.time_change = 4
        self.ind_im = 0

    def win_animation(self, screen, instant):

        width, height = screen.get_width(), screen.get_height()

        if int(instant) % int(self.time_change) == 0:
            self.ind_im += 1

            if self.ind_im > len(self.winims)-1:
                self.ind_im = 0

        im = self.winims[self.ind_im]
        screen.blit(im,(width/2-im.get_width()/2,height/2-im.get_height()/2))
