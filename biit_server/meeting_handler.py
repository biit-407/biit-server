import ast
from copy import deepcopy
from biit_server.rating import Rating
from datetime import datetime, timedelta
from biit_server.utils import send_discord_message
import json
from biit_server.authentication import AuthenticatedType, authenticated
import random
import string

import uuid

from .http_responses import http400, http401, http500, jsonHttp200
from .query_helper import ValidateType, validate_fields, validate_query_params
from .database import Database

from .meeting import (
    Meeting,
    MeetingFunction,
    UserInMeetingException,
    UserNotInMeetingException,
)
from .azure import azure_refresh_token


@validate_fields(
    [
        "timestamp",
        "location",
        "user_list",
        "meettype",
        "duration",
        "community",
        "token",
    ],
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
    community_db = Database("communities")
    community = community_db.get(body["community"]).to_dict()

    random_id = "".join(
        random.choice(string.ascii_letters + string.digits) for i in range(64)
    )

    meeting = Meeting(
        user_list=body["user_list"],
        timestamp=body["timestamp"],
        duration=body["duration"],
        meeting_type=body["meettype"],
        location=body["location"],
        community=community["id"],
        id=random_id,
    )

    try:
        meeting_db.add(meeting.to_dict(), id=random_id)
    except:
        send_discord_message(f"Meeting with id [{random_id}] is already in use")
        return http400("Meeting id already taken")

    rating_db = Database("ratings")
    rating = Rating(
        meeting_id=random_id,
        rating_dict={user: -1 for user in body["user_list"]},
        community=community["id"],
    )

    try:
        rating_db.add(rating.to_dict(), id=random_id)
        print("success")
    except:
        send_discord_message(f"Rating with id [{random_id}] is already in use")
        return http400("Rating id already taken")

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
        send_discord_message(f'Meeting with id [{args["id"]}] does not exist')
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
        return http500(
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
        send_discord_message(f'Error deleting meeting with id [{args["id"]}]')
        return http500("Meeting deletion error")


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
        return http500("Meeting update error")


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
        return http401("Not Authenticated")

    meeting_db = Database("meetings")

    meeting_snapshot = meeting_db.get(id)

    if not meeting_snapshot:
        return http400(
            f"Error in retrieving meeting id {id} from the Firestore database."
        )

    meeting = Meeting(document_snapshot=meeting_snapshot)
    accepted_user = meeting.accept_meeting(args["email"])
    try:
        result = meeting_db.update(id, {"user_list": accepted_user})

        if not result:
            return http500("Error updating meeting")

        user_count = 0
        for _, status in accepted_user.items():
            # user has accepted
            if status == 1:
                user_count += 1

        # check if meetup is fully accepted
        # we can only update if this person
        # accepting the meetup brings the total
        # count to 2 people (any more is a no op)
        if user_count == 2:
            # update the community stats to have
            # one more accepted meetup
            try:
                community_stat_db = Database("community_stats")
                community_stats = community_stat_db.get(meeting.community).to_dict()
                community_stat_db.update(
                    community_stats["community"],
                    {"accepted_meetups": community_stats["accepted_meetups"] - 1},
                )
            except:
                send_discord_message(
                    f"Failed to update community stats. The meetup was still successfully accepted"
                )

        response = {
            "access_token": auth[0],
            "refresh_token": auth[1],
            "data": meeting.to_dict(),
        }
        return jsonHttp200("User accepted the meeting!", response)
    except:
        return http500("Meeting update error")


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
        return http401("Not Authenticated")

    meeting_db = Database("meetings")

    meeting_snapshot = meeting_db.get(id)

    if not meeting_snapshot:
        return http400(
            f"Error in retrieving meeting id {id} from the Firestore database."
        )

    meeting = Meeting(document_snapshot=meeting_snapshot)
    declined_user = meeting.decline_meeting(args["email"])
    try:
        result = meeting_db.update(id, {"user_list": declined_user})
        if not result:
            return http500("Error updating meeting")

        user_count = 0
        for _, status in declined_user.items():
            # user has accepted
            if status == 1:
                user_count += 1

        # check if meetup is no longer fully accepted
        if user_count < 2:
            # update the community stats to have
            # one less accepted meetup
            try:
                community_stat_db = Database("community_stats")
                community_stats = community_stat_db.get(meeting.community).to_dict()
                community_stat_db.update(
                    community_stats["community"],
                    {"accepted_meetups": community_stats["accepted_meetups"] - 1},
                )
            except:
                send_discord_message(
                    f"Failed to update community stats. The meetup was still successfully declined"
                )

        response = {
            "access_token": auth[0],
            "refresh_token": auth[1],
            "data": meeting.to_dict(),
        }
        return jsonHttp200("User declined the meeting!", response)
    except:
        return http500("Meeting update error")


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
        return http401("Not Authenticated")

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
        return http500("Meeting update error")


@validate_fields(["email", "token"], ValidateType.QUERY)
@authenticated(AuthenticatedType.QUERY)
def meetings_get_all(request, auth):
    """Handles the meeting GET endpoint
        Validates the keys in the request then calls the database to get all meetings that the supplied email is a part of.
    Args:
        request: A request object that contains a json object with keys: email, token.

    Returns:
        (str): Http 200 string response containing information about the searched meeting

    Raises:
        Http 400 when the json is missing a key
    """
    args = request.args

    meeting_db = Database("meetings")

    meeting_db_response = meeting_db.collection_ref.get()

    meetings = [
        Meeting(document_snapshot=meeting_snapshot)
        for meeting_snapshot in meeting_db_response
    ]

    filtered_meetings = [
        meeting.to_dict() for meeting in meetings if args["email"] in meeting.user_list
    ]

    try:
        response = {
            "access_token": auth[0],
            "refresh_token": auth[1],
            "data": filtered_meetings,
        }
        return jsonHttp200("Meetings retrieved", response)
    except:
        send_discord_message(f'Meetings with id [{args["id"]}] do not exist')
        return http400("Meetings not found")


@validate_fields(["email", "token"], ValidateType.QUERY)
@authenticated(AuthenticatedType.QUERY)
def meetings_get_pending(request, auth):
    """Handles the meeting GET endpoint
        Validates the keys in the request then calls the database to get all meetings that the supplied email is a part of.
    Args:
        request: A request object that contains a json object with keys: email, token.

    Returns:
        (str): Http 200 string response containing information about the searched meeting

    Raises:
        Http 400 when the json is missing a key
    """
    args = request.args

    meeting_db = Database("meetings")

    meeting_db_response = meeting_db.collection_ref.get()

    meetings = [
        Meeting(document_snapshot=meeting_snapshot)
        for meeting_snapshot in meeting_db_response
    ]

    filtered_meetings = [
        meeting.to_dict()
        for meeting in meetings
        if args["email"] in meeting.user_list and meeting.user_list[args["email"]] == 0
    ]

    try:
        response = {
            "access_token": auth[0],
            "refresh_token": auth[1],
            "data": filtered_meetings,
        }
        return jsonHttp200("Meetings retrieved", response)
    except:
        send_discord_message(f'Meetings with id [{args["id"]}] do not exist')
        return http400("Meetings not found")


@validate_fields(["email", "token"], ValidateType.QUERY)
@authenticated(AuthenticatedType.QUERY)
def meetings_get_upcoming(request, auth):
    """Handles the meeting GET endpoint
        Validates the keys in the request then calls the database to get all meetings that the supplied email is a part of.
    Args:
        request: A request object that contains a json object with keys: email, token.

    Returns:
        (str): Http 200 string response containing information about the searched meeting

    Raises:
        Http 400 when the json is missing a key
    """
    args = request.args

    meeting_db = Database("meetings")

    meeting_db_response = meeting_db.collection_ref.get()

    meetings = [
        Meeting(document_snapshot=meeting_snapshot)
        for meeting_snapshot in meeting_db_response
    ]

    filtered_meetings = [
        meeting
        for meeting in meetings
        if args["email"] in meeting.user_list
        and meeting.user_list[args["email"]] == 1
        and datetime.utcfromtimestamp(meeting.timestamp) > datetime.now()
    ]

    # This sorts by the time of the meeting
    meeting_dict = {meeting.id: meeting for meeting in filtered_meetings}
    meeting_times = {meeting.id: meeting.timestamp for meeting in filtered_meetings}
    sorted_meeting_times = sorted(meeting_times.items(), key=lambda kv: (kv[1], kv[0]))

    return_meetings = [meeting_dict[key[0]].to_dict() for key in sorted_meeting_times]

    try:
        response = {
            "access_token": auth[0],
            "refresh_token": auth[1],
            "data": return_meetings,
        }
        return jsonHttp200("Meetings retrieved", response)
    except:
        send_discord_message(f'Meetings with id [{args["id"]}] do not exist')
        return http400("Meetings not found")


@validate_fields(["email", "token"], ValidateType.QUERY)
@authenticated(AuthenticatedType.QUERY)
def meetings_get_past(request, auth):
    """Handles the meeting GET endpoint
        Validates the keys in the request then calls the database to get all meetings that the supplied email is a part of.
    Args:
        request: A request object that contains a json object with keys: email, token.

    Returns:
        (str): Http 200 string response containing information about the searched meeting

    Raises:
        Http 400 when the json is missing a key
    """
    args = request.args

    meeting_db = Database("meetings")

    meeting_db_response = meeting_db.collection_ref.get()

    meetings = [
        Meeting(document_snapshot=meeting_snapshot)
        for meeting_snapshot in meeting_db_response
    ]

    filtered_meetings = [
        meeting.to_dict()
        for meeting in meetings
        if args["email"] in meeting.user_list
        and meeting.user_list[args["email"]] == 1
        and datetime.utcfromtimestamp(meeting.timestamp) < datetime.now()
    ]

    try:
        response = {
            "access_token": auth[0],
            "refresh_token": auth[1],
            "data": filtered_meetings,
        }
        return jsonHttp200("Meetings retrieved", response)
    except:
        send_discord_message(f'Meetings with id [{args["id"]}] do not exist')
        return http400("Meetings not found")


@validate_fields(["email", "community", "token"], ValidateType.QUERY)
@authenticated(AuthenticatedType.QUERY)
def matchup(request, auth):
    """Handles the meeting GET endpoint
        Generates meetings for everyone in the community that is specified after validating
        that the invokee has the correct permissions.
    Args:
        request: A request object that contains a json object with keys: email, community, token.

    Returns:
        (str): Http 200 string response containing information about the searched meeting

    Raises:
        Http 400 when the json is missing a key
    """
    args = request.args

    community_db = Database("communities")
    community_stat_db = Database("community_stats")

    community = community_db.get(args["community"]).to_dict()
    community_stats = community_stat_db.get(args["community"]).to_dict()

    if args["email"] not in community["Admins"]:
        return http401("User not authorized to start the matchup algorithm")

    users = community["Members"]

    random.shuffle(users)

    matches = []
    tmp = []

    for index, user in enumerate(users):
        tmp.append(user)

        if index % 2:
            matches.append(deepcopy(tmp))
            tmp = []

    meeting_list = []

    now = datetime.now()
    in_a_week = now + timedelta(hours=168)

    rating_db = Database("ratings")

    meeting_db = Database("meetings")
    failed_meetup_count = 0

    for match in matches:
        random_id = str(uuid.uuid4())
        meeting = Meeting(
            user_list={user: 0 for user in match},
            id=random_id,
            timestamp=in_a_week.timestamp(),
            location="WALC",
            meeting_type="In-Person",
            duration=30,
            community=community["id"],
        )

        try:
            meeting_db.add(meeting.to_dict(), id=random_id)
            meeting_list.append(meeting.to_dict())
        except:
            send_discord_message(
                f"Generating meetup {random_id} with {match} has failed"
            )
            failed_meetup_count += 1

        rating = Rating(
            meeting_id=random_id,
            rating_dict={user: -1 for user in match},
            community=community["id"],
        )

        try:
            rating_db.add(rating.to_dict(), id=random_id)
        except:
            send_discord_message(f"Rating with id [{random_id}] is already in use")
            return http400("Rating id already taken")

    try:
        community_stat_db.update(
            community["id"],
            {
                "total_meetups": community_stats["total_meetups"]
                + len(matches)
                - failed_meetup_count,
                "total_sessions": community_stats["total_sessions"] + 1,
            },
        )
    except:
        send_discord_message(
            f"Error updating community stats for community [{community['id']}]"
        )
        #! No error message is generated because the community still has the meetups generated properly

    response = {
        "access_token": auth[0],
        "refresh_token": auth[1],
        "data": meeting_list,
    }

    return jsonHttp200("Meetings created", response)
