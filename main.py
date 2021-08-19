from tkinter import *
from random import choice


def game_update():
    if direction != 0:
        forward()
    paint()
    global aid
    aid = root.after(300, game_update)
    print(aid)
def game_start():
    game_update()


def random_apple():
    snakeM = set(snake)
    available = all - (walls | snakeM)
    global apple
    apple = choice(list(available))

def game_over():
    print(aid,1)
    global snake, direction
    snake = [(3, 2), (2, 2)]
    direction = 0
    root.after_cancel(aid)
    c.create_rectangle(0 * scale, 0 * scale, size[0] * scale + scale, size[1] * scale + scale,
                       fill='black', outline='brown', width=3, activedash=(5, 4))


def paint():
    c.delete("all")
    c.create_oval(apple[0] * scale, apple[1] * scale, apple[0] * scale + scale, apple[1] * scale + scale,
                       fill='red', outline='green', width=3, activedash=(5, 4))
    head, *tail = snake
    c.create_rectangle(head[0] * scale, head[1] * scale, head[0] * scale + scale, head[1] * scale + scale,
                       fill='black', outline='brown', width=3, activedash=(5, 4))
    for link in tail:
        c.create_rectangle(link[0] * scale, link[1] * scale, link[0] * scale + scale, link[1] * scale + scale,
                           fill='yellow', outline='brown', width=3, activedash=(5, 4))
    for wall in walls:
        c.create_rectangle(wall[0] * scale, wall[1] * scale, wall[0] * scale + scale, wall[1] * scale + scale,
                           fill='black', outline='green', width=5, activedash=(5, 4))


def forward():
    global snake
    """[6 5] [5 5] [4 5]"""
    """1 - left"""
    """2 - right"""
    """3 - up"""
    """4 - down"""
    if direction == 1:
        x = snake[0][0] - 1
        y = snake[0][1]
    if direction == 2:
        x = snake[0][0] + 1
        y = snake[0][1]
    if direction == 3:
        x = snake[0][0]
        y = snake[0][1] - 1
    if direction == 4:
        x = snake[0][0]
        y = snake[0][1] + 1
    target = (x, y)
    if target in snake or target in walls:
        game_over()
    else:
        if apple not in snake:
            snake = [target] + snake[:-1]
        else:
            random_apple()
            snake = [target] + snake


def up(event):
    global direction
    if direction != 4:
        direction = 3


def left(event):
    global direction
    if direction != 2 and direction != 0:
        direction = 1


def right(event):
    global direction
    if direction != 1:
        direction = 2


def down(event):
    global direction
    if direction != 3:
        direction = 4


root = Tk()
root.bind('<Up>', up)
root.bind('<Down>', down)
root.bind('<Left>', left)
root.bind('<Right>', right)
root.bind('<w>', up)
root.bind('<s>', down)
root.bind('<d>', right)
root.bind('<a>', left)
size = (14, 8)
scale = 100
c = Canvas(root, width=size[0]*scale, height=size[1]*scale, bg='light green')
c.pack()
direction = 0
snake = [(3, 2), (2, 2)]
snakeM = set(snake)
walls = set()
for y in range(size[1]):
    walls.add((0, y))
    walls.add((size[0] - 1, y))
for x in range(size[0]):
    walls.add((x, 0))
    walls.add((x, size[1] - 1))
all = set()
for i in range(size[0]):
    for j in range(size[1]):
        all.add((i, j))
random_apple()
game_update()
root.mainloop()
