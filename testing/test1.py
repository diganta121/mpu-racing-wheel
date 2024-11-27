import vgamepad as vg

"""
gamepad = vg.VX360Gamepad()
gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)  # press the A button
gamepad.press_button(
    button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT
)  # press the left hat button

gamepad.update()  # send the updated state to the computer

# (...) A and left hat are pressed...

gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)  # release the A button

gamepad.update()  # send the updated state to the computer

# (...) left hat is still pressed...
'''
class XUSB_BUTTON(IntFlag):
    
    Possible XUSB report buttons.
    
    XUSB_GAMEPAD_DPAD_UP = 0x0001
    XUSB_GAMEPAD_DPAD_DOWN = 0x0002
    XUSB_GAMEPAD_DPAD_LEFT = 0x0004
    XUSB_GAMEPAD_DPAD_RIGHT = 0x0008
    XUSB_GAMEPAD_START = 0x0010
    XUSB_GAMEPAD_BACK = 0x0020
    XUSB_GAMEPAD_LEFT_THUMB = 0x0040
    XUSB_GAMEPAD_RIGHT_THUMB = 0x0080
    XUSB_GAMEPAD_LEFT_SHOULDER = 0x0100
    XUSB_GAMEPAD_RIGHT_SHOULDER = 0x0200
    XUSB_GAMEPAD_GUIDE = 0x0400
    XUSB_GAMEPAD_A = 0x1000
    XUSB_GAMEPAD_B = 0x2000
    XUSB_GAMEPAD_X = 0x4000
    XUSB_GAMEPAD_Y = 0x8000'''


gamepad.left_trigger_float(value_float=0.5)  # value between 0.0 and 1.0
gamepad.right_trigger_float(value_float=1.0)  # value between 0.0 and 1.0
gamepad.left_joystick_float(
    x_value_float=-0.5, y_value_float=0.0
)  # values between -1.0 and 1.0
gamepad.right_joystick_float(
    x_value_float=-1.0, y_value_float=0.8
)  # values between -1.0 and 1.0

gamepad.update()
"""

import vgamepad as vg
import time

gamepad = vg.VX360Gamepad()

# press a button to wake the device up
gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
gamepad.update()
time.sleep(0.5)
gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
gamepad.update()
time.sleep(0.5)

# press buttons and things
gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER)
gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN)
gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT)
gamepad.left_trigger_float(value_float=0.5)
gamepad.right_trigger_float(value_float=0.5)
gamepad.left_joystick_float(x_value_float=0.0, y_value_float=0.2)
gamepad.right_joystick_float(x_value_float=-1.0, y_value_float=1.0)

gamepad.update()

time.sleep(3.0)

# release buttons and things
gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT)
gamepad.right_trigger_float(value_float=0.0)
gamepad.right_joystick_float(x_value_float=0.0, y_value_float=0.0)

gamepad.update()

time.sleep(1.0)

# reset gamepad to default state
gamepad.reset()

gamepad.update()

time.sleep(1.0)
