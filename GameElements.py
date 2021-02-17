from enum import Enum


class Piece(Enum):
	empty = "[ ]"
	red = "[R]"
	yellow = "[Y]"

	def __str__(self):
		return str(self.value)


class Board(object):
	def __init__(self, dim_col, dim_row):
		self._GameBoard = [[Piece.empty for x in range(dim_col)] for y in range(dim_row)]

	def printBoard(self):

		for i in range(len(self._GameBoard)):
			for j in range(len(self._GameBoard[0])):
				print(self._GameBoard[i][j], end='')
			print()
