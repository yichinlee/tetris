from tkinter import *
import random
import copy
##AndrewID:yichinle
##Section:Q
####################################
# customize these functions
####################################

def init(data):
    gameData = gameDimensions()
    data.rows = gameData[0] #15
    data.cols = gameData[1] #10
    data.cellSize = gameData[2]
    data.margin = gameData[3]
    data.emptyColor = "blue"
    data.board = [([data.emptyColor]* data.cols) for i in range (data.rows)]
    
    # Seven "standard" pieces (tetrominoes)
    data.iPiece = [
        [  True,  True,  True,  True ]
    ]

    data.jPiece = [
        [  True, False, False ],
        [  True,  True,  True ]
    ]

    data.lPiece = [
        [ False, False,  True ],
        [  True,  True,  True ]
    ]

    data.oPiece = [
        [  True,  True ],
        [  True,  True ]
    ]

    data.sPiece = [
        [ False,  True,  True ],
        [  True,  True, False ]
    ]

    data.tPiece = [
        [ False,  True, False ],
        [  True,  True,  True ]
    ]

    data.zPiece = [
        [  True,  True, False ],
        [ False,  True,  True ]
    ]
    
    data.tetrisPieces = [ data.iPiece, data.jPiece, data.lPiece, data.
                            oPiece, data.sPiece, data.tPiece, data.zPiece ]
    data.tetrisPieceColors = [ "red", "yellow", "magenta", "pink", 
                                "cyan", "green", "orange" ]
    
    #for setting new piece position, color, shape
    data.fallingPieceRow = 0
    data.fallingPieceCol = 0
    data.newPieceData = []
    data.isGameOver = 0
    newFallingPiece(data)
    data.fullRow = 0
    data.newBoard=[]
    data.newBoardEmpty = []
    data.score = 0
    
def drawBoard(canvas,data):
    for r in range (data.rows):
        for c in range (data.cols):
            drawCell(canvas,data,r,c,data.board[r][c])

def drawCell(canvas,data,row,col,color):
    x0 = col*data.cellSize + data.margin
    y0 = row*data.cellSize + data.margin
    x1 = x0 + data.cellSize
    y1 = y0 + data.cellSize
    canvas.create_rectangle(x0,y0,x1,y1,fill = color,width = 2)

def mousePressed(event, data):
    pass

def keyPressed(event, data):
    if event.keysym == "Up":
        rotateFallingPiece(data)
    elif event.keysym == "Down":
        moveFallingPiece(data, 1, 0)
    elif event.keysym == "Right":
        moveFallingPiece(data, 0, 1)
    elif event.keysym == "Left":
        moveFallingPiece(data, 0, -1)
    
    # if event.keysym == "space":
    #     newFallingPiece(data)
    if event.keysym == "r":
        init(data)
        
def gameDimensions():
    row = 15
    col = 10
    cellSize = 20
    margin = 25
    return ((row,col,cellSize,margin))
    
#randomly choosing a new piece, setting its color, 
#and positioning it in the middle of the top row    
def newFallingPiece(data):
    if data.isGameOver == 0:
        #randomly choose
        randomIndex = random.randint(0, len(data.tetrisPieces) - 1)
        newPiece = data.tetrisPieces[randomIndex]
        data.fallingPieceRow = 0
        data.fallingPieceCol = (data.cols//2) - (len(newPiece[0]))// 2
        newPieceColor = data.tetrisPieceColors[randomIndex]
        data.newPieceData=[data.fallingPieceRow,data.fallingPieceCol,
                                newPiece,newPieceColor]
    else:
        pass
def timerFired(data):
    if moveFallingPiece(data, +1, 0) == False:
        placeFallingPiece(data)
        newFallingPiece(data)
        
        if fallingPieceIsLegal(data) == True:
            data.isGameOver = 0
        else:
            data.isGameOver = 1
    
#draw the falling piece
def drawFallingPiece(canvas,data):
    startRow = data.newPieceData[0]
    startCol = data.newPieceData[1]
    color = data.newPieceData[3]
    newPiece = data.newPieceData[2]
    for row in range(len(newPiece)):
        for col in range(len(newPiece[0])):
            if newPiece[row][col]==True:
                drawCell(canvas,data,startRow,startCol,color)
            startCol+=1
        startRow+=1
        startCol = data.newPieceData[1]
        
#move the falling piece by drow dcol        
def moveFallingPiece(data,drow,dcol):
    data.newPieceData[0]+=drow
    data.newPieceData[1]+=dcol
    
    if not fallingPieceIsLegal(data):
        data.newPieceData[0]-=drow
        data.newPieceData[1]-=dcol
        return False
    return True

#check whether the piece is out of range or on top of others
def fallingPieceIsLegal(data):
    startRow = data.newPieceData[0]
    startCol = data.newPieceData[1]
    rowRange = len(data.newPieceData[2])
    colRange = len(data.newPieceData[2][0])
    newPiece = data.newPieceData[2]
    
    for r in range(rowRange):
        for c in range(colRange):
            if newPiece[r][c] == True:
                if 0 <= r+startRow<data.rows and 0 <= c+startCol< data.cols:
                    if data.board[r+startRow][c+startCol] == data.emptyColor :
                        continue
                    return False
                return False
    return True

def rotateFallingPiece(data):
    #oldpiece
    oldPiece = data.newPieceData[2]
    oldNumRows = len(oldPiece)
    oldNumCols = len(oldPiece[0])
    oldRow = data.newPieceData[0]
    oldCol = data.newPieceData[1]
 
    #newpiece
    newNumRows = oldNumCols
    newNumCols = oldNumRows
    newRow = oldRow + oldNumRows//2 - newNumRows//2
    newCol = oldCol + oldNumCols//2 - newNumCols//2
    
    #append data into new piece
    newPiece = [([None]* newNumCols)for i in range (newNumRows)]
    for col in range(oldNumCols):
        for row in range(oldNumRows-1,-1,-1):
            newPiece[col][(oldNumRows-1)-row] = oldPiece[row][col]
            
    #update data into init    
    data.fallingPieceRow = newRow
    data.fallingPieceCol = newCol
    data.newPieceData[2] = newPiece
    if not fallingPieceIsLegal(data):
        data.fallingPieceRow = oldRow
        data.fallingPieceCol = oldCol
        data.newPieceData[2] = oldPiece

#replace the original cell
def placeFallingPiece(data):
    fallingPiece = data.newPieceData[2]
    for row in range(len(fallingPiece)):
        for col in range(len(fallingPiece[0])):
            if fallingPiece[row][col] == True:
                data.board[data.newPieceData[0]+row][data.newPieceData[1]+col] \
                = data.newPieceData[3]
    removeFullRows(data)        

#clear the full row and add the score
def removeFullRows(data):
    fullRow=0
    #if moveFallingPiece == False:
    newBoard = []
    for row in data.board:
        if data.emptyColor in row:
            newBoard += [row]
        else:
            fullRow += 1
            data.score +=1
    newBoard = [([data.emptyColor]*data.cols) for i in range (fullRow)] + newBoard

    
    data.board = copy.deepcopy(newBoard)
    
####################################
# use the run function as-is
####################################

def run(width, height):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 500 # milliseconds
    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

def playTetris():
    dataSet = gameDimensions();
    winHeight = dataSet[0]*dataSet[2] + (dataSet[3]*2)
    winWidth = dataSet[1]*dataSet[2] + (dataSet[3]*2)
    run(winWidth,winHeight)
    
def redrawAll(canvas, data):
    
    canvas.create_rectangle(0,0,data.width,data.height,fill = "orange")
    drawBoard(canvas,data)
    drawFallingPiece(canvas,data)
    if data.isGameOver == 1:
        x0 = 0
        y0 = data.margin + data.cellSize
        x1 = data.width
        y1 = y0 + 3*data.cellSize
        canvas.create_rectangle(x0,y0,x1,y1,fill = "black")
        canvas.create_text(data.width/2, data.margin + 2.5*data.cellSize, 
                            text = "GAME OVER",fill = "red",font="Arial 20 bold")
        
    canvas.create_text(data.width/2, data.margin/2, text = "Score: "+ \
    str(data.score), fill = "black",font="Arial 15 bold" )
    
        
playTetris()
   
