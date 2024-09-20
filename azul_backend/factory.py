from azul_backend.tilebag import TileBag
from azul_backend.tiles import ColourTile, P1Tile
from typing import cast
from textwrap import dedent

# I strongly considered to make the number of factories an argument,
# To allow easy extension for non 2 player versions of the game.
# I decided that a fixed number was cleaner. It is easy to change if needed
# Perhaps using a list of each factory of configurable length.


class Factory:
    """
    This Class is responsible for factory data and actions

    It should not be instantiated directly by users of the library.
    Please use the Game class to create a new game.

    Methods:
        reset_factory: Reset the factories at the start of each factory offer round to have 4 tiles each
        replace_p1_tile: Return the player1 tile to the centre of the table
        isempty: Returns True if all the factories (and centre of table) are empty
        show_factory: Show the contents of the specified factory or the centre of the table
        take_factory_tiles: Take all tiles of a specified colour from a specified factory
        __str__: Pretty print the class contents
    """

    __my_tiles: TileBag
    _factory1: list[ColourTile]
    _factory2: list[ColourTile]
    _factory3: list[ColourTile]
    _factory4: list[ColourTile]
    _factory5: list[ColourTile]
    _centretable: list[ColourTile | P1Tile]

    def __init__(self) -> None:
        """
        This is the constructor for the Factory class
        It creates a new tile bag and sets up the
        factories and the centre of the table
        for the first turn.
        """
        self.__my_tiles = TileBag()  # Create a new tile bag

        self._centretable = []
        self._factory1 = []
        self._factory2 = []
        self._factory3 = []
        self._factory4 = []
        self._factory5 = []
        # I initialise theses as empty, so that the isempty() check in reset_factory works

        self.reset_factory()

        # The starting player tile is placed into the centre of the table
        # at the start of the game. In later turns the replace_P1Tile method is used
        self._centretable.append(self.__my_tiles.take_p1_tile())

    # Private. Exposes mutable factories. Internal use only
    def __get_factory(
        self, factory: int
    ) -> list[ColourTile | P1Tile] | list[ColourTile]:
        # this type hint is a little messy. In effect. Factories return just ColourTile.
        # CentreTable returns a ColourTile or P1Tile
        """
        This method returns the specidied (factory=1-5) or the centre of the table (factory=0) as a list
        It exposes the mutable factories. It is for internal use only
        """
        if factory == 0:
            return self._centretable
        elif factory == 1:
            return self._factory1
        elif factory == 2:
            return self._factory2
        elif factory == 3:
            return self._factory3
        elif factory == 4:
            return self._factory4
        elif factory == 5:
            return self._factory5
        else:
            raise ValueError("Invalid factory number")

    def reset_factory(self) -> None:
        """
        This method resets the factories.
        It fills them with four random tiles from the Tilebag
        It should be called at the start of the Factory Offer Round
        """
        if not self.isempty:
            raise ValueError(
                "The factories are not empty, it is not an appropiate time to reset the factories"
            )

        self._factory1 = self._draw_factory_tiles()
        self._factory2 = self._draw_factory_tiles()
        self._factory3 = self._draw_factory_tiles()
        self._factory4 = self._draw_factory_tiles()
        self._factory5 = self._draw_factory_tiles()

    def _draw_factory_tiles(self) -> list[ColourTile]:
        """
        This method draws a list of four tiles for each factory.
        It is used by the reset_factory method
        """
        return [self.__my_tiles.draw_tile() for _ in range(4)]

    def replace_p1_tile(self, replaced_p1_tile: P1Tile) -> None:
        """
        This method place the player1 tile into the centre of the table.
        It should be used in the Preparing for Next Round Phase
        """
        if not isinstance(replaced_p1_tile, P1Tile):
            raise ValueError(f"{replaced_p1_tile} is not the player1 tile")

        if self._centretable:
            raise ValueError(
                "The centre of the table is not empty, it is not an appropiate time to replace the player1 tile"
            )

        self._centretable.append(replaced_p1_tile)

    @property
    def isempty(self) -> bool:
        """
        This property returns True if all the factories (and centre of table) are empty
        The only exception is the player1 tile in the centre of the table, which is not counted
        """

        if len(self._centretable) == 1 and type(self._centretable[0]) is P1Tile:
            # If there is only one tile in the Centre of the table, and that is the P1Tile
            # We just check if the factories are empty
            return not (
                self._factory1
                or self._factory2
                or self._factory3
                or self._factory4
                or self._factory5
            )
        else:
            # Else we check everything, including centre of table.
            return not (
                self._centretable
                or self._factory1
                or self._factory2
                or self._factory3
                or self._factory4
                or self._factory5
            )

    def show_factory(
        self, factory_number: int
    ) -> tuple[ColourTile | P1Tile, ...]:
        """
        This method returns the tiles in a specified factory as a tuple
        factory_number: 1-5 corresponds to the factory number
        factory_number: 0 corresponds to the centre of the table
        """
        return tuple(self.__get_factory(factory_number))  # Ensures immutability

    def _move_to_centre(self, factory_number: int) -> None:
        """
        This method moves all the remaining tiles from a factory to the centre of the table
        It is played after a player has selected tiles from a factory
        """
        if factory_number < 0 or factory_number > 5:
            raise ValueError(
                "Invalid factory number, please choose a number between 1 and 5"
            )

        factory = self.__get_factory(factory_number)
        self._centretable.extend(factory)
        factory.clear()

    def take_factory_tiles(
        self, factory_number: int, tile_type: str
    ) -> list[ColourTile | P1Tile] | list[ColourTile]:
        """
        This method returns any and all tiles from a specified factory of a specified
        colour, removing it from the factory at the same time.
        1-5 corresponds to the factory number
        0 corresponds to the centre of the table

        If retrieving from the centre of the table, the player1 tile is also returned if available
        """
        if tile_type not in ["blue", "yellow", "red", "black", "white"]:
            raise ValueError(
                f"{tile_type} Is an Invalid tile type, please choose from blue, yellow, red, black or white"
            )

        filtered_tiles: list[ColourTile | P1Tile] = []
        # The factory is returned as a list of ColourTiles, or if from the centre of the table,
        # a list of ColourTiles and P1Tile
        factory = self.__get_factory(factory_number)

        # The centre of the table also returns the player1 tile if available
        for tile in factory:
            if tile.get_tile_type() == tile_type or type(tile) is P1Tile:
                filtered_tiles.append(tile)

        # This helper method checks that valid tiles have been selected
        self._validate_take_factory_tiles(
            filtered_tiles, factory_number, tile_type
        )

        # Factory is updated to remove the tiles of the specified colour
        factory = cast(list[ColourTile | P1Tile], factory)
        # Messy cast to keep MyPy Happy.
        # Factory can be centre of table, so this is correct

        for tile in filtered_tiles:
            factory.remove(tile)

        if (
            factory_number > 0
        ):  # No need to move to centre of the table if we are taking from the centre of the table
            self._move_to_centre(
                factory_number
            )  # remaining tiles are moved to the centre of the table

        return filtered_tiles

    def _validate_take_factory_tiles(
        self,
        tiles: list[ColourTile | P1Tile] | list[ColourTile],
        factory_number: int,
        tile_type: str,
    ) -> None:
        """
        Used to check that a valid "take_factory_tiles" call is made.
        Raises error if no tiles are taken, or if only the P1Tile is taken
        This is used internally as a helper method for take_factory_tiles
        """
        # If no tiles are removed, raise an error
        if not tiles:
            raise ValueError(
                f"Not tile(s) of colour {tile_type} exists in factory {factory_number}"
            )

        # If ONLY the player1 tile is removed,
        if (
            any(tile.get_tile_type() == "player1" for tile in tiles)
            and len(tiles) == 1
        ):
            raise ValueError(
                f"Not tile(s) of colour {tile_type} exists in the centre of the table"
            )

    def __str__(self) -> str:
        """
        This method returns a string representation of the factory floor
        """
        cot_string = " ".join(map(str, self._centretable))
        f1_string = " ".join(map(str, self._factory1))
        f2_string = " ".join(map(str, self._factory2))
        f3_string = " ".join(map(str, self._factory3))
        f4_string = " ".join(map(str, self._factory4))
        f5_string = " ".join(map(str, self._factory5))

        return dedent(
            f"""\
        Factory 1: {f1_string}
        Factory 2: {f2_string}
        Factory 3: {f3_string}
        Factory 4: {f4_string}
        Factory 5: {f5_string}
        Centre of the table: {cot_string}
        """
        )
