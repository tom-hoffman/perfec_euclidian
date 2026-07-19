# PERFEC System Euclidian Sequencer
# model.py
# copyright 2026, Tom Hoffman
# MIT License

import config

class SequenceModel(object):
    def __init__(self, note_index: int, note_tuple: tuple):
        self.note_index: int = note_index
        self.note_tuple: tuple = note_tuple
        self.steps: int = config.DEFAULT_STEPS
        self.triggers: int = config.DEFAULT_TRIGGERS
        self.rotation: int = config.DEFAULT_ROTATION        
        self.active_step: int = 0
        self.velocity_index: int = config.DEFAULT_VELOCITY
        self.gate_duration_index: int = config.GATE_DURATION_INDEX
        self.ppqn_index: int = config.DEFAULT_PPQN_INDEX
        self.clock_count: int = 0
        self.update_display: bool = True
        self.midi_changed: bool = True
        self.led_count: int = 10
        # Pre-allocate a mutable bytearray to store step states allocation-free
        # True steps map to 1, False steps map to 0
        self.sequence: bytearray = bytearray(self.led_count)

    def generate(self) -> None:
        '''
        Generates a "Euclidian rhythm" where triggers are evenly distributed over a given number of steps.
        '''
        # clear the sequence.
        for i in range(self.steps):
            self.sequence[i] = 0
        if self.triggers > 0:
            previous = -1
            for i in range(self.steps):
                current = (i * self.triggers) // self.steps
                if current != previous:
                    is_trigger = 1
                else:
                    is_trigger = 0
                previous = current
                rotated_idx: int = (i + self.rotation) % self.steps
                self.sequence[rotated_idx] = is_trigger
        self.update_display = True

    def increment_note(self) -> None:
        self.note_index = (self.note_index + 1) % len(self.note_tuple)
        self.update_display = True

    def increment_clock(self) -> None:
        self.clock_count += 1
        # Read active PPQN value dynamically from config based on our model index selection
        if self.clock_count >= config.PPQN_VALUES[self.ppqn_index]:
            self.active_step = (self.active_step + 1) % self.steps
            self.update_display = True
            self.clock_count = 0

    def get_gate_pulses(self) -> int:
        '''
        Calculates the active gate duration in raw clock pulses.
        Uses pure integer percentage math: (PPQN * ratio) // 100
        '''
        active_ppqn: int = config.PPQN_VALUES[self.ppqn_index]
        return (active_ppqn * config.GATE_RATIOS[self.gate_duration_index]) // 100

    def is_active_step(self) -> bool:
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

    def increment_ppqn(self) -> None:
        '''Advances through our 5 available PPQN speeds smoothly, wrapping back to 0.'''
        self.ppqn_index = (self.ppqn_index + 1) % len(config.PPQN_VALUES)
        self.update_display = True
