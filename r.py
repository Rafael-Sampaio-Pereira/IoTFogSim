import random

import tkinter as tk

# --- constants --- # UPPERCASE name

RES_X = 800
RES_Y = 600

# --- classes --- # CamelCase name 

class Enemy(object):
    '''single enemy'''

    def __init__(self, canvas):

        # access to canvas
        self.canvas = canvas

        self.radius = 12.5 # random

        self.color = random.choice( ('black', 'red', 'green', 'blue', 'yellow') )

        self.x = random.uniform(self.radius, RES_X-self.radius)
        self.y = random.uniform(self.radius, RES_Y-self.radius)

        self.x1 = self.x-self.radius
        self.y1 = self.y-self.radius

        self.x2 = self.x+self.radius
        self.y2 = self.y+self.radius

        self.oval = self.canvas.create_oval(self.x1, self.y1, self.x2, self.y2, fill=self.color, outline=self.color)

        self.moving = True

        self.start()


    def start(self):
        '''start moving'''

        self.moving = True

        # move this enemy after random time
        random_time = random.randint(150, 3000)
        root.after(random_time, self.move)


    def stop(self):
        '''stop moving'''

        self.moving = False


    def move(self):

        if self.moving: # to stop root.after

            direction = random.randint(1,4)

            if direction == 1: # up
                self.y -= self.radius
                self.y1 -= self.radius
                self.y2 -= self.radius
            elif direction == 2: # down
                self.y += self.radius
                self.y1 += self.radius
                self.y2 += self.radius
            elif direction == 3: # left
                self.x -= self.radius
                self.x1 -= self.radius
                self.x2 -= self.radius
            elif direction == 4: # right
                self.x += self.radius
                self.x1 += self.radius
                self.x2 += self.radius

            self.canvas.coords(self.oval, self.x1, self.y1, self.x2, self.y2)
            # move this enemy after random time
            random_time = random.randint(150, 3000)
            root.after(random_time, self.move)

# --- functions --- # lower_case name 

def add_new_enemy():

    enemies.append(Enemy(canvas))

    # add next enemy after random time
    timer = random.randint(150, 3000)
    root.after(random_time, add_new_enemy)

# --- main ---

root = tk.Tk()
root.title("")

canvas = tk.Canvas(root, width=RES_X, height=RES_Y, bg="white")
canvas.pack()

# 5 enemies at the beginning
enemies = list()

for _ in range(5):
    enemies.append(Enemy(canvas))

# add new enemy after random time
random_time = random.randint(150, 3000)
root.after(random_time, add_new_enemy)

root.mainloop()