from copy import deepcopy

class MaxConnect4Game:

    def __init__(self):
        self.gameBoard = [[0 for i in range(7)] for j in range(6)]
        self.currentTurn = 1
        self.player1score = 0
        self.player2score = 0
        self.player1 = 0
        self.player2 = 0
	self.pieceCount = 0
    # Count the number of pieces already played
    def checkpieceCount(self):
        self.pieceCount = 0
        for row in self.gameBoard:
            for piece in row:
                if piece != 0:
                    self.pieceCount += 1
        return self.pieceCount
    # check the moves whether they are valid or not
    def isvalidMove(self,position):
        row = self.gameBoard[0]
        if row[position] == 0:
            return True
        else:
            return False

    # defines the number of possible columns
    def numberofPossibleColumns(self):
        return [i for i, x in enumerate(self.gameBoard[0]) if x == 0]

    # Output current game status to console
    def printGameBoard(self):
                print ' -----------------'
                for i in range (0,6):
                    print ' |',
                    for j in range (0,7):
                        print('%d' % self.gameBoard[i][j]),
                    print '| '
                print ' -----------------'

    # Output current game status to file
    def printGameBoardToFile(self,outputfile):
        f = open(outputfile, 'wb')
        for row in self.gameBoard:
            for piece in row:
                f.write(str(piece))
            f.write('\n')
        f.write(str(self.currentTurn))
        f.close()
    def setBoard(self,inputFile,gameMode,nextPlayer):
        count = 0
        fi = open(inputFile).readlines()
        for l in fi:
            if count == 6:
                self.currentTurn = int(l)
                if gameMode == 'one-move':
                    self.player1 = self.currentTurn
                    if self.player1 == 1:
                        self.player2 = 2
                    else:
                        self.player2 = 1
                elif gameMode == 'interactive':
                    if nextPlayer == 'human-next':
                        self.player1 = self.currentTurn
                        self.player2 = 3 - self.player1
                    elif nextPlayer == 'computer-next':
                        self.player2 = self.currentTurn
                        self.player1 = 3 - self.player2
            else:
                self.gameBoard[count] = map(int, list(l.rstrip()))
            count += 1

    # Place the current player's piece in the requested column
    def playPiece(self, column):
        temp = deepcopy(self)
        if temp.isvalidMove(column):
            for row in range(5,-1,-1):
                if temp.gameBoard[row][column] == 0:
                    temp.gameBoard[row][column] = temp.currentTurn
                    if temp.currentTurn == temp.player1:
                        temp.currentTurn = temp.player2
                    else:
                        temp.currentTurn = temp.player1
                    break
        else:
            print "Invalid Move"
            return False, self
        return True, temp

    # Utility Function 
    def utility(self):
        self.countScore()
        return self.player1score - self.player2score
    # Evaluation which returns the difference between player's score
    def evaluation(self):
        self.countScoreDepthLimit()
        return self.player1score - self.player2score
    def countScore(self):
        self.player1score = 0;
        self.player2score = 0;

        # Need to check horizontally
        for row in self.gameBoard:
            # Check Player 1
            if row[0:4] == [self.player1]*4:
                self.player1score += 1
            if row[1:5] == [self.player1]*4:
                self.player1score += 1
            if row[2:6] == [self.player1]*4:
                self.player1score += 1
            if row[3:7] == [self.player1]*4:
                self.player1score += 1

            # Check Player 2
            if row[0:4] == [self.player2]*4:
                self.player2score += 1
            if row[1:5] == [self.player2]*4:
                self.player2score += 1
            if row[2:6] == [self.player2]*4:
                self.player2score += 1
            if row[3:7] == [self.player2]*4:
                self.player2score += 1

        # Check vertically
        for j in range (7):
            # Check player 1
            if (self.gameBoard[0][j] == self.player1 and self.gameBoard[1][j] == self.player1 and
                    self.gameBoard[2][j] == self.player1 and self.gameBoard[3][j] == self.player1):
                self.player1score += 1
            if (self.gameBoard[1][j] == self.player1 and self.gameBoard[2][j] == self.player1 and
                    self.gameBoard[3][j] == self.player1 and self.gameBoard[4][j] == self.player1):
                self.player1score += 1
            if (self.gameBoard[2][j] == self.player1 and self.gameBoard[3][j] == self.player1 and
                    self.gameBoard[4][j] == self.player1 and self.gameBoard[5][j] == self.player1):
                self.player1score += 1
            # Check player 2
            if (self.gameBoard[0][j] == self.player2 and self.gameBoard[1][j] == self.player2 and
                    self.gameBoard[2][j] == self.player2 and self.gameBoard[3][j] == self.player2):
                self.player2score += 1
            if (self.gameBoard[1][j] == self.player2 and self.gameBoard[2][j] == self.player2 and
                    self.gameBoard[3][j] == self.player2 and self.gameBoard[4][j] == self.player2):
                self.player2score += 1
            if (self.gameBoard[2][j] == self.player2 and self.gameBoard[3][j] == self.player2 and
                    self.gameBoard[4][j] == self.player2 and self.gameBoard[5][j] == self.player2):
                self.player2score += 1

            # Check diagonally

            # Check player 1
            if (self.gameBoard[2][0] == self.player1 and self.gameBoard[3][1] == self.player1 and
                    self.gameBoard[4][2] == self.player1 and self.gameBoard[5][3] == self.player1):
                self.player1score += 1
            if (self.gameBoard[1][0] == self.player1 and self.gameBoard[2][1] == self.player1 and
                    self.gameBoard[3][2] == self.player1 and self.gameBoard[4][3] == self.player1):
                self.player1score += 1
            if (self.gameBoard[2][1] == self.player1 and self.gameBoard[3][2] == self.player1 and
                    self.gameBoard[4][3] == self.player1 and self.gameBoard[5][4] == self.player1):
                self.player1score += 1
            if (self.gameBoard[0][0] == self.player1 and self.gameBoard[1][1] == self.player1 and
                    self.gameBoard[2][2] == self.player1 and self.gameBoard[3][3] == self.player1):
                self.player1score += 1
            if (self.gameBoard[1][1] == self.player1 and self.gameBoard[2][2] == self.player1 and
                    self.gameBoard[3][3] == self.player1 and self.gameBoard[4][4] == self.player1):
                self.player1score += 1
            if (self.gameBoard[2][2] == self.player1 and self.gameBoard[3][3] == self.player1 and
                    self.gameBoard[4][4] == self.player1 and self.gameBoard[5][5] == self.player1):
                self.player1score += 1
            if (self.gameBoard[0][1] == self.player1 and self.gameBoard[1][2] == self.player1 and
                    self.gameBoard[2][3] == self.player1 and self.gameBoard[3][4] == self.player1):
                self.player1score += 1
            if (self.gameBoard[1][2] == self.player1 and self.gameBoard[2][3] == self.player1 and
                    self.gameBoard[3][4] == self.player1 and self.gameBoard[4][5] == self.player1):
                self.player1score += 1
            if (self.gameBoard[2][3] == self.player1 and self.gameBoard[3][4] == self.player1 and
                    self.gameBoard[4][5] == self.player1 and self.gameBoard[5][6] == self.player1):
                self.player1score += 1
            if (self.gameBoard[0][2] == self.player1 and self.gameBoard[1][3] == self.player1 and
                    self.gameBoard[2][4] == self.player1 and self.gameBoard[3][5] == self.player1):
                self.player1score += 1
            if (self.gameBoard[1][3] == self.player1 and self.gameBoard[2][4] == self.player1 and
                    self.gameBoard[3][5] == self.player1 and self.gameBoard[4][6] == self.player1):
                self.player1score += 1
            if (self.gameBoard[0][3] == self.player1 and self.gameBoard[1][4] == self.player1 and
                    self.gameBoard[2][5] == self.player1 and self.gameBoard[3][6] == self.player1):
                self.player1score += 1

            if (self.gameBoard[0][3] == self.player1 and self.gameBoard[1][2] == self.player1 and
                    self.gameBoard[2][1] == self.player1 and self.gameBoard[3][0] == self.player1):
                self.player1score += 1
            if (self.gameBoard[0][4] == self.player1 and self.gameBoard[1][3] == self.player1 and
                    self.gameBoard[2][2] == self.player1 and self.gameBoard[3][1] == self.player1):
                self.player1score += 1
            if (self.gameBoard[1][3] == self.player1 and self.gameBoard[2][2] == self.player1 and
                    self.gameBoard[3][1] == self.player1 and self.gameBoard[4][0] == self.player1):
                self.player1score += 1
            if (self.gameBoard[0][5] == self.player1 and self.gameBoard[1][4] == self.player1 and
                    self.gameBoard[2][3] == self.player1 and self.gameBoard[3][2] == self.player1):
                self.player1score += 1
            if (self.gameBoard[1][4] == self.player1 and self.gameBoard[2][3] == self.player1 and
                    self.gameBoard[3][2] == self.player1 and self.gameBoard[4][1] == self.player1):
                self.player1score += 1
            if (self.gameBoard[2][3] == self.player1 and self.gameBoard[3][2] == self.player1 and
                    self.gameBoard[4][1] == self.player1 and self.gameBoard[5][0] == self.player1):
                self.player1score += 1
            if (self.gameBoard[0][6] == self.player1 and self.gameBoard[1][5] == self.player1 and
                    self.gameBoard[2][4] == self.player1 and self.gameBoard[3][3] == self.player1):
                self.player1score += 1
            if (self.gameBoard[1][5] == self.player1 and self.gameBoard[2][4] == self.player1 and
                    self.gameBoard[3][3] == self.player1 and self.gameBoard[4][2] == self.player1):
                self.player1score += 1
            if (self.gameBoard[2][4] == self.player1 and self.gameBoard[3][3] == self.player1 and
                    self.gameBoard[4][2] == self.player1 and self.gameBoard[5][1] == self.player1):
                self.player1score += 1
            if (self.gameBoard[1][6] == self.player1 and self.gameBoard[2][5] == self.player1 and
                    self.gameBoard[3][4] == self.player1 and self.gameBoard[4][3] == self.player1):
                self.player1score += 1
            if (self.gameBoard[2][5] == self.player1 and self.gameBoard[3][4] == self.player1 and
                    self.gameBoard[4][3] == self.player1 and self.gameBoard[5][2] == self.player1):
                self.player1score += 1
            if (self.gameBoard[2][6] == self.player1 and self.gameBoard[3][5] == self.player1 and
                    self.gameBoard[4][4] == self.player1 and self.gameBoard[5][3] == self.player1):
                self.player1score += 1

            # Check player 2
            if (self.gameBoard[2][0] == self.player2 and self.gameBoard[3][1] == self.player2 and
                    self.gameBoard[4][2] == self.player2 and self.gameBoard[5][3] == self.player2):
                self.player2score += 1
            if (self.gameBoard[1][0] == self.player2 and self.gameBoard[2][1] == self.player2 and
                    self.gameBoard[3][2] == self.player2 and self.gameBoard[4][3] == self.player2):
                self.player2score += 1
            if (self.gameBoard[2][1] == self.player2 and self.gameBoard[3][2] == self.player2 and
                    self.gameBoard[4][3] == self.player2 and self.gameBoard[5][4] == self.player2):
                self.player2score += 1
            if (self.gameBoard[0][0] == self.player2 and self.gameBoard[1][1] == self.player2 and
                    self.gameBoard[2][2] == self.player2 and self.gameBoard[3][3] == self.player2):
                self.player2score += 1
            if (self.gameBoard[1][1] == self.player2 and self.gameBoard[2][2] == self.player2 and
                    self.gameBoard[3][3] == self.player2 and self.gameBoard[4][4] == self.player2):
                self.player2score += 1
            if (self.gameBoard[2][2] == self.player2 and self.gameBoard[3][3] == self.player2 and
                    self.gameBoard[4][4] == self.player2 and self.gameBoard[5][5] == self.player2):
                self.player2score += 1
            if (self.gameBoard[0][1] == self.player2 and self.gameBoard[1][2] == self.player2 and
                    self.gameBoard[2][3] == self.player2 and self.gameBoard[3][4] == self.player2):
                self.player2score += 1
            if (self.gameBoard[1][2] == self.player2 and self.gameBoard[2][3] == self.player2 and
                    self.gameBoard[3][4] == self.player2 and self.gameBoard[4][5] == self.player2):
                self.player2score += 1
            if (self.gameBoard[2][3] == self.player2 and self.gameBoard[3][4] == self.player2 and
                    self.gameBoard[4][5] == self.player2 and self.gameBoard[5][6] == self.player2):
                self.player2score += 1
            if (self.gameBoard[0][2] == self.player2 and self.gameBoard[1][3] == self.player2 and
                    self.gameBoard[2][4] == self.player2 and self.gameBoard[3][5] == self.player2):
                self.player2score += 1
            if (self.gameBoard[1][3] == self.player2 and self.gameBoard[2][4] == self.player2 and
                    self.gameBoard[3][5] == self.player2 and self.gameBoard[4][6] == self.player2):
                self.player2score += 1
            if (self.gameBoard[0][3] == self.player2 and self.gameBoard[1][4] == self.player2 and
                    self.gameBoard[2][5] == self.player2 and self.gameBoard[3][6] == self.player2):
                self.player2score += 1

            if (self.gameBoard[0][3] == self.player2 and self.gameBoard[1][2] == self.player2 and
                    self.gameBoard[2][1] == self.player2 and self.gameBoard[3][0] == self.player2):
                self.player2score += 1
            if (self.gameBoard[0][4] == self.player2 and self.gameBoard[1][3] == self.player2 and
                    self.gameBoard[2][2] == self.player2 and self.gameBoard[3][1] == self.player2):
                self.player2score += 1
            if (self.gameBoard[1][3] == self.player2 and self.gameBoard[2][2] == self.player2 and
                    self.gameBoard[3][1] == self.player2 and self.gameBoard[4][0] == self.player2):
                self.player2score += 1
            if (self.gameBoard[0][5] == self.player2 and self.gameBoard[1][4] == self.player2 and
                    self.gameBoard[2][3] == self.player2 and self.gameBoard[3][2] == self.player2):
                self.player2score += 1
            if (self.gameBoard[1][4] == self.player2 and self.gameBoard[2][3] == self.player2 and
                    self.gameBoard[3][2] == self.player2 and self.gameBoard[4][1] == self.player2):
                self.player2score += 1
            if (self.gameBoard[2][3] == self.player2 and self.gameBoard[3][2] == self.player2 and
                    self.gameBoard[4][1] == self.player2 and self.gameBoard[5][0] == self.player2):
                self.player2score += 1
            if (self.gameBoard[0][6] == self.player2 and self.gameBoard[1][5] == self.player2 and
                    self.gameBoard[2][4] == self.player2 and self.gameBoard[3][3] == self.player2):
                self.player2score += 1
            if (self.gameBoard[1][5] == self.player2 and self.gameBoard[2][4] == self.player2 and
                    self.gameBoard[3][3] == self.player2 and self.gameBoard[4][2] == self.player2):
                self.player2score += 1
            if (self.gameBoard[2][4] == self.player2 and self.gameBoard[3][3] == self.player2 and
                    self.gameBoard[4][2] == self.player2 and self.gameBoard[5][1] == self.player2):
                self.player2score += 1
            if (self.gameBoard[1][6] == self.player2 and self.gameBoard[2][5] == self.player2 and
                    self.gameBoard[3][4] == self.player2 and self.gameBoard[4][3] == self.player2):
                self.player2score += 1
            if (self.gameBoard[2][5] == self.player2 and self.gameBoard[3][4] == self.player2 and
                    self.gameBoard[4][3] == self.player2 and self.gameBoard[5][2] == self.player2):
                self.player2score += 1
            if (self.gameBoard[2][6] == self.player2 and self.gameBoard[3][5] == self.player2 and
                    self.gameBoard[4][4] == self.player2 and self.gameBoard[5][3] == self.player2):
                self.player2score += 1

    # For Evaluation
    def countScoreDepthLimit(self):
        self.player1score = 0;
        self.player2score = 0;

        # Check horizontally
        for row in self.gameBoard:
            # Check player 1
            if row[0:4] == [self.player1]*4:
                self.player1score += 1
            if row[1:5] == [self.player1]*4:
                self.player1score += 1
            if row[2:6] == [self.player1]*4:
                self.player1score += 1
            if row[3:7] == [self.player1]*4:
                self.player1score += 1

            if row[0:3] == [self.player1]*3:
                self.player1score += 0.75
            if row[1:4] == [self.player1]*3:
                self.player1score += 0.75
            if row[2:5] == [self.player1]*3:
                self.player1score += 0.75
            if row[3:6] == [self.player1]*3:
                self.player1score += 0.75

        # Check player 2
            if row[0:4] == [self.player2]*4:
                self.player2score += 1
            if row[1:5] == [self.player2]*4:
                self.player2score += 1
            if row[2:6] == [self.player2]*4:
                self.player2score += 1
            if row[3:7] == [self.player2]*4:
                self.player2score += 1

            if row[0:3] == [self.player2]*3:
                self.player2score += 0.75
            if row[1:4] == [self.player2]*3:
                self.player2score += 0.75
            if row[2:4] == [self.player2]*3:
                self.player2score += 0.75
            if row[3:5] == [self.player2]*3:
                self.player2score += 0.75

        # Check vertically
        for j in range(7):
            # Check player 1
            if (self.gameBoard[0][j] == self.player1 and self.gameBoard[1][j] == self.player1 and
                   self.gameBoard[2][j] == self.player1 and self.gameBoard[3][j] == self.player1):
                self.player1score += 1
            if (self.gameBoard[1][j] == self.player1 and self.gameBoard[2][j] == self.player1 and
                   self.gameBoard[3][j] == self.player1 and self.gameBoard[4][j] == self.player1):
                self.player1score += 1
            if (self.gameBoard[2][j] == self.player1 and self.gameBoard[3][j] == self.player1 and
                   self.gameBoard[4][j] == self.player1 and self.gameBoard[5][j] == self.player1):
                self.player1score += 1

            if (self.gameBoard[0][j] == self.player1 and self.gameBoard[1][j] == self.player1 and
                    self.gameBoard[2][j] == self.player1):
                self.player1score += 0.75
            if (self.gameBoard[1][j] == self.player1 and self.gameBoard[2][j] == self.player1 and
                    self.gameBoard[3][j] == self.player1):
                self.player1score += 0.75
            if (self.gameBoard[2][j] == self.player1 and self.gameBoard[3][j] == self.player1 and
                    self.gameBoard[4][j] == self.player1):
                self.player1score += 0.75
            if (self.gameBoard[3][j] == self.player1 and self.gameBoard[4][j] == self.player1 and
                    self.gameBoard[5][j] == self.player1):
                self.player1score += 0.75

            # Check player 2
            if (self.gameBoard[0][j] == self.player2 and self.gameBoard[1][j] == self.player2 and
                   self.gameBoard[2][j] == self.player2 and self.gameBoard[3][j] == self.player2):
                self.player2score += 1
            if (self.gameBoard[1][j] == self.player2 and self.gameBoard[2][j] == self.player2 and
                   self.gameBoard[3][j] == self.player2 and self.gameBoard[4][j] == self.player2):
                self.player2score += 1
            if (self.gameBoard[2][j] == self.player2 and self.gameBoard[3][j] == self.player2 and
                   self.gameBoard[4][j] == self.player2 and self.gameBoard[5][j] == self.player2):
                self.player2score += 1

            if (self.gameBoard[0][j] == self.player2 and self.gameBoard[1][j] == self.player2 and
                    self.gameBoard[2][j] == self.player2):
                self.player2score += 0.75
            if (self.gameBoard[1][j] == self.player2 and self.gameBoard[2][j] == self.player2 and
                    self.gameBoard[3][j] == self.player2):
                self.player2score += 0.75
            if (self.gameBoard[2][j] == self.player2 and self.gameBoard[3][j] == self.player2 and
                    self.gameBoard[4][j] == self.player2):
                self.player2score += 0.75
            if (self.gameBoard[3][j] == self.player2 and self.gameBoard[4][j] == self.player2 and
                    self.gameBoard[5][j] == self.player2):
                self.player2score += 0.75

        # Check diagonally

        # Check player 1
        if (self.gameBoard[2][0] == self.player1 and self.gameBoard[3][1] == self.player1 and
               self.gameBoard[4][2] == self.player1 and self.gameBoard[5][3] == self.player1):
            self.player1score += 1
        if (self.gameBoard[1][0] == self.player1 and self.gameBoard[2][1] == self.player1 and
               self.gameBoard[3][2] == self.player1 and self.gameBoard[4][3] == self.player1):
            self.player1score += 1
        if (self.gameBoard[2][1] == self.player1 and self.gameBoard[3][2] == self.player1 and
               self.gameBoard[4][3] == self.player1 and self.gameBoard[5][4] == self.player1):
            self.player1score += 1
        if (self.gameBoard[0][0] == self.player1 and self.gameBoard[1][1] == self.player1 and
               self.gameBoard[2][2] == self.player1 and self.gameBoard[3][3] == self.player1):
            self.player1score += 1
        if (self.gameBoard[1][1] == self.player1 and self.gameBoard[2][2] == self.player1 and
               self.gameBoard[3][3] == self.player1 and self.gameBoard[4][4] == self.player1):
            self.player1score += 1
        if (self.gameBoard[2][2] == self.player1 and self.gameBoard[3][3] == self.player1 and
               self.gameBoard[4][4] == self.player1 and self.gameBoard[5][5] == self.player1):
            self.player1score += 1
        if (self.gameBoard[0][1] == self.player1 and self.gameBoard[1][2] == self.player1 and
               self.gameBoard[2][3] == self.player1 and self.gameBoard[3][4] == self.player1):
            self.player1score += 1
        if (self.gameBoard[1][2] == self.player1 and self.gameBoard[2][3] == self.player1 and
               self.gameBoard[3][4] == self.player1 and self.gameBoard[4][5] == self.player1):
            self.player1score += 1
        if (self.gameBoard[2][3] == self.player1 and self.gameBoard[3][4] == self.player1 and
               self.gameBoard[4][5] == self.player1 and self.gameBoard[5][6] == self.player1):
            self.player1score += 1
        if (self.gameBoard[0][2] == self.player1 and self.gameBoard[1][3] == self.player1 and
               self.gameBoard[2][4] == self.player1 and self.gameBoard[3][5] == self.player1):
            self.player1score += 1
        if (self.gameBoard[1][3] == self.player1 and self.gameBoard[2][4] == self.player1 and
               self.gameBoard[3][5] == self.player1 and self.gameBoard[4][6] == self.player1):
            self.player1score += 1
        if (self.gameBoard[0][3] == self.player1 and self.gameBoard[1][4] == self.player1 and
               self.gameBoard[2][5] == self.player1 and self.gameBoard[3][6] == self.player1):
            self.player1score += 1

        if (self.gameBoard[0][3] == self.player1 and self.gameBoard[1][2] == self.player1 and
               self.gameBoard[2][1] == self.player1 and self.gameBoard[3][0] == self.player1):
            self.player1score += 1
        if (self.gameBoard[0][4] == self.player1 and self.gameBoard[1][3] == self.player1 and
               self.gameBoard[2][2] == self.player1 and self.gameBoard[3][1] == self.player1):
            self.player1score += 1
        if (self.gameBoard[1][3] == self.player1 and self.gameBoard[2][2] == self.player1 and
               self.gameBoard[3][1] == self.player1 and self.gameBoard[4][0] == self.player1):
            self.player1score += 1
        if (self.gameBoard[0][5] == self.player1 and self.gameBoard[1][4] == self.player1 and
               self.gameBoard[2][3] == self.player1 and self.gameBoard[3][2] == self.player1):
            self.player1score += 1
        if (self.gameBoard[1][4] == self.player1 and self.gameBoard[2][3] == self.player1 and
               self.gameBoard[3][2] == self.player1 and self.gameBoard[4][1] == self.player1):
            self.player1score += 1
        if (self.gameBoard[2][3] == self.player1 and self.gameBoard[3][2] == self.player1 and
               self.gameBoard[4][1] == self.player1 and self.gameBoard[5][0] == self.player1):
            self.player1score += 1
        if (self.gameBoard[0][6] == self.player1 and self.gameBoard[1][5] == self.player1 and
               self.gameBoard[2][4] == self.player1 and self.gameBoard[3][3] == self.player1):
            self.player1score += 1
        if (self.gameBoard[1][5] == self.player1 and self.gameBoard[2][4] == self.player1 and
               self.gameBoard[3][3] == self.player1 and self.gameBoard[4][2] == self.player1):
            self.player1score += 1
        if (self.gameBoard[2][4] == self.player1 and self.gameBoard[3][3] == self.player1 and
               self.gameBoard[4][2] == self.player1 and self.gameBoard[5][1] == self.player1):
            self.player1score += 1
        if (self.gameBoard[1][6] == self.player1 and self.gameBoard[2][5] == self.player1 and
               self.gameBoard[3][4] == self.player1 and self.gameBoard[4][3] == self.player1):
            self.player1score += 1
        if (self.gameBoard[2][5] == self.player1 and self.gameBoard[3][4] == self.player1 and
               self.gameBoard[4][3] == self.player1 and self.gameBoard[5][2] == self.player1):
            self.player1score += 1
        if (self.gameBoard[2][6] == self.player1 and self.gameBoard[3][5] == self.player1 and
               self.gameBoard[4][4] == self.player1 and self.gameBoard[5][3] == self.player1):
            self.player1score += 1

        if (self.gameBoard[3][0] == self.player1 and self.gameBoard[4][1] == self.player1 and
                self.gameBoard[5][2] == self.player1):
            self.player1score += 0.75
        if (self.gameBoard[2][0] == self.player1 and self.gameBoard[3][1] == self.player1 and
                self.gameBoard[4][2] == self.player1):
            self.player1score += 0.75
        if (self.gameBoard[3][1] == self.player1 and self.gameBoard[4][2] == self.player1 and
                self.gameBoard[5][3] == self.player1):
            self.player1score += 0.75
        if (self.gameBoard[1][0] == self.player1 and self.gameBoard[2][1] == self.player1 and
                self.gameBoard[3][2] == self.player1):
            self.player1score += 0.75
        if (self.gameBoard[2][1] == self.player1 and self.gameBoard[3][2] == self.player1 and
                self.gameBoard[4][3] == self.player1):
            self.player1score += 0.75
        if (self.gameBoard[3][2] == self.player1 and self.gameBoard[4][3] == self.player1 and
                self.gameBoard[5][4] == self.player1):
            self.player1score += 0.75
        if (self.gameBoard[0][0] == self.player1 and self.gameBoard[1][1] == self.player1 and
               self.gameBoard[2][2] == self.player1):
            self.player1score += 0.75
        if (self.gameBoard[1][1] == self.player1 and self.gameBoard[2][2] == self.player1 and
                self.gameBoard[3][3] == self.player1):
            self.player1score += 0.75
        if (self.gameBoard[2][2] == self.player1 and self.gameBoard[3][3] == self.player1 and
                self.gameBoard[4][4] == self.player1):
            self.player1score += 0.75
        if (self.gameBoard[3][3] == self.player1 and self.gameBoard[4][4] == self.player1 and
               self.gameBoard[5][5] == self.player1):
            self.player1score += 0.75
        if (self.gameBoard[0][1] == self.player1 and self.gameBoard[1][2] == self.player1 and
                self.gameBoard[2][3] == self.player1):
            self.player1score += 0.75
        if (self.gameBoard[1][2] == self.player1 and self.gameBoard[2][3] == self.player1 and
                self.gameBoard[3][4] == self.player1):
            self.player1score += 0.75
        if (self.gameBoard[2][3] == self.player1 and self.gameBoard[3][4] == self.player1 and
                self.gameBoard[4][5] == self.player1):
            self.player1score += 0.75
        if (self.gameBoard[3][4] == self.player1 and self.gameBoard[4][5] == self.player1 and
                self.gameBoard[5][6] == self.player1):
            self.player1score += 0.75
        if (self.gameBoard[0][2] == self.player1 and self.gameBoard[1][3] == self.player1 and
                self.gameBoard[2][4] == self.player1):
            self.player1score += 0.75
        if (self.gameBoard[1][3] == self.player1 and self.gameBoard[2][4] == self.player1 and
                self.gameBoard[3][5] == self.player1):
            self.player1score += 0.75
        if (self.gameBoard[2][4] == self.player1 and self.gameBoard[3][5] == self.player1 and
                self.gameBoard[4][6] == self.player1):
            self.player1score += 0.75
        if (self.gameBoard[0][3] == self.player1 and self.gameBoard[1][4] == self.player1 and
                self.gameBoard[2][5] == self.player1):
            self.player1score += 0.75
        if (self.gameBoard[1][4] == self.player1 and self.gameBoard[2][5] == self.player1 and
                self.gameBoard[3][6] == self.player1):
            self.player1score += 0.75
        if (self.gameBoard[0][4] == self.player1 and self.gameBoard[1][5] == self.player1 and
                self.gameBoard[2][6] == self.player1):
            self.player1score += 0.75

        if (self.gameBoard[0][2] == self.player1 and self.gameBoard[1][1] == self.player1 and
                self.gameBoard[2][2] == self.player1):
            self.player1score += 0.75
        if (self.gameBoard[0][3] == self.player1 and self.gameBoard[1][2] == self.player1 and
                self.gameBoard[2][1] == self.player1):
            self.player1score += 0.75
        if (self.gameBoard[1][2] == self.player1 and self.gameBoard[2][1] == self.player1 and
                self.gameBoard[3][0] == self.player1):
            self.player1score += 0.75
        if (self.gameBoard[0][4] == self.player1 and self.gameBoard[2][1] == self.player1 and
                self.gameBoard[2][2] == self.player1):
            self.player1score += 0.75
        if (self.gameBoard[1][3] == self.player1 and self.gameBoard[3][2] == self.player1 and
                self.gameBoard[3][1] == self.player1):
            self.player1score += 0.75
        if (self.gameBoard[2][2] == self.player1 and self.gameBoard[4][3] == self.player1 and
               self.gameBoard[4][0] == self.player1):
            self.player1score += 0.75
        if (self.gameBoard[0][5] == self.player1 and self.gameBoard[1][1] == self.player1 and
                self.gameBoard[2][3] == self.player1):
            self.player1score += 0.75
        if (self.gameBoard[1][4] == self.player1 and self.gameBoard[2][2] == self.player1 and
                self.gameBoard[3][2] == self.player1):
            self.player1score += 0.75
        if (self.gameBoard[2][3] == self.player1 and self.gameBoard[3][3] == self.player1 and
                self.gameBoard[4][1] == self.player1):
           self.player1score += 0.75
        if (self.gameBoard[3][2] == self.player1 and self.gameBoard[4][4] == self.player1 and
                self.gameBoard[5][0] == self.player1):
            self.player1score += 0.75
        if (self.gameBoard[0][6] == self.player1 and self.gameBoard[1][2] == self.player1 and
                self.gameBoard[2][4] == self.player1):
            self.player1score += 0.75
        if (self.gameBoard[1][5] == self.player1 and self.gameBoard[2][3] == self.player1 and
                self.gameBoard[3][3] == self.player1):
            self.player1score += 0.75
        if (self.gameBoard[2][4] == self.player1 and self.gameBoard[3][4] == self.player1 and
                self.gameBoard[4][2] == self.player1):
            self.player1score += 0.75
        if (self.gameBoard[3][3] == self.player1 and self.gameBoard[4][5] == self.player1 and
                self.gameBoard[5][1] == self.player1):
            self.player1score += 0.75
        if (self.gameBoard[1][6] == self.player1 and self.gameBoard[1][3] == self.player1 and
                self.gameBoard[3][4] == self.player1):
            self.player1score += 0.75
        if (self.gameBoard[2][5] == self.player1 and self.gameBoard[2][4] == self.player1 and
                self.gameBoard[4][3] == self.player1):
            self.player1score += 0.75
        if (self.gameBoard[3][4] == self.player1 and self.gameBoard[3][5] == self.player1 and
                self.gameBoard[5][2] == self.player1):
            self.player1score += 0.75
        if (self.gameBoard[2][6] == self.player1 and self.gameBoard[1][4] == self.player1 and
                self.gameBoard[4][4] == self.player1):
            self.player1score += 0.75
        if (self.gameBoard[3][5] == self.player1 and self.gameBoard[2][5] == self.player1 and
                self.gameBoard[5][3] == self.player1):
            self.player1score += 0.75
        if (self.gameBoard[3][6] == self.player1 and self.gameBoard[1][5] == self.player1 and
                self.gameBoard[5][4] == self.player1):
            self.player1score += 0.75

        # Check player 2
        if (self.gameBoard[2][0] == self.player2 and self.gameBoard[3][1] == self.player2 and
               self.gameBoard[4][2] == self.player2 and self.gameBoard[5][3] == self.player2):
            self.player2score += 1
        if (self.gameBoard[1][0] == self.player2 and self.gameBoard[2][1] == self.player2 and
               self.gameBoard[3][2] == self.player2 and self.gameBoard[4][3] == self.player2):
            self.player2score += 1
        if (self.gameBoard[2][1] == self.player2 and self.gameBoard[3][2] == self.player2 and
               self.gameBoard[4][3] == self.player2 and self.gameBoard[5][4] == self.player2):
            self.player2score += 1
        if (self.gameBoard[0][0] == self.player2 and self.gameBoard[1][1] == self.player2 and
               self.gameBoard[2][2] == self.player2 and self.gameBoard[3][3] == self.player2):
            self.player2score += 1
        if (self.gameBoard[1][1] == self.player2 and self.gameBoard[2][2] == self.player2 and
               self.gameBoard[3][3] == self.player2 and self.gameBoard[4][4] == self.player2):
            self.player2score += 1
        if (self.gameBoard[2][2] == self.player2 and self.gameBoard[3][3] == self.player2 and
               self.gameBoard[4][4] == self.player2 and self.gameBoard[5][5] == self.player2):
            self.player2score += 1
        if (self.gameBoard[0][1] == self.player2 and self.gameBoard[1][2] == self.player2 and
               self.gameBoard[2][3] == self.player2 and self.gameBoard[3][4] == self.player2):
            self.player2score += 1
        if (self.gameBoard[1][2] == self.player2 and self.gameBoard[2][3] == self.player2 and
               self.gameBoard[3][4] == self.player2 and self.gameBoard[4][5] == self.player2):
            self.player2score += 1
        if (self.gameBoard[2][3] == self.player2  and self.gameBoard[3][4] == self.player2 and
                self.gameBoard[4][5] == self.player2 and self.gameBoard[5][6] == self.player2):
            self.player2score += 1
        if (self.gameBoard[0][2] == self.player2 and self.gameBoard[1][3] == self.player2 and
                self.gameBoard[2][4] == self.player2 and self.gameBoard[3][5] == self.player2 ):
            self.player2score += 1
        if (self.gameBoard[1][3] == self.player2 and self.gameBoard[2][4] == self.player2 and
                self.gameBoard[3][5] == self.player2  and self.gameBoard[4][6] == self.player2):
            self.player2score += 1
        if (self.gameBoard[0][3] == self.player2 and self.gameBoard[1][4] == self.player2 and
              self.gameBoard[2][5] == self.player2 and self.gameBoard[3][6] == self.player2):
            self.player2score += 1

        if (self.gameBoard[0][3] == self.player2 and self.gameBoard[1][2] == self.player2 and
               self.gameBoard[2][1] == self.player2 and self.gameBoard[3][0] == self.player2):
            self.player2score += 1
        if (self.gameBoard[0][4] == self.player2 and self.gameBoard[1][3] == self.player2 and
               self.gameBoard[2][2] == self.player2 and self.gameBoard[3][1] == self.player2):
            self.player2score += 1
        if (self.gameBoard[1][3] == self.player2 and self.gameBoard[2][2] == self.player2 and
               self.gameBoard[3][1] == self.player2 and self.gameBoard[4][0] == self.player2):
            self.player2score += 1
        if (self.gameBoard[0][5] == self.player2 and self.gameBoard[1][4] == self.player2 and
               self.gameBoard[2][3] == self.player2 and self.gameBoard[3][2] == self.player2):
            self.player2score += 1
        if (self.gameBoard[1][4] == self.player2 and self.gameBoard[2][3] == self.player2 and
               self.gameBoard[3][2] == self.player2 and self.gameBoard[4][1] == self.player2):
            self.player2score += 1
        if (self.gameBoard[2][3] == self.player2 and self.gameBoard[3][2] == self.player2 and
               self.gameBoard[4][1] == self.player2 and self.gameBoard[5][0] == self.player2):
            self.player2score += 1
        if (self.gameBoard[0][6] == self.player2 and self.gameBoard[1][5] == self.player2 and
               self.gameBoard[2][4] == self.player2 and self.gameBoard[3][3] == self.player2):
            self.player2score += 1
        if (self.gameBoard[1][5] == self.player2 and self.gameBoard[2][4] == self.player2 and
               self.gameBoard[3][3] == self.player2 and self.gameBoard[4][2] == self.player2):
            self.player2score += 1
        if (self.gameBoard[2][4] == self.player2 and self.gameBoard[3][3] == self.player2 and
               self.gameBoard[4][2] == self.player2 and self.gameBoard[5][1] == self.player2):
            self.player2score += 1
        if (self.gameBoard[1][6] == self.player2 and self.gameBoard[2][5] == self.player2 and
               self.gameBoard[3][4] == self.player2 and self.gameBoard[4][3] == self.player2):
            self.player2score += 1
        if (self.gameBoard[2][5] == self.player2 and self.gameBoard[3][4] == self.player2 and
               self.gameBoard[4][3] == self.player2 and self.gameBoard[5][2] == self.player2):
            self.player2score += 1
        if (self.gameBoard[2][6] == self.player2 and self.gameBoard[3][5] == self.player2 and
               self.gameBoard[4][4] == self.player2 and self.gameBoard[5][3] == self.player2):
            self.player2score += 1

        if (self.gameBoard[3][0] == self.player2 and self.gameBoard[4][1] == self.player2 and
                self.gameBoard[5][2] == self.player2):
            self.player2score += 0.75
        if (self.gameBoard[2][0] == self.player2 and self.gameBoard[3][1] == self.player2 and
                self.gameBoard[4][2] == self.player2):
            self.player2score += 0.75
        if (self.gameBoard[3][1] == self.player2 and self.gameBoard[4][2] == self.player2 and
                self.gameBoard[5][3] == self.player2):
            self.player2score += 0.75
        if (self.gameBoard[1][0] == self.player2 and self.gameBoard[2][1] == self.player2 and
                self.gameBoard[3][2] == self.player2):
            self.player2score += 0.75
        if (self.gameBoard[2][1] == self.player2 and self.gameBoard[3][2] == self.player2 and
                self.gameBoard[4][3] == self.player2):
            self.player2score += 0.75
        if (self.gameBoard[3][2] == self.player2 and self.gameBoard[4][3] == self.player2 and
                self.gameBoard[5][4] == self.player2):
            self.player2score += 0.75
        if (self.gameBoard[0][0] == self.player2 and self.gameBoard[1][1] == self.player2 and
                self.gameBoard[2][2] == self.player2):
            self.player2score += 0.75
        if (self.gameBoard[1][1] == self.player2 and self.gameBoard[2][2] == self.player2 and
                self.gameBoard[3][3] == self.player2):
            self.player2score += 0.75
        if (self.gameBoard[2][2] == self.player2 and self.gameBoard[3][3] == self.player2 and
                self.gameBoard[4][4] == self.player2):
            self.player2score += 0.75
        if (self.gameBoard[3][3] == self.player2 and self.gameBoard[4][4] == self.player2 and
                self.gameBoard[5][5] == self.player2):
            self.player2score += 0.75
        if (self.gameBoard[0][1] == self.player2 and self.gameBoard[1][2] == self.player2 and
                self.gameBoard[2][3] == self.player2):
            self.player2score += 0.75
        if (self.gameBoard[1][2] == self.player2 and self.gameBoard[2][3] == self.player2 and
                self.gameBoard[3][4] == self.player1):
            self.player2score += 0.75
        if (self.gameBoard[2][3] == self.player2 and self.gameBoard[3][4] == self.player2 and
                self.gameBoard[4][5] == self.player2):
            self.player2score += 0.75
        if (self.gameBoard[3][4] == self.player2 and self.gameBoard[4][5] == self.player2 and
                self.gameBoard[5][6] == self.player2):
            self.player2score += 0.75
        if (self.gameBoard[0][2] == self.player2 and self.gameBoard[1][3] == self.player2 and
                self.gameBoard[2][4] == self.player2):
            self.player2score += 0.75
        if (self.gameBoard[1][3] == self.player2 and self.gameBoard[2][4] == self.player2 and
                self.gameBoard[3][5] == self.player2):
            self.player2score += 0.75
        if (self.gameBoard[2][4] == self.player2 and self.gameBoard[3][5] == self.player2 and
                self.gameBoard[4][6] == self.player2):
            self.player2score += 0.75
        if (self.gameBoard[0][3] == self.player2 and self.gameBoard[1][4] == self.player2 and
                self.gameBoard[2][5] == self.player2):
            self.player2score += 0.75
        if (self.gameBoard[1][4] == self.player2 and self.gameBoard[2][5] == self.player2 and
                self.gameBoard[3][6] == self.player2):
            self.player2score += 0.75
        if (self.gameBoard[0][4] == self.player2 and self.gameBoard[1][5] == self.player2 and
                self.gameBoard[2][6] == self.player2):
            self.player2score += 0.75

        if (self.gameBoard[0][2] == self.player2 and self.gameBoard[1][1] == self.player2 and
                self.gameBoard[2][2] == self.player2):
            self.player2score += 0.75
        if (self.gameBoard[0][3] == self.player2 and self.gameBoard[1][2] == self.player2 and
                self.gameBoard[2][1] == self.player2):
            self.player2score += 0.75
        if (self.gameBoard[1][2] == self.player2 and self.gameBoard[2][1] == self.player2 and
                self.gameBoard[3][0] == self.player2):
            self.player2score += 0.75
        if (self.gameBoard[0][4] == self.player2 and self.gameBoard[2][1] == self.player2 and
                self.gameBoard[2][2] == self.player2):
            self.player2score += 0.75
        if (self.gameBoard[1][3] == self.player2 and self.gameBoard[3][2] == self.player2 and
                self.gameBoard[3][1] == self.player2):
            self.player2score += 0.75
        if (self.gameBoard[2][2] == self.player2 and self.gameBoard[4][3] == self.player2 and
                self.gameBoard[4][0] == self.player2):
            self.player2score += 0.75
        if (self.gameBoard[0][5] == self.player2 and self.gameBoard[1][1] == self.player2 and
                self.gameBoard[2][3] == self.player2):
            self.player2score += 0.75
        if (self.gameBoard[1][4] == self.player2 and self.gameBoard[2][2] == self.player2 and
                self.gameBoard[3][2] == self.player2):
            self.player2score += 0.75
        if (self.gameBoard[2][3] == self.player2 and self.gameBoard[3][3] == self.player2 and
                self.gameBoard[4][1] == self.player2):
            self.player2score += 0.75
        if (self.gameBoard[3][2] == self.player2 and self.gameBoard[4][4] == self.player2 and
                self.gameBoard[5][0] == self.player2):
            self.player2score += 0.75
        if (self.gameBoard[0][6] == self.player2 and self.gameBoard[1][2] == self.player2 and
                self.gameBoard[2][4] == self.player2):
            self.player2score += 0.75
        if (self.gameBoard[1][5] == self.player2 and self.gameBoard[2][3] == self.player2 and
                self.gameBoard[3][3] == self.player2):
            self.player2score += 0.75
        if (self.gameBoard[2][4] == self.player2 and self.gameBoard[3][4] == self.player2 and
                self.gameBoard[4][2] == self.player2):
            self.player2score += 0.75
        if (self.gameBoard[3][3] == self.player2 and self.gameBoard[4][5] == self.player2 and
                self.gameBoard[5][1] == self.player2):
            self.player2score += 0.75
        if (self.gameBoard[1][6] == self.player2 and self.gameBoard[1][3] == self.player2 and
                self.gameBoard[3][4] == self.player2):
            self.player2score += 0.75
        if (self.gameBoard[2][5] == self.player2 and self.gameBoard[2][4] == self.player2 and
                self.gameBoard[4][3] == self.player2):
            self.player2score += 0.75
        if (self.gameBoard[3][4] == self.player2 and self.gameBoard[3][5] == self.player2 and
                self.gameBoard[5][2] == self.player2):
            self.player2score += 0.75
        if (self.gameBoard[2][6] == self.player2 and self.gameBoard[1][4] == self.player2 and
                self.gameBoard[4][4] == self.player2):
            self.player2score += 0.75
        if (self.gameBoard[3][5] == self.player2 and self.gameBoard[2][5] == self.player2 and
                self.gameBoard[5][3] == self.player2):
            self.player2score += 0.75
        if (self.gameBoard[3][6] == self.player2 and self.gameBoard[1][5] == self.player2 and
                self.gameBoard[5][4] == self.player2):
            self.player2score += 0.75