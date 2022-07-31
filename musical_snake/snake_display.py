'''Separating logic for our Constructivist Snake Game display into a separate module'''
import board
import displayio

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
