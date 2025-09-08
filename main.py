from turtle import Screen
from paddle import Paddle
from ball import Ball
from scoreboard import Scoreboard
import time

screen = Screen()

SCREEN_WIDTH = screen.window_width()
SCREEN_HEIGHT = screen.window_height()

screen.bgcolor("black")
screen.setup(width=800, height=600)
screen.title("Pong")
screen.tracer(0)

r_paddle = Paddle((350, 0))
l_paddle = Paddle((-350, 0))
ball = Ball()
scoreboard = Scoreboard()

screen.listen()
screen.onkey(r_paddle.go_up, "Up")
screen.onkey(r_paddle.go_down, key="Down")
screen.onkey(l_paddle.go_up, key="w")
screen.onkey(l_paddle.go_down, key="s")

game_is_on = True
while game_is_on:
    time.sleep(ball.move_speed)
    screen.update()
    ball.move()

    # Detect collision
    if ball.ycor() > SCREEN_HEIGHT/2 - 20 or ball.ycor() < -SCREEN_HEIGHT/2 + 20:
        ball.bounce_y()

    # Detect collision with r_paddle:
    if (ball.distance(r_paddle) < 50 and (ball.xcor() > r_paddle.xcor() - 10)) or (ball.distance(l_paddle) < 50 and (ball.xcor() < l_paddle.xcor() + 10)):
        ball.bounce_x()

    if ball.xcor() > SCREEN_WIDTH/2 - 10:
        ball.speed_up()
        ball.reset()
        scoreboard.increase_score(1)

    if ball.xcor() < -SCREEN_WIDTH/2 + 10:
        ball.speed_up()
        ball.reset()
        scoreboard.increase_score(2)


screen.exitonclick()
