from www import app
from config import Config

if __name__=='__main__':
    app.run(debug=True, port = Config.Web.PORT)
