import random, string, json
from flask import jsonify
from config import constants
from werkzeug.datastructures import ImmutableMultiDict as im

def generateAlphanumericKey():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(8))

def validationError(errorObj):
    return jsonify(errorObj), constants.statusCode['error']['badRequest']

def error(message):
    return jsonify(error = {'message' : message}), constants.statusCode['error']['badRequest']

def responseWithMessageAndData(data, message):
    return jsonify(data = data, message=message), constants.statusCode['success']

def messageResponse(message):
    return jsonify(message = message), constants.statusCode['success']

def dataResponse(data):
    return jsonify(data = data), constants.statusCode['success']


# To convert the data into immutable multidict in order for it to be compatible with the model
def toImmutableDictionary(data):
    return im.copy(json.loads(data.decode('utf8')))
