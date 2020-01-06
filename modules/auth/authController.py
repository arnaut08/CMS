from flask import Blueprint, jsonify, request
from config import constants
import json
from modules.auth.authModel import AuthModel

authBlueprint = Blueprint('authBlueprint', __name__, url_prefix= "/login")

@authBlueprint.route("", methods=['POST'])
def login():
    data = AuthModel(request.form)
    if data.validate():
        pass
        # HRMS Login API will be requested and token will be returned
    else:
        return jsonify(data.errors), constants.statusCode['error']['badRequest']
