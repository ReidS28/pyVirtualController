export class ControllerConnection {
    socket: WebSocket | null = null;
    status = $state("disconnected");

    constructor(controllerID: number) {
        const url = `ws://${window.location.host}/ws/gamepad/${controllerID}`;
        this.socket = new WebSocket(url);

        this.socket.onopen = () => { this.status = "connected"; };
        this.socket.onclose = () => { this.status = "disconnected"; };
    }

        send(data: object) {
            console.log("Sent: " + JSON.stringify(data));
            if (this.socket?.readyState === WebSocket.OPEN) {
                this.socket.send(JSON.stringify(data));
            }
        }

    close() {
        this.socket?.close();
    }
}