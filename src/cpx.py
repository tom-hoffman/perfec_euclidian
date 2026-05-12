# PERFEC System Euclidian Sequencer
# cpx.py
# copyright 2026, Tom Hoffman
# MIT License

# Set up board hardware and simple button Debouncer.

import board            # helps set up pins, etc. on the board
import digitalio        # digital (on/off) output to pins, including board LED.
import neopixel         # controls the RGB LEDs on the board

class Debouncer(object):

    def __init__(self, b, current_value=None):
        self.b = b
        if current_value is None:
            self.current_value = b.value
        else:
            self.current_value = current_value

    def went_down(self):
        new = self.b.value
        changed = new and (not self.current_value)
        self.current_value = new
        return changed
        
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT
led.value = True

a_button_raw = digitalio.DigitalInOut(board.BUTTON_A)
a_button_raw.direction = digitalio.Direction.INPUT
a_button_raw.pull = digitalio.Pull.DOWN
a_button = Debouncer(a_button_raw)

b_button_raw = digitalio.DigitalInOut(board.BUTTON_B)
b_button_raw.direction = digitalio.Direction.INPUT
b_button_raw.pull = digitalio.Pull.DOWN
b_button = Debouncer(b_button_raw) 

switch = digitalio.DigitalInOut(board.SLIDE_SWITCH)
switch.direction = digitalio.Direction.INPUT
switch.pull = digitalio.Pull.UP

out_pin = digitalio.DigitalInOut(board.D10)
out_pin.direction = digitalio.Direction.OUTPUT

def switch_is_left():
    return switch.value

pix = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=0.2, auto_write=False)
