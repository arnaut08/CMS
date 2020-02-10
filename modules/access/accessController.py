from flask import Blueprint, request
from flask_jwt import jwt_required
from modules.access.accessModel import AccessModel
import modules.access.accessUtils as utils
from language import translation_en as translate
from helper import utils as helperUtils

accessBlueprint = Blueprint('accessBlueprint', __name__)

@accessBlueprint.route('', methods=['POST', 'PUT'])
@jwt_required()
def manageAccess():
    data = helperUtils.toImmutableDictionary(request.data)
    accessData = AccessModel(data)
    if accessData.validate():
        if request.method == 'POST':
            id = utils.addAccessPermission(data)
            return helperUtils.responseWithMessageAndData({'id' : id}, translate.addAccess)
        if request.method == 'PUT':
            utils.updateAccessPermission(data)
            return helperUtils.messageResponse(translate.updateAccess)
    else:
        return helperUtils.validationError(accessData.errors)

@accessBlueprint.route('/<int:id>', methods=['GET'])
@jwt_required()
def getUserAccessData(id):
    result = utils.getProjectAccessData(id, request.args)
    return helperUtils.dataResponse(result)