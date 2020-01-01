from flask import Flask
from flask_cors import CORS
from config import configurations as config

server = Flask(__name__)

import routes

#Cross Origin Config
CORS(server)

#Configure Server
server.config.update(
    SECRET_KEY = config.SECRET,
)

if __name__ == '__main__':
    server.run()