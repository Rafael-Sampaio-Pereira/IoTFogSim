import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo

def popup_bonus():
    win = tk.Toplevel()
    win.wm_title("Window")

    l = tk.Label(win, text="Input")
    l.grid(row=0, column=0)

    b = ttk.Button(win, text="Okay", command=win.destroy)
    b.grid(row=0, column=1)

    CaixaDeEntrada1 = tk.Entry(win,width=20, bg='white', font=('Comic Sans MS', '10')).grid(row=1, column = 1, pady=2)

class Application(ttk.Frame):

    def __init__(self, master):
        ttk.Frame.__init__(self, master)
        self.pack()

        self.button_bonus = ttk.Button(self, text="Bonuses", command=popup_bonus)
        self.button_bonus.pack()



root = tk.Tk()

app = Application(root)

root.mainloop()