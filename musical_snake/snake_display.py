'''
snake_display.py - logic for Snake Game display into a separate module
'''

import asyncio
from math import sqrt
try:
    # We use the hack that avoids extra memory for typing imports, the typing lib isn't in
    # CircuitPython, so this will only be imported using a CPython interpreter
    import typing

    # documentation types to clarify where we expect an actual note
    Solfège = int
    Coords = tuple[int, int]
except ImportError:
    pass

import displayio

from adafruit_pybadger.pygamer import pygamer
import adafruit_imageload
from adafruit_display_shapes.circle import Circle

from instrument import Color


def dist(a, b):
    '''A simple Euclidean distance'''
    return sqrt(sum((s - t) ** 2 for s, t in zip(a, b)))

class Sequencer:
    '''
    Our core step-sequencer logic:

    1. Render circles onto the bacground group
    2. Provide logic for sprite collision and note-playing
    '''
    # On-screen left-right / x location of our circles
    lr_locs = [10 + 20*i for i in range(8)]
    # On-screen y location of our rows
    row_locs = [32 + 20*i for i in range(4)]
    group: displayio.Group
    notes: list[tuple[Coords, displayio.TileGrid, Solfège]]

    def __init__(self, instrument):
        self.instrument = instrument
        # Draw a white background
        background = displayio.Bitmap(160, 128, 1)
        bg_palette = displayio.Palette(1)
        bg_palette[0] = 0xFFFFFF
        bg_sprite = displayio.TileGrid(background, pixel_shader=bg_palette, x=0, y=0)

        self.group = displayio.Group()
        self.group.append(bg_sprite)
        self.notes = []

    def notes_for_sequence(self, seq: list[Solfège], row_index: int = 0):
        '''
        Make a visual row for the sequencer
        '''
        for lr_index, note in enumerate(seq):
            if note is not None:
                self.add_note(note, lr_index, row_index)

    def add_note(self, note: Solfège, lr_index: int, row_index: int, diameter: int = 5):
        '''
        Create a circle for display
        '''
        fill = self.instrument.colors[note]
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

    def bump(self, loc: Coords):
        for note_loc, _, note in self.notes:
            curr_dist = dist(loc, note_loc)
            if curr_dist <= 7:
                self.instrument.play(note, 'sequencer')
                break
        else:
            self.instrument.stop('sequencer')
            pass


class Snake:
    '''
    Keep track of the Blinka sprite

    Sprite positioning is based on the corner, so we also have some conversions to make collision
    computation easier.
    '''
    group: displayio.Group

    def __init__(self, sequencer: Sequencer, starting_loc: Coords):
        self.sequencer = sequencer
        # Set up a sprite from the Adafruit sprite sheet
        sprite_sheet, palette = adafruit_imageload.load("/cp_sprite_sheet.bmp",
                                                        bitmap=displayio.Bitmap,
                                                        palette=displayio.Palette)

        # I just looked to see what index was white (0xFFFFFF)
        # The eye is transparent now, which is a little weird, but better than a random square of white
        palette.make_transparent(19)

        sprite = displayio.TileGrid(sprite_sheet, pixel_shader=palette,
                                    width = 1,
                                    height = 1,
                                    tile_width = 16,
                                    tile_height = 16)

        # Create a Group to hold the sprite
        self.group = displayio.Group(scale=2)

        # Add the sprite to the Group
        self.group.append(sprite)

        self.set_location(starting_loc)

    def set_location(self, coords: Coords):
        # Set sprite location - unlike the adafruit instructions, I seem to need to set
        # the sprite_group location (not the sprite)
        # We subtract 8 to make our coordinates comparable to our sequencer's circle centers
        lr_loc, row_loc = coords
        self.group.x = lr_loc - 16
        self.group.y = row_loc - 16


    async def move(self):
        '''
        Update snake location and return current coordinates as a tuple

        We add 16 to make our coordinates comparable to our sequencer's circle centers
        '''
        lr_delta = 1
        row_delta = 0

        while True:
            lr_delta, row_delta = self.check_joystick(lr_delta, row_delta)

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

            self.sequencer.bump((self.group.x + 16, self.group.y + 16))

            await asyncio.sleep(1 / 30)


    def check_joystick(self, delta_x, delta_y) -> Coords:
        '''
        Update delta coordinates based on joystick

        We take the previous coordinates because we don't update if the joystick is neutral
        '''
        # I developed these thresholds empirically inspecting pygamer.joystick on the REPL
        # Maybe it's nicer to just use pygamer.button.right?
        # But will wait on that until after checking out the stage library
        thresh = {
            'right': 36000,
            'left': 30000,
            'up': 35000,
            'down': 29000,
        }

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

        return delta_x, delta_y
