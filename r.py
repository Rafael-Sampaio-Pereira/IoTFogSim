import tkinter as tk
from tkinter.constants import *


class MyClass:
    def __init__(self, parent):
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.canvas = tk.Canvas(self.parent)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.find_closest)

       # Create dictionary mapping canvas object ids to a name.
        self.object_names = {}
        id = self.canvas.create_oval(50, 50, 60, 60, fill="Red")
        self.object_names[id] = 'Red object'
        id = self.canvas.create_oval(100, 100, 110, 110, fill="Blue")
        self.object_names[id] = 'Blue object'
        id = self.canvas.create_oval(150, 150, 160, 160, fill="Green")
        self.object_names[id] = 'Green object'

        self.name_lbl1 = tk.Label(self.parent, text='Closest object:')
        self.name_lbl1.pack(side=LEFT)

        self.name_var = tk.StringVar(value='')
        self.name_lbl2 = tk.Label(self.parent, textvariable=self.name_var)
        self.name_lbl2.pack(side=LEFT)

    def find_closest(self, event):
        if (closest := self.canvas.find_closest(event.x, event.y)):
            obj_id = closest[0]
            self.name_var.set(self.object_names[obj_id])  # Updates lbl2.


if __name__ == '__main__':
    root = tk.Tk()
    instance = MyClass(root)
    root.mainloop()
