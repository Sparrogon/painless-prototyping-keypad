# SPDX-FileCopyrightText: 2021 Sandy Macdonald
#
# SPDX-License-Identifier: MIT

# A simple example of how to set up a keymap and HID keyboard on Keybow 2040.

# You'll need to connect Keybow 2040 to a computer, as you would with a regular
# USB keyboard.

# Drop the keybow2040.py file into your `lib` folder on your `CIRCUITPY` drive.

# NOTE! Requires the adafruit_hid CircuitPython library also!

import board
from keybow2040 import Keybow2040

import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode

# Set up Keybow
i2c = board.I2C()
keybow = Keybow2040(i2c)
keys = keybow.keys

# Set up the keyboard and layout
keyboard = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(keyboard)

# A map of keycodes that will be mapped sequentially to each of the keys, 0-15
keymap =    [Keycode.F10,
             Keycode.GRAVE_ACCENT,
             [Keycode.LEFT_SHIFT, Keycode.F1],
             Keycode.ONE,

             Keycode.KEYPAD_NUMLOCK,
             Keycode.LEFT_ARROW,
             Keycode.TAB,
             Keycode.TWO,

             Keycode.KEYPAD_NUMLOCK,
             Keycode.DOWN_ARROW,
             Keycode.UP_ARROW,
             Keycode.THREE,

             Keycode.SPACE,
             Keycode.RIGHT_ARROW,
             Keycode.TAB,
             Keycode.FOUR]

# The colour to set the keys when pressed.
rgb = (15, 15, 15)

# Attach handler functions to all of the keys
for key in keys:
    # A press handler that sends the keycode and turns on the LED
    @keybow.on_press(key)
    def press_handler(key):
        keycode = keymap[key.number]
        is_list = isinstance(keycode, list)
        keyboard.send(*keycode) if is_list else keyboard.press(keycode)
        key.set_led(*rgb)

    # A release handler that turns off the LED
    @keybow.on_release(key)
    def release_handler(key):
        keycode = keymap[key.number]
        is_list = isinstance(keycode, list)
        if not is_list:
            keyboard.release(keycode)
        key.led_off()

while True:
    # Always remember to call keybow.update()!
    keybow.update()
