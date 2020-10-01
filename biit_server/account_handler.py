from .http_responses import http200, http400
from .query_helper import *
from .database import (
    Database
)

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
    account_db = Database("accounts")

    try:
        account_db.add(body, id=body["email"])
    except:
        return http400("Email already taken")


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

    account_db = Database("accounts")

    try:
        return account_db.get(args["email"])
    except:
        return http400("Account not found")


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

    # TODO Add Authentication

    # TODO uncomment once db is implemented

    account_db = Database("accounts")

    try:
        account_db.update(args["email"], args["updateFields"])
        return http200("Account updated")
    except:
        return http400("Account update error")


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

    # TODO Add Authentication

    # TODO uncomment once db is implemented

    account_db = Database("accounts")
    try:
        account_db.delete(args["email"])
        return http200("Account deleted")
    except:
        return http400("Error in account deletion")