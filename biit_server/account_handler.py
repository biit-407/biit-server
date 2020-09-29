from .http_responses import http200, http400
from .query_helper import *
from .azure import azure_refresh_token


def account_post(request):
    """
    Handles the account POST endpoint
    """
    fields = ["fname", "lname", "email"]
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
    # if account.create(body):
    return http200("Account Created")

    # TODO uncomment once the DB is implemented
    # this was commented out for testing purposes
    # return http400("Failed to create account")


def account_get(request):
    """
    Handles the account GET endpoint
    """
    fields = ["email"]

    # serializes the quert string to a dict (neeto)
    args = request.args

    query_validation = validate_query_params(args, fields)
    # check that body validation succeeded
    if query_validation[1] != 200:
        return query_validation

    # TODO uncomment once db is implemented
    # return account.get(args)

    # TODO remove once db is implemented
    return http200("Account Returned")


def account_put(request):
    """
    Handles the account PUT endpoint
    """
    fields = ["email", "token"]

    # serializes the quert string to a dict (neeto)
    args = request.args

    query_validation = validate_query_params(args, fields)
    # check that body validation succeeded
    if query_validation[1] != 200:
        return query_validation

    auth = azure_refresh_token(args["token"])
    if not auth[0]:
        return http400("Not Authenticated")
    # TODO Add tuple to response

    # TODO uncomment once db is implemented
    # return account.update(args)

    # TODO remove once db is implemented
    return http200("Account Updated")


def account_delete(request):
    """
    Handles the account DELETE endpoint
    """
    fields = ["email", "token"]

    # serializes the quert string to a dict (neeto)
    args = request.args

    query_validation = validate_query_params(args, fields)
    # check that body validation succeeded
    if query_validation[1] != 200:
        return query_validation

    auth = azure_refresh_token(args["token"])
    if not auth[0]:
        return http400("Not Authenticated")
    # TODO Add tuple to response

    # TODO uncomment once db is implemented
    # return account.delete(args)

    # TODO remove once db is implemented
    return http200("Account Deleted")
