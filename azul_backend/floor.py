## File: floor.py
## Date: 2024-02-20
## This module creates the floor class

from collections import deque
from azul_backend.tiles import P1Tile, ColourTile
from textwrap import dedent


class Floor:
    """
    This is the floor class
    It is used to represent the floor of a player
    It is used to place tiles on the floor and to present score penalties
    """

    __player_floor: deque[ColourTile | P1Tile | None]
    __floor_size: int

    def __init__(self) -> None:
        """
        This is the constructor if the floor class
        """
        # Intiialising tile holding data structure.
        self.__player_floor = deque([None] * 7, maxlen=7)
        self.__floor_size = 0

    def show_floor(self) -> tuple[ColourTile | P1Tile | None, ...]:
        """
        This method returns the floor
        """
        # Making the deque immutable
        return tuple(self.__player_floor)

    def add_to_floor(self, tiles: deque[P1Tile | ColourTile]) -> None:
        """
        This method adds a tile to the floor
        If there is no space, no tile is added
        argument: tiles: deque[P1Tile | ColourTile]|P1Tile | ColourTile
                you can add a single tile or a deque of tiles
        """
        floor = self.__player_floor
        if isinstance(tiles, (P1Tile, ColourTile)):
            tiles = deque([tiles])  # Convert to deque if single tile

        # If we have space on the floor we can add it,
        # Otherwise tile is lost to oblivion
        for tile in tiles:
            if floor[-1] is None:
                floor.pop()
                floor.appendleft(tile)
                self.__floor_size += 1

    @property
    def floor_penalty(self) -> int:
        """
        Returns the penalty for the floor
        """
        # The penalty for each tile is cumulative
        CUMULATIVE_PENALTY = {
            0: 0,
            1: -1,
            2: -2,
            3: -4,
            4: -6,
            5: -8,
            6: -11,
            7: -14,
        }

        return CUMULATIVE_PENALTY[self.__floor_size]

    @property
    def check_player1_tile(self) -> bool:
        """
        Checks the floor for the next player1 tile
        """
        for tile in self.__player_floor:
            if tile is not None:  # None tyle won't have a get_tile_type method
                if tile.get_tile_type() == "player1":
                    return True
        return False

    def get_p1_tile(self) -> P1Tile:
        """
        Returns the P1 tile if found on the floor,
        Removing it from the floor if so.
        If not found, error is raised
        """
        for tile in self.__player_floor:
            if tile is not None:  # None tile won't have a get_tile_type method
                if tile.get_tile_type() == "player1":
                    self.__player_floor.remove(tile)
                    self.__floor_size -= 1
                    return tile
        raise RuntimeError("No P1 tile found on the floor")

    def clean_floor(self) -> None:
        """
        Clears the floor, removing all tiles and penalties
        """
        self.__player_floor = deque([None] * 7, maxlen=7)
        self.__floor_size = 0

    def __str__(self) -> str:
        """
        This method returns a string representation of the floor
        """
        pf = self.__player_floor

        return dedent(
            f"""\
    floor: {pf[0]} {pf[1]} {pf[2]} {pf[3]} {pf[4]} {pf[5]} {pf[6]}
    size: {self.__floor_size}
    penalty: {self.floor_penalty}
    """
        )
