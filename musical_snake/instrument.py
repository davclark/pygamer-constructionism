'''
instrument.py - frequencies and ways of organizing them
'''
import asyncio
import time
try:
    import typing
    Solfège = int
except ImportError:
    pass

import board
import busio
import adafruit_midi

from adafruit_midi.note_on import NoteOn
from adafruit_midi.note_off import NoteOff

from adafruit_pybadger.pygamer import pygamer


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

# The current plan is to use solfège in our sequences so we can easily select another root
# And already we're hitting the 0- vs. 1-offset thing
DO: Solfège = 0
RE: Solfège = 1
MI: Solfège = 2
SO: Solfège = 3

uart = busio.UART(board.TX, board.RX, baudrate=31250, timeout=0.001)  # init UART
midi_in_channel = 2
midi_out_channel = 1
midi = adafruit_midi.MIDI(
    midi_in=uart,
    midi_out=uart,
    in_channel=(midi_in_channel - 1),
    out_channel=(midi_out_channel - 1),
    debug=False,
)
note_hold = 0.85
rest = note_hold / 5

class AColorInstrument:
    # Frequencies with A natural (440 Hz) as the root
    tones = [440, 493.88, 554.37, 659.25]

    # Based on the keycap colors and ordering on my PyGamer
    colors = [Color.YELLOW, Color.WHITE, Color.RED, Color.BLACK]

    playing = None

    def start_playing(self, frequency: int):
        pygamer.start_tone(frequency)

    def stop_playing(self, frequency: int):
        """We have the frequency here as a placeholder for MIDI"""
        pygamer.stop_tone()

    def play(self, note: Solfège, source: str):
        '''
        Play a frequency corresponding to the given note on this instrument

        source can be 'button' or 'sequencer', and 'button' takes precedence
        '''
        frequency = self.tones[note]
        if source == 'button':
            if self.playing == 'sequencer':
                # Button overrides the sequencer
                self.stop('sequencer')
            # Not elif because we want to check this whether we hit the above branch or not
            if self.playing is None:
                self.playing = 'button'
                # This is used in the MIDI subclass
                self.played = frequency
                self.start_playing(frequency)

        elif source == 'sequencer' and self.playing is None:
            self.playing = 'sequencer'
            self.played = frequency
            self.start_playing(frequency)

    def stop(self, source: str):
        if source == self.playing:
            self.stop_playing(self.played)
            self.playing = None

    async def groove(self):
        while True:
            if pygamer.button.select:
                self.play(DO, 'button')
            elif pygamer.button.start:
                self.play(RE, 'button')
            elif pygamer.button.b:
                self.play(MI, 'button')
            elif pygamer.button.a:
                self.play(SO, 'button')
            else:
                self.stop('button')

            await asyncio.sleep(0)


class AColorMIDI(AColorInstrument):
    tones = [48, 50, 52, 55]
    # We're using maximum velocity for now
    def start_playing(self, frequency: int):
        midi.send(NoteOn(frequency, 127))

    def stop_playing(self, frequency: int):
        """We have the frequency here as a placeholder for MIDI"""
        midi.send(NoteOff(frequency, 0))
