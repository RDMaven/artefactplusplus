from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import sys

from config import Config
from www.routes.routes import router as http_router
import www.routes.websocket as websockets
from fastapi.middleware.cors import CORSMiddleware


# Simple setup ------------------------------------------ #
# Create FastAPI app
app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Permet toutes les origines (votre site sur le port 5000, etc.)
    allow_credentials=False,
    allow_methods=["*"], # Permet GET, POST, OPTIONS, etc.
    allow_headers=["*"], # Permet tous les en-têtes
)

# Static files
app.mount("/static", StaticFiles(directory=Config.Path.STATIC_DIRECTORY), name="static")


# Templates
templates = Jinja2Templates(directory=Config.Path.TEMPLATES_DIRECTORY)

# Include routers

app.include_router(websockets.router)
app.include_router(http_router)

# Déroulé setup ----------------------------------------- #
# @app.on_event("shutdown")
# async def shutdown_event():
#     print("Shutting down server… closing WebSocket connections.")
#     # await websockets.manager.broadcast_shutdown()
#     websockets.shutdown_event.set()

