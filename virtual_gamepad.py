import threading
import vgamepad as vg
import time


class VirtualGamepad:
    PROFILES = {
        "ds4_profile": {
            "BUTTON_MAP": {
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
            },
            "SPECIAL_BUTTON_MAP": {
                "b16": vg.DS4_SPECIAL_BUTTONS.DS4_SPECIAL_BUTTON_PS,
                "b17": vg.DS4_SPECIAL_BUTTONS.DS4_SPECIAL_BUTTON_TOUCHPAD,
            },
            "JOYSTICK_MAP": {
                "j0": "left",
                "j1": "right",
            },
            "DPAD_MAP": {
                "-1": vg.DS4_DPAD_DIRECTIONS.DS4_BUTTON_DPAD_NONE,
                "0": vg.DS4_DPAD_DIRECTIONS.DS4_BUTTON_DPAD_NORTH,
                "45": vg.DS4_DPAD_DIRECTIONS.DS4_BUTTON_DPAD_NORTHEAST,
                "90": vg.DS4_DPAD_DIRECTIONS.DS4_BUTTON_DPAD_EAST,
                "135": vg.DS4_DPAD_DIRECTIONS.DS4_BUTTON_DPAD_SOUTHEAST,
                "180": vg.DS4_DPAD_DIRECTIONS.DS4_BUTTON_DPAD_SOUTH,
                "225": vg.DS4_DPAD_DIRECTIONS.DS4_BUTTON_DPAD_SOUTHWEST,
                "270": vg.DS4_DPAD_DIRECTIONS.DS4_BUTTON_DPAD_WEST,
                "315": vg.DS4_DPAD_DIRECTIONS.DS4_BUTTON_DPAD_NORTHWEST,
            },
        },
        "fake_ds4_profile": {
            "BUTTON_MAP": {
                "b0": vg.DS4_BUTTONS.DS4_BUTTON_SQUARE,
                "b1": vg.DS4_BUTTONS.DS4_BUTTON_CROSS,
                "b2": vg.DS4_BUTTONS.DS4_BUTTON_CIRCLE,
                "b3": vg.DS4_BUTTONS.DS4_BUTTON_TRIANGLE,
                "b4": vg.DS4_BUTTONS.DS4_BUTTON_SHOULDER_LEFT,
                "b5": vg.DS4_BUTTONS.DS4_BUTTON_SHOULDER_RIGHT,
                "b6": vg.DS4_BUTTONS.DS4_BUTTON_SHARE,
                "b7": vg.DS4_BUTTONS.DS4_BUTTON_SHARE,
                "b8": vg.DS4_BUTTONS.DS4_BUTTON_TRIGGER_LEFT,
                "b9": vg.DS4_BUTTONS.DS4_BUTTON_TRIGGER_RIGHT,
                "b10": vg.DS4_BUTTONS.DS4_BUTTON_THUMB_LEFT,
                "b11": vg.DS4_BUTTONS.DS4_BUTTON_THUMB_RIGHT,
            },
            "SPECIAL_BUTTON_MAP": {
                "b16": vg.DS4_SPECIAL_BUTTONS.DS4_SPECIAL_BUTTON_PS,
                "b17": vg.DS4_SPECIAL_BUTTONS.DS4_SPECIAL_BUTTON_TOUCHPAD,
            },
            "JOYSTICK_MAP": {
                "j0": "left",
                "j1": "right",
            },
            "DPAD_MAP": {
                "-1": vg.DS4_DPAD_DIRECTIONS.DS4_BUTTON_DPAD_NONE,
                "0": vg.DS4_DPAD_DIRECTIONS.DS4_BUTTON_DPAD_NORTH,
                "45": vg.DS4_DPAD_DIRECTIONS.DS4_BUTTON_DPAD_NORTHEAST,
                "90": vg.DS4_DPAD_DIRECTIONS.DS4_BUTTON_DPAD_EAST,
                "135": vg.DS4_DPAD_DIRECTIONS.DS4_BUTTON_DPAD_SOUTHEAST,
                "180": vg.DS4_DPAD_DIRECTIONS.DS4_BUTTON_DPAD_SOUTH,
                "225": vg.DS4_DPAD_DIRECTIONS.DS4_BUTTON_DPAD_SOUTHWEST,
                "270": vg.DS4_DPAD_DIRECTIONS.DS4_BUTTON_DPAD_WEST,
                "315": vg.DS4_DPAD_DIRECTIONS.DS4_BUTTON_DPAD_NORTHWEST,
            },
        },
    }

    def __init__(
        self, controllerIndex: int, default_profile: str = "ds4_profile"
    ) -> None:
        self.controllerIndex = controllerIndex
        self.gamepad = vg.VDS4Gamepad()
        self.thread = None

        # Sets up active mappings using the property setter below
        self.current_profile = default_profile

    @property
    def current_profile(self) -> str:
        """Returns the name of the currently active profile."""
        return self._current_profile

    @current_profile.setter
    def current_profile(self, profile_name: str):
        """Changes the active profile and updates all maps with a single assignment."""
        if profile_name not in self.PROFILES:
            raise ValueError(f"Profile '{profile_name}' does not exist.")

        self._current_profile = profile_name
        profile = self.PROFILES[profile_name]

        # Reassign the maps dynamically based on the chosen profile
        self.BUTTON_MAP = profile["BUTTON_MAP"]
        self.SPECIAL_BUTTON_MAP = profile["SPECIAL_BUTTON_MAP"]
        self.JOYSTICK_MAP = profile["JOYSTICK_MAP"]
        self.DPAD_MAP = profile["DPAD_MAP"]

    def start(self):
        self.thread = threading.Thread(target=self.run)
        self.thread.daemon = True
        self.thread.start()

    def run(self):
        while True:
            self.gamepad.update()
            time.sleep(0.1)

    def update_button_state(self, button_key: str, state: bool):
        # Resolves the identifier via the currently active profile map
        button = self.BUTTON_MAP.get(button_key)
        if button is not None:
            if state:
                self.gamepad.press_button(button)
            else:
                self.gamepad.release_button(button)
            self.gamepad.update()

    def update_special_button_state(self, special_button_key: str, state: bool):
        special_button = self.SPECIAL_BUTTON_MAP.get(special_button_key)
        if special_button is not None:
            if state:
                self.gamepad.press_special_button(special_button)
            else:
                self.gamepad.release_special_button(special_button)
            self.gamepad.update()

    def update_joystick_state(self, joystick_key: str, x: float, y: float):
        joystick = self.JOYSTICK_MAP.get(joystick_key)
        if joystick == "left":
            self.gamepad.left_joystick_float(x, y)
        elif joystick == "right":
            self.gamepad.right_joystick_float(x, y)

    def update_dpad_state(self, angle_key):
        angle = self.DPAD_MAP.get(str(angle_key))
        if angle is not None:
            self.gamepad.directional_pad(angle)
