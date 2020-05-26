# oskaplayer(['wwww','---','--','---','bbbb'],'w',2)

import math
import copy

# ***** CHARACTER CONSTANTS ***** #
WHITE = 'w'
BLACK = 'b'
EMPTY_SPACE = '-'

# ***** WHITE MOVES ***** #
MOVE_DOWN = {
    "description": "move down",
    "i": 1,
    "j": 0
}
MOVE_DOWN_LEFT = {
    "description": "move down left",
    "i": 1,
    "j": -1
}
MOVE_DOWN_RIGHT = {
    "description": "move down right",
    "i": 1,
    "j": 1
}
JUMP_DOWN = {
    "description": "jump down",
    "i": 2,
    "j": 0,
    "iCapture": 1,
    "jCapture": 0
}
JUMP_DOWN_LEFT = {
    "description": "jump down left",
    "i": 2,
    "j": -2,
    "iCapture": 1,
    "jCapture": -1
}
JUMP_DOWN_RIGHT = {
    "description": "jump down right",
    "i": 2,
    "j": 2,
    "iCapture": 1,
    "jCapture": 1
}
JUMP_DOWN_DIAG_RIGHT = {
    "description": "jump down diagonal right",
    "i": 2,
    "j": 1,
    "iCapture": 1,
    "jCapture": 0
}
JUMP_DIAG_LEFT_DOWN = {
    "description": "jump diagonal left down",
    "i": 2,
    "j": -1,
    "iCapture": 1,
    "jCapture": -1
}

# ***** BLACK MOVES ***** #
MOVE_UP = {
    "description": "move up",
    "i": -1,
    "j": 0
}
MOVE_UP_LEFT = {
    "description": "move up left",
    "i": -1,
    "j": -1
}
MOVE_UP_RIGHT = {
    "description": "move up right",
    "i": -1,
    "j": 1
}
JUMP_UP = {
    "description": "jump up",
    "i": -2,
    "j": 0,
    "iCapture": -1,
    "jCapture": 0
}
JUMP_UP_LEFT = {
    "description": "jump up left",
    "i": -2,
    "j": -2,
    "iCapture": -1,
    "jCapture": -1
}
JUMP_UP_RIGHT = {
    "description": "jump up right",
    "i": -2,
    "j": 2,
    "iCapture": -1,
    "jCapture": 1
}
JUMP_UP_DIAG_RIGHT = {
    "description": "jump up diagonal right",
    "i": -2,
    "j": 1,
    "iCapture": -1,
    "jCapture": 0
}
JUMP_DIAG_LEFT_UP = {
    "description": "jump diagonal left up",
    "i": -2,
    "j": -1,
    "iCapture": -1,
    "jCapture": -1
}


class Game:
    def __init__(self, board, firstPlayer, depth):
        self.state = board  # current state of the game
        self.player = firstPlayer
        self.depth = depth

    def play(self):
        '''
            This function calls the minimax function to determine the next best move
            Return:
                @state: the next best state to take
        '''
        score, state = self.minimax()
        return state

    def minimax(self):
        '''
            This function performs minimax by going down the game tree up until the specified depth and gets the best score for each player
            Return:
                @score: score propagated up from the evaluated states
                @bestState: next best child state to choose 
        '''
        bestVal = 0
        bestState = self.state  # test
        if (self.depth == 0):
            score = self.eval()
            return score, self.state

        if (self.player == WHITE):  # maximizing player
            bestVal = -math.inf
            nextStates = self.moveGen()  # get nextStates
            for state in nextStates:
                nextState = copy.deepcopy(state)
                game = Game(nextState, BLACK, self.depth - 1)
                childVal, childState = game.minimax()
                bestVal = max(bestVal, childVal)

                if (bestVal == childVal):
                    bestState = nextState
        elif (self.player == BLACK):
            bestVal = math.inf
            nextStates = self.moveGen()  # get nextStates
            for state in nextStates:
                nextState = copy.deepcopy(state)
                game = Game(nextState, WHITE, self.depth - 1)
                childVal, childState = game.minimax()
                bestVal = min(bestVal, childVal)
                if (bestVal == childVal):
                    bestState = nextState

        return bestVal, bestState

    def eval(self):
        '''
            This function evaluates a state by assigning +/-100 if either player has won. Otherwise, it evaluates the board by considering the number of both players remaining on the board and the number of players in the opponent's rows
            Return:
                @score: state's value that is evaluated using the heuristics
        '''
        numWhite = 0
        numBlack = 0
        board = self.state.board

        # get number of player pieces
        for row in board:
            numWhite += row.count(WHITE)
            numBlack += row.count(BLACK)

        if (self.hasWon(WHITE, numWhite, numBlack)):
            return 100
        elif (self.hasWon(BLACK, numWhite, numBlack)):
            return -100
        else:
            numWhiteOnBlackRow = 0
            numBlackOnWhiteRow = 0
            for lastRow in board[-1]:  # number of whites in black's starting position
                numWhiteOnBlackRow = lastRow.count(WHITE)

            for firstRow in board[0]:  # number of black in white's starting position
                numBlackOnWhiteRow = firstRow.count(BLACK)

            score = (numWhite - numBlack) + 2 * \
                (numWhiteOnBlackRow - numBlackOnWhiteRow)

            return score

    def hasWon(self, player, numWhite, numBlack):
        '''
            This function determines whether white or black player has won by getting opponent's remaining pieces and if player's remaining pieces are in opponent's starting row
            Parameters:
                @player: either white or black
                @numWhite: the number of white pieces remaining on the board
                @numBlack: the number of black pieces remaining on the board
        '''
        opponent = BLACK if player == WHITE else WHITE
        board = self.state.board
        numRows = self.state.numRows

        # get number of player pieces
        for row in board:
            numWhite += row.count(WHITE)
            numBlack += row.count(BLACK)

        if (player == WHITE):
            if (numBlack == 0 or board[numRows - 1].count(WHITE) == numWhite):
                return True
        elif (player == BLACK):
            if (numWhite == 0 or board[0].count(BLACK) == numBlack):
                return True

        return False

    # *********** MOVE GENERATOR METHODS *********** #

    def moveGen(self):
        '''
            This function generates all possible states that can be generated by the players
            Return:
                @newStates: possible states generated by calling the possibleMoves and generateNewStates functions
        '''
        board = self.state.board
        newStates = []

        for i in range(self.state.numRows):
            for j in range(len(board[i])):
                if (board[i][j] == self.player):
                    moves = self.possibleMoves(i, j)
                    states = self.generateNewStates(moves, i, j)
                    newStates = newStates + states

        return newStates

    def possibleMoves(self, i, j):
        '''
            This function determines possible moves and/or jumps that player can make
            Parameters:
                @i: row position of player
                @j: column position of player
            Return:
                @moves: list of moves and/or jumps returned by helper functions
        '''
        moves = []
        if (self.player == WHITE):
            whiteMoves = self.possibleWhiteMoves(i, j)
            whiteJumps = self.possibleWhiteJumps(i, j)
            if (whiteMoves):
                moves = moves + whiteMoves
            if (whiteJumps):
                moves = moves + whiteJumps
        elif (self.player == BLACK):
            blackMoves = self.possibleBlackMoves(i, j)
            blackJumps = self.possibleBlackJumps(i, j)
            if (blackMoves):
                moves = moves + blackMoves
            if (blackJumps):
                moves = moves + blackJumps

        return moves

    def generateNewStates(self, possibleMoves, i, j):
        '''
            This function generates all the new states based on possible moves
            Parameters:
                @possibleMoves: possible moves that the current player can make
                @i: row position of player
                @j: column position of player
            Return:
                @newStates: all new possible states using deep-copied versions of current state
        '''
        newStates = []
        for move in possibleMoves:
            newI = i + move["i"]
            newJ = j + move["j"]

            newState = copy.deepcopy(self.state)
            newBoard = newState.board

            newBoard[i][j] = EMPTY_SPACE
            newBoard[newI][newJ] = self.player

            if "jump" in move["description"]:
                iCapture = i + move["iCapture"]
                jCapture = j + move["jCapture"]

                newBoard[iCapture][jCapture] = EMPTY_SPACE

            newStates.append(newState)

        return newStates

    def possibleWhiteMoves(self, i, j):
        '''
            This function returns all possible moves that white player can make
            Parameters:
                @i: row position of white player
                @j: column position of white player
            Return:
                @moves: list of all possible moves i.e. move down, move down left, move down right by verifying the bounds and whether the space is occupied or not. The move names do not reflect the actual oska board but rather the internal representation.
        '''
        moves = []
        board = self.state.board
        numRows = self.state.numRows

        if (i + 1 < numRows and j < len(board[i + 1]) and board[i + 1][j] == EMPTY_SPACE):
            moves.append(MOVE_DOWN)
        if (i < self.state.midpoint):
            if (i + 1 < numRows and j - 1 >= 0 and board[i + 1][j - 1] == EMPTY_SPACE):
                moves.append(MOVE_DOWN_LEFT)
        elif (i >= self.state.midpoint):
            if (i + 1 < numRows and j + 1 < len(board[i + 1]) and board[i + 1][j + 1] == EMPTY_SPACE):
                moves.append(MOVE_DOWN_RIGHT)

        return moves

    def possibleWhiteJumps(self, i, j):
        '''
            This function returns all possible jumps that white player can make
            Parameters:
                @i: row position of white player
                @j: column position of white player
            Return:
                @moves: list of all possible jumps by verifying the bounds, if the space is occupied, and that it skips over black player. The move names do not reflect the actual oska board but rather the internal representation.
        '''
        moves = []
        board = self.state.board
        numRows = self.state.numRows

        if (i + 2 < numRows):  # Jumping skips over one tile
            if (i == self.state.midpoint - 1):  # row before midpoint
                if (j + 1 < len(board[i + 2]) and board[i + 1][j] == BLACK and board[i + 2][j + 1] == EMPTY_SPACE):
                    moves.append(JUMP_DOWN_DIAG_RIGHT)
                if (j - 1 >= 0 and board[i + 1][j - 1] == BLACK and board[i + 2][j - 1] == EMPTY_SPACE):
                    moves.append(JUMP_DIAG_LEFT_DOWN)
            else:
                # white can jump down at row before midpoint - 1 and at and after midpoint
                if (j < len(board[i + 2]) and board[i + 1][j] == BLACK and board[i + 2][j] == EMPTY_SPACE):
                    moves.append(JUMP_DOWN)
                # row before midpoint - 1
                if (i < self.state.midpoint - 1 and j - 2 >= 0 and board[i + 1][j - 1] == BLACK and board[i + 2][j - 2] == EMPTY_SPACE):
                    moves.append(JUMP_DOWN_LEFT)
                # row at and after midpoint
                elif (j + 2 < len(board[i + 2]) and board[i + 1][j + 1] == BLACK and board[i + 2][j + 2] == EMPTY_SPACE):
                    moves.append(JUMP_DOWN_RIGHT)

        return moves

    def possibleBlackMoves(self, i, j):
        '''
            This function returns all possible moves that black player can make
            Parameters:
                @i: row position of black player
                @j: column position of black player
            Return:
                @moves: list of all possible moves i.e. move up, move up left, move up right by verifying the bounds and whether the space is occupied or not. The move names do not reflect the actual oska board but rather the internal representation.
        '''
        moves = []
        board = self.state.board

        if (i - 1 >= 0):
            if (j < len(board[i - 1]) and board[i - 1][j] == EMPTY_SPACE):
                moves.append(MOVE_UP)
            if (i <= self.state.midpoint):  # Row before or at midpoint
                # diagonal right up
                if (j + 1 < len(board[i - 1]) and board[i - 1][j + 1] == EMPTY_SPACE):
                    moves.append(MOVE_UP_RIGHT)
            elif (i > self.state.midpoint):  # After midpoint
                # diagonal left up
                if (i - 1 >= 0 and j - 1 >= 0 and board[i - 1][j - 1] == EMPTY_SPACE):
                    moves.append(MOVE_UP_LEFT)
        return moves

    def possibleBlackJumps(self, i, j):
        '''
            This function returns all possible jumps that black player can make
            Parameters:
                @i: row position of black player
                @j: column position of black player
            Return:
                @moves: list of all possible jumps by verifying the bounds, if the space is occupied, and that it skips over white player. The move names do not reflect the actual oska board but rather the internal representation.
        '''
        moves = []
        board = self.state.board

        if (i - 2 >= 0):
            if (i == self.state.midpoint + 1):  # row after midpoint
                if (j + 1 < len(board[i - 2]) and board[i - 1][j] == WHITE and board[i - 2][j + 1] == EMPTY_SPACE):
                    moves.append(JUMP_UP_DIAG_RIGHT)
                if (j - 1 >= 0 and board[i - 1][j - 1] == WHITE and board[i - 2][j - 1] == EMPTY_SPACE):
                    moves.append(JUMP_DIAG_LEFT_UP)
            else:
                # black can jump up at row after midpoint + 1 and at and before midpoint
                if (j < len(board[i - 2]) and board[i - 1][j] == WHITE and board[i - 2][j] == EMPTY_SPACE):
                    moves.append(JUMP_UP)
                # row after midpoint + 1
                if (i > self.state.midpoint + 1 and j - 2 >= 0 and board[i - 1][j - 1] == WHITE and board[i - 2][j - 2] == EMPTY_SPACE):
                    moves.append(JUMP_UP_LEFT)
                # row at and before midpoint
                elif (i <= self.state.midpoint and j + 2 < len(board[i - 2]) and board[i - 1][j + 1] == WHITE and board[i - 2][j + 2] == EMPTY_SPACE):
                    moves.append(JUMP_UP_RIGHT)

        return moves


class Board:
    def __init__(self, input):
        self.numPieces = self.getNumPieces(input)  # number of pieces
        self.numRows = self.getNumRows()  # number of rows in the board
        self.midpoint = self.getMidpoint()  # midpoint row of board
        self.board = self.makeBoard(input)  # parsed game board

    # *********** CONSTRUCTOR METHODS *********** #

    def makeBoard(self, input):
        '''
            This function parses the input and converts it into the desired representation
            Parameters:
                @input: input board from command line
            Return:
                @board: 2d array which contains mutable characters from input strings
        '''
        board = []
        for row in input:
            board.append(list(row))
        return board

    def getNumPieces(self, input):
        '''
            This function returns the number of pieces in the input
            Parameters:
                @input: input board from command line
            Return:
                Length of the first row of input
        '''
        return len(input[0])

    def getNumRows(self):
        '''
            This function returns the width and the height of the board
            Return:
                @width: the number of pieces
                @height: the number of rows, (2 * number of pieces) - 3
        '''
        height = (2 * self.numPieces) - 3  # Alternatively can use input length
        return height

    def getMidpoint(self):
        '''
            This function returns the midpoint of rows to determine possible moves
            Return:
                Rounded down value of (number of rows / 2)
        '''
        return math.floor(self.numRows / 2)

    # *********** DEBUGGING METHODS *********** #

    def printBoard(self):
        for row in self.board:
            print(row)


def movegen(inputBoard, player):
    gameBoard = Board(inputBoard)
    game = Game(gameBoard, player)
    newStates = game.moveGen()
    outputList = []

    for state in newStates:
        output = []
        for row in state.board:
            output.append("".join(row))
        outputList.append(output)

    print(outputList)


def oskaplayer(inputBoard, firstPlayer, depth):
    gameBoard = Board(inputBoard)  # create representation
    game = Game(gameBoard, firstPlayer, depth)  # create instance of game
    nextState = game.play()
    nextState.printBoard()
