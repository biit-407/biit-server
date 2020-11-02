from biit_server.utils import send_discord_message
from biit_server.http_responses import http400, http500, jsonHttp200
from biit_server.feedback import Feedback
from biit_server.database import Database
from biit_server.authentication import AuthenticatedType, authenticated
from biit_server.query_helper import validate_fields, ValidateType
from datetime import datetime
import uuid


@validate_fields(
    ["email", "title", "text", "feedback_type", "feedback_status", "token"],
    ValidateType.BODY,
)
@authenticated(AuthenticatedType.BODY)
def feedback_post(request, auth):
    """
    TODO

    """
    body = request.get_json()

    feedback_db = Database("feedback")

    feedback_id = uuid.uuid4()

    feedback = Feedback(
        id=feedback_id,
        email=body["email"],
        timestamp=body["timestamp"],
        title=body["title"],
        text=body["text"],
        feedback_type=body["feedback_type"],
        feedback_status=body["feedback_status"],
    )

    try:
        feedback_db.add(feedback, id=feedback_id)
    except:
        return http500(
            f"An error occured while attempting to submit feedback [{feedback}]",
            "stephen",
        )

    response = {
        "access_token": auth[0],
        "refresh_token": auth[1],
        "data": feedback.to_dict(),
    }
    return jsonHttp200("Feedback created", response)


@validate_fields(["email", "token", "id"], ValidateType.QUERY)
@authenticated(AuthenticatedType.QUERY)
def feedback_get(request, auth):
    """
    TODO

    """
    args = request.args
    feedback_db = Database("feedback")

    feedback_db_response = feedback_db.get(args["id"])

    if not feedback_db_response:
        return http400(
            f"Feedback with ID {args['id']} was not found in the Firestore database."
        )

    feedback = Feedback(document_snapshot=feedback_db_response)

    try:
        response = {
            "access_token": auth[0],
            "refresh_token": auth[1],
            "data": feedback.to_dict(),
        }
        return jsonHttp200("Feedback retrieved", response)
    except:
        return http500("Feedback not found")


@validate_fields(["email", "token", "id"], ValidateType.QUERY)
@authenticated(AuthenticatedType.QUERY)
def feedback_delete(request, auth):
    """
    TODO

    """
    # serializes the quert string to a dict (neeto)
    args = request.args

    # return community.delete(args)
    feedback_db = Database("feedback")

    try:
        feedback_db.delete(args["id"])
        response = {"access_token": auth[0], "refresh_token": auth[1]}
        return jsonHttp200("Feedback deleted", response)
    except:
        return http500("Feedback deletion error")


@validate_fields(
    ["email", "title", "text", "feedback_type", "feedback_status", "token"],
    ValidateType.QUERY,
)
@authenticated(AuthenticatedType.QUERY)
def report_user(request, auth):
    """Handles reporting a user per user request
    Validates data sent in a request then calls firestore to add the report

    Args:
        request: A request object that contains args with keys: email and file

    Returns:
        Http 200 returns success on submition

    Raises:
        Http 400 when the json is missing a key or the fils is not found
    """
    args = request.args

    feedback_db = Database("feedback")

    feedback_id = uuid.uuid4()

    feedback = Feedback(
        id=feedback_id,
        email=args["email"],
        timestamp=args["timestamp"],
        title=args["title"],
        text=args["text"],
        feedback_type=args["feedback_type"],
        feedback_status=args["feedback_status"],
    )

    try:
        feedback_db.add(feedback, id=feedback_id)
    except:
        return http500(
            f"An error occured while attempting to submit a report [{feedback}]",
            "sotails",
        )

    response = {
        "access_token": auth[0],
        "refresh_token": auth[1],
        "data": feedback.to_dict(),
    }
    return jsonHttp200("User Reported", response)
