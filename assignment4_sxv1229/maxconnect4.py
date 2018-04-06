import MaxConnect4Game as M
import time
import maxconnect4 as m
import sys

# AI Action. Referred Professor's Given Code
class AIPlay:
    def __init__(self):
        initialgameBoard = M.MaxConnect4Game()
        depth_limit = 0

    # Setting up the Initial State, StateBoard
    def initState(self,inputFile, gameMode,nextPlayer):
        self.initialgameBoard = M.MaxConnect4Game()
        self.initialgameBoard.setBoard(inputFile,gameMode,nextPlayer)
        self.initialgameBoard.printGameBoard()
        return self.initialgameBoard

  # The Successors generation
    def gettingSuccessors(self,gameboard):
        Matrix = {}
        numCol = gameboard.numberofPossibleColumns()
        for c in range(len(numCol)):
	    movement = numCol.pop()
            isValid, newGameBoard = gameboard.playPiece(movement)
            Matrix[movement] = newGameBoard
        return Matrix

    # Getting Minvalue based on Utility Value for minmax function # Coded based on Sir's material and class psuedo code
    def miniValue(self, currentGameboard, alpha, beta, depth):
        v = float(1000000)
        count = currentGameboard.checkpieceCount()
        if count == 42:
            utility = currentGameboard.utility()
            return utility
        if depth == self.depth_limit:
            score = currentGameboard.evaluation()
            return score
        else:
            depth = depth + 1
            Matrix = self.gettingSuccessors(currentGameboard)
            for key in Matrix.iterkeys():
                board = Matrix[key]
                temp = self.maxiValue(board, alpha, beta, depth)
                if temp <= v:
                    v = temp
                    movement = key
                if v <= alpha:
                    return v
                beta = min(beta, v)
            return v

    # Getting maxvalue based on Utility Value for minmax function
    def maxiValue(self, currentGameboard, alpha, beta, depth):
        v = float(-1000000)
        count = currentGameboard.checkpieceCount()
        if count == 42:
            utility = currentGameboard.utility()
            return utility
        elif depth == self.depth_limit:
            score = currentGameboard.evaluation()
            return score
        else:
            depth = depth + 1
            Matrix = self.gettingSuccessors(currentGameboard)
            for key in Matrix.iterkeys():
                board = Matrix[key]
                temp = self.miniValue(board, alpha, beta, depth)
                if temp >= v:
                    v = temp
                    movement = key
                if v >= beta:
                    return v
                alpha = max(alpha, v)
            return v


    # minmax Algorithm to decide what the current player picks
    def minmax(self, initialgameBoard):
        score = 0
        movement = -1
        startTime = time.time()
        Matrix = self.gettingSuccessors(initialgameBoard)
        v = float(-100000)
        # for i in range(0,6,1):
        #     if self.checkpieceCount(i) != None:
        #         #print self.initialgameBoard
        #         if self.pieceCount == 42:
        #             self.initialgameBoard = copy.deepcopy(currentGameboard)
        #             return i
        for key in Matrix.iterkeys():
            temp = self.miniValue(Matrix[key],alpha = -1000000, beta = 1000000, depth = 1)  #return min (utility)

            if temp >= v:
                v = temp
                movement = key
        endTime = time.time()
        print 'TIME :' , (endTime-startTime)
        isvalid, demo = initialgameBoard.playPiece(movement)
        return demo, movement, v

def main(argv):
    nextPlayer = ''
    inputFile = ''
    outputFile = ''
    gameMode = argv[1]

    # Checking all the args are present if not print error messages
    if len(argv) != 5:
        print 'All Four Command Line Arguments are required'
        print('Usage: %s interactive [inputFile] [computer-next/human-next] [depth]' % argv[0])
        print('or: %s one-move [inputFile] [outputFile] [depth]' % argv[0])
        sys.exit(2)

    gameMode, infile = argv[1:3]

    # Checking which is the Game Mode whether it is interactive or one-move othe than its invalid
    if not gameMode == 'interactive' and not gameMode == 'one-move':
        print('%s is an unrecognized/ Invalid game mode' %gameMode)
        sys.exit(2)

    # If Game Mode is interactive
    if gameMode == 'interactive':
        inputFile = argv[2]
        nextPlayer = argv[3]
        initnextplayer = nextPlayer
        player = m.AIPlay()
        player.depth_limit = int(argv[4])
        initstate = player.initState(inputFile,gameMode,nextPlayer)
        # Checking all possibilities
        while True:
            count = initstate.checkpieceCount()
            if count == 42 and initnextplayer == 'computer-next':
                initstate.countScore()
                print 'Computer Score: ', initstate.player2score
                print 'Player Score: ', initstate.player1score
                initstate.printGameBoard()
                break
            elif count == 42 and initnextplayer == 'human-next':
                initstate.countScore()
                print 'Computer Score: ', initstate.player2score
                print 'Player Score: ', initstate.player1score
                initstate.printGameBoard()
                break
            elif nextPlayer == 'computer-next':
                initstate, movement, score = player.minmax(initstate)
                initstate.countScore()
                print 'Computer Score: ', initstate.player2score
                print 'Player Score: ', initstate.player1score
                initstate.printGameBoardToFile('computer.txt')
                nextPlayer = 'human-next'
            elif nextPlayer == 'human-next':
                initstate.countScore()
                initstate.printGameBoard()
                print 'Computer Score: ', initstate.player2score
                print 'Player Score: ', initstate.player1score
                print "Enter the column(1-7): "
                humanMovement = int(raw_input())
                # check the human move is <1 or >7 because the column has to be between 1-7
                while humanMovement < 1 or humanMovement > 7:
                    print "The column has to be between 1-7:"
                    humanMovement = int(raw_input())
                isValid, initstate = initstate.playPiece(humanMovement-1)
                while not isValid:
                    print "Enter the column(1-7):"
                    humanMovement = int(raw_input())
                    isValid, initstate = initstate.playPiece(humanMovement-1)
                initstate.printGameBoardToFile('human.txt')
                nextPlayer = 'computer-next'

    # If Game Mode is One - Move
    elif gameMode == 'one-move':
        inputFile = argv[2]
        outputFile = argv[3]
        player  = m.AIPlay()
        player.depth_limit = int(argv[4])
        initstate = player.initState(inputFile,gameMode,nextPlayer)
        temp, movement, score = player.minmax(initstate)
        print 'Movement: Column', movement+1
        print 'Score:', score
        print 'GameBoard After Column', movement+1, 'move:'
        temp.printGameBoard()
        temp.printGameBoardToFile(outputFile)

if __name__ == '__main__':
    main(sys.argv)
