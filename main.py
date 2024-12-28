from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.graphics import Line, Ellipse, Color, Rectangle
from kivy.uix.label import Label
from kivy.clock import Clock
from random import randint  
from kivy.vector import Vector
#in the worm game, when the head moves, the one right behind it follows it so we need to edit it from the last piece not the head

class MyWidget(Widget): 
    def __init__(self, **kwargs):
        self.height = Window.height
        self.width = Window.width
        length_of_worm = 3
        self.worm_width = 50
        self.boost = False
        self.speed = self.worm_width #sets the speed of the worm to be equal to its width.
        self.boosted_speed = self.speed 
        self.direction = 1 # 1 will point to right, 2 will point to left, 3 will point to p and 4 points down 
        self.regular_speed = self.speed
        self.collision = False
        self.bad_food = False
        self.score = 0
        super().__init__(**kwargs)
        with self.canvas:
            self.keyboard = Window.request_keyboard(self.on_keyboard_closed, self) #from window request keyboard, set a method to say what will happen when its done 
            self.keyboard.bind(on_key_down = self.on_key_down) #binding this to a method called on key down 
            self.keyboard.bind(on_key_up = self.on_key_up)#when we lift our finger from the keyboard
            #need to make sure when we shut the keyboard it turns to null 
            Clock.schedule_interval(self.update, 1/20)
            Color(0.2, 0.3, 0.7, 0.5)
            Rectangle(pos = (0,0), size=(self.width, self.height)) #background 
            Color(0.4,0.8, 0.2, 1)
            self.elements = [] #array has to be an instance variable so you make it empty, create the worm 
            for i in range(length_of_worm):
                if i == 0:
                    self.source = "./images/head_right.png" #start from 0 and go to 2(lenght of worm) 
                else:
                    self.source = "./images/body.png"
                element = Ellipse(source=self.source, pos = (self.width/2 - i *self.worm_width, self.height/2), size =(self.worm_width, self.worm_width)) #give me the size based on the worm width now we used i *self.worm_width here so the circles wont print on top of each other but instead they keep pritning right next to each other 
                self.elements.append(element) #we 
            Color(0.5, 0, 0, 1)
            self.food = Ellipse(pos=(200,300), size = (50,50)) 
            self.label = Label(text = "Scores: " +str(self.score), pos = (100, self.height - 100), color = (1,0,0,1), font_size = 50) 
    def on_keyboard_closed(self): #its an instance method so it needs self as an argument
        self.keyboard.unbind(self.on_key_down, self)
        self.keyboard = None
        #what i want this keyboard to be associated with if its keydown do something 
    def on_key_down(self, keyboard, keycode, text, modifier): #self is the method, keyboard is an text gives , keycode gives you name of the key and its what we work with   
         for i in range(len(self.elements) -1,-1,-1): #Why backwards? In a snake game, each segment of the body moves to the position of the segment in front of it, so you need to update from the tail to the head.
              if i!=0: #For every segment that’s not the head (i != 0), move it to the position of the segment just in front of it (self.elements[i-1].pos). This makes the segments "follow" the head.
                self.elements[i].pos = self.elements[i-1].pos
            #Based on the arrow key pressed, the method updates the position of the ellipse (self.ellipse.pos). It moves the ellipse by 10 pixels in the corresponding direction:
              else:
                if keycode[1] == 'right':
                    self.direction = 1
                    self.boost = True
                    self.speed = self.boosted_speed
                    #self.elements[i].pos = (self.elements[i].pos[0] + self.worm_width, self.elements)
                elif keycode[1] == 'left':
                    self.direction = 2
                    self.boost = True
                    self.speed = self.boosted_speed
                    #self.elements[i].pos = (self.elements[i].pos[])
                elif keycode[1] == 'up':
                    self.direction = 3
                    self.boost = True
                    self.speed = self.boosted_speed
                elif keycode[1] == 'down':
                    self.direction = 4 #the direction changes once you click the key until you click another key 
                    self.boost = True
                    self.speed = self.boosted_speed
    def on_key_up(self, keyboard, keycode): #as long as the key is up then do sth 
        if keycode[1] == 'right' or keycode[1] == 'up' == keycode[1] == 'left' or keycode[1] == 'down':
          self.boost = False
          self.speed = self.regular_speed

          
    
            
    def update(self, dt):
            for i in range(len(self.elements)-1, -1, -1): #you want the index so it iwll separate the first one the head from the rest if the body
                #basically since it starts with 3, you minus 1 and keep minusing 1 
                #it will pick up the first value 3, but it wont start from one it will start from zero, so we do reverse order. len is the length of the elements and here its 3 but we should start from 2 thats why we minus 1 and end in -1 but exclusive because -1 is right after 0 
                #we arent hardcoding so it will be changeable 
             if i != 0: #you cant start from zero 
              if self.boost:
                if self.direction == 1:
                        self.elements[i].pos = (self.elements[i-1].pos[0] + (self.boosted_speed - self.regular_speed), self.elements[i-1].pos[1]) 
                     
                elif self.direction == 2:
                          self.elements[i].pos = (self.elements[i-1].pos[0] - (self.boosted_speed - self.regular_speed), self.elements[i-1].pos[1]) 
                     
                elif self.direction == 3:
                          self.elements[i].pos = (self.elements[i-1].pos[0], self.elements[i-1].pos[1] + (self.boosted_speed - self.regular_speed))
                elif self.direction == 4: 
                      self.elements[i].pos = (self.elements[i-1].pos[0], self.elements[i-1].pos[1] - (self.boosted_speed - self.regular_speed))
              else:                               
                 self.elements[i].pos = self.elements[i-1].pos
             else:
                 if self.direction == 1:
                    self.elements[0].source = "./images/head_right.png"
                    x = self.elements[i].pos[0] + self.speed
                    if x >= self.width:
                        x = 0
                    self.elements[i].pos = (x, self.elements[i].pos[1])
                    
                 elif self.direction == 2:
                    self.elements[0].source = "./images/head_left.png"
                    x = self.elements[i].pos[0] - self.speed
                    if x <= - self.worm_width:
                        x = self.width - self.worm_width
                    self.elements[i].pos = (x, self.elements[i].pos[1])
        
                 elif self.direction == 3:
                   self.elements[0].source = "./images/head_up.png"
                   y = self.elements[i].pos[1] + self.speed
                   if y >= self.height:
                       y = 0
                   self.elements[i].pos = (self.elements[i].pos[0], y)
                 elif self.direction == 4:
                  self.elements[0].source = "./images/head_down.png"
                  y = (self.elements[i].pos[1] - self.speed)
                  if y < 0:
                      y = self.height - self.worm_width 
                  self.elements[i].pos = (self.elements[i].pos[0], y)
                 self.check_collision(self.elements[i], self.food)

    def check_collision(self, r1,r2):
        x1, y1 = r1.pos #are the two objects (such as your worm and the food) whose collision you're checking.
        #Return the coordinates of the bottom-left corner of r1 and r2. These positions are in the format (x, y), where: x1, y1 = r1.pos assigns x1 and y1 to the x and y position of r1 and 
        # x2, y2 = r2.pos does the same for r2, assigning x2 and y2 to the x and y position of r2.
        #return the width and height of r1 and r2. These sizes are in the format (width, height), where: w1, h1 = r1.size assigns w1 and h1 to the width and height of r1.
        #w2, h2 = r2.size does the same for r2.
        #This is used for collision detection by checking if the bounding boxes of the two objects (r1 and r2) overlap. For example, x1 < x2 + w2 checks if the right side of r1 overlaps with the left side of r2, and similar checks are done for other sides to determine if the two objects collide.
        w1, h1 = r1.size
        x2, y2 = r2.pos
        w2, h2 = r2.size

        if x1 < x2+w2 and x1 + w1 > x2 and y1 < y2 + h2 and y1 + h1 > y2:
            if self.collision == True:
                self.score += 1
                self.label.text = 'Scores: '+str(self.score)
            #print("collision happened")
            with self.canvas:
                element = Ellipse(source = self.source, pos=(self.elements[-1].pos), size=(self.worm_width, self.worm_width)) #self.elements[-1].pos -1 is negative indexing so its the last 
                self.elements.append(element)
                self.food.pos = (randint(0, self.width - 50), randint(0, self.height - 50))

        else: 
            self.collision = False
            #print("collision didnt")
    def bad_food(self, food):
        if food: 
            Clock.schedule_interval(self.update, 1)
            with self.canvas:
                element = Ellipse(source = self.source, pos=(self.elements[-1].pos), size=(self.worm_width, self.worm_width)) #self.elements[-1].pos -1 is negative indexing so its the last 
                self.elements.remove(element)
        




# plus and minus is for right and left 

class MyApp(App): #
   def build(self): #
       return MyWidget() #
   
if __name__ == '__main__':
   myApp = MyApp()
   myApp.run() 