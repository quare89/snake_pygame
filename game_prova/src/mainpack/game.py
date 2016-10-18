'''
Created on 03/ott/2016

@author: simone.quaresmini
'''
import sys, pygame, random,os
from pygame.locals import *

class Game(object):
    '''
    classdocs
    '''
    
    SQUARE_UNIT=17
    Y_SIZE=20
    X_SIZE=20
    
    
    OFFSET_X_RIGHT=15
    OFFSET_X_LEFT=15
    OFFSET_Y_UP=15
    OFFSET_Y_DOWN=75
    WINDOW_X=X_SIZE*SQUARE_UNIT+OFFSET_X_RIGHT+OFFSET_X_LEFT
    WINDOW_Y=Y_SIZE*SQUARE_UNIT+OFFSET_Y_UP+OFFSET_Y_DOWN
    
    BLACK = (  0,   0,   0)
    WHITE = (255, 255, 255)
    RED = (255,   0,   0)
    GREEN = (  0, 255,   0)
    BLUE = (  0,   0, 255)
    #START_SNAKE_COORDS=[(2,5),(1,5),(0,5)]
    RIGHT=(1,0)
    LEFT=(-1,0)
    UP=(0,-1)
    DOWN=(0,1)
   
    SIZE_RESTART_BUTT=50
    SIZE_VOL_BUTT=40
    POSITION_RESTART_BUTT=(WINDOW_X-OFFSET_X_RIGHT-SIZE_RESTART_BUTT, WINDOW_Y-OFFSET_Y_DOWN//2-SIZE_RESTART_BUTT//2)
    POSITION_VOL_BUTT=(OFFSET_X_RIGHT*2, WINDOW_Y-OFFSET_Y_DOWN//2-SIZE_VOL_BUTT//2)
    
    display = pygame.display.set_mode((WINDOW_X, WINDOW_Y), 0, 32)
    

    def __init__(self,starting_coords,starting_fps):
        '''
        Constructor
        '''
        self.frameCounter=0
        self.game_over_status=False
        self.score=0
        self.fps=starting_fps
        self.snakecoords=starting_coords
        self.old_fruitcoords=[]
        self.direction=self.RIGHT
        self.fruitcoords=[(),()]
        self.locateFruit(0)
        
    def drawsnake(self):
        for i,coord in enumerate(self.snakecoords[::-1]):
            convcoords=self.convertCoords(coord)
            if i==len(self.snakecoords)-1:
                self.drawHead(coord)
            else:
                self.drawImage(resource_path(os.path.join('resources', "body2.png")), (convcoords[0]+1,convcoords[1]+1))    
    
    def drawHead(self,coord):
        convcoords=self.convertCoords(coord)
        if self.game_over_status:
            img="head_end1.png"
        elif self.snakeClosedToFruit():
            img="head_open1.png"
        else:
            img="head_closed1.png"
        self.drawImage(resource_path(os.path.join('resources', img)), (convcoords[0]+1,convcoords[1]+1),self.direction)
        #snakeRect=pygame.Rect(convcoords[0]+1,convcoords[1]+1,SQUARE_UNIT-1,SQUARE_UNIT-1)
        #pygame.draw.rect(display, BLUE, snakeRect)
    
    def drawFruit(self):
        for i,coords in enumerate(self.fruitcoords):
            if coords==():
                continue
            fc=self.convertCoords(coords)
            img=None
            if i==0:
                img="maialino.png"
            elif i==1:
                img="beer2.png"
            
            self.drawImage(resource_path(os.path.join('resources', img)), (fc[0]+1,fc[1]+1))
        
    def randomCoords(self):
        coords = random.randint(0,self.X_SIZE-1),random.randint(0,self.Y_SIZE-1)
        return coords
    
    def initializeWindow(self):
        a=self.convertCoords((0,0))
        b=self.convertCoords((self.X_SIZE,0))
        c=self.convertCoords((self.X_SIZE,self.Y_SIZE))
        d=self.convertCoords((0,self.Y_SIZE))
        lati=[a,b,c,d]
        for i,coord in enumerate(lati):
            pygame.draw.line(self.display,self.WHITE,coord,lati[(i+1)%4])
        self.drawImage(resource_path(os.path.join('resources', "ground.jpg")), tuple(map(sum,zip(self.convertCoords((0,0)),(1,1)))))
        self.drawImage(resource_path(os.path.join('resources', "redo2.png")),self.POSITION_RESTART_BUTT)
        #for i in range(1,Y_SIZE):
        #    pygame.draw.line(display,WHITE,convertCoords((0,i)),convertCoords((X_SIZE,i)))
        #for j in range(1,X_SIZE):
        #    pygame.draw.line(display,WHITE,convertCoords((j,0)),convertCoords((j,Y_SIZE)))
    
    
    def move(self):
        self.game_over_status=False
        
        new_head_coord=((self.snakecoords[0][0]+self.direction[0])%(self.X_SIZE),(self.snakecoords[0][1]+self.direction[1])%(self.Y_SIZE))
        if new_head_coord in self.snakecoords[0:-1]:
            self.game_over_status=True
            
        self.snakecoords=[new_head_coord]+self.snakecoords[0:-1]
        
    def eatFruit(self):
        for i in range(0,len(self.fruitcoords)):
            if self.fruitcoords[i] in self.snakecoords:
                pygame.mixer.music.play(0,1.77)
                
                if i==0:
                    self.score+=1
                elif i==1:
                    self.score+=2
                    
                self.old_fruitcoords+=[self.fruitcoords[i]]
                if i==0:
                    self.locateFruit(0)
                elif i==1:
                    self.fruitcoords[i]=tuple()
                    self.frameCounter=0
           
    def locateFruit(self,indexFruit):
        while True:
            coords=self.randomCoords()
            if coords not in self.snakecoords and coords not in self.fruitcoords:
                self.fruitcoords[indexFruit]=coords
                break
    
    def changeDir(self,event):
        direc=None
        
        if event.key==K_UP and self.direction!=self.DOWN:
            direc=self.UP
        elif event.key==K_DOWN and self.direction!=self.UP:
            direc=self.DOWN
        elif event.key==K_LEFT and self.direction!=self.RIGHT:
            direc=self.LEFT
        elif event.key==K_RIGHT and self.direction!=self.LEFT:
            direc=self.RIGHT
        return direc
               
    def drawText(self,fontObj,string,bkgColor,fontColor,center):
        textSurfaceObj = fontObj.render(string, True, bkgColor,fontColor)
        textRectObj = textSurfaceObj.get_rect()
        textRectObj.center = center
        self.display.blit(textSurfaceObj, textRectObj)
     
    def drawScore(self,fontObj):
        self.drawText(fontObj,"Score: %s" % self.score,self.WHITE,self.BLACK,(self.WINDOW_X//2, self.WINDOW_Y-self.OFFSET_Y_DOWN//2))
           
    def drawGameOver(self,fontObj):
        self.drawText(fontObj,'Game Over',self.WHITE,self.RED,self.convertCoords((self.X_SIZE//2,self.Y_SIZE//2)))
    
    def drawVolume(self,volumeOn):
        if volumeOn:
            img="vol.png"
        else:
            img="volOff.png"
        self.drawImage(resource_path(os.path.join('resources', img)),self.POSITION_VOL_BUTT)
        
    def processEatenFruit(self):
        #in old_fruitcoords there is the fruit that will become the tail of the snake
        for ofc in self.old_fruitcoords:
            if ofc not in self.snakecoords:
                self.snakecoords+=[ofc]
                self.old_fruitcoords.remove(ofc)
    
    def convertCoords(self,coord):
        return coord[0]*self.SQUARE_UNIT+self.OFFSET_X_RIGHT,coord[1]*self.SQUARE_UNIT+self.OFFSET_Y_UP                
     
    def drawImage(self,filename,coords,direcH=RIGHT):
        image=pygame.image.load(filename).convert_alpha()
        if direcH==self.RIGHT:
            pass
        elif direcH==self.UP:
            image=pygame.transform.rotate(image,90)
        elif direcH==self.LEFT:
            image=pygame.transform.rotate(image,180)
        elif direcH==self.DOWN:
            image=pygame.transform.rotate(image,270)
          
        self.display.blit(image, coords)   
        
    def snakeClosedToFruit(self):
        for fc in self.fruitcoords:
            if fc==():
                continue
            
            coordA=self.snakecoords[0]
            coordB=fc
            if (coordA[0]+1==coordB[0] and coordA[1]==coordB[1]) or \
                (coordA[0]-1==coordB[0] and coordA[1]==coordB[1]) or \
                (coordA[1]+1==coordB[1] and coordA[0]==coordB[0]) or \
                (coordA[1]-1==coordB[1] and coordA[0]==coordB[0]):
                return True
        return False

def resource_path(relative):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.join(relative)