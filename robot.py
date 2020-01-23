from collections import namedtuple
from enum import Enum


class Colors(Enum):
    RED = '\x1b[91m'
    GREEN = '\x1b[32m'
    END = '\x1b[0m'


def colorize(text: str, color: Colors) -> str:
    return f"{color.value}{text}{Colors.END.value}"


Point = namedtuple("Point", ["x", "y"])


class RotateDirection(Enum):
    FORWARD = None
    BACKWARD = 0
    LEFT = 1
    RIGHT = -1


class Robot:

    def __init__(self):
        self.position = Point(0, 0)
        self.direction = Point(0, 1)
        self.color = Colors.GREEN

        self.body = u'\u2554\u2551\u2557\u2551\u2550\u2551\u255a\u2550\u255d'
        self.rotated_up = u'\u2554\u2551\u2557\u2551\u2550\u2551\u255a\u2550\u255d'
        self.rotated_down = u'\u2554\u2550\u2557\u2551\u2550\u2551\u255a\u2551\u255d'
        self.rotated_left = u'\u2554\u2550\u2557\u2550\u2551\u2551\u255a\u2550\u255d'
        self.rotated_right = u'\u2554\u2550\u2557\u2551\u2551\u2550\u255a\u2550\u255d'

    def get_position(self) -> Point:
        return self.position

    def get_direction(self) -> Point:
        return self.direction

    def get_body(self):
        if self.direction == (0, 1):
            return self.rotated_up
        elif self.direction == (0, -1):
            return self.rotated_down
        elif self.direction == (-1, 0):
            return self.rotated_left
        elif self.direction == (1, 0):
            return self.rotated_right

    def move(self):
        self.position = Point(*map(sum, zip(self.position, self.direction)))

    def rotate(self, side: RotateDirection):
        if side == RotateDirection.LEFT:
            self.direction = Point(-self.direction.y, self.direction.x)
        elif side == RotateDirection.RIGHT:
            self.direction = Point(self.direction.y, -self.direction.x)
        elif side == RotateDirection.BACKWARD:
            self.direction = Point(-self.direction.x, -self.direction.y)


class Game:

    WALL_SIGN = '#'
    FREE_SIGN = '-'

    is_live = False

    def __init__(self, height, width, robot):
        self.robot = robot
        self.width = width
        self.height = height

        self.commands = []
        self.field = ['-'] * self.height * self.width
        self.center = self.height // 2 * self.width + self.width // 2
        self.last_command = None
        self.set_wall()

    def normalize_position(self, position: Point) -> int:
        return self.center + position.x - self.width * position.y

    def get_robot_body_idx(self) -> list:
        normalized_position = self.normalize_position(self.robot.get_position())
        row_up = normalized_position - self.width
        row_bottom = normalized_position + self.width
        robot_coord = [row_up - 1, row_up, row_up + 1,
                       normalized_position - 1, normalized_position, normalized_position + 1,
                       row_bottom - 1, row_bottom, row_bottom + 1]
        return robot_coord

    def get_rotate_direction(self, new_direction) -> RotateDirection:
        robot_direction = self.robot.get_direction()
        cross = ((robot_direction.x * new_direction.y
                 - robot_direction.y * new_direction.x)
                 if robot_direction != new_direction else None)
        return RotateDirection(cross)

    def set_wall(self):
        for idx, _ in enumerate(self.field):
            if (idx < self.width
                    or idx % self.width == 0
                    or (idx + 1) % self.width == 0
                    or idx > self.width * self.height - self.width):
                self.field[idx] = colorize(self.WALL_SIGN, Colors.RED)

    def render(self):
        # clear screen
        print(chr(27) + "[2J")

        # render field end robot
        robot_indexes = self.get_robot_body_idx()
        robot_body = self.robot.get_body()
        robot_render_idx = 0

        for idx, fld in enumerate(self.field):
            if idx in robot_indexes:
                item = colorize(robot_body[robot_render_idx], self.robot.color)
                robot_render_idx += 1
            else:
                item = fld

            if (idx + 1) % self.width == 0:
                print(item)
            else:
                print(item, end=" ")

        # render info
        print(f'Робот повернут: {self.robot.get_direction()}')
        position = self.normalize_position(self.robot.get_position())
        print(f'Вы сходили: {self.last_command or ""}, {position}')

        if self.is_live:
            print('\u2191 - move up, \u2193 - move down, \u2192 - move right, \u2190 - move left')
        else:
            print('W - move up, S - move down, D - move right, A - move left')
            print('REVERSE - rotate 180, LEFT - left rotate 90, RIGHT - right rotate 90')

    def can_move(self):
        front_center = self.normalize_position(Point(*map(sum, zip(self.robot.position, self.robot.direction))))
        if self.robot.direction.x != 0:
            front_idx = [front_center - 1,
                         front_center,
                         front_center + 1]
        else:
            front_idx = [front_center - self.width,
                         front_center,
                         front_center + self.width]
        for idx in front_idx:
            if self.field[idx] != '-':
                return False
        return True

    def update(self, command: str):
        command = command.upper()
        direction = self.robot.get_direction()
        if command == "W":
            direction = Point(0, 1)
        elif command == "S":
            direction = Point(0, -1)
        elif command == "D":
            direction = Point(1, 0)
        elif command == "A":
            direction = Point(-1, 0)

        if command == "REVERSE":
            self.robot.rotate(RotateDirection.BACKWARD)
        elif command == "LEFT":
            self.robot.rotate(RotateDirection.LEFT)
        elif command == "RIGHT":
            self.robot.rotate(RotateDirection.RIGHT)
        elif command == "LIVE":
            self.is_live = True
        elif command == "ESC":
            self.is_live = False
        else:
            if direction != self.robot.get_direction():
                self.robot.rotate(self.get_rotate_direction(direction))
            else:
                if self.can_move():
                    self.robot.move()

        self.commands.append(command)
        self.last_command = self.commands[-1]
        self.render()


def run_game():
    robot = Robot()
    game = Game(20, 30, robot)
    game.render()
    while True:
        if not game.is_live:
            command = input('Ваш ход: ')
            game.update(command)


if __name__ == '__main__':
    run_game()