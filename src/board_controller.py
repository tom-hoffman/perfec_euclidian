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
        if cpx.switch_is_left():
            self.model.update_display = True
            return ConfigStoppedView(self.model, self.pix)
        return self

    def check_buttons(self) -> None:
        if cpx.a_button.went_down():
            self.model.add_rotation()
        elif cpx.b_button.went_down():
            self.model.sub_rotation()

class ConfigPlayingView(View):
    '''Configuration view entered while the master clock is active.'''
    def check_buttons(self) -> None:
        if cpx.a_button.went_down():
            # Button A increments the left-side attribute (Velocity)
            self.model.increment_velocity()
        elif cpx.b_button.went_down():
            # Button B increments the right-side attribute (Gate)
            self.model.increment_gate()

    def update_mode(self) -> "View":
        if cpx.switch_is_left():
            return self
        else:
            self.model.update_display = True
            self.model.midi_changed = True
            return SeqPlayingView(self.model, self.pix)

    def display_velocity(self) -> None:
        # Upward-growing Blue velocity tracker handling 6 options (0 to 5 LEDs lit)
        idx: int = self.model.velocity_index
        for i in range(5):
            if i < idx:
                cpx.pix[4 - i] = (0, 0, 32)
            else:
                cpx.pix[4 - i] = (0, 0, 0)

    def display_gate(self) -> None:
        # Green gate duration tracker on the right half of the ring (LEDs 5 to 9) [Mnemonic: Green=Gate]
        idx: int = self.model.gate_duration_index
        for i in range(5):
            if i <= idx:
                cpx.pix[5 + i] = (0, 32, 0)
            else:
                cpx.pix[5 + i] = (0, 0, 0)

    def update_pixels(self) -> None:
        self.display_velocity()
        self.display_gate()
        self.model.update_display = False
        self.pix.show()

class ConfigStoppedView(View):
    '''Configuration view entered while the master clock is stopped.'''
    def check_buttons(self) -> None:
        if cpx.a_button.went_down():
            self.model.increment_note()
        elif cpx.b_button.went_down():
            # Button B increments through our available PPQN values
            self.model.increment_ppqn()

    def update_mode(self) -> "View":
        if cpx.switch_is_left():
            return self
        else:
            self.model.update_display = True
            self.model.midi_changed = True
            return SeqStoppedView(self.model, self.pix)

    def display_note(self) -> None:
        # Upward-growing violet note tracker handling 6 options (0 to 5 LEDs lit)
        idx: int = self.model.note_index
        for i in range(5):
            if i < idx:
                cpx.pix[4 - i] = (32, 0, 32)
            else:
                cpx.pix[4 - i] = (0, 0, 0)

    def display_ppqn(self) -> None:
        # Standard yellow (Red + Green) tracker on the right half of the ring (LEDs 5-9)
        idx: int = self.model.ppqn_index
        for i in range(5):
            if i <= idx:
                cpx.pix[5 + i] = (32, 32, 0)
            else:
                cpx.pix[5 + i] = (0, 0, 0)

    def update_pixels(self) -> None:
        self.display_note()
        self.display_ppqn()
        self.model.update_display = False
        self.pix.show()
