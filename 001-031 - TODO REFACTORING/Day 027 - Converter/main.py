import tkinter as tk
import tkinter.ttk as ttk


def calculate_miles_to_km(value: float) -> str:
    return f"{1.609344 * float(value):3.6f}"


def calculate_km_to_miles(value: float) -> str:
    return f"{float(value)/1.609344:3.6f}"


class Converter(tk.Tk):
    WINDOW_WIDTH = 400
    WINDOW_HEIGHT = 100
    TITLE = "Converter miles/km and km/miles"
    INIT_OUTPUT = 0
    MILES_TEXT = "miles"
    KM_TEXT = "km"

    def __init__(self):
        super(Converter, self).__init__()
        self.title(Converter.TITLE)
        #self.minsize(width=Converter.WINDOW_WIDTH, height=Converter.WINDOW_HEIGHT)
        #self.maxsize(width=Converter.WINDOW_WIDTH, height=Converter.WINDOW_HEIGHT)
        self.config(padx=20, pady=20)

        self.input_variable = tk.StringVar()

        self.input = ttk.Entry()
        self.input.config(validatecommand=(self.input.register(self.validate), '%P'),
                          validate="all")
        self.input.config(textvariable=self.input_variable)
        self.input.grid(row=1, column=1, columnspan=3, sticky=tk.N+tk.E+tk.S+tk.W)

        self.entry_unit = ttk.Label()
        self.entry_unit.grid(row=1, column=4, columnspan=1, sticky=tk.N+tk.E+tk.S+tk.W)

        self.output_text = ttk.Label()
        self.output_text.config(text="is equal to:")
        self.output_text.grid(row=2, column=0, columnspan=1, sticky=tk.N+tk.E+tk.S+tk.W)

        self.output_variable = tk.StringVar()

        self.output = ttk.Label()
        self.output.config(textvariable=self.output_variable)
        self.output.grid(row=2, column=1, columnspan=3, sticky=tk.N+tk.E+tk.S+tk.W)
        self.output_unit = ttk.Label()
        self.output_unit.grid(row=2, column=4, columnspan=1, sticky=tk.N+tk.E+tk.S+tk.W)

        self.button = ttk.Button()
        self.button.config(text="Switch", command=self.switch_units)
        self.button.grid(row=3, column=4, columnspan=1, sticky=tk.N+tk.E+tk.S+tk.W)

        # opposite to function we want to start with
        self.calculation = calculate_km_to_miles
        self.output_variable.set(self.calculation(self.INIT_OUTPUT))
        self.switch_units()

    def switch_units(self):
        self.input_variable.set(self.output_variable.get())
        if self.calculation == calculate_miles_to_km:
            self.calculation = calculate_km_to_miles
            self.set_km_to_miles()
        else:
            self.calculation = calculate_miles_to_km
            self.set_miles_to_km()

    def set_miles_to_km(self):
        self.entry_unit.config(text=self.MILES_TEXT)
        self.output_unit.config(text=self.KM_TEXT)
        self.calculation = calculate_miles_to_km
        self.validate(self.input_variable.get())

    def set_km_to_miles(self):
        self.entry_unit.config(text=self.KM_TEXT)
        self.output_unit.config(text=self.MILES_TEXT)
        self.calculation = calculate_km_to_miles
        self.validate(self.input_variable.get())

    def validate(self, new_value) -> bool:
        if new_value == "":
            new_value = self.INIT_OUTPUT
        try:
            self.output_variable.set(self.calculation(new_value))
        except ValueError:
            return False
        return True


Converter().mainloop()
