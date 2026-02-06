import vgamepad as vg
import time

class VirtualGamepad():

    def __init__(self, controllerIndex: int) -> None:
        self.controllerIndex = controllerIndex
        self.gamepad = vg.VDS4Gamepad()

    def start(self):
        self.run()

    def run(self):
        while True:
            self.gamepad.press_button(button=vg.DS4_BUTTONS.DS4_BUTTON_CROSS)
            self.gamepad.update()
            time.sleep(1)

            self.gamepad.release_button(button=vg.DS4_BUTTONS.DS4_BUTTON_CROSS)
            self.gamepad.update()
            time.sleep(1)