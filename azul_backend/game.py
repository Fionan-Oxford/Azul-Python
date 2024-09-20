## File: game.py
## Date: 2024-02-27
## This module creates the game class. It is the facade of all other classes in the backend
## And is the only one that should be instantiated by the user/frontend

# -ASSUMPTIONS AND SIMPLIFICATIONS------------------------------------------------------------
# I have made a number of simplifications to the game, and I have also made a number of assumptions.

# 1. There are only 2 players, and thus always five factories
# 2. The game will always start with player1.
#    The very first move, of placing the "starting player" marker into the centre of the table is
#    done automatically
# 3. At the end of the game, there are NO additional scoring points for having completed a row or column of
#    or maxed out the tiles of a specific colour
# 4. There is no variant play in this implementation
# 5. There is no "lid of the box". Any tiles that are removed from the game are simply deleted
# 6. If the tile bag is empty (100 tiles have been drawn), the bag magically reffils itself to 100. There
#    is no lid of the box for the bag to refill from. Thus it is possibe for more than 100 colour tiles to be in play
# 7. There is no means to reset a completed game. You need to create a new game object

# -HOW TO USE----------------------------------------------------------------------------------
# How to use the game class

# Much of the AZUL game is automated here, such as the entirety of the "Wall-Tiling" and "Prepare for Next Round" phases.
# Play starts with Player 1, and the game will change players. Any factory offers are made for the current player.
# To play the game, the user must
# 1. Make a factory offer (select tiles from a factory or the centre of the table) using the make_factory_offer method
# 2. Place the selected tiles on a pattern line using the place_on_patternlines method
#    There are occasions where there are no valid moves, in which case the game will automatically drop the tiles to the floor
#    and change the player
#    To detect this, you can check the contents of the hand after making a factory offer, or keep track of the moves this round
#    Or check the current player.

# The game will automatically advance to the next phase when the current phase is complete, and will auto`matically
# change the player when the current player's turn is complete.

# The game will also automatically determine the starting player for the next round, and will automatically
# apply the score penalty from the floor tiles at the end of the round.

# The game will also automatically determine if the game is over, and will automatically end the game if it is.

# To see the current state of the game, the user can call the following "show" methods
# These methods show immutabel information regarding the game
# 1. show_game_state - returns the current game state
# 2. show_hand - returns the tiles in the hand of the current player, i.e post factory offer and pre pattern line placement
# 3. show_current_player - returns the current player
# 4. show_factory - returns the tiles in a factory or centre of the table as a tuple
# 5. show_pattern_lines - returns the pattern lines of the specified player
# 6. show_floor - returns the floor of the specified player
# 7. show_wall - returns the wall of the specified player
# 8. show_score - returns the score of the specified player

# There are also a number of interesting public counters
# 1. moves_this_round - returns the number of moves made this round
# 2. rounds_played - returns the number of rounds played
# 3. moves_this_game - returns the number of moves made this game

# These are for display purposes and aren't critical to game function.

# -TESTING------------------------------------------------------------------------------
# I made a jupyter notebook for unit tests - test.ipynb

# -GUI----------------------------------------------------------------------------------
# I created a tkinter GUI for testing purposes which integrates using the above stated methods. Please see AzulGui.py.

from typing import Any, cast

# For making the dictionaries immutable when showing contents to the user
from types import MappingProxyType
from textwrap import dedent
from collections import deque

from azul_backend.factory import Factory
from azul_backend.tiles import P1Tile, ColourTile
from azul_backend.states import GameState
from azul_backend.wall import Wall
from azul_backend.floor import Floor
from azul_backend.patternlines import PatternLines


class Game:
    """
    This is the backend for the Azul Game
    This is the facacde of all other classes in the backend
    And is the only one that should be instantiated by the user/frontend

    Public Methods:
        SHOW METHODS
        show_game_state: Returns the current game state
        show_hand: Returns the tiles in the hand of the current player
        show_current_player: Returns the current player
        show_factory: Returns the tiles in a factory or centre of the table as a tuple
        show_pattern_lines: Returns the pattern lines of the specified player
        show_floor: Returns the floor of the specified player
        show_wall: Returns the wall of the specified player
        show_score: Returns the score of the specified player

        PLAY METHODS
        make_factory_offer: Selects tiles of a particular colour from a factory or centre of the table
        place_on_patternlines: Places the tiles in hand onto the specified pattern line of the current player

    Public Variables:
        moves_this_round: The number of moves made this round
        rounds_played: The number of rounds played
        moves_this_game: The number of moves made this game
    """

    # Class Constants to represent the players
    PLAYER_1: int = 1
    PLAYER_2: int = 2

    # These public variables aren't used for gameplay,
    # but offer interesting progress stats
    moves_this_round: int
    rounds_played: int
    moves_this_game: int

    # Private Variables
    # There are methods to access necessary information
    __player1score: int
    __player2score: int
    __my_factories: Factory
    __gamestate: GameState
    __current_player: int
    __hand: list[ColourTile | P1Tile] | list[ColourTile]
    __player1_patternlines: PatternLines
    __player2_patternlines: PatternLines
    __player1_floor: Floor
    __player2_floor: Floor
    __player1_wall: Wall
    __player2_wall: Wall

    def __init__(self) -> None:
        """
        This is the constructor for the Game class
        It also initializes the game, starting from the Factory Offer phase.

        It will always start with player1. The very first move, of placing the
        "starting player" marker into the centre of the table is done automatically
        by the factory class

        Once initialised, the game is ready to be played. Proceed from player 1
        By making a factory offer.
        """
        self.__my_factories = Factory()  # Create a new factory floor of 5 tiles
        self.__gamestate = GameState(1)  # Start with the factory offer phase
        self.__current_player = self.PLAYER_1  # Start with player1
        self.__player1score = 0
        self.__player2score = 0
        self.moves_this_round = 0
        self.rounds_played = 0
        self.moves_this_game = 0
        self.__hand = cast(list[ColourTile | P1Tile] | list[ColourTile], [])
        # This is an absolute mess, but lets me create the list object AND keep MyPy Happy.
        # I am effectiviely creating an empty list of type ColourTile or ColourTile/P1Tile or empty
        # I could have used a list of Any, but I wanted to keep the type hinting as specific as possible

        # The hand of the current player starts empty,
        # it's max possible is 16 (3 tiles from each factory plus P1 tile in Centre of table)
        self.__player1_patternlines = PatternLines()
        self.__player2_patternlines = PatternLines()
        self.__player1_floor = Floor()
        self.__player2_floor = Floor()
        self.__player1_wall = Wall()
        self.__player2_wall = Wall()

    def show_game_state(self) -> GameState:
        """
        This method returns the current game state
        as an enum (enumeration)
        FACTORY_OFFER = 1
        WALL_TILING = 2
        PREPARING_FOR_NEXT_ROUND = 3
        GAMEOVER = 4
        """
        return self.__gamestate

    def show_hand(self) -> tuple[ColourTile | P1Tile, ...]:
        """
        This method returns the tiles in the hand of the current player.
        The "hand" represents tiles picked from a factory offer, but not
        yet placed on a pattern line
        """
        return tuple(self.__hand)

    def show_current_player(self) -> int:
        """
        This method returns the current player as an int
        PLAYER_1 = 1
        PLAYER_2 = 2
        """
        return self.__current_player

    def show_factory(
        self, factory_number: int
    ) -> tuple[ColourTile | P1Tile, ...]:
        """
        This method returns the tiles in a factory or centre of the table as a tuple
        It is for display purposes only
        Please note that the factory number is 1-based
        Calling it with 0 will show the centre of the table

        centre of the table: factory_number = 0
        factory 1: factory_number = 1
        factory 2: factory_number = 2
        factory 3: factory_number = 3
        factory 4: factory_number = 4
        factory 5: factory_number = 5
        """
        return_tuple: tuple[ColourTile | P1Tile, ...] = (
            self.__my_factories.show_factory(factory_number)
        )  # Keeps MyPy happy
        return return_tuple

    def show_pattern_lines(
        self, player: int
    ) -> MappingProxyType[str, tuple[ColourTile | None, ...]]:
        """
        This method returns the pattern lines of the specified player
        In the form of a MappingProxyType (an immutable dictionary)
        """
        if player == 1:
            return self.__player1_patternlines.show_pattern_lines()
        elif player == 2:
            return self.__player2_patternlines.show_pattern_lines()
        else:
            raise ValueError("Invalid player number")

    def show_floor(self, player: int) -> tuple[ColourTile | P1Tile | None, ...]:
        """
        This method returns the floor of the specified player
        """
        if player == 1:
            return self.__player1_floor.show_floor()
        elif player == 2:
            return self.__player2_floor.show_floor()
        else:
            raise ValueError("Invalid player number")

    def show_wall(
        self, player: int
    ) -> MappingProxyType[str, tuple[ColourTile | None, ...]]:
        """
        This method returns the wall of the specified player
        """
        if player == 1:
            return self.__player1_wall.show_wall()
        elif player == 2:
            return self.__player2_wall.show_wall()
        else:
            raise ValueError("Invalid player number")

    def show_score(self, player: int) -> int:
        """
        This method returns the score of the specified player
        """
        if player == 1:
            return self.__player1score
        elif player == 2:
            return self.__player2score
        else:
            raise ValueError("Invalid player number")

    def make_factory_offer(
        self, factory_number: int, tile_type: str | ColourTile
    ) -> None:
        """
        Selects tiles of a particular colour from a factory or centre of the table
        Tiles are held "in hand" (internal memory) until they are places on patternlines.
        factory_number is 1-based, 0 is the centre of the table
        If there is no space on the patternlines to complete the move. The tiles will be placed on the floor

        Args:
            factory_number (int): The number of the factory to take tiles from,
                0 = centre of the table, 1-5 = factory number
            tile_type (str | ColourTile): The type of tile to take from the factory
                tile_type can be a string denoting colout, e.g 'black'
                or a ColourTile object
        """
        self._check_phase(GameState.FACTORY_OFFER)
        # Are we in the Factory Offer phase?

        if self.__hand:
            raise ValueError(
                "You must place the tiles you've selected on your pattern lines before selecting more tiles from the factory"
            )
        else:
            # I found it forgiving to allow the user to pass a string or a ColourTile object
            if type(tile_type) is ColourTile:
                self.__hand = self.__my_factories.take_factory_tiles(
                    factory_number, tile_type.get_tile_type()
                )
            elif isinstance(tile_type, str):
                self.__hand = self.__my_factories.take_factory_tiles(
                    factory_number, tile_type
                )
            else:
                raise ValueError(
                    f"{tile_type} - Invalid tile type, use either a string or a ColourTile object"
                )

        for tile in self.__hand:
            if not type(tile) is P1Tile:
                if not self._is_move_possible(
                    cast(ColourTile, tile)
                ):  # Keeps MyPy happy (already checked for P1Tile)
                    self._forced_move()  # Automatically drop the tiles to the floor and change the player
                    break

    def place_on_patternlines(self, line: str) -> None:
        """
        This method places the tiles in thehand onto the specified pattern line of the current player
        It is only playable after "make_factory_offer" has been called within the factory offer phase.
        If this the last move of the round, the game will advance to the wall tiling phase
        Else the current player changes
        """
        self._check_phase(GameState.FACTORY_OFFER)
        # Are we in the Factory Offer phase?

        floor_tiles: deque[ColourTile | P1Tile] = deque()
        if self.__hand:
            if not self._is_move_valid(line):
                raise ValueError("Invalid move, please select a different line")

            if self.__current_player == self.PLAYER_1:

                floor_tiles = self.__player1_patternlines.place_on_patternlines(
                    deque(self.__hand), line
                )
                if floor_tiles:
                    self.__player1_floor.add_to_floor(floor_tiles)
            else:
                floor_tiles = self.__player2_patternlines.place_on_patternlines(
                    deque(self.__hand), line
                )
                if floor_tiles:
                    self.__player2_floor.add_to_floor(floor_tiles)

            self.__hand.clear()
            self.moves_this_round += 1
            self.moves_this_game += 1
        else:
            raise ValueError(
                "You must select tiles from the factory before placing them on your pattern lines"
            )

        if self.__my_factories.isempty:
            self._wall_tiling()  # If factories are empty advance to wall tiling phase
        else:
            self._change_player()  # Change the player after the move

    def _is_move_valid(self, line: str) -> bool:
        """
        This method checks if a chosen move on the patternline is a valid.
        """
        if self.show_current_player() == self.PLAYER_1:
            pattern_lines = self.__player1_patternlines
            wall = self.__player1_wall
        else:
            pattern_lines = self.__player2_patternlines
            wall = self.__player2_wall

        if not self.__hand:
            raise RuntimeError("Hand is empty")

        wall_p_moves = wall.get_possible_moves(line)
        pl_p_moves = pattern_lines.get_possible_moves(line)

        for tile in self.__hand:
            if (
                tile.get_tile_type() != "player1"
            ):  # Could combine two "if" but I feel this is more readable
                if (
                    tile.get_tile_type() in wall_p_moves
                    and tile.get_tile_type() in pl_p_moves
                ):
                    return True
            else:
                continue
        return False

    def _forced_move(self) -> None:
        """
        If a player males a factory offer, and there are no possible moves, this method will be called on their behalf.
        It automatically drops tiles to the floor and changes the player.
        """
        if self.__current_player == self.PLAYER_1:
            self.__player1_floor.add_to_floor(deque(self.__hand))
        else:
            self.__player2_floor.add_to_floor(deque(self.__hand))

        self.__hand.clear()
        self.moves_this_round += 1
        self.moves_this_game += 1

        if self.__my_factories.isempty:
            self._wall_tiling()  # If factories are empty advance to wall tiling phase
        else:
            self._change_player()  # Change the player after the move

    def _change_player(self) -> None:
        """
        Change Player
        """
        if self.show_current_player() == self.PLAYER_1:
            self.__current_player = self.PLAYER_2
        else:
            self.__current_player = self.PLAYER_1

    def _wall_tiling(self) -> None:
        """
        Performs the wall tiling phase
        Before advancing to the prepare for next round phase
        Or completing the game
        """
        self._check_phase(GameState.FACTORY_OFFER)
        # Are we in the Factory Offer phase?
        self.__gamestate = GameState.WALL_TILING  # Advance to wall tiling

        lines = ["line1", "line2", "line3", "line4", "line5"]

        for line in lines:
            p1_t = self.__player1_patternlines.select_tile_for_wall(line)
            p2_t = self.__player2_patternlines.select_tile_for_wall(line)
            if p1_t:  # Perform wall tiling for player1
                self.__player1score += self.__player1_wall.move_tile_to_wall(
                    p1_t, line
                )
            if p2_t:  # Perform wall tiling for player2
                self.__player2score += self.__player2_wall.move_tile_to_wall(
                    p2_t, line
                )

        self._apply_score_penalty()  # Apply the score penalty from floor tiles

        if self.is_game_over:
            self.__gamestate = GameState.GAMEOVER
        else:
            self._prepare_for_next_round()  # Advance to the prepare for next round phase

    def _apply_score_penalty(self) -> None:
        """
        This method applies the score penalty to both players
        """
        # Score from floor is a negative value
        new_score_1 = self.__player1score + self.__player1_floor.floor_penalty
        new_score_2 = self.__player2score + self.__player2_floor.floor_penalty

        self.__player1score = max(new_score_1, 0)
        self.__player2score = max(new_score_2, 0)

    def _is_move_possible(self, tile: ColourTile) -> bool:
        """
        Returns true if there is a move possible to ANY pattern line
        """
        if self.show_current_player() == self.PLAYER_1:
            pattern_lines = self.__player1_patternlines
            wall = self.__player1_wall
        else:
            pattern_lines = self.__player2_patternlines
            wall = self.__player2_wall

        lines = ["line1", "line2", "line3", "line4", "line5"]
        for line in lines:
            if tile.get_tile_type() in pattern_lines.get_possible_moves(
                line
            ) and tile.get_tile_type() in wall.get_possible_moves(line):
                return True
        return False

    def _check_phase(self, phase: GameState) -> None:
        """
        This method checks if the game is in the specified phase
        It returns an error if not
        """
        if not self.__gamestate == phase:
            raise RuntimeError(
                f"Out of phase, this move can only be played in the {phase.name} phase, it is currently the {self.__gamestate.name} phase"
            )

    def _prepare_for_next_round(self) -> None:
        """
        This method prepares the game for the next round
        """
        self._check_phase(GameState.WALL_TILING)
        # Are we in the Wall_tiling phase?
        self.__gamestate = GameState.PREPARING_FOR_NEXT_ROUND
        # Advance to the preparing for next round phase

        # Decide who the starting player will be, and return P1 Tile to the centre of the table
        if self.__player1_floor.check_player1_tile:
            self.__current_player = self.PLAYER_1
            tile = self.__player1_floor.get_p1_tile()
            self.__my_factories.replace_p1_tile(tile)

        elif self.__player2_floor.check_player1_tile:
            self.__current_player = self.PLAYER_2
            tile = self.__player2_floor.get_p1_tile()
            self.__my_factories.replace_p1_tile(tile)

        else:
            raise RuntimeError(
                "Cannot determine from player floors who the next round's starting player will be"
            )

        # Clean floor, clean patternlines, refill factory
        self.__player1_floor.clean_floor()
        self.__player2_floor.clean_floor()
        self.__player1_patternlines.clean_pattern_lines()
        self.__player2_patternlines.clean_pattern_lines()
        self.__my_factories.reset_factory()
        self.rounds_played += 1
        self.moves_this_round = 0
        self.__gamestate = GameState.FACTORY_OFFER

    @property
    def is_game_over(self) -> bool:
        """
        Returns True if the game is over.
        Game ends when either player has
        completed a horizontal line on their wall
        """
        if self.__player1_wall.is_game_over or self.__player2_wall.is_game_over:
            return True
        return False

    def __repr__(self) -> str:
        """
        This method returns a detailed string representation of the game
        """
        p1pl = self.__player1_patternlines
        p1w = self.__player1_wall
        p1f = self.__player1_floor
        p2pl = self.__player2_patternlines
        p2w = self.__player2_wall
        p2f = self.__player2_floor
        mf = self.__my_factories

        # dedent() was producing strange behaviour, so I used a multiple string approach
        return (
            f"**************** Round {self.rounds_played} *****************\n"
            f"********* Phase  {self.__gamestate.name} *********\n"
            f"Current player: {self.__current_player}\n"
            f"Player1 score: {self.__player1score}\n"
            f"Player2 score: {self.__player2score}\n"
            f"Moves this round: {self.moves_this_round}\n"
            f"Rounds played: {self.rounds_played}\n"
            f"Moves this game: {self.moves_this_game}\n"
            f"{str(mf)}\n"
            f"=========PLAYER1 SUMMARY==========\n"
            f"Score: {self.__player1score}\n"
            "-------------------------------------------------------------\n"
            f"{str(p1pl)}\n"
            "-------------------------------------------------------------\n"
            f"{str(p1w)}\n"
            "-------------------------------------------------------------\n"
            f"{str(p1f)}\n"
            f"=========PLAYER2 SUMMARY==========\n"
            f"Score: {self.__player2score}\n"
            "-------------------------------------------------------------\n"
            f"{str(p2pl)}\n"
            "-------------------------------------------------------------\n"
            f"{str(p2w)}\n"
            "-------------------------------------------------------------\n"
            f"{str(p2f)}\n"
        )

    def __str__(self) -> str:
        """
        This method returns a summary string representation of the game
        """
        return dedent(
            f"""\
            **************** Round {self.rounds_played} *****************
            ********* Phase  {self.__gamestate.name} *********
            Current player: {self.__current_player}
            Player1 score: {self.__player1score}
            Player2 score: {self.__player2score}
            Moves this round: {self.moves_this_round}
            Rounds played: {self.rounds_played}
            Moves this game: {self.moves_this_game}
            """
        )
