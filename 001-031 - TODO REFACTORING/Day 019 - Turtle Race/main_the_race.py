import turtle as t
import random

# The Race challenge


class MyClass:
    COLORS = ('red', 'orange', 'yellow', 'green', 'blue', 'black', 'magenta', 'grey')
    NUM_OF_TURTLES = len(COLORS)
    SPEED_OF_RACE = 50
    SCREEN_WIDTH = 600
    SCREEN_HEIGHT = 300
    TURTLE_WIDTH = 40
    MARGIN = 20
    MAX_STEP = 15
    turtles = []
    screen = None
    winner = None
    START_POSITION = -SCREEN_WIDTH / 2 + MARGIN + TURTLE_WIDTH/2
    FINISH_POSITION = SCREEN_WIDTH / 2 - MARGIN * 2

    color_from_user = ""

    def __init__(self):
        self.screen = t.Screen()
        self.screen.setup(width=self.SCREEN_WIDTH + self.MARGIN * 2, height=self.SCREEN_HEIGHT + self.MARGIN * 2)
        self.draw_start_and_end()
        for i in range(self.NUM_OF_TURTLES):
            self.turtles.append(t.Turtle())
            self.turtles[i].hideturtle()
            self.turtles[i].penup()
            self.turtles[i].color(self.COLORS[i])
            self.turtles[i].shape("turtle")
            self.turtles[i].resizemode("user")
            self.turtles[i].shapesize(1, 1, 0)
            self.turtles[i].speed(0)
            self.turtles[i].setposition(-self.SCREEN_WIDTH / 2 + self.MARGIN,
                                        self.SCREEN_HEIGHT / 2 - (i + .5) * self.SCREEN_HEIGHT / self.NUM_OF_TURTLES)
            self.turtles[i].showturtle()

    def draw_start_and_end(self):
        draw = t.Turtle()
        draw.speed(0)
        draw.hideturtle()
        draw.pensize(3)
        draw.pencolor("DarkSeaGreen")
        for x in (self.START_POSITION, self.FINISH_POSITION):
            draw.penup()
            draw.setposition(x, self.SCREEN_HEIGHT / 2 - self.MARGIN)
            draw.setheading(270)
            draw.pendown()
            draw.forward(self.SCREEN_HEIGHT - 2 * self.MARGIN)

    def end_of_the_race(self):
        for turtle in self.turtles:
            if turtle.xcor() > self.FINISH_POSITION - self.TURTLE_WIDTH/2:
                if self.winner is None:
                    self.winner = turtle
                else:
                    # can't be two or more winners
                    # in case of the same end position the winner will be a turtle with the lowest index
                    # otherwise the winner will be a turtle which went the longest distance
                    if self.winner.xcor() < turtle.xcor():
                        self.winner = turtle
        return self.winner is not None

    def check_result(self):
        if self.turtles[self.COLORS.index(self.color_from_user)] == self.winner:
            return True
        return False

    def move_turtles(self):
        for turtle in self.turtles:
            turtle.forward(random.randint(-0, self.MAX_STEP))
        if not self.end_of_the_race():
            self.screen.ontimer(self.move_turtles, self.SPEED_OF_RACE)
        elif self.check_result():
            print("Congratulations!")
        else:
            print("Not this time, try again.")
            print(f"The winner is {self.winner.color()[1]} turtle.")

    def get_color_from_user(self):
        while self.color_from_user not in self.COLORS:
            print(f"Available options: {self.COLORS}")
            self.color_from_user = self.screen.textinput("Start of the race", "Which turtle will win the race?: ")

    def loop(self):
        self.get_color_from_user()
        self.screen.ontimer(self.move_turtles, self.SPEED_OF_RACE)
        self.screen.mainloop()


MyClass().loop()
