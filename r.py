from tkinter import *
#from ttk import *
from PIL import Image, ImageTk

trans_color = '-alpha'

root = Tk()
img = ImageTk.PhotoImage(Image.open('graphics/icons/iotfogsim_icon.png'))
img_label = Label(root, image=img)
img_label.pack()
img_label.img = img  # PIL says we need to keep a ref so it doesn't get GCed
root.update()
overlay = Toplevel(root)
print ('root.geo=', root.geometry())
geo = '{}x{}+{}+{}'.format(root.winfo_width(), root.winfo_height(),
    root.winfo_rootx(), root.winfo_rooty())
print ('geo=',geo)
overlay.geometry(geo)
overlay.overrideredirect(1)
overlay.wm_attributes('-transparent', trans_color)
overlay.config(background=trans_color)

lbl = Label(overlay, text='LABEL')
lbl.config(background=trans_color)
lbl.pack()

def moved(e):
    geo = '{}x{}+{}+{}'.format(root.winfo_width(), root.winfo_height(),
        root.winfo_rootx(), root.winfo_rooty())
    overlay.geometry(geo)

root.bind('<Configure>', moved)

root.mainloop()