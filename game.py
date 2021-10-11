from tkinter import Canvas, Tk
from random import choice


class Game:
    pass


def game_update():
    global r
    r = 0
    root.after_id = root.after(250, game_update)
    if direction != 0:
        forward()
    if root.after_id is not None:
        paint()


def game_start(event):
    game_over()
    global  direction, snake, score
    direction = 0
    snake = [(3, 2), (2, 2)]
    score = 0
    random_apple()
    game_update()


def random_apple():
    snakeM = set(snake)
    available = all - (walls | snakeM)
    global apple
    apple = choice(list(available))


def game_over():
    if root.after_id:
        global bstscore
        if score > bstscore:
            bstscore = score
        root.after_cancel(root.after_id)
        root.after_id = None
        c.create_rectangle(1,1 , size[0] * scale, size[1] * scale,
                      fill='white', outline="red", width=3)
        c.create_text(size[0] * scale // 2, size[1] * scale // 2 - 100, text="Press Space to continue", font="Verdana 40")
        c.create_text(size[0] * scale // 2 , size[1]  * scale // 2,text="Game over", font="Verdana 60",fill="red")
        c.create_text(size[0] * scale // 2, size[1] * scale // 2 + 100, text=score, font="Verdana 40",fill="green")
        c.create_text(size[0] * scale // 2, size[1] * scale // 2 + 300, text="best score", font="Verdana 40")
        c.create_text(size[0] * scale // 2, size[1] * scale // 2 + 380, text=bstscore, font="Verdana 40",fill="red")


def paint():
    c.delete("all")
    c.create_oval(apple[0] * scale, apple[1] * scale, apple[0] * scale + scale, apple[1] * scale + scale,
                       fill='red', outline='green', width=3, activedash=(5, 4))
    head, *tail = snake
    c.create_rectangle(head[0] * scale, head[1] * scale, head[0] * scale + scale, head[1] * scale + scale,
                       fill='black', outline='brown', width=3)
    for link in tail:
        c.create_rectangle(link[0] * scale, link[1] * scale, link[0] * scale + scale, link[1] * scale + scale,
                           fill='yellow', outline='brown', width=3, activedash=(5, 4))
    for wall in walls:
        c.create_rectangle(wall[0] * scale, wall[1] * scale, wall[0] * scale + scale, wall[1] * scale + scale,
                           fill='black', outline='green', width=5, activedash=(5, 4))
    c.create_text(size[0] * scale - 50,50, text=score, font="Verdana 40", fill="white")


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
    if target == apple:
        global score
        score += 1
        random_apple()
        snake = [target] + snake
    elif target not in snake[:-1] and target not in walls:
        snake = [target] + snake[:-1]
    else:
        game_over()

def up(event):
    global direction, r
    if direction != 4 and r == 0:
        direction = 3
        r += 1

def left(event):
    global direction, r
    if direction != 2 and direction != 0 and r == 0:
        direction = 1
        r += 1


def right(event):
    global direction, r
    if direction != 1 and r == 0:
        r += 1
        direction = 2


def down(event):
    global direction, r
    if direction != 3 and r == 0:
        r += 1
        direction = 4


if __name__ == "__main__":
    root = Tk()
    root.after_id = None
    size = (19, 10)
    scale = 100
    c = Canvas(root, width=size[0]*scale, height=size[1]*scale, bg='light green')
    c.pack()
    root.bind('<Up>', up)
    root.bind('<Down>', down)
    root.bind('<Left>', left)
    root.bind('<Right>', right)
    root.bind('<w>', up)
    root.bind('<s>', down)
    root.bind('<d>', right)
    root.bind('<a>', left)
    root.bind('<space>', game_start)
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
    bstscore = 0
    game_start(True)
    root.mainloop()
