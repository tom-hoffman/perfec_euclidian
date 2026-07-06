# PERFEC System Euclidian Sequencer # midi_controller.py 
# copyright 2026, Tom Hoffman # MIT License

import config
import cpx

_OUT_PIN = cpx.out_pin
_LED = cpx.led
_NOTE_NUMBERS = config.NOTE_NUMBERS
_VELOCITIES = config.VELOCITIES
_GATE_DURATION = config.GATE_DURATION

class MidiController(object):
    def __init__(self, model, midi, led=_LED):
        self.model = model
        self.midi = midi
        self.led = led
        self._midi_get_msg = midi.get_msg
        self._model_increment_clock = model.increment_clock

    def main(self):
        msg = self._midi_get_msg()
        if msg is None:
            return self
            
        m_type = msg['type']
        if m_type == 'Clock':
            return self.clock()
        elif m_type == 'Start':
            self.model.midi_changed = True
            if self.__class__ is Playing:
                return self
            return Playing(self.model, self.midi, self.led)
        elif m_type == 'Stop':
            self.model.midi_changed = True
            self.model.stop_reset()
            if self.__class__ is Stopped:
                return self
            return Stopped(self.model, self.midi, self.led)
            
        return self

class Playing(MidiController):
    def __init__(self, model, midi, led=_LED):
        super().__init__(model, midi, led)
        self._midi_send_note_on = midi.send_note_on
        self._model_is_active_step = model.is_active_step

    def clock(self):
        '''Handle clock messages when the sequencer is playing.'''
        model = self.model
        ccount = model.clock_count
        
        if ccount == 0:
            # Clean, direct hardware inversion execution path
            self.led.value = not self.led.value
            if self._model_is_active_step():
                self._midi_send_note_on(_NOTE_NUMBERS[model.note_index], _VELOCITIES[model.velocity_index])
                _OUT_PIN.value = True
        elif ccount == _GATE_DURATION:
            _OUT_PIN.value = False
            
        self._model_increment_clock()
        return self

class Stopped(MidiController):
    def clock(self):
        return self
