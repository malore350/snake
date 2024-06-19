import pygame
import random
import numpy as np

import heapq

pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 300, 300
GRID_SIZE = 20

WINDOW_WIDTH = WIDTH
WINDOW_HEIGHT = HEIGHT + 50  # Extra space for score

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Initialize screen
clock = pygame.time.Clock()

def heuristic(a, b):
      return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star_search(start, goal, obstacles):
      open_list = []
      heapq.heappush(open_list, (0, start))
      came_from = {}
      cost_so_far = {start: 0}

      while open_list:
            _, current = heapq.heappop(open_list)

            if current == goal:
                  break

            for dx, dy in [(-GRID_SIZE, 0), (GRID_SIZE, 0), (0, -GRID_SIZE), (0, GRID_SIZE)]:
                  neighbor = (current[0] + dx, current[1] + dy)
                  if neighbor in obstacles:
                        continue
                  new_cost = cost_so_far[current] + 1
                  if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                        cost_so_far[neighbor] = new_cost
                        priority = new_cost + heuristic(goal, neighbor)
                        heapq.heappush(open_list, (priority, neighbor))
                        came_from[neighbor] = current

      # Reconstruct path
      path = []
      while current in came_from:
            path.append(current)
            current = came_from[current]
      path.reverse()

      return path

class SnakeGameAI:
      def __init__(self):
            self.snake = [(100, 100), (80, 100), (60, 100)]
            self.direction = (20, 0)
            self.food = self.generate_food()
            self.score = 0
            self.done = False

      def reset(self):
            self.snake = [(100, 100), (80, 100), (60, 100)]
            self.direction = (20, 0)
            self.food = self.generate_food()
            self.score = 0
            self.done = False
            return self.get_state()

      def step(self, action):
            # Update direction based on action
            if action == 0:   # Up
                  if self.direction != (0, 20):
                        self.direction = (0, -20)
            elif action == 1:  # Down
                  if self.direction != (0, -20):
                        self.direction = (0, 20)
            elif action == 2:  # Left
                  if self.direction != (20, 0):
                        self.direction = (-20, 0)
            elif action == 3:  # Right
                  if self.direction != (-20, 0):
                        self.direction = (20, 0)

            self.move_snake()
            reward = -1  # Penalize each move to encourage shorter paths

            if self.check_collision():
                  self.done = True
                  reward = -20
            elif self.snake[0] == self.food:
                  self.snake.append(self.snake[-1])
                  self.food = self.generate_food()
                  self.score += 1
                  reward = 20
            else:
                  # Calculate path using A* algorithm
                  path = a_star_search(self.snake[0], self.food, set(self.snake))
                  if path:
                        next_move = path[0]
                        if next_move[0] > self.snake[0][0]:
                              self.direction = (GRID_SIZE, 0)
                        elif next_move[0] < self.snake[0][0]:
                              self.direction = (-GRID_SIZE, 0)
                        elif next_move[1] > self.snake[0][1]:
                              self.direction = (0, GRID_SIZE)
                        elif next_move[1] < self.snake[0][1]:
                              self.direction = (0, -GRID_SIZE)

            return self.get_state(), reward, self.done


      def move_snake(self):
            new_head = ((self.snake[0][0] + self.direction[0]) % WIDTH, (self.snake[0][1] + self.direction[1]) % HEIGHT)
            self.snake.insert(0, new_head)
            self.snake.pop()

      def check_collision(self):
            head = self.snake[0]
            return head in self.snake[1:]

      def generate_food(self):
        while True:
                  new_food = (random.randint(0, (WIDTH - GRID_SIZE) // GRID_SIZE) * GRID_SIZE,
                              random.randint(0, (HEIGHT - GRID_SIZE) // GRID_SIZE) * GRID_SIZE)
                  if new_food not in self.snake:
                        return new_food

      def get_state(self):
            head_x, head_y = self.snake[0]
            food_x, food_y = self.food
            direction_x, direction_y = self.direction

            # Relative position of food
            food_rel_x = (food_x - head_x) / WIDTH
            food_rel_y = (food_y - head_y) / HEIGHT

            # Obstacles
            danger_straight = (head_x + direction_x, head_y + direction_y) in self.snake
            danger_left = (head_x + direction_y, head_y - direction_x) in self.snake
            danger_right = (head_x - direction_y, head_y + direction_x) in self.snake

            state = [
                  # Danger straight, left, right
                  danger_straight,
                  danger_left,
                  danger_right,
                  # Current direction
                  direction_x == 20,
                  direction_x == -20,
                  direction_y == 20,
                  direction_y == -20,
                  # Relative position of food
                  food_rel_x,
                  food_rel_y
            ]

            return np.array(state, dtype=int)


      def render(self):
            screen.fill(BLACK)

            # Draw score in the extra space
            font = pygame.font.Font(None, 36)
            text = font.render(f'Score: {self.score}', True, WHITE)
            screen.blit(text, (10, 10))  # Draw text at the top of the window

            # Draw borders
            pygame.draw.line(screen, WHITE, (0, 50), (WIDTH, 50), 5)  # Top border
            pygame.draw.line(screen, WHITE, (0, HEIGHT + 50), (WIDTH, HEIGHT + 50), 5)  # Bottom border
            pygame.draw.line(screen, WHITE, (0, 50), (0, HEIGHT + 50), 5)  # Left border
            pygame.draw.line(screen, WHITE, (WIDTH, 50), (WIDTH, HEIGHT + 50), 5)  # Right border

            # Draw snake and food
            for segment in self.snake:
                  pygame.draw.rect(screen, GREEN, (segment[0], segment[1] + 50, GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, RED, (self.food[0], self.food[1] + 50, GRID_SIZE, GRID_SIZE))

            pygame.display.flip()
            clock.tick(10)

class GameScreen:
      def start_screen(self):
            while True:
                  screen.fill(BLACK)
                  font = pygame.font.Font(None, 22)
                  text = font.render('Press any key to start the game', True, WHITE)
                  screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
                  pygame.display.flip()

                  for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                              pygame.quit()
                              sys.exit()
                        elif event.type == pygame.KEYDOWN:
                              return

      def game_over_screen(self):
            button_width = 200
            button_height = 50
            exit_button = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2, button_width, button_height)
            play_again_button = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2 - 60, button_width, button_height)

            while True:
                  for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                              pygame.quit()
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                              mouse_pos = event.pos
                              if exit_button.collidepoint(mouse_pos):
                                    pygame.quit()
                              elif play_again_button.collidepoint(mouse_pos):
                                    return True

                  screen.fill(BLACK)
                  font = pygame.font.Font(None, 22)

                  # Draw exit button
                  pygame.draw.rect(screen, RED, exit_button)  # Draw button
                  exit_text = font.render('Exit', True, WHITE)
                  screen.blit(exit_text, (exit_button.x + (exit_button.width - exit_text.get_width()) // 2, exit_button.y + (exit_button.height - exit_text.get_height()) // 2))  # Draw text

                  # Draw play again button
                  pygame.draw.rect(screen, GREEN, play_again_button)  # Draw button
                  play_again_text = font.render('Play Again', True, WHITE)
                  screen.blit(play_again_text, (play_again_button.x + (play_again_button.width - play_again_text.get_width()) // 2, play_again_button.y + (play_again_button.height - play_again_text.get_height()) // 2))  # Draw text

                  pygame.display.flip()

# Example usage
if __name__ == "__main__":
      game = SnakeGameAI()
      state = game.reset()

      running = True
      while running:
            for event in pygame.event.get():
                  if event.type == pygame.QUIT:
                        running = False

            # Replace this with the action from the neural network
            action = random.randint(0, 3)
            state, reward, done = game.step(action)
            game.render()

            if done:
                  game.reset()

      pygame.quit()
