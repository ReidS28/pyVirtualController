import { Controller } from "./controller.js";

const socket = io();

window.globalState = {
    buttonTogglingEnabled: false,
	holdJoysticks: false,
	holdTriggers: false
};

window.addEventListener(
	"resize",
	function (event) {
		location.reload();
	},
	true
);

    const controller = new Controller('controller', 'static/assets/ds4-controller.svg');

    function sendControllerData() {

        socket.emit('joystick_data', controller.getControllerState());
    }

    setInterval(sendControllerData, 50);
