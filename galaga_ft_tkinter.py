import Tkinter # Python graphics library
import random # for random events that I am yet to implement
import math # for square roots, used in collision detection
import string # for the alphabet string used for enemy id

game_objects = []
x_pos = 200

class Player:
    def __init__ (self, x, y):
        global x_pos
        self.x = x_pos
        self.y = y
    
    def update(self):
        self.x = x_pos
    
    def draw(self, canvas):
        canvas.create_polygon(self.x, self.y, self.x-10, self.y+20, self.x+10, self.y+20, fill="red", outline="")

class Enemy:
    def __init__ (self, x, y, id):
        self.x = x
        self.y = y
        self.id = id
        
        self.speed = 1
        self.counter = 0
        self.bullet_bbox = None
    
    def update(self):
        self.x += self.speed
        self.counter += 1
        
        if self.counter == 24:
            self.counter = 0
            self.speed = self.speed * -1
    
    def check_collision(self):
        for game_object in game_objects:
            if game_object.__class__.__name__ == "Bullet":
                self.bullet_bbox = game_object.get_bbox()
                if math.sqrt((self.x-(self.bullet_bbox[0]+10))**2 +
                (self.y-(self.bullet_bbox[1]+10))**2) <= 20:
                    print("Enemy"), (self.id), ("was hit")
                self.counter += 1
    
    def draw(self, canvas):
        canvas.create_oval(self.x-10, self.y-10, self.x+10, self.y+10,
            fill="green", outline="", tags=self.id)

class Bullet:
    def __init__ (self, x, y):
        self.x = x
        self.y = y
        
        self.speed = -5
        self.bbox = None
        self.id = None
    
    def update(self):
        self.y += self.speed
    
    def draw(self, canvas):
        self.id = canvas.create_oval(self.x-3, self.y-3, self.x+3, self.y+3,
            fill="white", outline="", tags="bullet")
    
    def get_bbox(self):
        self.bbox = canvas.bbox(self, self.id)
        return self.bbox

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
        if game_object.__class__.__name__ == "Enemy":
            game_object.check_collision()
    
    delay = 33
    canvas.after(delay, draw, canvas) # call this draw function with the canvas argument again after the delay

def move_left(event):
    global x_pos
    if x_pos > 20:
        x_pos -= 20

def move_right(event):
    global x_pos
    if x_pos < 380:
        x_pos += 20

def player_shoot(event):
    global x_pos
    create_bullet(x_pos, 350)

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
    Every enemy would take its coordinates and put them in a place accessible to the 
    bullet. Each bullet would then compare the coordinates to the enemy's using pythag and 
    fun things like that.'''