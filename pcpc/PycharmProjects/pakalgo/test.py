import datetime
import random
from tkinter import *
import time

# GUI
root = Tk()
root.geometry('900x900+250+100')
root.title('Test')
root.configure(background='grey')
Kanvas = Canvas(root, width=900, height=900, bg='grey')
Kanvas.pack()

colors = ('white', 'yellow', 'green', 'red')


def new_sit():
    for row in range(60):
        for col in range(60):
            color = random.choice(colors)
            y = row * 15
            x = col * 15
            Kanvas.create_rectangle(x, y, x + 15, y + 15, fill=color)
    root.update()


steps = 0
while True:
    a = datetime.datetime.now()
    steps += 1
    Kanvas.delete('all')
    print(f'Step {steps}')
    new_sit()
    b = datetime.datetime.now()
    print(b - a)
