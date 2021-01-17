from typing import Tuple, List
from player.player import Player


class Board:
    __BOARD_ROWS = 6
    __BOARD_COLS = 7

    def __init__(self):
        self.__board = self.__initialize_board()

    def __initialize_board(self) -> List[List]:
        """Returns an empty board matrix with a numbered header for the columns"""

        board_header = [list(map(str, range(1, 8)))]
        board_proper = [[" " for _ in range(self.__BOARD_COLS)] for _ in range(self.__BOARD_ROWS)]
        return board_header + board_proper

    def player_move(self, player: Player, col: str) -> None or Tuple[int, int]:
        """Updates the board with the player symbol.

        Returns the board coordinates (row, col) for the player move.

        Performs validity check for column (and implicitly for row) input by user.

        Transforms user input into valid column index, and finds the valid row index"""

        if not self.__validate_column_input(col):
            print(f"{player.name}, you've entered an invalid column. Valid column numbers are 1 to 7.")
            return

        col = int(col) - 1
        last_free_row_idx = None
        for row_idx in range(1, self.__BOARD_ROWS + 1):
            if self.__board[row_idx][col] != " ":
                break
            else:
                last_free_row_idx = row_idx

        if not last_free_row_idx:
            print(f"{player.name}, this column is full. Choose another column.")
            return
        else:
            self.__board[last_free_row_idx][col] = player.symbol
            return last_free_row_idx, col

    def __validate_column_input(self, col: str) -> bool:
        """Checks if user column input is an integer and in the appropriate range"""

        try:
            col = int(col)
            if not 0 < col <= self.__BOARD_COLS:
                raise ValueError
            return True
        except ValueError:
            return False

    def draw_board(self, board_values) -> str:
        """Creates string representation from given board values"""

        rows = (self.__BOARD_ROWS * 2) + 1
        cols = (self.__BOARD_COLS * 2) + 1
        header_separator = "="
        row_separator = "-"
        vertical_separator = "|"
        newline = "\n"
        board = ""
        for row in range(rows):
            for col in range(cols):
                if row % 2 == 0:
                    if col % 2 == 0:
                        board += vertical_separator
                    else:
                        col_idx = col // 2
                        row_idx = row // 2
                        board += board_values[row_idx][col_idx]
                else:
                    if row == 1:
                        board += header_separator
                    else:
                        board += row_separator
            board += newline
        return board

    @property
    def board(self):
        return self.__board


class Symbols:
    def __init__(self):
        self.__colors = ["red", "yellow"]
        self.__symbols = ["O", "X"]

    def get_player_color(self, color: str) -> None or Tuple[str, str]:
        """Returns the chosen colors for the players if valid"""

        if color not in self.__colors:
            return

        color_other = None
        if color == "red":
            color_other = "yellow"
        elif color == "yellow":
            color_other = "red"

        return color, color_other

    def get_player_symbol(self, color: str) -> Tuple[str, str]:
        """Returns symbols for the players corresponding to the chosen colors"""

        symbol, symbol_other = None, None
        if color == "red":
            symbol, symbol_other = self.__symbols[0], self.__symbols[1]
        elif color == "yellow":
            symbol, symbol_other = self.__symbols[1], self.__symbols[0]

        return symbol, symbol_other





