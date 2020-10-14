import ast
import json

from .http_responses import http200, http400, jsonHttp200
from .query_helper import validate_query_params, validate_body
from .azure import azure_refresh_token
from .database import Database


def community_post(request):
    """Handles the community POST endpoint
    Validates the keys in the request then calls the database to create a commmunity
    Args:
        request: A request object that contains a json object with keys: name, codeofconduct, Admins, Members, mpm, meettype, token

    Returns:
        (json): Http 200 string response containing the  refresh token and new token

    Raises:
        Http 400 when the json is missing a key
    """
    fields = ["name", "codeofconduct", "Admins", "Members", "mpm", "meettype", "token"]
    body = None

    try:
        body = request.get_json()
    except:
        return http400("Missing body")

    body_validation = validate_body(body, fields)
    # check that body validation succeeded
    if body_validation[1] != 200:
        return body_validation

    auth = azure_refresh_token(body["token"])
    if not auth[0]:
        return http400("Not Authenticated")

    community_db = Database("communities")

    body["bans"] = []

    try:
        community_db.add(body, id=body["name"])
    except:
        return http400("Community name already taken")

    response = {
        "access_token": auth[0],
        "refresh_token": auth[1],
        "data": community_db.get(body["name"]).to_dict(),
    }
    return jsonHttp200("Community created", response)

    # this was commented out for testing purposes
    # return http400("Failed to create community")


def community_get(request):
    """Handles the community GET endpoint
        Validates the keys in the request then calls the database to get information about a commmunity
    Args:
        request: A request object that contains a json object with keys: name

    Returns:
        (str): Http 200 string response containing information about the searched community

    Raises:
        Http 400 when the json is missing a key
    """
    fields = ["name", "token"]

    args = request.args

    query_validation = validate_query_params(args, fields)

    if query_validation[1] != 200:
        return query_validation

    auth = azure_refresh_token(args["token"])
    if not auth[0]:
        return http400("Not Authenticated")

    community_db = Database("communities")

    try:
        response = {
            "access_token": auth[0],
            "refresh_token": auth[1],
            "data": community_db.get(args["name"]).to_dict(),
        }
        return jsonHttp200("Community Received", response)
    except:
        return http400("Community not found")


def community_put(request):
    """Handles the community PUT endpoint
        Validates the keys in the request then calls the database to update a commmunity
    Args:
        request: A request object that contains a json object with keys: name, email, token, and (values to change for a community)

    Returns:
        (json): Http 200 string response containing the refresh token and new token

    Raises:
        Http 400 when the json is missing a key
    """
    fields = ["name", "email", "token", "updateFields"]

    # serializes the quert string to a dict (neeto)
    args = request.args

    query_validation = validate_query_params(args, fields)
    # check that body validation succeeded
    if query_validation[1] != 200:
        return query_validation

    auth = azure_refresh_token(args["token"])
    if not auth[0]:
        return http400("Not Authenticated")

    community_db = Database("communities")

    community_db.update(args["name"], ast.literal_eval(args["updateFields"]))
    response = {
        "access_token": auth[0],
        "refresh_token": auth[1],
        "data": community_db.get(args["name"]).to_dict(),
    }
    return jsonHttp200("Community Updated", response)


def community_delete(request):
    """Handles the community DELETE endpoint
    Validates the keys in the request then calls the database to delete the commmunity
    Args:
        request: A request object that contains a json object with keys: name, email, token

    Returns:
        (json): Http 200 string response containing the refresh token and new token

    Raises:
        Http 400 when the json is missing a key
    """
    fields = ["email", "token", "name"]

    # serializes the quert string to a dict (neeto)
    args = request.args

    query_validation = validate_query_params(args, fields)
    # check that body validation succeeded
    if query_validation[1] != 200:
        return query_validation

    auth = azure_refresh_token(args["token"])
    if not auth[0]:
        return http400("Not Authenticated")

    # return community.delete(args)
    community_db = Database("communities")

    try:
        community_db.delete(args["name"])
        response = {"access_token": auth[0], "refresh_token": auth[1]}
        return jsonHttp200("Community Deleted", response)
    except:
        return http400("Community update error")


def community_join_post(request, community_id):
    """Handles the community joining POST endpoint
        Validates the keys in the request then calls the database to add a user to a community
    Args:
        request: A request object that contains a json object with keys: name, email, token

    Returns:
        (json): Http 200 string response containing the refresh token and new token

    Raises:
        Http 400 when the json is missing a key
    """
    fields = ["email", "token"]
    body = None

    try:
        body = request.get_json()
    except:
        return http400("Missing body")

    body_validation = validate_body(body, fields)
    # check that body validation succeeded
    if body_validation[1] != 200:
        return body_validation

    auth = azure_refresh_token(body["token"])
    if not auth[0]:
        return http400("Not Authenticated")

    community_db = Database("communities")
    community = community_db.get(community_id).to_dict()

    if body["email"] in community["Members"]:
        raise Exception

    community_db.update(
        community_id, {"Members": community["Members"] + [body["email"]]})
      
    response = {
        "access_token": auth[0],
        "refresh_token": auth[1],
        "data": community_db.get(community_id).to_dict(),
    }

    return jsonHttp200("Community Joined", response)


def community_leave_post(request, community_id):
    """Handles the community leaveing POST endpoint
        Validates the keys in the request then calls the database to remove a user from a community
    Args:
        request: A request object that contains a json object with keys: name, email, token

    Returns:
        (json): Http 200 string response containing the refresh token and new token

    Raises:
        Http 400 when the json is missing a key
    """
    fields = ["token", "email"]
    body = None

    try:
        body = request.get_json()
    except:
        return http400("Missing body")

    body_validation = validate_body(body, fields)
    # check that body validation succeeded
    if body_validation[1] != 200:
        return body_validation

    auth = azure_refresh_token(body["token"])
    if not auth[0]:
        return http400("Not Authenticated")

    community_db = Database("communities")
    community = community_db.get(community_id).to_dict()
    community_db.update(
        community_id,
        {"Members": [user for user in community["Members"] if user != body["email"]]},
    )
    response = {
        "access_token": auth[0],
        "refresh_token": auth[1],
        "data": community_db.get(community_id).to_dict(),
    }

    return jsonHttp200("Community Left", response)

