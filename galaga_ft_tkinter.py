# To do list: (in no particular order)
# -Lambdas to remove globals (see comment in 1st project check-in)
# -Have as active application when the program starts
# -Bullets not going through enemies
# -Enemies being the ones creating the bullets- seems like a better way to organize
# -More comments, so people know what I'm doing!

import Tkinter # Python graphics library
import random # for random events
import math # for square roots, used in collision detection
import abc # abstract base class

# I just need one element from each of these libraries
from string import ascii_lowercase # alphabet string is used for creating enemy ids
from time import sleep # to incorporate delays

game_objects = [] # list that holds all of the game objects- used as global
x_pos = 200 # x position of the player- used as global

game_state = "Playing" # keeps track of win conditions

class Game_Object:
    # creates a generic game object
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
    def win_check():
        global game_state
        alive_counter = 0
        for game_object in game_objects:
            if (game_object.__class__.__name__ == "Player" and
                game_object.life_check() == False):
                game_state = "Loss"
            elif (game_object.__class__.__name__ == "Enemy" and
                game_object.life_check() == True):
                alive_counter += 1
        if alive_counter == 0:
            game_state = "Win"
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
        canvas.create_polygon(self.x, self.y, self.x-10, self.y+20, self.x+10, self.y+20, 
            fill="red", outline="")

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
        
        # each frame the enemy has a 1% chance of shooting a bullet
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
            fill="yellow", outline="")
    
    def get_cors(self):
        return(self.x, self.y)

class Enemy_Bullet(Bullet):
    def update(self):
        self.y -= self.speed
    
    def draw(self, canvas):
        canvas.create_rectangle(self.x-3, self.y-3, self.x+3, self.y+3,
            fill="white", outline="")

def create_player():
    global game_objects
    game_objects.append(Player(200, 350))

def create_enemy(x, y, id):
    global game_objects
    game_objects.append(Enemy(x, y, id))

def create_bullet(x, y):
    global game_objects
    game_objects.append(Bullet(x, y))

def draw(canvas): # draw loop
    DELAY = 33  # The one constant variable in my code!
                # Unless the canvas count and root count?
    canvas.delete(Tkinter.ALL)
    
    global game_objects
    for game_object in game_objects:
        if game_object.life_check() == True:
            game_object.update()
            game_object.draw(canvas)
    
    global game_state
    game_state = Game_Object.win_check()
    
    if game_state == "Playing":
        # call this draw function with the canvas argument again after the delay
        # as long as the game is still going
        canvas.after(DELAY, draw, canvas)
    else:
        canvas.delete(Tkinter.ALL)
        if game_state == "Win":
            canvas.create_text(200, 200, text="u did gud", fill="white",
                font=("ubuntu", 24))
        elif game_state == "Loss":
            canvas.create_text(200, 200, text="u ded", fill="white",
                font=("ubuntu", 24))

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
        if (game_object.__class__.__name__ == "Player" and
            game_object.life_check() == True):
            create_bullet(x_pos, 350)

def start_game(event):
    global game_state
    if game_state == "Waiting":
        game_state = "Playing"
        for text_item in ["a and d keys to move", "press s to shoot", "3", "2", "1"]:
            canvas.delete(Tkinter.ALL)
            canvas.create_text(200, 200, text=text_item, fill="white",
                font=("ubuntu", 24))
            sleep(1)
        draw(canvas)

# this will only run in the original program, not if this file is imported for classes
if __name__ == '__main__': 

    root = Tkinter.Tk()
    canvas = Tkinter.Canvas(root, width=400, height=400, background="black")
    canvas.pack()
    root.attributes("-topmost", True)
    root.bind('<Key-a>', move_left)
    root.bind('<Key-d>', move_right)
    root.bind('<Key-s>', player_shoot)
    root.bind('<Button-1>', start_game)
    
    create_player()
    
    # creates the arrangement of enemies
    pos = 37.5
    for i in range(5):
        create_enemy(pos, 50, ascii_lowercase[i])
        pos += 75
    
    pos = 75
    for i in range(4):
        create_enemy(pos, 100, ascii_lowercase[i+5])
        pos += 75
    
    pos = 37.5
    for i in range(5):
        create_enemy(pos, 150, ascii_lowercase[i+9])
        pos += 75
    
    game_state = "Waiting"
    canvas.create_text(200, 200, text="click to begin", fill="white",
                font=("ubuntu", 24))

    root.mainloop() # keep the window open