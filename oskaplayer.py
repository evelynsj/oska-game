# oskaplayer(['wwww','---','--','---','bbbb'],'w',2)


class Board:
    def __init__(self, input):
        self.numPieces = self.getNumPieces(input)  # number of pieces
        self.width, self.height = self.getDimensions()  # width and height of board
        self.board = self.makeBoard(input)  # parsed game board
        self.winner = None  # TODO: winning player method

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

    # *********** CONSTRUCTOR METHODS *********** #

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
                @height: the number of rows, (2 * self.numPieces) - 3
        '''
        width = self.numPieces
        height = (2 * self.numPieces) - 3  # Alternatively can use input length
        return width, height

    # *********** DEBUGGING METHODS *********** #

    def printBoard(self):
        for row in self.board:
            print(row)


def oskaplayer(inputBoard, firstPlayer, depth):
    gameBoard = Board(inputBoard)  # create representation
