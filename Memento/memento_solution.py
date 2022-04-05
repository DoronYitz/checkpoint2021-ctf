import base64
import json
import requests
import random
from collections import Counter

ROWS=8
COLS=5
URL = "http://memento.csa-challenge.com:7777/verifygame"

l1_1="W1sxNCwxNiw5LDIsNSwyMCw2LDE4XSxbNCwxLDIsMTIsMTMsNCwxNywxNF0sWzksMTAsMSwxNiwyMCwxNywxMSwzXSxbOCwxNSw3LDYsNywxOCwzLDE5XSxbMTIsOCw1LDExLDEzLDE5LDE1LDEwXV0="

def distance(x1,x2,y1,y2):
    return abs(x1-x2) + abs(y1-y2)

def getPos(board):
    pos={}
    for i in range(COLS):
        for j in range(ROWS):
            val=board[i][j]
            if board[i][j] in pos:
                pos[val][1]=(i,j)
            else:
                pos[val] = [(i, j),0]
    return pos

def getDistances(pos):
    distances={}
    for val,p in pos.items():
        distances[val]=distance(p[0][0],p[1][0],p[0][1],p[1][1])
    return distances

def encodeBoard(board):
    json_encoded_board = json.dumps(board).encode()
    b64_encoded_board = base64.b64encode(json_encoded_board)
    return b64_encoded_board

def makeHttpRequest(level,board):
    params = {'level': level, 'board':  board}
    r = requests.get(url=URL, params=params)
    result = r.json()
    return result

def getCounter(board):
    pos = getPos(board)
    distances = getDistances(pos)
    counter = Counter(distances.values())
    return counter

def getRandomBoard():
    numbers = list(range(1, 21)) + list(range(1, 21))
    board_demo = [[0] * 8, [0] * 8, [0] * 8, [0] * 8, [0] * 8]

    for i in range(5):
        for j in range(8):
            random_num = random.choice(numbers)
            board_demo[i][j] = random_num
            numbers.remove(random_num)
    return board_demo


# Created 9 demos of boards with shortest path from 1-9, used counter to check if its the correct shortest path
demo1= [[1,1,0,0,0,0,0,0] ,[2,2,0,0,0,0,0,0] , [3,3,0,0,0,0,0,0], [4,4,0,0,0,0,0,0], [5,5,0,0,0,0,0,0]]
demo2= [[1,0,1,0,0,0,0,0] ,[2,0,2,0,0,0,0,0] , [3,0,3,0,0,0,0,0], [4,0,4,0,0,0,0,0], [5,0,5,0,0,0,0,0]]
demo3= [[1,0,0,1,0,0,0,0] ,[2,0,0,2,0,0,0,0] , [3,0,0,3,0,0,0,0], [4,0,0,4,0,0,0,0], [5,0,0,5,0,0,0,0]]
demo4= [[1,0,0,0,1,0,0,0] ,[2,0,0,0,2,0,0,0] , [3,0,0,0,3,0,0,0], [4,0,0,0,4,0,0,0], [5,0,0,0,5,0,0,0]]
demo5= [[1,0,0,0,0,1,0,0] ,[2,0,0,0,0,2,0,0] , [3,0,0,0,0,3,0,0], [4,0,0,0,0,4,0,0], [5,0,0,0,0,5,0,0]]
demo6= [[1,0,0,0,0,0,1,0] ,[2,0,0,0,0,0,2,0] , [3,0,0,0,0,0,3,0], [4,0,0,0,0,0,4,0], [5,0,0,0,0,0,5,0]]
demo7= [[1,0,0,0,0,0,0,1] ,[2,0,0,0,0,0,0,2] , [3,0,0,0,0,0,0,3], [4,0,0,0,0,0,0,4], [5,0,0,0,0,0,0,5]]
demo8= [[1,5,0,0,0,0,0,0] ,[2,0,0,0,0,0,0,1] , [3,0,0,0,0,0,0,2], [4,0,0,0,0,0,5,3], [0,0,0,0,0,0,0,4]]
demo9= [[1,3,0,0,0,0,0,0] ,[2,0,0,0,0,0,0,0] , [0,0,0,0,0,0,0,1], [0,0,0,0,0,0,0,2], [0,0,0,0,0,0,3,0]]

boards=[demo1,demo2,demo3,demo4,demo5,demo6,demo7,demo8,demo9]

# Check the validity of the shortest path of each board
for board in boards:
    print(getCounter(board))
    
# Using statictics, for each demo board check the result of 0,1 - maximum result is the shortest path of the level
# Changing level manually from 1-24
attempts = 15
for board in boards:
    result=0
    encoded_board=encodeBoard(board)
    for i in range(attempts):
        result+=makeHttpRequest(level=16,board=encoded_board)
    print(f"{result/attempts}:",getCounter(board))

# 95 is _
chars=[95]
# Adding each character
for i in range(ord("a"),ord("z")+1):
    chars.append(i)
    
# Checking which char belongs to each shortest path number from 1-9
for j in range(1,10):
    print("distance:",j)
    for i in chars:
        if i%9 + 1== j:
            print(i,chr(i))


lvl0=["g","p","y"]#5
lvl1=["e","n","w"]#3
lvl2=["e","n","w"]#3
lvl3=["i","r"]#7
lvl4=["e","n","w"]#3
lvl5=["e","n","w"]#3
lvl6=["_","h","q","z"]#6
lvl7=["a","j","s"]#8
lvl8=["c","l","u"]#1
lvl9=["c","l","u"] #1
lvl10=["_","h","q","z"]#6
lvl11=["e","n","w"]#3
lvl12=["e","n","w"]#3
lvl13=["e","n","w"]#3
lvl14=["d","m","v"]#2
lvl15=["_","h","q","z"]#6
lvl16=["d","m","v"]#2
lvl17=["i","r"]#7
lvl18=["i","r"]#7
lvl19=["i","r"]#7
lvl20=["f","o","x"]#4
lvl21=["i","r"]#7
lvl22=["a","j","s"]#8
lvl23=["b","k","t"]#9
lvl24=["d","m","v"]#2

#CSA{we_all_need_mirrors}
