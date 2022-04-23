import board
from adafruit_turtle import turtle, Color

# Square with dots
print("Turtle time! Lets draw a square with dots")

turtle = turtle(board.DISPLAY)
turtle.pendown()

for _ in range(4):
    turtle.dot(8)
    turtle.left(90)
    turtle.forward(25)

# Circles
mycolors = [Color.WHITE, Color.RED, Color.BLUE, Color.GREEN, Color.ORANGE, Color.PURPLE]
turtle.penup()
turtle.forward(130)
turtle.right(180)
turtle.pendown()

for i in range(6):
    turtle.pencolor(mycolors[i])
    turtle.circle(25)
    turtle.penup()
    turtle.forward(50)
    turtle.pendown()

while True:
    pass
