import argparse
import datetime
import json
import sys
import random
from collections import namedtuple
from enum import Enum
from time import sleep, time


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


class Commands(Enum):
    KEY_UP = 1
    KEY_DOWN = 2
    KEY_LEFT = 3
    KEY_RIGHT = 4
    ROTATE_LEFT = 5
    ROTATE_RIGHT = 6
    REVERSE = 7


KEY_COMMANDS = {
    "W": Commands.KEY_UP,
    "S": Commands.KEY_DOWN,
    "D": Commands.KEY_RIGHT,
    "A": Commands.KEY_LEFT,
    "REVERSE": Commands.REVERSE,
    "LEFT": Commands.ROTATE_LEFT,
    "RIGHT": Commands.ROTATE_RIGHT,
}


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

    def __init__(self, height, width, robot, field=None, obstacles=None):
        self.robot = robot
        self.width = width
        self.height = height
        self.center = self.height // 2 * self.width + self.width // 2
        self.last_command = None
        self.error_message = ''
        self.commands = []

        self.obstacles_count = obstacles if obstacles else 10

        if field is None:
            self.field = ['-'] * self.height * self.width
            self.set_wall()
            self.set_obstacles()
        else:
            self.field = field

    def normalize_position(self, position: Point) -> int:
        return self.center + position.x - self.width * position.y

    def get_robot_body_idx(self) -> list:
        position = self.normalize_position(self.robot.get_position())
        row_up = position - self.width
        row_bottom = position + self.width
        robot_coord = [row_up - 1, row_up, row_up + 1,
                       position - 1, position, position + 1,
                       row_bottom - 1, row_bottom, row_bottom + 1]
        return robot_coord

    def get_rotate_direction(self, new_direction) -> RotateDirection:
        robot_direction = self.robot.get_direction()
        cross = ((robot_direction.x * new_direction.y
                 - robot_direction.y * new_direction.x)
                 if robot_direction != new_direction else None)
        return RotateDirection(cross)

    def get_area_indexes(self, center, size):
        centers = [center]
        for i in range(1, size // 2 + 1):
            centers.append(center - self.width * i)
            centers.append(center + self.width * i)

        area = []
        for i in centers:
            area.extend(list(range(i - size // 2, i + size // 2 + 1)))
        return area

    def set_wall(self):
        for idx, _ in enumerate(self.field):
            if (idx < self.width
                    or idx % self.width == 0
                    or (idx + 1) % self.width == 0
                    or idx > self.width * self.height - self.width):
                self.field[idx] = self.WALL_SIGN

    def set_obstacles(self):
        position = self.normalize_position(self.robot.get_position())
        safe_area = self.get_area_indexes(position, 9)

        count = self.obstacles_count
        while count > 0:
            position = random.randint(0, self.height * self.width - 1)
            if position not in safe_area:
                area = self.get_area_indexes(position, random.choice([1, 2, 3, 4]))
                for idx in area:
                    if (0 <= idx < self.width * self.height
                            and idx not in safe_area):
                        self.field[idx] = self.WALL_SIGN
                count -= 1

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
                item = colorize(fld, Colors.RED) if fld == self.WALL_SIGN else fld

            if (idx + 1) % self.width == 0:
                print(item)
            else:
                print(item, end=" ")

        # render info
        print(colorize(f'Robot direction: {self.robot.get_direction()}', Colors.GREEN))
        position = self.normalize_position(self.robot.get_position())
        position_coord = self.robot.get_position()
        print(colorize(f'Your command: {self.last_command or ""}', Colors.GREEN))
        print(colorize(f'Your step: {position}', Colors.GREEN))
        print(colorize(f'Your step coordinate: {position_coord}', Colors.GREEN))

        if self.error_message:
            print(colorize(f"Error Message: {self.error_message}", Colors.RED))
            self.error_message = ''
        else:
            print()

        print('W - move up, S - move down, D - move right, A - move left')
        print('REVERSE - rotate 180, LEFT - left rotate 90, RIGHT - right rotate 90')

    def can_move(self):
        one_step = Point(*map(sum, zip(self.robot.get_position(),
                                       self.robot.get_direction())))
        center = self.normalize_position(
            Point(*map(sum, zip(one_step, self.robot.get_direction()))))

        if self.robot.direction.x == 0:
            front_idx = [center - 1, center, center + 1]
        else:
            front_idx = [center - self.width, center, center + self.width]
        for idx in front_idx:
            if self.field[idx] != '-':
                return False
        return True

    def update(self, command: str):
        command = command.upper()
        cmd = KEY_COMMANDS.get(command)
        direction = self.robot.get_direction()

        if cmd == Commands.KEY_UP:
            direction = Point(0, 1)
        elif cmd == Commands.KEY_DOWN:
            direction = Point(0, -1)
        elif cmd == Commands.KEY_RIGHT:
            direction = Point(1, 0)
        elif cmd == Commands.KEY_LEFT:
            direction = Point(-1, 0)

        if cmd == Commands.REVERSE:
            self.robot.rotate(RotateDirection.BACKWARD)
        elif cmd == Commands.ROTATE_LEFT:
            self.robot.rotate(RotateDirection.LEFT)
        elif cmd == Commands.ROTATE_RIGHT:
            self.robot.rotate(RotateDirection.RIGHT)
        else:
            if cmd is not None:
                if direction != self.robot.get_direction():
                    self.robot.rotate(self.get_rotate_direction(direction))
                else:
                    if self.can_move():
                        self.robot.move()
                    else:
                        self.error_message = "Can't move in that direction"
            else:
                self.error_message = f"\"{command}\" not supported!"

        self.commands.append(command)
        self.last_command = self.commands[-1]
        self.render()


def run_game(height, width):
    robot = Robot()
    game = Game(height, width, robot, obstacles=0)
    game.render()
    try:
        while True:
            command = input('Ваш ход: ')
            game.update(command)
    except KeyboardInterrupt:
        save_game(game)
        sys.exit(0)


def run_replay(replay):
    robot = Robot()
    game = Game(replay['height'], replay['width'], robot, replay['field'])
    game.render()
    try:
        for command in replay['commands']:
            game.update(command)
            sleep(1)
    except KeyboardInterrupt:
        sys.exit(0)


def save_game(game: Game):
    data = {
        "field": game.field,
        "height": game.height,
        "width": game.width,
        "commands": game.commands
    }
    date = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    with open(f"replay_{date}.json", "w") as output:
        json.dump(data, output)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--width", type=int, default=30,
                        help="width of game field")
    parser.add_argument("--height", type=int, default=20,
                        help="height of game field")
    parser.add_argument("--obstacles", type=int, default=10,
                        help="number of obstacles on the field")
    parser.add_argument("--replay", type=argparse.FileType('r'),
                        help="number of obstacles on the field")

    args = parser.parse_args()

    if args.replay is None:
        run_game(args.height, args.width)
    else:
        replay = json.load(args.replay)
        run_replay(replay)
