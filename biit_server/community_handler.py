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
    # TODO Add tuple ot response

    community_db = Database("communities")

    try:
        body["members"] = []
        community_db.add(body, id=body["name"])
    except:
        return http400("Community name already taken")

    return jsonHttp200(
        "Community Created", {"access_token": auth[0], "refresh_token": auth[1]}
    )

    # TODO uncomment once the DB is implemented
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
    fields = ["name"]

    # serializes the quert string to a dict (neeto)
    args = request.args

    query_validation = validate_query_params(args, fields)
    # check that body validation succeeded
    if query_validation[1] != 200:
        return query_validation

    community_db = Database("communities")

    try:
        return community_db.get(args["name"])
    except:
        return http400("Community name already taken")


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
    # TODO Add tuple ot response

    # TODO uncomment once db is implemented
    community_db = Database("communities")

    try:
        community_db.update(args["name"], args["updateFields"])
        return jsonHttp200(
            "Community Updated", {"access_token": auth[0], "refresh_token": auth[1]}
        )
    except:
        return http400("Community update error")


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
    # TODO Add tuple ot response

    # TODO uncomment once db is implemented
    # return community.delete(args)
    community_db = Database("communities")

    try:
        community_db.delete(args["name"])
        return jsonHttp200(
            "Community Deleted", {"access_token": auth[0], "refresh_token": auth[1]}
        )
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
    fields = ["name", "email", "token"]
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
    # TODO Add tuple to response

    # TODO @Ryan Create the DB stuff
    community_db = Database("communities")
    community = community_db.get(community_id).to_json()
    community_db.update(community_id, {"members": community["members"] + [body]})
    return jsonHttp200(
        "Community Joined", {"access_token": auth[0], "refresh_token": auth[1]}
    )


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
    fields = ["name", "token", "email"]
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
    # TODO Add tuple ot response

    community_db = Database("communities")
    community = community_db.get(community_id).to_json()
    community_db.update(
        community_id,
        {
            "members": [
                user for user in community["members"] if user["email"] != body["email"]
            ]
        },
    )
    return jsonHttp200(
        "Community Left", {"access_token": auth[0], "refresh_token": auth[1]}
    )
