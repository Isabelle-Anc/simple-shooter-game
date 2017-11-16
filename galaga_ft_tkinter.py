# To do list:
# -Win/lose condition
# -Lambdas (see comment in 1st project check-in)
# -Bring window to front and have as active application
# -Bullets not going through enemies
# -Enemies being the ones creating the bullets? Seems like a better way to organize
# -More comments!

import Tkinter # Python graphics library
import random # for random events
import math # for square roots, used in collision detection
import string # alphabet string is used for creating enemy ids
import abc # abstract base class

# globals- I need to fix
game_objects = []
x_pos = 200

game_state = None

class Game_Object:
    __metaclass__ = abc.ABCMeta
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.is_alive = True
        self.game_state = True
    
    @abc.abstractmethod
    def draw(self, canvas):
        pass
    
    @abc.abstractmethod
    def update(self, canvas):
        pass
    
    def life_check(self):
        return self.is_alive
    
    @staticmethod
    def win_check(self):
        global game_state
        for game_object in game_objects:
            if game_object.__class__.__name__ == "Player" and game_object.life_check() == False:
                game_state = "Loss"
            # elif game_object.__class__.__name__ == "Enemy"
#                 and game_object.life_check() == False:
#                 game_state = "Win"

            # currently detects if an enemy is dead, need to detect if ALL are
            # funny, it's easier to implement losing than winning.
        return game_state
    
class Player(Game_Object):
    def __init__ (self, x, y):
        Game_Object.__init__(self, x, y)
        global x_pos
        self.x = x_pos
        self.bullet_cors = None
    
    def update(self):
        self.x = x_pos
        
        for game_object in game_objects:
            if game_object.__class__.__name__ == "Enemy_Bullet":
                self.bullet_cors = game_object.get_cors()
                if math.sqrt((self.x-(self.bullet_cors[0]))**2 +
                (self.y-(self.bullet_cors[1]+10))**2) <= 15:
                    self.x = 420
                    self.y = 420
                    self.is_alive = False
    
    def draw(self, canvas):
        canvas.create_polygon(self.x, self.y, self.x-10, self.y+20, self.x+10, self.y+20, fill="red", outline="")

class Enemy(Game_Object):
    def __init__ (self, x, y, id):
        Game_Object.__init__(self, x, y)
        self.id = id
        
        self.speed = 1
        self.counter = 0
    
    def update(self):
        self.x += self.speed
        self.counter += 1
        
        if self.counter == 24:
            self.counter = 0
            self.speed = self.speed * -1
        
        # collision detection
        for game_object in game_objects:
            if game_object.__class__.__name__ == "Bullet":
                self.bullet_cors = game_object.get_cors()
                if math.sqrt((self.x-(self.bullet_cors[0]))**2 +
                (self.y-(self.bullet_cors[1]+10))**2) <= 15:
                    self.x = 420
                    self.y = 420
                    self.is_alive = False
        
        # shooting
        if random.randint(1, 100) == 100 and self.y != 400:
            game_objects.append(Enemy_Bullet(self.x, self.y))
    
    def draw(self, canvas):
        canvas.create_oval(self.x-10, self.y-10, self.x+10, self.y+10,
            fill="green", outline="", tags=self.id)

class Bullet(Game_Object):
    def __init__ (self, x, y):
        Game_Object.__init__(self, x, y)
        
        self.speed = -5
    
    def update(self):
        self.y += self.speed
    
    def draw(self, canvas):
        canvas.create_oval(self.x-3, self.y-3, self.x+3, self.y+3,
            fill="yellow", outline="", tags="bullet")
    
    def get_cors(self):
        return(self.x, self.y)

class Enemy_Bullet(Bullet):
    def update(self):
        self.y -= self.speed
    
    def draw(self, canvas):
        canvas.create_rectangle(self.x-3, self.y-3, self.x+3, self.y+3,
            fill="white", outline="", tags="bullet")

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
        if game_object.life_check() == True:
            game_object.update()
            game_object.draw(canvas)
    
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
    for game_object in game_objects:
        if game_object.__class__.__name__ == "Player" and game_object.life_check() == True:
            create_bullet(x_pos, 350)

# this will only run in the original program, not if this file is imported
if __name__ == '__main__': 

    root = Tkinter.Tk()
    canvas = Tkinter.Canvas(root, width=400, height=400, background="black")
    canvas.pack()
    root.attributes("-topmost", True)
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
    
    game_state = "Playing"
    # start the draw loop
    draw(canvas)

    root.mainloop() # keep the window open