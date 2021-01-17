from termcolor import colored
from typing import Tuple
from board.board import Board, Symbols
from player.player import Player


class Game:
    __PLAYERS_NUMBERS = [2, 1]

    def __init__(self):
        self.__board = Board()
        self.__symbols = Symbols()
        self.__player_one = Player()
        self.__player_two = Player()

    def play(self) -> None:
        """Contains main program logic"""

        print(self.__welcome_screen())

        self.__player_one.number = self.__PLAYERS_NUMBERS.pop()
        self.__player_two.number = self.__PLAYERS_NUMBERS.pop()

        self.__get_player_name(self.__player_one)
        self.__get_player_name(self.__player_two)

        self.__assign_players_colors()
        self.__colorize_players_names()
        self.__assign_players_symbols()

        print(f"{self.__player_one.name}, you will play with {self.__player_one.symbol}.\n"
              f"{self.__player_two.name}, you will play with {self.__player_two.symbol}.\n"
              f"{self.__player_one.name} starts.")

        self.__game_loop()

    def __game_loop(self):
        """Player moves are handled by this function."""

        current_player = self.__player_one
        other_player = self.__player_two

        while True:
            print(self.__board.draw_board(self.__board.board))
            player_col_choice = input(f"{current_player.name}, choose a move: ")
            move_coordinates = self.__board.player_move(current_player, player_col_choice)
            if not move_coordinates:
                continue
            else:
                win = self.__has_won(current_player, move_coordinates)
                draw = (not win) and self.__have_drawn()
                if win or draw:
                    print(self.__board.draw_board(self.__board.board))
                    if win:
                        print(f"{current_player.name} has won!")
                        current_player.wins = 1
                    elif draw:
                        print("Game drawn!")

                    if not self.__continue_playing():
                        print(self.__statistics())
                        return
                    else:
                        self.__board = Board()

                else:
                    current_player, other_player = other_player, current_player

    @staticmethod
    def __welcome_screen() -> str:
        """Prints the welcoming message to the screen"""

        welcome_message = """
Welcome to this Connect 4 game.
The objective is to put four symbols next to each other on the board.
The connection can be by row, column, or diagonal.
Enjoy the game!
"""
        return welcome_message

    @staticmethod
    def __get_player_name(player: Player) -> None:
        """Retrieves player name from input"""

        name_input = input(f"Player {player.number}, enter your name: ")
        player.name = name_input

    def __assign_players_colors(self) -> None:
        """Assigns player colors from input. Possible colors are red and yellow"""

        symbol_color_submitted = input(f"Player {self.__player_one.name}, enter the desired color, red or yellow: ")

        colors_returned = self.__symbols.get_player_color(symbol_color_submitted)
        if not colors_returned:
            print(f"{self.__player_one.name}, this is not a valid color.")
            return self.__assign_players_colors()
        else:
            player_one_color, player_two_color = colors_returned
            self.__player_one.color = player_one_color
            self.__player_two.color = player_two_color

    def __colorize_players_names(self) -> None:
        """Player names receive the corresponding color"""

        self.__player_one.name = colored(self.__player_one.name, self.__player_one.color)
        self.__player_two.name = colored(self.__player_two.name, self.__player_two.color)

    def __assign_players_symbols(self) -> None:
        """Players get the symbols corresponding to the respective chosen color"""

        symbol_player_one, symbol_player_two = self.__symbols.get_player_symbol(self.__player_one.color)
        self.__player_one.symbol = colored(symbol_player_one, self.__player_one.color)
        self.__player_two.symbol = colored(symbol_player_two, self.__player_two.color)

    def __has_won(self, last_player: Player, last_move: Tuple[int, int]) -> bool:
        """Checks if a player has won.
        Starting from the last move position, the function checks whether the player has connected four
        by checking all directions, while checking for the validity of the indices.

        If board border or a different value than the player's symbol is encountered, the orientation is either
        reversed to check the other corresponding direction, or a new vector is chosen, and the "connect four" counter
        is reset.

        When all orientations are checked and the player has not won, the function returns 'None', otherwise 'True'."""

        def are_valid_coordinates(row, col):
            return 1 <= row < len(self.__board.board) and 0 <= col < len(self.__board.board[1])

        directions_increments = {
            "up": (-1, 0),
            "down": (+1, 0),
            "left": (0, -1),
            "right": (0, +1),
            "up left": (-1, -1),
            "down right": (+1, +1),
            "up right": (-1, +1),
            "down left": (+1, -1),

        }

        connect_four_counter = 1
        orientation = 0
        current_row, current_col = last_move
        symbol = last_player.symbol
        for direction, increments in directions_increments.items():
            orientation += 1

            while True:
                inc_row, inc_col = increments
                current_row, current_col = current_row + inc_row, current_col + inc_col

                if not are_valid_coordinates(current_row, current_col):
                    break
                current_symbol = self.__board.board[current_row][current_col]
                if current_symbol != symbol:
                    break

                connect_four_counter += 1

            if connect_four_counter >= 4:
                return True

            if orientation == 2:
                connect_four_counter = 1
                orientation = 0

            current_row, current_col = last_move

    def __have_drawn(self):
        """ Checks the top non-header row in the board and returns True if no free spots are available"""
        return self.__board.board[1].count(" ") == 0

    def __statistics(self) -> str:
        """Returns overall game statistics for the current session"""

        overall_winner = None
        if self.__player_one.wins > self.__player_two.wins:
            overall_winner = self.__player_one.name
        elif self.__player_one.wins < self.__player_two.wins:
            overall_winner = self.__player_two.name
        else:
            overall_winner = "draw"

        message = f"{self.__player_one.name} wins: {self.__player_one.wins}\n" \
                  f"{self.__player_two.name} wins: {self.__player_two.wins}\n" \
                  f"Overall winner: {overall_winner}."
        return message

    def __continue_playing(self):
        """The players can choose whether to continue playing the current session, or to quit the game"""

        response = input("Do you want to continue playing? Press 'y' to continue or 'n' to quit: ")
        try:
            if response not in ("y", "n"):
                raise ValueError
            return True if response == "y" else False
        except ValueError:
            return self.__continue_playing()

