from .http_responses import http200, http400
from .query_helper import *


def ban_post(request):
    """
    Handles the community PUT endpoint
    """
    fields = ["banner", "bannee", "community", "token"]
    body = None

    try:
        body = request.get_json()
    except:
        return http400("Missing body")

    body_validation = validate_body(body, fields)
    # check that body validation succeeded
    if body_validation[1] != 200:
        return body_validation

    # TODO Add Authentication

    # TODO uncomment once db is implemented
    # return ban.add(args)

    # TODO remove once db is implemented
    return http200(body["bannee"] + " has been banned")


def ban_put(request):
    """
    Handles the community PUT endpoint
    """
    fields = ["banner", "bannee", "community", "token"]

    # serializes the quert string to a dict (neeto)
    args = request.args

    query_validation = validate_query_params(args, fields)
    # check that body validation succeeded
    if query_validation[1] != 200:
        return query_validation

    # TODO Add Authentication

    # TODO uncomment once db is implemented
    # return ban.remove(args)

    # TODO remove once db is implemented
    return http200(args["bannee"] + " has been unbanned")
