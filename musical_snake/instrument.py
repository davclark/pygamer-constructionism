'''
instrument.py - frequencies and ways of organizing them
'''
try:
    import typing
    Solfège = int
except ImportError:
    pass

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
DO = 0
RE = 1
MI = 2
SO = 3

mary_1 = [MI, RE, DO, RE, MI, MI, MI, None]

class AColorInstrument:
    # Frequencies with A natural (440 Hz) as the root
    tones = [440, 493.88, 554.37, 659.25]

    # Based on the keycap colors and ordering on my PyGamer
    colors = [Color.YELLOW, Color.WHITE, Color.RED, Color.BLACK]

    @classmethod
    def play(cls, note: Solfège):
        pygamer.start_tone(cls.tones[note])

    @classmethod
    def stop(cls):
        pygamer.stop_tone()

