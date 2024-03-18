import pygame
from player import Player
from bomb import Bomb

class BattleGround():
    def __init__(self, groundMatrix, player, player2, bombSurface, boxGoSurface, boxSatSurface):
        self.groundMatrix = groundMatrix
        self.player = player
        self.player2 = player2
        self.bombSurface = bombSurface
        self.boxGoSurface = boxGoSurface
        self.boxSatSurface = boxSatSurface
        self.boxSize = 50
        self.groundRect = [[0 for _ in range(17)] for _ in range(17)]
        self.listBomb = []
        self.listBomb.append(player.getListBomb())
        self.listBomb.append(player2.getListBomb())
        self.rectTemp = self.boxGoSurface.get_rect(center=(-1000, 0))

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
                if value == '-':
                    if self.groundRect[i][j] !=0:
                        self.groundRect[i][j].centerx=-1000
                
                # Lấy giá trị và chỉ mục của phần tử tại hàng i, cột j
               
                index = (i, j)
        self.drawObject(screen)
    def drawBox(self, boxSurface, boxRect, screen):
        # Vẽ Box
        screen.blit(boxSurface, boxRect)

    def drawObject(self, screen):        
        # Vẽ Bomb
        for bomb in self.player.getListBomb():
            if bomb.getStatus() <= 1:
                bomb.draw(screen)
            else:
                bomb.drawBombBang(screen)
        for bomb in self.player2.getListBomb():
            if bomb.getStatus() <= 1:
                bomb.draw(screen)
            else:
                bomb.drawBombBang(screen)

        # Vẽ Player
        self.drawPlayer(screen)

    def removeBox(self, i, j, screen):
        if self.groundMatrix[i][j]=='g':
            # print(self.groundRect[i][j].centerx, '-', self.groundRect[i][j].centery)
            self.groundRect[i][j] = self.rectTemp        
            screen.blit(self.boxGoSurface, self.groundRect[i][j])
            self.groundMatrix[i][j] = '-'
    
    def getPositionPlayerInMatrix(self): 
        rectPlayer = self.player.getRect()
        indexI = round(rectPlayer.centery/50)
        indexJ = round(rectPlayer.centerx/50)
        return indexI, indexJ
    
    def getPositionObjectInMatrix(self, ObjectRect): 
        indexI = round(ObjectRect.centery/50)
        indexJ = round(ObjectRect.centerx/50)
        return indexI, indexJ
    
    def printTest(self):
        print("GroundMatrix: \n")
        for i in self.groundMatrix:
            for j in i:
                print(j, end=",")
            print()
        print("GroundRect:")
        for i in self.groundRect:
            for j in i:
                print(j.centerx, end=",")
            print()

    def checkPlayerTouchingBox(self):
        indexPlayerI, indexPlayerJ = self.getPositionPlayerInMatrix()
        check4StraightDirection_PlayerPosition = self.player.checkTouchingObj(self.groundRect[indexPlayerI][indexPlayerJ]) or self.player.checkTouchingObj(self.groundRect[indexPlayerI+1][indexPlayerJ]) or self.player.checkTouchingObj(self.groundRect[indexPlayerI-1][indexPlayerJ]) or self.player.checkTouchingObj(self.groundRect[indexPlayerI][indexPlayerJ+1]) or self.player.checkTouchingObj(self.groundRect[indexPlayerI][indexPlayerJ-1])
        check4diagonalDirection = self.player.checkTouchingObj(self.groundRect[indexPlayerI-1][indexPlayerJ+1]) or self.player.checkTouchingObj(self.groundRect[indexPlayerI+1][indexPlayerJ+1]) or self.player.checkTouchingObj(self.groundRect[indexPlayerI+1][indexPlayerJ-1]) or self.player.checkTouchingObj(self.groundRect[indexPlayerI-1][indexPlayerJ-1])
        if check4StraightDirection_PlayerPosition or check4diagonalDirection:
            return True
        return False
    
    def checkPlayer_BoxTouchingBombBang(self, screen):
        self.listBomb = []
        self.listBomb.append(self.player.getListBomb())
        self.listBomb.append(self.player2.getListBomb())
        for ListBombPlayer in self.listBomb:
            for bomb in ListBombPlayer:
                bombSize = bomb.getBombSize()
                bombRect = bomb.getRect()                
                # Check Bomb touch Player
                if bomb.getStatus() == 2: 
                    for bombBang in bomb.getBombBang():
                        if bombBang.areCollidingPlayer(self.player):
                            self.player.gameOver()
                        if bombBang.areCollidingPlayer(self.player2):
                            self.player2.gameOver()
                    #Check Bomb touch Block
                    bombIndexI, bombIndexJ = self.getPositionObjectInMatrix(bombRect)
                    bombIndexI-=1
                    bombIndexJ-=1
                    for i in range(bombIndexI, bombIndexI+bombSize+1):   
                        if i>=15:
                            break
                        if self.groundMatrix[i][bombIndexJ] == 's':
                            break
                        if self.groundMatrix[i][bombIndexJ] == 'g':
                            self.removeBox(i, bombIndexJ, screen)
                            # print("1:", i, bombIndexJ, self.groundMatrix[bombIndexJ][i])
                    for i in range(bombIndexI, bombIndexI-bombSize-1, -1):
                        if self.groundMatrix[i][bombIndexJ] == 's':
                            break
                        if self.groundMatrix[i][bombIndexJ] == 'g':
                            self.removeBox(i, bombIndexJ, screen)
                            # print("2:", i, bombIndexJ, self.groundMatrix[bombIndexJ][i])
                    for j in range(bombIndexJ, bombIndexJ+bombSize+1):
                        if j >=15: 
                            break
                        if self.groundMatrix[bombIndexI][j] == 'g':
                            self.removeBox(bombIndexI, j, screen)
                    for j in range(bombIndexJ, bombIndexJ-bombSize-1, -1):
                        if self.groundMatrix[bombIndexI][j] == 's':
                            break
                        if self.groundMatrix[bombIndexI][j] == 'g':
                            self.removeBox(bombIndexI, j, screen)
                            # print("4:", bombIndexI, j, self.groundMatrix[bombIndexI][i])
    def playerAction(self, sound_PlaceBomb):
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
            self.player.placeABomb(bombRectx, bombRecty, sound_PlaceBomb)


    def drawPlayer(self, screen):
        self.player.draw(screen)
        self.player2.draw(screen)

    def getP1(self):
        return self.player
    def getP2(self):
        return self.player2
    
    def getGroundMatrix(self):
        return self.groundMatrix

    def setGroundMatrix(self, groundMatrix):
        self.groundMatrix = groundMatrix
