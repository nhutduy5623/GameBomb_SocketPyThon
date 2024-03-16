from ast import Return
import time
from asyncio.windows_utils import pipe
from distutils.spawn import spawn
from json import load
from multiprocessing.connection import wait
from tkinter import CENTER
import pygame, sys, random
from player import Player
from bomb import Bomb
from battleground import BattleGround
# Background





pygame.init()
screen = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()

run = False

# Player1
p1Skin = pygame.image.load('./img/Ske/idle_down (1).png')
p1Surface = pygame.transform.scale(p1Skin, (40,40))
p1SurfaceList = [p1Surface]
p1SurfaceIndex = 0
p1Rect = p1Surface.get_rect(center=(50,50))

# Boom
bombSkin = pygame.image.load('./img/bomb.gif')
bombSurface1 = pygame.transform.scale(bombSkin, (50,50))
bombSurface2 = pygame.transform.scale(bombSkin, (50,53))
bombSurfaceList = [bombSurface1, bombSurface2]
bombIndex = 0
bombSurface = bombSurfaceList[bombIndex]
bombRect = bombSurface.get_rect(center=(-1000, 100))
# BombEvent
BombAnimateEvt = pygame.USEREVENT + 60
pygame.time.set_timer(BombAnimateEvt, 200)
BombBangEvent = pygame.USEREVENT + 61
pygame.time.set_timer(BombAnimateEvt, 200)

CountTimeEvt = pygame.USEREVENT + 1
pygame.time.set_timer(CountTimeEvt, 100)

#Ground
groundMatrix = [
    ['-','-','g','-','-','-','-','-','-','-','-','-','g','-','-'],
    ['-','s','-','g','-','s','-','g','-','s','-','g','-','s','-'],
    ['g','g','-','s','-','g','-','s','-','g','-','s','-','g','g'],
    ['-','s','-','g','-','s','-','g','-','s','-','g','-','s','-'],
    ['-','g','-','s','-','g','-','s','-','g','-','s','-','g','-'],
    ['-','s','-','g','-','s','-','g','-','s','-','g','-','s','-'],
    ['-','g','-','s','-','g','-','s','-','g','-','s','-','g','-'],
    ['-','s','-','g','-','s','-','g','-','s','-','g','-','s','-'],
    ['-','g','-','s','-','g','-','s','-','g','-','s','-','g','-'],
    ['-','s','-','g','-','s','-','g','-','s','-','g','-','s','-'],
    ['-','g','-','s','-','g','-','s','-','g','-','s','-','g','-'],
    ['-','s','-','g','-','s','-','g','-','s','-','g','-','s','-'],
    ['g','g','-','s','-','g','-','s','-','g','-','s','-','g','g'],
    ['-','s','-','g','-','s','-','g','-','s','-','g','-','s','-'],
    ['-','-','g','-','-','-','-','-','-','-','-','-','g','-','-']
]

#Box
boxGoSkin = pygame.image.load('./img/boxgo.png')  
boxSatSkin = pygame.image.load('./img/boxsat.png')
boxGoSurface = pygame.transform.scale(boxGoSkin, (50,50))
boxSatSurface = pygame.transform.scale(boxSatSkin, (50,50))



def redrawScreen(screen, bomb, groundBt):
    screen.fill((255,255,255))
    groundBt.drawBattleGround(screen)   
    pygame.display.update()


def main():
    run = True
    bombP1 = Bomb(bombRect, bombSurfaceList)
    p = Player(p1Rect, p1SurfaceList, bombP1)
    battleGround = BattleGround(groundMatrix, p, bombSurface, boxGoSurface, boxSatSurface)
    battleGround.drawBattleGround(screen)
    while run:
        for event in pygame.event.get():  
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
            if event.type == BombAnimateEvt:
                if bombP1.getStatus() == 1:
                    bombP1.animate()
                pygame.time.set_timer(BombAnimateEvt, 200)
            if event.type == CountTimeEvt:
                p.increaseTimer_ExplodeBomb(100)
                pygame.time.set_timer(CountTimeEvt, 100)
                
        clock.tick(60)
        
        battleGround.playerAction()
        
        redrawScreen(screen, bombP1, battleGround)
main()