from random import randint as rand


class MineField:
    """
    A representation of the minefield in which the mines are placed
    """

    def __init__(self, rows: int, cols: int):
        self.rows, self.cols = rows, cols
        self.minefield, self.num_mines = self.lay_mines()
        self.opened_squares = []
        self.hit_mine = False

    def __repr__(self):
        return self.minefield

    def __str__(self):
        return f"Current Board: {self.minefield}\n" \
               f"Dimentions: {self.rows}x{self.cols}\n" \
               f"Opened Squares: {self.opened_squares}"

    def lay_mines(self, p_mine=0.15) -> tuple:
        """
        Add the mines to the minefield and determine the number of mines adjacent to a square
        """

        # Create empty minefield
        minefield = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

        # Keep count of the number of mines
        num_mines = 0

        # Add mines and update surrounding square's mine counts
        for row in range(self.rows):
            for col in range(self.cols):

                # Add mine to minefield
                if rand(0, 100) < p_mine * 100:

                    minefield[row][col] = 5
                    num_mines += 1

                    # List of squares that potentially border the mine
                    potential_squares = [(row + 1, col), (row - 1, col),
                                         (row, col + 1), (row, col - 1),
                                         (row + 1, col + 1), (row + 1, col - 1),
                                         (row - 1, col + 1), (row - 1, col - 1)]

                    # For each square, check if it exists (within the bounds of the minefield), and if is not a mine.
                    # Then increment its value by 1 to signify another bordering mine
                    for square in potential_squares:
                        r, c = square
                        if self.is_valid(r, c):
                            if minefield[r][c] != 5:
                                minefield[r][c] += 1

        return minefield, num_mines

    def is_valid(self, r:int, c:int) -> bool:
        """
        Checks if a value is within the boundaries of the minefield
        """

        return (0 <= r) and (r < self.rows) and (0 <= c) and (c < self.cols)

    def open_squares(self, row: int, col: int) -> [bool, list]:
        """
        After a square is selected, open all squares that are within the boundaries. If the square is a mine, return
        True. Otherwise, return a list of all squares to be opened
        """

        # Check if the square was a mine
        if self.minefield[row][col] == 5:
            return True

        # Create a set containing all the squares to be opened
        _opened_squares = []

        # Check if a square is a boundary square
        def _is_boundary(r, c):
            return self.is_valid(r, c) and self.minefield[r][c] != 0

        # Algorithm for finding which squares need to be opened
        def _open_squares(r, c):

            _opened_squares.append([r, c])

            if _is_boundary(r, c):
                return True

            for _dir in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                next_square = [_dir[0] + r, _dir[1] + c]
                if self.is_valid(*next_square) and (next_square not in _opened_squares):
                    _open_squares(*next_square)

        _open_squares(row, col)
        return _opened_squares

    def minefield_complete(self) -> tuple:
        """
        Check if all non-mine squares have been opened
        """

        return (len(self.opened_squares) == self.rows * self.cols - self.num_mines) or self.hit_mine, self.hit_mine

    def game_over(self):
        """
        In the event that the user hits a mine, force the minefield_complete function to return True
        """

        self.hit_mine = True

    def print_board(self):
        """
        Print the board row by row. For each unopened square, print an X. For an opened square, print the number of
        adjacent mines
        """

        for row in range(self.rows):
            line = ""

            for col in range(self.cols):
                sq = self.minefield[row][col]
                line += str(sq) if [row, col] in self.opened_squares else "X"
                line += " "

            print(line)
