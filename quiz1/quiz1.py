from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Ellipse
from kivy.core.window import Window
from kivy.clock import Clock
from random import uniform

class MyWidget(Widget):
   def __init__(self, **kwargs):
       self.window_height = Window.height
       self.window_width = Window.width
       self.main_clock = Clock.schedule_interval(self.update, 1/30)
       self.direction = None # Starting standing still
       self.speed = 20 # Wagon speed
       self.wagon_width = 200
       self.wagon_height = 100
       self.points = 0 # To keep track when higher difficulty is supposed to start
       self.time_for_food = 2 # seconds between food
       self.food_size = 50
       self.difficulty_trigger = 20 # Points needed for the higher difficulty
       self.food_speed = 20
       self.difficult_speed = self.food_speed * 1.5
       self.foods =[]
       super().__init__(**kwargs)
       self.keyboard = Window.request_keyboard(self.on_keyboard_closed, self) # mandatory: callback function closes the keyboard input after we close the app
       self.keyboard.bind(on_key_down = self.on_key_down)
       self.food_timer = Clock.schedule_interval(self.drop_food, self.time_for_food)
       with self.canvas:
           self.wagon = Rectangle(source='worm/quiz1/wagon.png', pos =(0,0), size=(self.wagon_width,self.wagon_height))
           Rectangle(source='worm/quiz1/background.png', pos=(0,0), size=(self.window_width, self.window_height)) # Setting background
           self.foods.append(Ellipse(source='worm/quiz1/food.png', pos=( uniform(0,self.window_width-self.food_size),self.window_height), size=(self.food_size,self.food_size)))

   def on_keyboard_closed(self):
       self.keyboard.unbind(self.on_key_down)
       self.keyboard = None 

   def on_key_down(self, keyboard, keycode, text, modifier):
       # Get direction from keys
       if keycode[1] == 'right':
           self.direction = 1
       elif keycode[1] == 'left':
           self.direction = 2

   def update(self, dl):
       # Check direction
       if self.direction == 1:
           self.wagon.pos = (self.wagon.pos[0] + self.speed, self.wagon.pos[1])
       elif self.direction == 2:
           self.wagon.pos = (self.wagon.pos[0] - self.speed, self.wagon.pos[1])

       # Check if wagon is out of frame
       # I am calculating with halves of the wagon because the it is quite big so I think it looks better if it 'teleports' once half of it is out of frame
       if self.wagon.pos[0] > self.window_width - self.wagon.size[1]/2: 
           self.wagon.pos = (-self.wagon.size[1]/2, 0)
       elif self.wagon.pos[0] < -self.wagon.size[1]/2:
           self.wagon.pos = (self.window_width - self.wagon.size[0]/2, 0)

       
       for food in self.foods:
           food.pos = (food.pos[0], food.pos[1]-self.food_speed) # Move food downwards
           # Check for collisions
           if self.check_collision(self.wagon, food):
               self.canvas.remove(food) # Remove caught food from canvas
               self.foods.remove(food) 
               self.points += 1
       # Increase speed of food once the points are high enough
       if self.points >= self.difficulty_trigger:
           self.food_speed = self.difficult_speed

   def drop_food(self,dl):
       # Add a new food every time they drop, this way multiple foods can be on the screen at once
       with self.canvas:
           self.foods.append(Ellipse(source='worm/quiz1/food.png', pos=(uniform(0,self.window_width-self.food_size),self.window_height), size=(self.food_size,self.food_size)))

   def check_collision(self, item1, item2):
       item1_x, item1_y = item1.pos
       item1_width, item1_height = item1.size

       item2_x, item2_y = item2.pos
       item2_width, item2_height= item2.size

       if item1_x < item2_x + item2_width and item1_x + item1_width > item2_x and item1_y < item2_y + item2_height and item1_y + item1_height > item2_y:
           return True
       else: 
           return False


class MyApp(App):
   def build(self):
       return MyWidget()


if __name__ == '__main__':
   myApp = MyApp()
   myApp.run()
