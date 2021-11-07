import time
import supervisor
import board
import digitalio
import adafruit_matrixkeypad
import usb_hid
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode

time.sleep(1)  # Sleep for a bit to avoid a race condition on some systems
cc = ConsumerControl(usb_hid.devices)

cols = [digitalio.DigitalInOut(x) for x in (board.D11, board.D12, board.D13)]
rows = [digitalio.DigitalInOut(x) for x in (board.D9, board.D10)]
keys = (
    (0,1,2),
    (3,4,5),
)

keypad = adafruit_matrixkeypad.Matrix_Keypad(rows, cols, keys)

KEYS = [
    ConsumerControlCode.MUTE,
    ConsumerControlCode.VOLUME_INCREMENT,
    ConsumerControlCode.PLAY_PAUSE,
    ConsumerControlCode.SCAN_PREVIOUS_TRACK,
    ConsumerControlCode.VOLUME_DECREMENT,
    ConsumerControlCode.SCAN_NEXT_TRACK,
]

press_start_time = 0
press_duration = 0
repeat_delay = 500 # ticks
repeat_interval = 0.1 # seconds
last_keys = []

def sendKeys(consumerControl, keys):
    for key in keys:
        consumerControl.send(KEYS[key])

while True:
    keys = keypad.pressed_keys
    if keys:
        last_keys = keys
        if press_start_time == 0:
            press_start_time = supervisor.ticks_ms()
        else:
            current_time = supervisor.ticks_ms()
            press_duration = current_time - press_start_time
            if (press_duration >= repeat_delay):
                sendKeys(cc, keys)
                time.sleep(repeat_interval)
    else:
        press_start_time = 0
        if press_duration < repeat_delay:
            sendKeys(cc, last_keys)
            last_keys = []
