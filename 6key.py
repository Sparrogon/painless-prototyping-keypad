import time
import board
import digitalio
import adafruit_matrixkeypad
import adafruit_dotstar
import usb_hid
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control_code import ConsumerControlCode

# Keycode options: https://circuitpython.readthedocs.io/projects/hid/en/latest/api.html#adafruit-hid-keycode-keycode
# ConsumerControlCode options: https://circuitpython.readthedocs.io/projects/hid/en/latest/api.html#adafruit-hid-consumer-control-code-consumercontrolcode
KEY_CODES = [
    # top left
    ConsumerControlCode.MUTE,
    # top middle
    [Keycode.CONTROL, Keycode.C],
    # top right
    [Keycode.CONTROL, Keycode.V],
    # bottom left
    Keycode.LEFT_ARROW,
    # bottom middle
    Keycode.RIGHT_ARROW,
    # bottom right
    "hello world",
]

time.sleep(1)  # Sleep for a bit to avoid a race condition on some systems
cc = ConsumerControl(usb_hid.devices)
kbd = Keyboard(usb_hid.devices)
kbd_layout = KeyboardLayoutUS(kbd)
cols = [digitalio.DigitalInOut(x) for x in (board.D11, board.D12, board.D13)]
rows = [digitalio.DigitalInOut(x) for x in (board.D9, board.D10)]
keys = (
    (0,1,2),
    (3,4,5),
)
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

    removed_keys = list(set(last_keys) - set(keys))
    for key in removed_keys:
        keycode = KEY_CODES[key]
        is_str = isinstance(keycode, str)
        is_list = isinstance(keycode, list)
        if not is_list and CONSUMER_CONTROL_CODES.get(keycode):
            cc.release()
        elif not is_str:
            kbd.release(*keycode) if is_list else kbd.release(keycode)

    added_keys = list(set(keys) - set(last_keys))
    for key in added_keys:
        keycode = KEY_CODES[key]
        is_str = isinstance(keycode, str)
        is_list = isinstance(keycode, list)
        if not is_list and CONSUMER_CONTROL_CODES.get(keycode):
            cc.press(keycode)
        elif is_str:
            kbd_layout.write(keycode)
        else:
            kbd.press(*keycode) if is_list else kbd.press(keycode)

    last_keys = keys

    time.sleep(0.05)
