import ast

from .http_responses import http200, http400, jsonHttp200
from .query_helper import validate_body, validate_query_params, validate_photo
from .azure import azure_refresh_token
from .database import Database
from .storage import Storage
from flask import send_file
import base64


def account_post(request):
    """Handles the account POST endpoint
    Validates data sent in a request then calls the database to add an account

    Args:
        request: A request object that contains a json object with keys: fname, lname, email

    Returns:
        Http 200 string response

    Raises:
        Http 400 when the json is missing a key
    """
    fields = ["fname", "lname", "email", "token"]
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

    account_db = Database("accounts")

    try:
        db_entry = {
            "fname": body["fname"],
            "lname": body["lname"],
            "email": body["email"],
        }

        account_db.add(db_entry, id=body["email"])
    except:
        return http400("Email already taken")

    response = {
        "fname": body["fname"],
        "lname": body["lname"],
        "email": body["email"],
        "access_token": auth[0],
        "refresh_token": auth[1],
    }

    return jsonHttp200("Account Created", response)


def account_get(request):
    """Handles the account GET endpoint
    Validates data sent in a request then calls the database to get the row of the associated account

    Args:
        request: A request object that contains args with keys: email

    Returns:
        (json) Http 200 string response with the associated account information

    Raises:
        Http 400 when the json is missing a key
    """
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

    account_db = Database("accounts")

    try:
        return jsonHttp200(
            "Account returned",
            {
                "access_token": auth[0],
                "refresh_token": auth[1],
                "data": account_db.get(args["email"]).to_dict(),
            },
        )
    except:
        return http400("Account not found")


def account_put(request):
    """Handles the account POST endpoint
    Validates data sent in a request then calls the database to edit the row of the account

    Args:
        request: A request object that contains args with keys: email, token, and (any account values to be changed)

    Returns:
        (json): Http 200 string response with refresh token and new token

    Raises:
        Http 400 when the json is missing required keys: email, token
        or if the token is not valid
    """
    fields = ["email", "token", "updateFields"]

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

    account_db = Database("accounts")

    try:
        account_db.update(args["email"], ast.literal_eval(args["updateFields"]))
        response = account_db.get(args["email"]).to_dict()
        response["access_token"] = auth[0]
        response["refresh_token"] = auth[1]
        return jsonHttp200("Account Updated", response)
    except:
        return http400("Account update error")


def account_delete(request):
    """Handles the account DELETE endpoint
    Validates data sent in a request then calls the database to remove the associated account

    Args:
        request: A request object that contains args with keys: email, token

    Returns:
        (json): Http 200 string response

    Raises:
        Http 400 when the json is missing required keys: email, token
        or if the token is not valid
    """
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
    # TODO Add tuple to response

    # TODO uncomment once db is implemented

    account_db = Database("accounts")
    try:
        account_db.delete(args["email"])
        return http200("Account deleted")
    except:
        return http400("Error in account deletion")


def profile_post(request):
    """Handles the profile picture POST endpoint
    Validates data sent in a request then calls gcs to save photo

    Args:
        request: A request object that contains a json object with keys: email, token and a file in request.files

    Returns:
        Http 200 string response

    Raises:
        Http 400 when the json is missing a key
    """
    fields = ["email", "token", "file", "filename"]
    body = None

    try:
        body = request.form
    except:
        return http400("Missing body")

    body_validation = validate_body(body, fields)

    # check that body validation succeeded
    if body_validation[1] != 200:
        return http400("Problem Validating Request")

    auth = azure_refresh_token(body["token"])
    if not auth[0]:
        return http400("Not Authenticated")

    profile_storage = Storage("biit_profiles")
    file_decode = base64.b64decode(body["file"])
    try:
        profile_storage.add(file_decode, body["filename"])
    except:
        return http400("File was unable to be uploaded")

    response = {
        "access_token": auth[0],
        "refresh_token": auth[1],
    }
    return jsonHttp200("File Uploaded", response)


def profile_get(request):
    """Handles the profile picture GET endpoint
    Validates data sent in a request then calls the gcs to get the photo

    Args:
        request: A request object that contains args with keys: email and file

    Returns:
        (File) The Data of the file is returned

    Raises:
        Http 400 when the json is missing a key or the fils is not found
    """
    fields = ["email", "filename"]

    # serializes the quert string to a dict (neeto)
    args = request.args

    query_validation = validate_query_params(args, fields)
    # check that body validation succeeded
    if query_validation[1] != 200 or not validate_photo(args["filename"]):
        return query_validation

    profile_storage = Storage("biit_profiles")

    try:
        ret_file = profile_storage.get(args["filename"])
        response = {"data": ret_file}
        return jsonHttp200("File Received", response)
    except:
        return http400("File not found")
