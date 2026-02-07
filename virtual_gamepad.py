import threading
import vgamepad as vg
import time

class VirtualGamepad:

    BUTTON_MAP = {
        'b0': vg.DS4_BUTTONS.DS4_BUTTON_CROSS,
        'b1': vg.DS4_BUTTONS.DS4_BUTTON_CIRCLE,
        'b2': vg.DS4_BUTTONS.DS4_BUTTON_SQUARE,
        'b3': vg.DS4_BUTTONS.DS4_BUTTON_TRIANGLE,
        'b4': vg.DS4_BUTTONS.DS4_BUTTON_SHOULDER_LEFT,
        'b5': vg.DS4_BUTTONS.DS4_BUTTON_SHOULDER_RIGHT,
        'b6': vg.DS4_BUTTONS.DS4_BUTTON_TRIGGER_LEFT,
        'b7': vg.DS4_BUTTONS.DS4_BUTTON_TRIGGER_RIGHT,
        'b8': vg.DS4_BUTTONS.DS4_BUTTON_SHARE,
        'b9': vg.DS4_BUTTONS.DS4_BUTTON_OPTIONS,
        'b10': vg.DS4_BUTTONS.DS4_BUTTON_THUMB_LEFT,
        'b11': vg.DS4_BUTTONS.DS4_BUTTON_THUMB_RIGHT,
    }

    def __init__(self, controllerIndex: int) -> None:
        self.controllerIndex = controllerIndex
        self.gamepad = vg.VDS4Gamepad()

        self.thread = None

    def start(self):
        self.thread = threading.Thread(target=self.run)

        self.thread.daemon = True
        self.thread.start()

    def run(self):
        self.gamepad.release_button(vg.DS4_BUTTONS.DS4_BUTTON_CIRCLE)
        while True:
            self.gamepad.update()
            time.sleep(0.1)

    def updateState(self, button, state: bool):
        if state:
            self.gamepad.press_button(button)   
        else:
            self.gamepad.release_button(button)
        self.gamepad.update()