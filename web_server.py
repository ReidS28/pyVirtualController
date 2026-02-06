import os
import uvicorn
from fastapi import FastAPI, APIRouter
from fastapi.staticfiles import StaticFiles

class WebServer:
    def __init__(self, num_gamepads: int):
        self.num_gamepads = num_gamepads
        self.app = FastAPI()
        
        self.router = APIRouter()
        self.register_routes()
        self.app.include_router(self.router)

        dist_path = "frontend/dist"
        if os.path.exists(dist_path):
            self.app.mount("/", StaticFiles(directory=dist_path, html=True), name="static")
        else:
            print(f"Warning: {dist_path} not found. Serve the frontend manually or run 'npm run build'.")

    def register_routes(self):
        @self.router.get("/api/status")
        async def read_root():
            return {"status": "online", "gamepads": self.num_gamepads}

    def run(self):
        uvicorn.run(self.app, host="0.0.0.0", port=8000)