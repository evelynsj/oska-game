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
    "j": 0
}
JUMP_DOWN_LEFT = {
    "description": "jump down left",
    "i": 2,
    "j": -2
}
JUMP_DOWN_RIGHT = {
    "description": "jump down right",
    "i": 2,
    "j": 2
}
JUMP_DOWN_DIAG_RIGHT = {
    "description": "jump down diagonal right",
    "i": 2,
    "j": 1
}
JUMP_DIAG_LEFT_DOWN = {
    "description": "jump diagonal left down",
    "i": 2,
    "j": -1
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
    "j": 0
}
JUMP_UP_LEFT = {
    "description": "jump up left",
    "i": -2,
    "j": -2
}
JUMP_UP_RIGHT = {
    "description": "jump up right",
    "i": -2,
    "j": 2
}
JUMP_UP_DIAG_RIGHT = {
    "description": "jump up diagonal right",
    "i": -2,
    "j": 1
}
JUMP_DIAG_LEFT_UP = {
    "description": "jump diagonal left up",
    "i": -2,
    "j": -1
}

class Game:
    def __init__(self, board, firstPlayer):
        self.state = board  # current state of the game
        self.player = firstPlayer
        self.winner = None  # TODO: winning player method

    def play(self):
        # TODO: while no winner, keep making moves and taking turns
        self.moveGen()

    # *********** MOVE GENERATOR METHODS *********** #

    def moveGen(self):
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
        newStates = []
        for move in possibleMoves:
            newI = i + move["i"]
            newJ = j + move["j"]

            newState = copy.deepcopy(self.state)
            newBoard = newState.board
            newBoard[i][j] = EMPTY_SPACE
            newBoard[newI][newJ] = self.player

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
        # width and height of board TODO: prob don't need width
        self.width, self.numRows = self.getDimensions()
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

    def getDimensions(self):
        '''
            This function returns the width and the height of the board
            Return:
                @width: the number of pieces
                @height: the number of rows, (2 * number of pieces) - 3
        '''
        width = self.numPieces
        height = (2 * self.numPieces) - 3  # Alternatively can use input length
        return width, height

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


def oskaplayer(inputBoard, firstPlayer, depth):
    gameBoard = Board(inputBoard)  # create representation
    game = Game(gameBoard, firstPlayer)  # create instance of game
    game.play()
