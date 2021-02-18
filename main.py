import GameElements
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--row", help="The row dimension. Defaults to 6", type=int, default=6)
    parser.add_argument("-c", "--col", help="The column dimension. Defaults to 7", type=int, default=7)
    args = parser.parse_args()
    DIM_ROW = args.row
    DIM_COL = args.col

    gameManager = GameElements.GameManager(DIM_COL, DIM_ROW)

    gameManager.run()


if __name__ == '__main__':
    main()
