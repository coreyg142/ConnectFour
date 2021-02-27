from enum import Enum
import Discord

class Piece(Enum):
    empty = "[ ]"
    red = "[X]"
    yellow = "[O]"

    def __str__(self):
        return str(self.value)


class Move(Enum):
    OUT_OF_BOUNDS = "Invalid input, please enter a number between 1 and "
    COL_FULL = "Invalid input, please enter a column that is not full"
    VALID = 2

    def __str__(self):
        return str(self.value)


class Board(object):
    def __init__(self, dimCol, dimRow):
        self.row = dimRow
        self.col = dimCol
        self._GameBoard = [[Piece.empty for x in range(dimCol)] for y in range(dimRow)]
        self._GameBoardFill = [len(self._GameBoard) - 1 for x in range(dimCol)]

    def __str__(self):
        strOutp = ""
        for i in range(len(self._GameBoard)):
            for j in range(len(self._GameBoard[0])):
                if self._GameBoard[i][j] == Piece.red:
                    strOutp += '🔴'
                elif self._GameBoard[i][j] == Piece.yellow:
                    strOutp += '🟡'
                else:
                    strOutp += '⚪'
            strOutp += '\n'
        return strOutp

    def printBoard(self):
        for i in range(len(self._GameBoard)):
            for j in range(len(self._GameBoard[0])):
                print(self._GameBoard[i][j], end='')
            print()

    def getMaxCol(self):
        return self.col

    def getMaxRow(self):
        return self.row

    def makeMove(self, team, col):
        fill = self._GameBoardFill
        if self.isValidMove(fill[col]):
            if team is Piece.red:
                self._GameBoard[fill[col]][col] = Piece.red
            else:
                self._GameBoard[fill[col]][col] = Piece.yellow
            fill[col] -= 1
            return True
        return False

    def isValidMove(self, col):
        if col < 0 or col > self.col:
            return Move.OUT_OF_BOUNDS
        elif self._GameBoardFill[col] < 0:
            return Move.COL_FULL
        else:
            return Move.VALID

    def checkIfWinner(self):
        directions = [[1, 0], [1, -1], [1, 1], [0, 1]]
        maxRow = self.row
        maxCol = self.col
        board = self._GameBoard
        for d in directions:
            dx = d[0]
            dy = d[1]
            for x in range(maxRow):
                for y in range(maxCol):
                    lastX = x + 3 * dx
                    lastY = y + 3 * dy
                    if 0 <= lastX < maxRow and 0 <= lastY < maxCol:
                        piece = board[x][y]
                        if piece is not Piece.empty \
                                and piece == board[x + dx][y + dy] \
                                and piece == board[x + 2 * dx][y + 2 * dy] \
                                and piece == board[lastX][lastY]:
                            return True, piece

        return False, Piece.empty


class Player(object):
    def __init__(self, team, name):
        self._team = team
        self._name = name

    def __str__(self):
        return self._name + str(self._team)

    def getTeam(self):
        return self._team


class GameManagerDUI(object):

    def __init__(self, dim_col, dim_row):
        self._player1 = None
        self._player2 = None
        self.dimCol = dim_col
        self.dimRow = dim_row
        self._board = Board(dim_col, dim_row)

    def login(self, p1, p2):
        self._player1 = Player(Piece.red, p1)
        self._player2 = Player(Piece.yellow, p2)

    def getBoard(self):
        return self._board


class GameManagerTUI(object):

    def __init__(self, dim_col, dim_row):
        self._player1 = None
        self._player2 = None
        self.dimCol = dim_col
        self.dimRow = dim_row
        self._board = Board(dim_col, dim_row)

    def mainLoop(self):
        board = self._board
        p1 = self._player1
        p2 = self._player2
        isOver = False
        winner = Piece.empty
        while not isOver:
            self.handleInpMove(p1, board)
            isOver, winner = board.checkIfWinner()
            if isOver: break
            self.handleInpMove(p2, board)
            isOver, winner = board.checkIfWinner()

        board.printBoard()
        if winner is Piece.red:
            self.endGame(p1)
        else:
            self.endGame(p2)

    def playerInput(self, player, board):
        dim = self._board.getMaxCol()
        valid = False
        print(str(player) + ", which column do you wish to drop in?")
        while not valid:
            try:
                inp = int(input("Input: ")) - 1
                isValid = board.isValidMove(inp)
                if isValid is Move.VALID:
                    return inp
                elif isValid is Move.OUT_OF_BOUNDS:
                    print(str(isValid) + str(dim))
                elif isValid is Move.COL_FULL:
                    print(isValid)
            except ValueError:
                print("Invalid input, please enter a number")

    def resetBoard(self):
        self._board = Board(self.dimCol, self.dimRow)

    def handleInpMove(self, player, board):
        board.printBoard()
        inp = self.playerInput(player, board)
        board.makeMove(player.getTeam(), inp)

    def endGame(self, winner):
        print("{} has won the game!".format(winner))
        print("Would you like to play another?")
        inp = input("yes/no: ").lower()
        if inp == "yes":
            print("Resetting board and restarting... ")
            self.resetBoard()
            self.mainLoop()
        elif inp == "no":
            print("Thank you for playing!")

    def run(self):
        self.login()

        self.mainLoop()

    def login(self):
        print("Player 1 please type your preferred name: ")
        p1Name = input("Name: ")
        print("Player 2 please type your preferred name: ")
        p2Name = input("Name: ")

        self._player1 = Player(Piece.red, p1Name)
        self._player2 = Player(Piece.yellow, p2Name)
