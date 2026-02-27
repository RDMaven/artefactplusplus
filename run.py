from config import Config
from www import app
from fastapi import FastAPI
import os


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
            app, 
            host=Config.Web.HOST, 
            port=Config.Web.PORT
        )