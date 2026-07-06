# PERFEC System Euclidian Sequencer # model.py 
# copyright 2026, Tom Hoffman # MIT License

import config

# Cache constant global lookups locally to eliminate module dictionary overhead
_PPQN = config.PPQN
_VELOCITIES_LEN = len(config.VELOCITIES)

def gen_mask(n, acc):
    # Replaced recursion with a highly efficient iterative loop to prevent call stack overhead
    while n > 1:
        acc += (1 << (n - 1))  # Use rapid bit-shifting instead of slow exponentiation (2 ** x)
        n -= 1
    return acc + 1

class SequenceModel(object):
    def __init__(self, note_index, note_tuple, steps=config.DEFAULT_STEPS, triggers=config.DEFAULT_TRIGGERS, led_count=9, rotation=config.DEFAULT_ROTATION):
        self.note_index = note_index
        self.note_tuple = note_tuple
        self.steps = steps
        self.triggers = triggers
        self.rotation = rotation
        self.sequence = [False] * steps
        self.active_step = 0
        self.velocity_index = config.DEFAULT_VELOCITY
        self.clock_count = 0
        self.update_display = True
        self.midi_changed = True
        self.led_count = led_count
        
        # Pre-cache internal constants and structure lengths
        self._note_tuple_len = len(note_tuple)

    def generate(self):
        '''Generates a "Euclidian rhythm" using high-speed integer arithmetic.'''
        steps = self.steps
        triggers = self.triggers
        
        if triggers == 0:
            self.sequence = [False] * steps
        else:
            # Replaced floating-point multiplication and math.floor with fast integer math.
            # (i * triggers) // steps removes floats and eliminates the 0.001 adjustment hack entirely.
            result = [False] * steps
            previous = -1
            for i in range(steps):
                current = (i * triggers) // steps
                if current != previous:
                    result[i] = True
                    previous = current
            
            # Fast slice rotation
            rot = self.rotation
            self.sequence = result[rot:] + result[:rot]
            
        self.update_display = True

    def increment_note(self):
        self.note_index = (self.note_index + 1) % self._note_tuple_len
        self.update_display = True

    def increment_clock(self):
        '''Highly optimized time-critical execution path.'''
        # Increment clock counter directly
        cc = self.clock_count + 1
        
        if cc >= _PPQN:
            # Advance step and use fast sequence boundary rollover
            step = self.active_step + 1
            if step >= len(self.sequence):
                step = 0
            self.active_step = step
            self.update_display = True
            self.clock_count = 0
        else:
            self.clock_count = cc

    def is_active_step(self):
        return self.sequence[self.active_step]

    def stop_reset(self):
        self.clock_count = 0
        self.active_step = 0
        self.update_display = True
        self.midi_changed = True

    def reset_clock(self):
        self.clock_count = 0

    def triggered(self):
        return 1 & self.seq

    def add_step(self):
        self.steps = (self.steps + 1) if (self.steps < self.led_count) else 1
        self.triggers = 0
        self.active_step = 0
        self.generate()

    def add_trigger(self):
        self.triggers = (self.triggers + 1) if (self.triggers < self.steps) else 0
        self.generate()

    def add_rotation(self):
        self.rotation = (self.rotation + 1) % self.steps
        self.generate()

    def sub_rotation(self):
        rot = self.rotation - 1
        self.rotation = (self.steps - 1) if (rot < 0) else rot
        self.generate()

    def increment_velocity(self):
        self.velocity_index = (self.velocity_index + 1) % _VELOCITIES_LEN
        self.update_display = True
