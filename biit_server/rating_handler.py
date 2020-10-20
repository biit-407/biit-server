from .http_responses import http200, http400, jsonHttp200
from .query_helper import validate_query_params, validate_body
from .azure import azure_refresh_token
from .database import Database
from .rating import Rating, RatingAlreadySetException


def rating_post(request):
    """Handles the rating POST endpoint
    Validates the keys in the request then calls the database to create a commmunity
    Args:
        request: A request object that contains a json object with keys: name, codeofconduct, Admins, Members, mpm, meettype, token

    Returns:
        (json): Http 200 string response containing the  refresh token and new token

    Raises:
        Http 400 when the json is missing a key
    """
    fields = ["meeting_id", "user", "rating" "token"]
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

    rating_db = Database("ratings")

    rating_snapshot = rating_db.get(body["meeting_id"])

    if rating_snapshot == False:
        rating = Rating(
            meeting_id=body["meeting_id"], rating_dict={body["user"], body["rating"]}
        )
    else:
        rating = Rating(document_snapshot=rating_snapshot)
        try:
            rating.set_rating(body["user"], body["rating"])
        except RatingAlreadySetException:
            return http400(f"Rating for user {body['user']} has already been set")

    success = rating_db.update(body["meeting_id"], rating.get_ratings())

    if not success:
        return http400(
            f"Error in updating meeting id {body['meeting_id']} in Firestore database."
        )

    response = {
        "access_token": auth[0],
        "refresh_token": auth[1],
        "data": rating.to_dict(),
    }

    return jsonHttp200("Rating created", response)


def rating_get(request):
    """Handles the rating GET endpoint
        Validates the keys in the request then calls the database to get information about a commmunity
    Args:
        request: A request object that contains a json object with keys: name

    Returns:
        (str): Http 200 string response containing information about the searched community

    Raises:
        Http 400 when the json is missing a key
    """
    fields = ["meeting_id", "token"]

    args = request.args

    query_validation = validate_query_params(args, fields)

    if query_validation[1] != 200:
        return query_validation

    auth = azure_refresh_token(args["token"])
    if not auth[0]:
        return http400("Not Authenticated")

    rating_db = Database("ratings")

    rating = rating_db.get("meeting_id")

    if not rating:
        return http400(f"Error in retrieving rating from Firestore database.")

    try:
        response = {
            "access_token": auth[0],
            "refresh_token": auth[1],
            "data": rating.to_dict(),
        }
        return jsonHttp200("Rating Received", response)
    except:
        return http400("Rating not found")
