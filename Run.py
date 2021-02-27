import GameElements
import Discord
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", help="Run game in command line or start Discord bot.\n"
                                     "\"cl\" for command line, \"dc\" for Discord", type=str, choices=["cl", "dc"])
    parser.add_argument("-r", "--row", help="The row dimension. Defaults to 6", type=int, default=6)
    parser.add_argument("-c", "--col", help="The column dimension. Defaults to 7", type=int, default=7)
    args = parser.parse_args()
    DIM_ROW = args.row
    DIM_COL = args.col
    mode = args.mode

    if mode == "cl":
        gameManager = GameElements.GameManagerTUI(DIM_COL, DIM_ROW)
        gameManager.run()
    elif mode == "dc":
        Discord.run(DIM_ROW, DIM_COL)


if __name__ == '__main__':
    main()
