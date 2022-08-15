'''
musical_snake/code.py - a snake game / step sequencer mashup
'''
import asyncio

import displayio
import board

from snake_display import Sequencer, Snake
from instrument import AColorInstrument, DO, RE, MI, SO


mary_1 = [MI, RE, DO, RE, MI, MI, MI, None]

async def main():
    # Top-level group for combining all our groups
    meta_group = displayio.Group()

    instrument = AColorInstrument()
    sequencer = Sequencer(instrument)
    sequencer.notes_for_sequence(mary_1)
    sequencer.draw_notes()

    snake = Snake(sequencer, (0, Sequencer.row_locs[0]))

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

asyncio.run(main())
