from biit_server.authentication import AuthenticatedType, authenticated
from .http_responses import jsonHttp200
from .query_helper import ValidateType, validate_fields
from .database import Database


@validate_fields(["banner", "bannee", "community", "token"], ValidateType.BODY)
@authenticated(AuthenticatedType.BODY)
def ban_post(request, auth):
    """Handles the ban post endpoint
    Validates data in from the request then calls the db to ban the user
    Args:
        request: A request object that contains a json object with keys: banner, banner, community, token

    Returns:
        (json): Http 200 string response with refresh token and new token of the banner

    Raises:
        Http 400 when the json is missing a key
    """
    body = request.get_json()  # wont fail because validation occurs first

    community_db = Database("communities")
    community = community_db.get(body["community"]).to_dict()
    community_db.update(
        body["community"],
        {"Members": [user for user in community["Members"] if user != body["bannee"]]},
    )

    ban_db = Database("communities")

    banned_user = ban_db.get(body["community"]).to_dict()

    insert_data = {
        "name": body["bannee"],
        "ordered_by": body["banner"],
    }

    banned_user["bans"].append(insert_data)

    ban_db.update(body["community"], {"bans": banned_user["bans"]})

    response = {"access_token": auth[0], "refresh_token": auth[1]}

    return jsonHttp200(body["bannee"] + " has been banned", response)


@validate_fields(["banner", "bannee", "community", "token"], ValidateType.QUERY)
@authenticated(AuthenticatedType.QUERY)
def ban_put(request, auth):
    """Handles the ban PUT endpoint
    Validates the request and calls the db to unban the banner

    Args:
        request: A request object that contains a json object with keys: banner, bannee, community, token

    Returns:
        (json): Http 200 string response containing the banners refresh token and new token

    Raises:
        Http 400 when the json is missing a key
    """
    # serializes the quert string to a dict (neeto)
    args = request.args  # wont fail because validation occurs first

    ban_db = Database("communities")

    banned_user = ban_db.get(args["community"]).to_dict()

    ban_db.update(
        args["community"],
        {
            "bans": [
                user for user in banned_user["bans"] if user["name"] != args["bannee"]
            ]
        },
    )

    response = {"access_token": auth[0], "refresh_token": auth[1]}

    return jsonHttp200(args["bannee"] + " has been unbanned", response)
