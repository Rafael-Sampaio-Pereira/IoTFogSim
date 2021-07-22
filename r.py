from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk
import pathlib


class Root(Tk):
    def __init__(self):
        super(Root, self).__init__()
        self.title("Python Tkinter Dialog Widget")
        self.minsize(640, 400)

        self.labelFrame = ttk.LabelFrame(self, text = "Open File")
        self.labelFrame.grid(column = 0, row = 1, padx = 20, pady = 20)

        self.button()


    def button(self):
        self.button = ttk.Button(self.labelFrame, text = "Browse A File",command = self.fileDialog)
        self.button.grid(column = 1, row = 1)


    def fileDialog(self):
        

        path = pathlib.Path.cwd().parent

        self.filename = filedialog.askopenfilename(initialdir =  path, title = "Select A File", filetypes =
        [("png files","*.png")] )
        self.label = ttk.Label(self.labelFrame, text = "")
        self.label.grid(column = 1, row = 2)
        self.label.configure(text = self.filename)

        img = Image.open(self.filename)
        photo = ImageTk.PhotoImage(img)

        self.label2 = Label(image=photo)
        self.label2.image = photo 
        self.label2.grid(column=3, row=4)

root = Root()
root.mainloop()