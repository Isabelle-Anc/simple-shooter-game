# Yay it's Galaga
# It's pretty much done for now

import Tkinter # Python graphics library
import random # for random events
import math # for square roots, used in collision detection
import abc # abstract base class

# next three variables are used as globals for now
game_objects = [] # list that holds all of the game objects
x_pos = 200 # x position of the player
game_state = "Playing" # keeps track of win conditions

class Game_Object:
    # creates a generic game object
    __metaclass__ = abc.ABCMeta
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.is_alive = True
        self.game_state = True
    
    # these next two methods are run every frame
    @abc.abstractmethod
    def draw(self, canvas):
        # draws object on canvas
        pass
    
    @abc.abstractmethod
    def update(self, canvas):
        # does anything
        pass
    
    def life_check(self):
        # returns whether or not the object is alive, used for detecting win conditions
        return self.is_alive
    
    def delete(self):
        # technically doesn't delete to avoid indexing errors (all of the objects are in a
        # list; it just moves the object offscreen
        self.x = 420
        self.y = 420
        self.is_alive = False
    
    def check_collision(self, object_type, target_number):
        # checks if the object has collided with another
        for game_object in game_objects:
            if game_object.__class__.__name__ == object_type:
                self.object_cors = game_object.get_cors()
                if math.sqrt((self.x-(self.object_cors[0]))**2 +
                    (self.y-(self.object_cors[1]+10))**2) <= target_number:
                    # deletes both objects that have collided
                    self.delete()
                    game_object.delete()
    
    @staticmethod
    def win_check():
        # checks if the player has won or lost the game
        global game_state
        alive_counter = 0
        for game_object in game_objects:
            # if the player is dead you lose the game
            if (game_object.__class__.__name__ == "Player" and
                game_object.life_check() == False):
                game_state = "Loss"
            # if none of the enemies remain alive you win
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
        self.check_collision("Enemy_Bullet", 12)
    
    def draw(self, canvas):
        canvas.create_polygon(self.x, self.y-10, self.x-10, self.y+10,
            self.x+10, self.y+10, fill="red", outline="")

class Enemy(Game_Object):
    def __init__ (self, x, y):
        Game_Object.__init__(self, x, y)
        self.speed = 1
        self.counter = 0
    
    def update(self):
        self.x += self.speed
        self.counter += 1
        
        if self.counter == 24:
            self.counter = 0
            self.speed = self.speed * -1
        
        self.check_collision("Bullet", 13)
        
        # each frame each enemy has a 1% chance of shooting a bullet
        if random.randint(1, 100) == 100 and self.y != 400:
            game_objects.append(Enemy_Bullet(self.x, self.y))
    
    def draw(self, canvas):
        canvas.create_oval(self.x-10, self.y-10, self.x+10, self.y+10,
            fill="green", outline="")

class Bullet(Game_Object):
    def __init__ (self, x, y):
        Game_Object.__init__(self, x, y)
        
        self.speed = -3
    
    def update(self):
        self.y += self.speed
        self.check_collision("Enemy_Bullet", 6)
    
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

def create_enemy(x, y):
    global game_objects
    game_objects.append(Enemy(x, y))

def create_bullet(x, y):
    global game_objects
    game_objects.append(Bullet(x, y))

def draw(canvas): # draw loop
    global game_state
    DELAY = 33
    canvas.delete(Tkinter.ALL)
    
    global game_objects
    for game_object in game_objects:
        if game_object.life_check() == True:
            game_object.update()
            game_object.draw(canvas)
    
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

def move_left(x_pos):
    if x_pos > 20:
        x_pos -= 10
    return x_pos

def move_right(event):
    global x_pos
    if x_pos < 380:
        x_pos += 10

def player_shoot(event):
    global x_pos
    for game_object in game_objects:
        if (game_object.__class__.__name__ == "Player" and
            game_object.life_check() == True):
            create_bullet(x_pos, 350)

def start_game(event):
    # runs once the player starts the game
    global game_state
    if game_state == "Waiting":
        game_state = "Writing"
        
        # the blank item provides a buffer and gets around some of the weird display stuff
        TEXT_ITEMS = ["a and d keys to move", "press s to shoot", "3", "2", "1", ""]
        
        def write_on_canvas(item_number):
            canvas.delete(Tkinter.ALL)
            canvas.create_text(200, 200, text=TEXT_ITEMS[item_number], fill="white",
                font=("ubuntu", 24))
            if item_number < (len(TEXT_ITEMS)-1):
                canvas.after(1000, write_on_canvas, item_number+1)
            else:
                global game_state
                game_state = "Playing"
                draw(canvas)
        write_on_canvas(0)

# this will only run in the original program, not if this file is imported into
# another program

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
    game_state = "Waiting"
    canvas.create_text(200, 200, text="click to begin", fill="white",
        font=("ubuntu", 24))

    root.mainloop() # keep the window open