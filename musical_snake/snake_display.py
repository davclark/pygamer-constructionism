'''
snake_display.py - logic for Snake Game display into a separate module
'''

import asyncio
try:
    # We use the hack that avoids extra memory for typing imports, the typing lib isn't in
    # CircuitPython, so this will only be imported using a CPython interpreter
    import typing

    # documentation types to clarify where we expect an actual note
    Solfège = int
    Coords = tuple[int, int]
except ImportError:
    pass

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


class Sequencer:
    '''
    Our core step-sequencer logic:

    1. Render circles onto the bacground group
    2. Provide logic for sprite collision and note-playing
    '''
    # On-screen left-right / x location of our circles
    lr_locs = [20, 40, 60, 80, 100, 120, 140]
    # On-screen y location of our rows
    row_locs = [64]
    group: displayio.Group
    notes: list[tuple]  # tuple[Coords, displayio.TileGrid, Solfège]

    def __init__(self, display_group: displayio.Group):
        self.group = display_group
        self.notes = []

    def notes_for_sequence(self, seq: list[Solfège], row_index: int = 0):
        '''
        Make a visual row for the sequencer
        '''
        # For the time being we will skip the 8th note, as we only have 7 x_locs
        for lr_index, note in enumerate(seq):
            if note is not None:
                self.add_note(note, lr_index, row_index)

    def add_note(self, note: Solfège, lr_index: int, row_index: int, diameter: int = 5):
        '''
        Create a circle for display
        '''
        fill = Instrument.colors[note]
        if fill == Color.WHITE:
            outline = Color.BLACK
        else:
            outline = None
        lr = self.lr_locs[lr_index]
        row = self.row_locs[row_index]
        self.notes.append((
            (lr, row),
            Circle(lr, row, diameter, fill=fill, outline=outline),
            note
            ))

    def draw_notes(self):
        '''
        Draw all of the notes in self.notes

        Call after populating self.notes with self.notes_for_sequence()
        '''
        for _, sprite, _ in self.notes:
            self.group.append(sprite)


sequencer = Sequencer(bg_group)
sequencer.notes_for_sequence(mary_1)
sequencer.draw_notes()


class Snake:
    '''
    Keep track of the Blinka sprite

    Sprite positioning is based on the corner, so we also have some conversions to make collision
    computation easier.
    '''
    group: displayio.Group

    def __init__(self, lr_loc, row_loc):
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
        self.group = displayio.Group(scale=2)

        # Add the sprite to the Group
        self.group.append(sprite)

        self.set_location(lr_loc, row_loc)

    def set_location(self, lr_loc: int, row_loc: int):
        # Set sprite location - unlike the adafruit instructions, I seem to need to set
        # the sprite_group location (not the sprite)
        # We subtract 8 to make our coordinates comparable to our sequencer's circle centers
        self.group.x = lr_loc - 16
        self.group.y = row_loc - 16


    def move(self, lr_delta: int, row_delta: int):
        '''
        Update snake location and return current coordinates as a tuple

        We add 8 to make our coordinates comparable to our sequencer's circle centers
        '''
        self.group.x += lr_delta
        self.group.y += row_delta

        if self.group.x < -16:
            self.group.x = 160 - 16
        if self.group.x > 160 - 16:
            self.group.x = -16

        if self.group.y < -16:
            self.group.y = 128 - 16
        if self.group.y > 128 - 16:
            self.group.y = -16

        return (self.group.x + 16, self.group.y + 16)

snake = Snake(0, Sequencer.row_locs[0])

# We combine our groups into a group
meta_group = displayio.Group()

meta_group.append(bg_group)
meta_group.append(snake.group)


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

        snake.move(delta_x, delta_y)

        await asyncio.sleep(0.1)
