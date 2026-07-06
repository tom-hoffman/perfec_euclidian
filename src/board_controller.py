# PERFEC System Euclidian Sequencer # board_controller.py 
# copyright 2026, Tom Hoffman # MIT License

import cpx

# Cache reference hooks directly to bypass multi-level property dictionary lookups
_PIX = cpx.pix
_A_BUTTON = cpx.a_button
_B_BUTTON = cpx.b_button
_SWITCH_IS_LEFT = cpx.switch_is_left

class View(object):
    '''This is the base class of all views.'''
    def __init__(self, model, pix=_PIX):
        self.model = model
        self.pix = pix
        
        # Pre-cache tracking attributes
        self._model_check_buttons = self.check_buttons
        self._model_update_pixels = self.update_pixels

    def main(self):
        self._model_check_buttons()
        if self.model.update_display:
            self._model_update_pixels()
        return self

class SeqPlayingView(View):
    def update_mode(self):
        if _SWITCH_IS_LEFT():
            self.model.update_display = True
            # Fetch globally cached views from code.py structure if possible, 
            # otherwise fall back to direct instantiation
            return view_config if 'view_config' in globals() else ConfigView(self.model, self.pix)
        return self

    def check_buttons(self):
        if _A_BUTTON.went_down():
            self.model.add_step()
        elif _B_BUTTON.went_down():
            self.model.add_trigger()

    def update_pixels(self):
        # Localize properties to maximize for-loop throughput
        model = self.model
        seq = model.sequence
        seq_len = len(seq)
        active = model.active_step
        pix = self.pix
        
        # Write directly to array indices instead of stacking 3 separate function helper calls
        for i in range(model.led_count):
            if i < seq_len:
                # Optimized color assignment blocks with zero call stack overhead
                r = 96 if (i == active) else 0
                g = 48 if seq[i] else 0
                pix[i] = (r, g, 16)
            else:
                pix[i] = (0, 0, 0)
                
        model.update_display = False
        pix.show()

class SeqStoppedView(SeqPlayingView):
    '''Sequence view while the clock has been stopped.'''
    def check_buttons(self):
        if _A_BUTTON.went_down():
            self.model.add_rotation()
        elif _B_BUTTON.went_down():
            self.model.sub_rotation()

class ConfigView(View):
    def check_buttons(self):
        if _A_BUTTON.went_down():
            self.model.increment_note()
        elif _B_BUTTON.went_down():
            self.model.increment_velocity()

    def update_mode(self):
        if _SWITCH_IS_LEFT():
            return self
        self.model.update_display = True
        self.model.midi_changed = True
        return view_playing if 'view_playing' in globals() else SeqPlayingView(self.model, self.pix)

    def update_pixels(self):
        model = self.model
        pix = self.pix
        note_idx = model.note_index
        vel_idx = model.velocity_index

        # Collapsed display_note() and display_velocity() into a unified, single pass 
        # for-loop to write all pixels simultaneously before initiating a hardware show()
        for i in range(6):
            # Combined index correction arithmetic into flat comparisons
            pix[i - 1] = (0, 0, 32) if (i >= (6 - note_idx)) else (0, 0, 0)
            
        for i in range(5, 10):
            pix[i] = (0, 32, 0) if (i <= (4 + vel_idx)) else (0, 0, 0)

        model.update_display = False
        pix.show()
