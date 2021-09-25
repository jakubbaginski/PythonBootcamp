import turtle as t

## Etch-A-Sketch

class MyClass:

    def __init__(self):
        self.pen = t.Turtle()
        self.screen = t.Screen()
        self.STEP = 20
        self.RADIUS = 100
        self.ANGLE = 5
        self.COLOR = "DarkSeaGreen"
        self.pen.speed(0)
        self.pen.pensize(3)
        self.pen.resizemode("user")
        self.pen.shapesize(1, 1, 10)
        self.pen.color(self.COLOR)
        self.pen.pencolor(self.COLOR)

        self.COMMANDS = {
            "W": (self.forwards_on_key_press, "move forwards"),
            "S": (self.backwards_on_key_press, "move backwards"),
            "A": (self.counter_clockwise_on_key_press, "move counter clockwise"),
            "D": (self.clockwise_on_key_press, "move clockwise"),
            "Z": (self.clockwise_rotate_on_key_press, "rotate clockwise"),
            "X": (self.counter_clockwise_rotate_on_key_press, "rotate counter clockwise"),
            "C": (self.clear_drawing_on_key_press, "clear the drawing and center position of pen")
        }

        for key in self.COMMANDS:
            self.on_key_press(self.COMMANDS[key][0], key)
        self.screen.listen()

    def on_key_press(self, function, key):
        self.screen.onkeypress(function, key.lower())
        self.screen.onkeypress(function, key.upper())

    def forwards_on_key_press(self):
        self.pen.forward(self.STEP)

    def backwards_on_key_press(self):
        self.pen.backward(self.STEP)

    def counter_clockwise_on_key_press(self):
        self.pen.circle(self.RADIUS, self.ANGLE)

    def clockwise_rotate_on_key_press(self):
        self.pen.setheading(self.pen.heading()-self.ANGLE)

    def counter_clockwise_rotate_on_key_press(self):
        self.pen.setheading(self.pen.heading()+self.ANGLE)

    def clockwise_on_key_press(self):
        self.pen.circle(self.RADIUS, -self.ANGLE)

    def clear_drawing_on_key_press(self):
        self.pen.clear()
        self.pen.penup()
        self.pen.home()
        self.pen.pendown()

    def loop(self):
        print("Close the window to finish.")
        for key in self.COMMANDS:
            print(f"{key} - {self.COMMANDS[key][1]}")

        self.screen.mainloop()


MyClass().loop()
