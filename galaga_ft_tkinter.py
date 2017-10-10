import Tkinter
import random
import time
import math

game_objects = []
id_tags = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n"]
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
    def __init__ (self, x, y, id):
        self.x = x
        self.y = y
        self.id = id
        
        self.speed = 1
        self.counter = 0
    
    def update(self):
        self.x += self.speed
        self.counter += 1
        
        if self.counter == 24:
            self.counter = 0
            self.speed = self.speed * -1
        return self.x
        return self.y
    
    def draw(self, canvas):
        canvas.create_oval(self.x-10, self.y-10, self.x+10, self.y+10, fill="green", outline="", tags=self.id)

class Bullet:
    def __init__ (self, x, y):
        self.x = x
        self.y = y
        
        self.speed = -5
    
    def update(self):
        self.y += self.speed
        global game_objects
        counter = 0
#         self_cors = canvas.bbox(self, *need tag for this bullet*)
        self_cors = canvas.bbox(self, "bullet")
#         canvas.gettags(self, "bullet")
        for game_object in game_objects:
            if "Enemy" in str(game_object):
                enemy_cors = canvas.bbox(self, id_tags[counter])
#                 print (str(self_cors)) + (",") + (str(enemy_cors))
#                 if enemy_cors - self.x) <= 20 and abs(Enemy.y - self.y) <= 20:
#                     print(Enemy.y)
#                     print(self.y)
                counter += 1
    
    def draw(self, canvas):
        canvas.create_oval(self.x-3, self.y-3, self.x+3, self.y+3, fill="white", outline="", tags="bullet")

def create_player():
    global game_objects
    game_objects.append(Player(200, 350))

def create_enemy(x, y, id):
    global game_objects
    game_objects.append(Enemy(x, y, id))

def create_bullet(x, y):
    global game_objects
    game_objects.append(Bullet(x, y))
    print len(game_objects)
    print 


def draw(canvas):
    # Clear the canvas, have all game objects update and redraw, then set up the next draw.

    canvas.delete(Tkinter.ALL)

    global game_objects
    for game_object in game_objects:
        game_object.update()
        game_object.draw(canvas)
    
    canvas.addtag_enclosed("delete", 0, 0, -400, -100)

    delay = 33 # milliseconds, so about 30 frames per second
    canvas.after(delay, draw, canvas) # call this draw function with the canvas argument again after the delay

def move_left(event):
    global xPos
    if xPos > 20:
        xPos -= 20

def move_right(event):
    global xPos
    if xPos < 380:
        xPos += 20

def player_shoot(event):
    global xPos
    create_bullet(xPos, 350)

create_player()

pos = 37.5
for i in range(5):
    create_enemy(pos, 50, id_tags[i])
    pos += 75

pos = 75
for i in range(4):
    create_enemy(pos, 100, id_tags[i+5])
    pos += 75

pos = 37.5
for i in range(5):
    create_enemy(pos, 150, id_tags[i+9])
    pos += 75


if __name__ == '__main__':

    # create the graphics root and a 400x400 canvas
    root = Tkinter.Tk()
    canvas = Tkinter.Canvas(root, width=400, height=400, background="black")
    canvas.pack()

    root.bind('<Key-a>', move_left)
    root.bind('<Key-d>', move_right)
    root.bind('<Key-s>', player_shoot)
    
    # start the draw loop
    draw(canvas)
    
    root.mainloop() # keep the window open