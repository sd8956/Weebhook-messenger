from flask import Flask
from flask_cors import CORS
from routes import weebhook
import os

app = Flask(__name__)

CORS(app)

app.register_blueprint(weebhook.weebhook_router)

if __name__ == '__main__':
  port = os.getenv('PORT')
  debug = os.getenv('DEBUG') == 'True'

  app.run(port=port, debug=debug)