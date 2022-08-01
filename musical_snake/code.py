'''
musical_snake/code.py - a snake game / step sequencer mashup
'''
import asyncio

from adafruit_pybadger.pygamer import pygamer

from snake_display import move


async def groove():
    while True:
        if pygamer.button.select:
            pygamer.start_tone(440)
        elif pygamer.button.start:
            pygamer.start_tone(493.88)
        elif pygamer.button.b:
            pygamer.start_tone(554.37)
        elif pygamer.button.a:
            pygamer.start_tone(659.25)
        else:
            pygamer.stop_tone()

        await asyncio.sleep(0)


async def main():
    move_task = move()
    groove_task = groove()

    # An Exception in either task will propagate here
    await asyncio.gather(move_task, groove_task)

asyncio.run(main())
