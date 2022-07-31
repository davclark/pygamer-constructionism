import time

from adafruit_turtle import turtle, Color
from adafruit_pybadger.pygamer import pygamer

from snake_display import sprite_group

# Loop through each sprite in the sprite sheet
source_index = 0
thresh = {
    'right': 36000,
    'left': 30000,
    'up': 35000,
    'down': 29000,
}
delta_x = 1
delta_y = 0
while True:
    # When you change the sprite, it seems to mess up the location?
    # sprite[0] = source_index % 6
    # source_index += 1
    x, y = pygamer.joystick
    if pygamer.button.select:
        pygamer.play_tone(440, 0.5)
    elif pygamer.button.start:
        pygamer.play_tone(493.88, 0.5)
    elif pygamer.button.b:
        pygamer.play_tone(554.37, 0.5)
    elif pygamer.button.a:
        pygamer.play_tone(659.25, 0.5)


    # We include ONLY cases where the joystick is pressed in some direction
    # If we're in the middle, we don't update
    # Maybe it's nicer to just use pygamer.button.right?
    if x > thresh['right']:
        delta_x = 1
        if y > thresh['up']:
            delta_y = 1
        elif y < thresh['down']:
            delta_y = -1
        else:
            delta_y = 0
    elif x < thresh['left']:
        delta_x = -1
        if y > thresh['up']:
            delta_y = 1
        elif y < thresh['down']:
            delta_y = -1
        else:
            delta_y = 0
    else:
        if y > thresh['up']:
            delta_y = 1
            delta_x = 0
        elif y < thresh['down']:
            delta_y = -1
            delta_x = 0

    # Actually move the snake
    sprite_group.x += delta_x
    sprite_group.y += delta_y

    if sprite_group.x < -16:
        sprite_group.x = 160 - 16
    if sprite_group.x > 160 - 16:
        sprite_group.x = -16

    if sprite_group.y < -16:
        sprite_group.y = 128 - 16
    if sprite_group.y > 128 - 16:
        sprite_group.y = -16
    time.sleep(0.1)

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
