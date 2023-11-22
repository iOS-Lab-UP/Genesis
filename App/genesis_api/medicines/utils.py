from genesis_api.models import Medicines
from genesis_api.tools.handlers import *
from genesis_api.tools.utils import *
from genesis_api import db
from sqlalchemy.orm import Session, joinedload, contains_eager
from sqlalchemy.exc import SQLAlchemyError

import logging


def get_all_medicines(page=1, per_page=100, search_term=None):
    """
    Get all medicines from the database with pagination and optional search.

    Args:
        page (int): The page number.
        per_page (int): The number of items per page.
        search_term (str, optional): The search term for filtering medicines. Default is None.

    Returns:
        list: A list containing medicines for the specified page and search criteria.
    """
    try:
        query = Medicines.query
        if search_term:
            # Adjust the field to match against if necessary
            query = query.filter(
                Medicines.short_composition2.like(f'%{search_term}%'))

        paginated_query = query.paginate(
            page=page, per_page=per_page, error_out=False)
        medicines = paginated_query.items
        if not medicines:
            raise ElementNotFoundError('Medicines not found')

        return [medicine.to_dict() for medicine in medicines]
    except SQLAlchemyError as e:
        logging.error(e)
        raise e
    except Exception as e:
        logging.error(e)
        raise e
