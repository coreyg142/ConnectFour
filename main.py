import GameElements

DIM_ROW = 6
DIM_COL = 7


def main():
    board = GameElements.Board(DIM_COL, DIM_ROW)

    board.printBoard()


if __name__ == '__main__':
    main()
