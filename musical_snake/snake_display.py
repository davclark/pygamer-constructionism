'''Separating logic for our Constructivist Snake Game display into a separate module'''
import asyncio
import board
import displayio

from adafruit_pybadger.pygamer import pygamer
import adafruit_imageload

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
