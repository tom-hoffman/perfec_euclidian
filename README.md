# PERFEC System: Euclidian Sequencer

A single channel USB-MIDI Euclidian Sequencer, written in CircuitPython for the Adafruit Circuit Playground Express (CPX).  

This sequencer will output NoteOn and NoteOff messages as well as 3.3v unipolar CV based on MIDI clock messages.  It will work as part of a CPX-based PERFEC System as well as any commercial or DIY MIDI devices that connect directly to USB or through an adapter.

A Euclidian Sequencer uses a variant of Euclid's Algorithm to generate a sequence based on a given number of steps and triggers.  The algorithm divides the triggers as evenly as possible among the steps.  This algorithm generates many of the traditional rhythms used around the world.  A set of Euclidian Sequencers is commonly used to create polyrhythmic music.

## Use

The Euclidian sequencer has two modes, set by the CPX switch:

* switch right -> **active mode**: an arc of blue and green neopixels starting from the top with a brighter white/red step indicator;
* switch left -> **config mode**: two arcs of blue (left) and green (right) neopixels starting from the bottom.

### Active Mode

There are two sub-modes in active mode, depending on whether or not the connected MIDI clock is started or stopped (note that this may present a problem if your im-PERFEC MIDI clock does not send out MIDI Start and MIDI Stop messages.

#### Active, clock started

In this mode, the sequencer will advance to the next step after the number of MIDI pulses specified in config.py.  This is 24 by default.  If the step is active -- the neopixel is green -- then the sequencer will send a NoteOn message, followed by a NoteOff message. 

##### Left button press, active, clock started

In this mode, the left button adds a step and calculates a new sequence.  After 10 steps, it resets to 1.

##### Right button press, active, clock started

In this mode, the right button adds a played trigger and calculates a new sequence.  If all the steps are currently played, it wraps to no played triggers.

#### Active, clock stopped

##### Left button press, active, clock stopped

In this mode, the active step is reset to zero, and the starting point of the sequence is shifted left one step.

##### Right button press, active, clock stopped

In this mode, the active step is reset to zero, and the starting point of the sequence is shifted right one step.

### Config Mode

This mode allows you to change the MIDI note value sent by the sequencer as well as the velocity of the notes.  There are no sub-modes based on clock activity.

#### Left button

Advances through a set of MIDI NoteOn values which are defined in `config.py`, with the value displayed in blue on the left half of the board.  Loops around to the beginning after the last selection.

#### Right button

Advances through a set of MIDI velocity values which are defined in `config.py.` as displayed in green on the right half of the board.  All played notes will use this value.  

