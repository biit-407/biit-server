from .http_responses import http200, http400
from .query_helper import *

def community_post(request):
    """
    Handles the community POST endpoint
    """
    fields = ["name", "codeofconduct", "Admins","Members","mpm","meettype"]
    body = None

    try:
        body = request.get_json()
    except:
        return http400("Missing body")

    body_validation = validate_body(body, fields)
    # check that body validation succeeded
    if body_validation[1] != 200:
        return body_validation

    # TODO @Ryan Create the DB stuff
    # if community.create(body):
    return http200("Community Created")

    # TODO uncomment once the DB is implemented
    # this was commented out for testing purposes
    # return http400("Failed to create community")


def community_get(request):
    """
    Handles the community GET endpoint
    """
    fields = ["name"]

    # serializes the quert string to a dict (neeto)
    args = request.args

    query_validation = validate_query_params(args, fields)
    # check that body validation succeeded
    if query_validation[1] != 200:
        return query_validation

    # TODO uncomment once db is implemented
    # return community.get(args)

    # TODO remove once db is implemented
    return http200("Community Returned")


def community_put(request):
    """
    Handles the community PUT endpoint
    """
    fields = ["name","email","token"]

    # serializes the quert string to a dict (neeto)
    args = request.args

    query_validation = validate_query_params(args, fields)
    # check that body validation succeeded
    if query_validation[1] != 200:
        return query_validation

    if not authenticate_community(args["email"],args["token"]):
        return http400("Invalid Administrative privilege")

    # TODO uncomment once db is implemented
    # return community.update(args)

    # TODO remove once db is implemented
    return http200("community Updated")


def community_delete(request):
    """
    Handles the community DELETE endpoint
    """
    fields = ["email","token","name"]

    # serializes the quert string to a dict (neeto)
    args = request.args

    query_validation = validate_query_params(args, fields)
    # check that body validation succeeded
    if query_validation[1] != 200:
        return query_validation

    if not authenticate_community(args["email"],args["token"]):
        return http400("Invalid Administrative privilege")

    # TODO uncomment once db is implemented
    # return community.delete(args)

    # TODO remove once db is implemented
    return http200("community Deleted")
