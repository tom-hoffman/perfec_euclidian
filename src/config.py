# PERFEC System Euclidian Sequencer
# config.py
# copyright 2026, Tom Hoffman
# MIT License
# Variables and settings that might need to be changed by the user.

from micropython import const

# Assign this CPX a one digit identifier different than other modules
# of the same type.
CPX_NUMBER: int = 0
USB_NAME: str = "EUCLID" + str(CPX_NUMBER)

# Output MIDI channel for note messages.
# This is the "raw" 0-15 scale used in code, rather than 1-16 as is often displayed.
# "Raw" channel 9 is the default drum and percussion channel under the
# General MIDI specification (listed as 10 on the 1-16 scale).
CHANNEL_OUT: int = 9

# STARTING VALUES
# Adjust these if you want to create a pleasant default rhythm
# when your sequencers are powered up.

# DEFAULT_NOTE note index this sequence sends out when restarted:
# Adjust this to create a pleasant default setting for
# multiple sequencers and voices.
DEFAULT_NOTE: int = 0

# Starting number of steps in the sequence.
DEFAULT_STEPS: int = 4

# Starting number of triggers in the sequence.
DEFAULT_TRIGGERS: int = 4

# The starting point in the sequence when powered up
# or when the sequence is stopped and restarted.
DEFAULT_ROTATION: int = 1

# Velocity (volume/intensity) selector uses these values
# Allowed range is integers from 0 to 127 (7 bits)
VELOCITIES: tuple = const((0, 25, 50, 75, 100, 127))

# Default velocity index:
DEFAULT_VELOCITY: int = 4

# Setting Available Notes
#
# NOTE_NUMBERS is a tuple of MIDI note values. The active value
# can be selected directly from the CPX
# using the buttons and neopixel interface.
# The default values are based on the General MIDI specification
# for percussion values and correspond to:
'''
* 36/C1: bass drum
* 40/E1: electric snare
* 43/G1: high tom-tom
* 41/F1: low tom-tom
* 46/Bb1: open hi-hat
* 42/F#1: closed hi-hat
'''
# If everyone is following the General MIDI specification correctly,
# if these sequencers are plugged into a computer running a DAW or
# other MIDI workstation, the sounds listed above should correspond to
# the values selected on the Circuit Playground.
# In practice, you might need to adjust the note numbers either in this
# config file (below) or on the MIDI synthesizer.
# The first four notes are also part of the C major scale,
# so with several sequencers and a melodic (non-percussion)
# synth you can make a quick melodic bass sequence.
# Changing the note values will of course change the notes in
# the melodic sequence.
NOTE_NUMBERS: tuple = const((36, 40, 43, 41, 46, 42))

# Pulses Per Quarter Note
# The number of clock triggers counted before the sequencer advances.
# 24 is the official MIDI standard.
# If you want some sequencers to run faster or slower than others,
# try doubling or halving this value.
PPQN: int = 24

# Gate open scaling configuration represented as percentages mapped to whole integers
# to prevent resource-heavy floating-point calculations at runtime.
# This represents target ratios of: 10%, 25%, 50%, 75%, and 100%
GATE_RATIOS: tuple = const((10, 25, 50, 75, 100))

# Default gate duration selection index (ranges from 0 to 4)
GATE_DURATION_INDEX: int = 2

# MIDI repeat count
# this is the number of times we check and process the MIDI queue
# for every time we check and update the board buttons, neopixels, etc.
# raising this value reduces audible rhythm lag
# reducing this value decreases button and neopixel lag
MIDI_READ_REPEAT: int = 256

# Pre-allocated range loop based on the configuration setting 
# to optimize execution speed without allocating RAM at runtime
ACTIVE_REPEATS = range(MIDI_READ_REPEAT)
