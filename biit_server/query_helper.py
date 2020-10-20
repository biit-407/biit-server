from .http_responses import http200, http400
import json
import re
from enum import Enum
from typing import List


def validate_body(body, fields):
    """
    Validates that the given fields exist in the body
    """
    for field in fields:
        if field not in body:
            return http400(f"Missing field {field} in request")
    return http200()


def validate_query_params(query_params, fields):
    """
    Validates that the given fields exist in the body
    """
    for field in fields:
        if field not in query_params:
            return http400(f"Missing query parameter {field}")
    return http200()


def validate_update_field(params, fields):
    """
    Validates that the update fields contains an updatable field
    """
    if not params["updateFields"]:
        return http400(f"Update Field empty")

    if not fields:
        return http400(f"Fields not being set")

    try:
        updateField = json.loads(params["updateFields"].replace("'", '"'))
    except:
        return http400(f"Issue when serializing updateFields")

    for field in updateField:
        if field not in fields:
            return http400(f"Not a valid update field: {field}")

    return http200()


def validate_photo(filename: str):
    """Validate that a photo sent is of a specific extension

    Args:
        file (str): File sent from client
    Returns:
        (Boolean): True if file is valid, false if not
    """
    if not filename:
        return False
    if not re.match("([A-Za-z0-9])*.(jpg|png)", filename):
        return False
    return True


class ValidateType(Enum):
    BODY = 0
    """
    the token to authenticate with is located in the body 
    of the request
    """
    QUERY = 1
    """
    the token to authenticate with is located in the query
    parameters of the request
    """
    FORM = 2
    """
    the token to authenticate with is located in the body, 
    under the form section within the request
    """ 
    NONE = 3
    """
    there is no authentication for this request
    """


def validate_fields(fields: List[str], type: ValidateType = ValidateType.NONE):
    """
    Decorator for making sure a request has the correct fields

    Args:
        fields (List[str]): the fields to be validated
        type (ValidateType): the location of the fields

    """

    def decorator(func):
        def wrapper(request):
            if type == ValidateType.BODY:
                body = None
                try:
                    body = request.get_json()
                except:
                    return http400("Missing body")

                body_validation = validate_body(body, fields)
                # check that body validation succeeded
                if body_validation[1] != 200:
                    return body_validation

            if type == ValidateType.QUERY:
                args = request.args
                query_validation = validate_query_params(args, fields)
                # check that body validation succeeded
                if query_validation[1] != 200:
                    return query_validation

            if type == ValidateType.FORM:
                body = None
                try:
                    body = request.form
                except:
                    return http400("Missing body")

                body_validation = validate_body(body, fields)
                # check that body validation succeeded
                if body_validation[1] != 200:
                    return body_validation
                    
            result = func(request)
            return result

        return wrapper

    return decorator
