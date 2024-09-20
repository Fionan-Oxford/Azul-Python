import random
from azul_backend.tiles import ColourTile, P1Tile
from textwrap import dedent


class TileBag:
    """
    This class is for management of the TileBag in the game
    Only Factory should need to access this class.
    Each TileBag has 100 tiles, 20 of each colour
    The tilebag also manages control of the P1Tile.

    Once the bag is empty, it is refilled with another 100 tiles

    Methods:
        draw_tile: Draw a random tile from the bag
        take_p1_tile: Take the P1 tile
        __len__: The total number of tiles in the bag
        __str__: Summary information about the TileBag
        __repr__: Detailed information about the TileBag
    """

    # All protected. Only Factory should need to access this class,
    # and only for the purposes of drawing tiles, for which there
    # are public methods.
    __tile_bag: list[ColourTile]
    __size: int
    __p1_size: int

    def __init__(self) -> None:
        """
        This is the constructor for the TileBag class
        It fills the tile bag with 100 tiles and shuffles them
        It records that the P1 tile has not been taken
        """
        self._reset_tile_bag()
        # The game starts with the player1 tile possessed by the _tiles object
        # The below is used to ensure player1 tile is released to the game

        # In reality I don't hold a P1 tile. Just count when one has been released
        self.__p1_size = 1  # 1 means the player1 tile has yet to be released

    # Protected as used internally only, but can imagine a use case for
    # a derived class using this in a different way. #Misuse does not
    # break the game, so no need to make it private.
    def _reset_tile_bag(self) -> None:
        """
        This method fills the tile bag back to 100 tiles
        It is automatically called at initialisation, and when the bag is empty
        All tiles within the bag are randomly shuffled.
        """
        NO_OF_COLOUR_TILES: int = 20  # Makes it easy for future changes

        self.__tile_bag = [
            ColourTile("blue"),
            ColourTile("yellow"),
            ColourTile("red"),
            ColourTile("black"),
            ColourTile("white"),
        ] * NO_OF_COLOUR_TILES
        self.__size = (
            NO_OF_COLOUR_TILES * 5
        )  # Maintain a count of the number of tiles in the bag

        random.shuffle(self.__tile_bag)  # Shuffle the bag

    def draw_tile(self) -> ColourTile:
        """
        This method draws a random ColourTile from the bag and returns it
        """
        if self.__size > 0:
            self.__size -= 1
        else:
            # Bag automagically refills if empty (a simplification of this implementation)
            self._reset_tile_bag()
            self.__size -= 1

        return self.__tile_bag.pop()

    def take_p1_tile(self) -> P1Tile:
        """
        This method takes the P1Tile and returns it
        It can only be called once per instance.
        """
        if self.__p1_size == 1:
            self.__p1_size = 0
        else:
            raise ValueError(
                "You have already taken the P1 tile. You cannot take it again."
            )

        return P1Tile()

    def __len__(self) -> int:
        """
        The total number of tiles in the bag
        """
        return self.__size

    def __str__(self) -> str:
        """
        This method is for pretty printing the TileBag object
        It returns summary information about the TileBag
        """
        return f"TileBag: ColourTiles[{self.__size}] P1Tile[{self.__p1_size}]"

    def __repr__(self) -> str:
        """
        This method returns a string detailing every tile
        Within the tile bag
        """
        bag_contents_string = ""

        # List comprehension to get the display text of each tile
        tile_strings = [tile.get_display_text() for tile in self.__tile_bag]
        bag_contents_string = ", ".join(tile_strings)

        return dedent(
            f"""\
            Player1 Tile: {self.__p1_size}
            No of ColourTiles: {self.__size}
            TileBag [{bag_contents_string}]"""
        )
