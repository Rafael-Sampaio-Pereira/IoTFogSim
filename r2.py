from tkinter import *
import random
import time


class Ball:
    def __init__(self, canvas,square):
        self.square = square
        self.canvas = canvas
        self.id = canvas.create_oval(10,10,25,25,fill='red')
        self.canvas.move(self.id,245,100)
        self.text = self.canvas.create_text(10, 10, text='GAME OVER', font=('Courier', 80))
        self.canvas.move(self.text, -7000, -7000)
        starts = [-3,-2,-1,1,2,3]
        self.x = random.choice(starts)
        self.y = -30
    def draw(self):
        self.canvas.move(self.id,self.x,self.y)
        pos = self.canvas.coords(self.id)
        if pos[1] <= 0:
            self.y = 4
        if pos[3] >= self.canvas.winfo_height():
            self.y = -4
        if self.hit_square(pos) == True:
            self.canvas.move(self.text,245,100)
            time.sleep(2)
            tk.destroy()
        if pos[0] <= 0:
            self.x = 4
        if pos[2] >= self.canvas.winfo_width():
            self.x = -4
    def hit_square(self, pos):
        square_pos = self.canvas.coords(self.square.id)
        if pos[2] >= square_pos[0] and pos[0] <= square_pos[2]:
            if pos[3] >= square_pos[1] and pos[3] <= square_pos[3]:
                return True
        return False
    def stay(self):
        self.x = 0
        self.y = 0
class Square:
    def __init__(self,canvas):
        self.canvas = canvas
        self.id = canvas.create_rectangle(15, 15, 30, 30,fill='green')
        self.x = 0
        self.y = 0
        self.canvas.move(self.id, 200, 250)
        self.canvas.bind_all('<KeyPress-Left>',self.left)
        self.canvas.bind_all('<KeyPress-Right>', self.right)
        self.canvas.bind_all('<KeyPress-Up>', self.up)
        self.canvas.bind_all('<KeyPress-Down>', self.down)
    def draw(self):
        self.canvas.move(self.id,self.x,self.y)
        pos = self.canvas.coords(self.id)
        if pos[0] <= 0:
            self.x = 0
        elif pos[2] >= self.canvas.winfo_width():
            self.x = 0
        if pos[1] <= 0:
            self.y = 0
        elif pos[3] >= self.canvas.winfo_height():
            self.y = 0
    def left(self, evt):
        self.x = -2
        self.y = 0
    def right(self, evt):
        self.x = 2
        self.y = 0
    def up(self, evt):
        self.y = -2
        self.x = 0
    def down(self, evt):
        self.y = 2
        self.x = 0
class Triangle:
    def __init__(self,canvas,square):
        self.canvas = canvas
        self.square = square
        self.id = self.canvas.create_polygon(26.5,10,20,25,35,25,fill='blue')
        self.canvas.move(self.id,random.randint(10,450),random.randint(10,380))
        self.score = 0
    def draw_score(self):
        self.score_show = self.canvas.create_text(450, 20, text='score:' + str(self.score), font=('Arial', 20))
    def hit_square(self):
        pos = self.canvas.coords(self.id)
        square_pos = self.canvas.coords(self.square.id)
        if pos[2] >= square_pos[0] and pos[0] <= square_pos[2]:
            if pos[3] >= square_pos[1] and pos[3] <= square_pos[3]:
                self.teleport(pos)
    def teleport(self, pos):
        x = self.canvas.winfo_width()-pos[0]-10
        y = self.canvas.winfo_height() - pos[1]-10
        self.score += 1
        self.canvas.move(self.id,)
tk = Tk()
tk.title("Run from the ball!")
tk.resizable(0,0)
tk.wm_attributes('-topmost',1)
canvas = Canvas(tk, width=500,height=400,bd=0,highlightthickness=0)
canvas.pack()
tk.update()

square = Square(canvas)
ball = Ball(canvas, square)
ball1 = Ball(canvas, square)
ball2 = Ball(canvas, square)
ball3 = Ball(canvas, square)
ball4 = Ball(canvas, square)
triangle = Triangle(canvas, square)
x = 0
while x < float('inf'):
    ball.draw()
    triangle.draw_score()
    triangle.hit_square()
    if x >= 10:
        ball1.draw()
    if x >= 20:
        ball2.draw()
    if x >= 30:
        ball3.draw()
    if x >= 40:
        ball4.draw()
    square.draw()
    tk.update_idletasks()
    tk.update()
    time.sleep(0.01)
    x += 0.01