from turtle import Turtle

FONT = ("Courier", 40, "bold")

class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.player1_score = 0
        self.player2_score = 0
        self.color("white")
        self.hideturtle()
        self.penup()
        self.goto(0, 200)
        self.write_score()

    def write_score(self):
        self.clear()
        self.write(f"{self.player1_score}\t\t{self.player2_score}", align = "center", font = FONT)


    def increase_score(self, player):
        if player == 1:
            self.player1_score += 1
        else:
            self.player2_score += 1
        self.write_score()