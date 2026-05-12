# PERFEC System Euclidian Sequencer
# midi_controller.py
# copyright 2026, Tom Hoffman
# MIT License

# Handle user and MIDI input/output

import config
import cpx

class MidiController(object):

    def __init__(self, model, midi, led=cpx.led):
        self.model = model
        self.midi = midi
        self.led = led

    def main(self):
        msg = self.midi.get_msg()
        if msg is not None:
            if msg['type'] == 'Clock':
                return self.clock()
            if msg['type'] == 'Start':
                self.model.midi_changed = True
                return Playing(self.model, self.midi)
            elif msg['type'] == 'Stop':
                self.model.midi_changed = True
                self.model.stop_reset()
                return Stopped(self.model, self.midi)
            else:
                return self
        else:
            return self


class Playing(MidiController):        
    def clock(self):
        '''Handle clock messages when the sequencer is playing.'''
        if self.model.clock_count == 0:
            self.led.value = not self.led.value
            if self.model.is_active_step():
                self.midi.send_note_on(config.NOTE_NUMBERS[self.model.note_index],
                                       config.VELOCITIES[self.model.velocity_index])
                cpx.out_pin.value = True
        elif self.model.clock_count == config.GATE_DURATION:
            cpx.out_pin.value = False
        self.model.increment_clock()
        return self

class Stopped(MidiController):
    def clock(self):
        return self

