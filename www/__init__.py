from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request, Body, Response
from fastapi.responses import HTMLResponse, StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os, sys

# Ajouter (salement) le dossier parent au path
sys.path.append('../src')

# Custom imports
import src.camera.image as im
from config import Config


# Define FastAPI app
app = FastAPI()


app.mount("/static", StaticFiles(directory=Config.Path.STATIC_DIRECTORY), name="static")

templates = Jinja2Templates(directory=Config.Path.TEMPLATES_DIRECTORY)



favicon_path = Config.Path.STATIC_DIRECTORY + '/images/favicon.ico'

@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse(favicon_path)


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


# Mount a static directory for serving static files (like camera.html)


# Robot Page
@app.get("/{robot_id}/", response_class=HTMLResponse)
async def robot_page(request: Request, robot_id: int = 1):
    # Checking the available robots
    available_robots = [1, 2, 3]  # TODO: Fetch the list of available robots dynamically

    if robot_id not in available_robots:
        return f"Asked for robot <strong>{robot_id}</strong>. That robot does not exist. The robot_id has to be between 1 and 3."
    else:
        return templates.TemplateResponse(request=request, name="robot.html", context={"robot_id": robot_id})
        # return HTMLResponse(content=f"<h1>Robot {robot_id}</h1><p>Details for Robot {robot_id} go here.</p>")

@app.get("/video")
async def video():
    return StreamingResponse(
        im.capture_video(Config.ID_CAMERA, Config.OS_IS_LINUX),  # change id if needed
        media_type="multipart/x-mixed-replace; boundary=frame"
    )


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            print(data)
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")

@app.post("/send")
async def send_message(message: str = Body(...)):
    await manager.broadcast(f"SERVER: {message}")
    return {"status": "Message sent"}