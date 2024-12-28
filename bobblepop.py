from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from random import randint

class ObstacleDodgingGame(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.width = Window.width
        self.height = Window.height
        self.player_width = 50
        self.player_height = 50
        self.player_pos = [self.width / 2 - self.player_width / 2, 50]
        self.obstacles = []
        self.game_over = False

        # Create player rectangle
        with self.canvas:
            Color(0, 0, 1, 1)  # Blue color for the player
            self.player = Rectangle(pos=self.player_pos, size=(self.player_width, self.player_height))

        # Create keyboard input
        self.keyboard = Window.request_keyboard(self.on_keyboard_closed, self)
        self.keyboard.bind(on_key_down=self.on_key_down)

        # Schedule game updates
        Clock.schedule_interval(self.update_obstacles, 1)
        Clock.schedule_interval(self.update, 1 / 60)

        # Label to show game over message
        self.game_over_label = Label(text='', font_size='30sp', pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.add_widget(self.game_over_label)

    def on_keyboard_closed(self):
        self.keyboard.unbind(on_key_down=self.on_keyboard_closed)
        self.keyboard = None

    def on_key_down(self, keyboard, keycode, text, modifier):
        if self.game_over:
            if keycode[1] == 'space':  # Press space to restart
                self.restart_game()
            return
            
        if keycode[1] == 'right':
            self.player_pos[0] += 10
        elif keycode[1] == 'left':
            self.player_pos[0] -= 10
            
        # Keep player within the screen bounds
        self.player_pos[0] = max(0, min(self.player_pos[0], self.width - self.player_width))
        self.player.pos = self.player_pos

    def update_obstacles(self, dt):
        if self.game_over:
            return
        
        obstacle_x = randint(0, self.width - 50)
        with self.canvas:
            Color(1, 0, 0, 1)  # Red color for obstacles
            obstacle = Rectangle(pos=(obstacle_x, self.height), size=(50, 50))
            self.obstacles.append(obstacle)

    def update(self, dt):
        if self.game_over:
            return
        
        for obstacle in self.obstacles:
            # Move obstacle down
            obstacle.pos = (obstacle.pos[0], obstacle.pos[1] - 5)

            # Check for collision
            if self.check_collision(self.player, obstacle):
                self.game_over = True
                self.on_game_over()  # Call the game over method
                return

        # Remove obstacles that go off screen
        self.obstacles = [obstacle for obstacle in self.obstacles if obstacle.pos[1] > 0]

    def check_collision(self, player, obstacle):
        player_x, player_y = player.pos
        obstacle_x, obstacle_y = obstacle.pos
        return (player_x < obstacle_x + 50 and player_x + self.player_width > obstacle_x and
                player_y < obstacle_y + 50 and player_y + self.player_height > obstacle_y)

    def on_game_over(self):
        # Display game over message
        self.game_over_label.text = "Game Over! Press Space to Restart"
        print("Game Over!")

    def restart_game(self):
        # Reset game state
        self.obstacles = []
        self.game_over = False
        self.game_over_label.text = ''
        self.player_pos = [self.width / 2 - self.player_width / 2, 50]
        self.player.pos = self.player_pos

class ObstacleDodgingApp(App):
    def build(self):
        return ObstacleDodgingGame()

if __name__ == '__main__':
    ObstacleDodgingApp().run()
