import logging
import time
import tkinter
import tkinter.ttk
import ttkthemes
import requests
import base64
import hashlib


class YaruStyleTk(ttkthemes.ThemedTk):

    YELLOW = 'yellow'
    PINK = 'pink'
    FONT_NAME = 'Arial'
    FONT_SIZE = 20

    def __init__(self):
        super(YaruStyleTk, self).__init__()
        self.style = ttkthemes.ThemedStyle()
        self.style_setup()

    def style_setup(self):
        self.style.set_theme('ubuntu')
        self.style.configure('.',
                             font=(self.FONT_NAME, self.FONT_SIZE),
                             background=self.YELLOW,
                             highlightcolor=self.YELLOW,
                             highlightbackground=self.YELLOW,
                             activeforeground=self.YELLOW,
                             activebackground=self.YELLOW,
                             disabledforeground=self.YELLOW,
                             foreground=self.PINK,
                             highlightthickness=0,
                             borderwidth=0,
                             padx=0, pady=0)
        self.style.configure('TButton', font=('', 15, ''))

        my_map = [('active', self.YELLOW),
                  ('!active', self.YELLOW),
                  ('alternate', self.YELLOW),
                  ('!alternate', self.YELLOW),
                  ('background', self.YELLOW),
                  ('!background', self.YELLOW),
                  ('disabled', self.YELLOW),
                  ('!disabled', self.YELLOW),
                  ('focus', self.YELLOW),
                  ('!focus', self.YELLOW),
                  ('invalid', self.YELLOW),
                  ('!invalid', self.YELLOW),
                  ('pressed', self.YELLOW),
                  ('!pressed', self.YELLOW),
                  ('selected', self.YELLOW),
                  ('!selected', self.YELLOW)]

        self.style.map('.',
                       background=my_map,
                       highlightcolor=my_map,
                       highlightbackground=my_map,
                       activeforeground=my_map,
                       activebackground=my_map,
                       disabledforeground=my_map,
                       # foreground=map,
                       indicatoron=my_map
                       )


class TriviaAPI:

    # API's URL https://opentdb.com/api_config.php
    # params of the value None are not to be passed through API
    API_PARAMS = {
        'amount': 1,
        'type': 'boolean',
        'category': None,
        'difficulty': None,
        'encode': 'base64'
    }

    def __init__(self, **kwargs):
        self.question: dict = {}
        self.api_params = self.API_PARAMS.copy()
        self.update_api_params(**kwargs)
        self.answered = []
        pass

    def update_api_params(self, **kwargs):
        not_default_params = {key: kwargs[key] for key in kwargs if key in self.API_PARAMS}
        self.api_params.update(not_default_params)
        self.api_params = {key: self.api_params[key] for key in self.api_params if self.api_params[key] is not None}

    def get_new_question(self, **kwargs) -> dict:
        self.update_api_params(**kwargs)
        response = requests.get('https://opentdb.com/api.php', params=self.api_params)
        response.raise_for_status()
        self.question: dict = response.json()['results'][0]
        self.decode_response()
        return self.question

    def decode_response(self):
        def decode(string):
            return base64.b64decode(str.encode(string)).decode()

        self.question['question'] = decode(self.question['question'])
        self.question['correct_answer'] = decode(self.question['correct_answer'])

    def is_in_answered(self, question, remember=False) -> bool:
        sha256 = hashlib.sha256(str.encode(str(question))).hexdigest()
        if sha256 in self.answered:
            logging.warning("Answered.")
            return True
        elif remember is True:
            self.answered.append(sha256)
        return False

    def get_new_not_answered_question(self, **kwargs):
        while self.is_in_answered(self.get_new_question(**kwargs)):
            pass
        return self.question


class TriviaQuizzerApp(YaruStyleTk):

    NAME = 'TriviaQuizzerApp'
    SCORE_TXT = 'Score: '

    def __init__(self):
        super(TriviaQuizzerApp, self).__init__()
        self.title(self.NAME)
        self.config(padx=50, pady=50)

        self.score = 0
        self.trivia_api = TriviaAPI()

        self.canvas = tkinter.Canvas(width=300, height=100)
        self.question = None
        self.question_text = None

        self.buttons = {
            True: tkinter.ttk.Button(),
            False: tkinter.ttk.Button()
        }
        self.score_label = tkinter.ttk.Label()
        self.update_score_label()
        self.set_layout_and_style()
        self.next_question()

    def next_question(self):
        if self.question_text is None:
            self.question_text = self.canvas.create_text(150, 50, text='', width=290, font=('', 15, ''))
        self.question = self.trivia_api.get_new_not_answered_question()
        self.canvas.itemconfig(self.question_text, text=self.question['question'])
        self.update()

    def update_score_label(self):
        self.score_label.config(text=self.SCORE_TXT + str(self.score))
        self.update()

    def set_layout_and_style(self):
        self.canvas.itemconfig(self.question_text, justify=tkinter.CENTER)
        self.buttons[True].config(text='True', command=self.answer_true)
        self.buttons[False].config(text='False', command=self.answer_false)

        self.score_label.grid(column=2, row=0, columnspan=1)
        self.canvas.grid(column=1, row=1, columnspan=2)
        self.buttons[True].grid(column=1, row=2, columnspan=1)
        self.buttons[False].grid(column=2, row=2, columnspan=1)
        self.update_score_label()
        self.update()

    def check_if_correct_answer(self, answer):
        if self.question['correct_answer'] == answer:
            self.trivia_api.is_in_answered(self.question, True)
            self.score += 1
            self.update_score_label()
            self.canvas.config(background='green')
            print(self.trivia_api.answered)
        else:
            self.canvas.config(background='red')
        self.update()
        time.sleep(1)
        self.canvas.config(background='white')
        self.update()
        self.next_question()

    def answer_true(self):
        self.check_if_correct_answer('True')

    def answer_false(self):
        self.check_if_correct_answer('False')


TriviaQuizzerApp().mainloop()
