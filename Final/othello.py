import pygame as pg
from sys import exit
import os
#import time

pg.init()
windowW = 900
windowH = 900
sectionW = windowW/3
sectionH = windowH/3
sqW = sectionW/3
sqH = sectionH/3
turn = 1
boxTaken = []
boxVal = {}
lastMove = ''
wirat = pg.image.load('kiwirat.png')#used for testing, but im keeping it bc i like it
xMark = pg.image.load('xMark.png')
lgxMark = pg.transform.scale(xMark,(sectionW,sectionH))#to fill the large squares w X
xMark = pg.transform.scale(xMark,(sqW,sqH))#to fill the small squares w X
oMark = pg.image.load('oMark.png')
lgoMark = pg.transform.scale(oMark,(sectionW,sectionH))#to fill the large squares w O
oMark = pg.transform.scale(oMark,(sqW,sqH)) #to fill the small squares w O
window = pg.display.set_mode((windowW,windowH))
sectSurface = pg.Surface((sectionW,sectionH))
sectSurface.set_alpha(123)
highlight = pg.Surface((sectionW,sectionH))
gloSectionInPlay = ''
pg.display.set_caption("notOthello")
gameWon = 0

coords = {}
secDict = {
    (0,0):'A',(1,0):'B',(2,0):'C',(0,1):'D',(1,1):'E',(2,1):'F',(0,2):'G',(1,2):'H',(2,2):'I'
}
wonSects = {v:'' for k,v in secDict.items()}
wonSects.update({'':''})
sectNums = 'xABCDEFGHI'
#print(wonSects)
clock = pg.time.Clock() # use for frame rate
section = pg.Rect(0,0,sectionW,sectionH)
def drawBoard(line=0):
    sqCol = 0
    if line == 0:
        window.fill((20,18,167))
        for i in range(3):#row
            for u in range(3):#column
                if sqCol%2 == 0:
                    pg.draw.rect(window,(215,213,207),pg.rect.Rect(u*sectionW,i*sectionH,sectionW,sectionH))
                else:
                    pg.draw.rect(window,(197,198,199),pg.rect.Rect(u*sectionW,i*sectionH,sectionW,sectionH))
                sqCol+=1
    
        for i in range(1,9):
            pg.draw.line(window,(94,125,126),(i*sectionW/3,0),(i*sectionW/3,windowH),width=1)# teal grey
            pg.draw.line(window,(94,125,126),(0,i*sectionH/3),(windowH,i*sectionH/3),width=1) #hor
    for i in range(0,4):#big lines
        pg.draw.line(window,'teal',(i*sectionW,0),(i*sectionW,windowH),width=2)#vert
        pg.draw.line(window,'teal',(0,i*sectionH),(windowH,i*sectionH),width=2)

#sqNum = '1'
def sqCoords():
    sqSect = 'A'
    coordKey = ''
    global boxVal
    for i in range(3):#big row
        for u in range(3):#big col
            sqNum = '1'
            for y in range(3):#small row
                for t in range(3): #small col
                    coordKey = sqSect + sqNum
                    coords.update({coordKey:(t*sectionW/3+u*sectionW,y*sectionH/3+i*sectionH)})
                    #print(f'i={i}, u={u}, y={y}, t={t} and coord is {coordKey}:{coords[coordKey]} ')
                    sqNum=str(int(sqNum)+1)
            sqSect = chr(ord(sqSect)+1)
    boxVal = {k:'' for k in coords} # could use = dict.fromkeys(coords,'')
    #print(boxVal)
    #print(coords)


def qSectWin():
    if gameWon != 0:
        print("Game over! Press backspace to restart game!")
        return None
    sqSect = 'A'
    box1 = ''
    box2 = ''
    box3 = ''
    for i in range(1,10):
        sectNum = sqSect + '1'
        for u in range(1,10):
            if u%3 == 0:# horizontal checks
                box1 = sqSect + str(u-2)
                box2 = sqSect + str(u-1)
                box3 = sqSect + str(u)
                if boxVal[box1] ==  boxVal[box2] and boxVal[box2] == boxVal[box3] and boxVal[box1] != '':
                    sectWin(boxVal[box1],sectNum)
            if u == 1 or u == 3: # diagonals checks
                if u == 1:    
                    box1 = sqSect + str(u)
                    box2 = sqSect + str(u+4)
                    box3 = sqSect + str(u+8)
                    if boxVal[box1] ==  boxVal[box2] and boxVal[box2] == boxVal[box3] and boxVal[box1] != '':
                        sectWin(boxVal[box1],sectNum)
                if u == 3:    
                    box1 = sqSect + str(u)
                    box2 = sqSect + str(u+2)
                    box3 = sqSect + str(u+4)
                    if boxVal[box1] ==  boxVal[box2] and boxVal[box2] == boxVal[box3] and boxVal[box1] != '':
                        sectWin(boxVal[box1],sectNum)
            if u < 4:
                box1 = sqSect + str(u)
                box2 = sqSect + str(u+3)
                box3 = sqSect + str(u+6)
                if boxVal[box1] ==  boxVal[box2] and boxVal[box2] == boxVal[box3] and boxVal[box1] != '':
                    sectWin(boxVal[box1],sectNum)
                
        sqSect = chr(ord(sqSect)+1)

def qBoardWin():
    #sqSect = 'A'
    if gameWon != 0:
        print("Game over! Press backspace to restart game!")
        return None
    box1 = ''
    box2 = ''
    box3 = ''
    for u in range(1,10):
        if u%3 == 0:# horizontal checks
            box1 = sectNums[u-2]
            box2 = sectNums[u-1]
            box3 = sectNums[u]
            if wonSects[box1] ==  wonSects[box2] and wonSects[box2] == wonSects[box3] and wonSects[box1] != '':
                gameWin(wonSects[box1]); return None
        if u == 1 or u == 3: # diagonals checks
            if u == 1:    
                box1 =  sectNums[u]
                box2 =  sectNums[u+4]
                box3 =  sectNums[u+8]
                if wonSects[box1] ==  wonSects[box2] and wonSects[box2] == wonSects[box3] and wonSects[box1] != '':
                    gameWin(wonSects[box1]); return None
            if u == 3:    
                box1 =  sectNums[u]
                box2 =  sectNums[u+2]
                box3 =  sectNums[u+4]
                if wonSects[box1] ==  wonSects[box2] and wonSects[box2] == wonSects[box3] and wonSects[box1] != '':
                    gameWin(wonSects[box1]); return None
        if u < 4:
            box1 =  sectNums[u]
            box2 =  sectNums[u+3]
            box3 =  sectNums[u+6]
            if wonSects[box1] ==  wonSects[box2] and wonSects[box2] == wonSects[box3] and wonSects[box1] != '':
                gameWin(wonSects[box1]); return None
            
    #sqSect = chr(ord(sqSect)+1)

def sectWin(side,sect):
    if gameWon != 0:
        print("Game over! Press backspace to restart game!")
        return None
    x, y = coords[sect]
    offset = 0
    cordKey = ''
    if side == 'X':
        pg.draw.rect(window,'light blue',pg.rect.Rect(x+offset,y,sectionW-offset,sectionH))
        window.blit(lgxMark,coords[sect])
        #window.blit(sectSurface,coords[sect])
        drawBoard(1)
    else:
        pg.draw.rect(window,'red',pg.rect.Rect(x+offset,y,sectionW-offset,sectionH))
        window.blit(lgoMark,coords[sect])
        #window.blit(sectSurface,coords[sect])
        drawBoard(1)
    for i in range(1,10):
        cordKey = sect[0:1] +str(i)
        boxVal[cordKey] = side
        #print(f"{cordKey}, {boxVal[cordKey]}")
    valHighlight(sectNums[int(lastMove[1])])
    wonSects[sect[0:1]] = side
    qBoardWin()

def gameWin(side):
    
    global boxVal
    global gameWon
    if gameWon != 0:
        #print("Game over! Press backspace to restart game!")
        return None
    gameWon = 1
    #boxVal = {k:'w' for k,v in boxVal.items()}
    print(f"{side} HAS WON THE GAME!")

def tttInit():# initialize tic tac toe
    drawBoard()
    sqCoords()
    #sqMatrices()
    #print(f"\n\n{matA}")
def valHighlight(valSect,any=0):
    #global highlight
    #if validSect(sect,sqNum) != False:
        #sectLet = sectNums[int(sqNum)]
        sect = valSect+'1'
        x, y = coords[sect]
        drawBoard(1)
        if turn%2 == 0:
            pg.draw.rect(window,'dark red',(x,y,sectionW+2,sectionH+2),2)
        else:
            pg.draw.rect(window,'indigo',(x,y,sectionW+2,sectionH+2),2)
        if any !=0:
            drawBoard(1)
def validSect(sect,thisMove):
    if gameWon != 0:
        print("Game over! Press backspace to restart game!")
        return None
    global lastMove
    if turn == 1:
        lastMove = sect+thisMove
        sectInPlay = sectNums[int(lastMove[1])]
        print(f"section in play is {sectInPlay}. Chosen: {sect}")
        return True
    sectInPlay = sectNums[int(lastMove[1])]
    valHighlight(sectInPlay)
    print(f"section in play is {sectInPlay}. Chosen: {sect}")
    if wonSects[sectInPlay] != '':#if a won section is chosen
        valHighlight(sectInPlay,1)
        print("anywhere!")
        return True
    if sect != sectInPlay:
        return False
    # global gloSectionInPlay
    # print(f"turn: {turn} and turncheck: {turnCheck}")
    # if turn == 1:
    #     gloSectionInPlay = sectNums[int(thisMove)]
    #     return True
    # sectInPlay = gloSectionInPlay
    # if turn > turnCheck:# Do not reassign on the same turn
    #     sectInPlay = sectNums[int(thisMove)]
    #     gloSectionInPlay = sectInPlay
    # if wonSects[sectInPlay] != '':
    #     sectInPlay = 'any!!'
    # print(f"section in play is {sectInPlay}")
    # if sectInPlay == "any!!":
    #     return True
  
    # if wonSects[sectInPlay] !='':#if this move chose a won section
    #     return True
    # if sect == sectNums[int(lastMove[1])]:
    #     return True
    # else:
    #     return False

def placeMark(tup=(0,0),boxLCoords=''):#letter cooridnates
    global turn
    global turnCheck
    global boxVal
    global lastMove
    if gameWon != 0:
        print("Game over! Press backspace to restart game!")
        return None
    if turn == 1:
        lastMove = boxLCoords
        #print(f"Sect{boxLCoords}: {sectNums[int(lastMove[1])]}")
        #if wonSects[sectNums[int(lastMove[1])]] != '':
    if validSect(boxLCoords[0],boxLCoords[1]) == False:
        print("invalid section"); return None
    if boxVal[boxLCoords] != '':
        print("occupied"); return None
    else:
        pass
        boxTaken.append(boxLCoords)
    if turn%2==0:
        boxVal[boxLCoords] = 'O'
        window.blit(oMark,tup)
    else:
        boxVal[boxLCoords] = 'X'
        window.blit(xMark,tup)
    lastMove = boxLCoords
    qSectWin()
    turn+=1

def boardReset(bgColor='black'):
    global turn
    global boxVal
    global gameWon
    global lastMove
    global wonSects
    lastMove = ''
    gameWon = 0
    coords = {}
    secDict = {
        (0,0):'A',(1,0):'B',(2,0):'C',(0,1):'D',(1,1):'E',(2,1):'F',(0,2):'G',(1,2):'H',(2,2):'I'
    }
    wonSects.clear()
    wonSects = {v:'' for k,v in secDict.items()}
    wonSects.update({'':''})
    sectNums = 'xABCDEFGHI'
    boxVal = {}
    coords = {}
    window.fill(bgColor)
    tttInit()
    turn = 1

tttInit()
print(len(coords))

while True: #game loop
    cur = pg.mouse.get_pos()
    click = pg.mouse.get_pressed()
    #window.blit(xMark,(500,500))
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()
        if event.type == pg.MOUSEBUTTONDOWN:
            mouseSq = cur[0]//sqW*100, cur[1]//sqH*100
            mouseSec = cur[0]//sectionW, cur[1]//sectionH
            #print(f'Small: {mouseSqX},{mouseSqY} Big: {mouseSecX},{mouseSecY} Section: {[mouseSec]}')
            match = next((k for (k, v) in coords.items() if v == mouseSq), None)
            print(match)
            #qSectWin()
            placeMark(coords[match],match)
            #turnCheck=turn
            valHighlight(sectNums[int(lastMove[1])])
            #qSectWin()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_BACKSPACE:
                boardReset()
            if event.unicode == '?':
                print(f"wonsects: {wonSects}")
                #print(coords)


    
    #sqCoords()
    #print(coords)
    pg.display.update()
    clock.tick(30) # set fps to 30
