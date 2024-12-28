from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.vector import Vector
from random import randint
from kivy.graphics import Rectangle, Color

class CatchGame(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Basket setup
        self.basket = Widget(size=(100, 20))
        self.basket.pos = (Window.width / 2 - 50, 50)
        with self.basket.canvas:
            Color(0, 1, 0)  # Green color for the basket
            self.basket_rect = Rectangle(pos=self.basket.pos, size=self.basket.size)
        self.add_widget(self.basket)

        # Object list and score
        self.objects = []
        self.score = 0
        self.score_label = Label(text=f'Score: {self.score}', pos=(10, Window.height - 30))
        self.add_widget(self.score_label)

        # Schedule game updates and object spawning
        Clock.schedule_interval(self.update, 1 / 60)
        Clock.schedule_interval(self.spawn_object, 1)

        # Keyboard control setup
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'left':
            self.basket.x -= 20
        elif keycode[1] == 'right':
            self.basket.x += 20
        # Update basket position visually
        self.basket_rect.pos = self.basket.pos

    def spawn_object(self, dt):
        # Create a new falling object
        new_object = Widget(size=(30, 30))
        new_object.pos = (randint(0, Window.width - 30), Window.height)

        with new_object.canvas:
            Color(1, 0, 0)  # Red color for the falling object
            new_object.rect = Rectangle(pos=new_object.pos, size=new_object.size)

        self.add_widget(new_object)
        self.objects.append(new_object)

    def update(self, dt):
        for obj in self.objects[:]:  # Iterate over a copy of the list
            obj.y -= 5
            obj.rect.pos = obj.pos  # Update the object's rectangle position

            # Check for collision with the basket
            if obj.collide_widget(self.basket):
                self.score += 1
                self.score_label.text = f'Score: {self.score}'
                self.remove_widget(obj)
                self.objects.remove(obj)

            # Remove objects that fall off the screen
            elif obj.y < 0:
                self.remove_widget(obj)
                self.objects.remove(obj)

class CatchApp(App):
    def build(self):
        return CatchGame()

if __name__ == '__main__':
    CatchApp().run()

"""
self.basket = Widget(size=(100, 20)): Creates a Widget for the basket with a size of 100x20 pixels.
self.basket.pos = (Window.width / 2 - 50, 50): Positions the basket at the bottom center of the screen.
with self.basket.canvas: Adds custom drawings (like shapes or colors) to the basket's canvas.
Color(0, 1, 0): Sets the color to green for the basket.
self.basket_rect = Rectangle(...): Draws a rectangle using the basket's position and size.
self.add_widget(self.basket): Adds the basket to the game screen.
Score and Objects List Setup:
python
Copy code
        self.objects = []
        self.score = 0
        self.score_label = Label(text=f'Score: {self.score}', pos=(10, Window.height - 30))
        self.add_widget(self.score_label)
self.objects = []: Initializes an empty list to store the falling objects.
self.score = 0: Initializes the player's score to zero.
self.score_label = Label(...): Creates a label to display the score, positioned at the top left of the screen.
self.add_widget(self.score_label): Adds the score label to the game.
Scheduling Game Updates:
python
Copy code
        Clock.schedule_interval(self.update, 1 / 60)
        Clock.schedule_interval(self.spawn_object, 1)
Clock.schedule_interval(self.update, 1 / 60): Calls the update method 60 times per second (1/60 seconds per frame).
Clock.schedule_interval(self.spawn_object, 1): Calls spawn_object every 1 second to create a new falling object.
Keyboard Handling:
python
Copy code
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
self._keyboard = Window.request_keyboard(...): Requests access to keyboard input.
self._keyboard.bind(on_key_down=self._on_keyboard_down): Binds a key press event to the _on_keyboard_down method, allowing the player to move the basket.
Keyboard Close and Key Press Handling:
python
Copy code
    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'left':
            self.basket.x -= 20
        elif keycode[1] == 'right':
            self.basket.x += 20
        self.basket_rect.pos = self.basket.pos
_keyboard_closed: Unbinds the keyboard when it is no longer needed.
_on_keyboard_down: Handles key presses:
If the left arrow is pressed, the basket moves left by 20 pixels.
If the right arrow is pressed, the basket moves right by 20 pixels.
self.basket_rect.pos = self.basket.pos: Updates the basket's rectangle to match the basket's new position after a movement.
Spawning Falling Objects:
python
Copy code
    def spawn_object(self, dt):
        new_object = Widget(size=(30, 30))
        new_object.pos = (randint(0, Window.width - 30), Window.height)

        with new_object.canvas:
            Color(1, 0, 0)  # Red color for the falling object
            new_object.rect = Rectangle(pos=new_object.pos, size=new_object.size)

        self.add_widget(new_object)
        self.objects.append(new_object)
new_object = Widget(size=(30, 30)): Creates a new Widget for a falling object with a size of 30x30 pixels.
new_object.pos = (randint(0, Window.width - 30), Window.height): Sets the object's starting position at a random horizontal location at the top of the screen.
with new_object.canvas: Adds a red rectangle to represent the falling object.
self.add_widget(new_object): Adds the falling object to the game screen.
self.objects.append(new_object): Adds the new object to the list of objects to track.
Updating Objects and Checking Collisions:
python
Copy code
    def update(self, dt):
        for obj in self.objects[:]:  # Iterate over a copy of the list
            obj.y -= 5
            obj.rect.pos = obj.pos

            if obj.collide_widget(self.basket):
                self.score += 1
                self.score_label.text = f'Score: {self.score}'
                self.remove_widget(obj)
                self.objects.remove(obj)

            elif obj.y < 0:
                self.remove_widget(obj)
                self.objects.remove(obj)
for obj in self.objects[:]: Loops over all falling objects in the game (using a copy to avoid modifying the list while iterating).
obj.y -= 5: Moves the object 5 pixels downward each frame.
obj.rect.pos = obj.pos: Updates the object's rectangle position to match the widget's position.
if obj.collide_widget(self.basket): Checks if the object has collided with the basket:
If there is a collision, the score is incremented, the object is removed from the game screen, and it is removed from the list of objects.
elif obj.y < 0: If the object falls off the screen, it is removed from the game.
Running the Application:
python
Copy code
class CatchApp(App):
    def build(self):
        return CatchGame()

if __name__ == '__main__':
    CatchApp().run()
class CatchApp(App): Defines the application class that inherits from App.
def build(self): Returns the root widget (CatchGame) to be displayed in the application window.
if __name__ == '__main__':: Runs the app only if the script is executed directly (not imported).
CatchApp().run(): Starts the Kivy application.

"""
