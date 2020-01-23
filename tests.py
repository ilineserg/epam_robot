import unittest
from robot import *


class TestRobot(unittest.TestCase):

    def test_robot_getters(self):
        robot = Robot()

        self.assertEqual(robot.get_position(), Point(0, 0))

        self.assertEqual(robot.get_direction(), Point(0, 1))

        self.assertEqual(robot.get_body(), robot.rotated_up)
        robot.direction = Point(0, -1)
        self.assertEqual(robot.get_body(), robot.rotated_down)
        robot.direction = Point(-1, 0)
        self.assertEqual(robot.get_body(), robot.rotated_left)
        robot.direction = Point(1, 0)
        self.assertEqual(robot.get_body(), robot.rotated_right)

    def test_robot_actions(self):
        robot = Robot()

        self.assertEqual(robot.position, Point(x=0, y=0))
        self.assertEqual(robot.direction, Point(x=0, y=1))
        robot.move()
        self.assertEqual(robot.position, Point(x=0, y=1))
        self.assertEqual(robot.direction, Point(x=0, y=1))
        robot.rotate(RotateDirection.LEFT)
        self.assertEqual(robot.position, Point(x=0, y=1))
        self.assertEqual(robot.direction, Point(x=-1, y=0))
        robot.move()
        self.assertEqual(robot.position, Point(x=-1, y=1))
        self.assertEqual(robot.direction, Point(x=-1, y=0))
        robot.rotate(RotateDirection.RIGHT)
        self.assertEqual(robot.position, Point(x=-1, y=1))
        self.assertEqual(robot.direction, Point(x=0, y=1))
        robot.move()
        self.assertEqual(robot.position, Point(x=-1, y=2))
        self.assertEqual(robot.direction, Point(x=0, y=1))
        robot.rotate(RotateDirection.BACKWARD)
        self.assertEqual(robot.position, Point(x=-1, y=2))
        self.assertEqual(robot.direction, Point(x=0, y=-1))
        robot.move()
        self.assertEqual(robot.position, Point(x=-1, y=1))
        self.assertEqual(robot.direction, Point(x=0, y=-1))


class TestGame(unittest.TestCase):

    def test_normalize_position(self):
        robot = Robot()
        game = Game(30, 30, robot, obstacles=0)

        self.assertEqual(game.normalize_position(Point(x=0, y=0)), 465)
        self.assertEqual(game.normalize_position(Point(x=0, y=13)), 75)
        self.assertEqual(game.normalize_position(Point(x=7, y=13)), 82)
        self.assertEqual(game.normalize_position(Point(x=3, y=6)), 288)
        self.assertEqual(game.normalize_position(Point(x=-6, y=-3)), 549)

    def test_get_robot_body_idx(self):
        robot = Robot()
        game = Game(30, 30, robot, obstacles=0)

        self.assertEqual(game.get_robot_body_idx(),
                         [434, 435, 436, 464, 465, 466, 494, 495, 496])
        game.robot.position = Point(x=7, y=13)
        self.assertEqual(game.get_robot_body_idx(),
                         [51, 52, 53, 81, 82, 83, 111, 112, 113])

    def test_get_area_indexes(self):
        robot = Robot()
        game = Game(30, 30, robot, obstacles=0)
        position_1 = game.normalize_position(Point(x=0, y=0))
        position_2 = game.normalize_position(Point(x=7, y=13))
        position_3 = game.normalize_position(Point(x=-1, y=-5))
        area_1 = [464, 465, 466, 434, 435, 436, 494, 495, 496]
        area_2 = [80, 81, 82, 83, 84, 50, 51, 52, 53, 54, 110, 111, 112, 113,
                  114, 20, 21, 22, 23, 24, 140, 141, 142, 143, 144]
        area_3 = [613, 614, 615, 583, 584, 585, 643, 644, 645]
        self.assertEqual(game.get_area_indexes(position_1, 3), area_1)
        self.assertEqual(game.get_area_indexes(position_2, 4), area_2)
        self.assertEqual(game.get_area_indexes(position_3, 2), area_3)

    def test_can_move(self):
        robot = Robot()
        game = Game(30, 30, robot, obstacles=0)
        game.robot.position = Point(x=0, y=13)
        game.robot.direction = Point(x=0, y=1)

        self.assertEqual(game.can_move(), False)

        game.robot.direction = Point(x=0, y=-1)
        self.assertEqual(game.can_move(), True)

        game.robot.direction = Point(x=1, y=0)
        self.assertEqual(game.can_move(), True)

        game.robot.direction = Point(x=-1, y=0)
        self.assertEqual(game.can_move(), True)


if __name__ == '__main__':
    unittest.main()