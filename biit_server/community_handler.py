import ast
from biit_server.utils import send_discord_message
from biit_server.authentication import AuthenticatedType, authenticated

from .http_responses import http400, http401, http500, jsonHttp200
from .query_helper import (
    ValidateType,
    validate_fields,
    validate_body,
)
from .azure import azure_refresh_token
from .database import Database


@validate_fields(
    ["name", "codeofconduct", "Admins", "Members", "mpm", "meettype", "token"],
    ValidateType.BODY,
)
@authenticated(AuthenticatedType.BODY)
def community_post(request, auth):
    """Handles the community POST endpoint
    Validates the keys in the request then calls the database to create a commmunity
    Args:
        request: A request object that contains a json object with keys: name, codeofconduct, Admins, Members, mpm, meettype, token

    Returns:
        (json): Http 200 string response containing the  refresh token and new token

    Raises:
        Http 400 when the json is missing a key
    """
    body = request.get_json()

    community_db = Database("communities")

    body["bans"] = []

    try:
        community_db.add(body, id=body["name"])
    except:
        send_discord_message(
            f'Attempted to create a community with an existing name [{body["name"]}]'
        )
        return http400("Community name already taken")

    response = {
        "access_token": auth[0],
        "refresh_token": auth[1],
        "data": community_db.get(body["name"]).to_dict(),
    }
    return jsonHttp200("Community created", response)


@validate_fields(["name", "token"], ValidateType.QUERY)
@authenticated(AuthenticatedType.QUERY)
def community_get(request, auth):
    """Handles the community GET endpoint
        Validates the keys in the request then calls the database to get information about a commmunity
    Args:
        request: A request object that contains a json object with keys: name

    Returns:
        (str): Http 200 string response containing information about the searched community

    Raises:
        Http 400 when the json is missing a key
    """
    args = request.args

    community_db = Database("communities")

    try:
        response = {
            "access_token": auth[0],
            "refresh_token": auth[1],
            "data": community_db.get(args["name"]).to_dict(),
        }
        return jsonHttp200("Community Received", response)
    except:
        send_discord_message(
            f"The community with the name [{args['name']}] does not exist"
        )
        return http400("Community not found")


@validate_fields(["name", "email", "token", "updateFields"], ValidateType.QUERY)
@authenticated(AuthenticatedType.QUERY)
def community_put(request, auth):
    """Handles the community PUT endpoint
        Validates the keys in the request then calls the database to update a commmunity
    Args:
        request: A request object that contains a json object with keys: name, email, token, and (values to change for a community)

    Returns:
        (json): Http 200 string response containing the refresh token and new token

    Raises:
        Http 400 when the json is missing a key
    """
    args = request.args

    community_db = Database("communities")

    community_db.update(args["name"], ast.literal_eval(args["updateFields"]))
    response = {
        "access_token": auth[0],
        "refresh_token": auth[1],
        "data": community_db.get(args["name"]).to_dict(),
    }
    return jsonHttp200("Community Updated", response)


@validate_fields(["email", "token", "name"], ValidateType.QUERY)
@authenticated(AuthenticatedType.QUERY)
def community_delete(request, auth):
    """Handles the community DELETE endpoint
    Validates the keys in the request then calls the database to delete the commmunity
    Args:
        request: A request object that contains a json object with keys: name, email, token

    Returns:
        (json): Http 200 string response containing the refresh token and new token

    Raises:
        Http 400 when the json is missing a key
    """
    args = request.args

    community_db = Database("communities")

    try:
        community_db.delete(args["name"])
        response = {"access_token": auth[0], "refresh_token": auth[1]}
        return jsonHttp200("Community Deleted", response)
    except:
        send_discord_message(f"Unable to delete community [{args['name']}]")
        return http500("Community delete error")


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
        send_discord_message(
            f"unable to parse body for request handler [community_join_post]"
        )
        return http400("Missing body")

    body_validation = validate_body(body, fields)
    # check that body validation succeeded
    if body_validation[1] != 200:
        send_discord_message(
            f"body validation failed for account {body['email']}. {body_validation[0]}"
        )
        return body_validation

    auth = azure_refresh_token(body["token"])
    if not auth[0]:
        send_discord_message(
            f"body authentication failed for account {body['email']}")
        return http401("Not Authenticated")

    community_db = Database("communities")
    community = community_db.get(community_id).to_dict()

    if body["email"] in community["Members"]:
        send_discord_message(
            f'Account [{body["email"]}] is already in community [{community_id}]'
        )
        raise Exception

    community_db.update(
        community_id, {"Members": community["Members"] + [body["email"]]}
    )

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
        send_discord_message(
            f"unable to parse body for request handler [community_leave_post]"
        )
        return http400("Missing body")

    body_validation = validate_body(body, fields)
    # check that body validation succeeded
    if body_validation[1] != 200:
        send_discord_message(
            f"body validation failed for account {body['email']}. {body_validation[0]}"
        )
        return body_validation

    auth = azure_refresh_token(body["token"])
    if not auth[0]:
        send_discord_message(
            f"body authentication failed for account {body['email']}")
        return http401("Not Authenticated")

    community_db = Database("communities")
    community = community_db.get(community_id).to_dict()
    community_db.update(
        community_id,
        {"Members": [user for user in community["Members"]
                     if user != body["email"]]},
    )
    response = {
        "access_token": auth[0],
        "refresh_token": auth[1],
        "data": community_db.get(community_id).to_dict(),
    }

    return jsonHttp200("Community Left", response)
