# PERFEC System Euclidian Sequencer
# config.py
# copyright 2026, Tom Hoffman
# MIT License

# Starting variables that might need to be changed by the user.

# Give each Circuit Playground a unique name so you don't get confused!
USB_NAME: str = "EUCLID0"

if len(USB_NAME) > 11:
    raise ValueError("USB_NAME too long (>11).")

# send MIDI messages on:
# this is the "raw" 0-15 scale
channel_out: int = 15

# MIDI repeat count
# this is the number of times we check and process the MIDI queue 
# for every time we check and update the board buttons, neopixels, etc.
# raise this value if you are getting audible rhythm lag
# which will in turn increase button and neopixel lag

MIDI_READ_REPEAT: int = 256

# These are the note values each sequencer will put out.
# preset for Nord Drum 3p - 60, 62, 64, 65, 67, 69
NOTE_NUMBERS: tuple[int] = (60, 62, 64, 65, 67, 69)

VELOCITIES: tuple[int] = const((0, 25, 50, 75, 100, 127))

# The note index THIS sequence sends out when restarted:
note: int = 0

# pulses per quarter note
PPQN: int = 24

# duration of analog gate
# currently must be less than PPQN
GATE_DURATION: int = 6

# starting values for the sequencer
DEFAULT_VELOCITY: int = 4
DEFAULT_STEPS: int = 4
DEFAULT_TRIGGERS: int = 1
DEFAULT_ROTATION: int = 0


