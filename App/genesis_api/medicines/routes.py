from flask import Blueprint
from genesis_api.medicines.utils import *
from genesis_api.tools.handlers import *
from genesis_api.tools.utils import parse_request, generate_response
from genesis_api.image_classifier.utils import *
from genesis_api.security import *
from genesis_api import db, limiter, cache

medicines_endpoint = Blueprint('medicines', __name__, url_prefix='/medicines')


@medicines_endpoint.route('get_all', methods=['GET'])
@token_required
@limiter.limit("30 per minute")  # Apply rate limiting
# Cache the result of this endpoint for 5 minutes
def get_medicines_endpoint(current_user) -> dict[str:str]:

    try:
        # Assuming there's a function to retrieve medical history in utils
        medicines = get_all_medicines()
        if medicines:
            return generate_response(True, 'Medical History retrieved successfully', medicines, 200), 200
        else:
            return generate_response(False, 'Medical History not found', None, 404), 404
    except Exception as e:
        return generate_response(False, 'Could not retrieve Medical History', None, 500, str(e)), 500
