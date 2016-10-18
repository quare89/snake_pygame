'''
Created on 27/set/2016

@author: simone.quaresmini
'''

import os,sys, pygame, random
from pygame.locals import *

from game import Game,resource_path


# BLACK = (  0,   0,   0)
# WHITE = (255, 255, 255)
# RED = (255,   0,   0)
# GREEN = (  0, 255,   0)
# BLUE = (  0,   0, 255)
START_SNAKE_COORDS=[(2,5),(1,5),(0,5)]
START_FPS=5
APPEAR_2PT_FRUIT=5
DISAPPEAR_2PT_FRUIT=2.5
# RIGHT=(1,0)
# LEFT=(-1,0)
# UP=(0,-1)
# DOWN=(0,1)
# DIRECTION=RIGHT
# SIZE_RESTART_BUTT=50
# POSITION_RESTART_BUTT=(WINDOW_X-OFFSET_X_RIGHT-SIZE_RESTART_BUTT, WINDOW_Y-OFFSET_Y_DOWN//2-SIZE_RESTART_BUTT//2)
 

def main():
    pygame.mixer.pre_init(44100, 16, 2, 4096) #frequency, size, channels, buffersize
    pygame.init()
    
    
    #call an instance of game
    game=Game(START_SNAKE_COORDS,START_FPS)
    
    #define fonts
    BASICFONT_SCORE = pygame.font.Font(resource_path(os.path.join('resources', 'freesansbold.ttf')), 18)
    BASICFONT_GO= pygame.font.Font(resource_path(os.path.join('resources', 'freesansbold.ttf')), 40)
    
    
    pygame.display.set_caption('Snake')
    fpsClock = pygame.time.Clock()
    pygame.mixer.music.load(resource_path(os.path.join('resources', "gnam.ogg")))
    baseMusic=pygame.mixer.Sound(resource_path(os.path.join('resources', "gigi.ogg")))
    gameover_sound=pygame.mixer.Sound(resource_path(os.path.join('resources', "azz.ogg")))
    baseMusic.set_volume(0.3)
    channel=baseMusic.play(1)
    musicIsPaused=False
    game.frameCounter=0
    #main loop
    while True:
        game.frameCounter+=1
        
        #BACKGROUND
        game.display.fill(game.BLACK)
        # initialize the game field
        game.initializeWindow()
        
        #CAPTURE EVENT AND CHANGE DIRECTION
        evdir=None
        for event in pygame.event.get():
            # Capture quit event
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            #Capture restart match
            if event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                #position in the range of the button restart
                if game.POSITION_RESTART_BUTT[0] < pos[0] < game.POSITION_RESTART_BUTT[0]+game.SIZE_RESTART_BUTT and \
                game.POSITION_RESTART_BUTT[1] < pos[1] < game.POSITION_RESTART_BUTT[1]+game.SIZE_RESTART_BUTT:
                    #re-initialize game
                    game=Game(START_SNAKE_COORDS,START_FPS)
                if game.POSITION_VOL_BUTT[0] < pos[0] < game.POSITION_VOL_BUTT[0]+game.SIZE_VOL_BUTT and \
                game.POSITION_VOL_BUTT[1] < pos[1] < game.POSITION_VOL_BUTT[1]+game.SIZE_VOL_BUTT:
                    #sound
                    if musicIsPaused:
                        channel.unpause()
                        musicIsPaused=False
                    else:
                        channel.pause()
                        musicIsPaused=True
                        
            # if you do not lose the match, capture changing direction
            if game.game_over_status is False:
                if event.type==KEYDOWN:
                    evdir=game.changeDir(event)
                    if evdir is not None:
                        game.direction=evdir
                        game.move() #move the snake
                        if game.game_over_status:
                            gameover_sound.play()
                        break #just one direction for fps
        
        #if you did not change direction, move the snake 
        #in the direction that it had previously        
        if evdir is None and not game.game_over_status:
            game.move()
            if game.game_over_status:
                gameover_sound.play()
        
        
        # check if you eat fruit
        game.eatFruit()
                   
        
        if game.fruitcoords[1]==() and game.frameCounter>=APPEAR_2PT_FRUIT*(game.fps+game.score/3):
            game.locateFruit(1)
            game.frameCounter=0
        elif game.fruitcoords[1]!=() and game.frameCounter>=DISAPPEAR_2PT_FRUIT*(game.fps+game.score/3):
            game.fruitcoords[1]=tuple()
            game.frameCounter=0
            
        
        # eaten fruit becomes snake when it "leave" the tail of the snake
        game.processEatenFruit()
        
        # draw the game
        game.drawVolume(not musicIsPaused)
        game.drawsnake()
        game.drawFruit()
        game.drawScore(BASICFONT_SCORE)
        if game.game_over_status:
            game.drawGameOver(BASICFONT_GO)
        
        #update display       
        pygame.display.update()
        #change the speed with the score
        fpsClock.tick(game.fps+game.score/3)
        
if __name__ == '__main__':
    main()