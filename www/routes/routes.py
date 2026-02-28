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


@router.get("/video")
async def video():
    return StreamingResponse(
        im.capture_video(Config.ID_CAMERA, Config.OS_IS_LINUX),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )