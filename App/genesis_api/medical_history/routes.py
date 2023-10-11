from flask import Blueprint
from sqlalchemy.orm import sessionmaker
from genesis_api.tools.handlers import *
from genesis_api.tools.utils import parse_request, generate_response
from genesis_api.image_classifier.utils import *
from genesis_api.security import *
from genesis_api import db, limiter, cache

medical_history = Blueprint('medical_history', __name__, url_prefix='/medical_history')
Session = sessionmaker(bind=db.engine)



@medical_history.route('/', methods=['GET'])
def get_medical_history():
    pass

@medical_history.route('/', methods=['POST'])
def create_medical_history():
    pass

@medical_history.route('/<int:id>', methods=['PUT'])
def update_medical_history(id):
    pass

@medical_history.route('/<int:id>', methods=['DELETE'])
def delete_medical_history(id):
    pass
