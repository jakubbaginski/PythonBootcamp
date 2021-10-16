# import logging
import secrets
import turtle

import numba
from matplotlib.path import Path
from numpy import array


class CarManager:

    STARTING_MOVE_DISTANCE = 5
    MOVE_INCREMENT = 10
    NUMBER_OF_CARS = 20

    class Car(turtle.Turtle):

        COLORS = ["red", "orange", "yellow", "green", "blue", "purple"]
        MARGIN = 50
        SQUARE_HEIGHT = 20
        SQUARE_WIDTH = 20
        CAR_SHAPE = "square"

        def __init__(self):
            super().__init__()
            self.shape(self.CAR_SHAPE)
            self.penup()
            self.shapesize(stretch_wid=1, stretch_len=2, outline=0)
            self.color(self.select_color())
            self.setheading(180)
            self.goto(self.generate_position())
            self.showturtle()

        def generate_position(self) -> (float, float):
            new_x = self.getscreen().window_width()/2
            new_y = secrets.choice(range(int(-self.getscreen().window_height()/2 + self.MARGIN),
                                   int(self.getscreen().window_height()/2 - self.MARGIN)-1))
            return turtle.Vec2D(float(new_x), float(new_y))

        def select_color(self):
            return secrets.choice(self.COLORS)

        @numba.jit(forceobj=True)
        def get_get_shape_polygon(self) -> Path:
            xcor = self.xcor()
            ycor = self.ycor()
            sqw2 = self.SQUARE_WIDTH/2
            sqh2 = self.SQUARE_HEIGHT/2
            polygon = array([(xcor-sqw2, ycor+sqh2),
                             (xcor-sqw2, ycor-sqh2),
                             (xcor+sqw2, ycor-sqh2),
                             (xcor+sqw2, ycor+sqh2),
                             (xcor-sqw2, ycor+sqh2)])
            return Path(vertices=polygon, codes=None, closed=True)

    def __init__(self, screen: turtle.TurtleScreen):
        self.screen = screen
        self.cars: [CarManager.Car] = []
        self.move_increment = CarManager.STARTING_MOVE_DISTANCE

    def move_cars(self):
        car: CarManager.Car
        for car in self.cars:
            new_x = car.xcor()-self.move_increment
            if new_x <= - self.screen.window_width()/2:
                car.goto(car.generate_position())
            else:
                car.goto(new_x, car.ycor())

    def generate_car(self):
        if len(self.cars) < self.NUMBER_OF_CARS:
            self.cars.append(CarManager.Car())
