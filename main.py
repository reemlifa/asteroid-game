import random
import time
import turtle
import math

# Set up the screen
turtle.setup(width=1000, height=1000)
turtle.bgcolor("black")
turtle.title("Asteroids")
turtle.speed(0)
turtle.hideturtle()
turtle.tracer(0)

# Initialize global variables
player = None
missile = None
asteroids = []
particles = []

class Sprite(turtle.Turtle):
    def __init__(self, spriteshape, color, startx, starty):
        turtle.Turtle.__init__(self, shape=spriteshape)
        self.speed(0)
        self.penup()
        self.color(color)
        self.goto(startx, starty)
        self.speed = 1

    def move(self):
        self.fd(self.speed)

        # Boundary detection (wrap around screen)
        if self.xcor() > 290:
            self.setx(self.xcor() - 580)
        if self.xcor() < -290:
            self.setx(self.xcor() + 580)
        if self.ycor() > 290:
            self.sety(self.ycor() - 580)
        if self.ycor() < -290:
            self.sety(self.ycor() + 580)

    def is_collision(self, other):
        # Check for collision based on distance
        distance = 20
        if (self.xcor() >= (other.xcor() - distance)) and \
           (self.xcor() <= (other.xcor() + distance)) and \
           (self.ycor() >= (other.ycor() - distance)) and \
           (self.ycor() <= (other.ycor() + distance)):
            return True
        return False

class Player(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.shapesize(stretch_wid=1.0, stretch_len=2.0, outline=None)
        self.speed = 0
        self.rotation_speed = 0

    def turn_left(self):
        self.rotation_speed = 30
        self.setheading(self.heading() + self.rotation_speed)

    def turn_right(self):
        self.rotation_speed = -30
        self.setheading(self.heading() + self.rotation_speed)

    def move(self):
        pass  # Player does not move vertically or horizontally; it only rotates

class Missile(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.shapesize(stretch_wid=0.2, stretch_len=0.4, outline=None)
        self.speed = 20
        self.status = "ready"
        self.goto(-1000, 1000)

    def fire(self):
        if self.status == "ready":
            self.goto(player.xcor(), player.ycor())
            self.setheading(player.heading())
            self.status = "firing"

    def move(self):
        if self.status == "firing":
            self.fd(self.speed)

        # Border check
        if self.xcor() < -290 or self.xcor() > 290 or \
           self.ycor() < -290 or self.ycor() > 290:
            self.goto(-1000, 1000)
            self.status = "ready"

        # Check for collision with asteroids
        for asteroid in asteroids:
            if self.is_collision(asteroid):
                self.status = "ready"
                asteroid.hideturtle()
                asteroids.remove(asteroid)
                game.score += 1  # Increment score when an asteroid is hit
                self.goto(-1000, 1000)

class Asteroid(Sprite):
    def __init__(self, spriteshape, color, size, speed, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.shapesize(stretch_wid=size, stretch_len=size, outline=None)
        self.speed = speed
        self.size = size
        self.setheading(random.randint(0, 360))

class Game:
    def __init__(self):
        self.level = 1
        self.score = 0
        self.lives = 3
        self.pen = turtle.Turtle()
        self.state = "playing"

    def start_level(self):
        global asteroids
        asteroids = []
        for i in range(self.level):
            while True:
                startx = random.randint(-300, 300)
                starty = random.randint(-300, 300)
                distance_from_earth = math.sqrt(startx**2 + starty**2)
                if distance_from_earth > 160:
                    break
            asteroid = Asteroid("circle", "brown", 3.0, 2, startx, starty)
            asteroids.append(asteroid)

    def draw_border(self):
        self.pen.speed(0)
        self.pen.color("white")
        self.pen.pensize(3)
        self.pen.penup()
        self.pen.goto(-300, 300)
        self.pen.pendown()
        for _ in range(4):
            self.pen.fd(600)
            self.pen.rt(90)
        self.pen.penup()
        self.pen.hideturtle()

        turtle.register_shape("download.gif")
        class CustomSprite(Sprite):
            def __init__(self, startx, starty):
                Sprite.__init__(self, spriteshape="circle", color="black", startx=startx, starty=starty)
                self.shape("download.gif")  # Use the GIF shape
                self.shapesize(stretch_wid=0.02, stretch_len=0.02)
          
        # Initialize a custom sprite
        custom_sprite = CustomSprite(0, 0)


    # def draw_earth(self):
    #     self.pen.penup()
    #     self.pen.goto(0, -130)
    #     self.pen.color("blue")
    #     self.pen.begin_fill()
    #     self.pen.circle(130)
    #     self.pen.end_fill()

    #     # Planets inside Earth (balanced and visually appealing)
    #     planet_positions = [
    #         (-80, -15),  # Left side of Earth
    #         (70, 20),   # Right side of Earth
    #         (-40, -80),  # Bottom-left side
    #         (65, -80),   # Bottom-right side
    #         (-50, 70),   # Top-left side
    #         (55, 60),    # Top-right side
    #         (0, 0)       # Center of Earth
    #     ]
    #     planet_sizes = [18, 15, 17, 16, 14, 18, 20]  # Planet sizes for balance

    #     # Draw planets ensuring they are evenly spaced inside the Earth
    #     self.pen.color("green")
    #     for pos, size in zip(planet_positions, planet_sizes):
    #         self.pen.penup()
    #         self.pen.goto(pos)
    #         self.pen.begin_fill()
    #         self.pen.circle(size)
    #         self.pen.end_fill()

        self.pen.hideturtle()

    def show_status(self):
        self.pen.undo()
        msg = f"ASTEROIDS! Level: {self.level}  Score: {self.score}  Lives: {self.lives}"
        self.pen.penup()
        self.pen.color("white")
        self.pen.goto(-300, 310)
        self.pen.write(msg, font=("Arial", 16, "normal"))

    def game_over(self):
        self.pen.goto(0, 0)
        self.pen.color("yellow")
        self.pen.write("GAME OVER", align="center", font=("Arial", 36, "bold"))

# Create the game and player objects
game = Game()
player = Player("triangle", "white", 0, 0)
missile = Missile("triangle", "yellow", 0, 0)

# Draw the game border and Earth
game.draw_border()


# Start the level
game.start_level()

# Keyboard bindings
turtle.onkeypress(player.turn_left, "Left")
turtle.onkeypress(player.turn_right, "Right")
turtle.onkeypress(missile.fire, "space")
turtle.listen()

# Main game loop
while True:
    turtle.update()
    time.sleep(0.02)

    player.move()
    missile.move()

    # Move asteroids
    for asteroid in asteroids:
        asteroid.move()

        # Check if asteroid touches Earth
        if math.sqrt(asteroid.xcor()**2 + asteroid.ycor()**2) < 130:
            game.lives -= 1
            asteroid.goto(random.randint(-300, 300), random.randint(-300, 300))

    # Check for game over
    if game.lives <= 0:
        game.game_over()
        turtle.update()
        time.sleep(3)
        turtle.bye()
        break

    # Level up if no asteroids are left
    if len(asteroids) == 0:
        game.level += 1
        game.start_level()

    game.show_status()
