import random
import turtle as t
from typing import Literal, Union

AllowedColorModes = Literal["one", "multi"]


class GameBoard:
    TITLE: str = "The Snake Game"

    BOARD_COLOR: str = "black"
    BOARD_SIZE: int = 22  # to get in pixels multiply by size of "square" turtle

    FRAME_COLOR: str = "red"
    FRAME_SIZE: int = 6  # pixels

    SNAKE_INITIAL_LENGTH = 5
    SNAKE_COLOR = "white"

    FOOD_COLOR = "DarkSeaGreen"

    DRAWING_SEED: str = "fastest"
    DEFAULT_GAME_SPEED = 200
    MAX_GAME_SPEED = 4*DEFAULT_GAME_SPEED
    GAME_SPEED_STEP = 50
    GAME_LEVEL = 1
    MAX_GAME_LEVEL = 10*GAME_LEVEL

    UP = 90
    DOWN = 270
    RIGHT = 0
    LEFT = 180

    class MyTurtle(t.Turtle):

        def __init__(self, shape="square", visible=False, color="white"):
            super().__init__(shape=shape, visible=visible)
            self.shape_size: int = 0
            if shape == "square":
                self.shape_size = int(abs(self.get_shapepoly()[0][0]) + abs(self.get_shapepoly()[2][0]))
            self.color(color)
            self.penup()
            self.speed(GameBoard.DRAWING_SEED)
            self.max_x_y: int = round(GameBoard.BOARD_SIZE / 2)

        def xcor(self) -> int:
            return round(super().xcor())

        def ycor(self) -> int:
            return round(super().ycor())

        def position(self) -> (int, int):
            _position = super().position()
            return tuple([round(_position[0]), round(_position[1])])

        def make_stamp(self, shape=None) -> int:
            # change shape
            if shape is not None:
                self.shape(shape)
            return self.stamp()

    class ScoreBoard(MyTurtle):

        def __init__(self):
            super().__init__(color=GameBoard.FRAME_COLOR)
            self.highest_score = 0
            self.get_highest_score()

        def print_score(self, score: int, level: int, speed: int):
            self.clear()
            self.goto(0, self.max_x_y*(self.shape_size+1))
            self.write(f"Score: {score}, Highest score: {self.highest_score}, "
                       f"Level: {level}, Speed: {speed}", align="center",
                       font=('Arial', 15, 'normal'))

        def get_highest_score(self):
            with open("highest_score.txt") as file:
                self.highest_score = int(file.read())

        def save_highest_score(self):
            with open("highest_score.txt", "w") as file:
                file.write(str(self.highest_score))

    class Food(MyTurtle):

        def __init__(self):
            super().__init__(color=GameBoard.FOOD_COLOR)
            # if True new food should be generated
            self.eaten: bool = True
            self.shapesize(stretch_wid=0.5, stretch_len=0.5)

        def generate_new_food(self, snake=None):
            if self.eaten is True:
                find_correct_food_position = True
                # find new food position outside snake's body
                while find_correct_food_position is True:
                    x = random.SystemRandom().randint(-self.max_x_y + 1, self.max_x_y - 1) * self.shape_size
                    y = random.SystemRandom().randint(-self.max_x_y + 1, self.max_x_y - 1) * self.shape_size
                    if snake is None or \
                            (tuple([x, y]) not in snake.body["positions"] and tuple([x, y]) != snake.head):
                        find_correct_food_position = False
                        self.setposition(x, y)
                        self.make_stamp()
                        self.eaten = False

        def eat_food(self):
            if self.eaten is False:
                self.eaten = True
                self.clearstamps()
                return True
            return False

    class Frame(MyTurtle):

        def __init__(self):
            super().__init__()

        def paint(self):
            self.pencolor(GameBoard.FRAME_COLOR)
            self.pensize(GameBoard.FRAME_SIZE)

            value = round(self.max_x_y * self.shape_size)
            self.setposition(-value, value)
            self.pendown()
            for corner_of_board in ((value, value), (value, -value), (-value, -value), (-value, value)):
                self.goto(corner_of_board)
            self.penup()

    class Snake(MyTurtle):

        def __init__(self):
            super().__init__(color=GameBoard.SNAKE_COLOR)
            # head of the snake in the centre, tail on the left
            # as snake starts moving to the right
            self.level: int = GameBoard.GAME_LEVEL
            self.length: int = GameBoard.SNAKE_INITIAL_LENGTH
            self.color_mode: AllowedColorModes = "one"
            self.setx(-self.shape_size * GameBoard.SNAKE_INITIAL_LENGTH)
            self.head: (int, int) = self.position()
            self.body: {[int], [(int, int)]} = {"stamps": [], "positions": []}
            for _ in range(self.length - 1):
                self.forward()
            self.score: int = 0
            self.showturtle()

        def kill(self):
            self.head = ()
            self.body = {"stamps": [], "positions": []}

        def forward(self, distance: int = 1, food=None) -> bool:
            self.body["stamps"].append(int(self.make_stamp()))
            self.body["positions"].append(self.head)
            if self.color_mode == "multi":
                self.color((random.SystemRandom().randint(0, 255),
                            random.SystemRandom().randint(0, 255),
                            random.SystemRandom().randint(0, 255)))
            else:
                self.color(GameBoard.SNAKE_COLOR)
            super().forward(self.shape_size * distance)
            self.head = self.position()
            if len(self.body["stamps"]) > self.length - 1:
                self.clearstamp(self.body["stamps"].pop(0))
                self.body["positions"].pop(0)

            if food is not None and self.head == food.position() and food.eat_food():
                # logging.info(f"Food is found at position {self.head}")
                self.snake_gets_longer()

            return not (self.check_tail_collision() or self.check_frame_collision())

        def check_frame_collision(self):
            x = self.xcor()
            y = self.ycor()
            value = self.max_x_y * self.shape_size
            if x in (-value, value) or y in (-value, value):
                # logging.info(f"Frame Collision Detected! {(x, y)}, {value}")
                return True
            return False

        def check_tail_collision(self) -> bool:
            if (self.head in self.body["positions"]) is True:
                # logging.info(f"Tail Collision Detected! {self.head}")
                return True
            return False

        def snake_gets_longer(self) -> None:
            self.length += self.level
            self.score += 1

        def move_up(self) -> None:
            if self.heading() != GameBoard.DOWN:
                self.setheading(GameBoard.UP)

        def move_down(self) -> None:
            if self.heading() != GameBoard.UP:
                self.setheading(GameBoard.DOWN)

        def move_right(self) -> None:
            if self.heading() != GameBoard.LEFT:
                self.setheading(GameBoard.RIGHT)

        def move_left(self) -> None:
            if self.heading() != GameBoard.RIGHT:
                self.setheading(GameBoard.LEFT)

        def level_up(self) -> None:
            if self.level < GameBoard.MAX_GAME_LEVEL:
                self.level += 1
                # logging.info(f"Level up, Current level: {self.level}")

        def level_down(self) -> None:
            if self.level > GameBoard.GAME_LEVEL:
                self.level -= 1
                # logging.info(f"Level down, Current level: {self.level}")

        def change_color_mode(self):
            if self.color_mode == "one":
                self.color_mode = "multi"
            else:
                self.color_mode = "one"
            # logging.info(f"Change of color mode to {self.color_mode}")

    frame: Union[Frame, None] = None
    picture: Union[MyTurtle, None] = None
    food: Union[Food, None] = None
    snake: Union[Snake, None] = None

    def __init__(self):

        self.game_started: bool = False
        self.semaphore: bool = True
        self.game_speed = GameBoard.DEFAULT_GAME_SPEED

        self.screen = t.Screen()
        self.screen.title(GameBoard.TITLE)
        self.register_pictures()
        self.scoreboard = GameBoard.ScoreBoard()
        self.screen.setup(width=0.8, height=0.8)
        self.screen.bgcolor(self.BOARD_COLOR)
        self.screen.colormode(255)

        self.screen.listen()
        self.screen.tracer(0)
        self.welcome_screen()

    def register_pictures(self):
        self.screen.addshape("images/the_snake.gif")
        self.screen.addshape("images/game_over.gif")
        self.screen.addshape("images/press_space.gif")
        self.screen.addshape("images/score.gif")
        for i in range(0, 10):
            self.screen.addshape(f"images/{i}.gif")

    def welcome_screen(self):
        self.picture = GameBoard.MyTurtle(visible=False)
        self.picture.make_stamp(shape="images/the_snake.gif")
        self.picture.setposition(0, -160)
        self.picture.make_stamp(shape="images/press_space.gif")
        self.screen.onkeypress(self.start_game, "space")

    def game_over_screen(self):
        for turtle in self.screen.turtles():
            turtle.clearstamps()
            turtle.hideturtle()

        self.picture.setposition(0, 0)
        self.picture.make_stamp("images/game_over.gif")
        self.picture.setposition(self.picture.xcor() - 80, self.picture.ycor() - 80)
        self.picture.make_stamp("images/score.gif")
        self.picture.setposition(self.picture.xcor() + 100, self.picture.ycor())

        score = f"{self.snake.score:03d}"
        for digit in score:
            self.picture.setposition(self.picture.xcor() + 35, self.picture.ycor())
            self.picture.make_stamp(f"images/{digit}.gif")

        self.picture.setposition(0, self.picture.ycor() - 80)
        self.picture.make_stamp("images/press_space.gif")
        self.screen.onkeypress(self.start_game, "space")

    def init_snake(self):
        self.snake = GameBoard.Snake()
        self.screen.update()

    def init_and_paint_frame(self):
        self.frame = GameBoard.Frame()
        self.frame.paint()

    def init_food(self):
        self.food = GameBoard.Food()

    def start_game(self):
        if self.game_started is False:
            for turtle in self.screen.turtles():
                turtle.clearstamps()
                turtle.hideturtle()

            self.game_speed = GameBoard.DEFAULT_GAME_SPEED
            self.game_started = True
            self.init_and_paint_frame()
            self.init_snake()
            self.init_food()
            self.register_keys()
            self.semaphore = True

    def move_snake(self):
        if self.semaphore is True:  # to prevent recursion
            self.semaphore = False
            # False of self.snake.forward means collision with frame or snake's tail
            if not self.snake.forward(food=self.food):
                # logging.warning("Game Over")
                self.snake.kill()
                self.food.eaten = False
                self.game_started = False
                self.game_over_screen()
            # this has to be checked in order to not continue
            elif self.game_started is True:
                self.screen.ontimer(self.move_snake, self.game_speed)
                self.food.generate_new_food(self.snake)

            self.scoreboard.print_score(self.snake.score, self.snake.level, self.game_speed)
            self.screen.update()
            if self.snake.score > self.scoreboard.highest_score:
                self.scoreboard.highest_score = self.snake.score
                self.scoreboard.save_highest_score()
            self.semaphore = True

    def do_nothing(self):
        # an empty function used to provide no reaction to space key
        pass

    def register_keys(self) -> None:
        self.screen.onkeypress(self.do_nothing, "space")
        keys = {
            self.snake.move_up: ("Up", "W", "w"),
            self.snake.move_down: ("Down", "S", "s"),
            self.snake.move_right: ("Right", "D", "d"),
            self.snake.move_left: ("Left", "A", "a"),
            self.snake.level_down: {"bracket"+"left", "brace"+"left"},
            self.snake.level_up: {"bracket"+"right", "brace"+"right"},
            self.snake.change_color_mode: {'c', 'C'},
            self.game_speed_down: {"comma", "less"},
            self.game_speed_up: {"period", "greater"}
        }
        for function_ref in keys:
            for key in keys[function_ref]:
                self.screen.onkeypress(function_ref, key)
        self.screen.ontimer(self.move_snake, self.game_speed)

    def game_speed_up(self):
        if self.game_speed > GameBoard.GAME_SPEED_STEP:
            self.game_speed -= GameBoard.GAME_SPEED_STEP
            # logging.info(f"Speed up: {self.game_speed}")

    def game_speed_down(self):
        if self.game_speed < GameBoard.MAX_GAME_SPEED:
            self.game_speed += GameBoard.GAME_SPEED_STEP
            # logging.info(f"Speed down {self.game_speed}")

    def mainloop(self):
        # logging.basicConfig(level=logging.INFO)
        self.screen.mainloop()


GameBoard().mainloop()
