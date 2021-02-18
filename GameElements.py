from enum import Enum


class _Piece(Enum):
    empty = "[ ]"
    red = "[X]"
    yellow = "[O]"

    def __str__(self):
        return str(self.value)


class _Board(object):
    def __init__(self, dimCol, dimRow):
        self._GameBoard = [[_Piece.empty for x in range(dimCol)] for y in range(dimRow)]
        self._GameBoardFill = [0 for x in range(dimCol)]

    def printBoard(self):
        for i in range(len(self._GameBoard)):
            for j in range(len(self._GameBoard[0])):
                print(self._GameBoard[i][j], end='')
            print()

    def getColNum(self):
        return len(self._GameBoardFill)


class _Player(object):
    def __init__(self, team, name):
        self._team = team
        self._name = name

    def __str__(self):
        return self._name + str(self._team)


class GameManager(object):
    def __init__(self, dim_col, dim_row):
        self._player1 = None
        self._player2 = None
        self._board = _Board(dim_col, dim_row)

    def mainLoop(self):
        while True:
            self._board.printBoard()
            inp = self.playerInput(self._player1, self._board.getColNum())

    def playerInput(self, player, dim):
        valid = False
        print(str(player) + ", which column do you wish to drop in?")
        while not valid:
            try:
                inp = int(input("Column: "))
                if inp > dim or inp <= 0:
                    print("Invalid input, please enter a number between 1 and " + str(dim))
                else:
                    return inp - 1
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
