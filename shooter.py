# Import necessary modules from the Kivy library
from kivy.app import App  # For creating the application
from kivy.uix.widget import Widget  # Base class for creating custom widgets
from kivy.core.window import Window  # To access window properties like size
from kivy.graphics import Rectangle, Ellipse, Color  # For drawing shapes and colors
from kivy.clock import Clock  # For scheduling periodic updates

class ShooterGame(Widget):  # Define the ShooterGame class, inheriting from Widget
    def __init__(self, **kwargs):  # Constructor method for initializing the game
        super().__init__(**kwargs)  # Call the parent constructor
        
        # Player setup
        self.player_pos = [Window.width // 2 - 25, 50]  # Set initial player position (centered at the bottom)
        self.player_size = (50, 50)  # Define the player's size (width, height)

        with self.canvas:  # Start drawing on the widget's canvas
            Color(0, 1, 0, 1)  # Set color to green (RGBA)
            self.player = Rectangle(pos=self.player_pos, size=self.player_size)  # Create a rectangle for the player
        
        # Bullets storage
        self.bullets = []  # List to store active bullets

        # Bind keyboard inputs to the game
        Window.bind(on_key_down=self.on_key_down)  # Listen for key press events
        Window.bind(on_key_up=self.on_key_up)  # Listen for key release events

        # Schedule updates to the game state
        Clock.schedule_interval(self.update, 1 / 60)  # Call update method 60 times per second
        
        # Initialize movement flags
        self.move_left = False
        self.move_right = False

    def on_key_down(self, window, key, *args):  # Method to handle key presses
        """Handle keyboard inputs."""
        if key in (276, 97):  # Left arrow or 'A' key
            self.move_left = True
        elif key in (275, 100):  # Right arrow or 'D' key
            self.move_right = True
        elif key == 32:  # Space bar
            self.shoot_bullet()  # Call the method to shoot a bullet

    def on_key_up(self, window, key, *args):  # Method to handle key releases
        """Handle key releases."""
        if key in (276, 97):  # Left arrow or 'A' key
            self.move_left = False
        elif key in (275, 100):  # Right arrow or 'D' key
            self.move_right = False

    def shoot_bullet(self):  # Method to create and add a bullet
        """Create and add a bullet to the canvas."""
        bullet_x = self.player.pos[0] + (self.player_size[0] / 2) - 5  # Center bullet horizontally
        bullet_y = self.player.pos[1] + self.player_size[1]  # Position bullet above the player

        bullet = Ellipse(pos=(bullet_x, bullet_y), size=(10, 10))  # Create a bullet as an ellipse
        self.bullets.append(bullet)  # Add bullet to the list of bullets
        
        # Add color context and bullet to the canvas
        with self.canvas:  # Start a new drawing context
            Color(1, 0, 0, 1)  # Set color to red (RGBA) for the bullet
            self.canvas.add(bullet)  # Add the bullet to the canvas

        print(f"Bullet created at position: {bullet.pos}")  # Debug statement to confirm bullet creation

    def update(self, dt):  # Method to update the game state
        """Update game state including player movement and bullet movement."""
        # Handle player movement
        if self.move_left:  # If moving left
            self.player.pos = (max(0, self.player.pos[0] - 10), self.player.pos[1])  # Move player left
        if self.move_right:  # If moving right
            self.player.pos = (min(Window.width - self.player_size[0], self.player.pos[0] + 10), self.player.pos[1])  # Move player right

        # Update bullets
        for bullet in self.bullets[:]:  # Iterate through a copy of the bullet list
            bullet.pos = (bullet.pos[0], bullet.pos[1] + 10)  # Move bullet upward

            # Check if bullet goes off-screen and remove it
            if bullet.pos[1] > Window.height:  # If the bullet's y position exceeds window height
                self.canvas.remove(bullet)  # Remove bullet from the canvas
                self.bullets.remove(bullet)  # Remove bullet from the list of bullets
                print("Bullet removed.")  # Debug statement to confirm bullet removal

class ShooterApp(App):  # Define the main application class
    def build(self):  # Method to build the app's interface
        return ShooterGame()  # Return an instance of the ShooterGame class

if __name__ == '__main__':  # Check if the script is being run directly
    ShooterApp().run()  # Create an instance of ShooterApp and run it
