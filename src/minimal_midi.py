# PERFEC System Euclidian Sequencer # midi_controller.py 
# copyright 2026, Tom Hoffman # MIT License

import usb_midi
from micropython import const

_CLOCK = const(0xF8)
_START = const(0xFA)
_CONTINUE = const(0xFB)
_STOP = const(0xFC)
_NOTE_ON_NYBBLE = const(0x9)
_NOTE_OFF_NYBBLE = const(0x8)

_INNIE = usb_midi.ports[0]
_OUTIE = usb_midi.ports[1]

class MinimalMidi(object):
    """Highly optimized, zero-allocation MIDI subset processor."""
    
    def __init__(self, in_channel, out_channel):
        self.in_channel = in_channel
        self.out_channel = out_channel
        
        # Pre-allocate static bytearrays to eliminate allocations during I/O
        self._out_buf3 = bytearray(3)
        self._out_buf1 = bytearray(1)
        self._in_buf = bytearray(1)
        
        # Pre-compute channel status bytes
        self._note_on_status = 144 + out_channel
        self._note_off_status = 128 + out_channel
        
        # Pre-allocated re-usable result dictionary to prevent GC thrashing
        self.msg_result = {'type': None, 'note': 0, 'velocity': 0}

    def send_note_on(self, n, v):
        buf = self._out_buf3
        buf[0] = self._note_on_status
        buf[1] = n
        buf[2] = v
        _OUTIE.write(buf)

    def send_note_off(self, n):
        buf = self._out_buf3
        buf[0] = self._note_off_status
        buf[1] = n
        buf[2] = 0
        _OUTIE.write(buf)

    def send_clock(self):
        buf = self._out_buf1
        buf[0] = _CLOCK
        _OUTIE.write(buf)

    def clear_msgs(self):
        buf = self._in_buf
        while _INNIE.readinto(buf, 1):
            pass

    def get_msg(self):
        buf = self._in_buf
        if not _INNIE.readinto(buf, 1):
            return None
            
        n = buf[0]
        
        # Real-time messages (Clock, Start, Stop, Continue)
        if n >= 0xF8:
            res = self.msg_result
            res['note'] = 0
            res['velocity'] = 0
            if n == _CLOCK:
                res['type'] = 'Clock'
            elif n == _START:
                res['type'] = 'Start'
            elif n == _STOP:
                res['type'] = 'Stop'
            elif n == _CONTINUE:
                res['type'] = 'Continue'
            else:
                return None
            return res

        # Status byte validation (Must have MSB set)
        if n < 0x80:
            return None

        # Channel voice messages
        nybble = n >> 4
        if nybble == _NOTE_ON_NYBBLE:
            if _INNIE.readinto(buf, 1):
                note = buf[0]
                if _INNIE.readinto(buf, 1):
                    res = self.msg_result
                    res['type'] = 'NoteOn'
                    res['note'] = note
                    res['velocity'] = buf[0]
                    return res
        elif nybble == _NOTE_OFF_NYBBLE:
            if _INNIE.readinto(buf, 1):
                note = buf[0]
                if _INNIE.readinto(buf, 1):
                    res = self.msg_result
                    res['type'] = 'NoteOff'
                    res['note'] = note
                    res['velocity'] = buf[0]
                    return res
                    
        return None
