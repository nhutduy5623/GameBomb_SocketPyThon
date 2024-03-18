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
from network import Network
from DTO.playerDTO import PlayerDTO
from DTO.battlegroundDTO import BattleGroundDTO
from converter.playerConvert import playerConvert
# Background





pygame.init()
screen = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()

run = False

# Player1
p1Skin = pygame.image.load('./img/Ske/idle_down (1).png')
p1SkinGhost = pygame.image.load('./img/ghost3.png')
p1Surface = pygame.transform.scale(p1Skin, (40,40))
p1SurfaceGhost = pygame.transform.scale(p1SkinGhost, (40,40))
p1SurfaceList = [p1Surface, p1SkinGhost]
p1SurfaceIndex = 0
p1Rect = pygame.Rect(0, 0, 40, 40)
p1Rect.center = (50, 50)

p2Skin = pygame.image.load('./img/Hero/idle_down (1).png')
p2Surface = pygame.transform.scale(p2Skin, (40,40))
p2SurfaceList = [p2Surface, p1SkinGhost]
p2Rect = pygame.Rect(0, 0, 40, 40)
p2Rect.center = (50, 50)

# Boom
bombSkin = pygame.image.load('./img/bomb.gif')
bombSurface1 = pygame.transform.scale(bombSkin, (50,50))
bombSurface2 = pygame.transform.scale(bombSkin, (50,53))
bombSurfaceList = [bombSurface1, bombSurface2]
bombIndex = 0
bombSurface = bombSurfaceList[bombIndex]
bombRect = bombSurface.get_rect(center=(-1000, 100))
bombP2Rect = bombSurface.get_rect(center=(-1000, 100))

# Event

# P1 Event
P1RecoverEvt = pygame.USEREVENT + 11

# P2 Event
P2RecoverEvt = pygame.USEREVENT + 21

# BombEvent
BombAnimateEvt = pygame.USEREVENT + 60
pygame.time.set_timer(BombAnimateEvt, 200)
BombBangEvent = pygame.USEREVENT + 61
pygame.time.set_timer(BombAnimateEvt, 200)

CountTimeEvt = pygame.USEREVENT + 1
pygame.time.set_timer(CountTimeEvt, 100)

# #Ground
# groundMatrix = [
#     ['-','g','-','-','-','-','-','-','-','-','-','-','g','-','-'],
#     ['-','s','-','g','-','s','-','g','-','s','-','g','-','s','-'],
#     ['g','g','-','s','-','g','-','s','-','g','-','s','-','g','g'],
#     ['-','s','-','g','-','s','-','g','-','s','-','g','-','s','-'],
#     ['-','g','-','s','-','g','-','s','-','g','-','s','-','g','-'],
#     ['-','s','-','g','-','s','-','g','-','s','-','g','-','s','-'],
#     ['-','g','-','s','-','g','-','s','-','g','-','s','-','g','-'],
#     ['-','s','-','g','-','s','-','g','-','s','-','g','-','s','-'],
#     ['-','g','-','s','-','g','-','s','-','g','-','s','-','g','-'],
#     ['-','s','-','g','-','s','-','g','-','s','-','g','-','s','-'],
#     ['-','g','-','s','-','g','-','s','-','g','-','s','-','g','-'],
#     ['-','s','-','g','-','s','-','g','-','s','-','g','-','s','-'],
#     ['g','g','-','s','-','g','-','s','-','g','-','s','-','g','g'],
#     ['-','s','-','g','-','s','-','g','-','s','-','g','-','s','-'],
#     ['-','-','-','-','-','-','-','-','-','-','-','-','g','-','-']
# ]

#Box
boxGoSkin = pygame.image.load('./img/boxgo.png')  
boxSatSkin = pygame.image.load('./img/boxsat.png')
boxGoSurface = pygame.transform.scale(boxGoSkin, (50,50))
boxSatSurface = pygame.transform.scale(boxSatSkin, (50,50))

#Âm thanh
sound_Game = pygame.mixer.Sound('sound/playgame.wav')
playmusic = pygame.USEREVENT + 71
pygame.time.set_timer(playmusic, 11500)
sound_Game.play()

sound_BombBang = pygame.mixer.Sound('sound/bomb_bang.wav')
sound_PlaceBomb = pygame.mixer.Sound('sound/newbomb.wav')



def redrawScreen(screen, bomb, groundBt):
    screen.fill((214, 165, 30))
    groundBt.drawBattleGround(screen)   
    pygame.display.update()


def main():
    run = True
    n = Network()
    battleGroundDTO = n.getBattleGround()
    p1Rect.centerx = battleGroundDTO.get_player().get_centerx()
    p1Rect.centery = battleGroundDTO.get_player().get_centery()
    bombP1 = Bomb(bombRect, bombSurfaceList)
    bombP2 = Bomb(bombP2Rect, bombSurfaceList)
    p1 = Player(p1Rect, p1SurfaceList, bombP1)
    p2 = Player(p2Rect, p2SurfaceList, bombP2)
    battleGround = BattleGround(battleGroundDTO.get_groundMatrix(), p1, p2, bombSurface, boxGoSurface, boxSatSurface)
    while run:
        battleGroundDTO = n.send(battleGroundDTO)
        p2DTO = battleGroundDTO.get_player()
        p2.setByDTO(p2DTO)
        battleGround.setGroundMatrix(battleGroundDTO.get_groundMatrix())
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
                p1.increaseTimer_BombBang(100, sound_BombBang)
                pygame.time.set_timer(CountTimeEvt, 100)
            if event.type == P1RecoverEvt:
                p1.recover()
                pygame.time.set_timer(P1RecoverEvt, 1000000000)
            if event.type == P2RecoverEvt:
                p2.recover()
                pygame.time.set_timer(P2RecoverEvt, 1000000000)
            if event.type == playmusic:
                sound_Game.play()
        clock.tick(60)
        # Vẽ lại các phần của player2
        # Cập nhật BombP2
        for bomb in p2.listBomb:
            if bomb.status == 2:
                sound_BombBang.play()
                bomb.Bang()

        battleGround.playerAction(sound_PlaceBomb)
        battleGround.checkPlayer_BoxTouchingBombBang(screen)
        if p1.isGameOver():
            p1.gameWaiting()
            pygame.time.set_timer(P1RecoverEvt, 1000)
        if p2.isGameOver():
            p2.gameWaiting()
            pygame.time.set_timer(P2RecoverEvt, 1000)

        redrawScreen(screen, bombP1, battleGround)
       


        battleGroundDTO.set_groundMatrix(battleGround.getGroundMatrix())
        p1DTO = playerConvert().toDTO(p1)
        battleGroundDTO.set_player(p1DTO)
        battleGroundDTO.set_player2(p2DTO)
main()