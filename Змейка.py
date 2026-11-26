import random
from abc import ABC, abstractmethod

import pygame


SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

BG_COLOR = (0, 0, 0)
GRID_COLOR = (10, 10, 10)
SNAKE_COLOR = (0, 255, 0)
APPLE_COLOR = (255, 0, 0)

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


class GameObj(ABC):

    def __init__(self, position, body_color):
        self.position = position
        self.body_color = body_color

    @abstractmethod
    def draw(self, surface):
        pass


class Apple(GameObj):

    def __init__(self):
        super().__init__(
            position=(
                random.randint(0, GRID_WIDTH - 1),
                random.randint(0, GRID_HEIGHT - 1),
            ),
            body_color=APPLE_COLOR,
        )

    def randomize_position(self, snake_positions):
        while True:
            new_pos = (
                random.randint(0, GRID_WIDTH - 1),
                random.randint(0, GRID_HEIGHT - 1),
            )
            if new_pos not in snake_positions:
                self.position = new_pos
                break

    def draw(self, surface):
        rect = pygame.Rect(
            (self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE),
            (GRID_SIZE, GRID_SIZE),
        )
        pygame.draw.rect(surface, self.body_color, rect)


class Snake(GameObj):

    def __init__(self):
        center = (GRID_WIDTH // 2, GRID_HEIGHT // 2)
        super().__init__(position=center, body_color=SNAKE_COLOR)
        self.length = 1
        self.positions = [center]
        self.direction = RIGHT
        self.next_direction = RIGHT

    def update_direction(self):
        if (self.next_direction[0] + self.direction[0] != 0
                or self.next_direction[1] + self.direction[1] != 0):
            self.direction = self.next_direction

    def get_head_position(self):
        return self.positions[0]

    def move(self):
        self.update_direction()
        head = self.get_head_position()
        new_head = (
            (head[0] + self.direction[0]) % GRID_WIDTH,
            (head[1] + self.direction[1]) % GRID_HEIGHT,
        )

        if new_head in self.positions[1:]:
            self.reset()
            return

        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self, surface):
        for position in self.positions:
            rect = pygame.Rect(
                (position[0] * GRID_SIZE, position[1] * GRID_SIZE),
                (GRID_SIZE, GRID_SIZE),
            )
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, BG_COLOR, rect, 1)

    def reset(self):
        center = (GRID_WIDTH // 2, GRID_HEIGHT // 2)
        self.length = 1
        self.positions = [center]
        self.direction = RIGHT
        self.next_direction = RIGHT


def handle_keys(snake):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        snake.next_direction = UP
    elif keys[pygame.K_DOWN]:
        snake.next_direction = DOWN
    elif keys[pygame.K_LEFT]:
        snake.next_direction = LEFT
    elif keys[pygame.K_RIGHT]:
        snake.next_direction = RIGHT


def draw_grid(surface):
    for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
        for x in range(0, SCREEN_WIDTH, GRID_SIZE):
            rect = pygame.Rect((x, y), (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, GRID_COLOR, rect, 1)


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Змейка')
    clock = pygame.time.Clock()

    snake = Snake()
    apple = Apple()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        handle_keys(snake)
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)

        screen.fill(BG_COLOR)
        draw_grid(screen)
        apple.draw(screen)
        snake.draw(screen)

        pygame.display.update()
        clock.tick(10)

    pygame.quit()


if __name__ == '__main__':
    main()
