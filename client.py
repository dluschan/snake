from tkinter import *
from game import Maze, Player, GameFrame, Controller, Snake, Game, Key


class Client:
    def __init__(self):
        self.root = Tk()
        self.root.title("Snake")
        self.root.geometry("400x300")
        Button(self.root, text="Single Player Offline Game", command=self.single_offline_game).pack(side=LEFT, expand=YES, fill=BOTH)
        Button(self.root, text="Online", command=lambda: None).pack(side=LEFT, expand=YES, fill=BOTH)
        self.root.mainloop()

    def single_offline_game(self):
        self.window = Toplevel(self.root)
        self.window.title("Snake")
        self.game_window = GameFrame(self.window)
        self.window.resizable(False, False)
        self.window.focus_set()
        self.window.grab_set()
        self.window.wait_window()


if __name__ == "__main__":
    player = Client()
