#----------------------------------
# MetroidPy
# Author: Pablo Villanueva Domingo
# Started: 13/02/2017
# Last update: 27/06/2021
#----------------------------------

# Import libraries
import pygame
from pygame.locals import *
import math
import random
import time
import warnings
from source.player import player
from source.enemies import metroid, mother_brain
from source.missil import missil
from source.background import background
from source.winning import win_anim


#ignore warning message (not working)
warnings.filterwarnings("ignore", message="known incorrect sRGB profile")

# Initialize the game
pygame.init()
width, height = 2*254, 300
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Metroid")

# Load images
backmenu = pygame.image.load("sprites/backgrounds/asteroids.png")
backmenu = pygame.transform.scale(backmenu, (width, height))
im_gameover = pygame.image.load("sprites/misc/gameover.png")
im_gameover = pygame.transform.scale(im_gameover,(width, height))
im_title = pygame.image.load("sprites/misc/title.png")
im_title = pygame.transform.scale(im_title,(im_title.get_width()*2,im_title.get_height()*2))
im_screw = pygame.image.load("sprites/misc/screw.png")
im_screw = pygame.transform.scale(im_screw,(im_screw.get_width()//2,im_screw.get_height()//2))
healthbar = pygame.image.load("sprites/misc/healthbar.png")
healthval = pygame.image.load("sprites/misc/health.png")
explosion = pygame.image.load("sprites/misc/explosion.png")
minimetroid = pygame.image.load("sprites/enemies/metroidred.png")
minimetroid = pygame.transform.scale(minimetroid,(minimetroid.get_width()//2,minimetroid.get_height()//2))


# Load audio
pygame.mixer.init()
sound_shoot = pygame.mixer.Sound("music/shoot.wav")
sound_shoot.set_volume(0.2)
sound_enemy = pygame.mixer.Sound("music/enemy.wav")
sound_enemy.set_volume(0.2)
sound_explode = pygame.mixer.Sound("music/explode.wav")
sound_explode.set_volume(0.2)

clock = pygame.time.Clock()

# Font from Metroid Fusion https://www.dafont.com/es/metroid-fusion.font
fuente = pygame.font.Font("Metroid-Fusion.ttf",30)
fuente2 = pygame.font.Font("Metroid-Fusion.ttf",20)
press_start = fuente.render("PRESS START", True, (240,200,80))
game_over = fuente.render("GAME OVER", True, (240,200,80))
victorytext1 = fuente2.render("THE GALAXY IS SAFE AGAIN", True, (240,200,80))
victorytext2 = fuente2.render("SEE YOU NEXT MISSION", True, (240,200,80))
#restart = fuente2.render("Press enter to restart", True, (240,200,80))




# Some flags
menu = True
menu = True
gameover = False
victory = False

#-----------------
# Menu screen
#-----------------

pygame.mixer.music.load("music/title_theme.mp3")
pygame.mixer.music.set_volume(0.6)
pygame.mixer.music.play(-1, 0.0)

while menu==True:

    # Draw the scenario
    screen.fill(0)
    screen.blit(backmenu,(0,0))
    screen.blit(im_title,(width/2-im_title.get_width()/2,40))
    screen.blit(im_screw,(width/2-im_screw.get_width()/2,height/2))
    screen.blit(press_start,(width/2-press_start.get_width()/2,3*height/4))

	# Events
    for event in pygame.event.get():

        if event.type==pygame.QUIT:
            pygame.quit()
            exit(0)

        if event.type == pygame.KEYDOWN:
            if event.key==K_RETURN:
                menu = False

    pygame.display.flip()



#-----------------
# Initialize classes
#-----------------

# Background
back = background()

# Initialize player
player = player(width//2-13, height-85) # 13 is half the size of the Samus sprite

# Initialize enemies
list_metroids = [ metroid(width-50,height//2+80,True,2),
                  metroid(width/2,height//2,False,2),
                  metroid(width//4,height//2-85,True,3),
                  metroid(width//2+50,height//2,False,3),
                  metroid(width//2+100,3*height//4,True,3),
                  metroid(width//5,height//2-115,True,4),
                  metroid(3*width//4,3*height//4,False,4),
                  metroid(width//2,height//2+30,True,4),
                  metroid(3*width//4+50,height//2-100,True,4),
                  metroid(width//2-30,height//2,True,5,"blue"),
                  metroid(width//2,height//2-30,False,5,"blue"),
                  metroid(width//2,height//2+30,True,5,"blue"),
                ]

# Final boss
motherbrain = mother_brain(3*width//4, height//2+20, 1)
list_enemies = []#list_metroids
list_enemies.append(motherbrain)

# Initialize shots
list_shots = []

# Start in first scene
scene = 1


#-----------------
# Opening scene
#-----------------

pygame.mixer.music.load("music/intro_fanfare.mp3")
pygame.mixer.music.play(0, 0.0)
back.draw_background(screen, scene)
screen.blit(player.image, (player.x, player.y))
pygame.display.update()
time.sleep(5.)


pygame.mixer.music.load("music/brinstar.mp3")
pygame.mixer.music.play(-1, 0.)

#-----------------
# Main loop
#-----------------

while 1:
    while (gameover==False) and (victory==False):

        # Draw background
        back.draw_background(screen, scene)

        # Enemy counter
        screen.blit(minimetroid, (width-50,5))
        counter = fuente2.render(str(len(list_metroids)), True, (240,200,80))
        screen.blit(counter, (width-25,5))

        # Draw healthbar
        screen.blit(healthbar, (5,5))
        for x in range(player.health):
            screen.blit(healthval,(x+8,8))

        # Update player times
        if player.jump==True:
            player.jumptime+=1
        player.timerun+=1
        if player.timerun >= len(player.list_run)*player.t_run:
            player.timerun = 0

        # Show player image
        player.imagesamus(screen)

        # Draw shots
        for bullet in list_shots:
            bullet.draw_shot(screen)
            if bullet.x<-bullet.image.get_width()/2 or bullet.x>width or bullet.y<0 or bullet.y>height:
                list_shots.remove(bullet)

        # Update metroids
        for enemy in list_enemies:
            if enemy.scene==scene:

                # Show enemy
                enemy.draw(screen)

                # Move metroid
                enemy.movement(player.x, player.y)

                enemyrect = enemy.rect
                enemyrect.top = enemy.y
                enemyrect.left = enemy.x

                # Enemies hit
                for bullet in list_shots:
                    missilrect = bullet.rect
                    missilrect.left = bullet.x
                    missilrect.top = bullet.y
                    if enemyrect.colliderect(missilrect):
                        enemy.health-=1
                        sound_enemy.play()
                        list_shots.remove(bullet)
                        if enemy.health<=0:
                            sound_explode.play()
                            screen.blit(explosion, (enemy.x, enemy.y))
                            enemy.death()
                            list_enemies.remove(enemy)

                if player.morf==True:
                    samusrect=pygame.Rect(player.im_morf1.get_rect())
                    samusrect.top=player.y+30
                else:
                    samusrect=pygame.Rect(player.im_stop.get_rect())
                    samusrect.top=player.y
                samusrect.left=player.x
                if enemyrect.colliderect(samusrect):
                    player.health-=1


    	# Events
        for event in pygame.event.get():

            if event.type==pygame.QUIT:
                pygame.quit()
                exit(0)

            if event.type == pygame.KEYDOWN:
                if event.key==K_SPACE:
                    player.up = False
                    if player.jump==False:
                        player.jump=True
                        player.jumptime=0
                if (event.key==K_LEFT) or (event.key==K_RIGHT):
                    if event.key==K_LEFT:   player.move_left=True
                    elif event.key==K_RIGHT:    player.move_right=True
                    timerun = 0
                    player.up = False
                if event.key==K_DOWN:
                    player.morf=True
                    player.up = False
                elif event.key==K_UP:
                    if player.morf==True:
                        player.morf=False
                    else:
                        if player.jump==False:
                            player.up = True

                if event.key==K_x:
                    sound_shoot.play()
                    list_shots.append( missil(player.x+player.im_stop.get_width()/2, player.y+15, player.to_right, player.up) )

            if event.type == pygame.KEYUP:
                if event.key==pygame.K_LEFT:
                    player.move_left=False
                elif event.key==pygame.K_RIGHT:
                    player.move_right=False

        # Move player
        player.move_player()

        # Change scene
        if player.x>width-player.im_stop.get_width():
            if scene<back.numscenes:
                scene+=1
                player.x=0
            else:
                player.x=width-player.im_stop.get_width()
        if player.x<0:
            if scene>1:
                scene-=1
                player.x=width-player.im_stop.get_width()
            else:
                player.x=0

        if player.health<=0:
            gameover = True

        pygame.display.update()
        #pygame.display.flip()
        time.sleep(0.01)

        if gameover==True:

            #-----------------
            # Game over screen
            #-----------------

            #screen.blit(im_gameover, (0,0))
            screen.blit(backmenu,(0,0))
            screen.blit(game_over,(width/2-game_over.get_width()/2,height/2-game_over.get_height()/2))
            pygame.mixer.music.load("music/title_theme.mp3")
            pygame.mixer.music.play(-1, 0.0)

        # Win when come back to the spaceship
        if (player.x < width//2) and (scene == 1) and (motherbrain.alive == False) and (len(list_enemies)==0):

            victory = True
            pygame.mixer.music.load("music/Metroid (NES) Music - Ending Theme.mp3")
            pygame.mixer.music.play(-1, 0.0)
            winanim = win_anim()


    while (victory==True):

        #-----------------
        # Win screen
        #-----------------

        screen.fill(0)
        screen.blit(backmenu,(0,0))
        screen.blit(victorytext1,(width/2-victorytext1.get_width()/2,height/4))
        screen.blit(victorytext2,(width/2-victorytext2.get_width()/2,3*height/4))

        instant = pygame.time.get_ticks()/100
        winanim.win_animation(screen, instant)
        for event in pygame.event.get():

            if event.type==pygame.QUIT:
                pygame.quit()
                exit(0)

        clock.tick(10)
        pygame.display.update()


    for event in pygame.event.get():
        """
        if event.type == pygame.KEYDOWN:
            if event.key==K_RETURN:
                gameover=False
                player.health = 194
        """

        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)

    pygame.display.update()
    #pygame.display.flip()
