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

        self.basket = Widget(size=(100, 20))
        self.basket.pos = (Window.width / 2 - 50, 50)
        with self.basket.canvas:
            self.source = "./Images/wagonpng.png"  # Updated image name
            Color(0, 1, 0)  
            self.basket_rect = Rectangle(source=self.source, pos=self.basket.pos, size=self.basket.size)
        self.add_widget(self.basket)

        self.objects = []
        self.score = 0
        self.score_label = Label(text=f'Score: {self.score}', pos=(10, Window.height - 30))
        self.add_widget(self.score_label)

        self.speed = 5
        self.catch_threshold = 20

        # Schedule game updates and object spawning
        Clock.schedule_interval(self.update, 1 / 60)
        Clock.schedule_interval(self.spawn_object, 1)
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
       
        self.basket_rect.pos = self.basket.pos

    def spawn_object(self, dt):
        new_object = Widget(size=(30, 30))
        new_object.pos = (randint(0, Window.width - 30), Window.height)

        with new_object.canvas:
            self.source = "./Images/foodpng.png"  # Updated image name
            Color(1, 0, 0)  
            new_object.rect = Rectangle(source=self.source, pos=new_object.pos, size=new_object.size)  # Ensure to set the source for the rectangle

        self.add_widget(new_object)
        self.objects.append(new_object)

    def update(self, dt):
        for obj in self.objects[:]:  
            obj.y -= self.speed  # Use the speed 
            obj.rect.pos = obj.pos  # Update the object's rectangle position

            # Check for collision with the basket
            if obj.collide_widget(self.basket):
                self.score += 1
                self.score_label.text = f'Score: {self.score}'
                self.remove_widget(obj)
                self.objects.remove(obj)

                # Increase speed after reaching the catch 
                if self.score == self.catch_threshold:
                    self.speed *= 1.5  # Increase speed by 50%
                    print(f'Speed increased to: {self.speed}')  # Optional: for debugging

            # Remove objects that fall off the screen
            elif obj.y < 0:
                self.remove_widget(obj)
                self.objects.remove(obj)

class CatchApp(App):
    def build(self):
        return CatchGame()

if __name__ == '__main__':
    CatchApp().run()

