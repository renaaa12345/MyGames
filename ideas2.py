"""
Falling Blocks Game
Create a simple game where random blocks fall from the top of the screen, and the player controls a paddle at the bottom to catch them. The player scores points by catching the blocks, and the speed of falling blocks increases over time.

python
Copy code
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.graphics import Rectangle
from kivy.clock import Clock
from random import randint

class BlockCatcher(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.paddle_width = 100
        self.paddle_height = 20
        self.block_size = 50
        self.speed = 5
        self.blocks = []
        self.score = 0
        Window.size = (400, 600)

        with self.canvas:
            self.paddle = Rectangle(pos=(Window.width/2 - self.paddle_width/2, 10), size=(self.paddle_width, self.paddle_height))

        self.bind(on_touch_move=self.on_touch_move)
        Clock.schedule_interval(self.update, 1/60)
        Clock.schedule_interval(self.spawn_block, 1)

    def on_touch_move(self, touch):
        # Move paddle based on touch position
        if 0 <= touch.x <= Window.width - self.paddle_width:
            self.paddle.pos = (touch.x, 10)

    def update(self, dt):
        # Update blocks and check for collision with paddle
        for block in self.blocks:
            block.pos = (block.pos[0], block.pos[1] - self.speed)
            if block.pos[1] < 0:
                self.canvas.remove(block)
                self.blocks.remove(block)
            elif self.check_collision(self.paddle, block):
                self.canvas.remove(block)
                self.blocks.remove(block)
                self.score += 1
                print(f"Score: {self.score}")

    def spawn_block(self, dt):
        # Create a new falling block at a random x position
        with self.canvas:
            block = Rectangle(pos=(randint(0, Window.width - self.block_size), Window.height),
                              size=(self.block_size, self.block_size))
            self.blocks.append(block)

    def check_collision(self, r1, r2):
        # Check for collision between paddle and block
        if r1.pos[0] < r2.pos[0] + r2.size[0] and r1.pos[0] + r1.size[0] > r2.pos[0] and \
           r1.pos[1] < r2.pos[1] + r2.size[1] and r1.pos[1] + r1.size[1] > r2.pos[1]:
            return True
        return False

class BlockCatcherApp(App):
    def build(self):
        return BlockCatcher()

if __name__ == '__main__':
    BlockCatcherApp().run()
2. Breakout Game
A simplified version of the classic Breakout game where the player controls a paddle and destroys bricks by bouncing a ball.

python
Copy code
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.graphics import Rectangle, Ellipse, Line
from kivy.clock import Clock
from random import randint

class Breakout(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.paddle_width = 100
        self.paddle_height = 20
        self.ball_size = 20
        self.ball_speed_x = 3
        self.ball_speed_y = 3
        self.bricks = []
        self.score = 0
        Window.size = (400, 600)

        with self.canvas:
            self.paddle = Rectangle(pos=(Window.width/2 - self.paddle_width/2, 10), size=(self.paddle_width, self.paddle_height))
            self.ball = Ellipse(pos=(Window.width/2 - self.ball_size/2, Window.height/2), size=(self.ball_size, self.ball_size))

        self.create_bricks()
        self.bind(on_touch_move=self.on_touch_move)
        Clock.schedule_interval(self.update, 1/60)

    def create_bricks(self):
        # Create rows of bricks
        brick_width = 50
        brick_height = 20
        for y in range(5):
            for x in range(7):
                with self.canvas:
                    brick = Rectangle(pos=(x * (brick_width + 10), Window.height - (y + 1) * (brick_height + 10)),
                                      size=(brick_width, brick_height))
                    self.bricks.append(brick)

    def on_touch_move(self, touch):
        # Move paddle based on touch position
        if 0 <= touch.x <= Window.width - self.paddle_width:
            self.paddle.pos = (touch.x, 10)

    def update(self, dt):
        # Update ball position
        self.ball.pos = (self.ball.pos[0] + self.ball_speed_x, self.ball.pos[1] + self.ball_speed_y)

        # Bounce ball off walls
        if self.ball.pos[0] <= 0 or self.ball.pos[0] + self.ball_size >= Window.width:
            self.ball_speed_x *= -1
        if self.ball.pos[1] >= Window.height:
            self.ball_speed_y *= -1

        # Check for collision with paddle
        if self.check_collision(self.paddle, self.ball):
            self.ball_speed_y *= -1

        # Check for collision with bricks
        for brick in self.bricks:
            if self.check_collision(brick, self.ball):
                self.bricks.remove(brick)
                self.canvas.remove(brick)
                self.ball_speed_y *= -1
                self.score += 1
                print(f"Score: {self.score}")
                break

        # Game over if ball goes below paddle
        if self.ball.pos[1] <= 0:
            Clock.unschedule(self.update)
            print("Game Over!")

    def check_collision(self, r1, r2):
        # Check for collision between two rectangles
        if r1.pos[0] < r2.pos[0] + r2.size[0] and r1.pos[0] + r1.size[0] > r2.pos[0] and \
           r1.pos[1] < r2.pos[1] + r2.size[1] and r1.pos[1] + r1.size[1] > r2.pos[1]:
            return True
        return False

class BreakoutApp(App):
    def build(self):
        return Breakout()

if __name__ == '__main__':
    BreakoutApp().run()
3. Dodge the Obstacles
A simple game where the player controls a character to avoid falling obstacles. The longer the player survives, the higher their score.

python
Copy code
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.graphics import Rectangle
from kivy.clock import Clock
from random import randint

class DodgeGame(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.player_size = 50
        self.obstacle_size = 50
        self.speed = 5
        self.obstacles = []
        self.score = 0
        Window.size = (400, 600)

        with self.canvas:
            self.player = Rectangle(pos=(Window.width/2 - self.player_size/2, 50), size=(self.player_size, self.player_size))

        self.bind(on_touch_move=self.on_touch_move)
        Clock.schedule_interval(self.update, 1/60)
        Clock.schedule_interval(self.spawn_obstacle, 1)

    def on_touch_move(self, touch):
        # Move player based on touch position
        if 0 <= touch.x <= Window.width - self.player_size:
            self.player.pos = (touch.x, 50)

    def update(self, dt):
        # Update obstacles and check for collision with player
        for obstacle in self.obstacles:
            obstacle.pos = (obstacle.pos[0], obstacle.pos[1] - self.speed)
            if obstacle.pos[1] < 0:
                self.canvas.remove(obstacle)
                self.obstacles.remove(obstacle)
            elif self.check_collision(self.player, obstacle):
                print(f"Game Over! Score: {self.score}")
                Clock.unschedule(self.update)
                Clock.unschedule(self.spawn_obstacle)

    def spawn_obstacle(self, dt):
        # Create a new obstacle at a random x position
        with self.canvas:
            obstacle = Rectangle(pos=(randint(0, Window.width - self.obstacle_size), Window.height),
                                 size=(self.obstacle_size, self.obstacle_size))
            self.obstacles.append(obstacle)

    def check_collision(self, r1, r2):
        # Check for collision between player and obstacle
        if r1.pos[0] < r2.pos[0] + r2.size[0] and r1.pos[0] + r1.size[0] > r2.pos[0] and \
           r1.pos[1] < r2.pos[1] + r2.size[1] and r1.pos[1] + r1.size[1] > r2.pos[1]:
            return True
        return False

class DodgeGameApp(App):
    def build(self):
        return DodgeGame()

if __name__ == '__main__':



"""