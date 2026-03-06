from fastapi import APIRouter, Request, Body
from fastapi.responses import HTMLResponse, StreamingResponse, FileResponse
from fastapi.templating import Jinja2Templates
import sys

sys.path.append('../src')

import src.camera.image as im
from config import Config

router = APIRouter()

templates = Jinja2Templates(directory=Config.Path.TEMPLATES_DIRECTORY)

favicon_path = Config.Path.STATIC_DIRECTORY + '/images/favicon.ico'


@router.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse(favicon_path)


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )


@router.get("/{robot_id}/", response_class=HTMLResponse)
async def robot_page(request: Request, robot_id: int = 1):

    available_robots = [1, 2, 3]  # TODO: dynamic fetch

    if robot_id not in available_robots:
        return f"Asked for robot <strong>{robot_id}</strong>. That robot does not exist. The robot_id has to be between 1 and 3."

    return templates.TemplateResponse(
        request=request,
        name="robot.html",
        context={"robot_id": robot_id}
    )


# Video stuff
from www.routes.utils.frame_store import frame_store
import cv2
import time

def mjpeg_generator(client_id: int):
    while not frame_store.stop:
        frame = frame_store.get_frame(client_id)
        if frame is None:
            time.sleep(0.01)
            continue

        ret, buffer = cv2.imencode(".jpg", frame)
        if not ret:
            continue

        yield b"--frame\r\n" \
              b"Content-Type: image/jpeg\r\n\r\n" + buffer.tobytes() + b"\r\n"

        time.sleep(0.01)

@router.get("/video/{robot_id}")
async def video(robot_id):
    return StreamingResponse(
        mjpeg_generator(int(robot_id)),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )

# @router.get("/video")
# async def video():
#     return StreamingResponse(
#         im.capture_video(Config.ID_CAMERA, Config.OS_IS_LINUX),
#         media_type="multipart/x-mixed-replace; boundary=frame"
#     )