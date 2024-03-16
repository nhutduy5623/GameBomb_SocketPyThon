import pygame
from player import Player
from bomb import Bomb

class BattleGround():
    def __init__(self, groundMatrix, player, bombSurface, boxGoSurface, boxSatSurface):
        self.groundMatrix = groundMatrix
        self.player = player
        self.bombSurface = bombSurface
        self.boxGoSurface = boxGoSurface
        self.boxSatSurface = boxSatSurface
        self.boxSize = 50
        self.groundRect = [[0 for _ in range(16)] for _ in range(16)]

    def drawBattleGround(self, screen):
        for i in range(len(self.groundMatrix)):  # Duyệt qua các hàng
            for j in range(len(self.groundMatrix)):  # Duyệt qua các cột của hàng đó
                value = self.groundMatrix[i][j]
                if value == 's':
                    self.groundRect[i][j] = self.boxSatSurface.get_rect(center=((j+1)*self.boxSize,(i+1)*self.boxSize))
                    self.drawBox(self.boxSatSurface, self.groundRect[i][j], screen)
                if value == 'g':
                    self.groundRect[i][j] = self.boxGoSurface.get_rect(center=((j+1)*self.boxSize, (i+1)*self.boxSize))
                    self.drawBox(self.boxGoSurface, self.groundRect[i][j], screen)
                # Lấy giá trị và chỉ mục của phần tử tại hàng i, cột j
               
                index = (i, j)
    def drawBox(self, boxSurface, boxRect, screen):
        screen.blit(boxSurface, boxRect)
        for bomb in self.player.getListBomb():
            if bomb.getStatus() <= 1:
                bomb.draw(screen)
            else:
                bomb.drawExplore(screen)
        self.drawPlayer(screen)
    
    def getPositionPlayerInMatrix(self): 
        rectPlayer = self.player.getRect()
        indexI = int(rectPlayer.centery/50)
        indexJ = int(rectPlayer.centerx/50)
        return indexI, indexJ
    
    def checkPlayerTouchingBox(self):
        indexPlayerI, indexPlayerJ = self.getPositionPlayerInMatrix()
        check4StraightDirection_PlayerPosition = self.player.checkTouchingObk(self.groundRect[indexPlayerI][indexPlayerJ]) or self.player.checkTouchingObk(self.groundRect[indexPlayerI+1][indexPlayerJ]) or self.player.checkTouchingObk(self.groundRect[indexPlayerI-1][indexPlayerJ]) or self.player.checkTouchingObk(self.groundRect[indexPlayerI][indexPlayerJ+1]) or self.player.checkTouchingObk(self.groundRect[indexPlayerI][indexPlayerJ-1])
        check4diagonalDirection = self.player.checkTouchingObk(self.groundRect[indexPlayerI-1][indexPlayerJ+1]) or self.player.checkTouchingObk(self.groundRect[indexPlayerI+1][indexPlayerJ+1]) or self.player.checkTouchingObk(self.groundRect[indexPlayerI+1][indexPlayerJ-1]) or self.player.checkTouchingObk(self.groundRect[indexPlayerI-1][indexPlayerJ-1])
        if check4StraightDirection_PlayerPosition or check4diagonalDirection:
            return True
        return False

    def playerAction(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player.move("left")
            if self.checkPlayerTouchingBox():
                self.player.move("right")
        if keys[pygame.K_RIGHT]:
            self.player.move("right")
            if self.checkPlayerTouchingBox():
                self.player.move("left")
        if keys[pygame.K_UP]:
            self.player.move("up")
            if self.checkPlayerTouchingBox():
                self.player.move("down")
        if keys[pygame.K_DOWN]:
            self.player.move("down")
            if self.checkPlayerTouchingBox():
                self.player.move("up")
        if keys[pygame.K_SPACE]:
            bombRecty, bombRectx = self.getPositionPlayerInMatrix()
            bombRectx*=50; bombRecty*=50
            self.player.placeABomb(bombRectx, bombRecty)


    def drawPlayer(self, screen):
        self.player.draw(screen)

