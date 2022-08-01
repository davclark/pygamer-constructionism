import time

from adafruit_pybadger.pygamer import pygamer

from snake_display import sprite_group

# Loop through each sprite in the sprite sheet
source_index = 0
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
    # When you change the sprite, it seems to mess up the location?
    # sprite[0] = source_index % 6
    # source_index += 1
    x, y = pygamer.joystick
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
    time.sleep(0.1)
