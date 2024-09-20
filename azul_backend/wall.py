## File: wall.py
## Date: 2021-02-20
## This module creates the wall class

from types import MappingProxyType

# For making the dictionaries immutable when showing contents to the use

from collections import deque
from azul_backend.tiles import ColourTile
from textwrap import dedent


class Wall:
    """
    This is the wall class
    It is used to represent the wall of a player
    Public methods:
        show_wall: returns the wall as an immutable dictionary
        move_tile_to_wall: moves a supplied Colour_Tile to the specified line on the wall
        get_possible_moves: returns a tuple of possible moves for a specified line

    Properties:
        is_game_over: returns True if this wall indicates the game is over
    """

    __player_wall: dict[str, deque[ColourTile | None]]

    def __init__(self) -> None:
        """
        This is the constructor for the Wall class
        """
        WALL_SIZE = 5

        # Could use a loop to fill this structure, however I feel laying it
        # out like this makes it clearer
        self.__player_wall = {
            "line1": deque([None] * WALL_SIZE, maxlen=WALL_SIZE),
            "line2": deque([None] * WALL_SIZE, maxlen=WALL_SIZE),
            "line3": deque([None] * WALL_SIZE, maxlen=WALL_SIZE),
            "line4": deque([None] * WALL_SIZE, maxlen=WALL_SIZE),
            "line5": deque([None] * WALL_SIZE, maxlen=WALL_SIZE),
        }

    def show_wall(self) -> MappingProxyType[str, tuple[ColourTile | None, ...]]:
        """
        This method returns the wall as an immutable dictionary
        (MappingProxyType) from types
        """
        tuple_dict_wall = {
            key: tuple(value) for key, value in self.__player_wall.items()
        }
        return MappingProxyType(tuple_dict_wall)

    def move_tile_to_wall(self, tile: ColourTile, line: str) -> int:
        """
        This method moves a supplied Colour_Tile to the specified line on the wall
        Line must be in the format of "line*"
        The position on the line is determined by the tile.
        An integer is returned to indicate the score of the move
        Args:
            tile: ColourTile - The tile to be moved to the wall
            line: str - The line on the wall to move the tile to (e.g "line1")
        """
        self._check_colour_tile(tile)  # Check that tile is a valid ColourTile
        self._check_line_string(line)  # Check that line is a valid input.

        wall = self.__player_wall
        wall_line = wall[line]
        wall_position = tile.wall_position(line)

        if wall_line[wall_position] is None:
            # Only place the tile on the wall if the position is empty
            wall_line[wall_position] = tile
        else:
            # If the position is already occupied, raise an error
            # This would only occur due to a failure in PaternLine class not checking the wall was free
            # before moving a tile to the wall
            raise RuntimeError(
                f"{tile} - Invalid move, position already occupied on wall"
            )

        return self._score_move(tile, line)

    def get_possible_moves(self, line: str) -> tuple[str, ...]:
        """
        This method returns a tuple of possible moves for a line
        e.g ("blue", "yellow", "red", "black", "white")
        If all moves are possible
        """
        self._check_line_string(line)  # Check that line is a valid input.

        possible_moves = ["blue", "yellow", "red", "black", "white"]

        for tile in self.__player_wall[line]:
            if tile is not None:
                possible_moves.remove(tile.get_tile_type())

        return tuple(possible_moves)

    @property
    def is_game_over(self) -> bool:
        """
        Returns True if this wall indicates the game is over
        i.e a horizontal line is complete
        """
        # Check if the  player has completed a horizontal line
        for i in range(1, 6):
            if not None in self.__player_wall["line" + str(i)]:
                return True
        # If not, return False
        return False

    def _check_line_string(self, line: str) -> None:
        """
        This method checks if the line string is in the correct format
        """
        if line not in ["line1", "line2", "line3", "line4", "line5"]:
            raise ValueError(
                f"{line} - Invalid line string, must be in format of line*, where * is a number between 1 and 5 inclusive."
            )

    def _check_colour_tile(self, tile: ColourTile) -> None:
        """
        This method checks if the tile is a valid ColourTile
        """
        # Deliberately not using isinstance() so
        # Parent class P1Tile is not accepted
        if not type(tile) is ColourTile:
            raise ValueError(f"{tile} - Invalid tile, must be a ColourTile")

    def _score_move(
        self,
        tile: ColourTile,
        line: str,
    ) -> int:
        """
        This method returns the score made from the placing
        of a single tile onto the wall
        """
        self._check_line_string(line)  # Check that line is a valid input.

        return_score = 0  # what is returned at the end
        basic_score = 1  # Starting from 1, as a tile on it's own scores 1

        # Get the horizontal and vertical sweep scores from the helper methods
        horizontal_sweep_score = self._score_move_horizontal(tile, line)
        vertical_sweep_score = self._vertical_sweep_score(tile, line)

        if horizontal_sweep_score and vertical_sweep_score == 1:
            # This is a tile on it's own, return just basic_score
            return_score = basic_score
        elif horizontal_sweep_score == 1 and vertical_sweep_score > 1:
            # This is a tile that scored just from the vertical sweep
            return_score = vertical_sweep_score
        elif vertical_sweep_score == 1 and horizontal_sweep_score > 1:
            # This is a tile that scored just from the horizontal sweep
            return_score = horizontal_sweep_score
        else:
            # This is a tile that scored from both the vertical and horizontal sweep
            return_score = horizontal_sweep_score + vertical_sweep_score

        return return_score

    def _score_move_horizontal(self, tile: ColourTile, line: str) -> int:
        """
        This method returns the "horizontal sweep" score made from the placing
        of a single tile onto the wall.
        It is a support method for _score_move()
        """
        horizontal_sweep_score: int = 0
        wall = self.__player_wall
        wall_line = wall[line]
        wall_position = tile.wall_position(line)
        # Check Horizontal
        # I have to be careful here, in left/rightmost position as I cannot search outside the bounds of the wall
        for i in range(wall_position, 5):
            if wall_line[i] is not None:
                horizontal_sweep_score += 1
            else:
                break
        return horizontal_sweep_score

    def _vertical_sweep_score(self, tile: ColourTile, line: str) -> int:
        """
        This method returns the "vertical sweep" score made from the placing
        of a single tile onto the wall.
        It is a support method for _score_move()
        """
        vertical_sweep_score: int = 0
        wall = self.__player_wall
        wall_position = tile.wall_position(line)

        vertical_dict = {
            "line1": 0,
            "line2": 1,
            "line3": 2,
            "line4": 3,
            "line5": 4,
        }

        # Check Vertical
        # I have to be careful here, in top/bottom as I cannot search outside the bounds of the wall
        for i in range(vertical_dict[line], 5):
            if wall["line" + str(i + 1)][wall_position] is not None:
                vertical_sweep_score += 1
            else:
                break

        for i in range(vertical_dict[line], 0, -1):
            # Note the max function here, as I cannot search outside the bounds of the wall
            if wall["line" + str(max(i, 1))][wall_position] is not None:
                vertical_sweep_score += 1
            else:
                break
        return vertical_sweep_score

    def __str__(self) -> str:
        """
        This method returns a detailed string representation of the game
        """
        pw = self.__player_wall
        return dedent(
            f"""\
            Wall:
            {pw['line1'][0]} {pw['line1'][1]} {pw['line1'][2]} {pw['line1'][3]} {pw['line1'][4]}
            {pw['line2'][0]} {pw['line2'][1]} {pw['line2'][2]} {pw['line2'][3]} {pw['line2'][4]}
            {pw['line3'][0]} {pw['line3'][1]} {pw['line3'][2]} {pw['line3'][3]} {pw['line3'][4]}
            {pw['line4'][0]} {pw['line4'][1]} {pw['line4'][2]} {pw['line4'][3]} {pw['line4'][4]}
            {pw['line5'][0]} {pw['line5'][1]} {pw['line5'][2]} {pw['line5'][3]} {pw['line5'][4]}
            """
        )
