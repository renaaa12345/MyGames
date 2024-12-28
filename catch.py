from kivy.app import App  # Import the App class from Kivy to create the application
from kivy.uix.widget import Widget  # Import Widget to create UI elements
from kivy.graphics import Rectangle, Color  # Import Rectangle and Color for drawing shapes
from kivy.core.window import Window  # Import Window to access the window size and control the UI
from kivy.clock import Clock  # Import Clock to schedule regular updates

class AvoidGame(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)  # Call the parent class constructor

        # Player setup
        self.player = Widget(size=(50, 50), pos=(Window.width / 2, Window.height / 2))  # Create player widget
        with self.player.canvas:
            Color(0, 1, 0)  # Set the player color to green
            self.rect = Rectangle(pos=self.player.pos, size=self.player.size)  # Draw player rectangle
        self.add_widget(self.player)  # Add player widget to the game

        # Obstacles setup (3 obstacles)
        self.obstacles = []  # List to store obstacles
        for _ in range(3):
            obstacle = Widget(size=(100, 100), pos=(100 + 200 * _, 100))  # Create and position each obstacle
            with obstacle.canvas:
                Color(1, 0, 0)  # Set obstacle color to red
                obs_rect = Rectangle(pos=obstacle.pos, size=obstacle.size)  # Draw the obstacle rectangle
            obstacle.rect = obs_rect  # Store the rectangle for position updates
            self.obstacles.append(obstacle)  # Add obstacle to the list
            self.add_widget(obstacle)  # Add obstacle to the game screen

        # Add vertical movement directions for obstacles
        self.obstacle_velocities = [3, -2, 4]  # Movement speed for each obstacle (can be positive or negative)

        # Schedule regular game updates
        Clock.schedule_interval(self.update, 1 / 60)  # Update the game 60 times per second (60 FPS)

        # Setup keyboard controls
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)  # Request access to the keyboard
        self._keyboard.bind(on_key_down=self._on_keyboard_down)  # Bind key press events to control the player

    def _keyboard_closed(self):
        # Unbind the keyboard when closed
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None  # Set the keyboard variable to None when closed

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        # Handle key press events to move the player
        if keycode[1] == 'up':
            self.player.y += 10  # Move the player up
        elif keycode[1] == 'down':
            self.player.y -= 10  # Move the player down
        elif keycode[1] == 'left':
            self.player.x -= 10  # Move the player left
        elif keycode[1] == 'right':
            self.player.x += 10  # Move the player right

    def update(self, dt):
        # Update player position visually
        self.rect.pos = self.player.pos  # Update the rectangle to match the player's new position

        # Move obstacles and check for collisions
        for i, obs in enumerate(self.obstacles):
            # Move the obstacle up or down based on its velocity
            obs.y += self.obstacle_velocities[i]

            # Bounce the obstacle back if it hits the window's top or bottom edge
            if obs.y <= 0 or obs.y + obs.height >= Window.height:
                self.obstacle_velocities[i] *= -1  # Reverse the direction of movement

            # Update the obstacle's rectangle position
            obs.rect.pos = obs.pos

            # Check for collision between the player and the obstacle
            if self.player.collide_widget(obs):
                print("Game Over!")  # Print a message if the player collides with an obstacle
                self.player.pos = (Window.width / 2, Window.height / 2)  # Reset player position
                self.rect.pos = self.player.pos  # Update the player rectangle position

class AvoidApp(App):
    def build(self):
        # Build the app and return the game widget
        return AvoidGame()

if __name__ == '__main__':
    # Start the application
    AvoidApp().run()

"""
self.player = Widget(size=(50, 50), pos=(Window.width / 2, Window.height / 2)): Creates a player widget at the center of the screen with a size of 50x50 pixels.
with self.player.canvas: Color(0, 1, 0): Adds a green-colored rectangle to represent the player visually.
self.add_widget(self.player): Adds the player widget to the game.
Obstacles Setup:
self.obstacles = []: Initializes an empty list to hold the obstacles.
for _ in range(3): ...: Loops 3 times to create 3 obstacles, each with a size of 100x100 pixels, spaced apart.
with obstacle.canvas: Color(1, 0, 0): Adds a red-colored rectangle for each obstacle.
self.obstacles.append(obstacle): Appends each obstacle to the obstacles list.
self.add_widget(obstacle): Adds each obstacle to the game screen.
Movement Velocities:
self.obstacle_velocities = [3, -2, 4]: Defines the vertical movement speed for each obstacle (positive for downward movement, negative for upward).
Game Update:
Clock.schedule_interval(self.update, 1 / 60): Schedules the update function to be called 60 times per second to update the game.
Keyboard Input Handling:
self._keyboard = Window.request_keyboard(...): Requests the system keyboard to control the player.
self._keyboard.bind(on_key_down=self._on_keyboard_down): Binds the key press events to a function that moves the player.
update Method:
self.rect.pos = self.player.pos: Updates the player's rectangle position to match the widget's position.
for i, obs in enumerate(self.obstacles):: Loops over all obstacles, indexed by i.
obs.y += self.obstacle_velocities[i]: Moves each obstacle vertically by its defined velocity.
if obs.y <= 0 or obs.y + obs.height >= Window.height:: Reverses the obstacle's direction if it hits the screen's top or bottom edge.
if self.player.collide_widget(obs):: Checks for a collision between the player and any obstacle. If they collide, it prints "Game Over!" and resets the player's position.
AvoidApp Class:
class AvoidApp(App): The main application class that builds and runs the game.
def build(self): Defines the main function that returns the game widget.
Running the App:
if __name__ == '__main__': AvoidApp().run(): Starts the game when the script is executed directly.

"""