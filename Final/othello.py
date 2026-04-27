import pygame as pg# so i dont have to always type "pygame." and its just "pg"
from sys import exit

pg.init()
#set up window dimensions. do not change (as of now)
windowW = 900
windowH = 900
sectionW = windowW/3
sectionH = windowH/3
sqW = sectionW/3
sqH = sectionH/3

turn = 1# start with X
boxVal = {}
lastMove = ''
wirat = pg.image.load('kiwirat.png')#used for testing, but im keeping it bc i like it. exclamation point for surprise
xMark = pg.image.load('xMark.png')
lgxMark = pg.transform.scale(xMark,(sectionW,sectionH))#to fill the large squares w X
xMark = pg.transform.scale(xMark,(sqW,sqH))#to fill the small squares w X
oMark = pg.image.load('oMark.png')
lgoMark = pg.transform.scale(oMark,(sectionW,sectionH))#to fill the large squares w O
oMark = pg.transform.scale(oMark,(sqW,sqH)) #to fill the small squares w O
# make window and surface and all
window = pg.display.set_mode((windowW,windowH))
pg.display.set_caption("notOthello")#because othello was the original thought; window name2
font = pg.font.Font(None,int(sqW))

gameWon = 0

def write(string,color=(181,105,255)):
    textSur = font.render(string,True,color)
    screenCent = textSur.get_rect(center=(windowW/2,windowH/2))
    window.blit(textSur,(screenCent))

coords = {}
secDict = {
    (0,0):'A',(1,0):'B',(2,0):'C',(0,1):'D',(1,1):'E',(2,1):'F',(0,2):'G',(1,2):'H',(2,2):'I'
}# Fixed coordinates for the big squares
wonSects = {v:'' for k,v in secDict.items()} #new dict, copy secDict's key and make the values empty strings. Will keep track of won sections
wonSects.update({'':''}) #if i recall having this here was to fix a key error. i dont remember where, may have fixed it but for now I'll leave it for security
sectNums = 'xABCDEFGHI'# i call from this string with section number, x is there to offset that it starts from zero. my sections are 1-9
clock = pg.time.Clock() # use for frame rate

def drawBoard(line=0):# As it's called, to draw the board
    sqCol = 0
    if line == 0:
        for i in range(3):#row
            for u in range(3):#column
                if sqCol%2 == 0:
                    pg.draw.rect(window,(215,213,207),pg.rect.Rect(u*sectionW,i*sectionH,sectionW,sectionH))
                else:
                    pg.draw.rect(window,(197,198,199),pg.rect.Rect(u*sectionW,i*sectionH,sectionW,sectionH))
                sqCol+=1
    
        for i in range(1,9):# small dividing lines
            pg.draw.line(window,(94,125,126),(i*sectionW/3,0),(i*sectionW/3,windowH),width=1)# teal grey
            pg.draw.line(window,(94,125,126),(0,i*sectionH/3),(windowH,i*sectionH/3),width=1) #hor
    for i in range(0,4):#big lines
        pg.draw.line(window,'teal',(i*sectionW,0),(i*sectionW,windowH),width=2)#vert
        pg.draw.line(window,'teal',(0,i*sectionH),(windowH,i*sectionH),width=2)

def sqCoords():# to give coordinates to each small square, uses dictionary. should depend on window size.
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
                    sqNum=str(int(sqNum)+1)
            sqSect = chr(ord(sqSect)+1)
    boxVal = {k:'' for k in coords} # could use = dict.fromkeys(coords,'')
    #above line is to make a dictionary for keeping track of which squares are occupied and by whom


def qSectWin():# checks if a section was won. should be after every time a square is placed
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
                if boxVal[box1] ==  boxVal[box2] and boxVal[box2] == boxVal[box3] and boxVal[box1] != '':#empty quotes are to make sure i dont cite empty squares in a row as a success
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
            if u < 4:# vertical checks
                box1 = sqSect + str(u)
                box2 = sqSect + str(u+3)
                box3 = sqSect + str(u+6)
                if boxVal[box1] ==  boxVal[box2] and boxVal[box2] == boxVal[box3] and boxVal[box1] != '':
                    sectWin(boxVal[box1],sectNum)
                
        sqSect = chr(ord(sqSect)+1)

def qBoardWin():#to check the sections to see if someone has met game winning conditions
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
        if u < 4:# vertical
            box1 =  sectNums[u]
            box2 =  sectNums[u+3]
            box3 =  sectNums[u+6]
            if wonSects[box1] ==  wonSects[box2] and wonSects[box2] == wonSects[box3] and wonSects[box1] != '':
                gameWin(wonSects[box1]); return None
            
def sectWin(side,sect):# what to do when a section is won
    if gameWon != 0:# so that more squares/actions can't be taken after a win. must clear board w/ backspace
        print("Game over! Press backspace to restart game!")
        return None
    x, y = coords[sect]
    offset = 0
    cordKey = ''
    if side == 'X':
        pg.draw.rect(window,'light blue',pg.rect.Rect(x+offset,y,sectionW-offset,sectionH)) # put a colored rectangle and the winning symbol. wanted rectangle to be lower opacity so you could still see the smaller board
        window.blit(lgxMark,coords[sect])
        drawBoard(1)
    else:
        pg.draw.rect(window,'red',pg.rect.Rect(x+offset,y,sectionW-offset,sectionH))
        window.blit(lgoMark,coords[sect])
        drawBoard(1)
    for i in range(1,10):
        cordKey = sect[0:1] +str(i)
        boxVal[cordKey] = side
    valHighlight(sectNums[int(lastMove[1])])
    wonSects[sect[0:1]] = side
    qBoardWin()# after any section win check if the game was won

def gameWin(side):# procedure for if a game is won
    
    global boxVal
    global gameWon
    if gameWon != 0: #if the game was already won, don't keep printing
        return None
    gameWon = 1
    write(str(side)+" has won the game!")
    print(f"{side} HAS WON THE GAME!")

def tttInit():# initialize tic tac toe
    drawBoard()
    sqCoords()
 
def valHighlight(valSect,any=0):#highlight the section in play
        sect = valSect+'1'
        x, y = coords[sect]
        drawBoard(1)
        if turn%2 == 0:#for O
            pg.draw.rect(window,'dark red',(x,y,sectionW+2,sectionH+2),2)#planned to make a colored square, but couldn't get them to disappear. the boarder works because lines are redrawn every move
        else:# for X
            pg.draw.rect(window,'indigo',(x,y,sectionW+2,sectionH+2),2)
        if any !=0:
            drawBoard(1)
def validSect(sect,thisMove):#check if the clicked section is in play
    if gameWon != 0:
        print("Game over! Press backspace to restart game!")
        return None
    global lastMove
    if turn == 1:# different proecedure for turn 1, as there was no previous move
        lastMove = sect+thisMove
        sectInPlay = sectNums[int(lastMove[1])]
        print(f"section in play is {sectInPlay}. Chosen: {sect}")
        return True
    sectInPlay = sectNums[int(lastMove[1])]#set the section in play to square corresponding to last clicked little square
    valHighlight(sectInPlay)#highlight the section in play
    print(f"section in play is {sectInPlay}. Chosen: {sect}")
    if wonSects[sectInPlay] != '':#if the section that *would* have been in play is won, let player go anywhere
        valHighlight(sectInPlay,1)
        print("anywhere!")
        return True
    if sect != sectInPlay:#if they chose a section not in play, return false
        return False

def placeMark(tup=(0,0),boxLCoords=''):#place mark in given box, given the section is in play
    global turn
    global turnCheck
    global boxVal
    global lastMove
    if gameWon != 0:
        print("Game over! Press backspace to restart game!")
        return None
    if turn == 1:
        lastMove = boxLCoords
    if validSect(boxLCoords[0],boxLCoords[1]) == False:
        print("invalid section"); return None
    if boxVal[boxLCoords] != '':
        print("occupied"); return None
    else:
        pass
    if turn%2==0:
        boxVal[boxLCoords] = 'O'
        window.blit(oMark,tup)
    else:
        boxVal[boxLCoords] = 'X'
        window.blit(xMark,tup)
    lastMove = boxLCoords
    qSectWin()#after any move, check if a section was won
    turn+=1

def boardReset(bgColor='black'):# titular
    global turn
    global boxVal
    global gameWon
    global lastMove
    global wonSects
    lastMove = ''
    gameWon = 0
    coords = {}# empty all the dictionaries so the loops can reset them.
    secDict = {
        (0,0):'A',(1,0):'B',(2,0):'C',(0,1):'D',(1,1):'E',(2,1):'F',(0,2):'G',(1,2):'H',(2,2):'I'
    }
    wonSects.clear()
    wonSects = {v:'' for k,v in secDict.items()}
    wonSects.update({'':''})
    sectNums = 'xABCDEFGHI'#added the x so i could think/type the corresponding numbers the same way i think of them
    boxVal = {}# empty boxes
    coords = {}# clear coordinates so it doesn't just add on starting from I
    window.fill(bgColor)
    tttInit()
    turn = 1# reset to X's turn

tttInit() #initialize tictactoe
print(len(coords))# should always print 81 meaning there are 81 boxes/coords (9*9)

while True: #game loop
    cur = pg.mouse.get_pos()
    click = pg.mouse.get_pressed()#when mouse is clicked
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()
        if event.type == pg.MOUSEBUTTONDOWN:
            mouseSq = cur[0]//sqW*100, cur[1]//sqH*100
            match = next((k for (k, v) in coords.items() if v == mouseSq), None)#match the coordinates to a (small) box
            print(match)
            placeMark(coords[match],match)
            valHighlight(sectNums[int(lastMove[1])])
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_BACKSPACE:
                boardReset()
            if event.unicode == '!':
                try:
                    window.blit(wirat,coords[lastMove])
                except:
                    window.blit(wirat,(0,0))
            if event.key == pg.K_ESCAPE:
                pg.quit()
                exit()
    pg.display.update()
    clock.tick(20) # set fps; 20 looks smooth while not being wholly unnecessary
