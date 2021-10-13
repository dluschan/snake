from random import choice
from json import dumps
from threading import Timer


def set_default(obj):
    if isinstance(obj, set):
        return list(obj)
    raise TypeError


class Game:
    def __init__(self, server):
        self.server = server
        self.size = (19, 10)
        self.walls = set()
        for y in range(self.size[1]):
            self.walls.add((0, y))
            self.walls.add((self.size[0] - 1, y))
        for x in range(self.size[0]):
            self.walls.add((x, 0))
            self.walls.add((x, self.size[1] - 1))
        self.all = set()
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                self.all.add((i, j))
        self.direction = 2
        self.snake = [(3, 2), (2, 2)]
        self.score = 0
        self.r = 0
        self.game_over = False
        self.snakeM = None
        self.available = None
        self.apple = None
        self.target = None
        self.timer = None
        self.random_apple()

    def up(self):
        if self.direction != 4 and self.r == 0:
            self.direction = 3
            self.r += 1

    def left(self):
        if self.direction != 2 and self.r == 0:
            self.direction = 1
            self.r += 1

    def right(self):
        if self.direction != 1 and self.r == 0:
            self.r += 1
            self.direction = 2

    def down(self):
        if self.direction != 3 and self.r == 0:
            self.r += 1
            self.direction = 4

    def forward(self):
        """[6 5] [5 5] [4 5]"""
        """1 - left"""
        """2 - right"""
        """3 - up"""
        """4 - down"""
        x, y = None, None
        if self.direction == 1:
            x = self.snake[0][0] - 1
            y = self.snake[0][1]
        if self.direction == 2:
            x = self.snake[0][0] + 1
            y = self.snake[0][1]
        if self.direction == 3:
            x = self.snake[0][0]
            y = self.snake[0][1] - 1
        if self.direction == 4:
            x = self.snake[0][0]
            y = self.snake[0][1] + 1
        self.target = (x, y)
        if self.target == self.apple:
            self.score += 1
            self.random_apple()
            self.snake = [self.target] + self.snake
        elif self.target not in self.snake[:-1] and self.target not in self.walls:
            self.snake = [self.target] + self.snake[:-1]
        else:
            self.game_over = True

    def random_apple(self):
        self.snakeM = set(self.snake)
        self.available = self.all - (self.walls | self.snakeM)
        self.apple = choice(list(self.available))

    def update(self):
        self.timer = Timer(1, self.update)
        self.timer.start()
        self.r = 0
        self.forward()
        level = {"apple": self.apple, "snake": self.snake, "walls": self.walls, "size": self.size, "score": self.score}
        self.server.send(dumps(level, default=set_default))
