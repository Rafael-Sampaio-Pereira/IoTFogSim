

import tkinter as tk

class DraggableImage(object):
    def __init__(self, canvas, file, x, y):
        self.canvas = canvas
        self.image_file = tk.PhotoImage(file=file)
        self.draggable_img = canvas.create_image(x, y, image=self.image_file)
         
        canvas.tag_bind(self.draggable_img, '<Button1-Motion>', self.move)
        canvas.tag_bind(self.draggable_img, '<ButtonRelease-1>', self.release)
        canvas.configure(cursor="hand1")
        self.move_flag = False
         
    def move(self, event):
        if self.move_flag:
            new_xpos = event.x
            new_ypos = event.y
             
            self.canvas.move(self.draggable_img,
                new_xpos-self.mouse_xpos ,new_ypos-self.mouse_ypos)
             
            self.mouse_xpos = new_xpos
            self.mouse_ypos = new_ypos
        else:
            self.move_flag = True
            self.canvas.tag_raise(self.draggable_img)
            self.mouse_xpos = event.x
            self.mouse_ypos = event.y
 
    def release(self, event):
        self.move_flag = False
