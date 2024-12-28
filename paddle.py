# Import necessary modules from Kivy
from kivy.app import App  # Import the base class for creating Kivy applications
from kivy.uix.widget import Widget  # Import the base class for creating widgets
from kivy.core.window import Window  # Import the window class to handle window properties
from kivy.graphics import Color, Rectangle  # Import classes for drawing colors and rectangles
from kivy.clock import Clock  # Import Clock for scheduling updates
from random import randint  # Import randint to generate random integers

# Define the main class for the falling blocks game, inheriting from Widget
class FallingBlocks(Widget):
    # Initialize the widget
    def __init__(self, **kwargs):
        super().__init__(**kwargs)  # Call the parent class's constructor
        
        # Initialize the player block as a rectangle
        self.block = Rectangle(pos=(200, 400), size=(50, 50))  # Starting position and size of the player block
        
        # List to hold obstacles
        self.obstacles = []  # Initialize an empty list to store obstacles
        
        # Speed of obstacles
        self.speed = 5  # Set the speed at which obstacles will fall
        
        # Bind the widget size to the update size method
        self.bind(size=self._update_size)  # Update size when the window size changes

        # Schedule updates for game logic and obstacle generation
        Clock.schedule_interval(self.update, 1 / 60)  # Call update method 60 times per second
        Clock.schedule_interval(self.add_obstacle, 1)  # Call add_obstacle method every second

    # Handle key down events
    def on_key_down(self, window, key, scancode, codepoint, modifier):
        # Control the player block with left and right arrow keys
        if key == 276:  # If left arrow key is pressed
            self.block.pos = (self.block.pos[0] - 20, self.block.pos[1])  # Move left
        elif key == 275:  # If right arrow key is pressed
            self.block.pos = (self.block.pos[0] + 20, self.block.pos[1])  # Move right

    # Update game state
    def update(self, dt):
        # Move obstacles down
        for obs in self.obstacles:  # Iterate through each obstacle
            obs.pos = (obs.pos[0], obs.pos[1] - self.speed)  # Move the obstacle down by the speed amount
        
        # Check for collisions with the player block
        self.check_collision()  # Call method to check for collisions

        # Redraw the canvas to reflect changes
        self.on_draw()  # Call method to redraw the game elements

    # Add a new obstacle at a random position
    def add_obstacle(self, dt):
        # Add a new obstacle at a random x position at the top of the window
        x_pos = randint(0, self.width - 50)  # Generate a random x position within the window width
        obstacle = Rectangle(pos=(x_pos, self.height), size=(50, 50))  # Create a new rectangle for the obstacle
        self.obstacles.append(obstacle)  # Add the new obstacle to the list

    # Check for collisions between the player block and obstacles
    def check_collision(self):
        # Iterate through each obstacle
        for obs in self.obstacles:
            # Check if the player block overlaps with the obstacle
            if (self.block.pos[0] < obs.pos[0] + 50 and  # Left edge of player < Right edge of obstacle
                self.block.pos[0] + 50 > obs.pos[0] and  # Right edge of player > Left edge of obstacle
                self.block.pos[1] < obs.pos[1] + 50 and  # Top edge of player < Bottom edge of obstacle
                self.block.pos[1] + 50 > obs.pos[1]):  # Bottom edge of player > Top edge of obstacle
                print("Collision Detected!")  # Print collision message to console
                self.reset_game()  # Call method to reset the game

    # Reset the game state
    def reset_game(self):
        # Clear obstacles on collision
        self.obstacles.clear()  # Clear the list of obstacles when a collision occurs

    # Draw game elements on the canvas
    def on_draw(self):
        # Clear the canvas and draw all elements
        self.canvas.clear()  # Clear existing graphics from the canvas
        with self.canvas:
            Color(0, 0, 1, 1)  # Set color to blue for the player block
            Rectangle(pos=self.block.pos, size=(50, 50))  # Draw the player block
            Color(1, 0, 0, 1)  # Set color to red for obstacles
            for obs in self.obstacles:  # Iterate through each obstacle
                Rectangle(pos=obs.pos, size=(50, 50))  # Draw each obstacle

    def _update_size(self, *args):
        # This method is called to ensure the size is bound correctly
        pass  # Currently does nothing, but can be used for resizing logic

# Define the main application class
class FallingBlocksApp(App):
    def build(self):
        game = FallingBlocks()  # Create an instance of the FallingBlocks widget
        Window.bind(on_key_down=game.on_key_down)  # Bind the key event to the game instance
        return game  # Return the game widget to be displayed

# Run the application
if __name__ == '__main__':
    FallingBlocksApp().run()  # Start the Kivy application
