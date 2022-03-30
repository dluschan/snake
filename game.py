from random import choice
from itertools import product
from tkinter import *


def set_default(obj):
    if isinstance(obj, set):
        return list(obj)
    raise TypeError


class Maze:
    """Лабиринт для игры.

    Нужен, чтобы можно было добавлять в лабиринт произвольные стены."""
    def __init__(self, size):
        self.size = size
        self.walls = {(x, y) for x, y in product((0, self.size[0] - 1), range(self.size[1]))}
        self.walls |= {(x, y) for x, y in product(range(self.size[0]), (0, self.size[1] - 1))}
        self.space = set(product(range(self.size[0]), range(self.size[1]))) - self.walls


class Snake:
    """Змея.

    Представляется списком ячеек, которые занимает.
    Тело змеи = голова змеи + хвост змеи.
    За один игровой такт змея должна менять направление движения не больше одного раза - контролируется на уровне выше.
    Направления движения змеи:
        1 - left
        2 - right
        3 - up
        4 - down
    """
    def __init__(self, body: list[tuple[int, int]], direction: int):
        self.cached_body = body[:]
        self.cached_direction = direction
        self.lock = False
        self.body = body
        self.direction = direction
        self.moves = {'right': self.right, 'up': self.up, 'left': self.left, 'down': self.down}

    def reset(self):
        self.body = self.cached_body
        self.direction = self.cached_direction

    def up(self, event):
        if not self.lock and self.direction in (1, 2):
            self.lock = True
            self.direction = 3

    def left(self, event):
        if not self.lock and self.direction in (3, 4):
            self.lock = True
            self.direction = 1

    def right(self, event):
        if not self.lock and self.direction in (3, 4):
            self.lock = True
            self.direction = 2

    def down(self, event):
        if not self.lock and self.direction in (1, 2):
            self.lock = True
            self.direction = 4

    def move(self, target):
        self.body = [target] + self.body[:-1]

    def grow(self, target):
        self.body = [target] + self.body

    def get_target(self):
        x, y = self.body[0]
        if self.direction == 1:
            x -= 1
        if self.direction == 2:
            x += 1
        if self.direction == 3:
            y -= 1
        if self.direction == 4:
            y += 1
        self.lock = False
        return x, y


class Key:
    def __init__(self, key):
        self.key = key

    def connect(self, frame, fun):
        frame.master.bind(self.key, fun)


class Controller:
    def __init__(self, keys, snake: Snake, frame: Frame):
        self.keys = keys
        self.snake = snake
        self.frame = frame
        for direction in self.keys:
            self.keys[direction].connect(self.frame, self.snake.moves[direction])


class Player:
    def __init__(self, name, snake, color):
        self.cached_color = color
        self.name = name
        self.snake = snake
        self.color = None
        self.crashed = False
        self.score = 0

    def game_over(self):
        self.crashed = True
        self.color = 'red'

    def eat(self):
        self.score += 1

    def reset(self):
        self.score = 0
        self.color = self.cached_color
        self.snake.reset()
        self.crashed = False


class Game:
    def __init__(self, players: list[Player], maze: Maze):
        self.maze = maze
        self.players = players
        self.apple = None
        self.speed = None

    def reset(self):
        self.apple = self.random_apple()
        self.speed = 1
        for player in self.players:
            player.reset()

    def random_apple(self):
        free_space = self.maze.space - set.union(*[set(player.snake.body) for player in self.players])
        if free_space:
            return choice(list(free_space))
        else:
            return None

    def forward(self):
        snake_targets = {player: player.snake.get_target() for player in self.players}

        for player in self.players:
            if snake_targets[player] == self.apple:
                player.snake.grow(snake_targets[player])
                self.speed += 1
                player.eat()
                self.apple = None
            else:
                player.snake.move(snake_targets[player])
        for player in self.players:
            bodies = set(player.snake.body[1:])
            for other in self.players:
                if other != player:
                    bodies |= set(other.snake.body)
            head = snake_targets[player]
            if head in bodies | self.maze.walls:
                player.game_over()
        if not self.apple:
            self.apple = self.random_apple()

        return all(not player.crashed for player in self.players)


class GameFrame(Frame):
    def __init__(self, parent, **options):
        Frame.__init__(self, parent, **options)
        self.pack(expand=YES, fill=BOTH)
        self.after_id = None
        self.maze = Maze((16, 10))
        self.keys = {'right': Key('<Right>'), 'up': Key('<Up>'), 'left': Key('<Left>'), 'down': Key('<Down>')}
        self.game = None
        self.scale = 50
        self.canvas = Canvas(self, width=self.scale * self.maze.size[0], height=self.scale * self.maze.size[1])
        self.canvas.pack(expand=YES, fill=BOTH)
        self.paint_maze(self.maze)
        self.labels = {}
        snake = Snake([(2, 2), (3, 2)], 2)
        player = Player("Garry", snake, 'yellow')
        self.controller = Controller(self.keys, snake, self)
        self.game = Game([player], self.maze)
        for player in self.game.players:
            self.labels[player] = Label(self, text=f"Игрок {player.name}: {player.score}")
            self.labels[player].pack(side=TOP, expand=YES, fill=X)
        Button(self, text="Pause", command=self.pause).pack(side=LEFT, expand=YES, fill=X)
        Button(self, text="Start", command=self.start).pack(side=LEFT, expand=YES, fill=X)
        Button(self, text="Quit", command=self.destroy).pack(side=RIGHT, expand=YES, fill=X)

    def paint_snake(self, player):
        head, *tail = player.snake.body
        scale = self.scale
        self.canvas.delete(player.name)
        self.canvas.create_rectangle(head[0] * scale, head[1] * scale, head[0] * scale + scale, head[1] * scale + scale,
                           fill='black', outline='brown', width=3, tag=player.name)
        for link in tail:
            self.canvas.create_rectangle(link[0] * scale, link[1] * scale, link[0] * scale + scale, link[1] * scale + scale,
                               fill=player.color, outline='brown', width=3, tag=player.name)
        self.labels[player].config(text=f"Игрок {player.name}: {player.score}")

    def paint(self):
        for player in self.game.players:
            self.paint_snake(player)
        self.paint_apple()

    def paint_apple(self):
        scale = self.scale
        apple = self.game.apple
        self.canvas.delete("apple")
        self.canvas.create_oval(apple[0] * scale, apple[1] * scale, apple[0] * scale + scale, apple[1] * scale + scale,
                      fill='red', outline='green', width=3, tag="apple")

    def paint_maze(self, maze):
        for wall in maze.walls:
            self.canvas.create_rectangle(wall[0] * self.scale, wall[1] * self.scale, wall[0] * self.scale + self.scale,
                                         wall[1] * self.scale + self.scale,
                                         fill='black', outline='green', width=5)

    def update(self):
        if self.game.forward():
            self.after_id = self.after(1000 // self.game.speed, self.update)
        self.paint()

    def pause(self):
        if self.after_id:
            self.after_cancel(self.after_id)
            self.after_id = None
        else:
            self.update()

    def start(self):
        self.game.reset()
        if self.after_id:
            self.after_cancel(self.after_id)
            self.after_id = None
        self.update()


