import time

import board
import displayio

from adafruit_turtle import turtle, Color
import adafruit_imageload
from adafruit_pybadger.pygamer import pygamer

# PyGamer resolution is 160x128
display = board.DISPLAY

# Draw a white background
background = displayio.Bitmap(160, 128, 1)
bg_palette = displayio.Palette(1)
bg_palette[0] = 0xFFFFFF

bg_sprite = displayio.TileGrid(background, pixel_shader=bg_palette, x=0, y=0)

bg_group = displayio.Group()
bg_group.append(bg_sprite)

sprite_sheet, palette = adafruit_imageload.load("/cp_sprite_sheet.bmp",
                                                bitmap=displayio.Bitmap,
                                                palette=displayio.Palette)

sprite = displayio.TileGrid(sprite_sheet, pixel_shader=palette,
                            width = 1,
                            height = 1,
                            tile_width = 16,
                            tile_height = 16)

# Create a Group to hold the sprite
sprite_group = displayio.Group(scale=2)

# Add the sprite to the Group
sprite_group.append(sprite)

# We combine our groups into a group
meta_group = displayio.Group()

meta_group.append(bg_group)
meta_group.append(sprite_group)


# Set sprite location - unlike the adafruit instructions, I seem to need to set the sprite_group location (not the
# sprite)
sprite_group.x = 0
sprite_group.y = 80

# Add the Group to the Display
display.show(meta_group)

# Loop through each sprite in the sprite sheet
source_index = 0
thresh = {
    'right': 36000,
    'left': 30000,
    'up': 35000,
    'down': 29000,
}
delta_x = 0
delta_y = 0
while True:
    # When you change the sprite, it seems to mess up the location?
    # sprite[0] = source_index % 6
    # source_index += 1
    x, y = pygamer.joystick

    # We include ONLY cases where the joystick is pressed in some direction
    # If we're in the middle, we don't update
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
