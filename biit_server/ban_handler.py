from .http_responses import http200, http400, jsonHttp200
from .query_helper import validate_body, validate_query_params
from .azure import azure_refresh_token


def ban_post(request):
    """Handles the ban post endpoint
    Validates data in from the request then calls the db to ban the user
    Args:
        request: A request object that contains a json object with keys: banner, banner, community, token

    Returns:
        (json): Http 200 string response with refresh token and new token of the banner

    Raises:
        Http 400 when the json is missing a key
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

    auth = azure_refresh_token(body["token"])
    if not auth[0]:
        return http400("Not Authenticated")
    # TODO Add tuple to response

    # TODO uncomment once db is implemented
    # return ban.add(args)

    # TODO remove once db is implemented
    return jsonHttp200(
        body["bannee"] + " has been banned",
        {"access_token": auth[0], "refresh_token": auth[1]},
    )


def ban_put(request):
    """Handles the ban PUT endpoint
    Validates the request and calls the db to unban the banner

    Args:
        request: A request object that contains a json object with keys: banner, bannee, community, token

    Returns:
        (json): Http 200 string response containing the banners refresh token and new token

    Raises:
        Http 400 when the json is missing a key
    """
    fields = ["banner", "bannee", "community", "token"]

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
    # return ban.remove(args)

    # TODO remove once db is implemented
    return jsonHttp200(
        args["bannee"] + " has been unbanned",
        {"access_token": auth[0], "refresh_token": auth[1]},
    )
