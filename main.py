import pygame as pg
import sys
import random

pg.init()

WIN_X, WIN_Y = 800, 600
SNAKE_SIZE = 30
FPS = 10

screen = pg.display.set_mode((WIN_X, WIN_Y))
pg.display.set_caption("Kača")
clock = pg.time.Clock()

class SnakePart:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = (0, 255, 0)  # Default color

    def move(self, new_x=None, new_y=None):
        if new_x is not None and new_y is not None:
            self.x = new_x
            self.y = new_y

class Snake:
    def __init__(self, x, y):
        self.parts = [SnakePart(x, y)]
        self.direction = "R"

    def move(self):
        head_x = self.parts[0].x
        head_y = self.parts[0].y

        if self.direction == "L":
            head_x -= SNAKE_SIZE
        elif self.direction == "R":
            head_x += SNAKE_SIZE
        elif self.direction == "U":
            head_y -= SNAKE_SIZE
        elif self.direction == "D":
            head_y += SNAKE_SIZE

        self.parts.insert(0, SnakePart(head_x, head_y))  # Add new head
        self.parts.pop()  # Remove the last part

    def change_direction(self, new_direction):
        if (self.direction == "L" and new_direction != "R") or \
           (self.direction == "R" and new_direction != "L") or \
           (self.direction == "U" and new_direction != "D") or \
           (self.direction == "D" and new_direction != "U"):
            self.direction = new_direction

    def grow(self):
        last_part = self.parts[-1]
        self.parts.append(SnakePart(last_part.x, last_part.y))  # Add a new part at the end

    def update_colors(self):
        for i in range(len(self.parts)):
            if i == 0 or i % 2 == 0:
                self.parts[i].color = (0, 200, 0)  # Dark green
            else:
                self.parts[i].color = (0, 255, 0)  # Light green

snake = Snake(0, 0)

food_x = random.randint(0, (WIN_X - SNAKE_SIZE) // SNAKE_SIZE) * SNAKE_SIZE
food_y = random.randint(0, (WIN_Y - SNAKE_SIZE) // SNAKE_SIZE) * SNAKE_SIZE

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    keys = pg.key.get_pressed()
    if keys[pg.K_w]:
        snake.change_direction("U")
    if keys[pg.K_s]:
        snake.change_direction("D")
    if keys[pg.K_a]:
        snake.change_direction("L")
    if keys[pg.K_d]:
        snake.change_direction("R")

    snake.move()

    if snake.parts[0].x == food_x and snake.parts[0].y == food_y:
        snake.grow()
        food_x = random.randint(0, (WIN_X - SNAKE_SIZE) // SNAKE_SIZE) * SNAKE_SIZE
        food_y = random.randint(0, (WIN_Y - SNAKE_SIZE) // SNAKE_SIZE) * SNAKE_SIZE

    snake.update_colors()  # Update colors of the snake parts

    screen.fill((0, 0, 0))

    for part in snake.parts:
        pg.draw.rect(screen, part.color, (part.x, part.y, SNAKE_SIZE, SNAKE_SIZE))

    pg.draw.rect(screen, (255, 0, 0), (food_x, food_y, SNAKE_SIZE, SNAKE_SIZE))

    clock.tick(FPS)

    pg.display.flip()

pg.quit()
sys.exit()