from flask import jsonify
import requests, json
from flask_jwt import JWT

class User(object):
    def __init__(self, id, name, error):
        self.id = id
        self.name = name
        self.error = error
    
    def getValues(self):
        return {'name':self.name , 'id':self.id, 'error': self.error}


def responseHandler(token, identity):
    user = identity.getValues()
    if user['error']:    
        return jsonify({'error': user['error']})
    else:
        return jsonify({'access_token': token.decode('utf-8'), 'name': user['name'], 'id': user['id'] })

def verify(email, password):
    responseObj = requests.post('https://hrms.solutionanalysts.com/php/auth/login',json.dumps({"email":email,"password":password})).json()
    if "msg" in responseObj.keys():
        loggedInUser = User(1, "", responseObj['msg'] )
    else:
        loggedInUser = User(responseObj['account']['id'], responseObj['account']['full_name'], "")
    return loggedInUser


def identity(payload):
    return {"userId": payload["identity"]}