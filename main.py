from tkinter import *


def game_update():
    forward()
    paint()
    root.after(1000, game_update)


def paint():
    c.delete("all")
    for link in snake:
        c.create_rectangle(link[0] * 100, link[1] * 100, link[0] * 100 + 100, link[1] * 100 + 100, fill='yellow',
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


root = Tk()
c = Canvas(root, width=1000, height=1000, bg='light green')
c.pack()
direction = 2
x = 100
y = 100
snake = [[5, 5], [4, 5], [4, 6],[4, 7],[4,8]]
eat = c.create_oval(520, 120, 580, 180, fill='red', outline='green', width=3, activedash=(5, 4))
game_update()
root.mainloop()