import os
import threading
import uvicorn
from fastapi import FastAPI, APIRouter, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
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
        @self.router.get("/gamepad/{gamepad_id}")
        async def serve_gamepad_ui(gamepad_id: int):
            if gamepad_id >= len(self.gamepads):
                return {"error": "Gamepad slot not found"}
            
            return FileResponse("frontend/dist/index.html")
        
        @self.router.get("/api/status")
        async def read_root():
            return {
                "status": "online", 
                "gamepads": [
                    {"id": i, "profile": g.current_profile} 
                    for i, g in enumerate(self.gamepads)
                ]
            }

        @self.router.post("/api/gamepad/{gamepad_id}/profile")
        async def change_profile(gamepad_id: int, profile_payload: dict):
            if gamepad_id >= len(self.gamepads):
                raise HTTPException(status_code=404, detail="Gamepad not found")
            
            new_profile = profile_payload.get("profile")
            try:
                self.gamepads[gamepad_id].current_profile = new_profile
                return {"status": "success", "gamepad_id": gamepad_id, "current_profile": new_profile}
            except ValueError as e:
                raise HTTPException(status_code=400, detail=str(e))

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

    def handle_data(self, gamepad_id: int, data: dict):
        target_gamepad = self.gamepads[gamepad_id]
        
        for input_id, payload in data.items():
            if input_id in target_gamepad.BUTTON_MAP:
                if "pressed" in payload:
                    target_gamepad.update_button_state(input_id, payload["pressed"])
                    
            elif input_id in target_gamepad.SPECIAL_BUTTON_MAP:
                if "pressed" in payload:
                    target_gamepad.update_special_button_state(input_id, payload["pressed"])
                    
            elif input_id in target_gamepad.JOYSTICK_MAP:
                if "x" in payload and "y" in payload:
                    target_gamepad.update_joystick_state(input_id, payload["x"], -payload["y"])
                    
            elif input_id == "dpad" and "angle" in payload:
                angle_key = str(payload["angle"])
                if angle_key in target_gamepad.DPAD_MAP:
                    target_gamepad.update_dpad_state(angle_key)