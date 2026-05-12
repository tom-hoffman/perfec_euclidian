# PERFEC System Euclidian Sequencer
# board_controller.py
# copyright 2026, Tom Hoffman
# MIT License

# handles board input and output

import cpx

class View(object):
    '''This is the base class of all views.'''
    def __init__(self, model, pix=cpx.pix):
        self.model = model 
        self.pix = pix

    def main(self):
        self.check_buttons()
        if self.model.update_display:
            self.update_pixels()  
        return self

class SeqPlayingView(View):

    def update_mode(self):
        # Check the switch and return current mode.
        if cpx.switch_is_left():
            self.model.update_display = True
            return ConfigView(self.model, self.pix)
        else:
            return self

    def check_buttons(self):
        if cpx.a_button.went_down():
            self.model.add_step()
        elif cpx.b_button.went_down():
            self.model.add_trigger()

    def getRed(self, i):
        if i == self.model.active_step:
            return 96
        else:
            return 0

    def getGreen(self, i):
        if self.model.sequence[i]:
            return 48
        else:
            return 0

    def getBlue(self, i):
        # add velocity calculation
        return 16

    def update_pixels(self):
        # Re-draw the neopixels.
        for i in range(self.model.led_count):
            if i < len(self.model.sequence):
                cpx.pix[i] = (self.getRed(i), self.getGreen(i), self.getBlue(i))
            else:
                cpx.pix[i] = (0, 0, 0)
        self.model.update_display = False
        cpx.pix.show()  

class SeqStoppedView(SeqPlayingView):
    '''Sequence view while the clock has been stopped.'''
    def check_buttons(self):
        if cpx.a_button.went_down():
            self.model.add_rotation()
        elif cpx.b_button.went_down():
            self.model.sub_rotation()


class ConfigView(View):

    def check_buttons(self):
        if cpx.a_button.went_down():
            self.model.increment_note()
        elif cpx.b_button.went_down():
            self.model.increment_velocity()

    def update_mode(self):
        if cpx.switch_is_left():
            return self
        else:
            self.model.update_display = True
            self.model.midi_changed = True
            return SeqPlayingView(self.model, self.pix)    

    def display_note(self):
        for i in range(6):
            if i >= (6 - self.model.note_index):
                cpx.pix[i - 1] = (0, 0, 32)
            else:
                cpx.pix[i - 1] = (0, 0, 0)

    def display_velocity(self):
        for i in range(5, 10):
            if i <= (4 + self.model.velocity_index):
                cpx.pix[i] = (0, 32, 0)
            else:
                cpx.pix[i] = (0, 0, 0)

    def update_pixels(self):
        self.display_note()
        self.display_velocity()
        self.model.update_display = False
        self.pix.show()


