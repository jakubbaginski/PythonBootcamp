import secrets
import colorgram
import turtle as t
t.colormode(255)

# colors = colorgram.extract("image.jpg", 20)
colors = colorgram.extract("claudemonet.jpg", 20)

colors_list = []
# skipping background color
# skip_color = True
skip_color = False

for color in colors:
    if not skip_color:
        colors_list.append((color.rgb.r, color.rgb.g, color.rgb.b))
    else:
        skip_color = False

SPACE_BETWEEN_DOTS = 10
DOT_SIZE = 20
NUMBER_OF_DOTS = 18*18

# number of dots in line equals to number of dots in column
dots_in_line = int(NUMBER_OF_DOTS ** 0.5)
offset = ((dots_in_line - 1) * (DOT_SIZE + SPACE_BETWEEN_DOTS)) / 2

my_turtle = t.Turtle()
my_turtle.hideturtle()
my_turtle.speed(0)
my_turtle.home()
my_turtle.penup()
my_turtle.setposition(-offset, -offset)

for y in range(dots_in_line):
    for x in range(dots_in_line):
        my_turtle.dot(DOT_SIZE, secrets.choice(colors_list))
        my_turtle.setx(my_turtle.xcor() + DOT_SIZE + SPACE_BETWEEN_DOTS)
    my_turtle.setx(-offset)
    my_turtle.sety(my_turtle.ycor() + DOT_SIZE + SPACE_BETWEEN_DOTS)

screen = t.Screen()
screen.exitonclick()
