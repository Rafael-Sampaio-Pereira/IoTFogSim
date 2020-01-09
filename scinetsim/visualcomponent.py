import tkinter
from config.settings import ICONS_PATH

from twisted.python import log

class VisualComponent(object):

    def __init__(self, is_wireless, canvas, deviceName, file, x, y):
        self.canvas = canvas
        self.x = x
        self.y = y


        self.is_wireless = is_wireless

        if self.is_wireless:
            self.signal_radius = 1
            self.coverage_area_radius = 100
            # The signal circle object to show wifi coverage area. - Rafael Sampaio
            # coverage are need not to be visible. - Rafael Sampaio
            self.draggable_coverage_area_circle = self.canvas.create_oval( self.x+self.coverage_area_radius, self.y+self.coverage_area_radius, self.x-self.coverage_area_radius, self.y-self.coverage_area_radius, fill="", outline="", width=1, stipple="gray12")

            # The signal circle object starts with no fill and no outline colors, these colors will be set in the propagate_signal method. - Rafael Sampaio
            self.draggable_signal_circle = self.canvas.create_oval(self.x, self.y, self.x, self.y, fill="", outline = "", dash=(4,2))

            canvas.tag_bind(self.draggable_coverage_area_circle, '<Button1-Motion>', self.move)
            canvas.tag_bind(self.draggable_coverage_area_circle, '<ButtonRelease-1>', self.release) 
            canvas.tag_bind(self.draggable_signal_circle, '<Button1-Motion>', self.move)
            canvas.tag_bind(self.draggable_signal_circle, '<ButtonRelease-1>', self.release)

        self.image_file = tkinter.PhotoImage(file=file)
        self.draggable_img = self.canvas.create_image(x, y, image=self.image_file)

        self.draggable_name = self.canvas.create_text(x,y+32,fill="black",font="Arial 9",
                        text=deviceName)

        self.draggable_alert = self.canvas.create_text(x,y-33,fill="black",font="Times 9",
                        text="alert")
        # font="Times 9 italic bold"
        
        canvas.tag_bind(self.draggable_alert, '<Button1-Motion>', self.move)
        canvas.tag_bind(self.draggable_alert, '<ButtonRelease-1>', self.release)
        canvas.tag_bind(self.draggable_name, '<Button1-Motion>', self.move)
        canvas.tag_bind(self.draggable_name, '<ButtonRelease-1>', self.release)
        canvas.tag_bind(self.draggable_img, '<Button1-Motion>', self.move)
        canvas.tag_bind(self.draggable_img, '<ButtonRelease-1>', self.release)
        canvas.configure(cursor="hand1")
        self.move_flag = False

        
         
    def move(self, event):
        
        if self.move_flag:
            new_xpos = event.x
            new_ypos = event.y
            self.x = new_xpos
            self.y = new_ypos
            
            if self.is_wireless:
                self.canvas.move(self.draggable_coverage_area_circle,
                    new_xpos-self.mouse_xpos ,new_ypos-self.mouse_ypos)

                self.canvas.move(self.draggable_signal_circle,
                    new_xpos-self.mouse_xpos ,new_ypos-self.mouse_ypos)

            self.canvas.move(self.draggable_name,
                new_xpos-self.mouse_xpos ,new_ypos-self.mouse_ypos)

            self.canvas.move(self.draggable_alert,
                new_xpos-self.mouse_xpos ,new_ypos-self.mouse_ypos)

            self.canvas.move(self.draggable_img,
                new_xpos-self.mouse_xpos ,new_ypos-self.mouse_ypos)

            self.mouse_xpos = new_xpos
            self.mouse_ypos = new_ypos
        else:
            self.move_flag = True
            if self.is_wireless:
                self.canvas.tag_raise(self.draggable_coverage_area_circle) 
                self.canvas.tag_raise(self.draggable_signal_circle)
            self.canvas.tag_raise(self.draggable_img)
            self.canvas.tag_raise(self.draggable_name)
            self.canvas.tag_raise(self.draggable_alert)
            self.mouse_xpos = event.x
            self.mouse_ypos = event.y

 
    def release(self, event):
        self.move_flag = False

    """
    def propagate_signal(self):
        self.canvas.itemconfig(self.draggable_signal_circle, outline="red")
        
        # The circle signal starts with raio 1 and propagates to raio 100. - Rafael Sampaio
        if self.signal_radius > 0 and self.signal_radius < self.coverage_area_radius:
            self.signal_radius += 1
            self.canvas.coords(self.draggable_signal_circle, self.x+self.signal_radius, self.y+self.signal_radius, self.x-self.signal_radius, self.y-self.signal_radius)
            
            # signal propagation event occurs at 10 milliseconds. - Rafael Sampaio
            self.canvas.after(1, self.propagate_signal)
        else:
            # Cleaning propagated signal for restore the signal draw. - Rafael Sampaio
            self.canvas.itemconfig(self.draggable_signal_circle, outline = "")
            self.signal_radius = 1
    """
    
    def set_coverage_area_radius(self, radius):
        self.coverage_area_radius = radius

    

