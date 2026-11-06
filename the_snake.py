"""Модуль. Изгиб питона."""
from random import choice, randint

import pygame as pg

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
MAX_SPEED = 20

# Минимальное и максимальное количество камней
MIN_STONES = 3
MAX_STONES = 6

# Словарь с назначением клавиш
KEY_DIRECTIONS = {
    (pg.K_UP, RIGHT): UP,
    (pg.K_UP, LEFT): UP,
    (pg.K_DOWN, RIGHT): DOWN,
    (pg.K_DOWN, LEFT): DOWN,
    (pg.K_LEFT, UP): LEFT,
    (pg.K_LEFT, DOWN): LEFT,
    (pg.K_RIGHT, UP): RIGHT,
    (pg.K_RIGHT, DOWN): RIGHT,
}

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self, body_color=None):
        """Задает позицию (центр экрана) и цвет объекта."""
        self.position = (
            (GRID_WIDTH // 2) * GRID_SIZE,
            (GRID_HEIGHT // 2) * GRID_SIZE,
        )
        self.body_color = body_color

    def randomize_position(self, occupied_cells=frozenset()):
        """Задаёт случайную позицию объекта на игровом поле."""
        while True:
            self.position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
            )
            if self.position not in occupied_cells:
                return

    def _draw_cell(self, position=None, color=None, border=True):
        """Отрисовывет одну клетку в заданной позиции и цвете."""
        position = position or self.position
        color = color or self.body_color
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, color, rect)
        if border:
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)

    def draw(self):
        """Отрисовка объекта. Переопределяется в дочерних классах."""
        raise NotImplementedError(
            f'Метод draw() класса {type(self).__name__} '
            'должен быть переопределен в дочернем классе.'
        )


class Apple(GameObject):
    """Класс объекта - яблоко."""

    def __init__(self, body_color=APPLE_COLOR, occupied_cells=frozenset()):
        """Задает цвет яблока и случайную начальную позицию."""
        super().__init__(body_color)
        self.randomize_position(occupied_cells)

    def draw(self):
        """Отрисовывает яблоко размеров в одну клетку."""
        self._draw_cell()


class Lemon(GameObject):
    """Класс объекта - лимон."""

    def __init__(self, body_color=LEMON_COLOR, occupied_cells=frozenset()):
        """Задает цвет лимона и случайную начальную позицию."""
        super().__init__(body_color)
        self.randomize_position(occupied_cells)

    def draw(self):
        """Отрисовывает лимон размеров в одну клетку."""
        self._draw_cell()


class Stone(GameObject):
    """Класс объекта - камень."""

    def __init__(self, body_color=STONE_COLOR, occupied_cells=frozenset()):
        """Задает цвет камня и случайную начальную позицию."""
        super().__init__(body_color)
        self.randomize_position(occupied_cells)

    def place_free(self, occupied_cells):
        """Ставит камень в свободную клетку поля."""
        self.randomize_position(occupied_cells)

    def draw(self):
        """Отрисовывает камень размеров в одну клетку."""
        self._draw_cell()


class Snake(GameObject):
    """Класс змейки."""

    def __init__(self, body_color=SNAKE_COLOR):
        """Инициализирует начальное состояние змейки."""
        super().__init__(body_color)
        self.reset(direction=RIGHT)

    def get_head_position(self):
        """Возвращает координаты головы змейки."""
        return self.positions[0]

    def update_direction(self, next_direction):
        """Применяет выбранное пользователем направление движения."""
        if next_direction:
            self.direction = next_direction

    def move(self):
        """Задает движение змейке."""
        head_x, head_y = self.get_head_position()
        direction_x, direction_y = self.direction

        # Шаг на одну клетку с телепортом через границы поля.
        new_head = (
            (head_x + direction_x * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + direction_y * GRID_SIZE) % SCREEN_HEIGHT,
        )

        # Запоминаем, столкнулась ли новая голова с телом до удаления хвоста.
        self.self_collision = new_head in self.positions[1:]

        self.positions.insert(0, new_head)
        self.last = []

        if len(self.positions) > self.length:
            self.last.append(self.positions.pop())

    def shrink(self):
        """Уменьшает змейку."""
        if self.length > 1:
            self.length -= 1
            self.last.append(self.positions.pop())

    def reset(self, direction=None):
        """Сбрасывает змейку в начальное состояние."""
        self.length = 1
        self.positions = [
            (
                (GRID_WIDTH // 2) * GRID_SIZE,
                (GRID_HEIGHT // 2) * GRID_SIZE,
            )
        ]
        self.direction = direction or choice([UP, DOWN, LEFT, RIGHT])
        self.last = []

    def draw(self):
        """Отрисовывает змейку и затирает след последнего сегмента."""
        # Затираем все клетки, удалённые за кадр
        for cell in self.last:
            self._draw_cell(cell, BOARD_BACKGROUND_COLOR, border=False)

        # Рисуем тело и голову
        for position in self.positions[1:]:
            self._draw_cell(position)

        self._draw_cell(self.get_head_position())


def handle_keys(current_direction):
    """Обрабатывает нажатия клавиш для смены направления змейки."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit('Игра завершена.')
        if event.type == pg.KEYDOWN:
            return KEY_DIRECTIONS.get(
                (event.key, current_direction), current_direction
            )
    return None


def eat_apple(apple, snake, lemon, stones, speed):
    """Обрабатывает поедание яблока, возвращает новую скорость."""
    snake.length += 1
    speed = min(speed + 1, MAX_SPEED)

    # Собираем занятые клетки, исключая само яблоко.
    apple.randomize_position(
        get_occupied_cells(snake, apple, lemon, stones, exclude=apple)
    )

    # Переставляем камни.
    for stone in stones:
        stone.place_free(
            get_occupied_cells(snake, apple, lemon, stones, exclude=stone)
        )

    return speed


def eat_lemon(lemon, snake, apple, stones, speed):
    """Обрабатывает поедание лимона, возвращает новую скорость."""
    if snake.length > 1:
        snake.shrink()
        speed = max(speed - 1, MIN_SPEED)

    # Собираем занятые клетки, исключая само яблоко.
    lemon.randomize_position(
        get_occupied_cells(snake, apple, lemon, stones, exclude=lemon)
    )

    # Переставляем камни.
    for stone in stones:
        stone.place_free(
            get_occupied_cells(snake, apple, lemon, stones, exclude=stone)
        )

    return speed


def reset_game(snake, apple, lemon, stones, initial_speed):
    """Сбрасывает игру."""
    snake.reset()
    apple.randomize_position(
        get_occupied_cells(snake, apple, lemon, stones, exclude=apple)
    )
    lemon.randomize_position(
        get_occupied_cells(snake, apple, lemon, stones, exclude=lemon)
    )
    stones = create_stones(snake, apple, lemon)
    return stones, initial_speed


def get_occupied_cells(snake, apple, lemon, stones, exclude=None):
    """Возвращает множество занятых клеток на поле."""
    cells = set(snake.positions)
    for fruit in (apple, lemon):
        if fruit is not exclude:
            cells.add(fruit.position)
    for stone in stones:
        if stone is not exclude:
            cells.add(stone.position)
    return cells


def create_stones(
        snake,
        apple,
        lemon
):
    """Создаёт случайное количество камней в свободных клетках."""
    count = randint(MIN_STONES, MAX_STONES)
    stones = []

    center = (
        (GRID_WIDTH // 2) * GRID_SIZE,
        (GRID_HEIGHT // 2) * GRID_SIZE,
    )

    # Базовый набор занятых клеток: змейка, фрукты, центр.
    occupied = set(snake.positions)
    occupied.add(apple.position)
    occupied.add(lemon.position)
    occupied.add(center)  # чтобы камень не попал в центр

    for _ in range(count):
        stone = Stone()  # временная позиция
        stone.randomize_position(occupied_cells=occupied)
        occupied.add(stone.position)  # новый камень тоже занимает клетку
        stones.append(stone)

    return stones


def main():
    """Запускает основной игровой цикл."""
    # Инициализация pygame:
    pg.init()

    # Тут нужно создать экземпляры классов.
    snake = Snake()
    apple = Apple(occupied_cells=set(snake.positions))
    lemon = Lemon(occupied_cells=set(snake.positions) | {apple.position})
    stones = create_stones(snake, apple, lemon)

    speed = SPEED
    initial_speed = speed

    screen.fill(BOARD_BACKGROUND_COLOR)

    while True:
        clock.tick(speed)

        next_direction = handle_keys(snake.direction)
        snake.update_direction(next_direction)
        snake.move()

        head = snake.get_head_position()

        # Если столкнулись с камнем, сбрасываем игру.
        if any(
            head == stone.position for stone in stones
        ):
            stones, speed = reset_game(
                snake, apple, lemon, stones, initial_speed
            )

        # Если съедаем яблоко, увеличиваем змейку, и появляется новое яблоко.
        if head == apple.position:
            speed = eat_apple(apple, snake, lemon, stones, speed)

        # Если съедаем лимон, уменьшаем змейку, и появляется новый лимон.
        if head == lemon.position:
            speed = eat_lemon(lemon, snake, apple, stones, speed)

        # Если столкнулись с собственным телом, сбрасываем игру.
        if snake.self_collision:
            stones, speed = reset_game(
                snake, apple, lemon, stones, initial_speed
            )

        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        lemon.draw()
        for stone in stones:
            stone.draw()
        snake.draw()

        pg.display.update()


if __name__ == '__main__':
    main()
