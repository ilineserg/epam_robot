class Robot:

    def __init__(self):
        self.position = [0, 0]
        self.body = [1, 1, 1, 1, 1, 1, 1, 1, 1]

    def get_position(self):
        return self.position

    def get_body(self):
        return self.body

    def move_up(self):
        self.position[1] += 1
        print(self.position)

    def move_down(self):
        self.position[1] -= 1
        print(self.position)

    def move_left(self):
        self.position[0] -= 1
        print(self.position)

    def move_right(self):
        self.position[0] += 1
        print(self.position)


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
        self.draw_wipe('+')

    def render(self):
        for i in range(0, self.height):
            raw = ' '.join([self.field[j] for j in range(i*self.width, i*self.width + self.width)])
            print(raw)

    def update(self, command):

        self.draw_wipe('-')
        self.move_robot_position(command)
        self.draw_wipe('+')
        print(f'Вы сходили: {command}, {type(command)}, {self.position}')
        self.render()

    def render_robot_body(self):
        row_up = self.position - self.width
        row_bottom = self.position + self.width
        robot_coord = [row_up - 1, row_up, row_up + 1,
                       self.position - 1, self.position, self.position + 1,
                       row_bottom - 1, row_bottom, row_bottom + 1]
        return robot_coord

    def draw_wipe(self, act):
        robot = self.render_robot_body()
        for c in robot:
            self.field[c] = act

    def move_robot_position(self, command):
        if command == 'w':
            self.robot.move_up()
        elif command == 's':
            self.robot.move_down()
        elif command == 'a':
            self.robot.move_left()
        elif command == 'd':
            self.robot.move_right()
        else:
            print('Неверная команда')

        self.set_position_robot()

    def set_position_robot(self):
        self.position = self.center + \
                        self.robot.position[0] - \
                        self.width * self.robot.position[1]


def run_game():
    print(' '.join([u'\u2554', u'\u2550', u'\u2557']))
    print(' '.join([u'\u2551', u'\u2551', u'\u2550']))
    print(' '.join([u'\u255a', u'\u2550', u'\u255d']))
    robot = Robot()
    game = Game(15, 15, robot)
    game.render()
    while True:
        print('w - up, s - down, d - right, a - left')
        command = input('Ваш ход: ')
        game.update(command)


if __name__ == '__main__':
    run_game()