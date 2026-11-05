"""Модуль. Изгиб питона."""
from random import choice, randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (75, 176, 83)
# (93, 216, 228) - старый цвет

# Цвет яблока
APPLE_COLOR = (255, 15, 23)
# (255, 0, 0) - старый цвет

# Цвет лимона
LEMON_COLOR = (255, 255, 23)

# Цвет камня
STONE_COLOR = (128, 128, 128)

# Цвет змейки
SNAKE_COLOR = (57, 255, 57)
# (0, 255, 0) - старый цвет

# Скорость движения змейки:
SPEED = 10
MIN_SPEED = 5
MAX_SPEED = 30

# Минимальное и максимальное количество камней
MIN_STONES = 4
MAX_STONES = 8

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self, body_color=None):
        """Задает позицию (центр экрана) и цвет объекта."""
        self.position = (
            (GRID_WIDTH // 2) * GRID_SIZE,
            (GRID_HEIGHT // 2) * GRID_SIZE,
        )
        self.body_color = body_color

    def draw(self):
        """Отрисовка объекта. Переопределяется в дочерних классах."""
        pass


class Apple(GameObject):
    """Класс объекта - яблоко."""

    def __init__(self, body_color=APPLE_COLOR):
        """Задает цвет яблока и случайную начальную позицию."""
        super().__init__(body_color)
        self.randomize_position()

    def randomize_position(self):
        """Задаёт случайную позицию яблока на игровом поле."""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
        )

    def draw(self):
        """Отрисовывает яблоко размеров в одну клетку."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Lemon(GameObject):
    """Класс объекта - лимон."""

    def __init__(self, body_color=LEMON_COLOR):
        """Задает цвет лимона и случайную начальную позицию."""
        super().__init__(body_color)
        self.randomize_position()

    def randomize_position(self):
        """Задаёт случайную позицию лимона на игровом поле."""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
        )

    def draw(self):
        """Отрисовывает лимон размеров в одну клетку."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Stone(GameObject):
    """Класс объекта - камень."""

    def __init__(self, body_color=STONE_COLOR):
        """Задает цвет камня и случайную начальную позицию."""
        super().__init__(body_color)
        self.randomize_position()

    def randomize_position(self):
        """Задаёт случайную позицию камня на игровом поле."""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
        )

    def place_free(self, snake, apple, lemon, stones):
        """Ставит камень в свободную клетку поля."""
        self.randomize_position()
        while is_occupied(
            self.position,
            snake,
            apple,
            lemon,
            stones,
            exclude=self
        ):
            self.randomize_position()

    def draw(self):
        """Отрисовывает камень размеров в одну клетку."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс змейки."""

    def __init__(self, body_color=SNAKE_COLOR):
        """Инициализирует начальное состояние змейки."""
        super().__init__(body_color)
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = []

    def get_head_position(self):
        """Возвращает координаты головы змейки."""
        return self.positions[0]

    def update_direction(self):
        """Применяет выбранное пользователем направление движения."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Задает движение змейке."""
        head_x, head_y = self.get_head_position()
        direction_x, direction_y = self.direction

        # Шаг на одну клетку с телепортом через границы поля.
        new_head = (
            (head_x + direction_x * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + direction_y * GRID_SIZE) % SCREEN_HEIGHT,
        )

        self.positions.insert(0, new_head)
        self.last = []

        if len(self.positions) > self.length:
            self.last.append(self.positions.pop())

    def shrink(self):
        """Уменьшает змейку."""
        if self.length > 1:
            self.length -= 1
            self.last.append(self.positions.pop())

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.length = 1
        self.positions = [
            (
                (GRID_WIDTH // 2) * GRID_SIZE,
                (GRID_HEIGHT // 2) * GRID_SIZE,
            )
        ]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None
        self.last = []

    def draw(self):
        """Отрисовывает змейку и затирает след последнего сегмента."""
        for position in self.positions[:-1]:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание всех клеток, удалённых за кадр
        for cell in self.last:
            last_rect = pygame.Rect(cell, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


def handle_keys(game_object):
    """Обрабатывает нажатия клавиш для смены направления змейки."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def eat_apple(apple, snake, lemon, stones, speed):
    """Обрабатывает поедание яблока, возвращает новую скорость."""
    snake.length += 1
    speed = min(speed + 1, MAX_SPEED)
    while is_occupied(
            apple.position, snake, apple, lemon, stones, exclude=apple):
        apple.randomize_position()
    for stone in stones:
        stone.place_free(snake, apple, lemon, stones)
    return speed


def eat_lemon(lemon, snake, apple, stones, speed):
    """Обрабатывает поедание лимона, возвращает новую скорость."""
    if snake.length > 1:
        snake.shrink()
        speed = max(speed - 1, MIN_SPEED)
    while is_occupied(
            lemon.position, snake, apple, lemon, stones, exclude=lemon):
        lemon.randomize_position()
    for stone in stones:
        stone.place_free(snake, apple, lemon, stones)
    return speed


def is_occupied(
        position,
        snake,
        apple,
        lemon,
        stones,
        exclude=None
):
    """Проверяет, занята ли клетка каким-нибудь игровым объектом."""
    objects = [apple, lemon, *stones]
    if exclude is not None:
        objects = [obj for obj in objects if obj is not exclude]
    return (
        position in snake.positions
        or any(position == obj.position for obj in objects)
    )


def create_stones(
        snake,
        apple,
        lemon
):
    """Создаёт случайное количество камней в свободных клетках."""
    count = randint(MIN_STONES, MAX_STONES)
    stones = [Stone() for _ in range(count)]

    center = (
        (GRID_WIDTH // 2) * GRID_SIZE,
        (GRID_HEIGHT // 2) * GRID_SIZE,
    )
    for stone in stones:
        while stone.position == center or is_occupied(
                stone.position, snake, apple, lemon, stones,
                exclude=stone):
            stone.randomize_position()
    return stones


def main():
    """Запускает основной игровой цикл."""
    global SPEED  # Разрешаем изменять глобальную SPEED

    # Инициализация PyGame:
    pygame.init()

    # Тут нужно создать экземпляры классов.
    snake = Snake()
    apple = Apple()
    lemon = Lemon()
    stones = create_stones(snake, apple, lemon)

    initial_speed = SPEED

    screen.fill(BOARD_BACKGROUND_COLOR)

    while True:
        clock.tick(SPEED)

        handle_keys(snake)
        snake.update_direction()
        snake.move()

        # Тут опишите основную логику игры.
        # Если столкнулись с камнем, сбрасываем игру.
        if any(
            snake.get_head_position() == stone.position for stone in stones
        ):
            snake.reset()
            stones = create_stones(snake, apple, lemon)
            SPEED = initial_speed

        # Если съедаем яблоко, увеличиваем змейку, и появляется новое яблоко.
        if snake.get_head_position() == apple.position:
            SPEED = eat_apple(apple, snake, lemon, stones, SPEED)
            # Каждый раз при поедании яблока камни перемещается.
            for stone in stones:
                stone.place_free(snake, apple, lemon, stones)

        # Если съедаем лимон, уменьшаем змейку, и появляется новый лимон.
        if snake.get_head_position() == lemon.position:
            SPEED = eat_lemon(lemon, snake, apple, stones, SPEED)
            # Каждый раз при поедании лимона камни перемещается.
            for stone in stones:
                stone.place_free(snake, apple, lemon, stones)

        # Если столкнулись с собственным телом, сбрасываем игру.
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            stones = create_stones(snake, apple, lemon)
            SPEED = initial_speed

        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        lemon.draw()
        for stone in stones:
            stone.draw()
        snake.draw()

        pygame.display.update()


if __name__ == '__main__':
    main()
