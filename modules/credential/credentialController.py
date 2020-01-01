from flask import Blueprint, jsonify, request
from modules.credential import credentialUtils as utils
from modules.credential.credentialModel import CredentialModel
from config import constants

credentialBlueprint = Blueprint('credentialBlueprint', __name__, url_prefix= "/credential")

@credentialBlueprint.route('', methods=['POST','PUT'])
def addOrUpdateCredential():
    try:
        data = CredentialModel(request.form)
        if data.validate():
            if request.method == 'POST':
                utils.addCredential(request.form)
                return jsonify(message = 'Credential Added Successfully'), constants.statusCode['success']
            elif request.method == 'PUT':
                utils.updateCredential(request.form)
                return jsonify(message = 'Credential Updated Successfully'), constants.statusCode['success']
        else:
            return jsonify(data.errors), constants.statusCode['error']['badRequest']
    except:
        return jsonify(error = 'Internal Server Error'), constants.statusCode['error']['internalServer']
