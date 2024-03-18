import socket
from _thread import *
import sys
from DTO.playerDTO import PlayerDTO
from DTO.bombDTO import BombDTO
from DTO.battlegroundDTO import BattleGroundDTO
import pickle
import SystemVariable
import pygame

server = SystemVariable.serverIP
port = SystemVariable.port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")

#Ground
groundMatrix = [
    ['-','-','-','-','-','-','-','-','-','-','-','-','g','-','-'],
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
    ['-','-','-','-','-','-','-','-','-','-','-','-','g','-','-']
]

bombP1 = BombDTO(-1000, 0, 0, 0, 1)
bombP2 = BombDTO(-1000, 0, 0, 0, 1)
p1 = PlayerDTO(50, 50, 1, 1, 1, 0, [bombP1])
p2 = PlayerDTO(750, 750, 1, 1, 2, 0, [bombP2])



battleGrounds = [BattleGroundDTO(groundMatrix, p1, p2), BattleGroundDTO(groundMatrix, p2, p1)]

def threaded_client(conn, battleGround_Idex):
    conn.send(pickle.dumps(battleGrounds[battleGround_Idex]))
    reply = ""
    while True:
        try:
            data = pickle.loads(conn.recv(2048))
            battleGrounds[battleGround_Idex] = data

            if not data:
                print("Disconnected")
                break
            else:
                if battleGround_Idex == 1:
                    reply = battleGrounds[0]
                else:
                    reply = battleGrounds[1]

            conn.sendall(pickle.dumps(reply))
        except:
            break

    print("Lost connection")
    conn.close()

currentPlayer = 0
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1

