import pygame
class Explore():
    def __init__(self, surfaceExplore):
        self.rect = 1000
        self.surfaceExplore = surfaceExplore
        self.bombExplodeSize = 1

    def drawExplore(self, screen):
        screen.blit(self.surfaceExplore, self.rect)

    def setRectCenterx(self, value):
        self.rect.centerx=value
    
    def setRectCentery(self, value):
        self.rect.centery=value

    def setRectCenterX_Y(self, centerx, centery):
        self.rect = self.surfaceExplore.get_rect(center=(centerx, centery))

    def setRect(self, rect):
        self.rect = rect

    def getRect(self):
        return self.rect
    
    def hide(self):
        self.rect = self.surfaceExplore.get_rect(center=(-1000, 0))
        self.status = 0  

    # def setUpSurfaceExplore(self):
    #     for i in range(1, 5):
    #         arrayTemp = []
    #         if i==1:
    #             direction = 'up'
    #         if i==2:
    #             direction = 'down'
    #         if i==3:
    #             direction = 'left'
    #         if i==4:
    #             direction = 'right'
    #         for j in range(1, 11):
    #             skin = pygame.image.load('./img/Bomb/bombbang_'+direction+''+j+'.png')
    #             if i==1 or i==2:
    #                 arrayTemp.append(pygame.transform.scale(skin, (50,50*j)))
    #             else:
    #                 arrayTemp.append(pygame.transform.scale(skin, (50*j,50)))
    #         self.Explode_Surface.append(arrayTemp)
        