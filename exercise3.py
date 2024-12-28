from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.graphics import Ellipse, Color, Rectangle
from kivy.clock import Clock
from kivy.vector import Vector
from random import randint


# This widget will hold the game logic
class MyWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Set window size for the game area
        self.height = Window.size[1]
        self.width = Window.size[0]
        
        # Initialize variables for player worm
        self.length_of_worm = 3  # Number of parts of the worm's body
        self.worm_width = 50  # Size of each part of the worm
        self.boost = False  # For potential speed boost
        self.speed = self.worm_width  # The movement speed of the worm
        self.direction = 1  # Direction of movement (1:right, 2:left, 3:up, 4:down)

        # A list to hold all the player's body parts (head + body segments)
        self.elements = []

        # Graphics: Add shapes to represent game objects
        with self.canvas:
            # Draw background color
            Color(0.2, 0.3, 0.7, 0.5)
            Rectangle(pos=(0, 0), size=(self.width, self.height))

            # Set color for the worm's body
            Color(0.4, 0.8, 0.2, 1)

            # Create the worm's body (head + body segments)
            for i in range(self.length_of_worm):
                # Create an Ellipse for each body part and add it to the list
                element = Ellipse(pos=(self.width / 2 - i * self.worm_width, self.height / 2),
                                  size=(self.worm_width, self.worm_width))
                self.elements.append(element)

            # Create a food object (random position)
            Color(0.5, 0, 0, 1)  # Red color for the food
            self.food = Ellipse(pos=(randint(0, self.width - 50), randint(0, self.height - 50)), size=(50, 50))

            # Create an enemy object (random position)
            Color(1, 0, 0, 1)  # Red color for the enemy
            self.enemy = Ellipse(pos=(randint(0, self.width - 50), randint(0, self.height - 50)), size=(50, 50))

        # Setup keyboard controls for the player
        self.keyboard = Window.request_keyboard(self.on_keyboard_closed, self)
        self.keyboard.bind(on_key_down=self.on_key_down)

        # Schedule the update method to run every 1/20th of a second
        Clock.schedule_interval(self.update, 1 / 20)

    # Method to handle when the keyboard is closed
    def on_keyboard_closed(self):
        self.keyboard.unbind(self.on_key_down)
        self.keyboard = None

    # Method to handle keypresses
    def on_key_down(self, keyboard, keycode, text, modifier):
        # Change the direction based on arrow key pressed
        if keycode[1] == 'right':
            self.direction = 1
        elif keycode[1] == 'left':
            self.direction = 2
        elif keycode[1] == 'up':
            self.direction = 3
        elif keycode[1] == 'down':
            self.direction = 4

    # Main game loop, called every 1/20th of a second
    def update(self, dt):
        # Move all body segments to follow the head
        for i in range(len(self.elements) - 1, 0, -1):
            self.elements[i].pos = self.elements[i - 1].pos  # Each segment takes the position of the one before it

        # Move the head based on the direction
        head_pos = self.elements[0].pos
        if self.direction == 1:  # Moving right
            self.elements[0].pos = (head_pos[0] + self.speed, head_pos[1])
        elif self.direction == 2:  # Moving left
            self.elements[0].pos = (head_pos[0] - self.speed, head_pos[1])
        elif self.direction == 3:  # Moving up
            self.elements[0].pos = (head_pos[0], head_pos[1] + self.speed)
        elif self.direction == 4:  # Moving down
            self.elements[0].pos = (head_pos[0], head_pos[1] - self.speed)

        # Screen wrapping logic
        if self.elements[0].pos[0] > self.width:  # If the worm goes off the right side
            self.elements[0].pos = (0, head_pos[1])  # Reappear on the left side
        elif self.elements[0].pos[0] < 0:  # If the worm goes off the left side
            self.elements[0].pos = (self.width, head_pos[1])  # Reappear on the right side
        elif self.elements[0].pos[1] > self.height:  # If the worm goes off the top
            self.elements[0].pos = (head_pos[0], 0)  # Reappear at the bottom
        elif self.elements[0].pos[1] < 0:  # If the worm goes off the bottom
            self.elements[0].pos = (head_pos[0], self.height)  # Reappear at the top

        # Move the enemy toward the player's head
        self.move_enemy()

        # Check for collision between the player and the enemy
        self.check_collision(self.elements[0], self.enemy)

    # Method to make the enemy follow the player
    def move_enemy(self):
        # Get the position of the player's head (first segment)
        player_head = self.elements[0].pos

        # Get the current position of the enemy
        enemy_pos = self.enemy.pos

        # Calculate the direction vector from the enemy to the player's head
        direction_vector = Vector(player_head) - Vector(enemy_pos)

        # Set the speed of the enemy
        step_size = 2  # Enemy speed

        # If the enemy is far from the player, move closer
        if direction_vector.length() > step_size:
            direction_vector = direction_vector.normalize() * step_size

        # Update the enemy's position by moving in the direction of the player
        self.enemy.pos = Vector(enemy_pos) + direction_vector

    # Method to check if the player has collided with the enemy
    def check_collision(self, r1, r2):
        # Get positions and sizes of player and enemy objects
        x1, y1 = r1.pos
        w1, h1 = r1.size
        x2, y2 = r2.pos
        w2, h2 = r2.size

        # Check for overlap in positions (simple collision detection)
        if x1 < x2 + w2 and x1 + w1 > x2 and y1 < y2 + h2 and y1 + h1 > y2:
            print("Collision with enemy! Resetting Game...")
            self.reset_game()  # Reset the game on collision

    # Method to reset the worm and enemy positions
    def reset_game(self):
        # Reset worm position to a random place on the screen
        for i in range(self.length_of_worm):
            new_pos = (randint(0, self.width - self.worm_width), randint(0, self.height - self.worm_width))
            self.elements[i].pos = new_pos

        # Reset enemy position to a random place
        self.enemy.pos = (randint(0, self.width - 50), randint(0, self.height - 50))


# Main Kivy App class
class MyApp(App):
    def build(self):
        return MyWidget()  # Load the game widget when the app starts


# Run the game when the script is executed
if __name__ == '__main__':
    MyApp().run()


"""
self.elements = []
Initializes an empty list that will hold the worm's body segments (head and body).

Graphics Setup
with self.canvas:
Begins drawing elements on the widget's canvas.

Color(0.2, 0.3, 0.7, 0.5)
Sets a background color (light blue).

Rectangle(pos=(0, 0), size=(self.width, self.height))
Fills the entire window with the defined background color by drawing a rectangle.

Color(0.4, 0.8, 0.2, 1)
Sets the color for the worm's body (green).

for i in range(self.length_of_worm):
Loops through the number of worm segments to create the worm.

element = Ellipse(pos=(self.width / 2 - i * self.worm_width, self.height / 2), size=(self.worm_width, self.worm_width))
Creates an ellipse for each worm segment and positions them at the center of the window.

self.elements.append(element)
Adds each ellipse (worm segment) to the list of worm body parts.

Color(0.5, 0, 0, 1)
Sets the color of the food object (red).

self.food = Ellipse(pos=(randint(0, self.width - 50), randint(0, self.height - 50)), size=(50, 50))
Creates a randomly positioned food object using an ellipse.

Color(1, 0, 0, 1)
Sets the color for the enemy (bright red).

self.enemy = Ellipse(pos=(randint(0, self.width - 50), randint(0, self.height - 50)), size=(50, 50))
Creates a randomly positioned enemy object.

Keyboard Setup and Game Loop
self.keyboard = Window.request_keyboard(self.on_keyboard_closed, self)
Requests the keyboard to capture key events.

self.keyboard.bind(on_key_down=self.on_key_down)
Binds the on_key_down method to handle key presses.

Clock.schedule_interval(self.update, 1 / 20)
Schedules the update method to run 20 times per second (game loop).

Event Handling and Logic
def on_keyboard_closed(self):
Handles what happens when the keyboard is closed.

self.keyboard.unbind(self.on_key_down)
Unbinds the keyboard when it’s closed.

def on_key_down(self, keyboard, keycode, text, modifier):
Handles keypress events to change the worm's direction based on arrow keys.

if keycode[1] == 'right': self.direction = 1
If the right arrow key is pressed, sets the direction to move right.

elif keycode[1] == 'left': self.direction = 2
If the left arrow key is pressed, sets the direction to move left.

elif keycode[1] == 'up': self.direction = 3
If the up arrow key is pressed, sets the direction to move up.

elif keycode[1] == 'down': self.direction = 4
If the down arrow key is pressed, sets the direction to move down.

Main Game Loop
def update(self, dt):
This is the main game loop that updates the game state. It runs every 1/20th of a second.

for i in range(len(self.elements) - 1, 0, -1): self.elements[i].pos = self.elements[i - 1].pos
Moves each body segment to follow the position of the one before it, making the worm move.

if self.direction == 1: self.elements[0].pos = (head_pos[0] + self.speed, head_pos[1])
Moves the head to the right if the direction is set to 1.

elif self.direction == 2: self.elements[0].pos = (head_pos[0] - self.speed, head_pos[1])
Moves the head to the left if the direction is set to 2.

elif self.direction == 3: self.elements[0].pos = (head_pos[0], head_pos[1] + self.speed)
Moves the head upward if the direction is set to 3.

elif self.direction == 4: self.elements[0].pos = (head_pos[0], head_pos[1] - self.speed)
Moves the head downward if the direction is set to 4.

if self.elements[0].pos[0] > self.width: self.elements[0].pos = (0, head_pos[1])
Implements screen wrapping: if the worm goes off the right side, it reappears on the left.

elif self.elements[0].pos[0] < 0: self.elements[0].pos = (self.width, head_pos[1])
If the worm goes off the left side, it reappears on the right.

self.move_enemy()
Calls the move_enemy method to make the enemy follow the player.

self.check_collision(self.elements[0], self.enemy)
Checks for collisions between the worm's head and the enemy.

Enemy Movement
def move_enemy(self):
Moves the enemy toward the player’s head.

direction_vector = Vector(player_head) - Vector(enemy_pos)
Calculates the vector pointing from the enemy to the player's head.

if direction_vector.length() > step_size: direction_vector = direction_vector.normalize() * step_size
If the enemy is far from the player, normalize the direction vector and move the enemy closer.

self.enemy.pos = Vector(enemy_pos) + direction_vector
Updates the enemy's position.

Collision Detection and Game Reset
def check_collision(self, r1, r2):
Checks if two rectangles (the player and the enemy) overlap.

**`if x1 < x2 + w2 and x1 + w1 > x2 and y1 <



"""