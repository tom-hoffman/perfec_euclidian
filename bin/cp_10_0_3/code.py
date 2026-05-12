# PERFEC System Euclidian Sequencer
# code.py
# copyright 2026, Tom Hoffman
# MIT License

# This module contains the main loop of the application.


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

led_count = 10

tm = SequenceModel(config.note, config.NOTE_NUMBERS, led_count=led_count)
tm.generate()

mc = midi_controller.Playing(tm, MinimalMidi(None, config.channel_out))

bc = board_controller.SeqPlayingView(tm).update_mode()
bc.update_pixels()
print("After object creation: " + str(gc.mem_free()))

def update_board(m, b):
    if isinstance(m, midi_controller.Playing):
        return board_controller.SeqPlayingView(b.model)
    elif isinstance(m, midi_controller.Stopped):
        return board_controller.SeqStoppedView(b.model)

mc.midi.clear_msgs()
bc = update_board(mc, bc)

while True:
    for i in range(config.MIDI_READ_REPEAT):
        mc = mc.main()
    if tm.midi_changed:
        bc = update_board(mc, bc)
        tm.midi_changed = False
    bc = bc.update_mode()
    bc = bc.main()
