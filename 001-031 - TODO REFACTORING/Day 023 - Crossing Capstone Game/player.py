import turtle
from matplotlib.path import Path
from numpy import array
import numba


class Player(turtle.Turtle):
    STARTING_POSITION = (0, -280)
    MOVE_DISTANCE = 10
    FINISH_LINE_Y = 280
    DEFAULT_LEVEL = 1
    TURTLE_H_UP_PIXELS = 16
    TURTLE_H_DOWN_PIXELS = 9
    TURTLE_WIDTH_PIXELS = 20
    PLAYER_COLOR = "DarkBlue"

    def __init__(self):
        super().__init__(shape="turtle")
        self.penup()
        self.color(self.PLAYER_COLOR)
        self.goto(self.STARTING_POSITION)
        self.showturtle()
        self.setheading(90)
        self.level = self.DEFAULT_LEVEL
        self.getscreen().onkeypress(self.move, "Up")

    def move(self) -> bool:
        new_y = self.ycor() + self.MOVE_DISTANCE
        if new_y >= self.FINISH_LINE_Y:
            new_y = self.STARTING_POSITION[1]
            self.level += 1
        self.goto(self.xcor(), new_y)
        self.getscreen().update()
        return new_y > self.ycor()

    @numba.jit(forceobj=True)
    def get_shape_polygon(self) -> Path:
        xcor = self.xcor()
        ycor = self.ycor()
        twp2 = self.TURTLE_WIDTH_PIXELS/2
        polygon = array([
            (xcor-twp2, ycor+self.TURTLE_H_UP_PIXELS),
            (xcor-twp2, ycor-self.TURTLE_H_DOWN_PIXELS),
            (xcor+twp2, ycor-self.TURTLE_H_DOWN_PIXELS),
            (xcor+twp2, ycor+self.TURTLE_H_UP_PIXELS),
            (xcor-twp2, ycor+self.TURTLE_H_UP_PIXELS)])
        return Path(vertices=polygon, codes=None, closed=True)
