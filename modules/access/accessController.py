from flask import Blueprint, jsonify, request
from config import constants
import json
from modules.auth.authModel import AuthModel

accessBlueprint = Blueprint('accessBlueprint', __name__)

