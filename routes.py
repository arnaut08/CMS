from app import server
from flask import jsonify


# For all the undefined routes
@server.errorhandler(404)
def not_found(error):
    return jsonify(error='The requested URL was not found')