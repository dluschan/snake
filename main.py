from tkinter import *


def game_update():
    forward()
    root.after(100, game_update)


def forward():
    global x
    x += 10
    c.create_rectangle(x, y, x + 200, y +100, fill='yellow', outline='brown', width=3, activedash=(5, 4))
    c.create_oval(520, 120, 580, 180, fill='red', outline='green', width=3, activedash=(5, 4))


root = Tk()
c = Canvas(root, width=1000, height=1000, bg='light green')
c.pack()
direction = 0
x = 100
y = 100

game_update()
root.mainloop()