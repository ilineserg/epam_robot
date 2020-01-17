

class Game:

    def __init__(self, height, width, obstructions=0):
        self.field = ['-'] * height * width
        self.width = width
        self.height = height
        self.position = self.height // 2 * self.width + self.width // 2
        self.field[self.position] = '+'

    def render(self):
        for i in range(0, self.height):
            raw = ''.join([self.field[j] for j in range(i*self.width, i*self.width + self.width)])
            print(raw)

    def update(self, command):
        self.field[command] = '+'
        self.field[self.position] = '-'
        self.position = command
        print(f'Вы сходили: {command}')
        self.render()


def run_game():
    game = Game(9, 9)
    game.render()
    while True:
        command = int(input('Ваш ход:'))
        game.update(command)


if __name__ == '__main__':
    run_game()