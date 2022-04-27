## Using the REPL

I already forgot once... but once you're connected, you just hit ctrl-c to get a prompt for the REPL or to restart.

## Joystick

Turns out the analog joystick is not 100% stable, so I did some sampling to get a sense of what to expect (using the
REPL via tio):

>>> import adafruit_pybadger
>>> samples = [adafruit_pybadger.pybadger.joystick for _ in range(100)]
>>> x, y = zip(*samples)
>>> len(x)
100
>>> sum(x) / 100
33228.2
>>> sum(y) / 100
32169.0
>>> min x
Traceback (most recent call last):
  File "<stdin>", line 1
SyntaxError: invalid syntax
>>> min(x)
33120
>>> max(x)
33344
>>> min(y)
32128
>>> max(y)
32256

Using a while loop, I did some interactive poking about.

"Up" is ~160
"Down" is 65520
"Left" is similarly ~160
"Right" is 65520
