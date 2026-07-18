# PERFEC System Euclidian Sequencer
# minimal_midi.py
# copyright 2026, Tom Hoffman
# MIT License
# Very stripped down and MIDI processing. Only handles the messages we need, and only the data we need from those messages.
# Note that MinimalMidi uses 0-15 numbering for MIDI channels.
# Your MIDI device may display channels as 1-15,
# thus you may need to subtract 1 from the displayed value
# to match the value here.

import usb_midi
from micropython import const
import config

# Official MIDI Real-Time System Status Bytes
_CLOCK: bytes = const(b'\xF8')
_START: bytes = const(b'\xFA')
_CONTINUE: bytes = const(b'\xFB')
_STOP: bytes = const(b'\xFC')

_DATA_MSG_MASK: int = const(0b10000000)

# These "ports" are not to be confused with MIDI channels, etc.
_INNIE = usb_midi.ports[0]
_OUTIE = usb_midi.ports[1]

# Generates NoteOn/NoteOff message values indexed for each channel
NOTE_ON_MESSAGES: bytes = bytes(range(144, 160))
NOTE_OFF_MESSAGES: bytes = bytes(range(128, 144))
ALL_CHANNELS: range = range(0, 15)

class MinimalMidi(object):
    """Tightly implementing the subset of MIDI we need."""
    
    def __init__(self, in_channel: int, out_channel: int):
        self.in_channel: int = in_channel
        self.out_channel: int = out_channel
        
        # Micro-cache local performance pointers to hardware I/O routines
        self._readinto = _INNIE.readinto
        self._write = _OUTIE.write
        
        # Pre-allocate a mutable byte array buffer for outbound note actions
        self._note_buffer: bytearray = bytearray(3)
        
        # Pre-allocate static 1-byte mutable input buffer to prevent heap allocations on reads
        self._in_buf: bytearray = bytearray(1)

    def send_note_on(self, n: int, v: int) -> None:
        msgByte: int = NOTE_ON_MESSAGES[self.out_channel]
        # Overwrite the existing elements of the pre-allocated buffer 
        # instead of instantiating an immutable bytes object on the fly.
        self._note_buffer[0] = msgByte
        self._note_buffer[1] = n
        self._note_buffer[2] = v
        self._write(self._note_buffer)

    def send_note_off(self, n: int) -> None:
        msgByte: int = NOTE_OFF_MESSAGES[self.out_channel]
        self._note_buffer[0] = msgByte
        self._note_buffer[1] = n
        self._note_buffer[2] = 0
        self._write(self._note_buffer)

    def send_clock(self) -> None:
        self._write(_CLOCK)

    def clear_msgs(self) -> None:
        # Flush the buffer allocation-free using our input buffer slot
        while self._readinto(self._in_buf, 1):
            pass

    def get_msg(self) -> bytes:
        # Use readinto to drop a single incoming byte directly into our pre-allocated memory slot
        if not self._readinto(self._in_buf, 1):
            return None
            
        n: int = self._in_buf[0] # Fetch the integer byte value directly from the buffer
        
        if not(n & _DATA_MSG_MASK): # ditch stray data bytes quickly
            return None
            
        # Match strictly against MIDI real-time transport bytes.
        if n == 0xF8:    # _CLOCK
            return _CLOCK
        elif n == 0xFA:  # _START
            return _START
        elif n == 0xFC:  # _STOP
            return _STOP
        elif n == 0xFB:  # _CONTINUE
            return _CONTINUE
        else:
            return None
