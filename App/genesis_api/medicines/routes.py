from flask import request
from flask import Blueprint
from genesis_api.medicines.utils import *
from genesis_api.tools.handlers import *
from genesis_api.tools.utils import parse_request, generate_response
from genesis_api.image_classifier.utils import *
from genesis_api.security import *
from genesis_api import db, limiter, cache

medicines_endpoint = Blueprint('medicines', __name__, url_prefix='/medicines')


@medicines_endpoint.route('/get_all', defaults={'page': 1, 'per_page': 100}, methods=['GET'])
@medicines_endpoint.route('/get_all/<int:page>', defaults={'per_page': 100}, methods=['GET'])
@medicines_endpoint.route('/get_all/<int:page>/<int:per_page>', methods=['GET'])
@token_required
@limiter.limit("30 per minute")  # Apply rate limiting
def get_medicines_endpoint(current_user, page=1, per_page=100) -> dict[str:str]:
    try:
        # Retrieve the search term from query parameters
        search_term = request.args.get('search', type=str)

        # Call the modified get_all_medicines function with pagination and search term
        medicines = get_all_medicines(page, per_page, search_term)
        if medicines:
            return generate_response(True, 'Medical History retrieved successfully', medicines, 200), 200
        else:
            return generate_response(False, 'Medical History not found', None, 404), 404
    except Exception as e:
        return generate_response(False, 'Could not retrieve Medical History', None, 500, str(e)), 500
