import turtle
import player


class Scoreboard:

    FONT = ("Courier", 24, "normal")

    def __init__(self):
        self.level = player.Player.LEVEL
        self.level_text = turtle.Turtle()
        self.level_text.hideturtle()
        self.level_text.penup()

    def print_level(self):
        self.level_text.setposition(-self.level_text.getscreen().window_width()/2+20,
                                    self.level_text.getscreen().window_height()/2-40)
        self.level_text.clear()
        self.level_text.write(f"Level {self.level}", align="left", font=self.FONT)

    def print_game_over(self, text="Game Over"):
        self.level_text.goto(0, 0)
        self.level_text.write(f"{text}", align="center", font=self.FONT)
