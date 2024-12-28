from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from random import choice
from kivy.core.window import Window

class MemoryGame(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sequence = []
        self.user_input = []
        self.colors = [(1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 0)]
        self.step = 0
        
        # Bind to the size of the window correctly
        self.bind(size=self._update_size)
        
        # Start the game with an initial color
        self.add_to_sequence()

    def _update_size(self, *args):
        # This method is called to ensure the size is bound correctly
        pass

    def add_to_sequence(self):
        new_color = choice(self.colors)
        self.sequence.append(new_color)
        self.step = 0
        self.show_sequence()

    def show_sequence(self):
        for i, color in enumerate(self.sequence):
            # Schedule to flash each color in the sequence
            Clock.schedule_once(lambda dt, c=color: self.flash_color(c), 1 * (i + 1))
        
        # Reset the user input after showing the sequence
        Clock.schedule_once(self.reset_user_input, len(self.sequence) + 1)

    def flash_color(self, color):
        with self.canvas:
            Color(color[0], color[1], color[2])
            Rectangle(pos=(0, 0), size=(self.width, self.height))

    def reset_canvas(self):
        self.canvas.clear()

    def reset_user_input(self, dt):
        self.user_input = []

    def on_key_down(self, window, keycode, text, modifiers):
        if keycode[1] == '1':
            self.user_input.append(self.colors[0])
        elif keycode[1] == '2':
            self.user_input.append(self.colors[1])
        elif keycode[1] == '3':
            self.user_input.append(self.colors[2])
        elif keycode[1] == '4':
            self.user_input.append(self.colors[3])
        
        # Check user input against the sequence
        if self.user_input == self.sequence:
            self.add_to_sequence()
        elif len(self.user_input) == len(self.sequence):
            self.reset_game()

    def reset_game(self):
        self.sequence = []
        self.user_input = []
        self.add_to_sequence()

class MemoryGameApp(App):
    def build(self):
        game = MemoryGame()
        Window.bind(on_key_down=game.on_key_down)  # Bind key down events to the game
        return game

if __name__ == '__main__':
    MemoryGameApp().run()
