from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.graphics import Line, Ellipse, Color, Rectangle
from kivy.uix.label import Label
from kivy.clock import Clock
from random import randint  
from kivy.vector import Vector
from random import uniform
class MyWidget(Widget):
   
   def __init__(self, **kwargs):
       self.window_height = Window.height
       self.window_width = Window.width
       self.time_for_fresh_food = 4
       length_of_worm = 3
       self.worm_width = 50
       self.fruit_size = 30
       self.speed = self.worm_width
       self.boost = False
       self.boosted_speed = self.speed # * 2
       self.regular_speed = self.speed
       self.collision = False
       self.rotten_fruits = []
       self.direction = 1 # 1 is right, 2 is left, 3 is up, 4 is down
       super().__init__(**kwargs)
       with self.canvas:
           self.keyboard = Window.request_keyboard(self.on_keyboard_closed, self) # mandatory: callback function closes the keyboard input after we close the app
           self.keyboard.bind(on_key_down = self.on_key_down)
           self.keyboard.bind(on_key_up = self.on_key_up)
           Clock.schedule_interval(self.update, 1/20)
           Color(0.3, 0.8, 0.4, 0.95)
           Rectangle(pos=(0,0), size=(self.window_width, self.window_height))
           Color(1, 0.7, 0.7, 1)
           self.worm_parts = []
           for i in range(length_of_worm):
               if i == 0:
                   self.source = "./Images/head_right.png"
               else:
                   self.source = "./Images/full_body.png"
               worm_part= Ellipse(source=self.source,pos=(self.window_width/2 - i*self.worm_width, self.window_height/2), size=(self.worm_width, self.worm_width))
               self.worm_parts.append(worm_part)
           Color(0.7,0.1,0.2,1)
           self.fruit = Rectangle(pos=(uniform(0,self.window_width - self.fruit_size), uniform(0,self.window_height-self.fruit_size)), size=(self.fruit_size,self.fruit_size))
           self.fruit_timer = Clock.schedule_once(self.rot_fruit, self.time_for_fresh_food)

   def on_keyboard_closed(self):
       self.keyboard.unbind(self.on_key_down) # Unbind key(?)
       self.keyboard.unbind(self.on_key_up)
       self.keyboard = None # Destroy keyboard

   def on_key_down(self, keyboard, keycode, text, modifier): # text gives the letter you press, keycode gives tuple of id and keyname
       for i in range(len(self.worm_parts) -1, -1, -1): # start on the last ellispe, end at 0, and go in reverse
           if i != 0: 
               self.worm_parts[i].pos = self.worm_parts[i-1].pos
           else:
               if keycode[1] == 'right' or keycode[1] == 'd':
                   self.direction = 1
                   self.boost = True
                   self.speed = self.boosted_speed
               elif keycode[1] == 'left' or keycode[1] == 'a':
                   self.direction = 2
                   self.boost = True
                   self.speed = self.boosted_speed
               elif keycode[1] == 'up'or keycode[1] == 'w':
                   self.direction = 3
                   self.boost = True
                   self.speed = self.boosted_speed
               elif keycode[1] == 'down'or keycode[1] == 's':
                   self.direction = 4
                   self.boost = True
                   self.speed = self.boosted_speed

   def on_key_up(self, keyboard, keycode):
       if keycode[1] == 'right' or keycode[1] == 'left' or keycode[1] == 'up' or keycode[1] == 'down':
           self.boost = False
           self.speed = self.regular_speed
           

   def update(self, dl):
       for i in range(len(self.worm_parts) -1, -1, -1): # start on the last ellispe, end at 0, and go in reverse
           if i != 0:
               if self.boost:
                   if self.direction == 1:
                       self.worm_parts[i].pos = (self.worm_parts[i-1].pos[0]+(self.boosted_speed-self.regular_speed), self.worm_parts[i-1].pos[1])
                   elif self.direction == 2: 
                       self.worm_parts[i].pos = (self.worm_parts[i-1].pos[0]-(self.boosted_speed-self.regular_speed), self.worm_parts[i-1].pos[1])
                   elif self.direction == 3:
                       self.worm_parts[i].pos = (self.worm_parts[i-1].pos[0], self.worm_parts[i-1].pos[1]+(self.boosted_speed-self.regular_speed))
                   elif self.direction == 4:
                       self.worm_parts[i].pos = (self.worm_parts[i-1].pos[0], self.worm_parts[i-1].pos[1]-(self.boosted_speed-self.regular_speed))
               else:
                   self.worm_parts[i].pos = (self.worm_parts[i-1].pos[0], self.worm_parts[i-1].pos[1])

           else:
               # Check direction
               if self.direction == 1:
                   self.worm_parts[0].source = "./Images/head_right.png"
                   self.worm_parts[i].pos = (self.worm_parts[i].pos[0] + self.speed, self.worm_parts[i].pos[1])
               elif self.direction == 2:
                   self.worm_parts[0].source = "./Images/head_left.png"
                   self.worm_parts[i].pos = (self.worm_parts[i].pos[0] - self.speed, self.worm_parts[i].pos[1])
               elif self.direction == 3:
                   self.worm_parts[0].source  = "./Images/head_up.png"
                   self.worm_parts[i].pos = (self.worm_parts[i].pos[0], self.worm_parts[i].pos[1] + self.speed)
               elif self.direction == 4:
                   self.worm_parts[0].source  = "./Images/head_down.png"
                   self.worm_parts[i].pos = (self.worm_parts[i].pos[0], self.worm_parts[i].pos[1] - self.speed)
               
               # Check out of frame
               if self.worm_parts[i].pos[0] >= self.window_width:
                   self.worm_parts[i].pos = (0, self.worm_parts[i].pos[1])
               elif self.worm_parts[i].pos[0] < 0:
                   self.worm_parts[i].pos = (self.window_width, self.worm_parts[i].pos[1])
               elif self.worm_parts[i].pos[1] >= self.window_height:
                   self.worm_parts[i].pos = (self.worm_parts[i].pos[0], 0)
               elif self.worm_parts[i].pos[1] < 0:
                   self.worm_parts[i].pos = (self.worm_parts[i].pos[0], self.window_height)

               # Check collision
               fruit_collision = self.check_collision(self.worm_parts[i], self.fruit)
               if fruit_collision:
                   self.fruit.pos = (uniform(0,self.window_width - self.fruit_size), uniform(0,self.window_height-self.fruit_size)) #This ensures that the fruit appears randomly within the horizontal space, but not outside the window’s boundaries.
                   self.fruit_timer.cancel()
                   self.fruit_timer = Clock.schedule_once(self.rot_fruit, self.time_for_fresh_food)
                   with self.canvas:
                       self.source = "./Images/full_body.png"
                       Color(1, 0.7, 0.7, 1)
                       worm_part= Ellipse(source=self.source,pos=(self.window_width/2 - self.worm_parts[-1].pos[0]*self.worm_width, self.window_height/2), size=(self.worm_width, self.worm_width))
                       self.worm_parts.append(worm_part)

               for y in self.rotten_fruits:
                   if self.check_collision(self.worm_parts[i], y):
                       obstacle_collision = self.check_collision(self.worm_parts[i], y)
                       if obstacle_collision:
                           self.canvas.remove(self.worm_parts.pop())
          
   def check_collision(self, r1, r2):
       x1, y1 = r1.pos
       w1, h1 = r1.size

       x2, y2 = r2.pos
       w2, h2= r2.size

       if x1 < x2 + w2 and x1 + w1 > x2 and y1 < y2 + h2 and y1 + h1 > y2:
           return True
       else: 
           return False

   def rot_fruit(self,dl):
       with self.canvas:
           Color(0.3, 0, 0, 1)
           rotten_fruit = Rectangle(pos=(self.fruit.pos[0], self.fruit.pos[1]), size=(self.fruit_size,self.fruit_size))
           self.rotten_fruits.append(rotten_fruit)
       self.fruit.pos = (uniform(0,self.window_width - self.fruit_size), uniform(0,self.window_height-self.fruit_size))
       self.fruit_timer.cancel()
       self.fruit_timer = Clock.schedule_once(self.rot_fruit, self.time_for_fresh_food)

       
class MyApp(App):
   def build(self):
       return MyWidget()


if __name__ == '__main__':
   myApp = MyApp()
   myApp.run()

"""
self.time_for_fresh_food = 4
length_of_worm = 3
self.worm_width = 50
self.fruit_size = 30
self.speed = self.worm_width
self.boost = False
self.boosted_speed = self.speed
self.regular_speed = self.speed
self.collision = False
self.rotten_fruits = []
self.direction = 1  # 1 = right, 2 = left, 3 = up, 4 = down

These lines initialize different game settings:
time_for_fresh_food: The time until the fruit rots.
worm_width: The size of the worm's body parts.
fruit_size: The size of the fruit.
speed: The speed of the worm.
boost: A flag to indicate whether the worm is moving faster.
boosted_speed: Faster speed when boost is active.
direction: The direction the worm is moving (right, left, up, or down).
rotten_fruits: A list to store rotten fruits in the game.


Drawing the Worm and Fruit

with self.canvas:
This line opens the canvas, which is where visual elements like the worm and fruit are drawn.
python
Copy code
self.keyboard = Window.request_keyboard(self.on_keyboard_closed, self)
self.keyboard.bind(on_key_down=self.on_key_down)
self.keyboard.bind(on_key_up=self.on_key_up)
These lines request access to the keyboard and bind key press and key release events to their respective functions.


Clock.schedule_interval(self.update, 1/20)
This schedules the update function to run 20 times per second (for game updates).



Color(0.3, 0.8, 0.4, 0.95)
Rectangle(pos=(0,0), size=(self.window_width, self.window_height))
This sets the background color and draws a rectangle (the background) the size of the window.
python
Copy code
self.worm_parts = []
for i in range(length_of_worm):
    if i == 0:
        self.source = "./Images/head_right.png"
    else:
        self.source = "./Images/full_body.png"
    worm_part = Ellipse(source=self.source, pos=(self.window_width/2 - i*self.worm_width, self.window_height/2), size=(self.worm_width, self.worm_width))
    self.worm_parts.append(worm_part)

This creates the worm’s body. The worm starts in the middle of the window, and each Ellipse represents one part of the worm (the head and the body).
python
Copy code
self.fruit = Rectangle(pos=(uniform(0,self.window_width - self.fruit_size), uniform(0,self.window_height-self.fruit_size)), size=(self.fruit_size,self.fruit_size))
self.fruit_timer = Clock.schedule_once(self.rot_fruit, self.time_for_fresh_food)
This creates the fruit at a random position within the window and starts a timer to change the fruit to rotten after time_for_fresh_food seconds.
Handling Keyboard Input
python
Copy code
def on_keyboard_closed(self):
This function unbinds the keyboard when it’s closed.
python
Copy code
def on_key_down(self, keyboard, keycode, text, modifier):
This function handles key presses. Depending on the key (right, left, up, down), it changes the direction of the worm and boosts the speed.
python
Copy code
def on_key_up(self, keyboard, keycode):
This function is triggered when a key is released, and it resets the speed to regular.
Updating the Game
python
Copy code
def update(self, dl):
This function is called every time the game updates (about 20 times per second).
python
Copy code
for i in range(len(self.worm_parts) - 1, -1, -1):
This loop goes through each part of the worm from the last one to the first one. The movement of the worm is updated based on its direction and speed.
python
Copy code
self.worm_parts[i].pos = (self.worm_parts[i-1].pos[0], self.worm_parts[i-1].pos[1])
Each part of the worm follows the position of the part in front of it (the head).
Movement and Collision
python
Copy code
if self.direction == 1:
    self.worm_parts[0].source = "./Images/head_right.png"
    self.worm_parts[i].pos = (self.worm_parts[i].pos[0] + self.speed, self.worm_parts[i].pos[1])
This section moves the worm based on its current direction and speed. The head also changes to an image representing the direction.
python
Copy code
if fruit_collision:
    self.fruit.pos = (uniform(0,self.window_width - self.fruit_size), uniform(0,self.window_height - self.fruit_size))
If the worm eats a fruit (i.e., the worm collides with the fruit), the fruit is repositioned randomly, and the worm grows by one part.
Rotten Fruit
python
Copy code
def rot_fruit(self, dl):
This function creates a rotten fruit if the timer runs out. The rotten fruits will act as obstacles for the worm.
Collision Detection
python
Copy code
def check_collision(self, r1, r2):
This function checks if two objects (like the worm and the fruit) overlap by comparing their positions and sizes.
Main App
python
Copy code
class MyApp(App):
    def build(self):
        return MyWidget()
This creates the MyApp class and returns MyWidget as the root widget of the app.
python
Copy code
if __name__ == '__main__':
    myApp = MyApp()
    myApp.run()
This runs the app if the script is executed directly.
Summary
This is a simple snake-like game where a worm moves around the screen, and the player controls the direction with the keyboard. The worm eats fruit to grow, and the fruit appears randomly on the screen. If the worm collides with a rotten fruit, it shrinks. The game keeps updating based on the keyboard input and collision detection.






The provided code snippet seems to be part of a worm game where a worm's head and body parts move in response to user input, and it handles boundary conditions for wrapping around the screen edges. Let’s break down the logic behind each part of the code and provide tips for understanding it better, especially if you have a quiz.

Code Logic Explanation
Direction Handling: The first part of the code uses an if-elif statement to determine the direction in which the worm is moving, as indicated by the self.direction variable:

python
Copy code
if self.direction == 1:  # Moving right
    self.worm_parts[0].source = "./Images/head_right.png"  # Update head image
    self.worm_parts[i].pos = (self.worm_parts[i].pos[0] + self.speed, self.worm_parts[i].pos[1])  # Move right
elif self.direction == 2:  # Moving left
    self.worm_parts[0].source = "./Images/head_left.png"  # Update head image
    self.worm_parts[i].pos = (self.worm_parts[i].pos[0] - self.speed, self.worm_parts[i].pos[1])  # Move left
elif self.direction == 3:  # Moving up
    self.worm_parts[0].source  = "./Images/head_up.png"  # Update head image
    self.worm_parts[i].pos = (self.worm_parts[i].pos[0], self.worm_parts[i].pos[1] + self.speed)  # Move up
elif self.direction == 4:  # Moving down
    self.worm_parts[0].source  = "./Images/head_down.png"  # Update head image
    self.worm_parts[i].pos = (self.worm_parts[i].pos[0], self.worm_parts[i].pos[1] - self.speed)  # Move down
Each direction (1 to 4) corresponds to a movement (right, left, up, down) for the worm.
The worm's head image changes depending on the current direction to visually represent where the worm is heading.
The pos attribute of each worm part is updated to reflect its new position based on the speed of movement.
Wrapping Logic: The second part of the code checks if any part of the worm goes out of the window's boundaries and wraps it around to the other side:

python
Copy code
# Check out of frame
if self.worm_parts[i].pos[0] >= self.window_width:
    self.worm_parts[i].pos = (0, self.worm_parts[i].pos[1])  # Wrap around to the left
elif self.worm_parts[i].pos[0] < 0:
    self.worm_parts[i].pos = (self.window_width, self.worm_parts[i].pos[1])  # Wrap around to the right
elif self.worm_parts[i].pos[1] >= self.window_height:
    self.worm_parts[i].pos = (self.worm_parts[i].pos[0], 0)  # Wrap around to the top
elif self.worm_parts[i].pos[1] < 0:
    self.worm_parts[i].pos = (self.worm_parts[i].pos[0], self.window_height)  # Wrap around to the bottom
This logic checks the position of each part of the worm (self.worm_parts[i].pos) against the window's dimensions (self.window_width and self.window_height).
If a part of the worm exceeds the window boundaries, it is repositioned to the opposite side, creating a seamless wrap-around effect.
Tips for Understanding and Working Through This Logic
Visualize the Movement:

Sketch out how the worm moves on a grid or in a coordinate system. This can help you understand how changing the position works.
Use diagrams to illustrate how the wrapping works when the worm moves out of bounds.
Break Down the Direction Logic:

Write down the conditions for each direction and what happens in each case. This can solidify your understanding of how movement is implemented.
Consider using print statements (e.g., print(self.direction)) to debug and track which direction is being processed when you run your game.
Understand Coordinate Systems:

Familiarize yourself with how 2D coordinates work. The origin (0,0) is typically the top-left corner of the window.
Understand how changes to self.pos affect the worm's position on the screen.
Wrap-Around Logic Practice:

Create a small function or pseudo-code to simulate the wrap-around logic separately to see how it behaves.
Test scenarios where the worm is close to the edges to ensure you grasp the concept of boundary conditions.


"""