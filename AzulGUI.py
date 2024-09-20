## File: AzulGui.py
## Date: 2024-02-27

# This is GUI frontend for the AZUL game.
# Run the file to run the game

import tkinter as tk
from typing import Any
from azul_backend.game import Game
from tkinter import PanedWindow
from tkinter import *

from collections import deque


class AzulApp(tk.Tk):

    __game: Game
    __windows: dict[str, tk.PanedWindow]
    __guirounds: int

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.__game = Game()
        self.__windows = {}
        self.__guirounds = 0
        self.create_windows(container)

    def create_windows(self, container: tk.Frame) -> None:

        paneldisplaykwargs = {"bd": "4", "relief": "raised", "bg": "lightblue"}
        # Create Main Panel. This is only done once on initalisation
        self.__windows["mainpanel"] = PanedWindow(
            container,
            paneldisplaykwargs,
            orient=VERTICAL,
        )
        self.__windows["mainpanel"].pack(fill=BOTH, expand=1)

        # Create scorepanel
        self.__windows["scorepanel"] = PanedWindow(
            self.__windows["mainpanel"], paneldisplaykwargs, height=70
        )
        self.__windows["mainpanel"].add(self.__windows["scorepanel"])

        # Create handpanel
        self.__windows["handpanel"] = PanedWindow(
            self.__windows["mainpanel"],
            paneldisplaykwargs,
            height=50,
        )
        self.__windows["mainpanel"].add(self.__windows["handpanel"])

        # Create playerboards Master Panel
        self.__windows["playerboardspanel"] = PanedWindow(
            self.__windows["mainpanel"], paneldisplaykwargs, height=325
        )
        self.__windows["mainpanel"].add(self.__windows["playerboardspanel"])

        # board for player1
        self.__windows["boardp1"] = PanedWindow(
            self.__windows["playerboardspanel"],
            paneldisplaykwargs,
            orient=VERTICAL,
            height=325,
        )
        self.__windows["playerboardspanel"].add(self.__windows["boardp1"])

        # Create board for player2
        self.__windows["boardp2"] = PanedWindow(
            self.__windows["playerboardspanel"],
            paneldisplaykwargs,
            orient=VERTICAL,
            height=325,
        )
        self.__windows["playerboardspanel"].add(self.__windows["boardp2"])

        # # Create top/bottom split for player 1
        self.__windows["toppanelp1"] = PanedWindow(
            self.__windows["boardp1"], paneldisplaykwargs, height=250
        )
        self.__windows["boardp1"].add(self.__windows["toppanelp1"])
        self.__windows["bottompanelp1"] = PanedWindow(
            self.__windows["boardp1"], paneldisplaykwargs, height=50
        )
        self.__windows["boardp1"].add(self.__windows["bottompanelp1"])

        # Create top/bottom split for player 2
        self.__windows["toppanelp2"] = PanedWindow(
            self.__windows["boardp2"], paneldisplaykwargs, height=250
        )
        self.__windows["boardp2"].add(self.__windows["toppanelp2"])
        self.__windows["bottompanelp2"] = PanedWindow(
            self.__windows["boardp2"], paneldisplaykwargs, height=50
        )
        self.__windows["boardp2"].add(self.__windows["bottompanelp2"])

        # Create Pattern Lines Panel P1
        self.__windows["patternlpanelp1"] = PanedWindow(
            self.__windows["toppanelp1"], paneldisplaykwargs
        )
        self.__windows["toppanelp1"].add(self.__windows["patternlpanelp1"])

        # Create Wall Panel P1
        self.__windows["wallpanelp1"] = PanedWindow(
            self.__windows["toppanelp1"], paneldisplaykwargs
        )
        self.__windows["toppanelp1"].add(self.__windows["wallpanelp1"])

        # Create Pattern Lines Panel P2
        self.__windows["patternlpanelp2"] = PanedWindow(
            self.__windows["toppanelp2"], paneldisplaykwargs
        )
        self.__windows["toppanelp2"].add(self.__windows["patternlpanelp2"])

        # Create Wall Panel P2
        self.__windows["wallpanelp2"] = PanedWindow(
            self.__windows["toppanelp2"], paneldisplaykwargs
        )
        self.__windows["toppanelp2"].add(self.__windows["wallpanelp2"])

        # Create Factory Names
        self.__windows["factorynamespanel"] = PanedWindow(
            self.__windows["mainpanel"], paneldisplaykwargs
        )
        self.__windows["mainpanel"].add(self.__windows["factorynamespanel"])
        factory_label = tk.Label(
            self.__windows["factorynamespanel"],
            text="F1                                F2                                F3                                F4                                F5",
            font=("Arial", 18),
        )
        self.__windows["factorynamespanel"].add(factory_label)

        # Create Factory Panel
        self.__windows["factorypanel"] = PanedWindow(
            self.__windows["mainpanel"], paneldisplaykwargs, orient=HORIZONTAL
        )
        self.__windows["mainpanel"].add(self.__windows["factorypanel"])

        self.__windows["factory1panel"] = PanedWindow(
            self.__windows["factorypanel"], paneldisplaykwargs
        )
        self.__windows["factorypanel"].add(self.__windows["factory1panel"])
        self.__windows["factory2panel"] = PanedWindow(
            self.__windows["factorypanel"], paneldisplaykwargs
        )
        self.__windows["factorypanel"].add(self.__windows["factory2panel"])
        self.__windows["factory3panel"] = PanedWindow(
            self.__windows["factorypanel"], paneldisplaykwargs
        )
        self.__windows["factorypanel"].add(self.__windows["factory3panel"])
        self.__windows["factory4panel"] = PanedWindow(
            self.__windows["factorypanel"], paneldisplaykwargs
        )
        self.__windows["factorypanel"].add(self.__windows["factory4panel"])
        self.__windows["factory5panel"] = PanedWindow(
            self.__windows["factorypanel"], paneldisplaykwargs
        )
        self.__windows["factorypanel"].add(self.__windows["factory5panel"])

        # Create Centre of Table
        self.__windows["cotpanel"] = PanedWindow(
            self.__windows["mainpanel"], paneldisplaykwargs
        )
        self.__windows["mainpanel"].add(self.__windows["cotpanel"])

        # Create Pattern Lines Player 1 and
        for i in range(5):
            self.__windows["patternlpanelp1"].columnconfigure(i, weight=1)
            self.__windows["patternlpanelp2"].columnconfigure(i, weight=1)

        self.create_pattern_line_buttons("patternlpanelp1", 1)
        self.create_pattern_line_buttons("patternlpanelp2", 2)

        for i in range(4):
            self.__windows["factory1panel"].columnconfigure(i, weight=1)
            self.__windows["factory2panel"].columnconfigure(i, weight=1)
            self.__windows["factory3panel"].columnconfigure(i, weight=1)
            self.__windows["factory4panel"].columnconfigure(i, weight=1)
            self.__windows["factory5panel"].columnconfigure(i, weight=1)

        self.Create_Factory_Buttons(1, "factory1panel")
        self.Create_Factory_Buttons(2, "factory2panel")
        self.Create_Factory_Buttons(3, "factory3panel")
        self.Create_Factory_Buttons(4, "factory4panel")
        self.Create_Factory_Buttons(5, "factory5panel")

        for i in range(16):
            self.__windows["cotpanel"].columnconfigure(i, weight=1)
        self.Create_Factory_Buttons(0, "cotpanel")

        # Create floor Player 1 and 2
        for i in range(8):
            self.__windows["bottompanelp1"].columnconfigure(i, weight=1)
            self.__windows["bottompanelp2"].columnconfigure(i, weight=1)

        self.create_floor_buttons("bottompanelp1", 1)
        self.create_floor_buttons("bottompanelp2", 2)

        # Create Wall Player 1 and 2
        for i in range(5):
            self.__windows["wallpanelp1"].columnconfigure(i, weight=1)
            self.__windows["wallpanelp2"].columnconfigure(i, weight=1)

        self.create_wall_buttons("wallpanelp1", 1)
        self.create_wall_buttons("wallpanelp2", 2)

        # Set the current score and players
        self.update_player_display()

    def Create_Factory_Buttons(self, factory: int, window: str) -> None:

        for widget in self.__windows[window].winfo_children():
            widget.destroy()

        tiles = self.__game.show_factory(factory)
        buttons: dict[str, tk.Button] = {}

        for i, item in enumerate(tiles):
            buttons[item.get_display_text() + str(i)] = tk.Button(
                self.__windows[window],
                text=item.get_display_text(),
                bg=item.get_display_colour(),
                font=("Arial, 14"),
                # Used type ignore, as the GUI is out of scope for the assignment
                command=lambda tile_type=item.get_tile_type(): self.make_factory_offer(  # type: ignore
                    factory, tile_type, window
                ),
            )
            buttons[item.get_display_text() + str(i)].grid(
                row=0, column=i, sticky=tk.W + tk.E
            )

    def create_pattern_line_buttons(self, window: str, player: int) -> None:
        for widget in self.__windows[window].winfo_children():
            widget.destroy()

        possible_lines = ["line1", "line2", "line3", "line4", "line5"]

        pattern_lines = self.__game.show_pattern_lines(player)

        for k, line in enumerate(possible_lines):
            tiles = pattern_lines[line]

            for i, item in enumerate(reversed(tiles)):
                if item is not None:
                    button = tk.Button(
                        self.__windows[window],
                        text=item.get_display_text(),
                        bg=item.get_display_colour(),
                        font=("Arial, 14"),
                        # Used type ignore, as the GUI is out of scope for the assignment
                        command=lambda line=line: self.place_on_patternlines(  # type: ignore
                            window, line, player
                        ),
                    )
                    button.grid(row=k, column=5 - i, sticky=tk.W + tk.E)
                else:
                    button = tk.Button(
                        self.__windows[window],
                        text="[         ]",
                        bg="white",
                        font=("Arial, 14"),
                        # Used type ignore, as the GUI is out of scope for the assignment
                        # and I'm happy it's giving be the correct behaviour
                        command=lambda line=line: self.place_on_patternlines(  # type: ignore
                            window, line, player
                        ),
                    )
                    button.grid(row=k, column=5 - i, sticky=tk.W + tk.E)

    def create_floor_buttons(self, window: str, player: int) -> None:

        for widget in self.__windows[window].winfo_children():
            widget.destroy()

        floor = self.__game.show_floor(player)

        for i, item in enumerate(floor):

            if item is not None:
                button = tk.Button(
                    self.__windows[window],
                    text=item.get_display_text(),
                    bg=item.get_display_colour(),
                    font=("Arial, 14"),
                    command=lambda: self.button_click(),
                )
                button.grid(row=0, column=i, sticky=tk.W + tk.E)

    def create_hand_buttons(self) -> None:

        for widget in self.__windows["handpanel"].winfo_children():
            widget.destroy()

        hand = self.__game.show_hand()
        for i, item in enumerate(hand):
            if item is not None:
                button = tk.Button(
                    self.__windows["handpanel"],
                    text=item.get_display_text(),
                    bg=item.get_display_colour(),
                    font=("Arial, 14"),
                    command=lambda: self.button_click(),
                )
                button.grid(row=0, column=i, sticky=tk.W + tk.E)

    def create_wall_buttons(self, window: str, player: int) -> None:

        for widget in self.__windows[window].winfo_children():
            widget.destroy()

        possible_lines = ["line1", "line2", "line3", "line4", "line5"]
        wall = self.__game.show_wall(player)

        for k, line in enumerate(possible_lines):
            tiles = wall[line]

            for i, item in enumerate(tiles):
                if item is not None:
                    button = tk.Button(
                        self.__windows[window],
                        text=item.get_display_text(),
                        bg=item.get_display_colour(),
                        font=("Arial, 14"),
                        command=lambda: self.button_click(),
                    )
                    button.grid(row=k, column=i, sticky=tk.W + tk.E)
                else:
                    button = tk.Button(
                        self.__windows[window],
                        text="[         ]",
                        bg=self.get_default_wall_colours(line, i),
                        font=("Arial, 14"),
                        command=lambda: self.button_click(),
                    )
                    button.grid(row=k, column=i, sticky=tk.W + tk.E)

    def button_click(self) -> None:
        print(f"Button has no effect")

    def place_on_patternlines(
        self, window: str, line: str, player: int
    ) -> None:
        if self.__game.show_current_player() == player:
            self.__game.place_on_patternlines(line)
            self.create_pattern_line_buttons(window, player)
            self.create_hand_buttons()

            if player == 1:
                self.create_floor_buttons("bottompanelp1", 1)
            else:
                self.create_floor_buttons("bottompanelp2", 2)

            if self.__game.rounds_played > self.__guirounds:
                self.__guirounds = self.__game.rounds_played
                self.refresh()
            else:
                self.update_player_display()
        else:
            raise RuntimeError(f"Player {player} is not the current player")

    def make_factory_offer(
        self, factory: int, tile_type: str, window: str
    ) -> None:
        self.__game.make_factory_offer(factory, tile_type)

        if (
            not self.__game.show_hand()
        ):  # hand is empty, forced moved made. we must refresh
            self.refresh()

        self.Create_Factory_Buttons(factory, window)
        self.Create_Factory_Buttons(0, "cotpanel")
        self.create_hand_buttons()

    def get_default_wall_colours(self, line: str, column: int) -> str:
        """
        Returns an appropriate colour for the wall
        If there are no tiles in place
        """
        # Format turned off to make the dictionary easier to read relative to the wall
        # fmt: off
        wall_colours = {
            "line1": ["deepskyblue", "khaki1", "darksalmon", "darkseagreen", "white",],
            "line2": ["white", "deepskyblue", "khaki1", "darksalmon", "darkseagreen",],
            "line3": ["darkseagreen", "white", "deepskyblue", "khaki1", "darksalmon",],
            "line4": ["darksalmon", "darkseagreen", "white", "deepskyblue", "khaki1",],
            "line5": ["khaki1", "darksalmon", "darkseagreen", "white", "deepskyblue",],
        }
        # fmt: on
        return wall_colours[line][column]

    def update_player_display(self) -> None:
        for widget in self.__windows["scorepanel"].winfo_children():
            widget.destroy()

        if self.__game.show_game_state().value == 4:

            if self.__game.show_score(1) > self.__game.show_score(2):
                scorelabel = tk.Label(
                    self.__windows["scorepanel"],
                    text=f"Game Over!!!\n Player 1 wins with {self.__game.show_score(1)} points vs {self.__game.show_score(2)} points",
                    font=("Arial", 18),
                )
            else:
                scorelabel = tk.Label(
                    self.__windows["scorepanel"],
                    text=f"Game Over!!!\n Player 2 wins with {self.__game.show_score(2)} points vs {self.__game.show_score(1)} points",
                    font=("Arial", 18),
                )

            self.__windows["scorepanel"].add(scorelabel)
        else:
            p1start_string = ""
            p2start_string = ""
            if self.__game.show_current_player() == 1:
                p1start_string = "*"
            else:
                p2start_string = "*"

            scorelabel = tk.Label(
                self.__windows["scorepanel"],
                text=f"Round {self.__guirounds+1}\n {p1start_string}Player 1: [{self.__game.show_score(1)}]     {p2start_string}Player 2: [{self.__game.show_score(2)}] ",
                font=("Arial", 18),
            )
            self.__windows["scorepanel"].add(scorelabel)

    def refresh(self) -> None:
        """
        Refreshes the GUI
        """
        self.create_pattern_line_buttons("patternlpanelp1", 1)
        self.create_pattern_line_buttons("patternlpanelp2", 2)
        self.Create_Factory_Buttons(1, "factory1panel")
        self.Create_Factory_Buttons(2, "factory2panel")
        self.Create_Factory_Buttons(3, "factory3panel")
        self.Create_Factory_Buttons(4, "factory4panel")
        self.Create_Factory_Buttons(5, "factory5panel")
        self.Create_Factory_Buttons(0, "cotpanel")
        self.create_floor_buttons("bottompanelp1", 1)
        self.create_floor_buttons("bottompanelp2", 2)
        self.create_wall_buttons("wallpanelp1", 1)
        self.create_wall_buttons("wallpanelp2", 2)
        self.create_hand_buttons()
        self.update_player_display()


if __name__ == "__main__":
    app = AzulApp()
    app.mainloop()
