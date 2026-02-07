import threading
import vgamepad as vg
import time


class VirtualGamepad:

    def __init__(self, controllerIndex: int) -> None:
        self.controllerIndex = controllerIndex
        self.gamepad = vg.VDS4Gamepad()

        self.thread = None

    def start(self):
        self.thread = threading.Thread(target=self.run)

        self.thread.daemon = True
        self.thread.start()

    def run(self):
        while True:
            self.gamepad.press_button(button=vg.DS4_BUTTONS.DS4_BUTTON_CROSS)
            self.gamepad.update()
            time.sleep(1)

            self.gamepad.release_button(button=vg.DS4_BUTTONS.DS4_BUTTON_CROSS)
            self.gamepad.update()
            time.sleep(1)

    def updateState(self, state: bool):
        button = vg.DS4_BUTTONS.DS4_BUTTON_CIRCLE
        if state:
            self.gamepad.press_button(button)
        else:
            self.gamepad.release_button(button)
        self.gamepad.update()