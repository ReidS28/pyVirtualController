import { Joystick } from './joystick.js';

const socket = io();
var togglingEnabled = false;

window.addEventListener('resize', function(event) {
    location.reload(); 
}, true);


const toggleButton = document.getElementById('toggle-button');
const buttons = document.querySelectorAll('.button');

toggleButton.addEventListener('click', function() {
    toggleButton.classList.toggle('active');
    togglingEnabled = toggleButton.classList.contains('active');
    if(!togglingEnabled){
        buttons.forEach(button =>{
            button.classList.remove('active');
        });
    }
});

buttons.forEach(button => {
    button.addEventListener('mousedown', function() {
        if(togglingEnabled){
            button.classList.toggle('active');
        }else{
            button.classList.add('active');
        }
    });
    button.addEventListener('mouseup', function() {
        if(!togglingEnabled){
            button.classList.remove('active');
        }
    });
});


const leftJoystick = new Joystick('left-joystick-container', -1.0, 0.0, 1.0, -1.0, 0.0, 1.0);
const rightJoystick = new Joystick('right-joystick-container', -1.0, 0.0, 1.0, -1.0, 0.0, 1.0);

function sendControllerData() {
    const leftPosition = leftJoystick.getPosition();
    const rightPosition = rightJoystick.getPosition();

    const buttonStates = {};
    buttons.forEach(button => {
        buttonStates[button.id] = button.classList.contains('active');
    });
    
    const joystickData = {
        left_x: leftPosition.x,
        left_y: leftPosition.y * -1,
        right_x: rightPosition.x,
        right_y: rightPosition.y * -1,
        buttons: buttonStates
    };
    
    socket.emit('joystick_data', joystickData);
    
}

setInterval(sendControllerData, 50);
