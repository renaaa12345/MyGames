from kivy.app import App  # Importing the App class to create the main application.
from kivy.uix.widget import Widget  # Importing the Widget class to create a custom widget.
from kivy.core.window import Window  # Importing Window to access window properties.
from kivy.graphics import Ellipse, Color, Rectangle  # Importing graphics classes for drawing shapes.
from kivy.clock import Clock  # Importing Clock to manage the timing of updates.
from random import randint, uniform  # Importing random functions to generate random numbers.

class MyWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)  # Initializing the parent Widget class.
        self.window_height = Window.height  # Getting the height of the window.
        self.window_width = Window.width  # Getting the width of the window.
        self.bullets = []  # List to store bullet objects.
        self.obstacles = []  # List to store obstacle objects.
        self.speed = 5  # Speed of the player movement.
        self.obstacle_speed = 2  # Speed of the obstacles movement.
        self.init_player()  # Initialize the player.
        self.init_obstacles()  # Initialize the obstacles.
        self.keyboard = Window.request_keyboard(self.on_keyboard_closed, self)  # Requesting keyboard input.
        self.keyboard.bind(on_key_down=self.on_key_down)  # Binding key press event.
        Clock.schedule_interval(self.update, 1/60)  # Schedule the update method to run 60 times per second.

    def init_player(self):
        # Initialize the player's position at the center of the window.
        self.player_pos = (self.window_width / 2, self.window_height / 2)
        with self.canvas:
            Color(0, 0, 1, 1)  # Set color to blue for the player.
            self.player = Rectangle(pos=self.player_pos, size=(50, 50))  # Create a blue rectangle for the player.

    def init_obstacles(self):
        # Create 5 random obstacles on the screen.
        for _ in range(5):
            x = uniform(0, self.window_width - 30)  # Random x position for the obstacle.
            y = uniform(0, self.window_height - 30)  # Random y position for the obstacle.
            with self.canvas:
                Color(1, 0, 0, 1)  # Set color to red for obstacles.
                obstacle = Rectangle(pos=(x, y), size=(30, 30))  # Create a red rectangle for the obstacle.
                self.obstacles.append(obstacle)  # Add the obstacle to the list.

    def on_keyboard_closed(self):
        # Unbind keyboard when closed.
        self.keyboard.unbind(on_key_down=self.on_key_down)
        self.keyboard = None

    def on_key_down(self, keyboard, keycode, text, modifier):
        moved = False  # Flag to check if the player moved.

        # Update player's position based on key presses.
        if keycode[1] == 'right': #we are checking if the second item in the keycode list (which is 'right') matches the string 'right'. This condition will evaluate to True, and the player's position will be updated accordingly.
            self.player_pos = (self.player_pos[0] + self.speed, self.player_pos[1]) #This moves the player to the right by adding the speed to the player's current x-position. The y-position stays the same.
            moved = True
        elif keycode[1] == 'left':
            self.player_pos = (self.player_pos[0] - self.speed, self.player_pos[1])
            moved = True
        elif keycode[1] == 'up':
            self.player_pos = (self.player_pos[0], self.player_pos[1] + self.speed)
            moved = True
        elif keycode[1] == 'down':
            self.player_pos = (self.player_pos[0], self.player_pos[1] - self.speed)
            moved = True

        self.player.pos = self.player_pos  # Update the player's rectangle position.

        # Shoot a bullet if the player moved.
        if moved:
            self.shoot_bullet()

    def shoot_bullet(self):
        bullet_x, bullet_y = self.player_pos  # Get the player's current position.
        with self.canvas:
            Color(1, 1, 0, 1)  # Set color to yellow for bullets.
            bullet = Ellipse(pos=(bullet_x + 25, bullet_y + 25), size=(10, 10))  # Create a yellow ellipse for the bullet.
            self.bullets.append(bullet)  # Add the bullet to the list.

    def update(self, dt):
        # Move bullets and check for collisions.
        for bullet in self.bullets:
            bullet.pos = (bullet.pos[0] + 5, bullet.pos[1])  # Move bullet to the right.
            if bullet.pos[0] > self.window_width:  # Check if the bullet is out of bounds.
                self.canvas.remove(bullet)  # Remove bullet from the canvas.
                self.bullets.remove(bullet)  # Remove bullet from the list.
                break

        # Move obstacles randomly and check for collisions.
        for obstacle in self.obstacles:
            # Randomly move obstacles within the window boundaries.
            obstacle.pos = (obstacle.pos[0] + uniform(-self.obstacle_speed, self.obstacle_speed), 
                            obstacle.pos[1] + uniform(-self.obstacle_speed, self.obstacle_speed))
            # Ensure obstacles remain within the window boundaries.
            obstacle.pos = (max(0, min(self.window_width - 30, obstacle.pos[0])),  # Clamp x position.
                            max(0, min(self.window_height - 30, obstacle.pos[1])))  # Clamp y position.

        # Check for collisions between bullets and obstacles.
        for bullet in self.bullets:
            for obstacle in self.obstacles:
                if self.check_collision(bullet, obstacle):  # If a collision is detected:
                    self.canvas.remove(bullet)  # Remove the bullet from the canvas.
                    self.bullets.remove(bullet)  # Remove the bullet from the list.
                    self.canvas.remove(obstacle)  # Remove the obstacle from the canvas.
                    self.obstacles.remove(obstacle)  # Remove the obstacle from the list.
                    self.init_obstacles()  # Create a new obstacle.
                    break

    def check_collision(self, bullet, obstacle):
        # Check for collision between a bullet and an obstacle.
        x1, y1 = bullet.pos  # Get the bullet's position.
        w1, h1 = bullet.size  # Get the bullet's size.

        x2, y2 = obstacle.pos  # Get the obstacle's position.
        w2, h2 = obstacle.size  # Get the obstacle's size.

        # Check if the bullet and obstacle overlap.
        if x1 < x2 + w2 and x1 + w1 > x2 and y1 < y2 + h2 and y1 + h1 > y2:
            return True  # Collision detected.
        return False  # No collision.

class MyApp(App):
    def build(self):
        return MyWidget()  # Build and return the main widget.

if __name__ == '__main__':
    myApp = MyApp()  # Create an instance of MyApp.
    myApp.run()  # Run the application.


"""
Using a list like self.bullets = [] in your game is a common practice for managing multiple items or objects, such as bullets in a shooting game. Let's explore why we need this list and how to determine when to use a list to store things in games.

Why Use a List for self.bullets
Dynamic Quantity:

In a game, the number of bullets can change dynamically as the player shoots bullets. Using a list allows you to store an unknown number of bullets, as they can be added or removed at any time.
For example, every time the player shoots, a new bullet is created and added to the list. If the player shoots 10 times, the list will contain 10 bullets.
Easy Management:

Lists provide convenient methods to manage collections of items. You can easily add bullets, remove them when they go out of bounds, and check for collisions with obstacles.
For instance, when a bullet hits an obstacle or goes off-screen, you can simply remove it from the list, keeping track of only the active bullets.
Iterating Through Items:

You can easily loop through the list of bullets to update their positions or check for collisions with other game objects (like obstacles).
This makes the code cleaner and more organized, as you can handle multiple bullets in one go rather than managing each one individually with separate variables.
When to Use a List in Games
Here are some scenarios where using a list (or similar data structures) is beneficial in game development:

Multiple Similar Objects:

Projectiles: As in your game, you might have multiple bullets or arrows.
Enemies: If there are several enemies on the screen, each one can be stored in a list for easier management.
Items: Collectible items, like coins or power-ups, can also be stored in a list.
Dynamic Changes:

If the number of objects can change during the game (e.g., bullets being fired, enemies being defeated, or obstacles appearing and disappearing), a list is useful.
This allows you to keep track of objects that are actively involved in the game state.
Collision Detection:

When checking for collisions, having all objects stored in a list allows you to loop through them efficiently. For example, you can check each bullet against every obstacle to see if any collisions occur.
Grouping Related Items:

If you have a collection of items that share similar properties or behaviors, a list helps keep them organized. For example, all bullets can be stored together, making it easier to apply a common action or effect to all of them.
Example in Your Game
In your code, self.bullets = [] is used to:

Store bullets: Each time a bullet is fired, you add it to this list.
Manage bullets: In the update method, you can iterate over this list to move each bullet and check if it goes off-screen or collides with an obstacle.
Dynamic handling: When bullets collide with obstacles or go out of bounds, you can remove them from the list, maintaining an accurate representation of the active bullets.
Conclusion
Using lists to store items like bullets, enemies, or collectibles is essential for effective game management. They allow for dynamic changes, easy management, and efficient iteration over game objects. When deciding whether to use a list, consider if the items you want to manage can vary in number and share similar behaviors or properties. If so, a list is often a great choice! If you have more questions or need clarification, feel free to ask!

The append method in Python adds a new item to the end of a list. Here’s how it works in your code:

Firing Bullets: In your shoot_bullet method, you create a new bullet and then add it to the self.bullets list using self.bullets.append(bullet). This makes it easy to keep track of all bullets currently in play.

python
Copy code
def shoot_bullet(self):
    bullet_x, bullet_y = self.player_pos  # Get the player's current position.
    with self.canvas:
        Color(1, 1, 0, 1)  # Set color to yellow for bullets.
        bullet = Ellipse(pos=(bullet_x + 25, bullet_y + 25), size=(10, 10))  # Create a yellow ellipse for the bullet.
        self.bullets.append(bullet)  # Add the bullet to the list.
Managing Bullets: As bullets are created, they are stored in the list. Later, in the update method, you loop through self.bullets to update their positions and check for collisions.

Deciding to Use append: Use append when you want to add an item to a list. If you’re dynamically generating objects (like bullets when a player shoots), append is the appropriate method to use. If you need to remove an item, you would use remove instead.

Other Types of Games Using Lists
Many game genres can benefit from using lists to manage multiple objects:

Platformers: Keeping track of multiple enemies, platforms, and power-ups can be managed with lists.
RPGs (Role-Playing Games): Items like weapons, potions, and quests can be stored in lists for inventory management.
Puzzle Games: Lists can manage pieces (like in Tetris) or blocks that the player interacts with.
Simulation Games: Keeping track of many similar entities (like animals, buildings, or cars) can be handled with lists.
Conclusion
Lists are a powerful tool in game development for managing collections of similar objects that may change during gameplay. They allow for easy addition, removal, and iteration of items, making game code cleaner and more efficient. Use the append method when you need to add new items dynamically to a list. If you have more questions or need further clarification, feel free to ask!








"""

