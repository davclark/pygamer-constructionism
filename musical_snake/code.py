'''
musical_snake/code.py - a snake game / step sequencer mashup
'''
import asyncio

import displayio
import board

from snake_display import Sequencer, Snake
from instrument import AColorInstrument, DO, RE, MI, SO

# Types
try:
    # We use the hack that avoids extra memory for typing imports, the typing lib isn't in
    # CircuitPython, so this will only be imported using a CPython interpreter
    import typing

    # documentation types to clarify where we expect an actual note
    Solfège = int
except ImportError:
    pass

mary: list[list[Solfège]] = [
        [MI, RE, DO, RE,   MI, MI, MI,   None],
        [RE, RE, RE, None, MI, SO, SO,   None],
        [MI, RE, DO, RE,   MI, MI, MI,   MI],
        [MI, RE, RE, MI,   RE, DO, None, None],
        ]

async def main(sequences: list[list[Solfège]]):
    # Top-level group for combining all our groups
    meta_group = displayio.Group()

    instrument = AColorInstrument()
    sequencer = Sequencer(instrument)
    for row, sequence in enumerate(sequences):
        sequencer.notes_for_sequence(sequence, row)
    sequencer.draw_notes()

    snake = Snake(sequencer, (-8, Sequencer.row_locs[0]))

    meta_group.append(sequencer.group)
    meta_group.append(snake.group)

    # Add the Group to the Display
    # PyGamer resolution is 160x128
    display = board.DISPLAY
    display.show(meta_group)

    move_task = snake.move()
    groove_task = instrument.groove()

    # An Exception in either task will propagate here
    await asyncio.gather(move_task, groove_task)

asyncio.run(main(mary))
