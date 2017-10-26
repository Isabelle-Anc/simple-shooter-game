import Tkinter # Python graphics library
import random # for random events that I am yet to implement
import math # for square roots, used in collision detection
import string # for the alphabet string used for enemy id

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
    def check_collision(self):
        for game_object in game_objects:
            if game_object.__class__.__name__ == "Bullet":
                if canvas.bbox(self, string.ascii_lowercase[counter]) != None:
                    enemy_cors = canvas.bbox(self, string.ascii_lowercase[counter])
                    if math.sqrt((self.x-(enemy_cors[0]+10))**2 + (self.y-(enemy_cors[1]+10))**2) <= 20:
                        print("Enemy"), (self.id), ("was hit")

    
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
        global id_tags
        global dead_list
    
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

def draw(canvas):
    # draw loop
    canvas.delete(Tkinter.ALL)

    global game_objects
    for game_object in game_objects:
        game_object.update()
        game_object.draw(canvas)
    
    canvas.addtag_enclosed("delete", 0, 0, -400, -100)

    delay = 33
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

if __name__ == '__main__':

    root = Tkinter.Tk()
    canvas = Tkinter.Canvas(root, width=400, height=400, background="black")
    canvas.pack()

    root.bind('<Key-a>', move_left)
    root.bind('<Key-d>', move_right)
    root.bind('<Key-s>', player_shoot)
    
    create_player()
    
    # creates the arrangement of enemies
    pos = 37.5
    for i in range(5):
        create_enemy(pos, 50, string.ascii_lowercase[i])
        pos += 75

    pos = 75
    for i in range(4):
        create_enemy(pos, 100, string.ascii_lowercase[i+5])
        pos += 75

    pos = 37.5
    for i in range(5):
        create_enemy(pos, 150, string.ascii_lowercase[i+9])
        pos += 75
    
    # start the draw loop
    draw(canvas)
    
    root.mainloop() # keep the window open
''' Ideally, this is how the collision detection code would work:
    Every enemy would take its coordinates and put them in a place accessible to the bullet. Each bullet would then compare the coordinates to the enemy's using pythag and fun things like that.'''