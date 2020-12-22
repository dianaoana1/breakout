"""
Breakout Arcade Game
========================
Created by: Diana Alexandra Merlusca
Start date: January 5 2020
========================
This is a simple breakout game where player uses a ball and a paddle to break bricks
"""
import pygame
import random
import math

# Define the width and height of the output window
(width, height) = (1050, 600)
clock = pygame.time.Clock()


# Class for the ball
class Particle(pygame.sprite.Sprite):
    # The __init__ thing basically memorizes the information you give it
    # so that you can reuse it later on
    def __init__(self, position):
        super().__init__()
        self.x, self.y = position
        self.size = 8
        self.colour = (150, 203, 239)
        self.thickness = 0
        self.speed = 7
        self.angle = random.uniform(math.pi*3/4, math.pi*5/4)

    # When you assign functions in a class you use the information assigned in __init__
    # to make other things with it, such as displaying, moving, etc.
    def display(self):
        self.rect = pygame.draw.circle(screen, self.colour, (int(self.x), int(self.y)), self.size, self.thickness)

    def move(self):
        self.x += math.sin(self.angle) * self.speed
        self.y -= math.cos(self.angle) * self.speed

    def bounce(self):
        if self.x > width - self.size:
            self.angle = -self.angle
        elif self.x < self.size:
            self.angle = -self.angle
        if self.y > height - self.size:
            self.angle = -self.angle + math.pi
        elif self.y < self.size:
            self.angle = -self.angle + math.pi

    def bounceoffpaddle(self):
        self.angle = -self.angle + math.pi


# Class for the paddle
class Platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x = 475
        self.y = 550
        self.width = 100
        self.height = 15
        self.colour = (255, 255, 255)
        self.thickness = 0
        self.movex = 0  # move along x

    def display(self):
        self.rect = pygame.draw.rect(screen, self.colour,(int(self.x), int(self.y), self.width, self.height), self.thickness)

    def control(self, x):
        self.movex += x

    def update(self):
        self.x += self.movex


class Block(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.width = 50
        self.height = 25
        self.colour = (255, 255, 255)
        self.thickness = 0
        self.blockx, self.blocky = position

    def display(self):
        self.rect = pygame.draw.rect(screen, self.colour,(int(self.blockx), int(self.blocky), self.width, self.height), self.thickness)


# Create a new pygame screen with this width and height
screen = pygame.display.set_mode((width, height))
# Set a name for the window
pygame.display.set_caption("Breakout yayy :)")

x = random.randint(50, 1000)
y = random.randint(250, 250)
blockx = random.randint(50, 1000)
blocky = random.randint(10, 200)

# Creating the ball
Ball = Particle((x, y))
# Creating the paddle
Paddle = Platform()
# Creating the block
Block = Block((blockx, blocky))

# Draw the screen
pygame.display.flip()

# Create a group of 1 ball (used in checking collision)
balls = pygame.sprite.Group()
balls.add(Ball)

# Create a group containing all of the blocks
blocks = pygame.sprite.Group()
for i in range(10):
    blocks.add(Block)

# ---------- Main Program Loop ----------
# Run until something sets `running` to False
running = True
while running:
    list_of_events = pygame.event.get()
    screen.fill((0, 0, 0))
    Ball.move()
    Ball.x = Ball.x # Wraps the movement of the ball around the screen
    Ball.y = Ball.y
    Ball.bounce()
    Ball.display()

    Paddle.update()
    Paddle.display()

    # Displaying all of the blocks
    blocks.update()
    blocks.draw(screen)

    pygame.display.update()  # Redraws the screen, incidentally the same as pygame.display.flip()
    clock.tick(30)
    # Checking for collisions
    # This code creates a list of sprites in group balls that overlapped with Paddle
    # Setting it to true removes colliding particles from list, false does not remove them
    col = pygame.sprite.spritecollide(Paddle, balls, False)
    if col:
        Ball.bounceoffpaddle()
        print("Collision")
    if len(list_of_events) > 0:
        print('\n\n')
        print(list_of_events)
        print('\n\n')
    # ---------------- EVENT LOOP: SHIT HAPPENS ONLY DURING AN EVENT ----------------
    # Loop through the current waiting events, setting event to each one in turn
    for event in list_of_events:
        # Print the current event for debug purposes
        print(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == ord("a"):
                print("left")
                Paddle.control(-10)
            if event.key == pygame.K_RIGHT or event.key == ord("d"):
                print("right")
                Paddle.control(10)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == ord("a") or Paddle.x == 0:
                Paddle.control(10)
                print("left stop")
            if event.key == pygame.K_RIGHT or event.key == ord("d") or Paddle.x == 1050:
                Paddle.control(-10)
                print("right stop")
        # If the event is a 'QUIT' event, set running to False which will stop our loop
        if event.type == pygame.QUIT:
            running = False

# TODO
# 1. ~~Make ball and paddle collide~~
# 2. create bricks
# 3. Have the ball interact with the bricks
# 4. Add a score
# 5. Create title screen