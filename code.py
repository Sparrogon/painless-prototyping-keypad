import time
import board
import digitalio
import adafruit_matrixkeypad
import usb_hid
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control_code import ConsumerControlCode

keys = (
    (0,1,2),
    (3,4,5),
)

KEYS = [
    ConsumerControlCode.MUTE,
    ConsumerControlCode.PLAY_PAUSE,
    ConsumerControlCode.VOLUME_INCREMENT,
    [Keycode.CONTROL, Keycode.C],
    [Keycode.CONTROL, Keycode.V],
    ConsumerControlCode.VOLUME_DECREMENT,
]


time.sleep(1)  # Sleep for a bit to avoid a race condition on some systems
cc = ConsumerControl(usb_hid.devices)
kbd = Keyboard(usb_hid.devices)
cols = [digitalio.DigitalInOut(x) for x in (board.D11, board.D12, board.D13)]
rows = [digitalio.DigitalInOut(x) for x in (board.D9, board.D10)]
keypad = adafruit_matrixkeypad.Matrix_Keypad(rows, cols, keys)

# This dict is just for being able to tell if a keycode is a cc code or normal code,
# to be able to send to the proper device (cc or kbd)
CONSUMER_CONTROL_CODES = {
    ConsumerControlCode.BRIGHTNESS_DECREMENT: 1,
    ConsumerControlCode.BRIGHTNESS_INCREMENT: 1,
    ConsumerControlCode.EJECT: 1,
    ConsumerControlCode.FAST_FORWARD: 1,
    ConsumerControlCode.MUTE: 1,
    ConsumerControlCode.PLAY_PAUSE: 1,
    ConsumerControlCode.RECORD: 1,
    ConsumerControlCode.REWIND: 1,
    ConsumerControlCode.SCAN_NEXT_TRACK: 1,
    ConsumerControlCode.SCAN_PREVIOUS_TRACK: 1,
    ConsumerControlCode.STOP: 1,
    ConsumerControlCode.VOLUME_DECREMENT: 1,
    ConsumerControlCode.VOLUME_INCREMENT: 1,
}

last_keys = []

while True:
    keys = keypad.pressed_keys
    added_keys = list(set(keys) - set(last_keys))
    removed_keys = list(set(last_keys) - set(keys))
    for key in added_keys:
        keycode = KEYS[key]
        is_list = isinstance(keycode, list)
        if not is_list and CONSUMER_CONTROL_CODES.get(keycode):
            cc.press(keycode)
        else:
            kbd.press(*keycode) if is_list else kbd.press(keycode)
    for key in removed_keys:
        keycode = KEYS[key]
        is_list = isinstance(keycode, list)
        if not is_list and CONSUMER_CONTROL_CODES.get(keycode):
            cc.release()
        else:
            kbd.release(*keycode) if is_list else kbd.release(keycode)
    last_keys = keys
