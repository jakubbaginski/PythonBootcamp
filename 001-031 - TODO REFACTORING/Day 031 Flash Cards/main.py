import logging
import random
import threading
import tkinter.messagebox
import typing
from tkinter import *
from tkinter.ttk import *

import pandas
from ttkthemes import *
from PIL import Image, ImageTk

logging.basicConfig(level=logging.WARN)


class FlashCards(ThemedTk):
    BACKGROUND_COLOR = "#B1DDC6"
    WIDTH = 800
    HEIGHT = 526
    SCALE = .5
    FONT_LANG = ("Arial", 30, 'italic')
    FONT_WORD = ('Arial', 50, 'bold')
    DELAY = 5
    TITLE = "FlashCards App"

    def __init__(self):
        super().__init__()

        # Data elements
        self.card_data: {str: str} = {}
        self.card_data_index: int = 0
        self.all_data: typing.Union[None, pandas.DataFrame] = None
        if not self.load_data():
            exit(0)
        # Timer
        self.timer: typing.Union[threading.Timer, None] = None

        # UI elements
        self.style = ThemedStyle()
        self.canvas = Canvas()
        self.images: {str: PhotoImage} = {
            'right': ImageTk.PhotoImage(Image.open("images/right.png").
                                        resize((int(100 * self.SCALE), int(100 * self.SCALE)), Image.BILINEAR)),
            'wrong': ImageTk.PhotoImage(Image.open("images/wrong.png").
                                        resize((int(100 * self.SCALE), int(100 * self.SCALE)), Image.BILINEAR)),
            'front': ImageTk.PhotoImage(Image.open("images/card_front.png").
                                        resize((int(self.WIDTH * self.SCALE), int(self.HEIGHT * self.SCALE)),
                                               Image.BILINEAR)),
            'back': ImageTk.PhotoImage(Image.open("images/card_back.png").
                                       resize((int(self.WIDTH * self.SCALE), int(self.HEIGHT * self.SCALE)),
                                              Image.BILINEAR))
        }
        self.buttons: {str: Button} = {
            'right': Button(),
            "wrong": Button()
        }
        self.labels: {str: Label} = {
        }

        self.card_image = None
        self.card_text_lang = None
        self.card_text_word = None

        self.generate_ui()
        self.show_new_card()

    def load_data(self) -> bool:
        def load_data_inner() -> bool:
            try:
                self.all_data = pandas.read_csv(file).transpose().to_dict()
            except pandas.errors.EmptyDataError:
                tkinter.messagebox.showerror(message="There are no data to learn.")
                return False
            else:
                return True

        try:
            with open('data/words_to_learn.csv', 'r') as file:
                return load_data_inner()
        except FileNotFoundError:
            with open('data/french_words.csv', 'r') as file:
                return load_data_inner()

    def save_words_to_learn(self):
        with open('data/words_to_learn.csv', 'w', newline='') as file:
            # to keep the same format default index must be removed from the dataset
            pandas.DataFrame(pandas.DataFrame(self.all_data).transpose()).to_csv(file, index=False)

    def button_action_right(self):
        del self.all_data[self.card_data_index]
        self.save_words_to_learn()
        if self.load_data():
            self.show_new_card()
        else:
            for item in self.buttons.values():
                item['state'] = DISABLED
                self.card_data = {'Good Job': 'Nothing to learn.'}
                self.show_flashcard()

    def button_action_wrong(self):
        self.show_new_card()

    def show_new_card(self):
        if self.timer is not None:
            self.timer.cancel()
        self.timer = threading.Timer(self.DELAY, self.flip_card)

        self.card_data_index = random.randint(0, len(self.all_data)-1)
        self.card_data = self.all_data[self.card_data_index]
        self.show_flashcard()
        self.timer.start()

    def flip_card(self):
        self.show_flashcard(side='back')

    def show_flashcard(self, side='front'):
        lang = tuple(self.card_data.keys())[0] if side == 'front' else tuple(self.card_data.keys())[-1]
        word = tuple(self.card_data.values())[0] if side == 'front' else tuple(self.card_data.values())[-1]
        self.canvas.itemconfig(self.card_image, image=self.images[side])
        self.canvas.itemconfig(self.card_text_lang, text=lang)
        self.canvas.itemconfig(self.card_text_word, text=word)

        self.canvas.update()

    def generate_ui(self):
        logging.info(self.style.get_themes())
        self.title(self.TITLE)

        self.config(padx=20, pady=20, background=self.BACKGROUND_COLOR, highlightcolor=self.BACKGROUND_COLOR)
        self.canvas.config(background=self.BACKGROUND_COLOR, width=self.SCALE * self.WIDTH,
                           height=self.SCALE * self.HEIGHT,
                           highlightthickness=0)
        self.buttons['right'].config(image=self.images['right'], command=self.button_action_right)
        self.buttons['wrong'].config(image=self.images['wrong'], command=self.button_action_wrong)

        self.canvas.grid(column=1, row=1, columnspan=2)
        self.buttons['right'].grid(column=1, row=2, columnspan=1, padx=10, pady=10)
        self.buttons['wrong'].grid(column=2, row=2, columnspan=1, padx=10, pady=10)

        self.card_image = self.canvas.create_image(self.SCALE * self.WIDTH / 2,
                                                   self.SCALE * self.HEIGHT / 2)
        self.card_text_lang = self.canvas.create_text(self.SCALE * self.WIDTH / 2,
                                                      self.SCALE * (self.HEIGHT / 2 - 150),
                                                      font=self.FONT_LANG)
        self.card_text_word = self.canvas.create_text(self.SCALE * self.WIDTH / 2,
                                                      self.SCALE * (self.HEIGHT / 2 + 100),
                                                      font=self.FONT_WORD)

        self.style.set_theme('default')
        self.style.configure('TButton', background=self.BACKGROUND_COLOR,
                             highlightcolor=self.BACKGROUND_COLOR, highlightthickness=0)

        my_map = [('active', self.BACKGROUND_COLOR),
                  ('!active', self.BACKGROUND_COLOR),
                  ('alternate', self.BACKGROUND_COLOR),
                  ('!alternate', self.BACKGROUND_COLOR),
                  ('background', self.BACKGROUND_COLOR),
                  ('!background', self.BACKGROUND_COLOR),
                  ('disabled', self.BACKGROUND_COLOR),
                  ('!disabled', self.BACKGROUND_COLOR),
                  ('focus', self.BACKGROUND_COLOR),
                  ('!focus', self.BACKGROUND_COLOR),
                  ('invalid', self.BACKGROUND_COLOR),
                  ('!invalid', self.BACKGROUND_COLOR),
                  ('pressed', self.BACKGROUND_COLOR),
                  ('!pressed', self.BACKGROUND_COLOR),
                  ('selected', self.BACKGROUND_COLOR),
                  ('!selected', self.BACKGROUND_COLOR)]

        self.style.map('.',
                       background=my_map,
                       highlightcolor=my_map,
                       highlightbackground=my_map,
                       activeforeground=my_map,
                       activebackground=my_map,
                       disabledforeground=my_map,
                       # foreground=map,
                       indicatoron=my_map,
                       )
        self.style.map('TButton',
                       background=my_map,
                       highlightcolor=my_map,
                       highlightbackground=my_map,
                       activeforeground=my_map,
                       activebackground=my_map,
                       disabledforeground=my_map,
                       # foreground=map,
                       indicatoron=my_map,
                       )

    def destroy(self):
        if self.timer is not None:
            self.timer.cancel()
        super(FlashCards, self).destroy()


FlashCards().mainloop()


# >>> a = [ [ str(a)+"x"+str(b)+","+str(a * b) for a in range(0,100) if a*b <= 100] for b in range(0,100)]
# >>> for x in a:
#     ...     for y in x:
#     ...

# >>> a = [ [ str(a)+":"+str(b)+","+str(a/b) for a in range(0,100) if a/b <= 100 and (a/b)*b == a ] for b in range(1,100)]
# >>> for x in a:
#     ...     for y in x:
#     ...             print(y)
# ...
