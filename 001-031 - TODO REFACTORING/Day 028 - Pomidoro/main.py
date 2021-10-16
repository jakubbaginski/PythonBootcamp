# ---------------------------- CONSTANTS ------------------------------- #
import threading
import time
import tkinter as tk
import tkinter.ttk as tkk
import typing
import ttkthemes as th

# logging.basicConfig(level=logging.ERROR)

WHITE = "#FFFFFF"
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
FONT_SIZE = 40
FONT_OFFSET = 25

WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20

WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500
IMAGE_WIDTH = 210
IMAGE_HEIGHT = 230
MARGIN = 20

TEXT_APP_NAME = 'Pomidoro App'
TEXT_START = 'Start'
TEXT_RESET = 'Reset'
TEXT_TIMER = 'Timer'
TEXT_WORK = "Work"
TEXT_BREAK = "Break"
DELAY = 1


def format_time(seconds: float):
    seconds_gm_time = time.gmtime(seconds)
    return f"{seconds_gm_time[4]:02d}:{seconds_gm_time[5]:02d}"


class PomidoroApp(th.ThemedTk):

    # ---------------------------- UI SETUP ------------------------------- #

    def __init__(self):
        super(PomidoroApp, self).__init__()
        self.title(TEXT_APP_NAME)
        self.config(bg=YELLOW, padx=MARGIN, pady=MARGIN)
        self.style = th.ThemedStyle()
        self.style_setup()

        self.period = 0
        self.time_frames = [(WORK_MIN, TEXT_WORK, GREEN), (SHORT_BREAK_MIN, TEXT_BREAK, PINK)] * 4
        self.time_frames[-1] = (LONG_BREAK_MIN, TEXT_BREAK, RED)
        self.time_frames = [(item[0] / 2 + DELAY, item[1], item[2]) for item in self.time_frames]

        self.photo = tk.PhotoImage(file="./tomato.png")
        self.canvas = tk.Canvas(width=IMAGE_WIDTH, height=IMAGE_HEIGHT, bg=YELLOW,
                                borderwidth=0, highlightthickness=0)
        self.canvas.create_image(IMAGE_WIDTH / 2, IMAGE_HEIGHT / 2, image=self.photo, anchor=tk.CENTER)
        self.timer_text = self.canvas.create_text(IMAGE_WIDTH / 2, FONT_OFFSET + IMAGE_HEIGHT / 2,
                                                  font=(FONT_NAME, FONT_SIZE, "bold"), fill=WHITE)

        self.start_button = tkk.Button(text=TEXT_START)
        self.reset_button = tkk.Button(text=TEXT_RESET, style='TButton')
        self.label = tkk.Label()
        self.check_label = tkk.Label(foreground=GREEN)
        self.progress_bar = tkk.Progressbar()

        self.label.grid(column=1, row=1, columnspan=3)
        self.canvas.grid(column=2, row=2, columnspan=1)
        self.start_button.grid(column=1, row=3, columnspan=1, sticky=tk.NW)
        self.check_label.grid(column=2, row=3, columnspan=1, sticky=tk.N)
        self.reset_button.grid(column=3, row=3, columnspan=1, sticky=tk.NE)
        self.progress_bar.grid(column=1, row=4, columnspan=3, sticky=tk.E + tk.W + tk.N + tk.S)

        # ---------------------------- TIMER RESET ------------------------------- #
        # ---------------------------- TIMER MECHANISM ------------------------------- #
        # ---------------------------- COUNTDOWN MECHANISM ------------------------------- #

        self.period = 0
        self.time_frames = [(WORK_MIN, TEXT_WORK, GREEN), (SHORT_BREAK_MIN, TEXT_BREAK, PINK)] * 4
        self.time_frames[-1] = (LONG_BREAK_MIN, TEXT_BREAK, RED)
        self.time_frames = [{'seconds': item[0] / 2 + DELAY,
                             'text': item[1],
                             'color': item[2]} for item in self.time_frames]
        self.update_text_elements()

        self.timer: typing.Union[threading.Timer, None] = None
        self.start_button.config(command=self.start_timer)
        self.reset_button.config(command=self.stop_timer)

        self.progress = tk.IntVar()
        self.progress.set(0)
        self.progress_bar.config(maximum=int(sum([item['seconds'] for item in self.time_frames])),
                                 variable=self.progress, mode='indeterminate')

    def start_timer(self, button=True):
        self.start_button['state'] = tk.DISABLED
        if button is False or self.timer is None:
            if self.timer is not None:
                self.timer.cancel()
            self.timer = threading.Timer(DELAY, self.timer_loop_function,
                                         kwargs={'start_time': time.time()})
            self.timer.start()
            self.update_text_elements()

    def stop_timer(self):
        self.start_button['state'] = tk.NORMAL
        if self.timer is not None:
            self.timer.cancel()
            self.timer = None
        self.period = 0
        self.progress.set(0)
        self.update_text_elements()

    def timer_loop_function(self, **kwargs):
        wait_sec = self.time_frames[self.period]['seconds'] - (time.time() - kwargs.get('start_time'))
        wait_sec = 0 if wait_sec < 0 else wait_sec
        self.canvas.itemconfig(self.timer_text, text=format_time(wait_sec))
        # logging.info(f" Period {self.period} : {self.time_frames[self.period]} -> {wait_sec}")
        self.progress.set(int(sum([item['seconds'] for item in self.time_frames[0:self.period+1]]) - wait_sec))
        if wait_sec > 0:
            self.timer.run()
        else:
            # push the window to the top
            self.lift()
            self.attributes("-topmost", True)
            self.attributes("-topmost", False)

            self.period += 1
            self.timer.cancel()
            if self.period < len(self.time_frames):
                self.start_timer(button=False)
            else:
                self.timer = None
                self.period = 0
                self.start_button['state'] = tk.NORMAL

    def destroy(self):
        if self.timer is not None:
            self.timer.cancel()
        super(PomidoroApp, self).destroy()

    # ---------------------------- UI SETUP ------------------------------- #

    def update_text_elements(self):
        self.label.config(text=self.time_frames[self.period]['text'],
                          foreground=self.time_frames[self.period]['color'])
        self.canvas.itemconfig(self.timer_text, text=format_time(self.time_frames[self.period]['seconds']))
        self.check_label.config(text="")
        checkmarks = ["✓" for item in self.time_frames[0:self.period] if item['text'] == TEXT_WORK]
        self.check_label.config(text="".join(checkmarks))
        self.canvas.update()

    # ---------------------------- Theme and Styles ----------------------- #

    def style_setup(self):
        # logging.info("Style configuration")
        self.set_theme('yaru')
        self.style.configure('.',
                             font=(FONT_NAME, FONT_SIZE),
                             background=YELLOW,
                             highlightcolor=YELLOW,
                             highlightbackground=YELLOW,
                             activeforeground=YELLOW,
                             activebackground=YELLOW,
                             disabledforeground=YELLOW,
                             foreground=PINK,
                             highlightthickness=0,
                             borderwidth=0,
                             padx=0, pady=0)
        self.style.configure('TButton', font=('', 15, ''))

        my_map = [('active', YELLOW),
                  ('!active', YELLOW),
                  ('alternate', YELLOW),
                  ('!alternate', YELLOW),
                  ('background', YELLOW),
                  ('!background', YELLOW),
                  ('disabled', YELLOW),
                  ('!disabled', YELLOW),
                  ('focus', YELLOW),
                  ('!focus', YELLOW),
                  ('invalid', YELLOW),
                  ('!invalid', YELLOW),
                  ('pressed', YELLOW),
                  ('!pressed', YELLOW),
                  ('selected', YELLOW),
                  ('!selected', YELLOW)]

        self.style.map('.',
                       background=my_map,
                       highlightcolor=my_map,
                       highlightbackground=my_map,
                       activeforeground=my_map,
                       activebackground=my_map,
                       disabledforeground=my_map,
                       indicatoron=my_map
                       )


PomidoroApp().mainloop()
