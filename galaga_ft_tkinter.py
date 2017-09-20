import Tkinter
import random
import time

game_objects = []
xPos = 200

class Player:
    def __init__ (self, x, y):
        global xPos
        self.x = xPos
        self.y = y
    
    def update(self):
        self.x = xPos
    
    def draw(self, canvas):
        canvas.create_polygon(self.x, self.y, self.x-10, self.y+20, self.x+10, self.y+20, fill="red", outline="")

class Enemy:
    def __init__ (self, x, y):
        self.x = x
        self.y = y
        
        self.speed = 2
        self.counter = 0
    
    def update(self):
        self.x += self.speed
        self.counter += 1
        
        if self.counter == 12:
            self.counter = 0
            self.speed = self.speed * -1
    
    def draw(self, canvas):
        canvas.create_oval(self.x-10, self.y-10, self.x+10, self.y+10, fill="green", outline="")

class Bullet:
    def __init__ (self, x, y):
        self.x = x
        self.y = y
        
        self.speed = 10
    
    def update(self):
        self.x += self.speed
    
    def draw(self, canvas):
        canvas.create_oval(self.x-3, self.y-3, self.x+3, self.y+3, fill="white", outline="")
    

def create_player():
    global game_objects
    game_objects.append(Player(200, 350))

def create_enemy(x, y):
    global game_objects
    game_objects.append(Enemy(x, y))

def create_bullet(x, y):
    global game_objects
    game_objects.append(Bullet(x, y))

def playerShoot(event, x, y):
    global xPos
    create_bullet(xPos+10, 350)

    

def draw(canvas):
    # Clear the canvas, have all game objects update and redraw, then set up the next draw.

    canvas.delete(Tkinter.ALL)

    global game_objects
    for game_object in game_objects:
        game_object.update()
        game_object.draw(canvas)

    delay = 33 # milliseconds, so about 30 frames per second
    canvas.after(delay, draw, canvas) # call this draw function with the canvas argument again after the delay

def moveLeft(event):
    global xPos
    xPos -= 20

def moveRight(event):
    global xPos
    xPos += 20

create_player()

pos = 37.5
for i in range(5):
    create_enemy(pos, 50)
    pos += 75

pos = 75
for i in range(4):
    create_enemy(pos, 100)
    pos += 75

pos = 37.5
for i in range(5):
    create_enemy(pos, 150)
    pos += 75

if __name__ == '__main__':

    # create the graphics root and a 400x400 canvas
    root = Tkinter.Tk()
    canvas = Tkinter.Canvas(root, width=400, height=400, background="black")
    canvas.pack()
    
    root.bind('<Key-a>', moveLeft)
    root.bind('<Key-d>', moveRight)
    root.bind(',Key-s>', playerShoot)
    
    # start the draw loop
    draw(canvas)
    
    root.mainloop() # keep the window open