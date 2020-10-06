from .http_responses import http200, http400
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


def validate_photo(filename: str):
    """Validate that a photo sent is of a specific extension

    Args:
        file (str): File sent from client
    Returns:
        (Boolean): True if file is valid, false if not
    """
    if not filename:
        return False
    if not re.match("([A-Za-z0-9])*.(jpg|png)", filename)[2]:
        return False
    return True
