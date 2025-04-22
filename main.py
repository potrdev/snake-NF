import pygame as pg
import sys
import random

pg.init()

WIN_X, WIN_Y = 810, 600
SNAKE_SIZE = 30
FPS = 10

screen = pg.display.set_mode((WIN_X, WIN_Y))
pg.display.set_caption("Kača")
clock = pg.time.Clock()

font = pg.font.Font(None, 36)

# Load sounds
collect_sound = pg.mixer.Sound("collect.mp3")
bg_music = pg.mixer.Sound("music.mp3")
bg_music.play(-1)  # Play background music in a loop
bg_music.set_volume(0.2)

class SnakePart:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = (0, 255, 0)

    def move(self, new_x=None, new_y=None):
        if new_x is not None and new_y is not None:
            self.x = new_x
            self.y = new_y

class Snake:
    def __init__(self, x, y):
        self.parts = [SnakePart(x, y)]
        self.direction = "R"
        self.growing = False

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

        self.parts.insert(0, SnakePart(head_x, head_y))

        if not self.growing:
            self.parts.pop()
        else:
            self.growing = False

    def change_direction(self, new_direction):
        if (self.direction == "L" and new_direction != "R") or \
           (self.direction == "R" and new_direction != "L") or \
           (self.direction == "U" and new_direction != "D") or \
           (self.direction == "D" and new_direction != "U"):
            self.direction = new_direction

    def grow(self):
        self.growing = True

    def update_colors(self):
        for i in range(len(self.parts)):
            if i == 0 or i % 2 == 0:
                self.parts[i].color = (0, 180, 0)
            else:
                self.parts[i].color = (0, 255, 0)

    def check_collision(self):
        head = self.parts[0]
        for part in self.parts[1:]:
            if head.x == part.x and head.y == part.y:
                return True
        return False

    def reset(self, x, y):
        self.parts = [SnakePart(x, y)]
        self.direction = "R"
        self.growing = False

def spawn_food(snake_parts):
    while True:
        food_x = random.randint(0, (WIN_X - SNAKE_SIZE) // SNAKE_SIZE) * SNAKE_SIZE
        food_y = random.randint(0, (WIN_Y - SNAKE_SIZE) // SNAKE_SIZE) * SNAKE_SIZE
        if all(part.x != food_x or part.y != food_y for part in snake_parts):
            return food_x, food_y

snake = Snake(0, 0)
score = 0
food_positions = [spawn_food(snake.parts)]

running = True
game_over = False
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    if not game_over:
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

        for food in food_positions:
            if snake.parts[0].x == food[0] and snake.parts[0].y == food[1]:
                snake.grow()
                score += 1
                collect_sound.play()  # Play collect sound
                food_positions.append(spawn_food(snake.parts))  # Spawn new food
                food_positions.remove(food)
                break

        if snake.check_collision() or \
           snake.parts[0].x < 0 or snake.parts[0].x >= WIN_X or \
           snake.parts[0].y < 0 or snake.parts[0].y >= WIN_Y:
            game_over = True

        snake.update_colors()

        for i in range(0, WIN_Y // SNAKE_SIZE * 2):
            for j in range(0, WIN_X // SNAKE_SIZE * 2):
                color = "#141414" if (i + j) % 2 == 0 else "#1c1c1b"
                pg.draw.rect(screen, color, (SNAKE_SIZE * j, SNAKE_SIZE * i, SNAKE_SIZE, SNAKE_SIZE))

        for part in snake.parts:
            pg.draw.rect(screen, part.color, (part.x, part.y, SNAKE_SIZE, SNAKE_SIZE))

        for food in food_positions:
            pg.draw.rect(screen, (255, 0, 0), (food[0], food[1], SNAKE_SIZE, SNAKE_SIZE))

        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

    else:
        game_over_text = font.render("GAME OVER", True, (255, 0, 0))
        score_display = font.render(f"Final Score: {score}", True, (255, 255, 255))
        retry_text = font.render("Press R to Retry", True, (255, 255, 255))
        screen.blit(game_over_text, (WIN_X // 2 - game_over_text.get_width() // 2, WIN_Y // 2 - 20))
        screen.blit(score_display, (WIN_X // 2 - score_display.get_width() // 2, WIN_Y // 2 + 20))
        screen.blit(retry_text, (WIN_X // 2 - retry_text.get_width() // 2, WIN_Y // 2 + 60))

        keys = pg.key.get_pressed()
        if keys[pg.K_r]:  # Retry the game
            snake.reset(0, 0)
            score = 0
            food_positions = [spawn_food(snake.parts)]
            game_over = False

    clock.tick(FPS)
    pg.display.flip()

pg.quit()
sys.exit()
