# PERFEC System Euclidian Sequencer
# board_controller.py
# copyright 2026, Tom Hoffman
# MIT License
# handles board input and output

import cpx
import config

class View(object):
    '''This is the base class of all views.'''
    def __init__(self, model, pix=cpx.pix):
        self.model = model
        self.pix = pix

    def main(self) -> "View":
        self.check_buttons()
        if self.model.update_display:
            self.update_pixels()
        return self

    def check_buttons(self) -> None:
        pass

    def update_pixels(self) -> None:
        pass

class SeqPlayingView(View):
    def update_mode(self) -> "View":
        # Check the switch and route to ConfigPlayingView if flipped left
        if cpx.switch_is_left():
            self.model.update_display = True
            return ConfigPlayingView(self.model, self.pix)
        else:
            return self

    def check_buttons(self) -> None:
        if cpx.a_button.went_down():
            self.model.add_step()
        elif cpx.b_button.went_down():
            self.model.add_trigger()

    def update_pixels(self) -> None:
        active: int = self.model.active_step
        total_steps: int = self.model.steps
        seq_data = self.model.sequence

        for i in range(self.model.led_count):
            if i < total_steps:
                if i == active:
                    r = 96
                else:
                    r = 0
                    
                if seq_data[i] == 1:
                    g = 48
                else:
                    g = 0
                    
                b = 16  # add velocity calculation
                cpx.pix[i] = (r, g, b)
            else:
                cpx.pix[i] = (0, 0, 0)

        self.model.update_display = False
        cpx.pix.show()

class SeqStoppedView(SeqPlayingView):
    '''Sequence view while the clock has been stopped.'''
    def update_mode(self) -> "View":
        # Check the switch and route to ConfigStoppedView if flipped left
        if cpx.switch_is_left():
            self.model.update_display = True
            return ConfigStoppedView(self.model, self.pix)
        else:
            return self

    def check_buttons(self) -> None:
        if cpx.a_button.went_down():
            self.model.add_rotation()
        elif cpx.b_button.went_down():
            self.model.sub_rotation()

class ConfigView(View):
    '''Base configuration layout handling shared display graphics.'''
    def display_velocity(self) -> None:
        # Standard green display tracking on the right half of the ring (LEDs 5-9)
        idx: int = self.model.velocity_index
        for i in range(5, 10):
            if i <= (4 + idx):
                cpx.pix[i] = (0, 32, 0)
            else:
                cpx.pix[i] = (0, 0, 0)

class ConfigPlayingView(ConfigView):
    '''Configuration view entered while the master clock is active.'''
    def check_buttons(self) -> None:
        if cpx.a_button.went_down():
            # Button A now increments our dynamic gate duration percentage
            self.model.increment_gate()
        elif cpx.b_button.went_down():
            self.model.increment_velocity()

    def update_mode(self) -> "View":
        if cpx.switch_is_left():
            return self
        else:
            self.model.update_display = True
            self.model.midi_changed = True
            return SeqPlayingView(self.model, self.pix)

    def display_gate(self) -> None:
        # Upward-growing blue gate tracker on the left half of the ring (LEDs 4 down to 0)
        idx: int = self.model.gate_duration_index
        for i in range(5):
            if i <= idx:
                cpx.pix[4 - i] = (0, 0, 32)
            else:
                cpx.pix[4 - i] = (0, 0, 0)

    def update_pixels(self) -> None:
        self.display_gate()
        self.display_velocity()
        self.model.update_display = False
        self.pix.show()

class ConfigStoppedView(ConfigView):
    '''Configuration view entered while the master clock is stopped.'''
    def check_buttons(self) -> None:
        if cpx.a_button.went_down():
            self.model.increment_note()
        elif cpx.b_button.went_down():
            # Button B now advances the raw binary MIDI channel selection!
            self.model.increment_channel()

    def update_mode(self) -> "View":
        if cpx.switch_is_left():
            return self
        else:
            self.model.update_display = True
            self.model.midi_changed = True
            return SeqStoppedView(self.model, self.pix)

    def display_note(self) -> None:
        # Upward-growing violet note index tracker on the left half of the ring (LEDs 4 down to 0)
        idx: int = self.model.note_index
        for i in range(5):
            if i <= idx:
                cpx.pix[4 - i] = (32, 0, 32)
            else:
                cpx.pix[4 - i] = (0, 0, 0)

    def display_channel(self) -> None:
        '''Uses a four bit binary number to display the active channel layout on LEDs 5-8.'''
        # Read directly from the live model state tracker
        n: int = self.model.channel_out
        
        # Explicit 4-bit index walk for students (evaluating bit 0 through bit 3)
        for i in range(4):
            # Bitwise check: if the bit at 2^i position is high (1)
            if n & (1 << i):
                # Bright Yellow/Amber color (Green + Red) representing 1
                cpx.pix[5 + i] = (32, 32, 0)
            else:
                # Dim White/Purple representing 0
                cpx.pix[5 + i] = (8, 8, 8)
                
        # Turn the remaining last pixel (LED 9) completely off to preserve the 4-bit UI boundary
        cpx.pix[9] = (0, 0, 0)

    def update_pixels(self) -> None:
        self.display_note()
        self.display_channel()
        self.model.update_display = False
        self.pix.show()
