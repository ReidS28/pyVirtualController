import { Controller } from "./controller.js";

const socket = io();

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
