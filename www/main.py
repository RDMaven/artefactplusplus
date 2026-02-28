from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import sys

from config import Config
from www.routes.routes import router as http_router
from www.routes.websocket import router as ws_router

# Create FastAPI app
app = FastAPI()

# Static files
app.mount("/static", StaticFiles(directory=Config.Path.STATIC_DIRECTORY), name="static")

# Templates
templates = Jinja2Templates(directory=Config.Path.TEMPLATES_DIRECTORY)

# Include routers
app.include_router(http_router)
app.include_router(ws_router)