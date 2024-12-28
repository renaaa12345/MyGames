from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.graphics import Ellipse, Color, Rectangle
from kivy.clock import Clock
from random import randint
from random import uniform

class MyWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.width = Window.width
        self.height = Window.height
        self.ellipse_width = 70
        self.speed = self.ellipse_width
        self.direction = None  # To store the direction of movement (None initially)
        self.collision = False
        self.food_size = 30

        # Create the keyboard controls
        self.keyboard = Window.request_keyboard(self.on_keyboard_closed, self)
        self.keyboard.bind(on_key_down=self.on_key_down)
        self.keyboard.bind(on_key_up=self.on_key_up)

        # Create the ellipse at a random position
        with self.canvas:
            Color(1, 0, 0, 0.9)
            self.ellipse = Ellipse (pos=(Window.width/2, Window.height/2), size= (self.ellipse_width, self.ellipse_width))

            Color(0, 1, 0, 1)
            self.food = Rectangle(pos=(uniform(0, self.width - self.food_size), uniform(0, self.height - self.food_size)), size=(self.food_size, self.food_size))
        
        
        # Call the update method repeatedly to move the ellipse based on key presses
        Clock.schedule_interval(self.update, 1 / 20)

    def on_keyboard_closed(self):
        self.keyboard.unbind(on_key_down=self.on_key_down)
        self.keyboard = None

    def on_key_down(self, keyboard, keycode, text, modifiers):
        # Handle direction based on key pressed
        if keycode[1] == 'right':
            self.direction = 'right'
        elif keycode[1] == 'left':
            self.direction = 'left'
        elif keycode[1] == 'up':
            self.direction = 'up'
        elif keycode[1] == 'down':
            self.direction = 'down'

    def on_key_up(self, keyboard, keycode):
        # Stop movement when the key is released
        if keycode[1] in ['right', 'left', 'up', 'down']:
            self.direction = None

    def update(self, dt):
        # Move the ellipse based on the direction
        if self.direction: #holds the current direction (like 'right', 'left', 'up', or 'down') based on which arrow key was pressed. If no direction is set (meaning no key is pressed), the movement won't happen.
            x, y = self.ellipse.pos #Here, we unpack the current pos (position) of the ellipse into two variables x and y, which represent the current x-coordinate and y-coordinate of the ellipse on the screen.
            if self.direction == 'right': #If true, it increases the x-coordinate (x += self.speed), moving the ellipse to the right by self.speed units.
            #It then checks if the new x position is beyond the right edge of the screen (x > self.width - self.ellipse.size[0]). If it is, the position is adjusted to the rightmost allowed point (x = self.width - self.ellipse.size[0]) so the ellipse stays within the window.
                x += self.speed
                if x > self.width - self.ellipse.size[0]:  # Keep within the window
                    x = 0
            elif self.direction == 'left':
                #If true, it decreases the x-coordinate (x -= self.speed), moving the ellipse to the left by self.speed units.
                #It then ensures that the ellipse doesn’t go off the left side of the screen by checking if x < 0. If it is less than 0, it resets the position to x = 0, keeping the ellipse within bounds.
                x -= self.speed
                if x < 0:
                    x = self.width - self.ellipse.size[0]
            elif self.direction == 'up':
                y += self.speed
                if y > self.height - self.ellipse.size[1]:
                    y = self.height - self.ellipse.size[1]
            elif self.direction == 'down':
                y -= self.speed
                if y < 0:
                    y = 0

            self.ellipse.pos = (x, y)
            fruit_collision = self.check_collision(self.ellipse, self.food)
            if fruit_collision:
                self.food.pos = (uniform(0,self.width - self.food_size), uniform(0,self.height-self.food_size))
                with self.canvas:
                       Color(1, 0.7, 0.7, 1)

    def check_collision(self, e1, e2):
       x1, y1 = e1.pos
       w1, h1 = e1.size

       x2, y2 = e2.pos
       w2, h2= e2.size

       if x1 < x2 + w2 and x1 + w1 > x2 and y1 < y2 + h2 and y1 + h1 > y2:
           return True
       else: 
           return False

       

class MyApp(App):
    def build(self):
        return MyWidget()

if __name__ == '__main__':
    MyApp().run()