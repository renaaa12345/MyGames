from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.graphics import Ellipse, Color, Rectangle
from kivy.clock import Clock
from kivy.vector import Vector

class MyWidget(Widget): 
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.height = Window.height
        self.width = Window.width
        self.length_of_worm = 20
        self.worm_width = 50
        self.direction = Vector(1, 0)  # Initial movement to the right (vector)
        self.speed_increaser = 1  # Initial speed increaser
        self.move_amount = self.worm_width  # the amount worm moves in one step, equal to the worm's width.

        with self.canvas:
            self.keyboard = Window.request_keyboard(self.on_keyboard_closed, self)
            self.keyboard.bind(on_key_down=self.on_key_down)
            self.keyboard.bind(on_key_up=self.on_key_up)
            
            Clock.schedule_interval(self.update, 1/20)  # Update 20 times per second
            
            Color(0.2, 0.3, 0.7, 1)
            Rectangle(pos=(0, 0), size=(self.width, self.height))  # Background
            
            Color(0.4, 0.8, 0.2, 1)
            self.elements = []  # Array to store worm parts like birzo did 
            
            # worm
            for i in range(self.length_of_worm): #Loops to create all the worm segments.
                source = "./images/head_right.png" if i == 0 else "./images/body.png"
                #i represents the index of the segment in the loop. For the head (when i = 0), this value is 0 * self.worm_width, placing the head at the center of the screen. For subsequent segments, it offsets each segment to the left by one worm segment width (self.worm_width), ensuring the worm’s body segments follow the head.
                element = Ellipse(source=source, pos=(self.width / 2 - i * self.worm_width, self.height / 2), size=(self.worm_width, self.worm_width))
                #Draws an elliptical worm segment at a calculated position. The head is centered in the window, and each body segment is placed to the left of the previous one.
                self.elements.append(element) #Stores each segment in the elements list.
    
    def on_keyboard_closed(self): 
        self.keyboard.unbind(self.on_key_down)
        self.keyboard = None
    
    def on_key_down(self, keyboard, keycode, text, modifier): 
        
        if keycode[1] == 'right':
            self.direction = Vector(1, 0)
        elif keycode[1] == 'left':
            self.direction = Vector(-1, 0)
        elif keycode[1] == 'up':
            self.direction = Vector(0, 1)
        elif keycode[1] == 'down':
            self.direction = Vector(0, -1)
        
        # Reset speed increaserr when you press keyy
        self.speed_increaser = 1
    
    def on_key_up(self, keyboard, keycode):
        # Increase speed when the key is released
        if keycode[1] in ['right', 'left', 'up', 'down']:
            self.speed_increaser += 0.5  # I Increased the speed when i leave thwe key
    
    def update(self, dt):
        # Update the worm's body segments (tail follows head)
        for i in range(len(self.elements) - 1, 0, -1):
            self.elements[i].pos = self.elements[i - 1].pos
        
        # Update the head based on the vector and speed
        move_vector = self.direction * self.move_amount * self.speed_increaser
        #is calculating how much the worm should move in its current direction, based on the speed and distance it moves.
        head_pos = Vector(*self.elements[0].pos) + move_vector #this tells the worm to move from where it currently is to its new position based on the direction and speed.
        #self.elements[0].pos is where the worm's head currently is. The position is made up of two values: x (left-right) and y (up-down).
        # asteriks is Python's unpacking operator, which splits the tuple (x, y) into two separate values. So the line creates a new vector using the values from the position of the worm's head.

        # Wrap around the screen if the worm moves out of bounds
        if head_pos[0] >= self.width: #If the worm’s head goes too far right (off the screen), it reappears on the left side.
            head_pos[0] = 0
        elif head_pos[0] < 0:
            head_pos[0] = self.width - self.worm_width #The subtraction of self.worm_width ensures the worm doesn’t go past the right edge.
        if head_pos[1] >= self.height:
            head_pos[1] = 0
        elif head_pos[1] < 0:
            head_pos[1] = self.height - self.worm_width #head_pos[0] and head_pos[1] represent the x-coordinate and y-coordinate of the worm's head, respectively.
        
        # Setting new position for the head
        self.elements[0].pos = head_pos
        
        # Update the image source for the head based on direction
        if self.direction == Vector(1, 0):
            self.elements[0].source = "./images/head_right.png"
        elif self.direction == Vector(-1, 0):
            self.elements[0].source = "./images/head_left.png"
        elif self.direction == Vector(0, 1):
            self.elements[0].source = "./images/head_up.png"
        elif self.direction == Vector(0, -1):
            self.elements[0].source = "./images.head_down.png"

class MyApp(App): 
    def build(self): 
        return MyWidget() 

if __name__ == '__main__':
    myApp = MyApp()
    myApp.run()

    #A Vector object allows you to easily add or subtract positions. By converting the position of the worm’s head to a vector, you can perform vector math (like adding movement to the current position) in a straightforward way.
    #Let’s say the worm’s head is at position (100, 200), and it moves 10 units to the right.
    # Current position: (100, 200)
    """After unpacking: *self.elements[0].pos gives us 100, 200.
    Creating a vector: Vector(100, 200) makes the current position a Vector.
    Adding movement: Adding another vector (for movement) to this will give the new position in a simple way, like Vector(100, 200) + Vector(10, 0) results in the new position Vector(110, 200)."""
