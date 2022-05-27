from minefield import MineField
from os import system
from time import time, sleep


def main():
    """
    Run the minesweeper game
    """
    print("MINESWEEPER")


    minefield = MineField(30, 30)
    start_time = time()

    while not minefield.minefield_complete()[0]:

        minefield.print_board()

        try:
            row, col = map(int, [input("ROW: "), input("COL: ")])
        except Exception:
            print("Invalid Input Type")
            continue

        if minefield.is_valid(row, col) and ([row, col] not in minefield.opened_squares):
            squares = minefield.open_squares(row, col)
            for sq in squares: minefield.opened_squares.append(sq)

        elif not ((0 <= row < minefield.rows) and (0 <= col < minefield.cols)):
            print(f"Invalid Position: ROW must be in the range 0 <= r < {minefield.rows}"
                                f"and COL must be in the range 0 <= c < {minefield.cols}")

        elif [row, col] in minefield.opened_squares:
            print(f"Square {row, col} is already open")

    if minefield.minefield_complete()[1]:
        print("You hit a mine")

    else:
        print(f"You cleared the minefield in {(time() - start_time) // 1000} seconds!")


if __name__ == "__main__":
    main()
