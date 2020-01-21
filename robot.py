class Robot:

    def __init__(self):
        self.position = [0, 0]
        self.body = [u'\u2554', u'\u2551', u'\u2557',
                     u'\u2551', u'\u2550', u'\u2551',
                     u'\u255a', u'\u2550', u'\u255d']
        self.rotated_up = [u'\u2554', u'\u2551', u'\u2557',
                           u'\u2551', u'\u2550', u'\u2551',
                           u'\u255a', u'\u2550', u'\u255d']
        self.rotated_down = [u'\u2554', u'\u2550', u'\u2557',
                             u'\u2551', u'\u2550', u'\u2551',
                             u'\u255a', u'\u2551', u'\u255d']
        self.rotated_left = [u'\u2554', u'\u2550', u'\u2557',
                             u'\u2550', u'\u2551', u'\u2551',
                             u'\u255a', u'\u2550', u'\u255d']
        self.rotated_right = [u'\u2554', u'\u2550', u'\u2557',
                              u'\u2551', u'\u2551', u'\u2550',
                              u'\u255a', u'\u2550', u'\u255d']
        self.rotated = [0, 1]

    def get_position(self):
        return self.position

    def get_body(self):
        return self.body

    def move(self):
        self.position = list(map(lambda a, b: a + b, self.position, self.rotated))
        print(self.position)

    def rotate(self, side):
        if side == 'left':
            if self.rotated[0] == 0:
                self.rotated[0], self.rotated[1] = self.rotated[1] * -1, self.rotated[0]
            else:
                self.rotated[0], self.rotated[1] = self.rotated[1], self.rotated[0]
        elif side == 'right':
            if self.rotated[1] == 0:
                self.rotated[0], self.rotated[1] = self.rotated[1], self.rotated[0] * -1
            else:
                self.rotated[0], self.rotated[1] = self.rotated[1], self.rotated[0]
        elif side == 'back':
            self.rotated = list(map(lambda x: x * (- 1), self.rotated))


class Game:

    def __init__(self, height, width, robot, obstructions=0):
        self.robot = robot
        self.field = ['-'] * height * width
        self.width = width
        self.height = height
        self.center = self.height // 2 * self.width + self.width // 2
        self.position = self.center + \
                        self.robot.position[0] - \
                        self.width * self.robot.position[1]
        self.last_command = 'w'
        self.rotates_dict = {('w', 'd'): 'right',
                             ('d', 's'): 'right',
                             ('s', 'a'): 'right',
                             ('a', 'w'): 'right',
                             ('w', 'a'): 'left',
                             ('a', 's'): 'left',
                             ('s', 'd'): 'left',
                             ('d', 'w'): 'left',
                             ('w', 's'): 'back',
                             ('s', 'w'): 'back',
                             ('a', 'd'): 'back',
                             ('d', 'a'): 'back'}
        self.set_wall()
        self.draw()

    def set_wall(self):
        for wall in range(0, self.width):
            self.field[wall] = '#'
        for wall in range(-self.width, -1):
            self.field[wall] = '#'
        for wall in range(self.width, self.width * self.height, self.width):
            self.field[wall] = '#'
        for wall in range(self.width * 2 - 1, self.width * self.height,
                          self.width):
            self.field[wall] = '#'

    def render(self):
        for i in range(0, self.height):
            raw = ' '.join([self.field[j] for j in
                            range(i * self.width, i * self.width + self.width)])
            print(raw)

    def update(self, command):

        self.wipe()
        self.move_robot_position(command)
        self.draw()
        print(f'Робот повернут: {self.robot.rotated}')
        print(f'')
        print(f'Вы сходили: {command}, {type(command)}, {self.position}')
        self.render()

    def render_robot_body(self):
        row_up = self.position - self.width
        row_bottom = self.position + self.width
        robot_coord = [row_up - 1, row_up, row_up + 1,
                       self.position - 1, self.position, self.position + 1,
                       row_bottom - 1, row_bottom, row_bottom + 1]
        return robot_coord

    def wipe(self):
        robot_shadow = self.render_robot_body()
        for rs in robot_shadow:
            self.field[rs] = ' '

    def draw(self):
        iterator_body = []
        robot_shadow = self.render_robot_body()
        if self.robot.rotated == [0, 1]:
            iterator_body = iter(self.robot.rotated_up)
        elif self.robot.rotated == [0, -1]:
            iterator_body = iter(self.robot.rotated_down)
        elif self.robot.rotated == [-1, 0]:
            iterator_body = iter(self.robot.rotated_left)
        elif self.robot.rotated == [1, 0]:
            iterator_body = iter(self.robot.rotated_right)
        for r in robot_shadow:
            self.field[r] = iterator_body.__next__()

    def move_robot_position(self, command):
        if command == self.last_command:
            self.robot.move()
        elif (self.last_command, command) in self.rotates_dict:
            self.robot.rotate(self.rotates_dict.get((self.last_command, command)))
            self.last_command = command
        else:
            print('Неверная команда')

        self.set_position_robot()

    def set_position_robot(self):
        self.position = self.center + \
                        self.robot.position[0] - \
                        self.width * self.robot.position[1]


def run_game():
    print(chr(27) + "[2J")

    robot = Robot()
    game = Game(15, 15, robot)
    game.render()
    while True:
        print('\x1b[0;32;40m' + 'Поехали!' + '\x1b[0m')
        print('w - move up, s - move down, d - move right, a - move left')
        print('up - rotate up, '
              'down - rotate down, '
              'right - rotate right, '
              'left - rotate left')
        command = input('Ваш ход: ')
        game.update(command)


if __name__ == '__main__':
    run_game()
