import random
import turtle
from turtle import Turtle, Screen

tim = Turtle()
tim.shape("turtle")
tim.resizemode("user")
tim.shapesize(3, 3, 6)
tim.color("DarkGreen")
tim.pencolor("DarkSeaGreen3")
tim.pensize(2)
tim.speed(0)


def random_color():
    return f"#{random.randint(0, 255):02X}{random.randint(0, 255):02X}{random.randint(0, 255):02X}"


# Position to start from
tim.penup()
tim.backward(300)
tim.pendown()

# Challenge 1
# Draw a square 100x100
for _ in range(4):
    tim.forward(100)
    tim.left(90)

# Challenge 2
# Draw a dashed line 300
tim.left(45)
for _ in range(30):
    if _ % 2 == 0:
        tim.penup()
    else:
        tim.pendown()
    tim.forward(10)

# Position to start from
tim.penup()
tim.right(45)
tim.forward(100)
tim.right(90)
tim.pendown()

#Challenge 3
#Figures with random colors
tim.left(90)
for figure in range(3, 15):
    tim.pencolor(random_color())
    for _ in range(figure):
        tim.forward(40)
        tim.right(360 / figure)


# Position to start from
tim.penup()
tim.right(90)
tim.forward(320)
tim.pendown()

# Challenge 4
# Random walk
tim.shapesize(1, 1, 1)
continue_walk = True
tim.pensize(15)
tim.speed(0)


# Random Walk stops on enter key press
def on_click():
    global continue_walk
    continue_walk = False


screen = Screen()
screen.onkeypress(on_click, "Return")
screen.listen()
print("Press Return to exit Random Walk")

while continue_walk:
    tim.pencolor(random_color())
    tim.right(random.choice((0, 90, 180, 270)))
    tim.forward(20)


# Challenge 5
# Spirograph
tim.pensize(2)
tim.penup()
tim.home()
tim.pendown()

step = 6
for _ in range(int(360/step)):
    tim.circle(100)
    tim.pencolor(random_color())
    tim.left(step)


screen.exitonclick()

