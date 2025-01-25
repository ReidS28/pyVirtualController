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
    "cross-button": vg.DS4_BUTTONS.DS4_BUTTON_CROSS
}

@app.route('/')
def index():
    return render_template('index.html')  # Serve the web interface


@socketio.on('joystick_data')
def handle_joystick_data(data):
    # Extract joystick values from the received data
    left_x = float(data.get('left_x', 0)) 
    left_y = float(data.get('left_y', 0)) * -1
    right_x = float(data.get('right_x', 0))
    right_y = float(data.get('right_y', 0)) * -1

    # Update joystick positions
    gamepad.left_joystick_float(x_value_float=left_x, y_value_float=left_y)
    gamepad.right_joystick_float(x_value_float=right_x, y_value_float=right_y)

    # Extract button states from the received data
    button_states = data.get('buttons', {})

    # Update button states
    for button_id, is_active in button_states.items():
        if button_id in BUTTON_MAP:
            if is_active:
                gamepad.press_button(BUTTON_MAP[button_id])  # Press button if active
            else:
                gamepad.release_button(BUTTON_MAP[button_id])  # Release button if inactive

    # Apply changes to the gamepad
    gamepad.update()

    # Log the joystick and button data for debugging
    print(f"Button States: {button_states}")


if __name__ == '__main__':
    socketio.run(app, host='127.0.0.1', port=5000)
