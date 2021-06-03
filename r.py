# from tkinter import *
# from random import randint

# class Ball:
#     def __init__(self, canvas, x1, y1, x2, y2):
#         self.x1 = x1
#         self.y1 = y1
#         self.x2 = x2
#         self.y2 = y2
#         self.canvas = canvas
#         self.ball = canvas.create_oval(self.x1, self.y1, self.x2, self.y2, fill="red")

#     def move_ball(self):
#         deltax = randint(0,5)
#         deltay = randint(0,5)
#         self.canvas.move(self.ball, deltax, deltay)
#         self.canvas.after(50, self.move_ball)

# # initialize root Window and canvas
# root = Tk()
# root.title("Balls")
# root.resizable(False,False)
# canvas = Canvas(root, width = 1000, height = 1000)
# canvas.pack()

# # create two ball objects and animate them
# ball1 = Ball(canvas, 10, 10, 30, 30)
# ball2 = Ball(canvas, 60, 60, 80, 80)

# ball1.move_ball()
# ball2.move_ball()

# root.mainloop()






# from tkinter import *
# from random import randint
# from twisted.internet.task import LoopingCall
# from twisted.internet import tksupport
# from twisted.internet import reactor

# class Ball:
#     def __init__(self, canvas, x1, y1, x2, y2):
#         self.x1 = x1
#         self.y1 = y1
#         self.x2 = x2
#         self.y2 = y2
#         self.canvas = canvas
#         self.deltax = 0
#         self.deltay = 0
#         self.ball = canvas.create_oval(self.x1, self.y1, self.x2, self.y2, fill="red")

#         self.main_lp = LoopingCall(self.move_ball, 10,10) # 150 apenas para fins de desenvlvimento
#         self.main_lp.start(0.1)

#     def move_ball(self, destiny_x, destiny_y):
#         if self.deltax >= destiny_x and self.deltay >= destiny_y:
#             self.main_lp.stop()
#         if self.deltax < destiny_x:
#             self.deltax = self.deltax + 1
#         if self.deltay < destiny_y:
#             self.deltay = self.deltay + 1
        
        

#         self.canvas.move(self.ball, (self.deltax-destiny_x)**2, (self.deltay-destiny_y)**2)
#         # self.canvas.after(50, self.move_ball)


# def main():

#     def  update_position_on_screen( event, canvas):
#       # sertting the coordinates to canvas relative. by default it is window realative and don't change when window is scrolled - Rafael Sampaio
#       x = canvas.canvasx(event.x)
#       y = canvas.canvasy(event.y)

#     p = "Position: "+str(x)+' x '+str(y)
#     print(p)
#     # initialize root Window and canvas
#     root = Tk()
#     tksupport.install(root)
#     root.title("Balls")
#     root.resizable(False,False)
#     canvas = Canvas(root, width = 1000, height = 1000)
#     canvas.pack()

#     # create two ball objects and animate them
#     ball1 = Ball(canvas, 5, 5, 10, 10)
#     ball2 = Ball(canvas, 105, 105, 110, 110)

#     root.bind("<Motion>", lambda e: update_position_on_screen(canvas=canvas, event=e))

    

#     # ball1.move_ball()
#     # ball2.move_ball()


# if __name__ == '__main__':
#     main()
#     reactor.run()






from tkinter import *
import tkinter
from random import randint
from twisted.internet.task import LoopingCall
from twisted.internet import tksupport
from twisted.internet import reactor
import math
import time

from bresenham import bresenham



class Ball:
    def __init__(self, canvas, x1, y1, color):
        self.x1 = x1
        self.y1 = y1
        self.destiny_x = 900
        self.destiny_y = 900
        self.canvas = canvas
        self.ball = canvas.create_oval(self.x1, self.y1, self.x1+7, self.y1+7, fill=color)
        self.all_coordinates = list(bresenham(self.x1, self.y1, self.destiny_x, self.destiny_y))
        self.display_time = 9 # time that the packege ball still on the screen after get the destinantion - Rafael Sampaio
        self.package_speed = 2 # this determines the velocity of the packet moving in the canvas - Rafael Sampaio

        self.animate_package()


    def animate_package(self):
        cont = 100
        for x, y in self.all_coordinates:
            # verify if package ball just got its destiny - Rafael Sampaio
            if x == self.destiny_x and y == self.destiny_y:
                self.canvas.after(cont+self.display_time,self.canvas.delete, self.ball)

            self.canvas.after(cont, self.canvas.coords, self.ball, x, y, x+7, y+7) # 7 is the package ball size - Rafael Sampaio
            cont = cont + self.package_speed
            






def main():

    def  update_position_on_screen( event, canvas):
        # sertting the coordinates to canvas relative. by default it is window realative and don't change when window is scrolled - Rafael Sampaio
        x = canvas.canvasx(event.x)
        y = canvas.canvasy(event.y)

        p = "Position: "+str(x)+' x '+str(y)
        print(p)


    # initialize root Window and canvas
    root = Tk()
    tksupport.install(root)
    root.title("Balls")
    
    root.resizable(False,False)
    canvas = Canvas(root, width = 1000, height = 1000)
    canvas.pack()

    # create two ball objects and animate them
    # ball1 = Ball(canvas, 5, 5, 10, 10, "black")
    ball2 = Ball(canvas, 20, 20, "red")

    root.bind("<Motion>", lambda e: update_position_on_screen(canvas=canvas, event=e))


if __name__ == '__main__':
    main()
    reactor.run()


