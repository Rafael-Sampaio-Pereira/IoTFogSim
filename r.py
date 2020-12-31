import PIL
from PIL import Image, ImageTk
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

root = Tk()



class Window:

    def __init__(self, master=None):
        tower = PIL.Image.open("teste.png")
        master.update()
        win_width = int(master.winfo_width())
        win_height = int(master.winfo_height())
        # Resize the image to the constraints of the root window.
        tower = tower.resize((win_width, win_height))
        tower_tk = ImageTk.PhotoImage(tower)
        # Create a label to hold the background image.
        canvas = Canvas(master, width=win_width, height=win_height)
        canvas.place(x=0, y=0, anchor='nw')
        canvas.create_image(0, 0, image=tower_tk, anchor='nw')
        canvas.image = tower_tk
        frame = Frame(master)
        frame.place(x=win_width, y=win_height, anchor='se')
        master.update()
        w = Label(master, text="Send and receive files easily", anchor='w')
        w.config(font=('times', 32))
        w.place(x=0, y=0, anchor='nw')

        master.title("Bifrost v1.0")
        self.img1 = PhotoImage(file="teste.png")
        self.img2 = PhotoImage(file="teste.png")

        frame.grid_columnconfigure(0, weight=1)
        sendButton = Button(frame, image=self.img2)
        sendButton.grid(row=0, column=1)
        sendButton.image = self.img2
        receiveButton = Button(frame, image=self.img1)
        receiveButton.grid(row=0, column=2)
        receiveButton.image = self.img1

        menu = Menu(master)
        master.config(menu=menu)

        file = Menu(menu)
        file.add_command(label='Exit', command=self.client_exit)
        menu.add_cascade(label='File', menu=file)

        edit = Menu(menu)
        edit.add_command(label='abcd')
        menu.add_cascade(label='Edit', menu=edit)

        help = Menu(menu)

        help.add_command(label='About Us', command=self.about)
        menu.add_cascade(label='Help', menu=help)

    def callback():
        path = filedialog.askopenfilename()
        e.delete(0, END)  # Remove current text in entry
        e.insert(0, path)  # Insert the 'path'
        # print path

        w = Label(root, text="File Path:")
        e = Entry(root, text="")
        b = Button(root, text="Browse", fg="#a1dbcd", bg="black", command=callback)

        w.pack(side=TOP)
        e.pack(side=TOP)
        b.pack(side=TOP)

    def client_exit(self):
        exit()

    def about(self):
        message = "This is a project developed by Aditi,Sagar and"
        message += "Suyash as the final year project."
        messagebox.showinfo("Delete Theme", message)

root.resizable(0,0)

#size of the window
root.geometry("700x400")
app = Window(root)
root.mainloop()