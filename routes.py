from app import server
from flask import jsonify
from modules.credential.credentialController import credentialBlueprint
from modules.auth.authController import authBlueprint

server.register_blueprint(credentialBlueprint, url_prefix= "/credential")
server.register_blueprint(authBlueprint, url_prefix= "/login")

# For all the undefined routes
@server.errorhandler(404)
@server.errorhandler(405)
def not_found(error):
    return jsonify(error='The requested URL was not found'), error.code

# Internal server error handling
@server.errorhandler(500)
def internalServer(error):
    return jsonify(error='Internal Server error'), error.code
    
