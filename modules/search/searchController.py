from flask import Blueprint, request
from flask_jwt import jwt_required
import modules.search.searchUtils as utils
from modules.search.searchModel import SearchModel
from language import translation_en as translate
from helper import utils as helperUtils


searchBlueprint = Blueprint('searchBlueprint', __name__)

@searchBlueprint.route("", methods=['GET'])
@jwt_required()
def searchCredentials():
    params = dict(request.args).keys()
    if 'keyword' in params:
        result = utils.getSearchedCredentials(request.args)
        return helperUtils.dataResponse(result)   
    else:
        return helperUtils.error(translate.keywordRequired)

@searchBlueprint.route("/employee", methods=['GET'])
@jwt_required()
def searchEmployees():
    data = SearchModel(request.args)
    if data.validate():
        result = utils.getSearchedUsers(request.args)
        return helperUtils.dataResponse(result)    
    else:
        return helperUtils.validationError(data.errors)

@searchBlueprint.route("/project", methods=['GET'])
@jwt_required()
def searchProjects():
    data = SearchModel(request.args)
    if data.validate():
        result = utils.getSearchedProjects(request.args)
        return helperUtils.dataResponse(result)    
    else:
        return helperUtils.validationError(data.errors)