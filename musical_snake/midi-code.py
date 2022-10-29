# Write your code here :-)
import time

import board
import busio
import adafruit_midi

from adafruit_midi.note_on import NoteOn
from adafruit_midi.note_off import NoteOff

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

print("MIDI Out demo")
print("Default output channel:", midi.out_channel + 1)

while True:
    midi.send(NoteOn(48, 20))  # play note
    time.sleep(note_hold)  # hold note
    midi.send(NoteOff(48, 0))  # release note
    time.sleep(rest)  # rest

    midi.send(NoteOn(55, 40))
    time.sleep(note_hold)
    midi.send(NoteOff(55, 0))
    time.sleep(rest)

    midi.send(NoteOn(51, 60))
    time.sleep(note_hold)
    midi.send(NoteOff(51, 0))
    time.sleep(rest)

    midi.send(NoteOn(58, 80))
    time.sleep(note_hold)
    midi.send(NoteOff(58, 0))
    time.sleep(rest)


    midi.send(NoteOn(48, 20))  # play note
    time.sleep(note_hold)  # hold note
    midi.send(NoteOff(48, 0))  # release note
    time.sleep(rest)  # rest

    midi.send(NoteOn(55, 40))
    time.sleep(note_hold)
    midi.send(NoteOff(55, 0))
    time.sleep(rest)

    midi.send(NoteOn(51, 60))
    time.sleep(note_hold)
    midi.send(NoteOff(51, 0))
    time.sleep(rest)

    midi.send(NoteOn(50, 80))
    time.sleep(note_hold)
    midi.send(NoteOff(50, 0))
    time.sleep(rest)
