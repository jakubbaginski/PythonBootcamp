import turtle
import pandas


class GameBoard:

    FILE_50 = "./50_states.csv"
    FILE_TO_LEARN = "./states_to_learn.csv"
    FILE_MAP = "./blank_states_img.gif"

    def __init__(self):
        self.screen = turtle.Screen()
        self.screen.title("U.S. States Game")
        self.screen.register_shape(self.FILE_MAP)
        self.screen.setup(width=725, height=491)
        self.picture = turtle.Turtle(shape=self.FILE_MAP)
        self.picture.showturtle()
        # logging.basicConfig(level="INFO")
        try:
            self.states: pandas.DataFrame = pandas.read_csv(self.FILE_TO_LEARN)
            # logging.warning(f"If you want to play from the scratch - delete {self.FILE_TO_LEARN} " +
            #                 f"file before starting new game")
        except FileNotFoundError:
            self.states: pandas.DataFrame = pandas.read_csv(self.FILE_50)
            # logging.info(f"New Game started.")
        self.score = 0

    def game(self):
        game_on = True
        max_number = len(self.states)
        while game_on:
            name = self.screen.textinput(f"Score: {self.score}/{max_number}", "Provide another state name")
            if name is not None and name.title() != "Exit":
                name = name.title()
                state = self.states[self.states["state"] == name]
                if len(state) == 1:
                    new_text = turtle.Turtle()
                    new_text.penup()
                    new_text.hideturtle()
                    new_text.goto(state["x"].values[0], state["y"].values[0])
                    new_text.write(state["state"].values[0])
                    self.states = self.states[self.states["state"] != name]
                    self.score += 1
                    if self.score == max_number:
                        game_on = False
                else:
                    game_on = False
            else:
                game_on = False
        print(f"Final Score: {self.score}/{max_number}")
        self.states = self.states.set_index("state")
        self.states.to_csv(self.FILE_TO_LEARN)


GameBoard().game()
