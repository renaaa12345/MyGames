from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.graphics import Ellipse, Color
from kivy.clock import Clock
from random import randint

class MyWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.width = Window.width
        self.height = Window.height
        self.ellipse_width = 30
        self.speed = self.ellipse_width
        self.direction = None  # To store the direction of movement (None initially)

        # Create the keyboard controls
        self.keyboard = Window.request_keyboard(self.on_keyboard_closed, self)
        self.keyboard.bind(on_key_down=self.on_key_down)
        self.keyboard.bind(on_key_up=self.on_key_up)

        # Create the ellipse at a random position
        with self.canvas:
            Color(1, 0, 0, 0.9)
            self.ellipse = Ellipse(pos=(randint(0, self.width - 30), randint(0, self.height - 30)))
        
        # Create a label to display the ellipse's position
        self.label = Label(text=f"Position: {self.ellipse.pos}", pos=(100, 50))
        self.add_widget(self.label)

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
                    x = self.width - self.ellipse.size[0]
            elif self.direction == 'left':
                #If true, it decreases the x-coordinate (x -= self.speed), moving the ellipse to the left by self.speed units.
                #It then ensures that the ellipse doesn’t go off the left side of the screen by checking if x < 0. If it is less than 0, it resets the position to x = 0, keeping the ellipse within bounds.
                x -= self.speed
                if x < 0:
                    x = 0
            elif self.direction == 'up':
                y += self.speed
                if y > self.height - self.ellipse.size[1]:
                    y = self.height - self.ellipse.size[1]
            elif self.direction == 'down':
                y -= self.speed
                if y < 0:
                    y = 0

            self.ellipse.pos = (x, y)

            # Update the label with the new position of the ellipse
            self.label.text = f"Position: {self.ellipse.pos}"

class MyApp(App):
    def build(self):
        return MyWidget()

if __name__ == '__main__':
    MyApp().run()
