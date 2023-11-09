import pygame

WIDTH, HEIGHT = 800, 811

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

icon = pygame.image.load("/Users/shayanmousavi/Documents/Chess Game Pics/chess-icon-512x512-1mnnsw7y.png")

pygame.display.set_caption("Chess - Saleh Version")
pygame.display.set_icon(icon)

background = pygame.image.load("/Users/shayanmousavi/Documents/Chess Game Pics/chessBoard.jpeg").convert()

highlight = pygame.image.load("/Users/shayanmousavi/Documents/Chess Game Pics/highlight.png")

pic = []
#add pics for each piece: 
"""order of pictures: black pawn, black rook, black horse, black bishop, black queen, black king, repeat the same order for white"""
for i in range (12):
    pic.append(pygame.image.load("/Users/shayanmousavi/Documents/Chess Game Pics/chessPieces/pic"+ str(i) + ".png"))

class chessPiece(pygame.sprite.Sprite):
    def __init__(self, xposition, yposition, image, type, colour, types):
        super(chessPiece, self).__init__()
        self.image = image
        self.width = self.image.get_rect()[2]
        self.height = self.image.get_rect()[3]
        self.rect = pygame.Rect(xposition, yposition, self.width, self.height)
        self.type = type
        self.colour = colour
        self.types = types
    def update(self):
        WINDOW.blit(self.image, self.rect)

class square(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.rect = pygame.Rect(x, y, 94, 94)

class mouseRect(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.rect = pygame.Rect(x, y, 3, 3)
    def update(self):
        self.rect.center = pygame.mouse.get_pos()

mouse = mouseRect(1000, 100)

squares = pygame.sprite.Group()

for i in range(8):
    for j in range(8):
        squares.add(square(25+(94*i), 29.8 + (94.4*j)))
        


pieces = pygame.sprite.RenderPlain()

whitePieces = pygame.sprite.Group()
blackPieces = pygame.sprite.Group()
#add in black pawns, then rook, horse, bishop, queen, king
for i in range(32):
    if(i < 8):
        pieces.add(chessPiece(35+94*(i), 123, pic[0], "Pawn", "Black", "P"))
    elif(i == 8 or i == 9):
        pieces.add(chessPiece((35+(7*94)*(i-8)), 34, pic[1], "Rook", "Black", "R"))
    elif(i == 10 or i == 11):
        pieces.add(chessPiece((129+(5*94)*(i-10)), 33, pic[2], "Knight", "Black", "N"))
    elif(i == 12 or i == 13):
        pieces.add(chessPiece((223+(3*94)*(i-12)), 39, pic[3], "Bishop", "Black", "B"))
    elif(i == 14 or i == 15):
        inputType = "Queen"
        inputTypes = "Q"
        if (i == 15):
            inputType = "King"
            inputTypes = "K"
        pieces.add(chessPiece((317+(94)*(i-14)), 47 - ((i-14)*6), pic[4 + i-14], inputType, "Black", inputTypes))
    elif(i > 15 and i < 24):
        pieces.add(chessPiece(35+94*(i-16), 597, pic[6], "Pawn", "White", "p"))
    elif(i == 24 or i == 25):
        pieces.add(chessPiece((35+(7*94)*(i-24)), 694, pic[7], "Rook", "White", "r"))
    elif(i == 26 or i == 27):
        pieces.add(chessPiece((129+(5*94)*(i-26)), 695, pic[8], "Knight", "White", "n"))
    elif(i == 28 or i == 29):
        pieces.add(chessPiece((223+(3*94)*(i-28)), 701, pic[9], "Bishop", "White", "b"))
    elif(i == 30 or i == 31):
        inputType = "Queen"
        inputTypes = "q"
        if (i == 31):
            inputType = "King"
            inputTypes = "k"
        pieces.add(chessPiece((317+(94)*(i-30)), 705 - ((i-30)*6), pic[10 + i-30], inputType, "White", inputTypes))
target = chessPiece(1000, 1000, highlight, None, None, None)

for i in pieces:
    if i.colour == "Black":
        blackPieces.add(i)
    else:
        whitePieces.add(i)

positions = dict()


rows = 8
columns = 1
boxes = 1

#create a dictionary holding the rect objects indexed for each square from A1 to G7
for i in squares:
    if((boxes-1) % 8 == 0 and (boxes-1) != 0):
        columns += 1
        rows = 8
    index = chr(ord("A")+ columns-1)+ str(rows)
    positions[index] = i
    rows -= 1
    boxes += 1

def positionToFen(square):
    for i in positions.keys():
        if (positions[i].rect.center == square.rect.center):
            return i

def drawWindow(): 
    WINDOW.fill((255,255,255))
    WINDOW.blit(background,(0,0))
    pieces.draw(WINDOW)
    WINDOW.blit(highlight, target.rect)
    pygame.display.update()



def checkHorse(oRow, oCol, nRow, nCol):
    changeRow = int(abs(nRow - oRow))
    changeCol = int(abs(nCol - oCol))
    if((changeRow == 2 and changeCol == 1) or (changeCol == 2 and changeRow == 1)):
        return True
    else:
        return False

def checkPath(oRow, oCol, nRow, nCol):
    if(oRow == nRow):
        deltaCol = int((nCol - oCol)/(abs(nCol - oCol)))
        currentPosition = chr(ord('A') + oCol+deltaCol)+ str(oRow)
        for i in range(abs(nCol-oCol)-1):
            if(pygame.sprite.spritecollideany(positions[currentPosition], pieces) != None):
                return False
            currentPosition = chr(ord("A") + oCol+ (i+1)*deltaCol)+ str(oRow)
    elif(oCol == nCol):
        deltaRow = int((nRow - oRow)/(abs(nRow - oRow)))
        currentPosition = chr(ord('A') + oCol)+ str(oRow+deltaRow)
        for i in range(abs(nRow-oRow)-1):
            if(pygame.sprite.spritecollideany(positions[currentPosition], pieces) != None):
                return False
            currentPosition = chr(ord('A') + oCol)+ str(oRow+(i+1)*(deltaRow))
    elif(abs(nCol - oCol) == abs(nRow-oRow)):
        deltaRow = int((nRow-oRow)/abs(nRow-oRow))
        deltaCol = int((nCol-oCol)/abs(nCol-oCol))
        currentPosition = chr(ord('A') + oCol+ deltaCol)+ str(oRow+deltaRow)
        for i in range(abs(nRow-oRow)-1):
            if(pygame.sprite.spritecollideany(positions[currentPosition], pieces) != None):
                return False
            currentPosition = chr(ord('A') + oCol + ((1+i)*deltaCol))+ str(oRow + ((1+i)*deltaRow))
    return True


def checkLegal(piece, currentPlace, newPlace, spots, colour, enemies):
    currentCoord = "  "
    newCoord = "  "
    killed = False
    for m in spots:
        if spots[m].rect.center == currentPlace.rect.center:
            currentCoord = m
        elif spots[m].rect.center == newPlace.rect.center:
            newCoord = m
    enemy = pygame.sprite.spritecollideany(newPlace, enemies)
    if (enemy):
        killed = True

    currentRow = int(currentCoord[1])
    newRow = int(newCoord[1])
    currentCol = ord(currentCoord[0])-ord('A')
    newCol = ord(newCoord[0])-ord('A')
    if(piece.type == "Pawn" and newCol == currentCol and ((piece.colour == "White" and newRow - currentRow == 1) or (piece.colour == "Black" and newRow - currentRow == -1))):
        return True
    elif(piece.type == "Pawn" and piece.colour == "Black" and currentRow == 7 and currentCol == newCol and abs(currentRow - newRow) == 2 and checkPath(currentRow, currentCol, newRow, newCol)):
        return True
    elif(piece.type == "Pawn" and piece.colour == "White" and currentRow == 2 and currentCol == newCol and abs(currentRow - newRow) == 2 and checkPath(currentRow, currentCol, newRow, newCol)):
        return True
    elif(piece.type == "Pawn" and piece.colour == "White" and killed and (newRow-currentRow) == abs(newCol - currentCol) and (abs(newCol-currentCol) == 1)):
        return True
    elif(piece.type == "Pawn" and piece.colour == "Black" and killed and ((-1)*(newRow-currentRow) == abs(newCol - currentCol)) and (abs(newCol-currentCol) == 1)):
        return True
    elif(piece.type == "Rook" and (currentRow == newRow or currentCol == newCol) and checkPath(currentRow, currentCol, newRow, newCol)):
        return True
    elif(piece.type == "Knight" and checkHorse(currentRow, currentCol, newRow, newCol)):
        return True
    elif(piece.type == "Bishop" and (abs(newCol - currentCol) == abs(newRow - currentRow)) and checkPath(currentRow, currentCol, newRow, newCol)):
        return True
    elif(piece.type == "Queen" and ((abs(newCol - currentCol) == (abs(newRow - currentRow))) or newRow == currentRow or newCol == currentCol) and checkPath(currentRow, currentCol, newRow, newCol)):
        return True
    elif(piece.type == "King" and (abs(newCol-currentCol) <= 1) and (abs(newRow - currentRow) <= 1) and ((abs(newCol - currentCol) == abs(newRow - currentRow)) or newRow == currentRow or newCol == currentCol)):
        return True
    else:
        return False

clicked = False
movePiece = pygame.sprite.Sprite()
turn = 0

board = dict()

def getPositions():
    global board
    for i in range(8):
        for j in range(8):
            key = chr(ord("A") + j) + str(8-i)
            currentPiece = pygame.sprite.spritecollideany(positions[key], pieces)
            if(currentPiece and currentPiece.colour == "White" and currentPiece.type != "Knight"):
                board[key] = currentPiece.type[0].lower()
            elif(currentPiece and currentPiece.colour == "White"):
                board[key] = "n"
            elif(currentPiece and currentPiece.colour == "Black" and currentPiece.type != "Knight"):
                board[key] = currentPiece.type[0]
            elif(currentPiece and currentPiece.colour == "Black"):
                board[key] = "N"
            else:
                board[key] = "-"
            print(board[key], end = " ")
        print(end = "\n")

def checkValidPosition(position):
    if(type(position) != str):
        return False
    elif(ord("A") <= ord(position[0]) and ord("H") >= ord(position[0]) and len(position) < 3 and (int(position[1])) > 0 and (int(position[1])) < 9):
        return True
    else: 
        return False

def checkDirection(dir, startPosition, limit, gameBoard):
    directionCovered = list()
    #check downwards
    m = 0
    if(dir == 0):
        square = chr(ord(startPosition[0])) + str(int(startPosition[1])-1)
        while(checkValidPosition(square) and m < limit):
            directionCovered.append(square)
            m += 1
            if(gameBoard[square] != "-"):
                m = limit
            square = chr(ord(startPosition[0])) + str(int(startPosition[1])-1-m)
    #to the right
    elif(dir == 1):
        square = chr(ord(startPosition[0])+1) + str(int(startPosition[1]))
        while(checkValidPosition(square) and m < limit):
            directionCovered.append(square)
            m += 1
            if(gameBoard[square] != "-"):
                m = limit
            square = chr(ord(startPosition[0])+1+m) + str(int(startPosition[1]))
    #upwards
    elif(dir == 2):
        square = chr(ord(startPosition[0])) + str(int(startPosition[1])+1)
        while(checkValidPosition(square) and m < limit):
            directionCovered.append(square)
            m += 1
            if(gameBoard[square] != "-"):
                m = limit
            square = chr(ord(startPosition[0])) + str(int(startPosition[1])+1+m)
    #to the left
    elif(dir == 3):
        square = chr(ord(startPosition[0])-1) + str(int(startPosition[1]))
        while(checkValidPosition(square) and m < limit):
            directionCovered.append(square)
            m += 1
            if(gameBoard[square] != "-"):
                m = limit
            square = chr(ord(startPosition[0])-1-m) + str(int(startPosition[1]))
    #to the down and right:
    elif(dir == 4):
        square = chr(ord(startPosition[0])+1) + str(int(startPosition[1])-1)
        while(checkValidPosition(square) and m < limit):
            directionCovered.append(square)
            m += 1
            if(gameBoard[square] != "-"):
                m = limit
            square = chr(ord(startPosition[0])+1+m) + str(int(startPosition[1])-1-m)
    #to the down and left:
    elif(dir == 5):
        square = chr(ord(startPosition[0])-1) + str(int(startPosition[1])-1)
        while(checkValidPosition(square) and m < limit):
            directionCovered.append(square)
            m += 1
            if(gameBoard[square] != "-"):
                m = limit
            square = chr(ord(startPosition[0])-1-m) + str(int(startPosition[1])-1-m)
    #to the up and right
    elif(dir == 6):
        square = chr(ord(startPosition[0])+1) + str(int(startPosition[1])+1)
        while(checkValidPosition(square) and m < limit):
            directionCovered.append(square)
            m += 1
            if(gameBoard[square] != "-"):
                m = limit
            square = chr(ord(startPosition[0])+1+m) + str(int(startPosition[1])+1+m)
    #to the up and left
    elif(dir == 7):
        square = chr(ord(startPosition[0])-1) + str(int(startPosition[1])+1)
        while(checkValidPosition(square) and m < limit):
            directionCovered.append(square)
            m += 1
            if(gameBoard[square] != "-"):
                m = limit
            square = chr(ord(startPosition[0])-1-m) + str(int(startPosition[1])+1+m)
    elif(dir == 8):
        for s in range(2):
            for j in range(2):
                for l in range(2):
                    y = ((1*(1-s))+1)*pow(-1,j)
                    x = (1*(s)+1)*pow(-1,l)
                    square = chr(ord(startPosition[0])+x)+str(int(startPosition[1])+y)
                    if(checkValidPosition(square)):
                        directionCovered.append(square)
    return directionCovered
#gets list of hittable squares
def getSquaresCovered(Piece, position, gameBoard):
    listCovered = list()
    if (Piece == "P"):
        square = chr(ord(position[0]) + 1) + str(int(position[1])-1)
        if(checkValidPosition(square)):
            listCovered.append(square)
        square = chr(ord(position[0]) - 1) + str(int(position[1])-1)
        if(checkValidPosition(square)):
            listCovered.append(square)
    elif(Piece == "p"):
        square = chr(ord(position[0]) + 1) + str(int(position[1])+1)
        if(checkValidPosition(square)):
            listCovered.append(square)
        square = chr(ord(position[0]) - 1) + str(int(position[1])+1)
        if(checkValidPosition(square)):
            listCovered.append(square)
    elif(Piece == "r" or Piece == "R"):
        for i in range (4):
            listCovered.extend(checkDirection(i, position, 7, gameBoard))
    elif(Piece == "b" or Piece == "B"):
        for i in range(4):
            listCovered.extend(checkDirection(i+4, position, 7, gameBoard))
    elif(Piece == "n" or Piece == "N"):
        listCovered.extend(checkDirection(8, position, 7, gameBoard))
    elif(Piece == "q" or Piece == "Q"):
        for i in range(8):
            listCovered.extend(checkDirection(i,position, 7, gameBoard))
    elif(Piece == "K" or Piece == "k"):
        for i in range(8):
            listCovered.extend(checkDirection(i,position, 1, gameBoard))   
    return listCovered  

def getCovered(colour, gameBoard):    
    listOfCovered = list()
    for i in range(8):
        for j in range(8):
            key = chr(ord("A") + j) + str(i+1)
            if(colour == "Black" and ord("A") < ord(board[key]) and ord("Z") > ord(board[key])):
                listOfCovered.extend(getSquaresCovered(board[key], key, gameBoard))
            elif(colour == "White" and ord("a") < ord(board[key]) and ord("z") > ord(board[key])):
                listOfCovered.extend(getSquaresCovered(board[key], key, gameBoard))
    return listOfCovered

def getMovesInDir(dir, startPosition, limit, gameBoard):
    directionCovered = list()

    #check downwards
    m = 0
    if(dir == 0):
        square = chr(ord(startPosition[0])) + str(int(startPosition[1])-1)
        while(checkValidPosition(square) and m < limit and gameBoard[square] == "-"):
            directionCovered.append(square)
            m += 1
            square = chr(ord(startPosition[0])) + str(int(startPosition[1])-1-m)
    #to the right
    elif(dir == 1):
        square = chr(ord(startPosition[0])+1) + str(int(startPosition[1]))
        while(checkValidPosition(square) and m < limit and gameBoard[square] == "-"):
            directionCovered.append(square)
            m += 1
            square = chr(ord(startPosition[0])+1+m) + str(int(startPosition[1]))
    #upwards
    elif(dir == 2):
        square = chr(ord(startPosition[0])) + str(int(startPosition[1])+1)
        while(checkValidPosition(square) and m < limit and gameBoard[square] == "-"):
            directionCovered.append(square)
            m += 1
            square = chr(ord(startPosition[0])) + str(int(startPosition[1])+1+m)
    #to the left
    elif(dir == 3):
        square = chr(ord(startPosition[0])-1) + str(int(startPosition[1]))
        while(checkValidPosition(square) and m < limit and gameBoard[square] == "-"):
            directionCovered.append(square)
            m += 1
            square = chr(ord(startPosition[0])-1-m) + str(int(startPosition[1]))
    #to the down and right:
    elif(dir == 4):
        square = chr(ord(startPosition[0])+1) + str(int(startPosition[1])-1)
        while(checkValidPosition(square) and m < limit and gameBoard[square] == "-"):
            directionCovered.append(square)
            m += 1
            square = chr(ord(startPosition[0])+1+m) + str(int(startPosition[1])-1-m)
    #to the down and left:
    elif(dir == 5):
        square = chr(ord(startPosition[0])-1) + str(int(startPosition[1])-1)
        while(checkValidPosition(square) and m < limit and gameBoard[square] == "-"):
            directionCovered.append(square)
            m += 1
            square = chr(ord(startPosition[0])-1-m) + str(int(startPosition[1])-1-m)
    #to the up and right
    elif(dir == 6):
        square = chr(ord(startPosition[0])+1) + str(int(startPosition[1])+1)
        while(checkValidPosition(square) and m < limit and gameBoard[square] == "-"):
            directionCovered.append(square)
            m += 1
            square = chr(ord(startPosition[0])+1+m) + str(int(startPosition[1])+1+m)
    #to the up and left
    elif(dir == 7):
        square = chr(ord(startPosition[0])-1) + str(int(startPosition[1])+1)
        while(checkValidPosition(square) and m < limit and gameBoard[square] == "-"):
            directionCovered.append(square)
            m += 1
            square = chr(ord(startPosition[0])-1-m) + str(int(startPosition[1])+1+m)
    elif(dir == 8):
        for s in range(2):
            for j in range(2):
                for l in range(2):
                    y = ((1*(1-s))+1)*pow(-1,j)
                    x = (1*(s)+1)*pow(-1,l)
                    square = chr(ord(startPosition[0])+x)+str(int(startPosition[1])+y)
                    if(checkValidPosition(square) and gameBoard[square] == "-"):
                        directionCovered.append(square)
    print(dir, directionCovered)
    return directionCovered

def getMovesForPiece(Piece, position, gameBoard):
    listMoves = list()
    if(Piece == "K" or "k"):
        for t in range(8):
            listMoves.append(getMovesInDir(t, position, 1, gameBoard))
    elif(Piece == "P"):
        square = chr(ord(position[0])) + str(int(position[1])-1)
        if(checkValidPosition(square)):
            listMoves.append(square)
        square = chr(ord(position[0])) + str(int(position[1])-2)
        if(checkValidPosition(square) and position[1] == "7"):
            listMoves.append(square)
    elif(Piece == "p"):
        square = chr(ord(position[0])) + str(int(position[1])+1)
        if(checkValidPosition(square)):
            listMoves.append(square)
        square = chr(ord(position[0])) + str(int(position[1])+2)
        if(checkValidPosition(square) and position[1] == "2"):
            listMoves.append(square)
    return listMoves

def checkMate(colour, gameBoard):
    trapped = True
    if(colour == "Black"):
        for i in range(8):
            for j in range(8):
                key = chr(ord("A") + j) + str(i+1)
                if(gameBoard[key] == "K"):
                    kingPos = key
                    kingTerritory = getMovesForPiece(gameBoard[key], key, gameBoard)
                    kingHitBox = getSquaresCovered(gameBoard[key], key, gameBoard)
                    gameBoard[kingPos] = "-"
        otherColour = "White"
        enemyCovered = getCovered(otherColour, gameBoard)
        gameBoard[kingPos] = "K"
        ownCovered = getCovered("Black", gameBoard)
        enemies = ["r", "n", "b", "q", "k", "p"]
    else:
        for i in range(8):
            for j in range(8):
                key = chr(ord("A") + j) + str(i+1)
                if(gameBoard[key] == "k"):
                    kingPos = key
                    kingTerritory = getMovesForPiece(gameBoard[key], key, gameBoard)
                    kingHitBox = getSquaresCovered(gameBoard[key], key, gameBoard)
                    gameBoard[kingPos] = "-"
        otherColour = "Black"
        enemyCovered = getCovered("Black", gameBoard)
        gameBoard[kingPos] = "k"
        ownCovered = getCovered("White", gameBoard)
        enemies = ["R", "N", "B", "Q", "K", "P"]
    print(kingTerritory)
    print(enemyCovered)
    print(ownCovered)
    for t in kingTerritory:
        print(t in enemyCovered, t)
        if(type(t) == str):
            ownCovered.remove(t)
        if(checkValidPosition(t) and not(enemyCovered.count(t))):
            print("can escape")
            trapped = False
    for t in ownCovered:
        #check if you can kill it 
        if(checkValidPosition(t)  and gameBoard[t] in enemies and kingPos in getSquaresCovered(gameBoard[t], t, gameBoard)):
            num = enemyCovered.count(kingPos)
            if(num == 1):
                print("can Kill")
                trapped = False
        #check if you can block
        elif(checkValidPosition(t) and gameBoard[t] == "-" and t in enemyCovered) :
            gameBoard[t] = "f"
            num = enemyCovered.count(kingPos)
            newEnemyCovered = getCovered(otherColour, gameBoard)
            if(not kingPos in newEnemyCovered and num == 1):
                print("can block")
                print(gameBoard)
                trapped = False
            gameBoard[t] = "-"
    for t in kingHitBox:
        if(checkValidPosition(t) and gameBoard[t] in enemies and kingPos in getSquaresCovered(gameBoard[t], t, gameBoard) and not t in enemyCovered):
            num = enemyCovered.count(kingPos)
            if(num == 1):
                print(gameBoard[t])
                print("king can Kill")
                trapped = False
    if(kingPos in enemyCovered and trapped):
        return 1 #checkMate
    elif(kingPos in enemyCovered):
        print("Check")
        print(trapped)
        return -1 #check
    else:
        return 0 #notChecked


def MakeMove(click, clickedBox, colourTurn):
    global clicked
    global pieces
    global movePiece
    global turn

    if(colourTurn == "Black"):
        group = blackPieces
        otherGroup = whitePieces
    else: 
        group = whitePieces
        otherGroup = blackPieces

    if not click and pygame.sprite.spritecollideany(clickedBox, group): 
        target.rect.center = clickedBox.rect.center
        clicked = True
        movePiece = pygame.sprite.spritecollideany(clickedBox, pieces)
    elif click and not pygame.sprite.spritecollideany(clickedBox, group) and checkLegal(movePiece, target, clickedBox, positions, colourTurn, otherGroup):
        oldPos = positionToFen(target)
        newPos = positionToFen(clickedBox)
        tempBoard = board
        tempBoard[oldPos] = "-"
        tempBoard[newPos] = movePiece.types
        print(tempBoard)
        num = checkMate(colourTurn, tempBoard)
        if(num == 0):
            occupiedPiece = pygame.sprite.spritecollideany(clickedBox, otherGroup)
            if(occupiedPiece):
                occupiedPiece.kill()
            movePiece.rect.center = clickedBox.rect.center
            target.rect.center = (1000, 1000)
            clicked = False
            turn += 1
        else: 
            return

def main():
    running = True
    global movePiece
    global clicked
    while running: 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                getPositions()
                mouse.update()
                collision = pygame.sprite.spritecollideany(mouse,squares)
                if(collision != None and turn % 2 == 0):
                    MakeMove(clicked, collision, "Black")
                    if(checkMate("White", board) == 1):
                        print("CheckMate, Black wins!")
                elif(collision != None): 
                    MakeMove(clicked, collision, "White")
                    if(checkMate("Black", board) == 1):
                        print("CheckMate, White wins!")
                        running = False
            elif (event.type == pygame.KEYDOWN):
                keys=pygame.key.get_pressed()
                if keys[pygame.K_SPACE]:
                    movePiece = None
                    target.rect.center = (1000, 1000)
                    clicked = False                 
        drawWindow()
        
if __name__ == "__main__":
    main()