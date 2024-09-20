## File: patternlines.py
## Date: 2024-02-20
## This module creates the patternline class

# For making the dictionaries immutable when showing contents to the user
from types import MappingProxyType
from collections import deque
from azul_backend.tiles import P1Tile, ColourTile
from textwrap import dedent


class PatternLines:
    """
    This is the PatternLines class
    It is used to represent the pattern lines of a player
    It is used to place tiles on the pattern lines, and to select tiles for wall tiling

    Public Methods:
        place_on_patternlines: places the supplied tiles on the pattern lines
        show_pattern_lines: returns the pattern lines as an immutable dictionary
        is_patternline_complete: returns True if the pattern line is complete
        get_possible_moves: returns a tuple of possible moves for a specified line
        select_tile_for_wall: selects a tile from the pattern line to be placed on the wall
        clean_pattern_lines: clears any empty spaces on the pattern lines
    """

    # Unlike tiles, I wish to allow the contents of my dictionary to change
    __player_patternlines: dict[str, deque[ColourTile | None]]
    __line_colours: dict[str, str]

    def __init__(self) -> None:
        """
        This is the constructor of the PatternLines Class
        """
        # Intiialising tile holding data structure.
        # I have chosen deque, as I only need to pop/push from the ends
        # And the maxlen parameter will allow me to limit the size of each structure
        self.__player_patternlines = {
            "line1": deque([None], maxlen=1),
            "line2": deque([None] * 2, maxlen=2),
            "line3": deque([None] * 3, maxlen=3),
            "line4": deque([None] * 4, maxlen=4),
            "line5": deque([None] * 5, maxlen=5),
        }

        self.__line_state = {
            "line1": "",
            "line2": "",
            "line3": "",
            "line4": "",
            "line5": "",
        }

    def place_on_patternlines(
        self, hand: deque[ColourTile | P1Tile] | ColourTile, line: str
    ) -> deque[ColourTile | P1Tile]:
        """
        Place the supplied tiles on the pattern line.
        Any excess tiles are returned for placing on the floor.
        The P1 tile is returned for placing on the floor
        ARGS:
            hand: deque[ColourTile | P1Tile] - The tiles to be placed on the pattern line
            line: str - The line to place the tiles on
        """
        if isinstance(hand, (ColourTile)):
            hand = deque([hand])  # Convert to deque if single tile

        # Is hand empty
        if not hand:
            raise ValueError("You have not passed any tiles")

        pattern_line = self.__player_patternlines[line]
        # If there's already tiles on the pattern line, you can only add tiles of the same type and colour
        # Need to be careful not to check the Player1 tile

        # If the pattern line is full, you can't add any more tiles
        if self.__line_state[line] == "full":  # If the line is full
            raise ValueError("This pattern line is full")

        if self.__line_state[line] != "":  # If the pattern line is not empty
            for tile in hand:
                if tile.get_tile_type() != "player1":
                    if tile.get_tile_type() != self.__line_state[line]:
                        raise ValueError(
                            "You can only add tiles of the same type to the pattern line"
                        )

        return_hand: deque[ColourTile | P1Tile] = deque([], maxlen=16)
        # We have space on the pattern line so append from the right
        for tile in hand:
            if (
                pattern_line[0] is None
                and tile.get_tile_type() != "player1"
                and isinstance(tile, ColourTile)
            ):
                # Checking if this is a Colour_Tile to satisy MyPy
                pattern_line.popleft()  # take off an empty space
                pattern_line.append(tile)
                if pattern_line[0] is not None:
                    self.__line_state[line] = "full"
                else:
                    self.__line_state[line] = (
                        tile.get_tile_type()
                    )  # mark as full or reserved of a particular colour
            else:
                return_hand.append(tile)

        return return_hand

    def show_pattern_lines(
        self,
    ) -> MappingProxyType[str, tuple[ColourTile | None, ...]]:
        """
        This method returns the pattern lines of the specified player
        In the form of a MappingProxyType (an immutable dictionary).
        Internal deques are converted to tuples for immutability
        """
        tuple_dict_patternlines = {
            key: tuple(value)
            for key, value in self.__player_patternlines.items()
        }

        # I have chosen to use MappingProxyType to make the dictionary immutable
        return MappingProxyType(tuple_dict_patternlines)

    def is_patternline_complete(self, line: str) -> bool:
        """
        This method checks if a pattern line is complete and returns a boolean
        """
        if self.__line_state[line] == "full":
            return True
        else:
            return False

    def get_possible_moves(self, line: str) -> tuple[str, ...]:
        """
        returns possible moves for a specific line, from the perspective of the patternline only
        .i.e does not take into account wall tiles
        """
        possible_moves = tuple(["blue", "yellow", "red", "black", "white"])
        if self.__line_state[line] == "":
            return possible_moves
        elif self.__line_state[line] == "full":
            return ()
        else:
            return tuple([self.__line_state[line]])

    def select_tile_for_wall(self, line: str) -> ColourTile | None:
        """
        This method selects a tile from the pattern line to be placed on the wall
        The method returns the selected tile
        The place on the pattern line is then set to None
        The pattern line must be complete to present a tile,
        If the pattern line is not complete, the method will return None
        """
        # Not raising an error, but instead doing nothing if the pattern line is not complete
        if self.is_patternline_complete(line):
            pattern_line = self.__player_patternlines[line]
            tile = pattern_line[-1]
            pattern_line[-1] = None  # Remove the tile from the pattern line
            return tile
        else:
            return None

    def clean_pattern_lines(self) -> None:
        """
        This method "cleans" the indicated the pattern line
        Any pattern line with an empty space in the rightmost position is cleared
        """
        none_list: deque[ColourTile | None]  # Keeps MyPy happy

        for line in self.__player_patternlines:
            if self.__player_patternlines[line][-1] is None:

                none_list = deque(
                    [None for _ in self.__player_patternlines[line]]
                )
                self.__player_patternlines[line] = none_list
                self.__line_state[line] = ""

    def __str__(self) -> str:
        """
        This method returns a string representation of the patternline
        """
        pl = self.__player_patternlines
        return dedent(
            f"""\
    Pattern lines:
    {pl['line1'][0]}
    {pl['line2'][0]} {pl['line2'][1]}
    {pl['line3'][0]} {pl['line3'][1]} {pl['line3'][2]}
    {pl['line4'][0]} {pl['line4'][1]} {pl['line4'][2]} {pl['line4'][3]}
    {pl['line5'][0]} {pl['line5'][1]} {pl['line5'][2]} {pl['line5'][3]} {pl['line5'][4]}
    """
        )
