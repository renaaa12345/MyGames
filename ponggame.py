# Import necessary modules from Kivy
from kivy.app import App  # Import the base class for creating Kivy applications
from kivy.clock import Clock  # Import Clock for scheduling updates
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty  # Import property classes for managing attributes
from kivy.uix.widget import Widget  # Import the base class for creating widgets
from kivy.vector import Vector  # Import Vector for handling 2D vector operations
from kivy.graphics import Ellipse, Rectangle  # Import classes for drawing shapes
from random import randint  # Import randint to generate random integers

# Define the paddle class for the Pong game
class PongPaddle(Widget):
    score = NumericProperty(0)  # Define a score property for the paddle

    def __init__(self, **kwargs):
        super().__init__(**kwargs)  # Call the parent class's constructor
        # Draw the paddle as a rectangle on the canvas
        with self.canvas:
            self.rect = Rectangle(pos=self.pos, size=(25, 150))  # Paddle dimensions
        self.bind(pos=self.update_graphics_pos)  # Bind position change to update graphics

    def update_graphics_pos(self, *args):
        # Update the rectangle's position when the paddle's position changes
        self.rect.pos = self.pos

    def bounce_ball(self, ball):
        # Reverse ball's direction and increase its speed when colliding with the paddle
        if self.collide_widget(ball):  # Check for collision with the ball
            ball.velocity_x *= -1.1  # Reverse direction and increase speed


# Define the ball class for the Pong game
class PongBall(Widget):
    velocity_x = NumericProperty(0)  # Define horizontal velocity property
    velocity_y = NumericProperty(0)  # Define vertical velocity property
    velocity = ReferenceListProperty(velocity_x, velocity_y)  # Combine x and y velocities into a single property

    def __init__(self, **kwargs):
        super().__init__(**kwargs)  # Call the parent class's constructor
        # Draw the ball as an ellipse on the canvas
        with self.canvas:
            self.ellipse = Ellipse(pos=self.pos, size=(50, 50))  # Ball dimensions
        self.bind(pos=self.update_graphics_pos)  # Bind position change to update graphics

    def update_graphics_pos(self, *args):
        # Update the ellipse's position when the ball's position changes
        self.ellipse.pos = self.pos

    def move(self):
        # Update the ball's position based on its velocity
        self.pos = Vector(*self.velocity) + self.pos  # Add velocity vector to current position


# Define the main game class for the Pong game
class PongGame(Widget):
    ball = ObjectProperty(None)  # Object property for the ball
    player1 = ObjectProperty(None)  # Object property for player 1's paddle
    player2 = ObjectProperty(None)  # Object property for player 2's paddle

    def __init__(self, **kwargs):
        super().__init__(**kwargs)  # Call the parent class's constructor
        self.ball = PongBall()  # Create a new ball instance
        self.player1 = PongPaddle()  # Create a new paddle for player 1
        self.player2 = PongPaddle()  # Create a new paddle for player 2

        # Add the ball and paddles to the game widget
        self.add_widget(self.ball)
        self.add_widget(self.player1)
        self.add_widget(self.player2)

        # Set initial positions for paddles
        self.player1.pos = (50, self.center_y - 75)  # Center player 1 vertically
        self.player2.pos = (self.width - 75, self.center_y - 75)  # Center player 2 vertically
        self.serve_ball()  # Serve the ball at the start of the game

    def on_size(self, *args):
        """Update the position of player2 when the window size changes."""
        self.player2.pos = (self.width - 50, self.center_y - 75)  # Update player2's position based on new width

    def serve_ball(self):
        # Center the ball on the screen and give it a random direction
        self.ball.center = self.center  # Center the ball on the widget
        self.ball.velocity = Vector(4, 0).rotate(randint(0, 360))  # Set initial random direction for the ball

    def update(self, dt):
        # Update game state
        self.ball.move()  # Move the ball based on its velocity

        # Bounce off top and bottom edges of the window
        if (self.ball.y < 0) or (self.ball.top > self.height):  # If the ball hits top or bottom
            self.ball.velocity_y *= -1  # Reverse vertical direction

        # Bounce off paddles
        if self.ball.x < self.player1.right and self.player1.collide_widget(self.ball):  # If ball hits player 1's paddle
            self.ball.velocity_x *= -1.1  # Reverse direction and increase speed
        if self.ball.right > self.player2.x and self.player2.collide_widget(self.ball):  # If ball hits player 2's paddle
            self.ball.velocity_x *= -1.1  # Reverse direction and increase speed

        # Check for scoring conditions
        if self.ball.x < 0:  # If the ball goes out of bounds on the left
            self.player2.score += 1  # Increment player 2's score
            self.serve_ball()  # Reset the ball for the next round
        if self.ball.right > self.width:  # If the ball goes out of bounds on the right
            self.player1.score += 1  # Increment player 1's score
            self.serve_ball()  # Reset the ball for the next round

    def on_touch_move(self, touch):
        # Move the paddles based on touch input
        if touch.x < self.width / 3:  # If touch is on the left side
            self.player1.center_y = touch.y  # Move player 1's paddle to follow touch
        if touch.x > self.width * 2 / 3:  # If touch is on the right side
            self.player2.center_y = touch.y  # Move player 2's paddle to follow touch


# Define the main application class
class PongApp(App):
    def build(self):
        game = PongGame()  # Create an instance of the PongGame
        game.bind(size=game.on_size)  # Bind the game size to update player2's position
        Clock.schedule_interval(game.update, 1.0 / 60.0)  # Schedule the update method to run 60 times per second
        return game  # Return the game widget to be displayed

# Run the application
if __name__ == '__main__':
    PongApp().run()  # Start the Kivy application
