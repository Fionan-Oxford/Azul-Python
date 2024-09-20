# This module is used to define enumerations used in the game.
from enum import Enum


class GameState(Enum):
    """
    GameState is an enumeration of the possible states of the game
    It is used to control the flow of the game, and to ensure that
    Only valid actions are taken at any given time

    """

    FACTORY_OFFER = 1
    WALL_TILING = 2
    PREPARING_FOR_NEXT_ROUND = 3
    GAMEOVER = 4
