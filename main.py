import pygame
import random

pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 400
GRID_SIZE = 20

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Snake and Food
snake = [(100, 100), (80, 100), (60, 100)]
direction = (20, 0)
food = (300, 200)

def draw_snake(snake):
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (*segment, GRID_SIZE, GRID_SIZE))

def draw_food(food):
    pygame.draw.rect(screen, RED, (*food, GRID_SIZE, GRID_SIZE))

def move_snake(snake, direction):
    new_head = ((snake[0][0] + direction[0]) % WIDTH, (snake[0][1] + direction[1]) % HEIGHT)
    snake.insert(0, new_head)
    snake.pop()

def check_collision(snake):
    head = snake[0]
    return head in snake[1:]

def generate_food(snake):
    while True:
        new_food = (random.randint(0, (WIDTH - GRID_SIZE) // GRID_SIZE) * GRID_SIZE,
                    random.randint(0, (HEIGHT - GRID_SIZE) // GRID_SIZE) * GRID_SIZE)
        if new_food not in snake:
            return new_food

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != (0, 20):
                direction = (0, -20)
            elif event.key == pygame.K_DOWN and direction != (0, -20):
                direction = (0, 20)
            elif event.key == pygame.K_LEFT and direction != (20, 0):
                direction = (-20, 0)
            elif event.key == pygame.K_RIGHT and direction != (-20, 0):
                direction = (20, 0)

    move_snake(snake, direction)

    if check_collision(snake):
        running = False

    if snake[0] == food:
        snake.append(snake[-1])
        food = generate_food(snake)

    screen.fill(BLACK)
    draw_snake(snake)
    draw_food(food)
    pygame.display.flip()
    clock.tick(10)

pygame.quit()
