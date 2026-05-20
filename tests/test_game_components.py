import sys
import types
import unittest
from unittest.mock import patch

try:
    import turtle as _turtle  # noqa: F401
except ModuleNotFoundError:
    fake_turtle_module = types.ModuleType("turtle")

    class Turtle:
        def __init__(self, *args, **kwargs):
            pass

        def shape(self, *args, **kwargs):
            pass

        def color(self, *args, **kwargs):
            pass

        def penup(self, *args, **kwargs):
            pass

        def shapesize(self, *args, **kwargs):
            pass

        def hideturtle(self, *args, **kwargs):
            pass

        def goto(self, *args, **kwargs):
            pass

        def xcor(self):
            return 0

        def ycor(self):
            return 0

        def clear(self):
            pass

        def write(self, *args, **kwargs):
            pass

    fake_turtle_module.Turtle = Turtle
    sys.modules["turtle"] = fake_turtle_module

from ball import Ball
from paddle import Paddle
from scoreboard import FONT, Scoreboard


def _fake_turtle_init(self, *args, **kwargs):
    self._x = 0
    self._y = 0
    self._clear_calls = 0
    self._last_write = None


def _fake_goto(self, x, y=None):
    if y is None:
        x, y = x
    self._x = x
    self._y = y


def _fake_xcor(self):
    return self._x


def _fake_ycor(self):
    return self._y


def _fake_clear(self):
    self._clear_calls += 1


def _fake_write(self, text, align=None, font=None):
    self._last_write = {"text": text, "align": align, "font": font}


class TurtlePatchedTestCase(unittest.TestCase):
    def setUp(self):
        self.patches = [
            patch("turtle.Turtle.__init__", _fake_turtle_init),
            patch("turtle.Turtle.shape", lambda *args, **kwargs: None),
            patch("turtle.Turtle.color", lambda *args, **kwargs: None),
            patch("turtle.Turtle.penup", lambda *args, **kwargs: None),
            patch("turtle.Turtle.shapesize", lambda *args, **kwargs: None),
            patch("turtle.Turtle.hideturtle", lambda *args, **kwargs: None),
            patch("turtle.Turtle.goto", _fake_goto),
            patch("turtle.Turtle.xcor", _fake_xcor),
            patch("turtle.Turtle.ycor", _fake_ycor),
            patch("turtle.Turtle.clear", _fake_clear),
            patch("turtle.Turtle.write", _fake_write),
        ]
        for active_patch in self.patches:
            active_patch.start()

    def tearDown(self):
        for active_patch in reversed(self.patches):
            active_patch.stop()


class BallTests(TurtlePatchedTestCase):
    def test_init_sets_default_motion_and_speed(self):
        ball = Ball()

        self.assertEqual(ball.x_move, 10)
        self.assertEqual(ball.y_move, 10)
        self.assertEqual(ball.move_speed, 0.1)

    def test_move_updates_position_by_motion_values(self):
        ball = Ball()
        ball.goto(15, -10)
        ball.x_move = 7
        ball.y_move = -3

        ball.move()

        self.assertEqual(ball.xcor(), 22)
        self.assertEqual(ball.ycor(), -13)

    def test_bounce_y_inverts_y_direction(self):
        ball = Ball()
        ball.y_move = 8

        ball.bounce_y()

        self.assertEqual(ball.y_move, -8)

    def test_bounce_x_inverts_x_direction_and_increases_speed(self):
        ball = Ball()
        ball.x_move = 10
        ball.move_speed = 0.2

        ball.bounce_x()

        self.assertEqual(ball.x_move, -10)
        self.assertAlmostEqual(ball.move_speed, 0.18)

    def test_speed_up_scales_both_motion_axes(self):
        ball = Ball()
        ball.x_move = 10
        ball.y_move = -5

        ball.speed_up()

        self.assertAlmostEqual(ball.x_move, 11)
        self.assertAlmostEqual(ball.y_move, -5.5)

    def test_reset_returns_to_center_and_resets_speed(self):
        ball = Ball()
        ball.goto(120, -40)
        ball.x_move = 10
        ball.move_speed = 0.04

        ball.reset()

        self.assertEqual((ball.xcor(), ball.ycor()), (0, 0))
        self.assertEqual(ball.x_move, -10)
        self.assertAlmostEqual(ball.move_speed, 0.09)


class PaddleTests(TurtlePatchedTestCase):
    def test_init_positions_paddle(self):
        paddle = Paddle((350, 0))

        self.assertEqual((paddle.xcor(), paddle.ycor()), (350, 0))

    def test_go_up_moves_paddle_up_by_twenty(self):
        paddle = Paddle((0, 0))

        paddle.go_up()

        self.assertEqual((paddle.xcor(), paddle.ycor()), (0, 20))

    def test_go_down_moves_paddle_down_by_twenty(self):
        paddle = Paddle((0, 0))

        paddle.go_down()

        self.assertEqual((paddle.xcor(), paddle.ycor()), (0, -20))


class ScoreboardTests(TurtlePatchedTestCase):
    def test_init_starts_scores_at_zero_and_writes_initial_text(self):
        scoreboard = Scoreboard()

        self.assertEqual(scoreboard.player1_score, 0)
        self.assertEqual(scoreboard.player2_score, 0)
        self.assertEqual((scoreboard.xcor(), scoreboard.ycor()), (0, 200))
        self.assertEqual(scoreboard._last_write["text"], "0\t\t0")
        self.assertEqual(scoreboard._last_write["align"], "center")
        self.assertEqual(scoreboard._last_write["font"], FONT)

    def test_increase_score_for_player_one_updates_display(self):
        scoreboard = Scoreboard()

        scoreboard.increase_score(1)

        self.assertEqual(scoreboard.player1_score, 1)
        self.assertEqual(scoreboard.player2_score, 0)
        self.assertEqual(scoreboard._last_write["text"], "1\t\t0")

    def test_increase_score_for_player_two_updates_display(self):
        scoreboard = Scoreboard()

        scoreboard.increase_score(2)

        self.assertEqual(scoreboard.player1_score, 0)
        self.assertEqual(scoreboard.player2_score, 1)
        self.assertEqual(scoreboard._last_write["text"], "0\t\t1")

    def test_write_score_clears_previous_text_before_writing(self):
        scoreboard = Scoreboard()
        initial_clear_calls = scoreboard._clear_calls

        scoreboard.write_score()

        self.assertEqual(scoreboard._clear_calls, initial_clear_calls + 1)


if __name__ == "__main__":
    unittest.main()
