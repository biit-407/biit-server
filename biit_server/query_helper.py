from .http_responses import http200, http400

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

def authenticate_token(token):
        #TODO DB method for verifying token
        #account.auth()
        
    return True
