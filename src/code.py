# PERFEC System Euclidian Sequencer
# code.py
# copyright 2026, Tom Hoffman
# MIT License
# This module contains the main loop of the application.

__version__ = "1.0.0 beta"

import gc
print("After gc: " + str(gc.mem_free()))
import config
import midi_controller
print("After midi controller: " + str(gc.mem_free()))
from minimal_midi import MinimalMidi
print("After minimal_midi: " + str(gc.mem_free()))
from model import SequenceModel
print("After model: " + str(gc.mem_free()))
import board_controller
print("After board controller: " + str(gc.mem_free()))

led_count: int = 10

# Initialize core model and generate the initial pattern
tm: SequenceModel = SequenceModel(config.DEFAULT_NOTE, config.NOTE_NUMBERS, led_count=led_count)
tm.generate()

# Pre-instantiate our MIDI parser and initial state
midi_driver: MinimalMidi = MinimalMidi(0, config.CHANNEL_OUT) # Explicitly initialized with 0 for in_channel
mc: midi_controller.MidiController = midi_controller.Stopped(tm, midi_driver)

# Pre-instantiate ALL possible views once at boot time to prevent dynamic heap fragmentation
view_playing = board_controller.SeqPlayingView(tm)
view_stopped = board_controller.SeqStoppedView(tm)
view_config_playing = board_controller.ConfigPlayingView(tm)
view_config_stopped = board_controller.ConfigStoppedView(tm)

# Fast nested dictionary map to swap active view modes allocation-free based on:
# 1. The slide switch state (cpx.switch_is_left() -> True means config menu, False means sequencer)
# 2. The MIDI transport status class type (Playing vs Stopped)
view_map: dict = {
    False: {
        midi_controller.Playing: view_playing,
        midi_controller.Stopped: view_stopped
    },
    True: {
        midi_controller.Playing: view_config_playing,
        midi_controller.Stopped: view_config_stopped
    }
}

# Determine our initial view state based on the physical switch position
bc = view_map[board_controller.cpx.switch_is_left()][type(mc)].update_mode()
bc.update_pixels()

# Set garbage collection to only happen when explicitly triggered.
gc.disable()
gc.collect()
print("After object creation: " + str(gc.mem_free()))

# Flush any stray startup bytes out of the UART serial ring buffer
mc.midi.clear_msgs()

while True:
    # 1. High-Priority MIDI Parsing: Run multiple read iterations in a tight block
    for _ in config.ACTIVE_REPEATS:
        mc = mc.main()

    # 2. State-Machine Synchronization: Map views cleanly when transport changes happen
    # We dynamically fetch the current switch state to index into our nested grid layout
    if tm.midi_changed:
        bc = view_map[board_controller.cpx.switch_is_left()][type(mc)]
        tm.midi_changed = False

    # 3. Handle Board Input and Redraw Visual Elements
    bc = bc.update_mode()
    bc = bc.main()
