from flask import Blueprint, jsonify, request
from flask_jwt import jwt_required
from config import constants
from modules.access.accessModel import AccessModel
import modules.access.accessUtils as utils

accessBlueprint = Blueprint('accessBlueprint', __name__)

@accessBlueprint.route('', methods=['POST', 'PUT'])
@jwt_required()
def manageAccess():
    data = AccessModel(request.form)
    if data.validate():
        if request.method == 'POST':
            utils.addAccessPermission(request.form)
            return jsonify(message = 'Access Permission Added Successfully'), constants.statusCode['success']

        if request.method == 'PUT':
            utils.updateAccessPermission(request.form)
            return jsonify(message = 'Access Permission Updated Successfully'), constants.statusCode['success']
    else:
        return jsonify(data.errors), constants.statusCode['error']['badRequest']
