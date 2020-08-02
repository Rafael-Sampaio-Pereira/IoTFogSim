from tkinter import *

root = Tk()
menu_bar = Menu(root)

def clicked(menu):
    menu.entryconfigure(1, label="Clicked!")

file_menu = Menu(menu_bar, tearoff=False)
file_menu.add_command(label="An example item", command=lambda: clicked(file_menu))
menu_bar.add_cascade(label="File", menu=file_menu)

root.config(menu=menu_bar)
root.mainloop()