Plug in the keypad, go to This PC and it will show up as a USB Drive. Open the `code.py` file in the drive and edit using any editor. Saving the file will automatically flash the new code onto the microcontroller. The red LED next to the button on the microcontroller will flash off and back on if flashing is successful, and the other brighter LED should be off. Can use the Serial button in the Mu editor to see debugging output.

Code samples and setup guide: https://github.com/painlessprototyping/byo_keyboard_code/tree/master/byo_sample_code/circuit_python
* Must use CircuitPython 7.0 instead of the 6.3 linked in the setup guide to get support for `supervisor.ticks_ms()`. Bootloader 7.0 is found in `bootloader` folder and 7.0 lib is found in `lib` folder.
