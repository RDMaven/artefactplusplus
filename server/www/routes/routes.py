# ------------------------------------------------------- #
# ROUTES NORMALES (i.e. non WebSockets) ----------------- #
# ------------------------------------------------------- #

from fastapi import APIRouter, Request, Body
from fastapi.responses import HTMLResponse, StreamingResponse, FileResponse
from fastapi.templating import Jinja2Templates

from config import Config
from www.routes.utils.utils_video import mjpeg_generator

from www.routes.websocket import ask_client

# import sys
# sys.path.append('../src')
# import src.camera.image as im

# Init router, et import des templates ------------------ #
router = APIRouter()
templates = Jinja2Templates(directory=Config.Path.TEMPLATES_DIRECTORY)

@router.get("/connected")
async def connected():
    return ask_client()

# ICON du projet ---------------------------------------- #
@router.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse(Config.Path.STATIC_DIRECTORY + '/images/favicon.ico')

# Page principale --------------------------------------- #
@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )

# Page de contrôle pour chaque robot. ------------------- #
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

#  Pages de feed video par robot ------------------------- #
@router.get("/video/{robot_id}")
async def video(robot_id):
    return StreamingResponse(
        mjpeg_generator(int(robot_id)),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )


#  Pages de feed video par robot (AVEC BOXXXXXX) ------------------------- #
#@router.get("/videobox/{robot_id}")
#async def videobox(robot_id):
#    return StreamingResponse(
#        mjpeg_generator_with_box(int(robot_id)),
#        media_type="multipart/x-mixed-replace; boundary=frame"
#    )


# @router.get("/video")
# async def video():
#     return StreamingResponse(
#         im.capture_video(Config.ID_CAMERA, Config.OS_IS_LINUX),
#         media_type="multipart/x-mixed-replace; boundary=frame"
#     )