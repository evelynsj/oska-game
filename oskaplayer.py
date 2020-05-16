# oskaplayer(['wwww','---','--','---','bbbb'],'w',2)

import math

# ***** CHARACTER CONSTANTS ***** #
WHITE = 'w'
BLACK = 'b'
EMPTY_SPACE = '-'

# ***** WHITE MOVES ***** #
MOVE_DOWN = "move down"
MOVE_DOWN_LEFT = "move down left"
MOVE_DOWN_RIGHT = "move down right"
JUMP_DOWN = "jump down"
JUMP_DOWN_LEFT = "jump down left"
JUMP_DOWN_RIGHT = "jump down right"
JUMP_DOWN_DIAG_RIGHT = "jump down diagonal right"
JUMP_DIAG_LEFT_DOWN = "jump diagonal left down"

# ***** BLACK MOVES ***** #
MOVE_UP = "move up"
MOVE_UP_LEFT = "move up left"
MOVE_UP_RIGHT = "move up right"
JUMP_UP = "jump up"
JUMP_UP_LEFT = "jump up left"
JUMP_UP_RIGHT = "jump up right"
JUMP_UP_DIAG_RIGHT = "jump up diagonal right"
JUMP_DIAG_LEFT_UP = "jump diagonal left up"


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
        for i in range(self.state.numRows):
            for j in range(len(board[i])):
                if (board[i][j] == self.player):
                    self.possibleMoves(i, j)
                    # TODO: make moves, return list of boards

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
