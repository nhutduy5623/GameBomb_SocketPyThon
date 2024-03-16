import pygame
from explore import Explore

class Bomb():
    def __init__(self, rect, surfaceList):
        self.rect = rect
        self.surfaceList = surfaceList
        self.surfaceIndex = 0
        self.surface = surfaceList[self.surfaceIndex]
        self.status = 0
        self.timer = 0
        self.bombExplodeSize = 1        
        self.Explode_Surface = []
        self.setUpSurfaceExplore()
        self.bombExplode = [Explore(self.Explode_Surface[0][0]),Explore(self.Explode_Surface[1][0]),Explore(self.Explode_Surface[2][0]),Explore(self.Explode_Surface[3][0])]


    def animate(self):
        if self.surfaceIndex == 0:
            self.rect.centery -=3
            self.surfaceIndex = 1
        else:
            self.rect.centery +=3
            self.surfaceIndex = 0
        self.surface = self.surfaceList[self.surfaceIndex]

    def draw(self, screen):
        screen.blit(self.surface, self.rect)
    
    def drawExplore(self, screen):
        for explore in self.bombExplode:
            explore.drawExplore(screen)

    def placeABomb(seft, playerRect):
        seft.status = 1
        seft.rect = playerRect

    def setSurface_Rect(self, playerRect, indexSurface):
        self.rect = playerRect
        self.surface = self.surfaceList[indexSurface]

    def setStatus(self, status):
        self.status = status
        if status == 1:
            self.timer=0

    def getStatus(self):
        return self.status
    
    def setRect(self, rect):
        self.rect = rect

    def getRect(self):
        return self.rect
    
    def setRectWithPosition(self, bombRectx, bombRecty):
        self.rect = self.surface.get_rect(center=(bombRectx, bombRecty))

    def increaseTimer(self, value):
        self.timer+=value
    
    def getTimer(self):
        return self.timer
    
    def Explode(self):
        self.status = 2
        i=0
        for explore in self.bombExplode:
            if i==0:
                explore.setRectCenterX_Y(self.getRect().centerx,self.getRect().centery-35*self.bombExplodeSize)
            elif i==1:
                explore.setRectCenterX_Y(self.getRect().centerx,self.getRect().centery+35*self.bombExplodeSize)
            elif i==2:
                explore.setRectCenterX_Y(self.getRect().centerx-35*self.bombExplodeSize,self.getRect().centery)
            elif i==3:
                explore.setRectCenterX_Y(self.getRect().centerx+35*self.bombExplodeSize,self.getRect().centery)
            i+=1
        
    
    def hide(self):
        self.rect = self.surface.get_rect(center=(-1000, 0))
        for explore in self.bombExplode:
            explore.hide()
        self.status = 0
        

    def setUpSurfaceExplore(self):
        for i in range(1, 5):
            arrayTemp = []
            if i==1:
                direction = 'up'
            if i==2:
                direction = 'down'
            if i==3:
                direction = 'left'
            if i==4:
                direction = 'right'
            for j in range(1, 11):
                print(i)
                skin = pygame.image.load('./img/Bomb/bombbang_'+str(direction)+''+str(j)+'.png')
                print(direction)
                if i==1 or i==2:
                    arrayTemp.append(pygame.transform.scale(skin, (50,45*(j+1))))
                else:
                    arrayTemp.append(pygame.transform.scale(skin, (45*(j+1),50)))
            self.Explode_Surface.append(arrayTemp)
        