from app import server
from flask import jsonify
from modules.credential.credentialController import credentialBlueprint

server.register_blueprint(credentialBlueprint)

# For all the undefined routes
@server.errorhandler(404)
@server.errorhandler(405)
def not_found(error):
    return jsonify(error='The requested URL was not found')
