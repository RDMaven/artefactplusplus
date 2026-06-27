from config import Config
from sites.www.main import app
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
            app, 
            host=Config.Web.HOST, 
            port=Config.Web.PORT
        )