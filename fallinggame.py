from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.core.window import Window

class Paddle(Widget):
    # Paddle properties
    width = NumericProperty(100)
    height = NumericProperty(20)

    def move(self, dx):
        # Move the paddle left or right
        self.x += dx
        # Keep the paddle within the window boundaries
        self.x = max(0, min(self.x, Window.width - self.width))

class FallingBall(Widget):
    # Ball properties
    x_velocity = NumericProperty(0)
    y_velocity = NumericProperty(-5)  # Initial downward velocity

    def update(self, paddle):
        # Update ball position
        self.pos = Vector(*self.pos) + Vector(self.x_velocity, self.y_velocity)

        # Check for collision with paddle
        if self.collide_widget(paddle):
            self.y_velocity *= -1  # Bounce off the paddle
            self.y += 10  # Move the ball slightly up to avoid getting stuck

        # Check for hitting the bottom of the window
        if self.y < 0:
            self.pos = (self.x, Window.height)  # Reset position to the top

class GameWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.paddle = Paddle(center_x=Window.width / 2, y=50, size=(100, 20))
        self.add_widget(self.paddle)

        self.ball = FallingBall(x=Window.width / 2, y=Window.height - 50, size=(30, 30))
        self.ball.x_velocity = 3  # Horizontal speed of the ball
        self.add_widget(self.ball)

        # Schedule the update function to run every 1/60th of a second
        Clock.schedule_interval(self.update, 1.0 / 60.0)

    def update(self, dt):
        # Update the ball's position, passing the paddle for collision detection
        self.ball.update(self.paddle)

    def on_touch_move(self, touch):
        # Move paddle based on touch position
        self.paddle.center_x = touch.x

class FallingGameApp(App):
    def build(self):
        return GameWidget()

if __name__ == '__main__':
    Window.size = (800, 600)  # Set the window size
    FallingGameApp().run()
