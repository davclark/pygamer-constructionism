'''
snake_display.py - logic for Snake Game display into a separate module
'''

import asyncio
import board
import displayio

from adafruit_pybadger.pygamer import pygamer
import adafruit_imageload
from adafruit_display_shapes.circle import Circle

from instrument import AColorInstrument as Instrument
from instrument import DO, RE, MI, SO, Color, mary_1

# Draw a white background
background = displayio.Bitmap(160, 128, 1)
bg_palette = displayio.Palette(1)
bg_palette[0] = 0xFFFFFF

bg_sprite = displayio.TileGrid(background, pixel_shader=bg_palette, x=0, y=0)

bg_group = displayio.Group()
bg_group.append(bg_sprite)

# documentation type to clarify where we expect an actual note
Solfège = int

def circle_for_note(note: Solfège, x_loc: int, y_loc: int = 64, diameter: int = 5) -> displayio.TileGrid:
    '''
    Create a circle for display
    '''
    fill = Instrument.colors[note]
    if fill == Color.WHITE:
        outline = Color.BLACK
    else:
        outline = None
    return Circle(x_loc, y_loc, diameter, fill=fill, outline=outline)


def circles_for_sequence(seq: list[Solfège], x_locs: list[int]) -> list[displayio.TileGrid]:
    '''
    Make a visual row for the sequencer
    '''
    return [circle_for_note(note, x_loc) for note, x_loc in zip(seq, x_locs)]

sequence_x_locs = [20, 40, 60, 80, 100, 120, 140]

for c in circles_for_sequence(mary_1, sequence_x_locs):
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
