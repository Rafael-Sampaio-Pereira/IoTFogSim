import tkinter as tk

# --- constants ---

WIDTH = 800
HEIGHT = 1000

# --- functions ---

# for smooth move of platform

def left_press(event):
    global platform_left
    platform_left = True

def left_release(event):
    global platform_left
    platform_left = False

def right_press(event):
    global platform_right
    platform_right = True

def right_release(event):
    global platform_right
    platform_right = False


def eventloop():
    global xspeed
    global yspeed

    # move ball
    canvas.move(ball, xspeed, yspeed)
    ball_pos = canvas.coords(ball)

    # move platform
    if platform_left:
        # move
        canvas.move(platform, -20, 0)
        platform_pos = canvas.coords(platform)
        # check if not leave canvas
        if platform_pos[0] < 0:
            # move back
            canvas.move(platform, 0-platform_pos[0], 0)
    if platform_right:
        # move
        canvas.move(platform, 20, 0)
        # check if not leave canvas
        platform_pos = canvas.coords(platform)
        if platform_pos[2] > 1200:
            # move back
            canvas.move(platform, -(platform_pos[2]-1200), 0)

    # - collisions -

    # check collision with border

    if ball_pos[3] >= 900 or ball_pos[1] <= 0: # y range
        yspeed = -yspeed
    if ball_pos[2] >= 1200 or ball_pos[0] <= 0: # x range
        xspeed = -xspeed

    # check collisions with objects 

    collide = canvas.find_overlapping(*ball_pos)

    if platform in collide:
        yspeed = -yspeed

    remove = []

    # check collision with bricks
    for brick in bricks:
        if brick in collide:
            remove.append(brick)
            yspeed = -yspeed

    # remove bricks
    for brick in remove:
        bricks.remove(brick)
        canvas.delete(brick)

    root.after(10, eventloop)

# --- main ---

# - init -

root = tk.Tk()
root.title("Brick Breaker")

canvas = tk.Canvas(root, width=1200, height=900)
canvas.pack()

# - objects -

ball = canvas.create_oval(5, 5, 30, 30, fill="black")
xspeed = 1 # gravity
yspeed = 4

platform = canvas.create_rectangle(5, 40, 250, 30, fill="black")
platform_left = False
platform_right = False
root.bind('<Left>', left_press)
root.bind('<KeyRelease-Left>', left_release)
root.bind('<Right>', right_press)
root.bind('<KeyRelease-Right>', right_release)

bricks = []

for i in range(10):
    x = i*100
    y = 700
    brick = canvas.create_rectangle(x, y, x+50, y+30, fill="red")
    bricks.append(brick)

# - mainloop -

root.after(100, eventloop)
root.mainloop()