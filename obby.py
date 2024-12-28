from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Ellipse, Rectangle
from kivy.core.window import Window
from kivy.clock import Clock
from random import randint
#This code adds collectible objects that randomly appear on the screen. The player moves around to collect them.

class CollectGame(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.player = Widget(size=(50, 50), pos=(Window.width / 2, Window.height / 2))
        self.add_widget(self.player)

        with self.player.canvas:
            self.rect = Rectangle(pos=self.player.pos, size=self.player.size)

        self.collectible = Widget(size=(30, 30))
        self.add_widget(self.collectible)
        with self.collectible.canvas:
            self.collectible_shape = Ellipse(pos=self.collectible.pos, size=self.collectible.size)
        
        self.score = 0
        self.spawn_collectible()
        Clock.schedule_interval(self.update, 1 / 60)

        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

        self.dx = 0
        self.dy = 0

    def spawn_collectible(self):
        self.collectible.pos = (randint(0, Window.width - self.collectible.width),
                                randint(0, Window.height - self.collectible.height))
        self.collectible_shape.pos = self.collectible.pos

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'up':
            self.dy = 5
        elif keycode[1] == 'down':
            self.dy = -5
        elif keycode[1] == 'left':
            self.dx = -5
        elif keycode[1] == 'right':
            self.dx = 5

    def update(self, dt):
        self.player.x += self.dx
        self.player.y += self.dy
        self.rect.pos = self.player.pos

        # Check collision with collectible
        if self.player.collide_widget(self.collectible):
            self.score += 1
            print(f'Score: {self.score}')
            self.spawn_collectible()

class CollectApp(App):
    def build(self):
        return CollectGame()

if __name__ == '__main__':
    CollectApp().run()
