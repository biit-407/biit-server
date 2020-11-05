import ast
from biit_server.authentication import AuthenticatedType, authenticated

from .http_responses import http200, http400, http500, jsonHttp200
from .query_helper import (
    ValidateType,
    validate_fields,
    validate_update_field,
)
from .database import Database
from .storage import Storage
from .utils import send_discord_message, utcToInt
from flask import send_file
import base64
import json


@validate_fields(["fname", "lname", "email", "token"], AuthenticatedType.BODY)
@authenticated(AuthenticatedType.BODY)
def account_post(request, auth):
    """Handles the account POST endpoint
    Validates data sent in a request then calls the database to add an account

    Args:
        request: A request object that contains a json object with keys: fname, lname, email

    Returns:
        Http 200 string response

    Raises:
        Http 400 when the json is missing a key
    """
    body = request.get_json()

    account_db = Database("accounts")

    try:
        db_entry = {
            "fname": body["fname"],
            "lname": body["lname"],
            "email": body["email"],
        }

        account_db.add(db_entry, id=body["email"])
    except:
        send_discord_message(
            f'Attempted to create an account with existing email: {body["email"]} with args [{body}]'
        )
        return http400("Email already taken")

    response = {
        "fname": body["fname"],
        "lname": body["lname"],
        "email": body["email"],
        "access_token": auth[0],
        "refresh_token": auth[1],
    }

    return jsonHttp200("Account Created", response)


@validate_fields(["email", "token"], ValidateType.QUERY)
@authenticated(AuthenticatedType.QUERY)
def account_get(request, auth):
    """Handles the account GET endpoint
    Validates data sent in a request then calls the database to get the row of the associated account

    Args:
        request: A request object that contains args with keys: email

    Returns:
        (json) Http 200 string response with the associated account information

    Raises:
        Http 400 when the json is missing a key
    """
    args = request.args

    account_db = Database("accounts")

    try:
        response = {
            "access_token": auth[0],
            "refresh_token": auth[1],
            "data": account_db.get(args["email"]).to_dict(),
        }
        return jsonHttp200("Account returned", response)
    except:
        send_discord_message(f"Account with email [{args['email']}] does not exist")
        return http400("Account not found")


@validate_fields(["email", "token", "updateFields"], ValidateType.QUERY)
@authenticated(AuthenticatedType.QUERY)
def account_put(request, auth):
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
    valid_updates = [
        "age",
        "agePref",
        "covid",
        "email",
        "fname",
        "lname",
        "meetType",
        "opt-in",
        "schedule",
        "birthday",
    ]

    # serializes the quert string to a dict (neeto)
    args = request.args

    update_validation = validate_update_field(args, valid_updates)
    if update_validation[1] != 200:
        send_discord_message(
            f'Error updating account [{args["email"]}]: {update_validation[0]}'
        )
        return update_validation

    account_db = Database("accounts")

    if "schedule" in args["updateFields"]:
        temp_schedule = [
            [int(item[0]), int(item[1])]
            for item in ast.literal_eval(args["updateFields"])["schedule"]
        ]
        schedule = utcToInt(temp_schedule)
        account_db.update(args["email"], {"schedule": schedule})

    try:
        account_db.update(args["email"], ast.literal_eval(args["updateFields"]))
        response = {
            "access_token": auth[0],
            "refresh_token": auth[1],
        }
        response.update(account_db.get(args["email"]).to_dict())

        return jsonHttp200("Account Updated", response)
    except:
        send_discord_message(
            f'`account_db.update` failed with account [{args["email"]}] and updateFields [{args["updateFields"]}]'
        )
        return http500("Account update error")


@validate_fields(["email", "token"], ValidateType.QUERY)
@authenticated(AuthenticatedType.QUERY)
def account_delete(request, auth):
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
    args = request.args

    account_db = Database("accounts")
    storage = Storage("biit_profiles")
    try:
        account_db.delete(args["email"])
        storage.delete(args["email"] + ".jpg")
        return http200("Account deleted")
    except:
        send_discord_message(
            f'Error deleting account [{args["email"]}] with parameters [{args}]'
        )
        return http500("Error in account deletion")


@validate_fields(["email", "token", "file", "filename"], ValidateType.FORM)
@authenticated(AuthenticatedType.FORM)
def profile_post(request, auth):
    """Handles the profile picture POST endpoint
    Validates data sent in a request then calls gcs to save photo

    Args:
        request: A request object that contains a json object with keys: email, token and a file in request.files

    Returns:
        Http 200 string response

    Raises:
        Http 400 when the json is missing a key
    """
    body = request.form

    profile_storage = Storage("biit_profiles")
    file_decode = base64.b64decode(body["file"])
    try:
        profile_storage.add(file_decode, body["filename"])
    except:
        send_discord_message(
            f'Unable to upload file [{body["filename"]}] for account [{body["email"]}]'
        )
        return http500("File was unable to be uploaded")

    response = {
        "access_token": auth[0],
        "refresh_token": auth[1],
    }
    return jsonHttp200("File Uploaded", response)


@validate_fields(["email", "token", "filename"], ValidateType.QUERY)
@authenticated(AuthenticatedType.QUERY)
def profile_get(request, auth):
    """Handles the profile picture GET endpoint
    Validates data sent in a request then calls the gcs to get the photo

    Args:
        request: A request object that contains args with keys: email and file

    Returns:
        (File) The Data of the file is returned

    Raises:
        Http 400 when the json is missing a key or the fils is not found
    """
    args = request.args

    profile_storage = Storage("biit_profiles")

    try:
        response = {
            "data": profile_storage.get(args["filename"]),
            "access_token": auth[0],
            "refresh_token": auth[1],
        }

        return jsonHttp200("File Received", response)
    except:
        send_discord_message(
            f'Profile image does not exist for account [{args["email"]}]'
        )
        return http400("File not found")
