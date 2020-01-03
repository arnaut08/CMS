from flask import Blueprint, jsonify, request
from modules.credential import credentialUtils as utils
from modules.credential.credentialModel import CredentialModel, FieldModel
from config import constants
from werkzeug.datastructures import ImmutableMultiDict as im

import json

credentialBlueprint = Blueprint('credentialBlueprint', __name__, url_prefix= "/credential")

@credentialBlueprint.route('', methods=['POST','PUT'])
def addOrUpdateCredential():
    try:
        credentialData = CredentialModel(request.form)
        fieldValidity = True
        for field in (json.loads(request.form['fields'])):
            newDict = im.copy(field)
            fieldData = FieldModel(newDict)
            errorObj = {}
            if not fieldData.validate():
                fieldValidity = False
                errorObj = fieldData.errors
                break

        if credentialData.validate() and fieldValidity:
            if request.method == 'POST':
                utils.addCredential(request.form)
                return jsonify(message = 'Credential Added Successfully'), constants.statusCode['success']
            elif request.method == 'PUT':
                utils.updateCredential(request.form)
                return jsonify(message = 'Credential Updated Successfully'), constants.statusCode['success']
        else:
            return jsonify(credentialData.errors or errorObj), constants.statusCode['error']['badRequest']
    except:
        return jsonify(error = 'Internal Server Error'), constants.statusCode['error']['internalServer']
