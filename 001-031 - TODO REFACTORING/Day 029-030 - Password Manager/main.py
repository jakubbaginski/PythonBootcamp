import logging
import secrets
import random
import pyclip
import json
import re

import numpy
import ttkthemes as tt
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as mb

# logging.basicConfig(level=logging.DEBUG)


class PasswordManager(tt.ThemedTk):
    APP_TITLE = "Password Manager"
    IMAGE_WIDTH = 210
    IMAGE_HEIGHT = 200
    FONT = ('Arial', 11, 'bold')
    FONT2 = ('Courier', 11, '')
    FILE_NAME = "password.json"

    def __init__(self):
        super(PasswordManager, self).__init__()
        self.title(self.APP_TITLE)
        self.style = tt.ThemedStyle()
        self.style_setup()
        self.config(padx=45, pady=45)

        self.canvas = tk.Canvas()
        self.canvas.config(width=self.IMAGE_WIDTH, height=self.IMAGE_HEIGHT)
        self.picture = tk.PhotoImage(file="logo.png")
        self.canvas.create_image(self.IMAGE_WIDTH / 2, self.IMAGE_HEIGHT / 2, image=self.picture)

        self.labels = {
            'website': ttk.Label(width=12, text="WebSite Name:", font=self.FONT),
            'email': ttk.Label(width=12, text="E-mail:", font=self.FONT),
            'password': ttk.Label(width=12, text="Password:", font=self.FONT)
        }

        self.data: {str: tk.StringVar} = {
            'website': tk.StringVar(),
            'email': tk.StringVar(),
            'password': tk.StringVar()
        }

        self.all_data = {str: {str: str}}
        self.load_from_file()
        self.entries = {
            'website': ttk.Combobox(width=21, textvariable=self.data['website'],
                                    values=self.get_unique_values('website'),
                                    font=self.FONT2),
            'email': ttk.Combobox(width=43, textvariable=self.data['email'],
                                  values=self.get_unique_values('email'),
                                  font=self.FONT2),
            'password': ttk.Entry(width=23, textvariable=self.data['password'], font=self.FONT2)
        }
        self.entries['email'].config(validatecommand=(self.entries['email'].register(self.validate_email), '%P'),
                                     validate='all')

        self.buttons = {
            'search': ttk.Button(width=15, text="Search", command=self.search),
            'password': ttk.Button(width=15, text="Generate Password", command=self.generate_password),
            'save': ttk.Button(width=30, text="Save and Back", command=self.save_to_file)
        }

        sticky = tk.N + tk.S + tk.W + tk.E
        self.canvas.grid(column=0, row=0, columnspan=3)
        self.labels['website'].grid(column=0, row=1, columnspan=1, sticky=sticky)
        self.labels['email'].grid(column=0, row=2, columnspan=1, sticky=sticky)
        self.labels['password'].grid(column=0, row=3, columnspan=1, sticky=sticky)
        self.entries['website'].grid(column=1, row=1, columnspan=1, sticky=sticky)
        self.entries['email'].grid(column=1, row=2, columnspan=2, sticky=sticky)
        self.entries['password'].grid(column=1, row=3, columnspan=1, sticky=sticky)
        self.buttons['search'].grid(column=2, row=1, columnspan=1, sticky=sticky)
        self.buttons['password'].grid(column=2, row=3, columnspan=1, sticky=sticky)
        self.buttons['save'].grid(column=0, row=4, columnspan=3, sticky=sticky)

        self.entries['website'].focus()

    def validate_email(self, new_value) -> bool:
        pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if re.fullmatch(pattern, new_value):
            self.entries['email'].config(foreground="green")
        else:
            self.entries['email'].config(foreground="red")
        self.update()
        return True

    def update_entries(self):
        for variable in self.data.values():
            variable.set("")
        self.entries['website'].config(values=self.get_unique_values('website')),
        self.entries['email'].config(values=self.get_unique_values('email'))
        self.update()

    def get_unique_values(self, entry: str):
        return list(set([item[entry] for item in self.all_data.values()]))

    def search(self):
        data = [item for item in self.all_data.values() if item['website'] == self.data['website'].get()]
        if self.data['email'].get() != "":
            data = [item for item in data if item['email'] == self.data['email'].get()]
        if len(data) >= 1:
            self.data['email'].set(data[0]['email'])
            self.data['password'].set(data[0]['password'])
            if len(data) > 1:
                mb.showwarning(message="There are more data for this website.\n"
                                       "Use email field to narrow down search.\n"
                                       "First found result is presented.")
        else:
            mb.showinfo(message="There are no data for this website.")
            self.data['email'].set("")
            self.data['password'].set("")
        self.update()

    def generate_password(self):
        allowed_chars = {
            0: {
                'chars': [chr(x) for x in range(ord('A'), ord('Z') + 1)] + [chr(x) for x in
                                                                            range(ord('a'), ord('z') + 1)],
                'number': 12},
            1: {
                'chars': [str(x) for x in range(0, 10)] + [x for x in "!@#$%^&*"],
                'number': 6}}
        pwd = numpy.concatenate([[secrets.choice(allowed_chars[i]['chars'])
                                  for _ in range(0, allowed_chars[i]['number'])]
                                 for i in range(0, len(allowed_chars))])
        random.shuffle(list(pwd))
        self.data['password'].set("".join([pwd[i] + "-" if i % 6 == 5 and i != len(pwd) - 1 else pwd[i]
                                           for i in range(0, len(pwd))]))
        pyclip.copy(self.data['password'].get())

    def load_from_file(self):
        self.all_data: {str: {str: str}} = {}
        try:
            with open(self.FILE_NAME, "r") as file:
                self.all_data = json.load(file)
        except FileNotFoundError:
            with open(self.FILE_NAME, "w") as _:
                # new file created
                pass
        except json.JSONDecodeError:
            # file is empty, do continue
            pass

    def save_to_file(self):
        if len([True for item in self.data.values() if item.get() == ""]) > 0:
            mb.showerror(message="Please provide all data: website, email and password.")
        else:
            self.load_from_file()
            hash_key = str(hash("".join([self.data['website'].get(), self.data['email'].get()])))
            self.all_data[hash_key] = {key: self.data[key].get() for key in self.data.keys()}
            with open(self.FILE_NAME, "w") as file:
                json.dump(self.all_data, file, indent=3, sort_keys=True)
                self.update_entries()
                mb.showinfo(message="Data saved successfully.")

    def style_setup(self):
        logging.info(f"Style configuration / one of {self.style.get_themes()}")
        self.set_theme('arc')
        self.style.configure('.', font=self.FONT)
        self.style.configure('TLabel', font=self.FONT)


PasswordManager().mainloop()
