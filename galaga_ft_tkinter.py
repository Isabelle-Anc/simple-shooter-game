import Tkinter
import random
import time

game_objects = []

class Player:
    def __init__ (self, x, y):
        self.x = x
        self.y = y
    
    def update(self):
        self.placeholder = 1
    
    def draw(self, canvas):
        canvas.create_polygon(self.x, self.y, self.x-10, self.y+20, self.x+10, self.y+20, fill="red", outline="")

class Enemy:
    def __init__ (self, x, y):
        self.x = x
        self.y = y
        
        self.speed = 5
    
    def update(self):
        self.placeholder = 1
    
    def draw(self, canvas):
        canvas.create_oval(self.x-10, self.y-10, self.x+10, self.y+10, fill="green", outline="")

        
def create_player():
    '''Draws a new player ship'''

    global game_objects
    game_objects.append(Player(200, 300))

def create_enemy(x, y):
    '''Draws a new enemy alien'''
    
    global game_objects
    game_objects.append(Enemy(x, y))
    

def draw(canvas):
    '''Clear the canvas, have all game objects update and redraw, then set up the next draw.'''

    canvas.delete(Tkinter.ALL)

    global game_objects
    for game_object in game_objects:
        game_object.update()
        game_object.draw(canvas)

    delay = 33 # milliseconds, so about 30 frames per second
    canvas.after(delay, draw, canvas) # call this draw function with the canvas argument again after the delay

# this is a standard Python thing: definitions go above, and any code that will actually
# run should go into the __main__ section. This way, if someone imports the file because
# they want to use the functions or classes you've defined, it won't start running your game
# automatically

create_player()
pos = 50

for i in range(5):
    create_enemy(pos, 75)
    pos =+ 50

if __name__ == '__main__':

    # create the graphics root and a 400x400 canvas
    root = Tkinter.Tk()
    canvas = Tkinter.Canvas(root, width=400, height=400, background="black")
    canvas.pack()
    
    # start the draw loop
    draw(canvas)
    
    root.mainloop() # keep the window open