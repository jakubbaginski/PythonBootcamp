from turtle import Turtle, Screen

timmy = Turtle()
jenny = Turtle()
screen = Screen()
screen.title("This is the very first drawing.")
timmy.shape("turtle")
jenny.shape("turtle")
timmy.color("grey", "blue")
timmy.forward(100)
jenny.forward(100)
timmy.color("green")
timmy.circle(140)
timmy.color("red")
timmy.circle(-140)

jenny.color("yellow")
jenny.left(90)
jenny.circle(-30)
jenny.color("blue")
jenny.circle(30)

screen.exitonclick()
