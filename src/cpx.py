# PERFEC System Euclidian Sequencer # cpx.py 
# copyright 2026, Tom Hoffman # MIT License

import board
import digitalio
import neopixel

class Debouncer(object):
    def __init__(self, b):
        self.b = b
        self.current_value = b.value

    def went_down(self):
        old = self.current_value
        new = self.b.value
        self.current_value = new
        return new and not old

# Clean, direct hardware mapping to the red LED via pin D13
led = digitalio.DigitalInOut(board.D13)
led.direction = digitalio.Direction.OUTPUT
led.value = True

# Initialize Buttons & Switch
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

switch_is_left = lambda: switch.value
pix = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=0.2, auto_write=False)
