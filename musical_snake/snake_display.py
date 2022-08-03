'''Separating logic for our Constructivist Snake Game display into a separate module'''
import asyncio
import board
import displayio

from adafruit_pybadger.pygamer import pygamer
import adafruit_imageload
from adafruit_display_shapes.circle import Circle

# Draw a white background
background = displayio.Bitmap(160, 128, 1)
bg_palette = displayio.Palette(1)
bg_palette[0] = 0xFFFFFF

bg_sprite = displayio.TileGrid(background, pixel_shader=bg_palette, x=0, y=0)

bg_group = displayio.Group()
bg_group.append(bg_sprite)


# Basic shapes for now
class Color:
    """Standard colors"""

    WHITE = 0xFFFFFF
    BLACK = 0x000000
    RED = 0xFF0000
    ORANGE = 0xFFA500
    YELLOW = 0xFFEE00
    GREEN = 0x00C000
    BLUE = 0x0000FF
    PURPLE = 0x8040C0
    PINK = 0xFF40C0
    LIGHT_GRAY = 0xAAAAAA
    GRAY = 0x444444
    BROWN = 0xCA801D
    DARK_GREEN = 0x008700
    TURQUOISE = 0x00C0C0
    DARK_BLUE = 0x0000AA
    DARK_RED = 0x800000

    colors = (
        BLACK,
        WHITE,
        RED,
        YELLOW,
        GREEN,
        ORANGE,
        BLUE,
        PURPLE,
        PINK,
        GRAY,
        LIGHT_GRAY,
        BROWN,
        DARK_GREEN,
        TURQUOISE,
        DARK_BLUE,
        DARK_RED,
    )

circles = [Circle(20, 64, 5, fill=Color.RED),
           Circle(40, 64, 5, fill=Color.WHITE, outline=Color.BLACK),
           Circle(60, 64, 5, fill=Color.YELLOW),
           Circle(80, 64, 5, fill=Color.WHITE, outline=Color.BLACK),
           Circle(100, 64, 5, fill=Color.RED),
           Circle(120, 64, 5, fill=Color.RED),
           Circle(140, 64, 5, fill=Color.RED),
           ]

for c in circles:
    bg_group.append(c)

# Set up a sprite from the Adafruit sprite sheet
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


# Set sprite location - unlike the adafruit instructions, I seem to need to set
# the sprite_group location (not the sprite)
sprite_group.x = 0
sprite_group.y = 80

# Add the Group to the Display
# PyGamer resolution is 160x128
display = board.DISPLAY

display.show(meta_group)

async def move():
    # I developed these thresholds empirically inspecting pygamer.joystick on the REPL
    thresh = {
        'right': 36000,
        'left': 30000,
        'up': 35000,
        'down': 29000,
    }
    delta_x = 1
    delta_y = 0

    while True:
        x, y = pygamer.joystick

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

        await asyncio.sleep(0.1)
