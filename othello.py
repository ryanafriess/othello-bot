import sys; args = sys.argv[1:]

global size

size = 8

def printBoard(board):
    print("\n".join([board[i:i+size] for i in range(0, size*size, size)]))
            

def findDiags(board, pos):
    row = pos // size
    col = pos % size
    amountOfDiagonals = min(row, col)
    startInd = pos - (amountOfDiagonals*(size+1))
    upLeft = board[startInd:pos:size+1]

    amountOfDiagonals = min(size-(col+1), row)
    startInd = pos - (amountOfDiagonals*(size-1))
    upRight = board[startInd:pos:size-1]

    amountOfDiagonals = min(col, size-(row+1))
    endInd = pos + (amountOfDiagonals*(size-1))
    downLeft = board[pos+size-1:endInd+1:size-1]

    amountOfDiagonals = min(size-(col+1), size-(row+1))
    endInd = pos + (amountOfDiagonals*(size+1))
    downRight = board[pos+size+1:endInd+1:size+1]

    return [upLeft[::-1], upRight[::-1], downLeft, downRight]

CACHEP = {}

def possibleMoves(board, tokenToPlay):
    key = (board, tokenToPlay)
    if key in CACHEP:
        #updateStats("CACHEP HIT")
        return CACHEP[key]
    
    possibles = set()
    if tokenToPlay == "x":
        tokenNotToPlay = "o"
    elif tokenToPlay == "X":
        tokenNotToPlay = "O"
    elif tokenToPlay == "O":
        tokenNotToPlay = "X"
    else:
        tokenNotToPlay = "x"
    
    listOfTokenPos = [idx for idx, token in enumerate(board) if token == tokenToPlay]
    for pos in listOfTokenPos:
        posRow = pos // size
        posCol = pos % size
        leftString = board[posRow*size:pos]
        upString = board[posCol:pos:size]
        #print(pos, upString)
        rightString = board[pos+1:posRow*size+size]
        downString = board[pos+size::size]

        listOfStrings = [leftString[::-1], upString[::-1], rightString, downString]
        listOfDiags = findDiags(board, pos)

        listOfStrings += listOfDiags

        #print(pos, listOfStrings)

        for direction, string in enumerate(listOfStrings):
            if "." in string:
                if tokenNotToPlay in string[:string.index(".")] and not tokenToPlay in string[:string.index(".")]:
                    if direction == 0: #left
                        possibles.add(pos-(1+string.index(".")))
                    if direction == 1: #up
                        possibles.add(pos-(size*(1+string.index("."))))
                    if direction == 2: #right
                        possibles.add(pos+(1+string.index(".")))
                    if direction == 3: #down
                        possibles.add(pos+(size*(1+string.index("."))))
                    if direction == 4: #leftUP
                        possibles.add(pos-((size+1)*(1+string.index("."))))
                    if direction == 5: #rightUP
                        possibles.add(pos-((size-1)*(1+string.index("."))))
                    if direction == 6: #leftDown
                        possibles.add(pos+((size-1)*(1+string.index("."))))
                    if direction == 7: #rightDown
                        possibles.add(pos+((size+1)*(1+string.index("."))))

    possibles = {idx for idx in possibles if idx >= 0}
                
    if possibles: 
        CACHEP[key] = [*possibles]
        #updateStats("CACHENOTUSED")
        return [*possibles]
    else:
        CACHEP[key] = [-1]
        #updateStats("CACHENOTUSED")
        return [-1]

def getMove(move):
    #print(move)
    if move[:1].upper() in "ABCDEFGH":
        col = "ABCDEFGH".index(move[:1].upper())
        row = int(move[1:])
        return (size*(row-1)) + col
    else:
        return int(move)

    
def makeMove(board, tokenToPlay, pos):
    board = board.lower()
    board = [*board]
    board[pos] = tokenToPlay
    
    if tokenToPlay == "x":
        tokenNotToPlay = "o"
    elif tokenToPlay == "X":
        tokenNotToPlay = "O"
    elif tokenToPlay == "O":
        tokenNotToPlay = "X"
    else:
        tokenNotToPlay = "x"

    # print(tokenToPlay, tokenNotToPlay)

    posRow = pos // size
    posCol = pos % size
    leftString = board[posRow*size:pos]
    upString = board[posCol:pos:size]
    rightString = board[pos+1:posRow*size+size]
    downString = board[pos+size::size]

    listOfStrings = [leftString[::-1], upString[::-1], rightString, downString]
    listOfDiags = findDiags(board, pos)

    listOfStrings += listOfDiags

    #print(listOfStrings)
    for direction, string in enumerate(listOfStrings):
        #print(direction, string)
        if tokenToPlay in string:
                xInd = string.index(tokenToPlay)
                if tokenNotToPlay in string[:string.index(tokenToPlay)] and not tokenToPlay in string[:string.index(tokenToPlay)] and not "." in string[:string.index(tokenToPlay)]:
                    #print(xInd, direction)
                    if direction == 0: #left
                        startInd = pos - (xInd+1)
                        endInd = pos
                        for idx in range(startInd, endInd):
                            board[idx] = tokenToPlay
                    if direction == 1: #up
                        startInd = pos-(size)
                        endInd = pos-(size*xInd)
                        #print("up", startInd, endInd)
                        for idx in range(startInd, endInd-1, -size):
                            board[idx] = tokenToPlay
                    if direction == 2: #right
                        startInd = pos+1
                        endInd = pos + xInd + 1
                        for idx in range(startInd, endInd):
                            board[idx] = tokenToPlay
                    if direction == 3: #down
                        startInd = pos+size
                        endInd = pos + (size*xInd) + 1
                        for idx in range(startInd, endInd, size):
                            board[idx] = tokenToPlay 
                    if direction == 4: #leftUP
                        startInd = pos - (xInd*(size+1))
                        endInd = pos
                        for idx in range(startInd, endInd+1, size+1):
                            board[idx] = tokenToPlay
                    if direction == 5: #rightUP
                        startInd = pos - (xInd*(size-1))
                        endInd = pos
                        for idx in range(startInd, endInd+1, size-1):
                            board[idx] = tokenToPlay
                    if direction == 6: #leftDown
                        endInd = pos + (xInd*(size-1))
                        startInd = pos
                        for idx in range(startInd, endInd+1, size-1):
                            board[idx] = tokenToPlay
                    if direction == 7: #rightDown
                        startInd = pos
                        endInd = pos + (xInd*(size+1))
                        for idx in range(startInd, endInd+1, size+1):
                            board[idx] = tokenToPlay
    
    return "".join(board)

            
def ruleOfThumb(board, tokenToPlay):
    possibles = possibleMoves(board, tokenToPlay)
    #print(tokenToPlay, possibles)
    corners = [0, 7, 56, 63]

    for corner in corners:
        if corner in possibles:
            return corner
        if board[corner] == tokenToPlay:
            if corner == 0: #top left
                for pos in range(1, size):
                    rightStr = board[1:pos]
                    if rightStr == tokenToPlay*len(rightStr):
                        if pos in possibles: return pos
                for pos in range(0, size*size, size):
                    downStr = board[8:pos:size]
                    if downStr == tokenToPlay*len(downStr):
                        if pos in possibles: return pos

            if corner == 7: #top right
                for pos in range(7, 0, -1):
                    leftStr = board[pos:0:-1]
                    if leftStr == tokenToPlay*len(leftStr):
                        if pos in possibles: return pos
                for pos in range(7, size*size, size):
                    downStr = board[7:pos:size]
                    if downStr == tokenToPlay*len(downStr):
                        if pos in possibles: return pos

            if corner == 56: #bottom left
                for pos in range(56, 63):
                    rightStr = board[56:pos]
                    if rightStr == tokenToPlay*len(rightStr):
                        if pos in possibles: return pos
                for pos in range(56, 0, -size):
                    upStr = board[56:pos:-size]
                    if upStr == tokenToPlay*len(upStr):
                        if pos in possibles: return pos

            if corner == 63: #bottom right
                for pos in range(56, 63):
                    leftStr = board[62:pos:-1]
                    if leftStr == tokenToPlay*len(leftStr):
                        if pos in possibles: return pos
                for pos in range(63, 0, -size):
                    upStr = board[63:pos:-size]
                    if upStr == tokenToPlay*len(upStr):
                        if pos in possibles: return pos
    
    avoid = [1, 6, 8, 9, 14, 15, 48, 49, 57, 54, 55, 62]

    newPossibles = [pos for pos in possibles if pos not in avoid]
    if newPossibles:
        possibles = newPossibles

    if tokenToPlay == "x":
        tokenToAvoid = "o"
    elif tokenToPlay == "X":
        tokenToAvoid = "O"
    elif tokenToPlay == "o":
        tokenToAvoid = "x"
    else:
        tokenToAvoid = "X"

    
    struct = {pos:len(possibleMoves(makeMove(board, tokenToPlay, pos), tokenToAvoid)) for pos in possibles}
    minPos = -1
    minVal = 1000
    for pos in struct:
        if struct[pos] < minVal:
            minPos = pos
            minVal = struct[pos]

    return minPos

def convertCondensed(transcript):
    moveList = [transcript[i:i+2] for i in range(0, len(transcript)-1, 2)] 
    moveList = [move[1:] if "_" in move else move for move in moveList]
    return moveList

CACHEC = {}
global STATS, HLLIM
STATS = {}

def updateStats(keyPhrase):
    if keyPhrase not in STATS: STATS[keyPhrase] = 1
    else: STATS[keyPhrase] += 1

def negamax(brd, tkn, level=0):

    key = (brd, tkn)
    if key in CACHEC: 
        return CACHEC[key]

    if tkn == "x": eTkn = "o"
    elif tkn == "X": eTkn = "O"
    elif tkn == "o": eTkn  = "x"
    else: eTkn = "X"
    
    possibleMovesTkn = possibleMoves(brd, tkn)

    if possibleMovesTkn == [-1]:
        if possibleMoves(brd, eTkn) == [-1]:
            CACHEC[key] = [brd.count(tkn)-brd.count(eTkn)]
            return CACHEC[key]
        nm = negamax(brd, eTkn, level+1)
        CACHEC[key] = [-nm[0]] + nm[1:] + [-1]
        return CACHEC[key]

      
    bestSoFar = [-65]
    for mv in possibleMovesTkn:
        newBrd = makeMove(brd, tkn, mv)
        nm = negamax(newBrd, eTkn, level+1)
        if -nm[0] > bestSoFar[0]:
            bestSoFar = [-nm[0]] + nm[1:] + [mv]
            if(level == 0): print("Min score:", str(bestSoFar[0])+"; Move sequence:", bestSoFar[1:])
    CACHEC[key] = bestSoFar
    return CACHEC[key]


def alphabeta(brd, tkn, lowerBnd, upperBnd, level=0):

    if tkn == "x": eTkn = "o"
    elif tkn == "X": eTkn = "O"
    elif tkn == "o": eTkn  = "x"
    else: eTkn = "X"
    
    possibleMovesTkn = possibleMoves(brd, tkn)

    if possibleMovesTkn == [-1]:
        if possibleMoves(brd, eTkn) == [-1]:
            return [brd.count(tkn)-brd.count(eTkn)]
        ab = alphabeta(brd, eTkn, -upperBnd, -lowerBnd, level+1)
        return [-ab[0]] + ab[1:] + [-1]
      
    bestSoFar = [lowerBnd-1]
    for mv in orderPossibles(brd, eTkn, possibleMovesTkn):
        newBrd = makeMove(brd, tkn, mv)
        ab = alphabeta(newBrd, eTkn, -upperBnd, -lowerBnd, level+1)
        score = -ab[0]
        if score < lowerBnd: continue
        if score > upperBnd: return [score]
        bestSoFar = [score] + ab[1:] + [mv]
        if level == 0: print("Min score: " + str(bestSoFar[0]) + "; move sequence:", bestSoFar[1:])
        lowerBnd = score+1

    return bestSoFar


global midgameLim, corners

corners = [0, 7, 56, 63]
edges = set([i for i in range(64) if i % 8 == 0] + [i for i in range(64) if i % 8 == 7] + [i for i in range(64) if i // 8 == 0] + [i for i in range(64) if i // 8 == 7])
nextToTL = [1, 8, 9]
nextToTR = [6, 14, 15]
nextToBL = [48, 49, 57]
nextToBR = [54, 55, 62]

midgameLim = 5

def checkAvoidCorners(brd, idxToCheck, eTkn):
    avoidCornersCt = 0
    if idxToCheck in nextToTL and brd[0] == eTkn:
        avoidCornersCt += 1
    if idxToCheck in nextToTR and brd[7] == eTkn:
        avoidCornersCt += 1
    if idxToCheck in nextToBL and brd[56] == eTkn:
        avoidCornersCt += 1
    if idxToCheck in nextToBR and brd[63] == eTkn:
        avoidCornersCt += 1
    return avoidCornersCt


def brdEval(brd, tkn, eTkn):
    cornerCt = 0
    edgeCt = 0
    otherCt = 0
    avoidCornerCt = 0
    for idx, val in enumerate(brd):
        if val == tkn:
            if idx in corners:
                cornerCt += 1
            elif idx in edges:
                edgeCt += 1
            elif checkAvoidCorners(brd, idx, eTkn) > 0:
                avoidCornerCt += 1
            else:
                otherCt += 1
        if val == eTkn:
            if idx in corners:
                cornerCt -= 1
            elif idx in edges:
                edgeCt -= 1
            elif checkAvoidCorners(brd, idx, eTkn) > 0:
                avoidCornerCt -= 1
            else:
                otherCt -= 1
    
    return cornerCt*10 + edgeCt*2 + avoidCornerCt*-2 + otherCt

             
def orderPossibles(brd, eTkn, possibles):
    if possibles == [-1]:
        return possibles
    else:
        corner = []
        edge = []
        other = []
        avoid = []
        for mv in possibles:
            if mv in corners:
                corner += [mv]
            elif mv in edges:
                edge += [mv]
            elif checkAvoidCorners(brd, mv, eTkn) > 0:
                avoid += [mv]
            else:
                other += [mv]
    #print(possibles, corner+edge+other+avoid)
    return corner + edge + other + avoid
            


def alphabeta_midgame(brd, tkn, lowerBnd, upperBnd, level=0):
    
    if tkn == "x": eTkn = "o"
    elif tkn == "X": eTkn = "O"
    elif tkn == "o": eTkn  = "x"
    else: eTkn = "X"

    if level >= midgameLim:
        #print(level, midgameLim)
        return [brdEval(brd, tkn, eTkn)]

    
    possibleMovesTkn = possibleMoves(brd, tkn)

    if possibleMovesTkn == [-1]:
        if possibleMoves(brd, eTkn) == [-1]:
            print("terminal")
            return [brd.count(tkn)-brd.count(eTkn)]
        ab = alphabeta_midgame(brd, eTkn, -upperBnd, -lowerBnd, level+1)
        return [-ab[0]] + ab[1:] + [-1]
      
    bestSoFar = [lowerBnd-1]
    for mv in orderPossibles(brd, eTkn, possibleMovesTkn):
        newBrd = makeMove(brd, tkn, mv)
        ab = alphabeta_midgame(newBrd, eTkn, -upperBnd, -lowerBnd, level+1)
        score = -ab[0]
        if score < lowerBnd: continue
        if score > upperBnd: return [score]
        bestSoFar = [score] + ab[1:] + [mv]
        lowerBnd = score+1

    return bestSoFar

def quickMove(brd, tkn):
    if not brd: global HLLIM; HLLIM = tkn; return
    HLCT = brd.count('.')
    if HLCT <= HLLIM: return alphabeta(brd, tkn, -65, 65)[-1]
    #return alphabeta_midgame(brd, tkn, -650, 650)[-1]
    return ruleOfThumb(brd, tkn)

    #return ruleOfThumb(brd, tkn)

quickMove("", 10)
def main():
    # quickMove("", 7)
    movesList = []
    snapshotFlag = True
    board = "."*27 + "ox......xo" + "."*27
    tokenToPlay = -1
    for arg in args:
        if "HL" in arg and len(arg) > 2:
            quickMove('', int(arg[2:]))
            #print("HL:", holeLimit)
        elif len(arg) == size*size and arg[1] in "xXOo.":
            board = arg
        elif arg in "xXOo": 
            if board.count(arg.lower()) >= board.count(arg):
                tokenToPlay = arg.lower()
            else:
                tokenToPlay = arg
        elif len(arg) > 2:
            #print(arg)
            movesList += convertCondensed(arg)
        elif arg == "v" or arg == "V":
            snapshotFlag = False
        else:
            movesList.append(arg)

    if tokenToPlay == -1:
        xCt = board.count("x") + board.count("X")
        oCt = board.count("o") + board.count("O")
        if (xCt + oCt) % 2 == 0: 
            if board.count("X") > board.count("x"):
                tokenToPlay = "X"
            else:
                tokenToPlay = "x"
        else:
            if board.count("O") > board.count("o"):
                tokenToPlay = "O"
            else:
                tokenToPlay = "o"

    #print(board, tokenToPlay, movesList)
    movesList = [getMove(move) for move in movesList]
    movesList = [move for move in movesList if move >= 0]

    #print(board, movesList, tokenToPlay)
    print(board, " ", str(board.count("x") + board.count("X")) + "/" +  str(board.count("o") + board.count("O")))

    possibles = possibleMoves(board, tokenToPlay)
    boardWithPossiblesShowing = board
    if possibles != [-1]:
        #print(possibles)
        boardList = [*board]
        for possible in possibles:
            boardList[int(possible)] = "*"
        boardWithPossiblesShowing = "".join(boardList)
        #possibles = ", ".join(possibles)
    printBoard(boardWithPossiblesShowing)
    print()
    print(board, " ", str(board.count("x") + board.count("X")) + "/" +  str(board.count("o") + board.count("O")))
    if possibles == [-1]:
        possibles = "No moves possible"
    print("Possible moves for", tokenToPlay+":", possibles)
    if possibles == "No moves possible": #pass
        print(tokenToPlay, "passes")
        print()
        if tokenToPlay == "x":
            tokenToPlay = "o"
        elif tokenToPlay == "X":
            tokenToPlay = "O"
        elif tokenToPlay == "O":
            tokenToPlay = "X"
        else:
            tokenToPlay = "x"

    possibles = possibleMoves(board, tokenToPlay)
    boardWithPossiblesShowing = board
    if possibles != [-1]:
        #print(possibles)
        boardList = [*board]
        for possible in possibles:
            boardList[int(possible)] = "*"
        boardWithPossiblesShowing = "".join(boardList)
        #possibles = ", ".join(possibles)
    printBoard(boardWithPossiblesShowing)
    print()
    print(board, " ", str(board.count("x") + board.count("X")) + "/" +  str(board.count("o") + board.count("O")))
    if possibles == [-1]:
        possibles = "No moves possible"
    print("Possible moves for", tokenToPlay+":", possibles)


    for moveNum, move in enumerate(movesList):
        if(snapshotFlag):
            if moveNum == len(movesList) - 1:
                print()
                print(tokenToPlay, "moves to", move)
                board = makeMove(board, tokenToPlay, move)
                board = [*board]
                board[move] = tokenToPlay.upper()
                board = "".join(board)
                #print(tokenToPlay)
                if tokenToPlay == "x":
                    tokenToPlay = "o"
                elif tokenToPlay == "X":
                    tokenToPlay = "O"
                elif tokenToPlay == "O":
                    tokenToPlay = "X"
                else:
                    tokenToPlay = "x"
                possibles = possibleMoves(board.lower(), tokenToPlay)
                if possibles == [-1]: #pass
                    if tokenToPlay == "x":
                        tokenToPlay = "o"
                    elif tokenToPlay == "X":
                        tokenToPlay = "O"
                    elif tokenToPlay == "O":
                        tokenToPlay = "X"
                    else:
                        tokenToPlay = "x"
                    possibles = possibleMoves(board.lower(), tokenToPlay)
                boardWithPossiblesShowing = board
                if possibles != [-1]:
                    #print(possibles)
                    boardList = [*board]
                    for possible in possibles:
                        boardList[int(possible)] = "*"
                    boardWithPossiblesShowing = "".join(boardList)
                    #possibles = ", ".join(possibles)
                printBoard(boardWithPossiblesShowing)
                print()
                if possibles == [-1]:
                    possibles = "No moves possible"
                print(board, " ", str(board.count("x") + board.count("X")) + "/" +  str(board.count("o") + board.count("O")))
                print("Possible moves for", tokenToPlay+":", possibles)

            else:
                board = makeMove(board, tokenToPlay, move)
                board = [*board]
                board[move] = tokenToPlay.upper()
                board = "".join(board)
                if tokenToPlay == "x":
                    tokenToPlay = "o"
                elif tokenToPlay == "X":
                    tokenToPlay = "O"
                elif tokenToPlay == "O":
                    tokenToPlay = "X"
                else:
                    tokenToPlay = "x"
                possibles = possibleMoves(board.lower(), tokenToPlay)
                if possibles == [-1]: #pass
                    if tokenToPlay == "x":
                        tokenToPlay = "o"
                    elif tokenToPlay == "X":
                        tokenToPlay = "O"
                    elif tokenToPlay == "O":
                        tokenToPlay = "X"
                    else:
                        tokenToPlay = "x"
                    possibles = possibleMoves(board.lower(), tokenToPlay)
                    boardWithPossiblesShowing = board
                    if possibles != [-1]:
                        #print(possibles)
                        boardList = [*board]
                        for possible in possibles:
                            boardList[int(possible)] = "*"
                        boardWithPossiblesShowing = "".join(boardList)
                        #possibles = ", ".join(possibles)
        

        else:
            print()
            print(tokenToPlay, "moves to", move)
            board = makeMove(board, tokenToPlay, move)
            board = [*board]
            board[move] = tokenToPlay.upper()
            board = "".join(board)
            
            #print(tokenToPlay)
            if tokenToPlay == "x":
                tokenToPlay = "o"
            elif tokenToPlay == "X":
                tokenToPlay = "O"
            elif tokenToPlay == "O":
                tokenToPlay = "X"
            else:
                tokenToPlay = "x"
            possibles = possibleMoves(board.lower(), tokenToPlay)
            if possibles == [-1]: #pass
                if tokenToPlay == "x":
                    tokenToPlay = "o"
                elif tokenToPlay == "X":
                    tokenToPlay = "O"
                elif tokenToPlay == "O":
                    tokenToPlay = "X"
                else:
                    tokenToPlay = "x"
                possibles = possibleMoves(board.lower(), tokenToPlay)
            boardWithPossiblesShowing = board
            if possibles != [-1]:
                #print(possibles)
                boardList = [*board]
                for possible in possibles:
                    boardList[int(possible)] = "*"
                boardWithPossiblesShowing = "".join(boardList)
                #possibles = ", ".join(possibles)
            printBoard(boardWithPossiblesShowing)
            print()
            board = board.lower()
            if possibles == [-1]:
                possibles = "No moves possible"
            print(board, " ", str(board.count("x") + board.count("X")) + "/" +  str(board.count("o") + board.count("O")))
            print("Possible moves for", tokenToPlay+":", possibles)
        
    if possibleMoves(board, tokenToPlay) != [-1]:
        myPref = ruleOfThumb(board, tokenToPlay)
        print(f"The preferred move is: {myPref}")

        if(board.count(".") <= HLLIM):
            ab = alphabeta(board, tokenToPlay, -65, 65)
            #print(board, tokenToPlay)
            #ab = (board, tokenToPlay)
            print("Min score: " + str(ab[0]) + "; move sequence:", ab[1:])
        # else:
        #     ab = alphabeta_midgame(board, tokenToPlay, -6500, 6500)
        #     print("Min score midgame: " + str(ab[0]) + "; move sequence:", ab[1:])

    #print(STATS)
            

class Strategy:
    # Uncomment the below flags as needed
    # logging = True
    # uses_10x10_board = True
    # uses_10x10_moves = True

    def best_strategy(self, board, player, best_move, still_running, time_limit):
        move = quickMove(board, player)
        best_move.value = move


if __name__ == '__main__': main()
