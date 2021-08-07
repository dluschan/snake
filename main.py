from tkinter import *


def game_update():
        forward()
        paint()
        root.after(500, game_update)


def paint():
    c.delete("all")
    for link in snake:
        c.create_rectangle(link[0] * scale, link[1] * scale, link[0] * scale + scale, link[1] * scale + scale, fill='yellow',
                           outline='brown', width=3, activedash=(5, 4))  


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
    target = [x, y]
    snake = [target] + snake[:-1]


def up(event):
    global direction
    if direction != 4:
        direction = 3


def left(event):
    global direction
    if direction != 2:
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
direction = 2
snake = [[3, 1], [2, 1], [1, 1]]
eat = c.create_oval(520, 120, 580, 180, fill='red', outline='green', width=3, activedash=(5, 4))
game_update()
root.mainloop()