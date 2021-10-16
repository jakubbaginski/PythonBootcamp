import random
import time
from tkinter import Tk, CENTER, GROOVE, N, E, S, W, END, StringVar, IntVar
from tkinter.ttk import Progressbar, Label, Entry, Button, Checkbutton


class MyClass:

    WINDOW_WIDTH = 600
    WINDOW_HEIGHT = 480

    def __init__(self):
        self.window = Tk()
        self.window.title("Test tkinter App")
        self.window.minsize(width=MyClass.WINDOW_WIDTH, height=MyClass.WINDOW_HEIGHT)
        self.window.maxsize(width=MyClass.WINDOW_WIDTH, height=MyClass.WINDOW_HEIGHT)
        self.window.config(padx=20, pady=20)

        self.label = Label(self.window, text="Test label", font=("Jellyka Saint-Andrew's Queen", 40, "normal"))
        self.label.config(anchor=CENTER, relief=GROOVE, width=21, background="#FFFFFF")
        # self.label.pack(expand=True)
        self.label.grid(row=1, column=1, columnspan=3, sticky=N+E+S+W)

        self.entry = Entry(self.window, font=("Jellyka Saint-Andrew's Queen", 40, "normal"), width=10)
        vcmd = (self.entry.register(self.validate_entry), '%s', '%P')
        self.entry.config(validatecommand=vcmd, validate="all")
        self.entry.insert(index=END, string="BUTTON")
        # self.entry.pack()
        self.entry.grid(row=2, column=1, columnspan=3, sticky=N+E+S+W)

        self.button = Button(self.window)
        self.button["text"] = "A button"
        self.button["command"] = self.test_command
        # self.button.pack(expand=True)
        self.button.grid(row=5, column=4, columnspan=1, sticky=N+E+S+W)

        self.check_value = StringVar()
        self.check_value.set('no')
        self.check_upper = Checkbutton(text="Upper/Lower", width=10, variable=self.check_value, command=self.radio)
        self.check_upper.configure(onvalue='yes', offvalue='no')
        # self.check_upper.pack()
        self.check_upper.grid(row=3, column=1, columnspan=1, sticky=N+E+S+W)

        self.progress_value = IntVar()
        self.progress_bar = Progressbar(self.window, variable=self.progress_value, mode='determinate')
        self.progress_bar.grid(row=4, column=1, columnspan=3, sticky=N+E+S+W)

    def radio(self):
        # do nothing function
        pass

    def test_command(self):
        self.progress_bar.start()
        while self.progress_value.get() < 80:
            time.sleep(.25)
            self.progress_value.set(self.progress_value.get()+20)
            self.progress_bar.update()
        self.progress_bar.stop()
        self.progress_value.set(0)
        if self.check_value.get() == 'yes':
            new_text = str(self.entry.get()).upper()
        else:
            new_text = str(self.entry.get()).lower()
        self.label.config(text=f"{new_text} {random.SystemRandom().randint(1, 100):03d}")

    def validate_entry(self, current_value, new_value):
        # logging.warning(f"'{current_value}' -> '{new_value}'")
        if len(new_value) > 10:
            return False
        return True

    def main_loop(self):
        self.window.mainloop()


MyClass().main_loop()
