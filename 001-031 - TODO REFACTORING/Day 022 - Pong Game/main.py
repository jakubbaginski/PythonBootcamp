import logging
import random
import turtle
from typing import Literal
from enum import Enum


class PlayerNames(Enum):
    RIGHT = "Right",
    LEFT = "Left"


UP: int = 90
DOWN: int = 270
RIGHT: int = 0
LEFT: int = 180
FULL_ANGLE = 360

Players = Literal[PlayerNames.RIGHT, PlayerNames.LEFT]
Result = Literal[PlayerNames.RIGHT, PlayerNames.LEFT, False]


class GameBoard:

    SCREEN_COLOR = "black"
    SCREEN_WIDTH = 0.7
    SCREEN_HEIGHT = 0.7
    GAME_TITLE = "Pong Game"

    HEADING_DOWN = DOWN
    DASH_LINE_STEP = 10
    DASH_LINE_SIZE = 3
    LINE_COLOR = "grey"

    NEW_BALL_DELAY = 3000
    CHECKS_TO_SKIP = 5

    class GamePaddle(turtle.Turtle):

        PADDLE_STEP = 80
        PADDLE_MARGIN = 50
        PADDLE_COLOR = "white"
        PADDLE_SHAPE = "circle"
        PADDLE_SHAPE_WIDTH = 5
        PADDLE_SHAPE_STRETCH = .4

        class Directions(Enum):
            UP = "Up",
            DOWN = "Down"

        KEYS: {Players: {Directions: str}} = {
            PlayerNames.RIGHT: {
                Directions.UP: "o",
                Directions.DOWN: "l"
            },
            PlayerNames.LEFT: {
                Directions.UP: "s",
                Directions.DOWN: "z"
            }
        }

        def __init__(self, player: Players):
            super().__init__(visible=True, shape=self.PADDLE_SHAPE)
            self.penup()
            self.color(self.PADDLE_COLOR)
            self.shapesize(stretch_wid=self.PADDLE_SHAPE_WIDTH, stretch_len=self.PADDLE_SHAPE_STRETCH)
            self.player: Players = player

            x_position = self.getscreen().window_width()/2 - GameBoard.GamePaddle.PADDLE_MARGIN
            if self.player in list(GameBoard.GamePaddle.KEYS.keys()):
                self.setx(x_position if self.player == PlayerNames.RIGHT else -x_position)
                self.getscreen().onkeypress(self.move_up,
                                            GameBoard.GamePaddle.KEYS[self.player][self.Directions.UP])
                self.getscreen().onkeypress(self.move_down,
                                            GameBoard.GamePaddle.KEYS[self.player][self.Directions.DOWN])
            else:
                pass
                # logging.error("Wrong paddle position")

        def move_up(self):
            if self.ycor() < self.getscreen().window_height()/2 - GameBoard.GamePaddle.PADDLE_STEP:
                self.sety(self.ycor() + GameBoard.GamePaddle.PADDLE_STEP)
                self.getscreen().update()

        def move_down(self):
            if self.ycor() > -self.getscreen().window_height()/2 + GameBoard.GamePaddle.PADDLE_STEP:
                self.sety(self.ycor() - GameBoard.GamePaddle.PADDLE_STEP)
                self.getscreen().update()

    class Ball(turtle.Turtle):

        BALL_SEED = 60
        BALL_SPEED_MAX = 10
        BALL_STEP = 10
        BALL_SHAPE = "circle"
        BALL_COLOR = "white"
        BALL_SIZE = 20

        # angles from 90 +/- BALL_EXC_ANGLE and 270 +/- BALL_EXC_ANGLE will be corrected to prevent "slow" game
        BALL_EXC_ANGLE = 10

        def __init__(self):
            super().__init__(shape=self.BALL_SHAPE)
            self.color(self.BALL_COLOR)
            self.penup()
            self.ball_step = self.BALL_STEP
            self.ball_speed = self.BALL_SEED
            self.getscreen().onkeypress(self.inc_speed, "plus")
            self.getscreen().onkeypress(self.dec_speed, "minus")
            self.start_position()

        def start_position(self):
            self.goto(0, 0)
            self.setheading(random.randint(RIGHT, FULL_ANGLE))
            self.showturtle()

        def inc_step(self):
            if self.ball_step <= self.BALL_STEP * 2:
                pass
                # self.ball_step += 1
                # logging.warning(f"Ball step changed to {self.ball_step}")

        def inc_speed(self):
            if self.ball_speed >= self.BALL_SPEED_MAX:
                self.ball_speed *= 0.9
                logging.warning(f"Ball speed changed to {self.ball_speed}")

        def dec_step(self):
            if self.ball_step > 0:
                pass
                # self.ball_step -= 1
                # logging.warning(f"Ball step changed to {self.ball_step}")

        def dec_speed(self):
            if self.ball_speed <= self.BALL_SEED:
                self.ball_speed *= 1.1
                logging.warning(f"Ball speed changed to {self.ball_speed}")

        def setheading(self, to_angle: float) -> None:
            """
            Implemented in order to prevent angles close to UP or DOWN directions
            :param to_angle:
            :return:
            """
            correction = 0
            if UP - self.BALL_EXC_ANGLE < to_angle <= UP + self.BALL_EXC_ANGLE or \
                    DOWN - self.BALL_EXC_ANGLE < to_angle <= DOWN + self.BALL_EXC_ANGLE:
                correction = random.randint(self.BALL_EXC_ANGLE, 2 * self.BALL_EXC_ANGLE)
                if RIGHT < to_angle < UP or LEFT < to_angle < DOWN:
                    correction = -correction
                # logging.warning(f"Angle correction {correction}, {to_angle} -> {to_angle + correction}")
            super().setheading(to_angle + correction)

        def move(self):
            self.change_angle_if_collision_with_wall()
            self.forward(self.ball_step)
            if self.check_if_outside() is False:
                pass
            else:
                self.hideturtle()
            self.getscreen().update()

        def change_angle_if_collision_with_wall(self):
            max_y = (self.getscreen().window_height() - self.BALL_SIZE) / 2
            if self.ycor() >= max_y or self.ycor() <= - max_y:
                self.setheading(FULL_ANGLE - self.heading())

        def check_if_outside(self) -> Result:
            """
            Check if a ball is outside the screen
            :return: If ball is outside the screen returns name of player who should get a point otherwise False
            """
            max_x = (self.getscreen().window_width() - self.BALL_SIZE) / 2
            if self.xcor() >= max_x:
                return PlayerNames.LEFT
            elif self.xcor() <= -max_x:
                return PlayerNames.RIGHT
            else:
                return False

    class ScoreBoard(turtle.Turtle):

        IMAGE_WIDTH = 35
        Y_POSITION = 250
        X_START_POSITION = -4 * IMAGE_WIDTH

        def __init__(self):
            super().__init__()
            for i in range(0, 10):
                self.getscreen().register_shape(f"images/{i}.gif")
            self.score = 0
            self.hideturtle()
            self.penup()

        def print_result(self, point: [int, int], score: int):
            self.score = f"{score:03d}"
            for i in self.score:
                self.shape(f"images/{i}.gif")
                self.goto(point)
                self.stamp()
                point[0] += self.IMAGE_WIDTH

        def print_board(self, scores):
            self.print_result([self.X_START_POSITION, self.Y_POSITION], scores[PlayerNames.LEFT])
            self.print_result([self.IMAGE_WIDTH*2, self.Y_POSITION], scores[PlayerNames.RIGHT])

    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.screen: turtle.Screen = turtle.Screen()
        self.screen.tracer(False)
        self.screen.setup(width=GameBoard.SCREEN_WIDTH, height=GameBoard.SCREEN_HEIGHT)
        self.screen.bgcolor(GameBoard.SCREEN_COLOR)
        self.screen.title(GameBoard.GAME_TITLE)
        self.semaphore = True

        self.ball = GameBoard.Ball()
        self.new_ball()

        self.picture = turtle.Turtle()
        self.draw_screen_elements()

        self.game_paddle: {Players: GameBoard.GamePaddle} = {
            PlayerNames.LEFT: GameBoard.GamePaddle(PlayerNames.LEFT),
            PlayerNames.RIGHT: GameBoard.GamePaddle(PlayerNames.RIGHT)
        }
        self.score = {
            PlayerNames.RIGHT: 0,
            PlayerNames.LEFT: 0
        }
        self.skip_next_check = 0
        self.collision_of_game_paddle_and_ball()
        self.screen.listen()

        self.information = GameBoard.ScoreBoard()
        self.print_scores()

    def collision_of_game_paddle_and_ball(self):

        if self.semaphore is False:
            logging.error("Recursion detected: skipping one move.")
            return

        self.semaphore = False

        def check_if_in_the_same_q(angle, new_angle):
            return (RIGHT <= angle < UP and RIGHT <= new_angle < UP) or \
                   (UP <= angle < LEFT and UP <= new_angle < LEFT) or \
                   (LEFT <= angle < DOWN and LEFT <= new_angle < DOWN) or \
                   (DOWN <= angle < FULL_ANGLE and DOWN <= new_angle < FULL_ANGLE)

        self.ball.move()
        if self.skip_next_check > 0:
            self.skip_next_check -= 1
        else:
            for paddle in self.game_paddle:
                if (paddle == PlayerNames.RIGHT and
                    self.game_paddle[paddle].xcor() - max(self.ball.BALL_SIZE, self.ball.ball_step) <=
                    self.ball.xcor() <= self.game_paddle[paddle].xcor()) or \
                        (paddle == PlayerNames.LEFT and
                         self.game_paddle[paddle].xcor() <=
                         self.ball.xcor() <=
                         self.game_paddle[paddle].xcor() + max(self.ball.BALL_SIZE, self.ball.ball_step)):

                    logging.info(f"Distance to {paddle}: {self.ball.distance(self.game_paddle[paddle])}")
                    if self.ball.distance(self.game_paddle[paddle]) < \
                            GameBoard.GamePaddle.PADDLE_MARGIN + self.ball.BALL_SIZE / 2:
                        logging.info(f"Touched {self.game_paddle[paddle].player}")

                        # each time paddle touches the ball speed is increasing
                        # self.ball.ball_step += .5
                        if self.ball.ball_speed * .9 >= self.ball.BALL_SPEED_MAX:
                            self.ball.ball_speed *= .9
                            logging.info(f"Speed changed to {self.ball.ball_speed}")
                        heading = self.ball.heading()
                        rand_heading = random.randint(-self.ball.BALL_EXC_ANGLE*2, self.ball.BALL_EXC_ANGLE*2)
                        new_heading = (1.5 * FULL_ANGLE - heading) % FULL_ANGLE
                        # while not check_if_in_the_same_q(new_heading, new_heading + rand_heading):
                        # rand_heading = random.randint(-self.ball.BALL_EXC_ANGLE*2, self.ball.BALL_EXC_ANGLE*2)
                        if not check_if_in_the_same_q(new_heading, new_heading + rand_heading):
                            new_heading = 0

                        # logging.warning(f"Correcting angle {heading}: {new_heading} to {new_heading + rand_heading}")
                        new_heading += rand_heading
                        self.ball.setheading(new_heading)
                        self.skip_next_check = (GameBoard.GamePaddle.PADDLE_MARGIN * 2 + self.ball.BALL_SIZE) / \
                            self.ball.ball_step
                    else:
                        self.skip_next_check = 0

        self.screen.ontimer(self.collision_of_game_paddle_and_ball, int(self.ball.ball_speed))

        self.semaphore = True

    def draw_screen_elements(self):
        self.picture.color(self.LINE_COLOR)
        self.picture.pensize(GameBoard.DASH_LINE_SIZE)
        self.picture.penup()
        self.picture.goto(0, self.screen.window_height() / 2)
        self.picture.pendown()
        self.picture.setheading(GameBoard.HEADING_DOWN)
        for _ in range(0, self.screen.window_height(), GameBoard.DASH_LINE_STEP):
            self.picture.forward(GameBoard.DASH_LINE_STEP)
            if self.picture.isdown():
                self.picture.penup()
            else:
                self.picture.pendown()
        self.picture.penup()
        self.picture.goto(-100, 0)
        self.picture.pendown()
        self.picture.color(self.LINE_COLOR)
        self.picture.circle(radius=100, steps=100)
        self.picture.penup()
        self.picture.hideturtle()

    def new_ball(self):
        result: Result = self.ball.check_if_outside()
        if result is not False:
            self.score[result] += 1
            logging.info(f"{result}: {self.score[result]}")
            self.ball.start_position()
            self.print_scores()
        self.screen.ontimer(self.new_ball, GameBoard.NEW_BALL_DELAY)

    def print_scores(self):
        self.information.print_board(self.score)
        # self.screen.ontimer(self.print_scores, GameBoard.NEW_BALL_DELAY)

    def main_loop(self):
        self.screen.mainloop()


GameBoard().main_loop()
