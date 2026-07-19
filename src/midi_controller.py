# PERFEC System Euclidian Sequencer
# midi_controller.py
# copyright 2026, Tom Hoffman
# MIT License
# Handle user and MIDI input/output

import gc
import config
import cpx
from minimal_midi import MinimalMidi

# Import real-time status bytes and channel arrays directly from our minimal module
from minimal_midi import _CLOCK, _START, _STOP, NOTE_ON_MESSAGES, NOTE_OFF_MESSAGES

class MidiController(object):
    def __init__(self, model, midi: MinimalMidi, led=cpx.led):
        self.model = model
        self.midi: MinimalMidi = midi
        self.led = led
        # Track globally across state transitions if a voice is active
        self.note_is_open: bool = False
        # Store the active sounding note number to guarantee accurate NoteOff routing
        self.active_note_num: int = 0

    def _send_note(self, status_byte: int, note_num: int, velocity: int) -> None:
        '''Fills and writes to the pre-allocated mutable note buffer allocation-free.'''
        self.midi._note_buffer[0] = status_byte
        self.midi._note_buffer[1] = note_num
        self.midi._note_buffer[2] = velocity
        self.midi._write(self.midi._note_buffer)

    def main(self) -> "MidiController":
        msg: bytes = self.midi.get_msg()
        if msg is not None:
            # High school lesson reinforce: directly evaluate the official raw hex byte
            if msg == _CLOCK:
                return self.clock()
            elif msg == _START:
                self.model.midi_changed = True
                return Playing(self.model, self.midi)
            elif msg == _STOP:
                # If a note is actively left hanging open when the song stops,
                # immediately clamp the hardware pins and issue an explicit MIDI NoteOff.
                if self.note_is_open:
                    cpx.out_pin.value = False
                    self._send_note(NOTE_OFF_MESSAGES[config.CHANNEL_OUT],
                                    self.active_note_num,
                                    0)
                    self.note_is_open = False

                self.model.midi_changed = True
                self.model.stop_reset()
                return Stopped(self.model, self.midi)
            else:
                return self
        else:
            return self

class Playing(MidiController):
    def __init__(self, model, midi: MinimalMidi, led=cpx.led):
        super().__init__(model, midi, led)
        self.note_is_open: bool = False

    def clock(self) -> "MidiController":
        '''Handle clock messages when the sequencer is playing.'''
        # If we are starting a fresh step (0) but a previous step left a note hanging open,
        # cleanly turn it off right here using its original note number before anything else executes.
        if self.model.clock_count == 0 and self.note_is_open:
            cpx.out_pin.value = False
            self._send_note(NOTE_OFF_MESSAGES[config.CHANNEL_OUT],
                            self.active_note_num,
                            0)
            self.note_is_open = False

        # Proceed with normal step tracking
        if self.model.clock_count == 0:
            self.led.value = not self.led.value
            if self.model.is_active_step():
                # Cache the note number we are actively triggering
                self.active_note_num = config.NOTE_NUMBERS[self.model.note_index]
                
                self._send_note(NOTE_ON_MESSAGES[config.CHANNEL_OUT],
                                self.active_note_num, 
                                config.VELOCITIES[self.model.velocity_index])
                cpx.out_pin.value = True
                self.note_is_open = True
                
        # Standard sub-100% gate window matches
        elif self.model.clock_count == self.model.get_gate_pulses():
            cpx.out_pin.value = False
            if self.note_is_open:
                self._send_note(NOTE_OFF_MESSAGES[config.CHANNEL_OUT],
                    self.active_note_num, 
                    0)
                self.note_is_open = False
            
        self.model.increment_clock()
        gc.collect()
        return self

class Stopped(MidiController):
    def clock(self) -> "MidiController":
        gc.collect()
        return self
