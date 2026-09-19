import turtle, random, time
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
#----------FunctionsSetup----------
def createGrid(HalfScreenX,HalfScreenY,SqSize,Gutter,DimensionRow,DimensionCol,showScreenSize):
    global startingX,startingY,ifDead,ifWin,endX,endY,coordinates
    ifDead = False
    ifWin = False
    coordinates = []
    gridSquare.shape(unopenSquare)
    startingX = int(-1*HalfScreenX+Gutter+SqSize/2)
    startingY = int(HalfScreenY-Gutter-showScreenSize-SqSize/2)
    gridSquare.goto(startingX,startingY)
    endX = int(startingX+(DimensionRow*SqSize))
    endY = int(startingY-(DimensionCol*SqSize))
    for x in range(startingX,endX,SqSize):
        temp = []
        for y in range(startingY,endY,-1*SqSize):
            gridSquare.goto(x,y)
            temp.append((x,y))
            gridSquare.stamp()
        coordinates.append(temp)
    myWin.update()
    return
def generateMinemineMap(row,col):
    global dimensionRow,dimensionCol,mineNum
    while True:
        mineMap.clear()
        for i in range(dimensionRow):
            temp = []
            for i in range(dimensionCol):
                temp.append(0)
            mineMap.append(temp)
        for i in range(mineNum):
            CurrMineRow = random.randint(0,dimensionRow-1)
            CurrMineCol = random.randint(0,dimensionCol-1)
            while mineMap[CurrMineRow][CurrMineCol] != 0:
                CurrMineRow = random.randint(0,dimensionRow-1)
                CurrMineCol = random.randint(0,dimensionCol-1)
            mineMap[CurrMineRow][CurrMineCol] = 1
        if mineMap[row][col] == 0:
            blankValue = 0
            for nextX,nextY in directions:
                nebRow,nebCol = row+nextX,col+nextY
                if mineMap[nebRow][nebCol] == 0:
                    blankValue += 1
                else:
                    break
            if blankValue == 8:
                break
    generateValueMap(mineMap)
    return
def generateValueMap(mineMap):
    global dimensionRow,dimensionCol
    valueMap.clear()
    for i in range(dimensionRow):
        temp = []
        for i in range(dimensionCol):
            temp.append(-1)
        valueMap.append(temp)
    for row in range(len(mineMap)):
        for col in range(len(mineMap[i])):
            if mineMap[row][col] == 0:
                valueMap[row][col] = checkNeighbors(row,col,mineMap)
    generateFlagMap()
    return
def generateFlagMap():
    global dimensionRow,dimensionCol,coordinates
    flagMap.clear()
    flagHit.clear()
    alreadyHit.clear()
    for i in range(dimensionRow):
        temp = []
        for i in range(dimensionCol):
            temp.append(0)
        flagMap.append(temp)
def checkNeighbors(row,col,Map):
    global dimensionRow,dimensionCol,coordinates
    count = 0
    for nextX,nextY in directions:
        nebRow,nebCol = row+nextX,col+nextY
        if 0 <= nebRow < dimensionRow and 0 <= nebCol < dimensionCol:
            if Map[nebRow][nebCol] == 1:
                count += 1
    return count
def checkNeighborsBlank(row,col,blankPlace):
    global dimensionRow,dimensionCol
    for nextX,nextY in directions:
        nebRow,nebCol = row+nextX,col+nextY
        if 0 <= nebRow < dimensionRow and 0 <= nebCol < dimensionCol:
            if valueMap[nebRow][nebCol] == 0 and (nebRow,nebCol) not in blankPlace:    
                if (nebRow,nebCol) not in alreadyHit and (nebRow,nebCol) not in flagHit:
                    alreadyHit.append((nebRow,nebCol))
                    blankPlace.append((nebRow,nebCol))
                    checkNeighborsBlank(nebRow,nebCol,blankPlace)
            elif valueMap[nebRow][nebCol] == -1 and flagMap[nebRow][nebCol] == 0:
                hitMine(nebRow,nebCol)
            elif (nebRow,nebCol) in flagHit:
                if mineMap[nebRow][nebCol] != 1:
                    flagWrong(nebRow,nebCol)
            elif valueMap[nebRow][nebCol] > 0 :
                if (nebRow,nebCol) not in alreadyHit:
                    alreadyHit.append((nebRow,nebCol))
                    blankPlace.append((nebRow, nebCol))
    return
def openBlankSpace(blankPlace):
    global coordinates
    for i in blankPlace:
        gridSquare.goto(coordinates[i[0]][i[1]])
        if valueMap[i[0]][i[1]] > 0:
            gridSquare.shape(mineNumber[valueMap[i[0]][i[1]]-1])
            gridSquare.stamp()
        else:
            gridSquare.shape(blankSquare)
            gridSquare.stamp()
    myWin.update()
def hitMine(row,col):
    global coordinates
    gridSquare.goto(coordinates[row][col])
    gridSquare.shape(mineHitSquare)
    gridSquare.stamp()
    isDead(row,col)
    return
def hitBlank(row,col):
    if valueMap[row][col] == 0:
        blankPlace = []
        blankPlace.append((row,col))
        alreadyHit.append((row,col))
        checkNeighborsBlank(row,col,blankPlace)
        openBlankSpace(blankPlace)
    else:
        hitValue(row,col)
def hitValue(row,col):
    global coordinates
    gridSquare.goto(coordinates[row][col])
    gridSquare.shape(mineNumber[valueMap[row][col]-1])
    gridSquare.stamp()
    return
def hitSquare(x,y):
    global offsetWord,ifDead,ifWin,sqSize,blankNum,startingX,startingY
    row,col = whichSquare(x,y)
    if startingX-sqSize/2 <= x <= endX-sqSize/2 and endY+sqSize/2 <= y <= startingY+sqSize/2:
        if len(alreadyHit) == 0:
            generateMinemineMap(row,col)
        if (row,col) not in flagHit and ifDead is False and ifWin is False:
            if (row,col) not in alreadyHit:
                if mineMap[row][col] == 0:
                    hitBlank(row,col)
                else:
                    hitMine(row,col)
                if (row,col) not in alreadyHit:
                    alreadyHit.append((row,col))
            elif valueMap[row][col] > 0:
                count = checkNeighbors(row,col,flagMap)
                if count == valueMap[row][col]:
                    blankPlace = []
                    checkNeighborsBlank(row,col,blankPlace)
                    openBlankSpace(blankPlace)
            if blankNum == len(alreadyHit):
                    isWinCheckAllMine()
    return
def flagSquares(x,y):
    global ifDead,ifWin,coordinates
    row,col = whichSquare(x,y)
    if ifDead is False and ifWin is False:
        if (row,col) not in alreadyHit and (row,col) not in flagHit:
            gridSquare.goto(coordinates[row][col])
            gridSquare.shape(flagSquare)
            gridSquare.stamp()
            flagHit.append((row,col))
            flagMap[row][col] = 1
            calcFlag()
            myWin.update()
        elif flagMap[row][col] == 1:
            gridSquare.goto(coordinates[row][col])
            gridSquare.shape(unopenSquare)
            gridSquare.stamp()
            flagHit.remove((row,col))
            flagMap[row][col] = 0
            calcFlag()
            myWin.update()
def flagWrong(row,col):
    gridSquare.shape(wrongFlag)
    gridSquare.goto(coordinates[row][col])
    gridSquare.stamp()
    return
def isDead(row,col):
    global ifDead,coordinates
    ifDead = True
    faceSquare.shape(sadFace)
    for i in range(len(mineMap)):
        for j in range(len(mineMap[i])):
            if mineMap[i][j] == 1 and (i,j) != (row,col) and (i,j) not in flagHit:
                gridSquare.goto(coordinates[i][j])
                gridSquare.shape(mineSquare)
                gridSquare.stamp()
    myWin.update()
    return
def isWinCheckAllMine():
    global ifWin,coordinates
    ifWin = True
    faceSquare.shape(winFace)
    for i in range(len(mineMap)):
        for j in range(len(mineMap[i])):
            if (i,j) not in alreadyHit and (i,j) not in flagHit:
                if mineMap[i][j] == 1:
                    gridSquare.goto(coordinates[i][j])
                    gridSquare.shape(flagSquare)
                    gridSquare.stamp()
                    flagMap[i][j] = 1
                    flagHit.append((i,j))
    calcFlag()
    myWin.update()
    return
def whichSquare(x,y):
    global coordinates
    indexX = 100
    indexY = 100
    dist = 10000000
    for row in range(len(coordinates)):
        for col in range(len(coordinates[row])):
            currX = coordinates[row][col][0]
            currY = coordinates[row][col][1]
            currDist = ((x-currX)**2+(y-currY)**2)**0.5
            if currDist < dist:
                dist = currDist
                indexX = col
                indexY = row
    return indexY, indexX
def restart(x,y):
    global halfScreen,sqSize,gutter,dimensionRow,dimensionCol,startTime,elapsed
    faceSquare.shape(smileFace)
    timeCounter.clearstamps()
    flagCounter.clearstamps()
    startTime = time.time()
    elapsed = 0
    createGrid(halfScreenX,halfScreenY,sqSize,gutter,dimensionRow,dimensionCol,showScreenSize)
    alreadyHit.clear()
    flagHit.clear()
    calcFlag()
    calcTime()
    return
def calcTime():
    global ifDead,ifWin,startTime,elapsed,chooseMode
    if ifDead is False and ifWin is False:
        if time.time()-startTime >= 1:
            elapsed += 1
            timeList = []
            for i in str(elapsed):
                timeList.append(int(i))
            ones = timeList[-1]
            timeCounter.goto(timeCoordinates[chooseMode][-1])
            timeCounter.shape(BartholomewV[ones])
            timeCounter.stamp()
            if len(timeList) == 2:
                tens = timeList[-2]
                timeCounter.goto(timeCoordinates[chooseMode][-2])
                timeCounter.shape(BartholomewV[tens])
                timeCounter.stamp()
            if len(timeList) == 3:
                hundreds = timeList[-3]
                timeCounter.goto(timeCoordinates[chooseMode][-3])
                timeCounter.shape(BartholomewV[hundreds])
                timeCounter.stamp()
            startTime = time.time()
            myWin.update()
        turtle.ontimer(calcTime, 1000)
    return
def calcFlag():
    global mineNum,chooseMode
    flagCounter.clearstamps()
    flagList = []
    if mineNum-len(flagHit) >= 0:
        for i in str(mineNum-len(flagHit)):
            flagList.append(int(i))
        ones = flagList[-1]
        flagCounter.goto(flagCoordinates[chooseMode][-1])
        flagCounter.shape(BartholomewV[ones])
        flagCounter.stamp()
        if len(flagList) == 2:
            tens = flagList[-2]
            flagCounter.goto(flagCoordinates[chooseMode][-2])
            flagCounter.shape(BartholomewV[tens])
            flagCounter.stamp()
        if len(flagList) == 3:
            hundreds = flagList[-3]
            flagCounter.goto(flagCoordinates[chooseMode][-3])
            flagCounter.shape(BartholomewV[hundreds])
            flagCounter.stamp()
        myWin.update()
    return
def leave():
    myWin.bye()
    return
#----------WindowSetup----------
mode = [(378,475),(630,727),(1134,727)]
chooseMode = input("Choose your mode(enter the number): (0)easy (1)medium (2)hard!")
while True:
    if chooseMode in ("0","1","2"):
        break
    print("Invalid input! Please enter a valid integer between 0 and 2.")
    chooseMode = input("Choose your mode(enter the number): (0)easy (1)medium (2)hard!")
chooseMode = int(chooseMode)
turtle.setup(mode[chooseMode][0],mode[chooseMode][1])
myWin = turtle.Screen()
myWin.title('MineSweeper')
myWin.tracer(0)
#----------VariablesSetup----------
gutter = 27
showScreenSize = 97
dimensionRow = int((mode[chooseMode][0]-2*gutter)/36)
dimensionCol = int((mode[chooseMode][1]-2*gutter-showScreenSize)/36)
halfScreenX = int(mode[chooseMode][0]/2)
halfScreenY = int(mode[chooseMode][1]/2)
useableSpaceX = mode[chooseMode][0]-2*gutter
useableSpaceY = mode[chooseMode][1]-2*gutter
sqSize = 36
turtSize = sqSize / 20
mineNum = round(dimensionRow*dimensionCol/6.4)
blankNum = dimensionRow*dimensionCol-mineNum
ifDead = False
ifWin = False
startTime = time.time()
elapsed = 0
quitFlag = False
#----------ImageSetup----------
mineHitSquare = str(BASE_DIR / "Squares" / "mineHitSquare.gif")
mineSquare = str(BASE_DIR / "Squares" / "mineSquare.gif")
blankSquare = str(BASE_DIR / "Squares" / "blankSquare.gif")
flagSquare = str(BASE_DIR / "Squares" / "flagSquare.gif")
unopenSquare = str(BASE_DIR / "Squares" / "unopenSquare.gif")
wrongFlag = str(BASE_DIR / "Squares" / "wrongFlag.gif")
oneMine = str(BASE_DIR / "mineNumber" / "oneMine.gif")
twoMine = str(BASE_DIR / "mineNumber" / "twoMine.gif")
threeMine = str(BASE_DIR / "mineNumber" / "threeMine.gif")
fourMine = str(BASE_DIR / "mineNumber" / "fourMine.gif")
fiveMine = str(BASE_DIR / "mineNumber" / "fiveMine.gif")
sixMine = str(BASE_DIR / "mineNumber" / "sixMine.gif")
sevenMine = str(BASE_DIR / "mineNumber" / "sevenMine.gif")
eightMine = str(BASE_DIR / "mineNumber" / "eightMine.gif")
smileFace = str(BASE_DIR / "Squares" / "smileFace.gif")
sadFace = str(BASE_DIR / "Squares" / "sadFace.gif")
winFace = str(BASE_DIR / "Squares" / "winFace.gif")
numberZero = str(BASE_DIR / "Bartholomew V" / "numberZero.gif")
numberOne = str(BASE_DIR / "Bartholomew V" / "numberOne.gif")
numberTwo = str(BASE_DIR / "Bartholomew V" / "numberTwo.gif")
numberThree = str(BASE_DIR / "Bartholomew V" / "numberThree.gif")
numberFour = str(BASE_DIR / "Bartholomew V" / "numberFour.gif")
numberFive = str(BASE_DIR / "Bartholomew V" / "numberFive.gif")
numberSix = str(BASE_DIR / "Bartholomew V" / "numberSix.gif")
numberSeven = str(BASE_DIR / "Bartholomew V" / "numberSeven.gif")
numberEight = str(BASE_DIR / "Bartholomew V" / "numberEight.gif")
numberNine = str(BASE_DIR / "Bartholomew V" / "numberNine.gif")
easyBackGround = str(BASE_DIR / "Squares" / "easyBackGround.png")
mediumBackGround = str(BASE_DIR / "Squares" / "mediumBackGround.png")
hardBackGround = str(BASE_DIR / "Squares" / "hardBackGround.png")
myWin.addshape(mineHitSquare)
myWin.addshape(mineSquare)
myWin.addshape(blankSquare)
myWin.addshape(flagSquare)
myWin.addshape(unopenSquare)
myWin.addshape(wrongFlag)
myWin.addshape(oneMine)
myWin.addshape(twoMine)
myWin.addshape(threeMine)
myWin.addshape(fourMine)
myWin.addshape(fiveMine)
myWin.addshape(sixMine)
myWin.addshape(sevenMine)
myWin.addshape(eightMine)
myWin.addshape(smileFace)
myWin.addshape(sadFace)
myWin.addshape(winFace)
myWin.addshape(numberZero)
myWin.addshape(numberOne)
myWin.addshape(numberTwo)
myWin.addshape(numberThree)
myWin.addshape(numberFour)
myWin.addshape(numberFive)
myWin.addshape(numberSix)
myWin.addshape(numberSeven)
myWin.addshape(numberEight)
myWin.addshape(numberNine)
backGround = [easyBackGround,mediumBackGround,hardBackGround]
myWin.bgpic(backGround[chooseMode])
#----------ListSetup----------
coordinates = []
mineMap = []
valueMap = []
flagMap = []
alreadyHit = []
flagHit = []
directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]
mineNumber = [oneMine,twoMine,threeMine,fourMine,fiveMine,sixMine,sevenMine,eightMine]
BartholomewV = [numberZero,numberOne,numberTwo,numberThree,numberFour,numberFive,numberSix,numberSeven,numberEight,numberNine]
timeCoordinates = [[(79,177),(109,177),(139,177)],[(206,303),(235,303),(264,303)],[(457,303),(487,303),(517,303)]]
flagCoordinates = [[(-139,177),(-109,177),(-79,177)],[(-264,303),(-235,303),(-206,303)],[(-517,303),(-487,303),(-457,303)]]
faceCoordinates = [(0,177),(0,303),(0,303)]
#----------TurtleCreation----------
gridSquare = turtle.Turtle()
gridSquare.penup()
gridSquare.speed(0)
gridSquare.hideturtle()
faceSquare = turtle.Turtle()
faceSquare.penup()
faceSquare.shape(smileFace)
faceSquare.goto(faceCoordinates[chooseMode])
timeCounter = turtle.Turtle()
timeCounter.hideturtle()
timeCounter.speed(0)
timeCounter.penup()
flagCounter = turtle.Turtle()
flagCounter.hideturtle()
flagCounter.speed(0)
flagCounter.penup()
calcFlag()
myWin.update()
#----------GameSetup----------
createGrid(halfScreenX,halfScreenY,sqSize,gutter,dimensionRow,dimensionCol,showScreenSize)
#----------EventHandlers----------
myWin.listen()
myWin.onkey(leave,'q')
myWin.onclick(hitSquare)
myWin.onclick(flagSquares,btn=3)
faceSquare.onclick(restart)
myWin.onclick(restart,btn=2)
#----------TimeLoop-------------
calcTime()
#----------TheLastLine----------
myWin.mainloop()