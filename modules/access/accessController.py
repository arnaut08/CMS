from flask import Blueprint, jsonify, request
from flask_jwt import jwt_required
from config import constants
from modules.access.accessModel import AccessModel
import modules.access.accessUtils as utils
from werkzeug.datastructures import ImmutableMultiDict as im
import json

accessBlueprint = Blueprint('accessBlueprint', __name__)

@accessBlueprint.route('', methods=['POST', 'PUT'])
@jwt_required()
def manageAccess():
    data = im.copy(json.loads(request.data.decode('utf8')))
    accessData = AccessModel(data)
    if accessData.validate():
        if request.method == 'POST':
            id = utils.addAccessPermission(data)
            return jsonify(message = 'Access Permission Added Successfully', id = id), constants.statusCode['success']

        if request.method == 'PUT':
            utils.updateAccessPermission(data)
            return jsonify(message = 'Access Permission Updated Successfully'), constants.statusCode['success']
    else:
        return jsonify(accessData.errors), constants.statusCode['error']['badRequest']

@accessBlueprint.route('/<int:id>', methods=['GET'])
@jwt_required()
def getUserAccessData(id):
    result = utils.getProjectAccessData(id, request.args)
    return jsonify(data = result), constants.statusCode['success']