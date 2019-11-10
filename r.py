import tkinter
import random


c = tkinter.Canvas(width = 400, height = 300)
c.pack()

def klik(event):
    r = 1
    x, y = event.x, event.y
    color = "red"
    circ = c.create_oval(x - r, y - r, x + r, y + r, fill="", outline = 'red', dash=(4,2))

    def shrink(r, x, y, color, circ):
        if r > 0 and r < 40:
            r += 1
            c.coords(circ, x+r, y+r, x-r, y-r)
            c.after(100, shrink, r, x, y, color, circ)

    shrink(r, x, y, color, circ)

c.bind('<Button-1>', klik)
tkinter.mainloop()