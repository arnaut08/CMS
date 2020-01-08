from flask import Flask
from flask_cors import CORS
from config import configurations as config
from auth import verify, identity, responseHandler
from flask_jwt import JWT

server = Flask(__name__)

import routes

#Cross Origin Config
CORS(server)

#Configure Server
server.config.update(
    SECRET_KEY = config.SECRET,
    JWT_AUTH_URL_RULE = config.JWT_URL,
    JWT_AUTH_USERNAME_KEY = config.JWT_USERNAME_KEY,
    JWT_EXPIRATION_DELTA = config.JWT_EXPIRATION_TIME
)

#JWT Config
jwt = JWT(server, verify, identity)
jwt.auth_response_handler(responseHandler)

if __name__ == '__main__':
    server.run()