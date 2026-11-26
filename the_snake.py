import random
from abc import ABC, abstractmethod

import pygame

pygame.init()

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

BOARD_BACKGROUND_COLOR = (0, 0, 0)
GRID_COLOR = (10, 10, 10)
SNAKE_COLOR = (0, 255, 0)
APPLE_COLOR = (255, 0, 0)

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()


class GameObject(ABC):
    """Базовый класс игровых объектов."""

    def __init__(self, position, body_color):
        """Инициализирует позицию и цвет."""
        self.position = position
        self.body_color = body_color

    @abstractmethod
    def draw(self, surface):
        """Рисует объект на поверхности."""
        pass


class Apple(GameObject):
    """Яблоко со случайной позицией на поле."""

    def __init__(self):
        """Создаёт яблоко в случайной клетке."""
        super().__init__(
            position=(
                random.randint(0, GRID_WIDTH - 1),
                random.randint(0, GRID_HEIGHT - 1),
            ),
            body_color=APPLE_COLOR,
        )

    def randomize_position(self, snake_positions=None):
        """Ставит яблоко в свободную от змейки клетку."""
        if snake_positions is None:
            snake_positions = []
        while True:
            new_pos = (
                random.randint(0, GRID_WIDTH - 1),
                random.randint(0, GRID_HEIGHT - 1),
            )
            if new_pos not in snake_positions:
                self.position = new_pos
                break

    def draw(self, surface):
        """Рисует квадрат яблока."""
        rect = pygame.Rect(
            (self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE),
            (GRID_SIZE, GRID_SIZE),
        )
        pygame.draw.rect(surface, self.body_color, rect)


class Snake(GameObject):
    """Змейка из сегментов тела."""

    def __init__(self):
        """Создаёт змейку длиной 1 в центре."""
        center = (GRID_WIDTH // 2, GRID_HEIGHT // 2)
        super().__init__(position=center, body_color=SNAKE_COLOR)
        self.length = 1
        self.positions = [center]
        self.direction = RIGHT
        self.next_direction = RIGHT

    def update_direction(self):
        """Меняет направление, если новое не противоположно."""
        if (self.next_direction[0] + self.direction[0] != 0
                or self.next_direction[1] + self.direction[1] != 0):
            self.direction = self.next_direction

    def get_head_position(self):
        """Возвращает координаты головы."""
        return self.positions[0]

    def move(self):
        """Сдвигает змейку, проверяя столкновение с собой."""
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
        """Рисует все сегменты змейки."""
        for position in self.positions:
            rect = pygame.Rect(
                (position[0] * GRID_SIZE, position[1] * GRID_SIZE),
                (GRID_SIZE, GRID_SIZE),
            )
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, rect, 1)

    def reset(self):
        """Возвращает змейку в начальное состояние."""
        center = (GRID_WIDTH // 2, GRID_HEIGHT // 2)
        self.length = 1
        self.positions = [center]
        self.direction = RIGHT
        self.next_direction = RIGHT


def handle_keys(game_object):
    """Меняет направление змейки по стрелкам."""
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and game_object.direction != DOWN:
        game_object.next_direction = UP
    elif keys[pygame.K_DOWN] and game_object.direction != UP:
        game_object.next_direction = DOWN
    elif keys[pygame.K_LEFT] and game_object.direction != RIGHT:
        game_object.next_direction = LEFT
    elif keys[pygame.K_RIGHT] and game_object.direction != LEFT:
        game_object.next_direction = RIGHT


def draw_grid(surface):
    """Рисует сетку поля."""
    for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
        for x in range(0, SCREEN_WIDTH, GRID_SIZE):
            rect = pygame.Rect((x, y), (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, GRID_COLOR, rect, 1)


def main():
    """Запускает игровой цикл."""
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

        screen.fill(BOARD_BACKGROUND_COLOR)
        draw_grid(screen)
        apple.draw(screen)
        snake.draw(screen)

        pygame.display.update()
        clock.tick(10)

    pygame.quit()


if __name__ == '__main__':
    main()
