from flask import Blueprint, jsonify, request
from flask_jwt import jwt_required
from config import constants
import json
import modules.search.searchUtils as utils
from modules.search.searchModel import SearchEmployeeModel


searchBlueprint = Blueprint('searchBlueprint', __name__)

@searchBlueprint.route("", methods=['GET'])
@jwt_required()
def searchCredentials():
    params = dict(request.args).keys()
    if 'keyword' in params:
        result = utils.getSearchedCredentials(request.args)
        return jsonify(data = result), constants.statusCode['success']    
    else:
        return jsonify(error = "Keyword is required."), constants.statusCode['error']['badRequest']

@searchBlueprint.route("/employee", methods=['GET'])
@jwt_required()
def searchEmployees():
    data = SearchEmployeeModel(request.args)
    if data.validate():
        result = utils.getSearchedUsers(request.args)
        return jsonify(data = result), constants.statusCode['success']    
    else:
        return jsonify(error = data.errors), constants.statusCode['error']['badRequest']