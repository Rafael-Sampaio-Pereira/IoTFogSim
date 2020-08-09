#!/usr/bin/env python3
import tkinter as tk


class MainCanvas(tk.Canvas):
    def __init__(self, tk_parent):
        super().__init__(tk_parent, height=200, width=200, bg="green")
        self.pack()
        self.bind("<Motion>",     self.print_move)
        self.bind("<MouseWheel>", self.print_scroll)  # For Mac
        self.bind("<Button-4>",   self.print_scroll)  # For Linux
        self.bind("<Button-5>",   self.print_scroll)  # For Linux

    def print_coords(self, name, event):
        print("{}: x: ({}, {}), y: ({}, {})".format(
            name,
            event.x, int(self.canvasx(event.x)),
            event.y, int(self.canvasy(event.y))))

    def print_move(self, event):
        self.print_coords("moving", event)

    def print_scroll(self, event):
        self.print_coords("scroll", event)


class Bottom(tk.Canvas):
    def __init__(self, tk_parent):
        super().__init__(tk_parent, height=5, width=500, bg="red")
        self.pack()


class GUI(tk.Frame):
    def __init__(self, tk_parent):
        super().__init__(tk_parent)
        self.pack()
        self.main = MainCanvas(self)
        self.bottom = Bottom(self)


if __name__ == "__main__":
    root = tk.Tk()
    gui = GUI(root)

    # Make an easy way to exit
    for char in "wWqQ":
        root.bind("<Control-{}>".format(char), lambda _: root.destroy())

    root.mainloop()