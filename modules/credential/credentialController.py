from flask import Blueprint, jsonify, request
from modules.credential import credentialUtils as utils
from modules.credential.credentialModel import CredentialModel, FieldModel
from config import constants
from werkzeug.datastructures import ImmutableMultiDict as im
from flask_jwt import jwt_required
import json

credentialBlueprint = Blueprint('credentialBlueprint', __name__)

@credentialBlueprint.route('', methods=['POST', 'PUT'])
@jwt_required()
def manageCredential():
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
            added = utils.addCredential(request.form)
            if added:
                return jsonify(message = 'Credential Added Successfully'), constants.statusCode['success']
            else:
                return jsonify(error = "You don't have permission to add a credential in this project"), constants.statusCode['error']['badRequest']
        elif request.method == 'PUT':
            updated = utils.updateCredential(request.form)
            if updated:
                return jsonify(message = 'Credential Updated Successfully'), constants.statusCode['success']
            else:
                return jsonify(error = "You don't have permission to update this credential"), constants.statusCode['error']['badRequest']                
    else:
        return jsonify(credentialData.errors or errorObj), constants.statusCode['error']['badRequest']

@credentialBlueprint.route('/projects', methods=['GET'])
@jwt_required()
def getProjectsAndCredentials():
    keys = dict(request.args).keys()
    result = utils.getProjectCredentials(request.args) if ('pId' in keys) else utils.getProjects(request.args)
    return jsonify(result), constants.statusCode['success']


@credentialBlueprint.route('/<string:credentialId>', methods=['GET'])
@jwt_required()
def getCredentialDetails(credentialId):
    result = utils.getCredentialDetails(credentialId)
    return jsonify(result), constants.statusCode['success']


@credentialBlueprint.route('/star', methods=['GET', 'POST'])
@jwt_required()
def manageStarredCredentials():
    if request.method == 'GET':
        result = utils.getFavouriteCredentials()
        return jsonify(result), constants.statusCode['success']
    else:
        starred = utils.manageFavouriteCredential(request.form)
        if starred:
            return jsonify(message = 'Credential Added to Favourites Successfully'), constants.statusCode['success']
        else:
            return jsonify(message = "Credential Removed from Favourites Successfully"), constants.statusCode['success']