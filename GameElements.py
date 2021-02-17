from enum import Enum


class Token(Enum):
	empty = "[ ]"
	red = "[R]"
	yellow = "[Y]"

	def __str__(self):
		return str(self.value)


class Board(object):
	def __init__(self, dim):
		self._GameBoard = [[Token.empty for x in range(dim)] for y in range(dim)]

	def printBoard(self):

		for i in range(len(self._GameBoard)):
			for j in range(len(self._GameBoard[0])):
				print(self._GameBoard[i][j], end='')
			print()
