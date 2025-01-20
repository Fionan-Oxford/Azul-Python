# Azul Python
## This is a 2-player implementation of the AZUL board game

# ASSUMPTIONS AND SIMPLIFICATIONS
I have made a number of simplifications to the game, and I have also made a number of assumptions.

1.  There are only 2 players, and thus always five factories
2. The game will always start with player1.
   The very first move, of placing the "starting player" marker into the centre of the table is
   done automatically
3. At the end of the game, there are NO additional scoring points for having completed a row or column of
   or maxed out the tiles of a specific colour
4. There is no variant play in this implementation
5. There is no "lid of the box". Any tiles that are removed from the game are simply deleted
6. If the tile bag is empty (100 tiles have been drawn), the bag magically reffils itself to 100. There
   is no lid of the box for the bag to refill from. Thus it is possibe for more than 100 colour tiles to be in play
7. There is no means to reset a completed game. You need to create a new game object

# HOW TO USE
How to use the game class

Much of the AZUL game is automated here, such as the entirety of the "Wall-Tiling" and "Prepare for Next Round" phases.
Play starts with Player 1, and the game will change players. Any factory offers are made for the current player.
To play the game, the user must
1. Make a factory offer (select tiles from a factory or the centre of the table) using the make_factory_offer method
2. Place the selected tiles on a pattern line using the place_on_patternlines method
   There are occasions where there are no valid moves, in which case the game will automatically drop the tiles to the floor
   and change the player
   To detect this, you can check the contents of the hand after making a factory offer, or keep track of the moves this round
   Or check the current player.

The game will automatically advance to the next phase when the current phase is complete, and will auto`matically
change the player when the current player's turn is complete.

The game will also automatically determine the starting player for the next round, and will automatically
apply the score penalty from the floor tiles at the end of the round.

The game will also automatically determine if the game is over, and will automatically end the game if it is.

To see the current state of the game, the user can call the following "show" methods
These methods show immutabel information regarding the game
1. show_game_state - returns the current game state
2. show_hand - returns the tiles in the hand of the current player, i.e post factory offer and pre pattern line placement
3. show_current_player - returns the current player
4. show_factory - returns the tiles in a factory or centre of the table as a tuple
5. show_pattern_lines - returns the pattern lines of the specified player
6. show_floor - returns the floor of the specified player
7. show_wall - returns the wall of the specified player
8. show_score - returns the score of the specified player

There are also a number of interesting public counters
1. moves_this_round - returns the number of moves made this round
2. rounds_played - returns the number of rounds played
3. moves_this_game - returns the number of moves made this game

# TESTING
I made a jupyter notebook for unit tests - test.ipynb

# GUI
I created a tkinter GUI for testing purposes which integrates using the above stated methods. Please see AzulGui.py.
