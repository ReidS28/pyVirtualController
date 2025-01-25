import vgamepad as vg
import time

#gamepad = vg.VDS4Gamepad()  # Virtual DualShock 4 controller
gamepad = vg.VX360Gamepad()  # Virtual Xbox 360 controller

while True:
    gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
    print("pressed")
    time.sleep(1)
    gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
    print("pressedn't")
    time.sleep(1)

    gamepad.update()

