from enum import Enum


class _Piece(Enum):
    empty = "[ ]"
    red = "[X]"
    yellow = "[O]"

    def __str__(self):
        return str(self.value)


class _Move(Enum):
    OUT_OF_BOUNDS = "Invalid input, please enter a number between 1 and "
    COL_FULL = "Invalid input, please enter a column that is not full"
    VALID = 2

    def __str__(self):
        return str(self.value)


class _Board(object):
    def __init__(self, dimCol, dimRow):
        self._GameBoard = [[_Piece.empty for x in range(dimCol)] for y in range(dimRow)]
        self._GameBoardFill = [len(self._GameBoard) - 1 for x in range(dimCol)]

    def printBoard(self):
        for i in range(len(self._GameBoard)):
            for j in range(len(self._GameBoard[0])):
                print(self._GameBoard[i][j], end='')
            print()

    def getColNum(self):
        return len(self._GameBoardFill)

    def getColFill(self, col):
        return self._GameBoardFill[col]

    def makeMove(self, team, col):
        fill = self._GameBoardFill
        if self.isValidMove(fill[col]):
            if team is _Piece.red:
                self._GameBoard[fill[col]][col] = _Piece.red
            else:
                self._GameBoard[fill[col]][col] = _Piece.yellow
            fill[col] -= 1
            return True
        return False

    def isValidMove(self, col):
        if col < 0 or col > self.getColNum():
            return _Move.OUT_OF_BOUNDS
        elif self._GameBoardFill[col] < 0:
            return _Move.COL_FULL
        else:
            return _Move.VALID


class _Player(object):
    def __init__(self, team, name):
        self._team = team
        self._name = name

    def __str__(self):
        return self._name + str(self._team)

    def getTeam(self):
        return self._team


class GameManager(object):
    def __init__(self, dim_col, dim_row):
        self._player1 = None
        self._player2 = None
        self._board = _Board(dim_col, dim_row)
        global COL
        COL = dim_col

    def mainLoop(self):
        board = self._board
        p1 = self._player1
        p2 = self._player2
        while True:
            board.printBoard()
            inp = self.playerInput(p1, board)
            board.makeMove(p1.getTeam(), inp)

    def playerInput(self, player, board):
        dim = self._board.getColNum()
        valid = False
        print(str(player) + ", which column do you wish to drop in?")
        while not valid:
            try:
                inp = int(input("Column: ")) - 1
                isValid = board.isValidMove(inp)
                if isValid is _Move.VALID:
                    return inp
                elif isValid is _Move.OUT_OF_BOUNDS:
                    print(str(isValid) + str(dim))
                else:
                    print(isValid)
            except ValueError:
                print("Invalid input, please enter a number")

    def run(self):
        self.login()

        self.mainLoop()

    def login(self):
        print("Player 1 please type your preferred name: ")
        p1Name = input("Name: ")
        print("Player 2 please type your preferred name: ")
        p2Name = input("Name: ")

        self._player1 = _Player(_Piece.red, p1Name)
        self._player2 = _Player(_Piece.yellow, p2Name)
