# I originally used a MappingProxyType for each tile,
# however I realised that a tyle class would give me an opportunity
# to use inheritance, explore dunder methods and polymprphism.
# Using a class also allowed me tailor how to print the object

# This is probably overkill for this project, but I wanted to explore
# These concepts and learn how to use them in a project

# Allowing users to specify any colour is hazardous, as they can choose
# colour strings that do not exist and may cause errors later.
# However I want users to have flexibility in their choice of colours,
# as different GUI packages use different strings


# Tile structures
# I have made the design choice for the tiles to manage the possible wall positions
# and not the wall itself. This was to simplify the wall logic.
# Ordered and unchangeable, these are the only tiles in the game

from textwrap import dedent


class P1Tile:
    """
    This class is is used to represent the player 1 tile

    Args:
        display_colour (str): The colour of the tile, for display purposes
                    If not supplied, the default is "white".
                    The choice of colour is up to the user, depending on their preference and GUI tools

        display_text (str): OPTIONAL: The text to display on the tile, for display purposes
                    If default then "[ 1 ]" is used

    Methods:
        get_tile_type: Get the tile type
        set_display_colour: Set the display colour of the tile
        set_display_text: Set the display text of the tile
        __str__: This method is for pretty printing the object
        __repr__: Detailed string representation, for debugging.
        __eq__: Is this instance equal to another object?
    """

    # Chose private. Messing with this could break the game
    __tile_type: str  # The inherent type of the tile

    # Chose protected. I want to allow inheritance, but not allow direct access to these attributes
    _display_colour: str  # The colour of the tile, for display purposes. Allows for flexibility in GUI tools. Default is for tkinter
    _display_text: str  # The display text of the tile, again allows flexibility in GUI tools, print function etc

    def __init__(
        self, display_colour: str = "white", display_text: str = "[ 1 ]"
    ) -> None:
        """Initialise the tile type, display colour and display text"""

        self.__tile_type = "player1"

        # I will allow users to specify colour and string, as this are for display purposes
        # and will not affect the game. The choice is up to the user depending on their preference
        # and what GUI tools they are using. The default works for tkinter, as this suits my GUI choice
        self._display_colour = display_colour
        self._display_text = display_text

    def get_tile_type(self) -> str:
        """Get the tile type in the form of a string"""
        return self.__tile_type

    # The below methods allow people to change the display colour and text, if they want to tailor
    # Presentation within a GUI.
    def set_display_colour(self, display_colour: str) -> None:
        """Set the display colour of the tile as a string"""
        if not isinstance(display_colour, str):
            raise ValueError(
                f"{display_colour} is not valid - You must enter a string for the display colour"
            )
        self._display_colour = display_colour

    def set_display_text(self, display_text: str) -> None:
        """Set the display text of the tile as a string"""
        if not isinstance(display_text, str):
            raise ValueError(
                f"{display_text} is not valid - You must enter a string for the display text"
            )
        self._display_text = display_text

    def get_display_colour(self) -> str:
        """Get the display colour of the tile as a string"""
        return self._display_colour

    def get_display_text(self) -> str:
        """Get the display text of the tile as a string"""
        return self._display_text

        # This method tells Python how to print our object:

    def __str__(self) -> str:
        """
        This method is for pretty printing the P1Tile
        It returns the display text
        """
        return f"{self._display_text}"  # Return the display text

    def __repr__(self) -> str:
        """Detailed string representation, for debugging. Returns all internal attributes"""
        # Return the internal state of the object
        return f"Tile ({self.__tile_type!r}, {self._display_colour!r}, {self._display_text!r})"

    def __eq__(self, other: object) -> bool:
        """
        Is this instance equal to another object?
        Comparision with subclasses returns False
        """
        if (
            not type(other) is P1Tile
        ):  # I deliberatly do not want to compare to subclasses
            return NotImplemented

        # I only care about the tile type, colour and display text are for the user
        return self.__tile_type == other.get_tile_type()


class ColourTile(P1Tile):
    """
    This class is for the coloured tiles. It inherits from the P1_Tile class
    It has additional attributes and methods for the coloured tiles.
    Args:
        tile_type (str): The type of tile, chosen from the list of tiles
                    ["blue", "yellow", "red", "black", "white"]

        Optional:
        display_colour (str): The colour of the tile, for display purposes
                    If not supplied, an appropiate colour for tkinter is used, inferred
                    from the tile type.
        display_text (str): OPTIONAL: The text to display on the tile, for display purposes
                    If default then "[tile_type] is used"
    Methods:
        wall_position: Gives the valid wall positions for the tile
        __repr__: Detailed string representation, for debugging.
        __eq__: Is this instance equal to another object?
    """

    __tile_type: str  # The inherent type of the tile, "blue", "yellow", "red", "black", "white
    _display_colour: str  # Not to be confused with type. This is used for displaying in a GUI. Default used tkinter colours
    _display_text: str  # The display text of the tile, again allows flexibility in GUI tools, print function etc

    # Override the __init__ method
    def __init__(
        self,
        tile_type: str,
        display_colour: str = "default",
        display_text: str = "default",
    ) -> None:
        """Initialise the tile type, display colour and display text"""
        # Check that valid initialisation parameters have been entered
        if not isinstance(tile_type, str):
            raise ValueError(
                f"{tile_type} is not valid - You must enter a string for the tile type"
            )
        if not isinstance(display_colour, str):
            raise ValueError(
                f"{display_colour} is not valid - You must enter a string for the display colour"
            )
        if not isinstance(display_text, str):
            raise ValueError(
                f"{display_text} is not valid - You must enter a string for the display text"
            )

        # Check that a valid tile type has been entered
        if tile_type not in ["blue", "yellow", "red", "black", "white"]:
            raise ValueError(
                f"Invalid tile type {tile_type}, you must select from 'blue', 'yellow', 'red', 'black', 'white'"
            )

        self.__tile_type = tile_type

        if display_colour == "default":
            # If no colour is specified, use the tile type to infer the colour. Default colours are for tkinter GUI tools
            if tile_type == "blue":
                self._display_colour = "blue"
            elif tile_type == "yellow":
                self._display_colour = "yellow"
            elif tile_type == "red":
                self._display_colour = "red"
            elif tile_type == "black":
                self._display_colour = "aquamarine4"  # This is a dark green, easier to see than black
            elif tile_type == "white":
                self._display_colour = (
                    "azure1"  # This is a light blue, easier to see than white
                )
        else:
            # If a colour is specified, use that
            self._display_colour = display_colour

        if display_colour == "default":
            self._display_text = f"[{self.__tile_type}]"  # The default text is the tile type in square brackets
        else:
            self._display_text = display_text

    def wall_position(self, wall_line: str) -> int:
        """
        Returns the valid wall position for the tile
        For the specific wall line in the form of an int
        ["line1", "line2", "line3", "line4", "line5"]
        """
        # This was a design choice for simplicity. However, it's perhaps cleaner to have this logic
        # Performed by the wall module. As this functionality is only used there
        # This is a potential refactor for the future

        if wall_line not in ["line1", "line2", "line3", "line4", "line5"]:
            raise ValueError(
                f"{wall_line} is not a valid wall line, please use 'line1', 'line2', 'line3', 'line4', 'line5'"
            )

        blue_positions = {
            "line1": 0,
            "line2": 1,
            "line3": 2,
            "line4": 3,
            "line5": 4,
        }
        yellow_positions = {
            "line1": 1,
            "line2": 2,
            "line3": 3,
            "line4": 4,
            "line5": 0,
        }
        red_positions = {
            "line1": 2,
            "line2": 3,
            "line3": 4,
            "line4": 0,
            "line5": 1,
        }
        black_positions = {
            "line1": 3,
            "line2": 4,
            "line3": 0,
            "line4": 1,
            "line5": 2,
        }
        white_positions = {
            "line1": 4,
            "line2": 0,
            "line3": 1,
            "line4": 2,
            "line5": 3,
        }

        if self.__tile_type == "blue":
            return blue_positions[wall_line]
        elif self.__tile_type == "yellow":
            return yellow_positions[wall_line]
        elif self.__tile_type == "red":
            return red_positions[wall_line]
        elif self.__tile_type == "black":
            return black_positions[wall_line]
        elif self.__tile_type == "white":
            return white_positions[wall_line]
        else:
            raise ValueError("Invalid tile type")

    # Need to override this method, as __tile_type is private in parent class
    def get_tile_type(self) -> str:
        """Get the tile type in the form of a string"""
        return self.__tile_type

    # Overriding as there is a bit more to print for the coloured tiles
    def __repr__(self) -> str:
        """Detailed string representation, for debugging. Returns all internal data as a string"""
        # dedent used to remove leading whitespace
        return dedent(
            f"""\
            Coloured Tile
            tile_type: {self.__tile_type!r}
            display_colour: {self._display_colour!r}
            display_text: {self._display_text!r}
            wall_position: line1: {self.wall_position('line1')}
            wall_position: line1: {self.wall_position('line2')}
            wall_position: line1: {self.wall_position('line3')}
            wall_position: line1: {self.wall_position('line4')}
            wall_position: line1: {self.wall_position('line5')}
            """
        )

    def __eq__(self, other: object) -> bool:
        """
        Is this instance equal to another object?
        """
        if (
            not type(other) is ColourTile
        ):  # I deliberatly do not want to compare to parent class
            # i.e comparing to P1Tile would not return True
            return NotImplemented

        # I only care about the tile type, colour and display text are for the user
        return self.__tile_type == other.__tile_type
