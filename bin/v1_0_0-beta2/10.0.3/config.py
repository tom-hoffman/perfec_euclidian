# PERFEC System Euclidian Sequencer
# config.py
# copyright 2026, Tom Hoffman
# MIT License
# Variables and settings that might need to be changed by the user.

from micropython import const

# Output MIDI channel for note messages.
# This is the "raw" 0-15 scale used in code, rather than 1-16 as is often displayed.
# "Raw" channel 9 is the default drum and percussion channel under the
# General MIDI specification (listed as 10 on the 1-16 scale).
CHANNEL_OUT: int = 9

# Assign this CPX a one digit identifier different than other modules
# of the same type.
CPX_NUMBER: int = 0
# By default, the device name will be EUCLID + the CPX_NUMBER.
USB_NAME: str = "EUCLID" + str(CPX_NUMBER)


# STARTING VALUES
# Adjust these if you want to create a pleasant default rhythm
# when your sequencers are powered up.

# Starting number of steps in the sequence.
DEFAULT_STEPS: int = 4

# Starting number of triggers in the sequence.
DEFAULT_TRIGGERS: int = 1

# The starting point in the sequence when powered up
# or when the sequence is stopped and restarted.
DEFAULT_ROTATION: int = 0

# Starting Indexed Values
# These are all settings which are based on selecting one
# value out of a list.  These numbers correspond to the number
# of neopixels lit when selecting values directly on the CPX.
# Generally smaller numbers represent less of the thing. 
# The specific list of values are grouped in the next section.

# DEFAULT_NOTE (range 0 - 5)
# The pitch sent by this sequencer.
# Adjust this to create a pleasant default setting for
# multiple sequencers and voices.
# Change on CPX by pressing A in config mode while clock is stopped.
# Represented by purple neopixels.
DEFAULT_NOTE: int = CPX_NUMBER

# Default velocity index (range 0 - 5)
# "Velocity" in MIDI is usually interpreted as volume.
# 0 is silent.
# Change on CPX by pressing A in config mode while clock is playing.
# Represented in blue neopixels.
DEFAULT_VELOCITY: int = 4

# Default PPQN index (range 0 - 4)
# "PPQN" is MIDI clock pulses per quarter note.
# The original MIDI standard is 24 PPQN.  
# Increasing this one step will DOUBLE the beats per minute.
# Decreasing this will one step HALVE the beats per minute.
# Change on the CPX by pressing B in config mode while clock is stopped.
# Represented in yellow neopixels.
# Default of 2 = 24 PPQN.
DEFAULT_PPQN_INDEX: int = 2

# Default gate duration index (ranges 0 to 4)
# This is the length of time between the 
# MIDI NoteOn and NoteOff message, so generally
# the length of the played note.
# 0 is 1/10 of the quarter note defined by PPQN.
# 4 is 100% of the quarter note defined by PPQN.
# Change on the CPX by pressing B in config mode while clock is playing.
# Represented in green neopixels (G for gate, g for green).
# Default of 2 is 50%.
GATE_DURATION_INDEX: int = 2



# Value lists
# Generally you won't need to change these, 
# unless you want a special distribution, EXCEPT:

# Setting Available Notes
# If you want to play a specific scale or chord on a melodic
# synth, find the correct numbers for each note in the MIDI spec.
# You may also need to send specific notes to trigger a percussion synth.
NOTE_NUMBERS: tuple = const((36, 40, 43, 41, 46, 42))

# Velocity (volume/intensity) selector uses these values
# Allowed range is integers from 0 to 127 (7 bits)
VELOCITIES: tuple = const((0, 25, 50, 75, 100, 127))

# Pulses Per Quarter Note options from slowest (96) to fastest (6)
PPQN_VALUES: tuple = const((96, 48, 24, 12, 6))

# Gate open scaling configuration represented as percentages mapped to whole integers
# to prevent resource-heavy floating-point calculations at runtime.
# This represents target ratios of: 10%, 25%, 50%, 75%, and 100%
GATE_RATIOS: tuple = const((10, 25, 50, 75, 100))



# MIDI repeat count
# this is the number of times we check and process the MIDI queue
# for every time we check and update the board buttons, neopixels, etc.
# raising this value reduces audible rhythm lag
# reducing this value decreases button and neopixel lag
MIDI_READ_REPEAT: int = 256

# Pre-allocated range loop based on the configuration setting 
# to optimize execution speed without allocating RAM at runtime
# Do not change this.
ACTIVE_REPEATS = range(MIDI_READ_REPEAT)

