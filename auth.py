from flask import jsonify
import requests, json
from flask_jwt import JWT

class User(object):
    def __init__(self, id, name):
        self.id = id
        self.name = name
    
    def getName(self):
        return self.name

def responseHandler(token, identity):
    name = identity.getName()
    return jsonify({'access_token': token.decode('utf-8'), 'name': name})


def verify(email, password):
    responseObj = requests.post('https://hrms.solutionanalysts.com/php/auth/login',json.dumps({"email":email,"password":password})).json()
    loggedInUser = User(responseObj['account']['id'],responseObj['account']['full_name'] )
    return loggedInUser


def identity(payload):
    return {"userId": payload["identity"]}