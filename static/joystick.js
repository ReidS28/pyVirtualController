export class Joystick {
    constructor(containerId, minX, centerX, maxX, minY, centerY, maxY) {
        this.container = document.getElementById(containerId);
        this.joystick = document.createElement('div');
        this.joystick.className = 'joystick';
        this.container.appendChild(this.joystick);

        this.minX = minX; 
        this.centerX = centerX;
        this.maxX = maxX;

        this.minY = minY;
        this.centerY = centerY;
        this.maxY = maxY;

        this.x = this.centerX;
        this.y = this.centerY;

        this.containerWidth = this.container.offsetWidth;
        this.containerHeight = this.container.offsetHeight;

        this.joystickWidth = this.containerWidth * 0.7;
        this.joystickHeight = this.containerHeight * 0.7;
        this.maxRadius = Math.min(this.container.clientWidth, this.container.clientHeight) / 2;

        this.resetPosition();

        this.container.addEventListener('mousedown', (event) => this.startDrag(event));
        window.addEventListener('mouseup', () => this.endDrag());
        window.addEventListener('mousemove', (event) => this.drag(event));
    }

    resetPosition() {
        this.joystick.style.width = `${this.joystickWidth}px`;
        this.joystick.style.height = `${this.joystickHeight}px`;
        this.joystick.style.position = 'absolute';
        this.joystick.style.left = `${this.containerWidth / 2 - this.joystickWidth / 2}px`;
        this.joystick.style.top = `${this.containerHeight / 2 - this.joystickHeight / 2}px`;
        this.x = this.centerX;
        this.y = this.centerY;
    }

    startDrag(event) {
        this.isDragging = true;
        this.updatePosition(event);
    }

    endDrag() {
        this.isDragging = false;
        this.resetPosition();
    }

    drag(event) {
        if (this.isDragging) {
            this.updatePosition(event);
        }
    }

    updatePosition(event) {
        const rect = this.container.getBoundingClientRect();

        // Calculate offsets from the center of the container
        const offsetX = event.clientX - rect.left - this.containerWidth / 2;
        const offsetY = event.clientY - rect.top - this.containerHeight / 2;

        // Clamp joystick movement within maxRadius
        const distance = Math.sqrt(offsetX ** 2 + offsetY ** 2);
        const angle = Math.atan2(offsetY, offsetX);
        const radius = Math.min(distance, this.maxRadius);

        // Calculate joystick's new position within the circle
        const x = Math.cos(angle) * radius;
        const y = Math.sin(angle) * radius;

        // Update joystick's visual position
        this.joystick.style.left = `${this.container.clientWidth / 2 + x - this.joystick.clientWidth / 2}px`;
        this.joystick.style.top = `${this.container.clientHeight / 2 + y - this.joystick.clientHeight / 2}px`;

        this.x = (x / this.maxRadius) * (this.maxX - this.minX) / 2 + this.centerX;
        this.y = (y / this.maxRadius) * (this.maxY - this.minY) / 2 + this.centerY;

        // Clamp the values to the min and max
        this.x = Math.max(this.minX, Math.min(this.x, this.maxX));
        this.y = Math.max(this.minY, Math.min(this.y, this.maxY));

    }

    getPosition() {
        const position = {
            x: this.x,
            y: this.y
        };

        // Invert the y-axis
        //position.y = 255 - position.y;

        return position;
    }
}
