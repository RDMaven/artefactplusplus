from config import Config
from www import app

if __name__=='__main__':
    app.run(debug=True, port = Config.Web.PORT)
