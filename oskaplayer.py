# oskaplayer(['wwww','---','--','---','bbbb'],'w',2)

import math

WHITE = 'w'
BLACK = 'b'
EMPTY_SPACE = '-'
MOVE_DOWN = "move down"
MOVE_DOWN_LEFT = "move down left"
MOVE_DOWN_RIGHT = "move down right"


class Game:
    def __init__(self, board, firstPlayer):
        self.state = board  # current state of the game
        self.player = firstPlayer
        self.winner = None  # TODO: winning player method

    def play(self):
        # TODO: while no winner, keep making moves and taking turns
        self.movegen()

    # *********** MOVE GENERATOR METHODS *********** #

    def movegen(self):
        board = self.state.board
        for i in range(self.state.numRows):
            for j in range(len(board[i])):
                if (board[i][j] == self.player):
                    self.possibleMoves(i, j)
                    # TODO: make moves, return list of boards

    def possibleMoves(self, i, j):
        moves = []
        if (self.player == WHITE):
            whiteMoves = self.moveWhite(i, j)
            if (whiteMoves):
                moves = moves + whiteMoves
            # TODO: jump forward
        elif (self.player == BLACK):  # TODO
            pass

        print(moves)

    def moveWhite(self, i, j):
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
