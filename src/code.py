# PERFEC System Euclidian Sequencer # code.py 
# copyright 2026, Tom Hoffman # MIT License

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
tm = SequenceModel(config.DEFAULT_NOTE, config.NOTE_NUMBERS, led_count=led_count)
tm.generate()

mc = midi_controller.Playing(tm, MinimalMidi(None, config.channel_out))

# Pre-instantiate both views to prevent continuous garbage collection pauses
view_playing = board_controller.SeqPlayingView(tm)
view_stopped = board_controller.SeqStoppedView(tm)
view_config = board_controller.ConfigView(tm) # Instantiated once at startup

# Set initial state
bc = view_playing.update_mode()
bc.update_pixels()
print("After object creation: " + str(gc.mem_free()))

mc.midi.clear_msgs()

# Cache global configuration lookup and direct methods locally to bypass dictionary lookups
MIDI_READ_REPEAT = config.MIDI_READ_REPEAT
playing_class = midi_controller.Playing

# Cache view states into a fast list lookup rather than using 'isinstance'
# Index 0: Stopped, Index 1: Playing
views = [view_stopped, view_playing]

while True:
    # 1. High-speed MIDI parsing burst
    for _ in range(MIDI_READ_REPEAT):
        mc = mc.main()
        
    # 2. Optimized conditional state check
    if tm.midi_changed:
        # Determine view state based on type match without allocating memory
        is_playing = 1 if (mc.__class__ is playing_class) else 0
        bc = views[is_playing]
        tm.midi_changed = False
        
    # 3. Hardware UI refresh
    bc = bc.update_mode()
    bc = bc.main()
