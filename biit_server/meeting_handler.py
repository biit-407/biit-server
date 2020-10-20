import ast
import json
import random
import string

from .http_responses import http200, http400, jsonHttp200
from .query_helper import validate_query_params, validate_body
from .azure import azure_refresh_token
from .database import Database

from .meeting import Meeting, MeetingType


def meeting_post(request):
    """Handles the meeting POST endpoint
    Validates the keys in the request then calls the database to create a meeting
    Args:
        request: A request object that contains a json object with keys: name, codeofconduct, Admins, Members, mpm, meettype, token

    Returns:
        (json): Http 200 string response containing the  refresh token and new token

    Raises:
        Http 400 when the json is missing a key
    """
    fields = ["time", "location", "users", "meettype", "token"]
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

    meeting_db = Database("meetings")

    random_id = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(64))

    meeting = Meeting(
        user_list=body["users"],
        time_stamp=body["time"],
        duration=body["duration"],
        meeting_type=body["meettype"],
        location=body["location"],
        id=random_id
    )

    try:
        meeting_db.add(meeting, id=random_id)
    except:
        return http400("Meeting id already taken")

    response = {
        "access_token": auth[0],
        "refresh_token": auth[1],
        "data": meeting.to_dict(),
    }
    return jsonHttp200("Meeting created", response)


def meeting_get(request):
    """Handles the meeting GET endpoint
        Validates the keys in the request then calls the database to get information about a meeting
    Args:
        request: A request object that contains a json object with keys: id

    Returns:
        (str): Http 200 string response containing information about the searched meeting

    Raises:
        Http 400 when the json is missing a key
    """
    fields = ["id", "token"]

    args = request.args

    query_validation = validate_query_params(args, fields)

    if query_validation[1] != 200:
        return query_validation

    auth = azure_refresh_token(args["token"])
    if not auth[0]:
        return http400("Not Authenticated")

    meeting_db = Database("meetings")

    meeting_db_response = meeting_db.get(args["id"])

    if not meeting_db_response:
        return http400(f"Meeting with ID {args['id']} was not found in the Firestore database.")

    meeting = Meeting(document_snapshot=meeting_db_response)

    try:
        response = {
            "access_token": auth[0],
            "refresh_token": auth[1],
            "data": meeting.to_dict(),
        }
        return jsonHttp200("Meeting Received", response)
    except:
        return http400("Meeting not found")


def meeting_put(request):
    """Handles the community PUT endpoint
        Validates the keys in the request then calls the database to update a commmunity
    Args:
        request: A request object that contains a json object with keys: name, email, token, and (values to change for a community)

    Returns:
        (json): Http 200 string response containing the refresh token and new token

    Raises:
        Http 400 when the json is missing a key
    """
    fields = ["id", "token", "updateFields"]

    # serializes the quert string to a dict (neeto)
    args = request.args

    query_validation = validate_query_params(args, fields)
    # check that body validation succeeded
    if query_validation[1] != 200:
        return query_validation

    auth = azure_refresh_token(args["token"])
    if not auth[0]:
        return http400("Not Authenticated")

    meeting_db = Database("meetings")

    meeting_db.update(args["id"], ast.literal_eval(args["updateFields"]))

    updated_meeting_snapshot = meeting_db.get(args["id"])

    if not updated_meeting_snapshot:
        return http400(f"Error retrieving updated meeting with id {args['id']} from the Firestore database.")

    updated_rating = Meeting(document_snapshot=updated_meeting_snapshot)

    response = {
        "access_token": auth[0],
        "refresh_token": auth[1],
        "data": updated_rating.to_dict(),
    }

    return jsonHttp200("Meeting Updated", response)


def meeting_delete(request):
    """Handles the meeting DELETE endpoint
    Validates the keys in the request then calls the database to delete the meeting.
    Args:
        request: A request object that contains a json object with keys: id, token

    Returns:
        (json): Http 200 string response containing the refresh token and new token

    Raises:
        Http 400 when the json is missing a key
    """
    fields = ["id", "token"]

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
    meeting_db = Database("meetings")

    try:
        meeting_db.delete(args["id"])
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
