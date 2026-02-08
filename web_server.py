import os
import threading
import uvicorn
from fastapi import FastAPI, APIRouter, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from virtual_gamepad import VirtualGamepad


class WebServer:
    def __init__(self, gamepads: list[VirtualGamepad]):
        self.gamepads = gamepads
        self.app = FastAPI()
        self.router = APIRouter()
        self.register_routes()
        self.app.include_router(self.router)

        dist_path = "frontend/dist"
        if os.path.exists(dist_path):
            self.app.mount(
                "/", StaticFiles(directory=dist_path, html=True), name="static"
            )

        self.server = None
        self.server_thread = None

    def register_routes(self):
        @self.router.get("/api/status")
        async def read_root():
            return {"status": "online", "gamepads": len(self.gamepads)}

        @self.app.websocket("/ws/gamepad/{gamepad_id}")
        async def websocket_endpoint(websocket: WebSocket, gamepad_id: int):
            await websocket.accept()

            if gamepad_id >= len(self.gamepads):
                await websocket.close(code=1008)
                return

            try:
                while True:
                    data = await websocket.receive_json()
                    self.handle_data(gamepad_id, data)

            except WebSocketDisconnect:
                print(f"Client disconnected from gamepad {gamepad_id}")

    def start(self):
        config = uvicorn.Config(self.app, host="0.0.0.0", port=8000, log_level="info")
        self.server = uvicorn.Server(config)
        self.server_thread = threading.Thread(target=self.server.run, daemon=True)
        self.server_thread.start()

    def stop(self):
        if self.server:
            self.server.should_exit = True
            self.server_thread.join()

    def handle_data(self, gamepad_id: int, data):
        target_gamepad = self.gamepads[gamepad_id]
        for id, payload in data.items():
            if id in VirtualGamepad.BUTTON_MAP:
                button_constant = VirtualGamepad.BUTTON_MAP[id]
                if "pressed" in payload:
                    state = payload["pressed"]
                    target_gamepad.update_button_state(button_constant, state)
            elif id in VirtualGamepad.SPECIAL_BUTTON_MAP:
                special_button_constant = VirtualGamepad.SPECIAL_BUTTON_MAP[id]
                if "pressed" in payload:
                    state = payload["pressed"]
                    target_gamepad.update_special_button_state(special_button_constant, state)
            elif id in VirtualGamepad.JOYSTICK_MAP:
                joystick = VirtualGamepad.JOYSTICK_MAP[id]
                if "x" in payload and "y" in payload:
                    target_gamepad.update_joystick_state(joystick, payload["x"], payload["y"])
