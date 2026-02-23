from config import Config
from www import app as _

if __name__=='__main__':
    app.run(debug=True, port = Config.Web.PORT)
