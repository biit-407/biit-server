import ast
from biit_server.authentication import AuthenticatedType, authenticated
import random
import string

from .http_responses import http400, jsonHttp200
from .query_helper import (
    ValidateType,
    validate_fields,
)
from .database import Database

from .meeting import (
    Meeting,
    MeetingFunction,
    UserInMeetingException,
    UserNotInMeetingException,
)


@validate_fields(
    ["timestamp", "location", "user_list", "meettype", "duration", "token"],
    ValidateType.BODY,
)
@authenticated(AuthenticatedType.BODY)
def meeting_post(request, auth):
    """Handles the meeting POST endpoint
    Validates the keys in the request then calls the database to create a meeting
    Args:
        request: A request object that contains a json object with keys: name, codeofconduct, Admins, Members, mpm, meettype, token, duration

    Returns:
        (json): Http 200 string response containing the  refresh token and new token

    Raises:
        Http 400 when the json is missing a key
    """
    body = request.get_json()

    meeting_db = Database("meetings")

    random_id = "".join(
        random.choice(string.ascii_letters + string.digits) for i in range(64)
    )

    meeting = Meeting(
        user_list=body["user_list"],
        timestamp=body["timestamp"],
        duration=body["duration"],
        meeting_type=body["meettype"],
        location=body["location"],
        id=random_id,
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


@validate_fields(["id", "token"], ValidateType.QUERY)
@authenticated(AuthenticatedType.QUERY)
def meeting_get(request, auth):
    """Handles the meeting GET endpoint
        Validates the keys in the request then calls the database to get information about a meeting
    Args:
        request: A request object that contains a json object with keys: id

    Returns:
        (str): Http 200 string response containing information about the searched meeting

    Raises:
        Http 400 when the json is missing a key
    """
    args = request.args

    meeting_db = Database("meetings")

    meeting_db_response = meeting_db.get(args["id"])

    if not meeting_db_response:
        return http400(
            f"Meeting with ID {args['id']} was not found in the Firestore database."
        )

    meeting = Meeting(document_snapshot=meeting_db_response)

    try:
        response = {
            "access_token": auth[0],
            "refresh_token": auth[1],
            "data": meeting.to_dict(),
        }
        return jsonHttp200("Meeting retrieved", response)
    except:
        return http400("Meeting not found")


@validate_fields(["id", "token", "updateFields"], ValidateType.QUERY)
@authenticated(AuthenticatedType.QUERY)
def meeting_put(request, auth):
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

    meeting_db = Database("meetings")

    meeting_db.update(args["id"], ast.literal_eval(args["updateFields"]))

    updated_meeting_snapshot = meeting_db.get(args["id"])

    if not updated_meeting_snapshot:
        return http400(
            f"Error retrieving updated meeting with id {args['id']} from the Firestore database."
        )

    updated_rating = Meeting(document_snapshot=updated_meeting_snapshot)

    response = {
        "access_token": auth[0],
        "refresh_token": auth[1],
        "data": updated_rating.to_dict(),
    }

    return jsonHttp200("Meeting updated", response)


@validate_fields(["id", "token"], ValidateType.QUERY)
@authenticated(AuthenticatedType.QUERY)
def meeting_delete(request, auth):
    """Handles the meeting DELETE endpoint
    Validates the keys in the request then calls the database to delete the meeting.
    Args:
        request: A request object that contains a json object with keys: id, token

    Returns:
        (json): Http 200 string response containing the refresh token and new token

    Raises:
        Http 400 when the json is missing a key
    """
    args = request.args

    # return community.delete(args)
    meeting_db = Database("meetings")

    try:
        meeting_db.delete(args["id"])
        response = {"access_token": auth[0], "refresh_token": auth[1]}
        return jsonHttp200("Meeting deleted", response)
    except:
        return http400("Meeting deletion error")


@validate_fields(["id", "email", "token", "function"], ValidateType.QUERY)
@authenticated(AuthenticatedType.QUERY)
def meeting_user_put(request, auth):
    """A handler function to join a meeting
    Validates the keys in the request then adds the user in the meeting.
    Args:
        request: A request object that contains a json object with keys: id, email, token, function.

    Returns:
        (json): Http 200 string response containing the refresh token and new token

    Raises:
        Http 400 when the json is missing a key
        Http 400 if the user is already in the meeting
    """
    args = request.args

    meeting_db = Database("meetings")

    meeting_snapshot = meeting_db.get(args["id"])

    if not meeting_snapshot:
        return http400(
            f"Error in retrieving meeting id {args['id']} from the Firestore database."
        )

    meeting = Meeting(document_snapshot=meeting_snapshot)

    if int(args["function"]) == MeetingFunction.REMOVE.value:
        try:
            new_users = meeting.remove_user(args["email"])
        except UserNotInMeetingException:
            return http400(f"User {args['email']} was not found in the meeting")
    elif int(args["function"]) == MeetingFunction.ADD.value:
        try:
            new_users = meeting.add_user(args["email"])
        except UserInMeetingException:
            return http400(f"User {args['email']} is already in this meeting!")
    else:
        return http400(
            f"Function value {args['function']} was not recognized by the server. Options are 0 to remove and 1 to add users."
        )

    try:
        meeting_db.update(args["id"], {"user_list": new_users})
        response = {
            "access_token": auth[0],
            "refresh_token": auth[1],
            "data": meeting.to_dict(),
        }
        return jsonHttp200(
            f"User {'added' if args['function'] else 'removed'}", response
        )
    except:
        return http400("Meeting update error")


def meeting_accept(request, id):

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

    meeting_db = Database("meetings")

    meeting_snapshot = meeting_db.get(id)

    if not meeting_snapshot:
        return http400(
            f"Error in retrieving meeting id {id} from the Firestore database."
        )

    meeting = Meeting(document_snapshot=meeting_snapshot)
    accepted_user = meeting.accept_meeting(args["email"])
    try:
        meeting_db.update(id, {"user_list": accepted_user})
        response = {
            "access_token": auth[0],
            "refresh_token": auth[1],
            "data": meeting.to_dict(),
        }
        return jsonHttp200("User accepted the meeting!", response)
    except:
        return http400("Meeting update error")


def meeting_decline(request, id):
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

    meeting_db = Database("meetings")

    meeting_snapshot = meeting_db.get(id)

    if not meeting_snapshot:
        return http400(
            f"Error in retrieving meeting id {id} from the Firestore database."
        )

    meeting = Meeting(document_snapshot=meeting_snapshot)
    declined_user = meeting.decline_meeting(args["email"])
    try:
        meeting_db.update(id, {"user_list": declined_user})
        response = {
            "access_token": auth[0],
            "refresh_token": auth[1],
            "data": meeting.to_dict(),
        }
        return jsonHttp200("User declined the meeting!", response)
    except:
        return http400("Meeting update error")


def meeting_set_venue(request, id):
    """Handles setting the venue of a meeting
    Args:
        request: A request object that contains a json object with keys: email, token, venue

    Returns:
        (json): Http 200 string response containing the refresh token and new token and meeting

    Raises:
        Http 400 when the json is missing a key
    """
    fields = ["email", "token", "venues"]

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

    meeting_snapshot = meeting_db.get(id)

    if not meeting_snapshot:
        return http400(
            f"Error in retrieving meeting id {id} from the Firestore database."
        )
    venues = json.loads(args["venues"])

    meeting = Meeting(document_snapshot=meeting_snapshot)

    venue = meeting.location

    if meeting.location:
        if meeting.location not in venues:
            venues.append(meeting.location)
            venue = random.choice(venues)
    else:
        venue = venues[0]
    meeting.location = venue
    try:
        meeting_db.update(id, {"location": venue})
        response = {
            "access_token": auth[0],
            "refresh_token": auth[1],
            "data": meeting.to_dict(),
        }
        return jsonHttp200("Venue has been set!", response)
    except:
        return http400("Meeting update error")
