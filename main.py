import vgamepad as vg
from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

gamepad = vg.VDS4Gamepad()  # Virtual DualShock 4 controller


# Mapping of button IDs from the frontend to virtual gamepad buttons
BUTTON_MAP = {
    "triangle-button": vg.DS4_BUTTONS.DS4_BUTTON_TRIANGLE,
    "square-button": vg.DS4_BUTTONS.DS4_BUTTON_SQUARE,
    "circle-button": vg.DS4_BUTTONS.DS4_BUTTON_CIRCLE,
    "cross-button": vg.DS4_BUTTONS.DS4_BUTTON_CROSS,

    "l3-button": vg.DS4_BUTTONS.DS4_BUTTON_THUMB_LEFT,
    "r3-button": vg.DS4_BUTTONS.DS4_BUTTON_THUMB_RIGHT,
}

SPECIAL_BUTTON_MAP = {
    "ps-button": vg.DS4_SPECIAL_BUTTONS.DS4_SPECIAL_BUTTON_PS,
}

DPAD_MAP = {
    -1 : vg.DS4_DPAD_DIRECTIONS.DS4_BUTTON_DPAD_NONE,
    0 : vg.DS4_DPAD_DIRECTIONS.DS4_BUTTON_DPAD_NORTH,
    45 : vg.DS4_DPAD_DIRECTIONS.DS4_BUTTON_DPAD_NORTHEAST,
    90 : vg.DS4_DPAD_DIRECTIONS.DS4_BUTTON_DPAD_EAST,
    135 : vg.DS4_DPAD_DIRECTIONS.DS4_BUTTON_DPAD_SOUTHEAST,
    180 : vg.DS4_DPAD_DIRECTIONS.DS4_BUTTON_DPAD_SOUTH,
    225 : vg.DS4_DPAD_DIRECTIONS.DS4_BUTTON_DPAD_SOUTHWEST,
    270 : vg.DS4_DPAD_DIRECTIONS.DS4_BUTTON_DPAD_WEST,
    315 : vg.DS4_DPAD_DIRECTIONS.DS4_BUTTON_DPAD_NORTHWEST,
}


@app.route('/')
def index():
    return render_template('index.html')  # Serve the web interface


@socketio.on('joystick_data')
def handle_joystick_data(data):
    button_states = data.get('buttons', {})
    dpad_pov = data.get('dpad', 0)
    left_x = float(data.get('left_x', 0)) 
    left_y = float(data.get('left_y', 0)) * -1
    right_x = float(data.get('right_x', 0))
    right_y = float(data.get('right_y', 0)) * -1

    # update values
    for button_id, is_active in button_states.items():
        if button_id in BUTTON_MAP:
            if is_active:
                gamepad.press_button(BUTTON_MAP[button_id])
            else:
                gamepad.release_button(BUTTON_MAP[button_id])
        elif button_id in SPECIAL_BUTTON_MAP:
            if is_active:
                gamepad.press_special_button(SPECIAL_BUTTON_MAP[button_id])
            else:
                gamepad.release_special_button(SPECIAL_BUTTON_MAP[button_id])

    gamepad.left_joystick_float(x_value_float=left_x, y_value_float=left_y)
    gamepad.right_joystick_float(x_value_float=right_x, y_value_float=right_y)

    gamepad.directional_pad(direction=DPAD_MAP[dpad_pov])

    # Apply changes to the gamepad
    gamepad.update()

    # Log the joystick and button data for debugging
    print(f"Button States: {button_states}")


if __name__ == '__main__':
    socketio.run(app, host='127.0.0.1', port=5000)
