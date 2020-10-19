import ast

from flask.globals import request

from .http_responses import http200, http400, jsonHttp200
from .query_helper import (
    validate_body,
    validate_query_params,
    validate_photo,
    validate_update_field,
)
from .azure import azure_refresh_token
from .database import Database
from .storage import Storage
from flask import send_file
import base64


def meeting_accept(request, id):
    return NotImplementedError


def meeting_decline(request, id):
    return NotImplementedError
