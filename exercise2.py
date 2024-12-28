from kivy.app import App  # Import the base App class from Kivy, which is required to run a Kivy application
from kivy.uix.widget import Widget  # Import the Widget class to define the main interactive area
from kivy.uix.label import Label  # Import Label to display text (currently unused but can be for future UI)
from kivy.core.window import Window  # Import Window to manage window properties like width and height
from kivy.graphics import Ellipse, Color, Rectangle  # Import Ellipse, Color, Rectangle for drawing shapes and adding colors
from kivy.clock import Clock  # Import Clock to schedule regular updates to the game (movement)
from random import randint  # Import randint to generate random integers (currently unused)
from random import uniform  # Import uniform to generate random floating-point numbers (used for random positions)

# Define a class that inherits from Widget to create our game interface
class MyWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)  # Initialize the base Widget class
        self.width = Window.width  # Set the widget width equal to the window width
        self.height = Window.height  # Set the widget height equal to the window height
        self.ellipse_width = 70  # Width (and height) of the ellipse (circle)
        self.speed = 10  # Speed at which the ellipse moves
        self.direction = None  # Variable to store the direction of movement (starts as None)
        self.collision = False  # Tracks if a collision happens (not actively used here)
        self.food_size = 30  # Size of the food rectangle (smaller than the ellipse)

        # Create the keyboard control setup to listen for key presses
        self.keyboard = Window.request_keyboard(self.on_keyboard_closed, self)  # Request access to the keyboard
        self.keyboard.bind(on_key_down=self.on_key_down)  # Bind key press events to the on_key_down method
        self.keyboard.bind(on_key_up=self.on_key_up)  # Bind key release events to the on_key_up method

        # Create the ellipse (circle) at the center of the screen
        with self.canvas:
            Color(1, 0, 0, 0.9)  # Set the color of the ellipse (red with some transparency)
            self.ellipse = Ellipse(pos=(Window.width/2, Window.height/2), size=(self.ellipse_width, self.ellipse_width))  # Draw the ellipse

            Color(0, 1, 0, 1)  # Set the color of the food (green)
            self.food = Rectangle(pos=(uniform(0, self.width - self.food_size), uniform(0, self.height - self.food_size)), size=(self.food_size, self.food_size))  # Place the food rectangle at a random position on the screen

        # Call the update method 20 times per second to handle movement and game logic
        Clock.schedule_interval(self.update, 1 / 20)

    def on_keyboard_closed(self):
        # When the keyboard is closed, unbind the key events
        self.keyboard.unbind(on_key_down=self.on_key_down)
        self.keyboard = None  # Set the keyboard object to None

    def on_key_down(self, keyboard, keycode, text, modifiers):
        # Handle the direction based on the key pressed (arrow keys)
        if keycode[1] == 'right':  # Right arrow key
            self.direction = 'right'
        elif keycode[1] == 'left':  # Left arrow key
            self.direction = 'left'
        elif keycode[1] == 'up':  # Up arrow key
            self.direction = 'up'
        elif keycode[1] == 'down':  # Down arrow key
            self.direction = 'down'

    def on_key_up(self, keyboard, keycode):
        # When any arrow key is released, stop the movement
        if keycode[1] in ['right', 'left', 'up', 'down']:
            self.direction = None  # Reset direction to None (stops movement)

    def update(self, dt):
        # Update the position of the ellipse based on the current direction
        if self.direction:
            x, y = self.ellipse.pos  # Get the current position of the ellipse (x, y)

            if self.direction == 'right':  # If moving right
                x += self.speed  # Increase x to move right
                if x > self.width - self.ellipse.size[0]:  # Check if the ellipse is beyond the window's right edge
                    x = self.width - self.ellipse.size[0]  # Keep it within bounds
            elif self.direction == 'left':  # If moving left
                x -= self.speed  # Decrease x to move left
                if x < 0:  # Check if the ellipse is beyond the window's left edge
                    x = 0  # Keep it within bounds
            elif self.direction == 'up':  # If moving up
                y += self.speed  # Increase y to move up
                if y > self.height - self.ellipse.size[1]:  # Check if the ellipse is beyond the window's top edge
                    y = self.height - self.ellipse.size[1]  # Keep it within bounds
            elif self.direction == 'down':  # If moving down
                y -= self.speed  # Decrease y to move down
                if y < 0:  # Check if the ellipse is beyond the window's bottom edge
                    y = 0  # Keep it within bounds

            self.ellipse.pos = (x, y)  # Update the position of the ellipse

            # Check if the ellipse has collided with the food
            fruit_collision = self.check_collision(self.ellipse, self.food)
            if fruit_collision:  # If a collision happens
                self.food.pos = (uniform(0, self.width - self.food_size), uniform(0, self.height - self.food_size))  # Move the food to a new random position
                with self.canvas:  # Change the color of the ellipse (optional visual effect)
                    Color(1, 0.7, 0.7, 1)

    def check_collision(self, e1, e2):
        # Check if two objects (e1 and e2) are colliding (using bounding boxes)
        x1, y1 = e1.pos  # Position of the first object (ellipse)
        w1, h1 = e1.size  # Size of the first object

        x2, y2 = e2.pos  # Position of the second object (food)
        w2, h2 = e2.size  # Size of the second object

        # Collision detection logic (checks if the objects' bounding boxes overlap)
        if x1 < x2 + w2 and x1 + w1 > x2 and y1 < y2 + h2 and y1 + h1 > y2:
            return True  # Collision happened
        else:
            return False  # No collision

# Main App class that runs the application
class MyApp(App):
    def build(self):
        return MyWidget()  # Return the MyWidget class as the root widget

# Entry point for the application
if __name__ == '__main__':
    MyApp().run()  # Run the app
