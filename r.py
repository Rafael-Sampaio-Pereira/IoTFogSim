from tkinter import *

# New Tkinter
root = Tk()
sw = str(root.winfo_screenwidth())

# Function for new toplevel
def new_wdow():
    w = Toplevel(root)
    w.geometry("0x0+" + sw + "+0")
    w.state('zoomed')
    w.overrideredirect(1)
    Label(w, text='Hello Secondary Display').pack()

# Make button in main window
Button(root, text="Hello", command=new_wdow).pack()

root.mainloop()