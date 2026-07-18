# PERFEC System Euclidian Sequencer
# model.py
# copyright 2026, Tom Hoffman
# MIT License

import config
import math

def gen_mask(n: int, acc: int) -> int:
    # generates a bitmask for n bits
    if n == 1:
        return acc + 1
    else:
        return gen_mask(n - 1, acc + (2 ** (n - 1)))

class SequenceModel(object):
    def __init__(self, 
                 note_index: int, 
                 note_tuple: tuple, 
                 steps: int = config.DEFAULT_STEPS, 
                 triggers: int = config.DEFAULT_TRIGGERS, 
                 led_count: int = 9, 
                 rotation: int = config.DEFAULT_ROTATION,
                 channel_out: int = config.CHANNEL_OUT):
        self.note_index: int = note_index
        self.note_tuple: tuple = note_tuple
        self.steps: int = steps
        self.triggers: int = triggers
        self.rotation: int = rotation
        self.channel_out: int = channel_out
        
        # Pre-allocate a mutable bytearray to store step states allocation-free
        # True steps map to 1, False steps map to 0
        self.sequence: bytearray = bytearray(led_count)
        
        self.active_step: int = 0
        self.velocity_index: int = config.DEFAULT_VELOCITY
        
        # Tracks the user selected index (0-4) for the active gate ratio duration
        self.gate_duration_index: int = config.GATE_DURATION_INDEX
        
        self.clock_count: int = 0
        self.update_display: bool = True
        self.midi_changed: bool = True
        self.led_count: int = led_count

    def generate(self) -> None:
        '''
        Generates a "Euclidian rhythm" where triggers are evenly distributed over a given number of steps.
        '''
        # Clear out our pre-allocated array up to the active step boundary without instantiating new lists
        for i in range(self.steps):
            self.sequence[i] = 0

        if self.triggers > 0:
            # Replicating your original math exactly, but using pure integer floor division (//)
            # to remain allocation-free and avoid CircuitPython floating-point errors.
            previous = -1  # Initialize to -1 so the very first step (0) always calculates as a change/trigger
            
            for i in range(self.steps):
                current = (i * self.triggers) // self.steps
                
                if current != previous:
                    is_trigger = 1
                else:
                    is_trigger = 0
                    
                previous = current
                
                # Apply the user-first rotation shift cleanly using our modulo bounds
                rotated_idx: int = (i + self.rotation) % self.steps
                self.sequence[rotated_idx] = is_trigger
                
        self.update_display = True



    def increment_channel(self) -> None:
        '''Advances through MIDI channels 0-15 smoothly, wrapping back to 0.'''
        self.channel_out = (self.channel_out + 1) % 16
        self.update_display = True

    def increment_note(self) -> None:
        self.note_index = (self.note_index + 1) % len(self.note_tuple)
        self.update_display = True

    def increment_clock(self) -> None:
        self.clock_count += 1
        if self.clock_count >= config.PPQN:
            # Use self.steps directly for modulo instead of invoking len()
            self.active_step = (self.active_step + 1) % self.steps
            self.update_display = True
            self.clock_count = 0

    def get_gate_pulses(self) -> int:
        '''
        Calculates the active gate duration in raw clock pulses.
        Uses pure integer percentage math: (PPQN * ratio) // 100
        '''
        return (config.PPQN * config.GATE_RATIOS[self.gate_duration_index]) // 100

    def is_active_step(self) -> bool:
        # Evaluate integer mapping cleanly (1 acts as True, 0 acts as False)
        return self.sequence[self.active_step] == 1

    def stop_reset(self) -> None:
        self.reset_clock()
        self.active_step = 0
        self.update_display = True
        self.midi_changed = True

    def reset_clock(self) -> None:
        self.clock_count = 0

    def triggered(self) -> int:
        return 1 & self.seq

    def add_step(self) -> None:
        if self.steps < self.led_count:
            self.steps += 1
        else:
            self.steps = 1
        self.triggers = 0
        self.active_step = 0
        self.generate()

    def add_trigger(self) -> None:
        if self.triggers < self.steps:
            self.triggers += 1
        else:
            self.triggers = 0
        self.generate()

    def add_rotation(self) -> None:
        self.rotation = (self.rotation + 1) % self.steps
        self.generate()

    def sub_rotation(self) -> None:
        self.rotation -= 1
        if self.rotation < 0:
            self.rotation = self.steps - 1
        self.generate()

    def increment_velocity(self) -> None:
        self.velocity_index = (self.velocity_index + 1) % len(config.VELOCITIES)
        self.update_display = True

    def increment_gate(self) -> None:
        '''Advances through our 5 available gate durations smoothly.'''
        self.gate_duration_index = (self.gate_duration_index + 1) % len(config.GATE_RATIOS)
        self.update_display = True
