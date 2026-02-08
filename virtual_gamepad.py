import threading
import vgamepad as vg
import time


class VirtualGamepad:

    BUTTON_MAP = {
        "b0": vg.DS4_BUTTONS.DS4_BUTTON_CROSS,
        "b1": vg.DS4_BUTTONS.DS4_BUTTON_CIRCLE,
        "b2": vg.DS4_BUTTONS.DS4_BUTTON_SQUARE,
        "b3": vg.DS4_BUTTONS.DS4_BUTTON_TRIANGLE,
        "b4": vg.DS4_BUTTONS.DS4_BUTTON_SHOULDER_LEFT,
        "b5": vg.DS4_BUTTONS.DS4_BUTTON_SHOULDER_RIGHT,
        "b6": vg.DS4_BUTTONS.DS4_BUTTON_TRIGGER_LEFT,
        "b7": vg.DS4_BUTTONS.DS4_BUTTON_TRIGGER_RIGHT,
        "b8": vg.DS4_BUTTONS.DS4_BUTTON_SHARE,
        "b9": vg.DS4_BUTTONS.DS4_BUTTON_OPTIONS,
        "b10": vg.DS4_BUTTONS.DS4_BUTTON_THUMB_LEFT,
        "b11": vg.DS4_BUTTONS.DS4_BUTTON_THUMB_RIGHT,
    }

    SPECIAL_BUTTON_MAP = {
        "b16": vg.DS4_SPECIAL_BUTTONS.DS4_SPECIAL_BUTTON_PS,
        "b17": vg.DS4_SPECIAL_BUTTONS.DS4_SPECIAL_BUTTON_TOUCHPAD,
    }

    JOYSTICK_MAP = {
        "j0": "left",
        "j1": "right",
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

    def update_button_state(self, button, state: bool):
        if state:
            self.gamepad.press_button(button)
        else:
            self.gamepad.release_button(button)
        self.gamepad.update()

    def update_special_button_state(self, special_button, state: bool):
        if state:
            self.gamepad.press_special_button(special_button)
        else:
            self.gamepad.release_special_button(special_button)
        self.gamepad.update()

    def update_joystick_state(self, joystick, x, y):
        if joystick == "left":
            self.gamepad.left_joystick_float(x, y)
        elif joystick == "right":
            self.gamepad.right_joystick_float(x, y)
