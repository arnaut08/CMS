from flask import Blueprint, request, send_file
from modules.credential import credentialUtils as utils
from modules.credential.credentialModel import CredentialModel, FieldModel
from werkzeug.datastructures import ImmutableMultiDict as im
from flask_jwt import jwt_required
import json, os
from language import translation_en as translate
from helper import utils as helperUtils

credentialBlueprint = Blueprint('credentialBlueprint', __name__)

@credentialBlueprint.route('', methods=['POST', 'PUT'])
@jwt_required()
def manageCredential():
    data = helperUtils.toImmutableDictionary(request.data)
    credentialData = CredentialModel(data)
    fieldValidity = True
    for field in json.loads(data['fields']):
        newDict = im.copy(field)
        fieldData = FieldModel(newDict)
        errorObj = {}
        if not fieldData.validate():
            fieldValidity = False
            errorObj = fieldData.errors
            break

    if credentialData.validate() and fieldValidity:
        if request.method == 'POST':
            added = utils.addCredential(data)
            if added:
                return helperUtils.messageResponse(translate.addCredential)
            else:
                return helperUtils.error(translate.addCredentialPermission)
        elif request.method == 'PUT':
            updated = utils.updateCredential(data)
            if updated:
                return helperUtils.messageResponse(translate.updateCredential)
            else:
                return helperUtils.error(translate.updateCredentialPermission)
    else:
        return helperUtils.validationError(credentialData.errors or errorObj)

@credentialBlueprint.route('/projects', methods=['GET'])
@jwt_required()
def getProjectsAndCredentials():
    keys = dict(request.args).keys()
    result = utils.getProjectCredentials(request.args) if ('pId' in keys) else utils.getProjects(request.args)
    return helperUtils.dataResponse(result)


@credentialBlueprint.route('/<string:credentialId>', methods=['GET'])
@jwt_required()
def getCredentialDetails(credentialId):
    result = utils.getCredentialDetails(credentialId)
    return helperUtils.dataResponse(result)


@credentialBlueprint.route('/star', methods=['GET', 'POST'])
@jwt_required()
def manageStarredCredentials():
    if request.method == 'GET':
        result = utils.getFavouriteCredentials()
        return helperUtils.dataResponse(result)
    else:
        starred = utils.manageFavouriteCredential(helperUtils.toImmutableDictionary(request.data))
        if starred:
            return helperUtils.messageResponse(translate.addFavourite)
        else:
            return helperUtils.messageResponse(translate.removeFavourite)

@credentialBlueprint.route('/upload', methods=['POST', 'DELETE'])
@jwt_required()
def uploadFile():
    data = request.form
    if request.method == 'POST':
        currentFilePath = os.path.dirname(os.path.realpath(__file__))
        projectPath = currentFilePath[0: currentFilePath[0: currentFilePath.rindex("/")].rindex("/")]
        uploadPath = "{}/uploads/{}/{}".format(projectPath, data['projectName'], data['credentialName'])
        files = request.files['file']
        try:
            files.save(os.path.join(uploadPath, files.filename))
        except FileNotFoundError:
            os.makedirs(uploadPath)
            files.save(os.path.join(uploadPath, files.filename))
        return helperUtils.responseWithMessageAndData({'path': os.path.join(uploadPath, files.filename)}, translate.uploadFile)
    else:
        os.remove(data['filePath'])
        return helperUtils.messageResponse(translate.removeFile)

@credentialBlueprint.route('/file/<path:path>', methods=['GET'])
@jwt_required()
def getFile(path):
    try:
        return send_file('/{}'.format(path), as_attachment=True)
    except FileNotFoundError:
        return helperUtils.error(translate.incorrectPath)