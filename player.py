import pygame
from asyncio.windows_utils import pipe
from distutils.spawn import spawn
from json import load
from multiprocessing.connection import wait
from tkinter import CENTER
import pygame, sys, random
from bomb import Bomb

class Player():
    def __init__(self, rect, surfaceList, bomb):
        self.rect = rect
        self.vel = 2
        self.surfaceList = surfaceList
        self.surface = surfaceList[0]
        self.maxBomb = 1
        self.listBomb = [bomb]

    def draw(self, screen):
        screen.blit(self.surface, self.rect)

    def update(seft, playerRect):
        seft.rect = playerRect

    def setSurface_Rect(self, playerRect, indexSurface):
        self.rect = playerRect
        self.surface = self.surfaceList[indexSurface]

    def move(self, direction):
        keys = pygame.key.get_pressed()
        if direction == "left":
            if self.ValidNextStep("left"):
                self.rect.centerx -= self.vel

        if direction == "right":
            if self.ValidNextStep("right"):
                self.rect.centerx += self.vel

        if direction == "up":
            if self.ValidNextStep("up"):
                self.rect.centery -= self.vel

        if direction == "down":
            if self.ValidNextStep("down"):
                self.rect.centery += self.vel

    def ValidNextStep(self, direction):
        if direction == "left":
            if self.rect.centerx - self.vel <= 50:
                return False
        if direction == "right":
            if self.rect.centerx + self.vel >= 800-50:
                return False
        if direction == "up":
            if self.rect.centery - self.vel <= 0+50:
                return False
        if direction == "down":
            if self.rect.centery + self.vel >= 800-50:
                return False
        return True
    
    def checkTouchingObk(self, Obj):
        if Obj == 0:
            return False
        if self.rect.colliderect(Obj):
            return True
        return False

    def getRect(self):
        return self.rect
    
    def getSurface(self):
        return self.surface
    
    def placeABomb(self, bombRectx, bombRecty):
        for i in range(len(self.listBomb)):
            if self.listBomb[i].getStatus() == 0:
                self.listBomb[i].setStatus(1)
                self.listBomb[i].setRectWithPosition(bombRectx,bombRecty)
                print("BombX = ", bombRectx, "BombY = ", bombRecty)
                break
            print("BombX = ", bombRectx, "BombY = ", bombRecty)
    
    def getListBomb(self):
        return self.listBomb
    
    def increaseTimer_ExplodeBomb(self, value):
        for bomb in self.listBomb:
            if bomb.getStatus()==1 or bomb.getStatus()==2:
               
                bomb.increaseTimer(value)
                if bomb.getTimer() == 2000:
                    print(bomb.getTimer())
                    bomb.Explode()
                    print("Có chạy 2")
                if bomb.getTimer() == 2500:
                    bomb.hide()
                    print("Có chạy 2")
        
            