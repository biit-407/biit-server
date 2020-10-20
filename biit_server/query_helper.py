from .http_responses import http200, http400
import json
import re


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
