from flask import Flask
from flask_cors import CORS
from config import configurations as config
from auth import verify, identity
from flask_jwt import JWT

server = Flask(__name__)

import routes

#Cross Origin Config
CORS(server)

#Configure Server
server.config.update(
    SECRET_KEY = config.SECRET,
    JWT_VERIFY_CLAIMS = config.JWT,
    JWT_REQUIRED_CLAIMS = config.JWT,
)

#JWT Config
jwt = JWT(server, verify, identity)

if __name__ == '__main__':
    server.run()